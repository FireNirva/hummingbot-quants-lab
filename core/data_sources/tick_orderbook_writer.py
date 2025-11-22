"""
Efficient parquet writer for tick-level orderbook data

This module implements a buffered writer that:
- Writes to multiple part files per day (no read-concat-rewrite overhead)
- Uses in-memory buffer with periodic flush (count or time based)
- Maintains explicit PyArrow schema for consistency
- Supports daily partitioning by exchange/symbol/date
"""

import asyncio
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING
import pyarrow as pa
import pyarrow.parquet as pq

from core.data_structures.orderbook_tick import OrderBookTick, ORDERBOOK_TICK_SCHEMA, tick_to_dict

if TYPE_CHECKING:
    from core.monitoring.metrics import OrderbookMetrics

logger = logging.getLogger(__name__)


class TickOrderBookWriter:
    """
    Efficient parquet writer for tick-level orderbook data
    
    Strategy:
    - Daily partition per exchange/symbol: {exchange}_{symbol}_{YYYYMMDD}/
    - Multiple part files per day: part_00001.parquet, part_00002.parquet, ...
    - In-memory buffer with periodic flush (every N ticks or M seconds)
    - Flush writes NEW parquet file, no read-concat-rewrite overhead
    - Use pyarrow.dataset for reading multiple part files as single dataset
    
    Example directory structure:
        orderbook_ticks/
        ├── gate_io_VIRTUAL-USDT_20241119/
        │   ├── part_00001.parquet  (first flush)
        │   ├── part_00002.parquet  (second flush)
        │   └── part_00003.parquet  (third flush)
        └── gate_io_IRON-USDT_20241119/
            ├── part_00001.parquet
            └── part_00002.parquet
    
    Usage:
        writer = TickOrderBookWriter(output_dir=Path("data/orderbook_ticks"))
        
        # Add ticks to buffer
        await writer.write_tick(tick1)
        await writer.write_tick(tick2)
        
        # Buffer auto-flushes when reaching size limit or time interval
        
        # Manual flush at shutdown
        await writer.flush_all()
    """
    
    def __init__(
        self,
        output_dir: Path,
        buffer_size: int = 100,
        flush_interval: float = 10.0,
        metrics: Optional['OrderbookMetrics'] = None
    ):
        """
        Initialize tick orderbook writer
        
        Args:
            output_dir: Base directory for storing partition directories
            buffer_size: Number of ticks to buffer before auto-flush (default: 100)
            flush_interval: Time in seconds between flushes (default: 10.0)
            metrics: Optional OrderbookMetrics instance for monitoring
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.metrics = metrics
        
        # Buffer: key=(exchange, symbol, date) -> list of ticks
        self.buffer: Dict[Tuple[str, str, str], List[OrderBookTick]] = {}
        
        # Track last flush time for each partition
        self.last_flush_time: Dict[Tuple[str, str, str], float] = {}
        
        # Track part file counters for each partition
        self.part_counters: Dict[Tuple[str, str, str], int] = {}
        
        logger.info(f"TickOrderBookWriter initialized: dir={output_dir}, "
                   f"buffer_size={buffer_size}, flush_interval={flush_interval}s")
    
    def get_buffer_sizes(self) -> Dict[Tuple[str, str], int]:
        """
        Get current buffer sizes for each (exchange, symbol) pair
        
        Returns:
            Dictionary mapping (exchange, symbol) to current buffer size
        """
        buffer_sizes = {}
        for (exchange, symbol, date), ticks in self.buffer.items():
            key = (exchange, symbol)
            buffer_sizes[key] = buffer_sizes.get(key, 0) + len(ticks)
        return buffer_sizes
    
    async def write_tick(self, tick: OrderBookTick) -> None:
        """
        Add tick to buffer, auto-flush if needed
        
        Args:
            tick: OrderBookTick instance to write
            
        Triggers flush if:
        - Buffer size >= buffer_size
        - Time since last flush >= flush_interval
        """
        # Generate partition key
        date_str = tick.timestamp.strftime('%Y%m%d')
        key = (tick.exchange, tick.trading_pair, date_str)
        
        # Initialize buffer for this partition if needed
        if key not in self.buffer:
            self.buffer[key] = []
            self.last_flush_time[key] = asyncio.get_event_loop().time()
            self.part_counters[key] = 0
        
        # Add tick to buffer
        self.buffer[key].append(tick)
        
        # Check flush triggers
        current_time = asyncio.get_event_loop().time()
        time_since_flush = current_time - self.last_flush_time[key]
        
        should_flush = (
            len(self.buffer[key]) >= self.buffer_size or
            time_since_flush >= self.flush_interval
        )
        
        if should_flush:
            await self.flush_buffer(key)
    
    async def flush_buffer(self, key: Optional[Tuple[str, str, str]] = None) -> None:
        """
        Write buffered ticks to NEW parquet part file
        
        Args:
            key: Partition key (exchange, symbol, date). If None, flush all buffers.
            
        Strategy:
        1. Convert buffer to PyArrow Table with explicit schema
        2. Create partition directory if not exists
        3. Write new part file with incremented counter
        4. Clear buffer and update last flush time
        """
        if key is None:
            # Flush all buffers
            keys_to_flush = list(self.buffer.keys())
            for k in keys_to_flush:
                await self.flush_buffer(k)
            return
        
        # Check if buffer has data
        if key not in self.buffer or len(self.buffer[key]) == 0:
            return
        
        try:
            # Extract partition info
            exchange, symbol, date_str = key
            ticks = self.buffer[key]
            tick_count = len(ticks)
            
            # Start timing flush operation
            flush_start = time.time()
            
            # Create partition directory
            partition_name = f"{exchange}_{symbol}_{date_str}"
            partition_dir = self.output_dir / partition_name
            partition_dir.mkdir(parents=True, exist_ok=True)
            
            # Increment part counter
            self.part_counters[key] += 1
            part_num = self.part_counters[key]
            
            # Generate part file path
            part_filename = f"part_{part_num:05d}.parquet"
            part_path = partition_dir / part_filename
            
            # Convert ticks to list of dicts
            tick_dicts = [tick_to_dict(tick) for tick in ticks]
            
            # Create PyArrow Table with explicit schema
            table = pa.Table.from_pylist(tick_dicts, schema=ORDERBOOK_TICK_SCHEMA)
            
            # Write to parquet with compression
            pq.write_table(
                table,
                part_path,
                compression='snappy',
                use_dictionary=True,  # Efficient for string columns
                write_statistics=True  # Enable statistics for query optimization
            )
            
            # Record flush metrics
            flush_duration = time.time() - flush_start
            if self.metrics:
                self.metrics.increment_files_written(exchange, symbol)
                self.metrics.observe_file_write_latency(exchange, symbol, flush_duration)
                # Update buffer size (now empty for this partition)
                self.metrics.set_buffer_size(exchange, symbol, 0)
            
            # Clear buffer and update last flush time
            self.buffer[key] = []
            self.last_flush_time[key] = asyncio.get_event_loop().time()
            
            logger.debug(f"✅ Flushed {tick_count} ticks to {partition_name}/{part_filename} in {flush_duration:.3f}s")
            
        except Exception as e:
            logger.error(f"Failed to flush buffer for {key}: {e}", exc_info=True)
            # Keep buffer in memory for retry
            raise
    
    async def flush_all(self) -> None:
        """
        Flush all remaining buffered data
        
        Call this during graceful shutdown to ensure no data loss
        """
        logger.info("Flushing all buffers...")
        await self.flush_buffer(None)
        logger.info("All buffers flushed")
    
    def get_buffer_stats(self) -> Dict[str, any]:
        """
        Get statistics about current buffer state
        
        Returns:
            Dictionary with buffer statistics:
            - total_partitions: Number of active partitions
            - total_buffered_ticks: Total ticks in all buffers
            - partition_details: List of (partition_key, tick_count, time_since_flush)
        """
        current_time = asyncio.get_event_loop().time()
        
        partition_details = []
        total_ticks = 0
        
        for key, ticks in self.buffer.items():
            tick_count = len(ticks)
            total_ticks += tick_count
            time_since_flush = current_time - self.last_flush_time.get(key, current_time)
            
            partition_details.append({
                'exchange': key[0],
                'symbol': key[1],
                'date': key[2],
                'buffered_ticks': tick_count,
                'seconds_since_flush': round(time_since_flush, 2)
            })
        
        return {
            'total_partitions': len(self.buffer),
            'total_buffered_ticks': total_ticks,
            'partition_details': partition_details
        }


def load_orderbook_ticks(
    connector_name: str,
    trading_pair: str,
    start_date: str,
    end_date: str,
    output_dir: Path = None,
    only_snapshots: bool = False
) -> pa.Table:
    """
    Load tick-level orderbook data using pyarrow dataset API
    
    Automatically aggregates all part files within date range.
    
    Args:
        connector_name: Exchange name ("gate_io" or "mexc")
        trading_pair: Trading pair ("VIRTUAL-USDT")
        start_date: Start date (YYYYMMDD format)
        end_date: End date (YYYYMMDD format)
        output_dir: Base directory containing partitions (default: data_paths.raw_dir / "orderbook_ticks")
        only_snapshots: If True, filter snapshot_flag=True records
                       (useful for validation against 5s snapshot system)
    
    Returns:
        PyArrow Table with all ticks in chronological order
        
    Example:
        >>> table = load_orderbook_ticks(
        ...     "gate_io", "VIRTUAL-USDT", "20241119", "20241120"
        ... )
        >>> df = table.to_pandas()
        >>> print(f"Loaded {len(df)} ticks")
    """
    if output_dir is None:
        from core.data_paths import data_paths
        output_dir = data_paths.raw_dir / "orderbook_ticks"
    
    output_dir = Path(output_dir)
    
    # Find matching partition directories
    # Pattern: {exchange}_{symbol}_{YYYYMMDD}/
    matching_dirs = []
    
    for partition_dir in output_dir.iterdir():
        if not partition_dir.is_dir():
            continue
        
        # Parse partition directory name
        parts = partition_dir.name.split('_')
        if len(parts) < 3:
            continue
        
        # Extract date (last part)
        date_str = parts[-1]
        
        # Check if matches exchange, symbol, and date range
        expected_prefix = f"{connector_name}_{trading_pair}"
        if partition_dir.name.startswith(expected_prefix) and start_date <= date_str <= end_date:
            matching_dirs.append(partition_dir)
    
    if not matching_dirs:
        logger.warning(f"No tick data found for {connector_name} {trading_pair} "
                      f"between {start_date} and {end_date}")
        return pa.table({}, schema=ORDERBOOK_TICK_SCHEMA)
    
    logger.info(f"Loading ticks from {len(matching_dirs)} partition(s)")
    
    # Load all matching partitions as a single dataset
    import pyarrow.dataset as ds
    
    tables = []
    for partition_dir in sorted(matching_dirs):
        try:
            dataset = ds.dataset(partition_dir, format='parquet')
            
            # Apply snapshot filter if requested
            if only_snapshots:
                table = dataset.to_table(filter=ds.field('snapshot_flag') == True)
            else:
                table = dataset.to_table()
            
            tables.append(table)
            logger.debug(f"Loaded {len(table)} ticks from {partition_dir.name}")
            
        except Exception as e:
            logger.error(f"Error loading {partition_dir}: {e}")
            continue
    
    if not tables:
        return pa.table({}, schema=ORDERBOOK_TICK_SCHEMA)
    
    # Concatenate all tables
    combined_table = pa.concat_tables(tables)
    
    # Sort by timestamp for chronological order
    indices = pa.compute.sort_indices(combined_table, sort_keys=[('timestamp', 'ascending')])
    sorted_table = pa.compute.take(combined_table, indices)
    
    logger.info(f"Loaded {len(sorted_table)} total ticks")
    
    return sorted_table

