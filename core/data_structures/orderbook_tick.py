"""
Unified tick-level orderbook data structure

This module defines the schema for storing tick-level orderbook updates in long-table format.
Each tick represents a single price level change from either WebSocket diff updates or
periodic REST snapshot checkpoints.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import pyarrow as pa


@dataclass
class OrderBookTick:
    """
    Unified schema for tick-level orderbook data (long-table format)
    
    Each instance represents ONE price level change. A single WebSocket update
    affecting 10 price levels becomes 10 OrderBookTick instances.
    
    Design principles:
    - Long-table format for natural pandas/polars/pyarrow support
    - Explicit separation of diff updates (snapshot_flag=False) and full snapshots (snapshot_flag=True)
    - Sequence number (update_id) for ordering and gap detection
    - Latency tracking via timestamp vs received_timestamp
    - amount=0 indicates price level deletion
    
    Attributes:
        timestamp: Event timestamp from exchange (exchange server time)
        received_timestamp: Local receipt time (client time)
        exchange: Exchange identifier ("gate_io" or "mexc")
        trading_pair: Trading pair in QuantsLab format ("BTC-USDT")
        update_id: Sequence number from exchange for ordering and gap detection
        snapshot_flag: True for full snapshot checkpoints, False for incremental diffs
        side: "bid" or "ask"
        price: Price level
        amount: Amount at this price level (0 = delete this level)
        best_bid_price: Best bid price (only populated for snapshot_flag=True rows)
        best_ask_price: Best ask price (only populated for snapshot_flag=True rows)
        total_bid_volume: Total bid volume (only populated for snapshot_flag=True rows)
        total_ask_volume: Total ask volume (only populated for snapshot_flag=True rows)
    
    Example usage:
        # Diff update (WebSocket)
        tick = OrderBookTick(
            timestamp=datetime(2024, 11, 19, 10, 30, 45, tzinfo=timezone.utc),
            received_timestamp=datetime.now(timezone.utc),
            exchange="gate_io",
            trading_pair="VIRTUAL-USDT",
            update_id=123456789,
            snapshot_flag=False,
            side="bid",
            price=1.2345,
            amount=100.0
        )
        
        # Full snapshot checkpoint (REST)
        tick = OrderBookTick(
            timestamp=datetime(2024, 11, 19, 10, 35, 0, tzinfo=timezone.utc),
            received_timestamp=datetime.now(timezone.utc),
            exchange="gate_io",
            trading_pair="VIRTUAL-USDT",
            update_id=123456800,
            snapshot_flag=True,
            side="bid",
            price=1.2345,
            amount=100.0,
            best_bid_price=1.2345,
            best_ask_price=1.2346,
            total_bid_volume=50000.0,
            total_ask_volume=48000.0
        )
    """
    timestamp: datetime          # Event timestamp (exchange time)
    received_timestamp: datetime # Local receipt time
    exchange: str               # "gate_io" or "mexc"
    trading_pair: str          # "BTC-USDT"
    update_id: int             # Sequence number from exchange
    snapshot_flag: bool        # True = full snapshot, False = diff
    side: str                  # "bid" or "ask"
    price: float               # Price level
    amount: float              # Amount (0 = delete this level)
    
    # Optional: aggregated metrics (only for snapshot records)
    best_bid_price: Optional[float] = None
    best_ask_price: Optional[float] = None
    total_bid_volume: Optional[float] = None
    total_ask_volume: Optional[float] = None


# Explicit PyArrow schema for parquet storage
# This prevents type inference issues and ensures consistent schema across all files
ORDERBOOK_TICK_SCHEMA = pa.schema([
    ('timestamp', pa.timestamp('us', tz='UTC')),
    ('received_timestamp', pa.timestamp('us', tz='UTC')),
    ('exchange', pa.string()),
    ('trading_pair', pa.string()),
    ('update_id', pa.int64()),
    ('snapshot_flag', pa.bool_()),
    ('side', pa.string()),  # 'bid' or 'ask'
    ('price', pa.float64()),
    ('amount', pa.float64()),
    ('best_bid_price', pa.float64()),
    ('best_ask_price', pa.float64()),
    ('total_bid_volume', pa.float64()),
    ('total_ask_volume', pa.float64()),
])


def tick_to_dict(tick: OrderBookTick) -> dict:
    """
    Convert OrderBookTick to dictionary for DataFrame/PyArrow conversion
    
    Args:
        tick: OrderBookTick instance
        
    Returns:
        Dictionary with all fields
    """
    return {
        'timestamp': tick.timestamp,
        'received_timestamp': tick.received_timestamp,
        'exchange': tick.exchange,
        'trading_pair': tick.trading_pair,
        'update_id': tick.update_id,
        'snapshot_flag': tick.snapshot_flag,
        'side': tick.side,
        'price': tick.price,
        'amount': tick.amount,
        'best_bid_price': tick.best_bid_price,
        'best_ask_price': tick.best_ask_price,
        'total_bid_volume': tick.total_bid_volume,
        'total_ask_volume': tick.total_ask_volume,
    }

