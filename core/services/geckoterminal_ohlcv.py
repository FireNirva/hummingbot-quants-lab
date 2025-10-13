"""
GeckoTerminal OHLCV Service

Handles DEX OHLCV data fetching from GeckoTerminal API with rate limiting,
pagination, and data transformation to canonical schema.
"""
import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

import pandas as pd
from geckoterminal_py import GeckoTerminalAsyncClient

logger = logging.getLogger(__name__)


def parse_interval(interval: str) -> Tuple[str, int]:
    """
    Parse interval string to GeckoTerminal timeframe and aggregate.
    
    Args:
        interval: Interval string like "1m", "5m", "15m", "1h", "4h", "12h", "1d"
    
    Returns:
        Tuple of (timeframe, aggregate) where timeframe is "minute", "hour", or "day"
    
    Examples:
        >>> parse_interval("1m")
        ("minute", 1)
        >>> parse_interval("5m")
        ("minute", 5)
        >>> parse_interval("1h")
        ("hour", 1)
        >>> parse_interval("4h")
        ("hour", 4)
        >>> parse_interval("1d")
        ("day", 1)
    
    Raises:
        ValueError: If interval format is invalid or not supported by GeckoTerminal
    """
    if not interval:
        raise ValueError("Interval cannot be empty")
    
    # Extract number and unit
    import re
    match = re.match(r'^(\d+)([mhd])$', interval.lower())
    if not match:
        raise ValueError(f"Invalid interval format: {interval}. Expected format like '5m', '1h', '1d'")
    
    num_str, unit = match.groups()
    num = int(num_str)
    
    # Map to GeckoTerminal timeframe
    timeframe_map = {
        'm': 'minute',
        'h': 'hour',
        'd': 'day'
    }
    timeframe = timeframe_map[unit]
    
    # Validate against GeckoTerminal allowed aggregates
    allowed_aggregates = {
        'minute': [1, 5, 15],
        'hour': [1, 4, 12],
        'day': [1]
    }
    
    if num not in allowed_aggregates[timeframe]:
        raise ValueError(
            f"Aggregate {num} not allowed for timeframe {timeframe}. "
            f"Allowed values: {allowed_aggregates[timeframe]}"
        )
    
    return timeframe, num


def interval_to_seconds(interval: str) -> int:
    """Convert interval string to seconds."""
    timeframe, aggregate = parse_interval(interval)
    
    multipliers = {
        'minute': 60,
        'hour': 3600,
        'day': 86400
    }
    
    return aggregate * multipliers[timeframe]


