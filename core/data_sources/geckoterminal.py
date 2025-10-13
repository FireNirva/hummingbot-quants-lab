"""
GeckoTerminal Data Source

DEX candles data source using GeckoTerminal API, mirroring CLOBDataSource interface.
"""
import logging
from typing import Dict, Tuple
from pathlib import Path

import pandas as pd

from core.data_structures.candles import Candles
from core.data_paths import data_paths
from core.services.geckoterminal_ohlcv import (
    GeckoTerminalOhlcvService,
    load_existing_parquet,
    merge_and_sort,
    interval_to_seconds
)

logger = logging.getLogger(__name__)


class GeckoTerminalDataSource:
    """DEX candles data source using GeckoTerminal API."""
    
    def __init__(self, rate_limit_sleep: float = 1.0):
        """
        Initialize data source.
        
        Args:
            rate_limit_sleep: Seconds to wait between API requests
        """
        self.service = GeckoTerminalOhlcvService(rate_limit_sleep)
        # Cache key: (network, trading_pair, interval)
        self._candles_cache: Dict[Tuple[str, str, str], pd.DataFrame] = {}
        
    async def get_candles(
        self,
        network: str,
        pool_address: str,
        trading_pair: str,
        interval: str,
        start_time: int,
        end_time: int
    ) -> Candles:
        """
        Fetch DEX candles for a pool.
        
        Args:
            network: Network ID (e.g., "base")
            pool_address: Pool contract address
            trading_pair: Trading pair name (e.g., "AERO-USDT")
            interval: Interval string (e.g., "5m", "1h")
            start_time: Start timestamp (seconds)
            end_time: End timestamp (seconds)
        
        Returns:
            Candles object with data
        """
        cache_key = (network, trading_pair, interval)
        
        # Check if cached and range is covered
        if cache_key in self._candles_cache:
            cached_df = self._candles_cache[cache_key]
            
            if not cached_df.empty:
                cached_start_time = int(cached_df.index.min().timestamp())
                cached_end_time = int(cached_df.index.max().timestamp())
                
                # If cache covers the requested range, return from cache
                if cached_start_time <= start_time and cached_end_time >= end_time:
                    logger.info(
                        f"Using cached data for {network} {trading_pair} {interval} "
                        f"from {start_time} to {end_time}"
                    )
                    
                    # Filter to requested range
                    filtered_df = cached_df[
                        (cached_df.index >= pd.to_datetime(start_time, unit='s', utc=True)) &
                        (cached_df.index <= pd.to_datetime(end_time, unit='s', utc=True))
                    ]
                    
                    return Candles(
                        candles_df=filtered_df,
                        connector_name=f"geckoterminal_{network}",
                        trading_pair=trading_pair,
                        interval=interval
                    )
        
        # Fetch from API
        logger.info(f"Fetching {network} {trading_pair} {interval} from API")
        
        new_df = await self.service.fetch_ohlcv_range(
            network=network,
            pool_address=pool_address,
            interval=interval,
            start_timestamp=start_time,
            end_timestamp=end_time
        )
        
        # Merge with cache if exists
        if cache_key in self._candles_cache:
            merged_df = merge_and_sort(self._candles_cache[cache_key], new_df)
            self._candles_cache[cache_key] = merged_df
        else:
            self._candles_cache[cache_key] = new_df
        
        # Return Candles object
        return Candles(
            candles_df=self._candles_cache[cache_key],
            connector_name=f"geckoterminal_{network}",
            trading_pair=trading_pair,
            interval=interval
        )
    
    def load_candles_cache(self):
        """
        Load existing parquet files from disk into cache.
        
        Pattern: geckoterminal_{network}|{trading_pair}|{interval}.parquet
        """
        candles_dir = data_paths.candles_dir
        
        if not candles_dir.exists():
            logger.info(f"Candles directory does not exist: {candles_dir}")
            return
        
        # Find all geckoterminal parquet files
        pattern = "geckoterminal_*.parquet"
        files = list(candles_dir.glob(pattern))
        
        logger.info(f"Loading {len(files)} GeckoTerminal candles files from cache")
        
        for file in files:
            try:
                # Parse filename: geckoterminal_{network}|{trading_pair}|{interval}.parquet
                stem = file.stem  # Remove .parquet
                
                # Remove "geckoterminal_" prefix
                if not stem.startswith("geckoterminal_"):
                    continue
                
                remainder = stem[len("geckoterminal_"):]
                
                # Split by |
                parts = remainder.split('|')
                if len(parts) != 3:
                    logger.warning(f"Invalid filename format: {file.name}")
                    continue
                
                network, trading_pair, interval = parts
                
                # Load DataFrame
                df = load_existing_parquet(file)
                
                if df is not None and not df.empty:
                    cache_key = (network, trading_pair, interval)
                    self._candles_cache[cache_key] = df
                    logger.debug(
                        f"Loaded {len(df)} candles for {network}|{trading_pair}|{interval}"
                    )
                
            except Exception as e:
                logger.error(f"Error loading {file.name}: {e}")
                continue
        
        logger.info(f"Loaded {len(self._candles_cache)} candles into cache")
    
    def dump_candles_cache(self):
        """
        Save all cached candles to parquet files.
        
        Filename: geckoterminal_{network}|{trading_pair}|{interval}.parquet
        """
        candles_dir = data_paths.candles_dir
        candles_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Dumping {len(self._candles_cache)} candles to {candles_dir}")
        
        for (network, trading_pair, interval), df in self._candles_cache.items():
            try:
                if df.empty:
                    logger.debug(f"Skipping empty DataFrame: {network}|{trading_pair}|{interval}")
                    continue
                
                # Build filename
                filename = candles_dir / f"geckoterminal_{network}|{trading_pair}|{interval}.parquet"
                
                # Load existing and merge
                existing_df = load_existing_parquet(filename)
                
                if existing_df is not None:
                    merged_df = merge_and_sort(existing_df, df)
                else:
                    merged_df = df
                
                # Save
                merged_df.to_parquet(
                    filename,
                    engine='pyarrow',
                    compression='snappy',
                    index=True
                )
                
                logger.info(
                    f"Saved {len(merged_df)} candles to "
                    f"{network}|{trading_pair}|{interval}.parquet"
                )
                
            except Exception as e:
                logger.error(f"Error saving {network}|{trading_pair}|{interval}: {e}")
                continue
        
        logger.info("Candles cache dumped successfully")
    
    @property
    def candles_cache(self):
        """
        Get candles cache as Candles objects.
        
        Returns:
            Dict mapping cache keys to Candles objects
        """
        return {
            (network, trading_pair, interval): Candles(
                candles_df=df,
                connector_name=f"geckoterminal_{network}",
                trading_pair=trading_pair,
                interval=interval
            )
            for (network, trading_pair, interval), df in self._candles_cache.items()
        }

