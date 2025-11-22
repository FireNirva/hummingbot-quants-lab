"""
Minimal WebSocket client for exchange connections

This module provides a basic WebSocket client optimized for exchange orderbook streaming.
First version focuses on essential features:
- Basic connection and reconnection
- Message callback handling  
- Ping/pong keep-alive
- Graceful shutdown

Advanced features (deferred to future iterations):
- Exponential backoff
- Message queue buffering
- Connection health metrics
- Advanced error recovery
"""

import asyncio
import json
import logging
from typing import Callable, Optional
import websockets
from websockets.client import WebSocketClientProtocol

logger = logging.getLogger(__name__)

# Global protobuf module (loaded once at module level to avoid descriptor pool conflicts)
# Load immediately when this module is imported (not lazily)
_PROTOBUF_MODULE = None

try:
    from core.data_sources.mexc_proto import PushDataV3ApiWrapper_pb2
    _PROTOBUF_MODULE = PushDataV3ApiWrapper_pb2
    logger.info("✅ Protobuf module loaded at module import time")
except Exception as e:
    # If import fails, log but don't crash - protobuf is optional
    if "duplicate file name" in str(e):
        # Descriptor pool conflict - try to recover from sys.modules
        logger.warning("⚠️ Protobuf descriptor pool conflict detected during module import")
        import sys
        module_name = 'core.data_sources.mexc_proto.PushDataV3ApiWrapper_pb2'
        if module_name in sys.modules:
            _PROTOBUF_MODULE = sys.modules[module_name]
            logger.info("✅ Protobuf module recovered from sys.modules during module import")
        else:
            logger.error("❌ Protobuf module not available - descriptor pool conflict without module in sys.modules")
    else:
        logger.warning(f"⚠️ Protobuf module not available: {e}")

def _get_protobuf_module():
    """
    Get the globally loaded protobuf module
    
    Returns:
        The protobuf module, or None if not available
    """
    return _PROTOBUF_MODULE