class GeckoTerminalOhlcvService:
    """Service for fetching DEX OHLCV data from GeckoTerminal API."""
    
    def __init__(self, rate_limit_sleep: float = 1.0):
        """
        Initialize service.
        
        Args:
            rate_limit_sleep: Seconds to wait between API requests (default 1.0)
        """
        self.gt_client = GeckoTerminalAsyncClient()
        self.rate_limit_sleep = rate_limit_sleep
        self.last_request_time = 0
        
    async def _enforce_rate_limit(self):
        """Enforce rate limiting between API requests."""
        now = time.time()
        elapsed = now - self.last_request_time
        
        if elapsed < self.rate_limit_sleep:
            sleep_time = self.rate_limit_sleep - elapsed
            logger.debug(f"Rate limit: sleeping {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    async def fetch_ohlcv_chunk(
        self,
        network: str,
        pool_address: str,
        timeframe: str,
        aggregate: int,
        before_timestamp: Optional[int] = None,
        limit: int = 1000
    ) -> Dict[str, Any]:
        """
        Fetch a single chunk of OHLCV data.
        
        Args:
            network: Network ID (e.g., "base", "eth")
            pool_address: Pool contract address
            timeframe: "minute", "hour", or "day"
            aggregate: Aggregation period (1, 5, 15 for minute; 1, 4, 12 for hour; 1 for day)
            before_timestamp: Get data before this timestamp (for pagination)
            limit: Max number of data points (default 1000, max 1000)
        
        Returns:
            Raw API response dict with 'data' and 'meta' keys
        
        Raises:
            Exception: On API errors after retries
        """
        # Enforce rate limit
        await self._enforce_rate_limit()
        
        # Build params
        params = {
            'aggregate': str(aggregate),
            'limit': str(min(limit, 1000)),
            'currency': 'usd'
        }
        
        if before_timestamp:
            params['before_timestamp'] = str(before_timestamp)
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.gt_client.api_request(
                    'GET',
                    f'/networks/{network}/pools/{pool_address}/ohlcv/{timeframe}',
                    params=params
                )
                
                logger.debug(f"Fetched OHLCV chunk: {pool_address[:10]}... {timeframe}/{aggregate}")
                return response
                
            except Exception as e:
                error_msg = str(e)
                
                # Check for specific HTTP errors
                if '429' in error_msg:
                    # Rate limit - exponential backoff
                    wait_time = (2 ** attempt) * self.rate_limit_sleep
                    logger.warning(f"Rate limited (429), waiting {wait_time:.1f}s...")
                    await asyncio.sleep(wait_time)
                    continue
                elif '400' in error_msg or '404' in error_msg:
                    # Bad request or not found - don't retry
                    logger.error(f"API error (400/404): {error_msg}")
                    raise
                elif '500' in error_msg or '502' in error_msg or '503' in error_msg:
                    # Server error - retry
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * self.rate_limit_sleep
                        logger.warning(f"Server error (5xx), retrying in {wait_time:.1f}s...")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"Server error after {max_retries} attempts: {error_msg}")
                        raise
                else:
                    # Unknown error
                    if attempt < max_retries - 1:
                        logger.warning(f"Error: {error_msg}, retrying...")
                        await asyncio.sleep(self.rate_limit_sleep)
                        continue
                    else:
                        logger.error(f"Failed after {max_retries} attempts: {error_msg}")
                        raise
        
        raise Exception(f"Failed to fetch OHLCV after {max_retries} retries")
    
    async def fetch_ohlcv_range(
        self,
        network: str,
        pool_address: str,
        interval: str,
        start_timestamp: int,
        end_timestamp: int
    ) -> pd.DataFrame:
        """
        Fetch OHLCV data for a time range using pagination.
        
        Args:
            network: Network ID
            pool_address: Pool address
            interval: Interval string (e.g., "5m", "1h")
            start_timestamp: Start time (Unix timestamp, seconds)
            end_timestamp: End time (Unix timestamp, seconds)
        
        Returns:
            DataFrame with OHLCV data, sorted by timestamp, deduplicated
        """
        # Parse interval
        timeframe, aggregate = parse_interval(interval)
        
        logger.info(f"Fetching {interval} OHLCV for {pool_address[:10]}... from {start_timestamp} to {end_timestamp}")
        
        all_ohlcv = []
        before_timestamp = None
        chunks_fetched = 0
        
        while True:
            # Fetch chunk
            try:
                response = await self.fetch_ohlcv_chunk(
                    network=network,
                    pool_address=pool_address,
                    timeframe=timeframe,
                    aggregate=aggregate,
                    before_timestamp=before_timestamp,
                    limit=1000
                )
            except Exception as e:
                logger.error(f"Failed to fetch chunk: {e}")
                break
            
            # Extract data
            if 'data' not in response or 'attributes' not in response['data']:
                logger.warning("No data in response")
                break
            
            ohlcv_list = response['data']['attributes'].get('ohlcv_list', [])
            
            if not ohlcv_list:
                logger.debug("No more OHLCV data")
                break
            
            # Check if we've reached start_timestamp
            earliest_ts = min(row[0] for row in ohlcv_list)
            logger.debug(f"Chunk {chunks_fetched + 1}: {len(ohlcv_list)} candles, earliest={earliest_ts}")
            
            # Filter candles within range
            filtered = [row for row in ohlcv_list if start_timestamp <= row[0] <= end_timestamp]
            all_ohlcv.extend(filtered)
            
            chunks_fetched += 1
            
            # Stop if we've reached the start
            if earliest_ts <= start_timestamp:
                logger.debug(f"Reached start_timestamp, stopping")
                break
            
            # Update pagination cursor
            before_timestamp = earliest_ts
            
            # Safety limit
            if chunks_fetched >= 100:
                logger.warning(f"Reached max chunks (100), stopping")
                break
        
        logger.info(f"Fetched {len(all_ohlcv)} candles in {chunks_fetched} chunks")
        
        # Convert to DataFrame
        if all_ohlcv:
            # Extract meta if available
            meta = response.get('meta', {})
            df = convert_ohlcv_to_dataframe(all_ohlcv, meta)
            return df
        else:
            # Return empty DataFrame with correct schema
            return pd.DataFrame(columns=[
                'open', 'high', 'low', 'close', 'volume',
                'quote_asset_volume', 'n_trades', 
                'taker_buy_base_volume', 'taker_buy_quote_volume'
            ])


