"""
Tick-level orderbook data collection via WebSocket

This task collects real-time orderbook updates from exchanges via WebSocket,
storing both incremental diffs and periodic full snapshots for reconstruction.

Features:
- WebSocket streaming for low-latency tick data
- Long-table format (one row per price level change)
- Periodic REST snapshot checkpoints every N minutes
- Sequence number tracking for gap detection
- Buffered writing with automatic flush

Author: Alice  
Date: 2024-11-19
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import aiohttp

from core.data_paths import data_paths
from core.data_sources.tick_orderbook_writer import TickOrderBookWriter
from core.data_sources.websocket_client import WebSocketClient
from core.data_structures.orderbook_tick import OrderBookTick
from core.tasks import BaseTask, TaskContext
from core.monitoring.metrics import get_metrics
from core.monitoring.exporter import get_exporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrderBookTickCollector(BaseTask):
    """
    Collect tick-level orderbook updates via WebSocket
    
    Gate.io WebSocket API:
    - Endpoint: wss://api.gateio.ws/ws/v4/
    - Channel: spot.order_book_update
    - Documentation: https://www.gate.io/docs/developers/apiv4/ws/en/
    
    IMPORTANT: Field names follow Gate.io v4 WebSocket specification.
    Do NOT use Binance-style field names.
    
    Configuration example:
    ```yaml
    tasks:
      orderbook_tick_gateio:
        enabled: true
        task_class: app.tasks.data_collection.orderbook_tick_collector.OrderBookTickCollector
        
        schedule:
          type: continuous  # Long-running streaming task
        
        config:
          connector_name: "gate_io"
          trading_pairs:
            - "VIRTUAL-USDT"
            - "IRON-USDT"
          depth_limit: 100
          snapshot_interval: 300  # Full snapshot every 5 minutes
          buffer_size: 100
          flush_interval: 10.0
    ```
    
    Task Lifecycle:
    - Unlike periodic snapshot tasks, this runs continuously
    - execute() method streams indefinitely until cancelled
    - Internal reconnect/retry logic handles transient failures
    - Only returns on fatal errors or explicit cancellation
    """
    
    def __init__(self, config):
        super().__init__(config)
        
        # Configuration parameters
        task_config = self.config.config
        self.connector_name = task_config["connector_name"]
        self.trading_pairs = task_config.get("trading_pairs", [])
        self.depth_limit = task_config.get("depth_limit", 100)
        self.snapshot_interval = task_config.get("snapshot_interval", 300)  # 5 minutes
        self.buffer_size = task_config.get("buffer_size", 100)
        self.flush_interval = task_config.get("flush_interval", 10.0)
        self.gap_warning_threshold = task_config.get("gap_warning_threshold", 50)  # Warn only for gaps > 50
        
        # Initialize components
        self.ws_client: Optional[WebSocketClient] = None
        self.writer: Optional[TickOrderBookWriter] = None
        
        # Track per-symbol state
        self.last_snapshot_time: Dict[str, float] = {}
        self.update_id_tracker: Dict[str, int] = {}  # Track sequence per symbol
        
        # Initialize Prometheus metrics
        self.metrics = get_metrics()
        
        # Initialize metrics exporter (only once globally)
        # The exporter runs in a separate thread and exposes /metrics endpoint
        self.exporter = get_exporter(port=8000)
        
        logger.info("OrderBookTickCollector initialized")
        logger.info(f"  Connector: {self.connector_name}")
        logger.info(f"  Trading pairs: {len(self.trading_pairs)}")
        logger.info(f"  Snapshot interval: {self.snapshot_interval}s")
        logger.info(f"  Buffer size: {self.buffer_size} ticks")
        logger.info(f"  Gap warning threshold: >{self.gap_warning_threshold}")
        logger.info(f"  📊 Metrics exporter: http://localhost:8000/metrics")
    
    async def setup(self, context: TaskContext) -> None:
        """Initialize WebSocket client and writer"""
        try:
            await super().setup(context)
            
            # Initialize tick writer (with metrics support)
            output_dir = data_paths.raw_dir / "orderbook_ticks"
            self.writer = TickOrderBookWriter(
                output_dir=output_dir,
                buffer_size=self.buffer_size,
                flush_interval=self.flush_interval,
                metrics=self.metrics  # Pass metrics for flush monitoring
            )
            
            # Initialize WebSocket client
            ws_url = self._get_websocket_url()
            ws_format = "protobuf" if self.connector_name == "mexc" else "json"
            self.ws_client = WebSocketClient(
                url=ws_url,
                on_message=self._handle_message,
                ping_interval=20.0,
                ping_timeout=10.0,
                format=ws_format
            )
            
            logger.info(f"Setup complete: WebSocket URL={ws_url}")
            
        except Exception as e:
            logger.error(f"Setup failed: {e}", exc_info=True)
            raise
    
    def _get_websocket_url(self) -> str:
        """Get WebSocket URL for the exchange"""
        if self.connector_name == "gate_io":
            return "wss://api.gateio.ws/ws/v4/"
        elif self.connector_name == "mexc":
            # MEXC 官方 WebSocket 端点（需要 protobuf 支持）
            return "wss://wbs-api.mexc.com/ws"
        else:
            raise ValueError(f"Unsupported exchange: {self.connector_name}")
    
    def _get_rest_url(self) -> str:
        """Get REST API base URL for the exchange"""
        if self.connector_name == "gate_io":
            return "https://api.gateio.ws/api/v4"
        elif self.connector_name == "mexc":
            return "https://api.mexc.com/api/v3"
        else:
            raise ValueError(f"Unsupported exchange: {self.connector_name}")
    
    async def execute(self, context: TaskContext) -> Dict[str, Any]:
        """
        Main execution: connect and stream indefinitely
        
        TASK LIFECYCLE CLARIFICATION:
        - This is a long-running streaming task (unlike periodic snapshot task)
        - execute() method runs continuously until task is cancelled/stopped
        - Scheduler must support this pattern (continuous streaming)
        - Internal reconnect/retry logic handles transient failures
        - Only returns on fatal errors or explicit cancellation
        
        Flow:
        1. Connect to WebSocket
        2. Subscribe to order_book_update for all trading pairs
        3. Fetch initial full snapshots via REST
        4. Stream diffs, write to buffer
        5. Periodically fetch full snapshot as checkpoint
        """
        try:
            # Connect to WebSocket
            connected = await self.ws_client.connect()
            if not connected:
                # Record disconnection
                for pair in self.trading_pairs:
                    self.metrics.set_connection_status(self.connector_name, pair, 0)
                    self.metrics.record_disconnection(self.connector_name, pair, "initial_connection_failed")
                raise RuntimeError("Failed to establish WebSocket connection")
            
            # Record successful connection
            for pair in self.trading_pairs:
                self.metrics.set_connection_status(self.connector_name, pair, 1)
            logger.info(f"✅ WebSocket connected for {len(self.trading_pairs)} pairs")
            
            # Subscribe to all pairs
            await self._subscribe_all_pairs()
            
            # Fetch initial snapshots for all pairs
            await self._fetch_initial_snapshots()
            
            # Stream loop (runs until task cancelled)
            await self._stream_loop()
            
            return {"status": "stopped", "reason": "stream_loop_exited"}
            
        except asyncio.CancelledError:
            logger.info("Task cancelled, shutting down gracefully")
            # Mark all as disconnected
            for pair in self.trading_pairs:
                self.metrics.set_connection_status(self.connector_name, pair, 0)
            return {"status": "cancelled"}
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}", exc_info=True)
            # Record disconnection and failure
            for pair in self.trading_pairs:
                self.metrics.set_connection_status(self.connector_name, pair, 0)
                self.metrics.record_disconnection(self.connector_name, pair, "execution_error")
            return {"status": "error", "error": str(e)}
    
    async def _subscribe_all_pairs(self):
        """Subscribe to orderbook updates for all trading pairs"""
        for pair in self.trading_pairs:
            formatted_pair = self._format_pair_for_websocket(pair)
            
            if self.connector_name == "gate_io":
                # Gate.io subscription format
                subscription = {
                    "time": int(datetime.now(timezone.utc).timestamp()),
                    "channel": "spot.order_book_update",
                    "event": "subscribe",
                    "payload": [formatted_pair, "100ms"]  # Update frequency: 100ms
                }
            elif self.connector_name == "mexc":
                # MEXC subscription format（官方文档格式）
                # 注意：MEXC 使用 protobuf 格式推送数据，需要特殊处理
                # 增量深度更新（推荐）- 需要 protobuf 支持
                subscription = {
                    "method": "SUBSCRIPTION",
                    "params": [
                        f"spot@public.aggre.depth.v3.api.pb@100ms@{formatted_pair}"
                    ]
                }
                # 备选：限量深度快照（JSON 格式）
                # f"spot@public.limit.depth.v3.api@{formatted_pair}@20"
            else:
                logger.error(f"Unsupported exchange for subscription: {self.connector_name}")
                continue
            
            await self.ws_client.send(subscription)
            logger.info(f"Subscribed to {formatted_pair} orderbook updates ({self.connector_name})")
    
    def _format_pair(self, pair: str) -> str:
        """Format trading pair for exchange API"""
        if self.connector_name == "gate_io":
            # Gate.io uses underscore: BTC_USDT
            return pair.replace("-", "_")
        elif self.connector_name == "mexc":
            # MEXC uses no separator: BTCUSDT
            return pair.replace("-", "")
        return pair
    
    def _format_pair_for_websocket(self, pair: str) -> str:
        """Format trading pair specifically for WebSocket subscription"""
        if self.connector_name == "gate_io":
            return pair.replace("-", "_")  # BTC_USDT
        elif self.connector_name == "mexc":
            return pair.replace("-", "")  # BTCUSDT
        return pair
    
    async def _fetch_initial_snapshots(self):
        """Fetch initial full snapshots for all pairs via REST"""
        logger.info(f"Fetching initial snapshots for {len(self.trading_pairs)} pairs...")
        
        tasks = []
        for pair in self.trading_pairs:
            tasks.append(self._fetch_snapshot_checkpoint(pair))
        
        await asyncio.gather(*tasks, return_exceptions=True)
        
        logger.info("Initial snapshots fetched")
    
    async def _stream_loop(self):
        """
        Main streaming loop
        
        Continuously checks snapshot intervals while WebSocket
        message_loop handles incoming updates
        """
        try:
            while self.ws_client.is_connected():
                # Check if any pair needs snapshot checkpoint
                current_time = asyncio.get_event_loop().time()
                
                for pair in self.trading_pairs:
                    last_snapshot = self.last_snapshot_time.get(pair, 0)
                    time_since_snapshot = current_time - last_snapshot
                    
                    if time_since_snapshot >= self.snapshot_interval:
                        await self._fetch_snapshot_checkpoint(pair)
                
                # Update buffer size metrics for all pairs
                buffer_sizes = self.writer.get_buffer_sizes()
                for (exchange, symbol), size in buffer_sizes.items():
                    self.metrics.set_buffer_size(exchange, symbol, size)
                
                # Sleep before next check
                await asyncio.sleep(10)
                
        except Exception as e:
            logger.error(f"Stream loop error: {e}", exc_info=True)
            raise
    
    async def _handle_message(self, message: dict):
        """
        Process incoming WebSocket message
        
        Supports both Gate.io (JSON) and MEXC (Protobuf) formats.
        Convert to OrderBookTick (long-table: one row per price level)
        """
        start_time = time.time()
        trading_pair = None
        ticks = None  # Initialize ticks variable
        message_type = None
        
        try:
            # Debug: Log MEXC messages to understand format
            if self.connector_name == "mexc" and message:
                # Log first few messages to understand structure
                logger.debug(f"MEXC message keys: {list(message.keys())}")
                if "publicincreasedepths" in message or "publiclimitdepths" in message:
                    logger.info(f"📨 MEXC diff message received: {message.get('symbol', 'unknown')}")
            
            # Check message type
            event = message.get("event")
            channel = message.get("channel")
            
            # Handle subscription confirmation (both exchanges)
            if event == "subscribe" or message.get("code") == 0:
                if message.get("error") is None:
                    # Only log if there's meaningful content
                    msg_content = channel or message.get('msg')
                    if msg_content and msg_content != "method is empty.":
                        logger.info(f"Subscription confirmed: {msg_content}")
                    else:
                        # Ignore empty or irrelevant messages
                        logger.debug(f"Received empty confirmation message: {message}")
                else:
                    logger.error(f"Subscription error: {message}")
                return
            
            # Route to appropriate parser based on connector
            if self.connector_name == "gate_io":
                # Gate.io format
                if channel == "spot.order_book_update" and event == "update":
                    ticks = self._parse_gateio_message(message)
                    message_type = "diff"
                else:
                    return
            elif self.connector_name == "mexc":
                # MEXC format (protobuf parsed to dict)
                logger.debug(f"📦 MEXC message: event={event}, has_result={'result' in message}")
                if event == "update":
                    ticks = self._parse_mexc_message(message)
                    message_type = "diff"
                    tick_count = len(ticks) if ticks else 0
                    logger.info(f"📨 MEXC diff parsed: {tick_count} ticks, ticks_type={type(ticks)}, ticks_bool={bool(ticks)}")
                    if ticks and len(ticks) > 0:
                        logger.info(f"   First tick: pair={ticks[0].trading_pair}, price={ticks[0].price}")
                else:
                    logger.debug(f"⚠️  MEXC message skipped: event={event}")
                    return
            else:
                logger.warning(f"Unknown connector: {self.connector_name}")
                return
            
            logger.info(f"🚦 About to check ticks: ticks={ticks is not None}, bool(ticks)={bool(ticks) if ticks is not None else 'None'}, len={len(ticks) if ticks else 'N/A'}")
            if ticks:
                trading_pair = ticks[0].trading_pair
                logger.info(f"🔧 Processing {len(ticks)} ticks for {trading_pair}, exchange={self.connector_name}")
                
                # Record message received
                self.metrics.increment_messages_received(self.connector_name, trading_pair, message_type)
                logger.info(f"✅ Metrics recorded: messages_received for {self.connector_name}/{trading_pair}")
                
                # Write all ticks to buffer
                for tick in ticks:
                    await self.writer.write_tick(tick)
                
                # Record ticks written
                self.metrics.increment_ticks_written(self.connector_name, trading_pair, len(ticks))
                
                # Update last message timestamp
                self.metrics.update_last_message_time(self.connector_name, trading_pair, time.time())
                
                # Record processing latency
                processing_time = time.time() - start_time
                self.metrics.observe_processing_latency(self.connector_name, trading_pair, processing_time)
                
                # Record successful processing
                self.metrics.increment_messages_processed(self.connector_name, trading_pair)
                
                # Log sequence tracking
                first_tick = ticks[0]
                self._track_sequence(first_tick.trading_pair, first_tick.update_id)
            else:
                logger.warning(f"⚠️  No ticks generated from message (connector={self.connector_name})")
            
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)
            # Record failure
            if trading_pair:
                self.metrics.increment_messages_failed(self.connector_name, trading_pair, "processing_error")
            else:
                # If we don't know the pair, use a placeholder
                self.metrics.increment_messages_failed(self.connector_name, "unknown", "parse_error")
    
    def _parse_gateio_message(self, message: dict) -> List[OrderBookTick]:
        """
        Convert Gate.io WS message to list of OrderBookTick
        
        Gate.io spot.order_book_update format:
        {
            "time": 1606292218,
            "time_ms": 1606292218231,
            "channel": "spot.order_book_update",
            "event": "update",
            "result": {
                "t": 1606292218231,
                "e": "depthUpdate",
                "E": 1606292218,
                "s": "BTC_USDT",
                "U": 48776301,
                "u": 48776310,
                "b": [["10000.1", "0.1"], ["10000.2", "0.2"]],
                "a": [["10001.1", "0.1"], ["10001.2", "0.0"]]
            }
        }
        
        Returns one OrderBookTick per price level (long-table format)
        """
        ticks = []
        
        try:
            result = message.get("result", {})
            
            # Extract fields from Gate.io format
            timestamp_ms = result.get("t", message.get("time_ms", 0))
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            received_timestamp = datetime.now(timezone.utc)
            
            symbol = result.get("s", "")
            trading_pair = symbol.replace("_", "-")  # Convert back to QuantsLab format
            
            # Use end update_id (u) as the sequence number
            update_id = result.get("u", 0)
            
            # Parse bid updates
            for price_str, amount_str in result.get("b", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="bid",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
            
            # Parse ask updates
            for price_str, amount_str in result.get("a", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="ask",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
            
        except Exception as e:
            logger.error(f"Error parsing Gate.io message: {e}", exc_info=True)
        
        return ticks
    
    def _parse_mexc_message(self, message: dict) -> List[OrderBookTick]:
        """
        Convert MEXC protobuf message to list of OrderBookTick
        
        MEXC message format (after protobuf parsing):
        {
            "channel": "spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT",
            "symbol": "BTCUSDT",
            "sendtime": 1736411507002,
            "event": "update",
            "result": {
                "bids": [["92877.58", "0.00000000"], ...],
                "asks": [["93180.18", "0.21976424"], ...],
                "eventtype": "spot@public.aggre.depth.v3.api.pb@100ms",
                "fromVersion": "10589632359",
                "toVersion": "10589632359"
            }
        }
        
        Returns one OrderBookTick per price level (long-table format)
        """
        ticks = []
        
        try:
            result = message.get("result", {})
            
            # Extract metadata
            timestamp_ms = message.get("sendtime", 0)
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            received_timestamp = datetime.now(timezone.utc)
            
            symbol = message.get("symbol", "")
            # Convert MEXC format to QuantsLab format (BTCUSDT -> BTC-USDT)
            if symbol and len(symbol) > 4:
                # 简单处理：假设以USDT结尾
                if symbol.endswith("USDT"):
                    base = symbol[:-4]
                    trading_pair = f"{base}-USDT"
                else:
                    trading_pair = symbol
            else:
                trading_pair = symbol
            
            # Use toVersion as update_id (similar to Gate.io's u field)
            update_id = int(result.get("toVersion", "0"))
            
            # Parse bid updates
            for price_str, amount_str in result.get("bids", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="bid",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
            
            # Parse ask updates
            for price_str, amount_str in result.get("asks", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="ask",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
            
        except Exception as e:
            logger.error(f"Error parsing MEXC message: {e}", exc_info=True)
        
        return ticks
    
    def _track_sequence(self, trading_pair: str, update_id: int):
        """
        Track sequence numbers for gap detection
        
        Args:
            trading_pair: Trading pair
            update_id: Current update_id from message
        """
        last_id = self.update_id_tracker.get(trading_pair)
        
        if last_id is not None:
            # Check for gap
            if update_id != last_id + 1 and update_id != last_id:
                gap_size = update_id - last_id - 1
                
                # Record sequence gap in metrics
                self.metrics.record_sequence_gap(self.connector_name, trading_pair, gap_size)
                
                # Only warn for significant gaps (configurable threshold)
                # Small gaps are normal for active pairs due to WebSocket update merging
                if gap_size > self.gap_warning_threshold:
                    logger.warning(f"⚠️ Large sequence gap detected for {trading_pair}: "
                                 f"expected {last_id + 1}, got {update_id} (gap: {gap_size})")
                else:
                    # Log small gaps at debug level
                    logger.debug(f"Small gap for {trading_pair}: {gap_size}")
        
        self.update_id_tracker[trading_pair] = update_id
    
    async def _fetch_snapshot_checkpoint(self, trading_pair: str):
        """
        Fetch full orderbook via REST and write as snapshot ticks
        
        Reuses REST API from existing OrderBookSnapshotTask logic
        Converts to OrderBookTick with snapshot_flag=True (one row per level)
        """
        try:
            formatted_pair = self._format_pair(trading_pair)
            
            # Fetch orderbook via REST (exchange-specific)
            if self.connector_name == "gate_io":
                orderbook = await self._fetch_gateio_orderbook(formatted_pair)
            elif self.connector_name == "mexc":
                orderbook = await self._fetch_mexc_orderbook(formatted_pair)
            else:
                logger.error(f"Unsupported connector for REST snapshot: {self.connector_name}")
                return
            
            if not orderbook:
                logger.warning(f"Failed to fetch snapshot for {trading_pair}")
                self.metrics.increment_messages_failed(self.connector_name, trading_pair, "snapshot_fetch_failed")
                return
            
            # Extract data
            timestamp = datetime.now(timezone.utc)
            update_id = orderbook.get("id", 0)
            bids = orderbook.get("bids", [])[:self.depth_limit]
            asks = orderbook.get("asks", [])[:self.depth_limit]
            
            # Calculate aggregated metrics
            best_bid_price = float(bids[0][0]) if bids else None
            best_ask_price = float(asks[0][0]) if asks else None
            total_bid_volume = sum(float(b[1]) for b in bids) if bids else None
            total_ask_volume = sum(float(a[1]) for a in asks) if asks else None
            
            # Create snapshot ticks (one per level)
            ticks = []
            
            for price_str, amount_str in bids:
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=True,
                    side="bid",
                    price=float(price_str),
                    amount=float(amount_str),
                    best_bid_price=best_bid_price,
                    best_ask_price=best_ask_price,
                    total_bid_volume=total_bid_volume,
                    total_ask_volume=total_ask_volume
                ))
            
            for price_str, amount_str in asks:
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=timestamp,
                    exchange=self.connector_name,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=True,
                    side="ask",
                    price=float(price_str),
                    amount=float(amount_str),
                    best_bid_price=best_bid_price,
                    best_ask_price=best_ask_price,
                    total_bid_volume=total_bid_volume,
                    total_ask_volume=total_ask_volume
                ))
            
            # Write all snapshot ticks
            for tick in ticks:
                await self.writer.write_tick(tick)
            
            # Record snapshot metrics
            self.metrics.increment_messages_received(self.connector_name, trading_pair, "snapshot")
            self.metrics.increment_messages_processed(self.connector_name, trading_pair)
            self.metrics.increment_ticks_written(self.connector_name, trading_pair, len(ticks))
            
            # Update last snapshot time
            self.last_snapshot_time[trading_pair] = asyncio.get_event_loop().time()
            
            logger.info(f"✅ Snapshot checkpoint for {trading_pair}: "
                       f"{len(bids)} bids, {len(asks)} asks, update_id={update_id}")
            
        except Exception as e:
            logger.error(f"Error fetching snapshot checkpoint for {trading_pair}: {e}", exc_info=True)
    
    async def _fetch_gateio_orderbook(self, formatted_pair: str) -> Optional[Dict]:
        """
        Directly call Gate.io REST API to get orderbook (includes update_id)
        
        Args:
            formatted_pair: Trading pair in Gate.io format (e.g., "BTC_USDT")
        
        Returns:
            Orderbook data dict with 'id', 'bids', 'asks' fields
        """
        try:
            url = "https://api.gateio.ws/api/v4/spot/order_book"
            params = {
                "currency_pair": formatted_pair,
                "limit": self.depth_limit,
                "with_id": "true"  # Critical: returns update_id
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"Gate.io API error {response.status}: {text}")
                        return None
                    
                    data = await response.json()
                    
                    if 'id' not in data:
                        logger.warning(f"No 'id' field in response for {formatted_pair}")
                    
                    return data
                    
        except Exception as e:
            logger.error(f"Error fetching Gate.io orderbook for {formatted_pair}: {e}")
            return None
    
    async def _fetch_mexc_orderbook(self, formatted_pair: str) -> Optional[Dict]:
        """
        Call MEXC REST API to get orderbook
        
        Args:
            formatted_pair: Trading pair in MEXC format (e.g., "BTCUSDT")
        
        Returns:
            Orderbook data dict with 'lastUpdateId', 'bids', 'asks' fields
        """
        try:
            url = "https://api.mexc.com/api/v3/depth"
            params = {
                "symbol": formatted_pair,
                "limit": self.depth_limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        text = await response.text()
                        logger.error(f"MEXC API error {response.status}: {text}")
                        return None
                    
                    data = await response.json()
                    
                    # Convert MEXC format to our standard format
                    # MEXC uses 'lastUpdateId' instead of 'id'
                    return {
                        'id': data.get('lastUpdateId', 0),
                        'bids': data.get('bids', []),
                        'asks': data.get('asks', [])
                    }
                    
        except Exception as e:
            logger.error(f"Error fetching MEXC orderbook for {formatted_pair}: {e}")
            return None
    
    async def cleanup(self, context: TaskContext, result) -> None:
        """Graceful shutdown: flush buffer and close WebSocket"""
        try:
            logger.info("Cleaning up OrderBookTickCollector...")
            
            # Flush all buffered data
            if self.writer:
                await self.writer.flush_all()
                logger.info("All buffers flushed")
            
            # Close WebSocket connection
            if self.ws_client:
                await self.ws_client.close()
                logger.info("WebSocket connection closed")
            
            await super().cleanup(context, result)
            logger.info("Cleanup complete")
            
        except Exception as e:
            logger.warning(f"Cleanup error: {e}")

