"""
DEX Candles Downloader Task

Scheduled task for downloading DEX OHLCV data from GeckoTerminal API.
"""
import logging
from typing import Dict, Any
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from core.tasks import BaseTask, TaskContext
from core.data_sources.geckoterminal import GeckoTerminalDataSource
from core.data_sources.clob import CLOBDataSource
from core.data_paths import data_paths
from core.services.geckoterminal_ohlcv import interval_to_seconds

logging.basicConfig(level=logging.INFO)


class DexCandlesDownloader(BaseTask):
    """Download DEX OHLCV data from GeckoTerminal."""
    
    def __init__(self, config):
        super().__init__(config)
        
        # Parse config
        task_config = self.config.config
        self.network = task_config.get("network", "base")
        self.connector = task_config.get("connector", "gate_io")
        self.mapping_file = task_config.get("mapping_file")
        self.intervals = task_config.get("intervals", ["5m", "15m", "1h"])
        self.lookback_days = task_config.get("lookback_days", 7)
        self.start_from_cex = task_config.get("start_from_cex", False)
        self.rate_limit_sleep = task_config.get("rate_limit_sleep", 1.0)
        self.max_requests = task_config.get("max_requests", 100)
        
        # Data sources (initialized in setup)
        self.gt_ds = None
        self.cex_ds = None
        
    async def setup(self, context: TaskContext) -> None:
        """Initialize data sources."""
        await super().setup(context)
        
        # Initialize GeckoTerminal data source
        self.gt_ds = GeckoTerminalDataSource(self.rate_limit_sleep)
        
        # Load existing cache
        self.gt_ds.load_candles_cache()
        
        # Initialize CEX data source if needed
        if self.start_from_cex:
            self.cex_ds = CLOBDataSource()
        
        logging.info(f"Setup completed for {context.task_name}")
        logging.info(f"  Network: {self.network}")
        logging.info(f"  Connector: {self.connector}")
        logging.info(f"  Intervals: {', '.join(self.intervals)}")
        logging.info(f"  Lookback days: {self.lookback_days}")
        
    async def cleanup(self, context: TaskContext, result) -> None:
        """Cleanup after task execution."""
        await super().cleanup(context, result)
        logging.info(f"Cleanup completed for {context.task_name}")
        
    async def execute(self, context: TaskContext) -> Dict[str, Any]:
        """Main execution logic."""
        start_time = datetime.now(timezone.utc)
        logging.info(f"Starting DEX candles download for {self.network}")
        
        try:
            # Load pool mapping
            if self.mapping_file:
                mapping_path = Path(self.mapping_file)
            else:
                mapping_path = data_paths.processed_dir / 'pool_mappings' / f'{self.network}_{self.connector}_pool_map.parquet'
            
            if not mapping_path.exists():
                raise FileNotFoundError(f"Pool mapping not found: {mapping_path}")
            
            df = pd.read_parquet(mapping_path)
            top_pools = df[df['rank'] == 1].copy()
            
            logging.info(f"Found {len(top_pools)} pools (rank=1)")
            
            # Statistics
            stats = {
                'pairs_total': len(top_pools),
                'pairs_success': 0,
                'pairs_failed': 0,
                'candles_fetched': 0,
                'requests_made': 0,
                'failed_pairs': []
            }
            
            request_count = 0
            
            # For each pool × interval
            for idx, (_, pool) in enumerate(top_pools.iterrows(), 1):
                trading_pair = pool['trading_pair']
                pool_address = pool['pool_address']
                
                logging.info(f"[{idx}/{len(top_pools)}] Processing {trading_pair}")
                
                pair_success = True
                
                for interval in self.intervals:
                    # Check request limit
                    if request_count >= self.max_requests:
                        logging.warning(f"Reached max requests ({self.max_requests}), stopping")
                        break
                    
                    try:
                        # Determine time range
                        end_time = int(datetime.now(timezone.utc).timestamp())
                        start_time_ts = self._determine_start_time(trading_pair, interval, end_time)
                        
                        # Fetch candles
                        candles = await self.gt_ds.get_candles(
                            network=self.network,
                            pool_address=pool_address,
                            trading_pair=trading_pair,
                            interval=interval,
                            start_time=start_time_ts,
                            end_time=end_time
                        )
                        
                        stats['candles_fetched'] += len(candles.data)
                        stats['requests_made'] += 1
                        request_count += 1
                        
                        logging.debug(f"  {interval}: fetched {len(candles.data)} candles")
                        
                    except Exception as e:
                        logging.error(f"  {interval}: Failed - {e}")
                        stats['failed_pairs'].append(f"{trading_pair}|{interval}")
                        pair_success = False
                        continue
                
                if pair_success:
                    stats['pairs_success'] += 1
                else:
                    stats['pairs_failed'] += 1
                
                # Check request limit
                if request_count >= self.max_requests:
                    break
            
            # Dump to parquet
            logging.info("Saving candles to parquet files")
            self.gt_ds.dump_candles_cache()
            
            # Prepare result
            duration = datetime.now(timezone.utc) - start_time
            result = {
                'status': 'completed',
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'execution_id': context.execution_id,
                'network': self.network,
                'connector': self.connector,
                'stats': stats,
                'duration_seconds': duration.total_seconds()
            }
            
            logging.info(f"DEX candles download completed: {stats}")
            return result
            
        except Exception as e:
            logging.error(f"Error executing DEX candles downloader: {e}")
            raise
    
    def _determine_start_time(self, trading_pair: str, interval: str, end_time: int) -> int:
        """
        Determine start_time based on config and existing data.
        
        Args:
            trading_pair: Trading pair name
            interval: Interval string
            end_time: End timestamp
        
        Returns:
            Start timestamp (seconds)
        """
        # Option 1: Align with CEX data
        if self.start_from_cex and self.cex_ds:
            cex_file = data_paths.candles_dir / f"{self.connector}|{trading_pair}|{interval}.parquet"
            
            if cex_file.exists():
                try:
                    cex_df = pd.read_parquet(cex_file)
                    start_time = int(cex_df.index.min().timestamp())
                    logging.debug(f"  {interval}: Aligning with CEX data")
                    return start_time
                except Exception as e:
                    logging.warning(f"  {interval}: Failed to read CEX data: {e}")
        
        # Option 2: Incremental from existing DEX data
        dex_file = data_paths.candles_dir / f"geckoterminal_{self.network}|{trading_pair}|{interval}.parquet"
        
        if dex_file.exists():
            try:
                existing_df = pd.read_parquet(dex_file)
                # Start from last timestamp minus overlap (10 candles)
                overlap = 10 * interval_to_seconds(interval)
                start_time = int(existing_df.index.max().timestamp()) - overlap
                logging.debug(f"  {interval}: Incremental from {existing_df.index.max()}")
                return start_time
            except Exception as e:
                logging.warning(f"  {interval}: Failed to read existing DEX data: {e}")
        
        # Option 3: Fresh download with lookback
        start_time = end_time - (self.lookback_days * 86400)
        logging.debug(f"  {interval}: Fresh download ({self.lookback_days} days)")
        return start_time
    
    async def on_success(self, context: TaskContext, result) -> None:
        """Success callback."""
        stats = result.result_data.get('stats', {})
        logging.info(f"✓ DexCandlesDownloader succeeded in {result.duration_seconds:.2f}s")
        logging.info(f"  - Pairs: {stats.get('pairs_success', 0)}/{stats.get('pairs_total', 0)}")
        logging.info(f"  - Candles: {stats.get('candles_fetched', 0):,}")
        logging.info(f"  - Requests: {stats.get('requests_made', 0)}")
    
    async def on_failure(self, context: TaskContext, result) -> None:
        """Failure callback."""
        logging.error(f"✗ DexCandlesDownloader failed: {result.error_message}")
        logging.error(f"  Execution ID: {context.execution_id}")
    
    async def on_retry(self, context: TaskContext, attempt: int, error: Exception) -> None:
        """Retry callback."""
        logging.warning(f"🔄 DexCandlesDownloader retry attempt {attempt}: {error}")