def convert_ohlcv_to_dataframe(ohlcv_list: List[List], meta: Dict = None) -> pd.DataFrame:
    """
    Convert raw OHLCV list to DataFrame with canonical schema.
    
    Args:
        ohlcv_list: List of [timestamp, open, high, low, close, volume]
        meta: Optional metadata dict with base/quote token info
    
    Returns:
        DataFrame with timestamp as UTC index and OHLC columns
    """
    if not ohlcv_list:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(ohlcv_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # Convert timestamp to datetime (UTC)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
    df.set_index('timestamp', inplace=True)
    
    # Add missing columns with 0 defaults (to match CEX schema)
    df['quote_asset_volume'] = 0.0
    df['n_trades'] = 0
    df['taker_buy_base_volume'] = 0.0
    df['taker_buy_quote_volume'] = 0.0
    
    # Sort and deduplicate
    df = df.sort_index()
    df = df[~df.index.duplicated(keep='last')]
    
    return df


def load_existing_parquet(path: Path) -> Optional[pd.DataFrame]:
    """
    Load existing parquet file.
    
    Args:
        path: Path to parquet file
    
    Returns:
        DataFrame if file exists, None otherwise
    """
    if not path.exists():
        return None
    
    try:
        df = pd.read_parquet(path)
        
        # Ensure index is datetime with timezone
        if df.index.tz is None:
            df.index = pd.to_datetime(df.index, utc=True)
        
        return df
    except Exception as e:
        logger.error(f"Error loading parquet {path}: {e}")
        return None


def merge_and_sort(existing_df: pd.DataFrame, new_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge existing and new DataFrames, deduplicate, and sort.
    
    Args:
        existing_df: Existing DataFrame
        new_df: New DataFrame to merge
    
    Returns:
        Merged DataFrame, sorted by timestamp, deduplicated
    """
    if existing_df is None or existing_df.empty:
        return new_df
    
    if new_df is None or new_df.empty:
        return existing_df
    
    # Ensure both have timezone-aware indices
    if existing_df.index.tz is None:
        existing_df.index = pd.to_datetime(existing_df.index, utc=True)
    
    if new_df.index.tz is None:
        new_df.index = pd.to_datetime(new_df.index, utc=True)
    
    # Concatenate
    merged = pd.concat([existing_df, new_df])
    
    # Deduplicate (keep last)
    merged = merged[~merged.index.duplicated(keep='last')]
    
    # Sort
    merged = merged.sort_index()
    
    return merged


def save_raw_response(
    response: Dict[str, Any],
    output_dir: Path,
    pool_address: str
):
    """
    Save or append raw OHLCV response to aggregated JSON file.
    
    Args:
        response: Raw API response dict
        output_dir: Output directory
        pool_address: Pool address (used in filename)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    filename = output_dir / f"{pool_address}_raw.json"
    
    # Load existing if present
    if filename.exists():
        try:
            with open(filename, 'r') as f:
                existing = json.load(f)
        except Exception as e:
            logger.warning(f"Error loading existing raw file: {e}, creating new")
            existing = {'responses': []}
    else:
        existing = {'responses': []}
    
    # Append new response
    existing['responses'].append({
        'timestamp': pd.Timestamp.now(tz='UTC').isoformat(),
        'data': response
    })
    
    # Save
    with open(filename, 'w') as f:
        json.dump(existing, f, indent=2, default=str)
    
    logger.debug(f"Saved raw response to {filename}")