class WebSocketClient:
    """
    Minimal WebSocket client for exchange connections
    
    Designed for streaming orderbook data from exchanges like Gate.io and MEXC.
    Handles connection lifecycle, message routing, and basic ping/pong keep-alive.
    
    Usage:
        async def on_message(msg: dict):
            print(f"Received: {msg}")
        
        client = WebSocketClient("wss://api.gateio.ws/ws/v4/", on_message)
        await client.connect()
        await client.send({"event": "subscribe", "channel": "spot.order_book_update"})
        
        # Client runs message loop automatically
        # Call close() for graceful shutdown
        await client.close()
    """
    
    def __init__(
        self,
        url: str,
        on_message: Callable,
        ping_interval: float = 20.0,
        ping_timeout: float = 10.0,
        format: str = "json"
    ):
        """
        Initialize WebSocket client
        
        Args:
            url: WebSocket endpoint URL
            on_message: Async callback function for incoming messages
            ping_interval: Seconds between ping messages (default: 20)
            ping_timeout: Timeout for pong response (default: 10)
            format: Message format - "json" (default) or "protobuf" (MEXC)
        """
        self.url = url
        self.on_message = on_message
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.format = format
        
        self.ws: Optional[WebSocketClientProtocol] = None
        self.running = False
        self._message_task: Optional[asyncio.Task] = None
        self._ping_task: Optional[asyncio.Task] = None
        
        # Get protobuf module if needed (uses module-level singleton)
        self.protobuf_module = None
        if format == "protobuf":
            self.protobuf_module = _get_protobuf_module()
            if self.protobuf_module is None:
                logger.warning("⚠️ Protobuf module not available - WebSocket will not work correctly")
        
        logger.info(f"WebSocketClient initialized: url={url}, format={format}")
    
    async def connect(self) -> bool:
        """
        Establish WebSocket connection with basic retry
        
        Returns:
            True if connection successful, False otherwise
            
        Note:
            First version uses simple retry logic. Advanced exponential
            backoff can be added in future iterations.
        """
        max_retries = 3
        retry_delay = 5.0
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Connecting to {self.url} (attempt {attempt}/{max_retries})")
                
                self.ws = await websockets.connect(
                    self.url,
                    ping_interval=None,  # We handle ping/pong manually
                    close_timeout=10
                )
                
                self.running = True
                
                # Start message loop and ping loop
                self._message_task = asyncio.create_task(self._message_loop())
                self._ping_task = asyncio.create_task(self._ping_loop())
                
                logger.info(f"✅ Connected to {self.url}")
                return True
                
            except Exception as e:
                logger.error(f"Connection failed (attempt {attempt}/{max_retries}): {e}")
                
                if attempt < max_retries:
                    logger.info(f"Retrying in {retry_delay}s...")
                    await asyncio.sleep(retry_delay)
                else:
                    logger.error(f"Failed to connect after {max_retries} attempts")
                    return False
        
        return False
    
    async def send(self, message: dict) -> bool:
        """
        Send JSON message to WebSocket
        
        Args:
            message: Dictionary to send as JSON
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.ws or not self.running:
            logger.error("Cannot send: not connected")
            return False
        
        try:
            await self.ws.send(json.dumps(message))
            logger.debug(f"Sent: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return False
    
    async def _message_loop(self):
        """
        Main message receiving loop
        
        Continuously receives and processes messages from WebSocket.
        Handles both JSON (Gate.io) and Protobuf (MEXC) formats.
        """
        try:
            while self.running and self.ws:
                try:
                    # Receive message with timeout
                    message_data = await asyncio.wait_for(
                        self.ws.recv(),
                        timeout=self.ping_interval + self.ping_timeout
                    )
                    
                    # Parse based on format
                    if self.format == "protobuf":
                        # MEXC protobuf format
                        message = await self._parse_protobuf(message_data)
                        if message is None:
                            continue
                    else:
                        # Standard JSON format (Gate.io)
                        try:
                            message = json.loads(message_data)
                        except json.JSONDecodeError:
                            logger.warning(f"Received non-JSON message: {str(message_data)[:100]}")
                            continue
                        
                        # Handle ping/pong protocol (Gate.io specific)
                        if message.get("event") == "ping":
                            await self._handle_ping(message)
                            continue
                    
                    # Route message to callback
                    try:
                        await self.on_message(message)
                    except Exception as e:
                        logger.error(f"Error in message callback: {e}", exc_info=True)
                    
                except asyncio.TimeoutError:
                    logger.warning("Message receive timeout - connection may be stale")
                    # For first version, just log and continue
                    # Future versions can implement reconnect logic here
                    continue
                    
                except websockets.exceptions.ConnectionClosed as e:
                    logger.warning(f"Connection closed: {e}")
                    self.running = False
                    break
                    
        except Exception as e:
            logger.error(f"Message loop error: {e}", exc_info=True)
        finally:
            logger.info("Message loop stopped")
    
    async def _ping_loop(self):
        """
        Periodic ping loop to keep connection alive
        
        Note: Some exchanges (like Gate.io) require responding to server pings
        rather than client-initiated pings. This method handles both patterns.
        """
        try:
            while self.running and self.ws:
                await asyncio.sleep(self.ping_interval)
                
                if not self.running or not self.ws:
                    break
                
                try:
                    # Send application-level ping (Gate.io style)
                    # Some exchanges expect {"event": "ping"}
                    # For standard WebSocket ping, we'd use: await self.ws.ping()
                    logger.debug("Sending ping")
                    await self.send({"event": "ping"})
                    
                except Exception as e:
                    logger.error(f"Ping failed: {e}")
                    # Connection likely dead, let message_loop handle it
                    break
                    
        except Exception as e:
            logger.error(f"Ping loop error: {e}", exc_info=True)
        finally:
            logger.info("Ping loop stopped")
    
    async def _parse_protobuf(self, data: bytes) -> Optional[dict]:
        """
        Parse MEXC protobuf message
        
        Args:
            data: Binary protobuf data
            
        Returns:
            Parsed message as dict, or None if parsing fails
        """
        # Check if protobuf module was loaded at init
        if self.protobuf_module is None:
            logger.error("Protobuf module not available")
            return None
        
        try:
            # First try to parse as JSON (for subscription responses)
            try:
                return json.loads(data)
            except:
                pass
            
            # Parse as protobuf
            wrapper = self.protobuf_module.PushDataV3ApiWrapper()
            wrapper.ParseFromString(data)
            
            # Convert to dict format similar to Gate.io
            message = {
                "channel": wrapper.channel,
                "symbol": wrapper.symbol,
                "sendtime": wrapper.sendTime,  # Note: capital T in sendTime
                "event": "update"  # Mark as update event
            }
            
            # Parse depth data - MEXC uses publicAggreDepths, not publicIncreaseDepths!
            if wrapper.HasField("publicAggreDepths"):
                depth = wrapper.publicAggreDepths
                result = {
                    "bids": [[level.price, level.quantity] for level in depth.bids],
                    "asks": [[level.price, level.quantity] for level in depth.asks],
                    "eventtype": depth.eventtype if hasattr(depth, 'eventtype') else "",
                    "fromVersion": depth.fromVersion if hasattr(depth, 'fromVersion') else "",
                    "toVersion": depth.toVersion if hasattr(depth, 'toVersion') else ""
                }
                message["result"] = result
                logger.debug(f"📦 MEXC protobuf parsed: {wrapper.symbol}, {len(depth.bids)} bids, {len(depth.asks)} asks")
            elif wrapper.HasField("publicIncreaseDepths"):
                # Fallback for incremental depth (if used)
                depth = wrapper.publicIncreaseDepths
                result = {
                    "bids": [[level.price, level.quantity] for level in depth.bids],
                    "asks": [[level.price, level.quantity] for level in depth.asks],
                    "eventtype": depth.eventtype,
                    "fromVersion": depth.fromVersion,
                    "toVersion": depth.toVersion
                }
                message["result"] = result
                logger.debug(f"📦 MEXC protobuf parsed (increase): {wrapper.symbol}, {len(depth.bids)} bids, {len(depth.asks)} asks")
            else:
                logger.debug(f"📦 MEXC protobuf has no depth data")
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to parse protobuf message: {e}")
            return None
    
    async def _handle_ping(self, message: dict):
        """
        Handle ping message from server
        
        Gate.io WebSocket protocol requires responding to server pings
        with a pong message containing the same payload.
        
        Args:
            message: Ping message from server
        """
        try:
            # Extract ping timestamp if present
            timestamp = message.get("time", message.get("t"))
            
            # Send pong response
            pong_message = {"event": "pong"}
            if timestamp:
                pong_message["time"] = timestamp
            
            await self.send(pong_message)
            logger.debug(f"Sent pong response")
            
        except Exception as e:
            logger.error(f"Failed to handle ping: {e}")
    
    async def close(self):
        """
        Gracefully close WebSocket connection
        
        Stops message loop, cancels tasks, and closes the connection.
        """
        logger.info("Closing WebSocket connection...")
        
        self.running = False
        
        # Cancel background tasks
        if self._message_task and not self._message_task.done():
            self._message_task.cancel()
            try:
                await self._message_task
            except asyncio.CancelledError:
                pass
        
        if self._ping_task and not self._ping_task.done():
            self._ping_task.cancel()
            try:
                await self._ping_task
            except asyncio.CancelledError:
                pass
        
        # Close WebSocket
        if self.ws:
            try:
                await self.ws.close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket: {e}")
            finally:
                self.ws = None
        
        logger.info("✅ WebSocket connection closed")
    
    def is_connected(self) -> bool:
        """
        Check if WebSocket is currently connected
        
        Returns:
            True if connected and running, False otherwise
        """
        if not self.running or self.ws is None:
            return False
        
        # Check connection state using the proper attribute
        # websockets library uses different attributes in different versions
        try:
            # Try modern websockets (>= 10.0) which uses state
            from websockets.protocol import State
            return self.ws.state == State.OPEN
        except (ImportError, AttributeError):
            # Fallback: check if we can access basic properties
            try:
                return hasattr(self.ws, 'open') and self.ws.open
            except:
                # Last resort: assume connected if object exists and running flag is True
                return True

