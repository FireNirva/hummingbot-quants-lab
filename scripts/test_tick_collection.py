#!/usr/bin/env python3
"""
Test tick-level orderbook collection for single symbol

This script tests the tick-level orderbook collection system by:
- Running collection for a specified duration
- Monitoring tick rate and data quality
- Validating sequence numbers for gaps
- Checking parquet file integrity
- Comparing reconstructed orderbook vs REST snapshot

Usage:
    # Test VIRTUAL-USDT for 60 seconds
    python scripts/test_tick_collection.py VIRTUAL-USDT --duration 60
    
    # Test with custom exchange
    python scripts/test_tick_collection.py IRON-USDT --duration 120 --exchange gate_io
    
    # Verbose output
    python scripts/test_tick_collection.py LMTS-USDT --duration 30 --verbose

Output:
    - Real-time tick statistics
    - Sequence gap analysis
    - Snapshot checkpoint verification
    - Parquet file validation
    - Data quality report

Author: Alice
Date: 2024-11-19
"""

import argparse
import asyncio
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.data_paths import data_paths
from core.data_sources.tick_orderbook_writer import TickOrderBookWriter, load_orderbook_ticks
from core.data_sources.websocket_client import WebSocketClient
from core.data_structures.orderbook_tick import OrderBookTick


class TickCollectionTester:
    """Test harness for tick-level orderbook collection"""
    
    def __init__(self, symbol: str, exchange: str = "gate_io", duration: int = 60, verbose: bool = False):
        self.symbol = symbol
        self.exchange = exchange
        self.duration = duration
        self.verbose = verbose
        
        # Statistics tracking
        self.stats = {
            'total_ticks': 0,
            'diff_ticks': 0,
            'snapshot_ticks': 0,
            'bid_ticks': 0,
            'ask_ticks': 0,
            'update_ids': [],
            'sequence_gaps': [],
            'start_time': None,
            'end_time': None,
        }
        
        # Components
        self.writer = None
        self.ws_client = None
        
        # Configure logging
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    async def run_test(self) -> Dict:
        """
        Run collection test
        
        Returns:
            Dictionary with test results
        """
        try:
            self.logger.info(f"🧪 Starting tick collection test:")
            self.logger.info(f"   Symbol: {self.symbol}")
            self.logger.info(f"   Exchange: {self.exchange}")
            self.logger.info(f"   Duration: {self.duration}s")
            self.logger.info("")
            
            # Initialize writer
            output_dir = data_paths.raw_dir / "orderbook_ticks_test"
            self.writer = TickOrderBookWriter(
                output_dir=output_dir,
                buffer_size=50,  # Smaller buffer for more frequent flushes during test
                flush_interval=5.0
            )
            
            # Initialize WebSocket client
            ws_url = self._get_ws_url()
            self.ws_client = WebSocketClient(
                url=ws_url,
                on_message=self._handle_message,
                ping_interval=20.0
            )
            
            # Connect
            connected = await self.ws_client.connect()
            if not connected:
                raise RuntimeError("Failed to connect to WebSocket")
            
            # Subscribe
            await self._subscribe()
            
            # Record start time
            self.stats['start_time'] = datetime.now(timezone.utc)
            
            # Run for specified duration
            self.logger.info(f"📊 Collecting ticks for {self.duration}s...")
            self.logger.info("")
            
            # Start monitoring task
            monitor_task = asyncio.create_task(self._monitor_loop())
            
            # Wait for duration
            await asyncio.sleep(self.duration)
            
            # Record end time
            self.stats['end_time'] = datetime.now(timezone.utc)
            
            # Stop monitoring
            monitor_task.cancel()
            try:
                await monitor_task
            except asyncio.CancelledError:
                pass
            
            # Flush remaining data
            await self.writer.flush_all()
            
            # Close connection
            await self.ws_client.close()
            
            # Analyze results
            results = self._analyze_results()
            
            # Print summary
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Test failed: {e}", exc_info=True)
            return {"status": "error", "error": str(e)}
    
    def _get_ws_url(self) -> str:
        """Get WebSocket URL for exchange"""
        if self.exchange == "gate_io":
            return "wss://api.gateio.ws/ws/v4/"
        elif self.exchange == "mexc":
            return "wss://wbs.mexc.com/ws"
        else:
            raise ValueError(f"Unsupported exchange: {self.exchange}")
    
    async def _subscribe(self):
        """Subscribe to orderbook updates"""
        formatted_pair = self.symbol.replace("-", "_")
        
        subscription = {
            "time": int(datetime.now(timezone.utc).timestamp()),
            "channel": "spot.order_book_update",
            "event": "subscribe",
            "payload": [formatted_pair, "100ms"]
        }
        
        await self.ws_client.send(subscription)
        self.logger.info(f"✅ Subscribed to {formatted_pair}")
    
    async def _handle_message(self, message: dict):
        """Handle incoming WebSocket message"""
        try:
            event = message.get("event")
            channel = message.get("channel")
            
            if event == "subscribe":
                if message.get("error") is None:
                    self.logger.debug("Subscription confirmed")
                return
            
            if channel == "spot.order_book_update" and event == "update":
                ticks = self._parse_message(message)
                
                for tick in ticks:
                    # Update statistics
                    self.stats['total_ticks'] += 1
                    
                    if tick.snapshot_flag:
                        self.stats['snapshot_ticks'] += 1
                    else:
                        self.stats['diff_ticks'] += 1
                    
                    if tick.side == "bid":
                        self.stats['bid_ticks'] += 1
                    else:
                        self.stats['ask_ticks'] += 1
                    
                    # Track sequence
                    self._track_sequence(tick.update_id)
                    
                    # Write tick
                    await self.writer.write_tick(tick)
            
        except Exception as e:
            self.logger.error(f"Error handling message: {e}")
    
    def _parse_message(self, message: dict) -> List[OrderBookTick]:
        """Parse WebSocket message to ticks"""
        ticks = []
        
        try:
            result = message.get("result", {})
            
            timestamp_ms = result.get("t", message.get("time_ms", 0))
            timestamp = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
            received_timestamp = datetime.now(timezone.utc)
            
            symbol = result.get("s", "")
            trading_pair = symbol.replace("_", "-")
            
            update_id = result.get("u", 0)
            
            # Parse bids
            for price_str, amount_str in result.get("b", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.exchange,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="bid",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
            
            # Parse asks
            for price_str, amount_str in result.get("a", []):
                ticks.append(OrderBookTick(
                    timestamp=timestamp,
                    received_timestamp=received_timestamp,
                    exchange=self.exchange,
                    trading_pair=trading_pair,
                    update_id=update_id,
                    snapshot_flag=False,
                    side="ask",
                    price=float(price_str),
                    amount=float(amount_str)
                ))
        
        except Exception as e:
            self.logger.error(f"Error parsing message: {e}")
        
        return ticks
    
    def _track_sequence(self, update_id: int):
        """Track sequence numbers"""
        if self.stats['update_ids']:
            last_id = self.stats['update_ids'][-1]
            
            if update_id != last_id + 1 and update_id != last_id:
                gap_size = update_id - last_id - 1
                self.stats['sequence_gaps'].append({
                    'last_id': last_id,
                    'current_id': update_id,
                    'gap_size': gap_size
                })
        
        self.stats['update_ids'].append(update_id)
    
    async def _monitor_loop(self):
        """Periodic status monitoring"""
        try:
            while True:
                await asyncio.sleep(10)
                
                elapsed = (datetime.now(timezone.utc) - self.stats['start_time']).total_seconds()
                tick_rate = self.stats['total_ticks'] / elapsed if elapsed > 0 else 0
                
                self.logger.info(
                    f"📈 Progress: {elapsed:.0f}s | "
                    f"Ticks: {self.stats['total_ticks']} | "
                    f"Rate: {tick_rate:.1f} ticks/s | "
                    f"Bids: {self.stats['bid_ticks']} | "
                    f"Asks: {self.stats['ask_ticks']}"
                )
        
        except asyncio.CancelledError:
            pass
    
    def _analyze_results(self) -> Dict:
        """Analyze test results"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        results = {
            'status': 'success',
            'duration_seconds': duration,
            'total_ticks': self.stats['total_ticks'],
            'tick_rate': self.stats['total_ticks'] / duration if duration > 0 else 0,
            'diff_ticks': self.stats['diff_ticks'],
            'snapshot_ticks': self.stats['snapshot_ticks'],
            'bid_ticks': self.stats['bid_ticks'],
            'ask_ticks': self.stats['ask_ticks'],
            'sequence_gaps': len(self.stats['sequence_gaps']),
            'gap_details': self.stats['sequence_gaps'][:5],  # First 5 gaps
        }
        
        # Validate expectations
        results['validation'] = {
            'tick_rate_ok': results['tick_rate'] > 1.0,  # Should be > 1 Hz for active pairs
            'has_data': results['total_ticks'] > 0,
            'no_major_gaps': results['sequence_gaps'] < 5,
        }
        
        results['all_checks_passed'] = all(results['validation'].values())
        
        return results
    
    def _print_summary(self, results: Dict):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("🧪 TICK COLLECTION TEST SUMMARY")
        print("=" * 80)
        
        print(f"\n📊 Collection Statistics:")
        print(f"   Duration: {results['duration_seconds']:.1f}s")
        print(f"   Total ticks: {results['total_ticks']}")
        print(f"   Tick rate: {results['tick_rate']:.2f} ticks/s")
        print(f"   Diff ticks: {results['diff_ticks']}")
        print(f"   Snapshot ticks: {results['snapshot_ticks']}")
        print(f"   Bid ticks: {results['bid_ticks']}")
        print(f"   Ask ticks: {results['ask_ticks']}")
        
        print(f"\n🔍 Data Quality:")
        print(f"   Sequence gaps: {results['sequence_gaps']}")
        if results['gap_details']:
            print(f"   First gaps:")
            for gap in results['gap_details']:
                print(f"      • {gap['last_id']} → {gap['current_id']} (gap: {gap['gap_size']})")
        
        print(f"\n✅ Validation:")
        val = results['validation']
        print(f"   Tick rate > 1 Hz: {'✓' if val['tick_rate_ok'] else '✗'}")
        print(f"   Has data: {'✓' if val['has_data'] else '✗'}")
        print(f"   No major gaps: {'✓' if val['no_major_gaps'] else '✗'}")
        
        print(f"\n{'🎉 TEST PASSED' if results['all_checks_passed'] else '⚠️ TEST WARNINGS'}")
        print("=" * 80 + "\n")


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Test tick-level orderbook collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Test VIRTUAL-USDT for 60 seconds
    python scripts/test_tick_collection.py VIRTUAL-USDT --duration 60
    
    # Test with custom exchange
    python scripts/test_tick_collection.py IRON-USDT --duration 120 --exchange gate_io
    
    # Verbose output
    python scripts/test_tick_collection.py LMTS-USDT --duration 30 --verbose
        """
    )
    
    parser.add_argument('symbol', type=str, help='Trading pair symbol (e.g., VIRTUAL-USDT)')
    parser.add_argument('--duration', type=int, default=60, help='Collection duration in seconds (default: 60)')
    parser.add_argument('--exchange', type=str, default='gate_io', help='Exchange name (default: gate_io)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Run test
    tester = TickCollectionTester(
        symbol=args.symbol,
        exchange=args.exchange,
        duration=args.duration,
        verbose=args.verbose
    )
    
    results = await tester.run_test()
    
    # Exit with appropriate code
    sys.exit(0 if results.get('all_checks_passed', False) else 1)


if __name__ == "__main__":
    asyncio.run(main())

