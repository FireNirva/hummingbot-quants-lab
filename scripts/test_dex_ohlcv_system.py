#!/usr/bin/env python3
"""
DEX OHLCV System Comprehensive Test Suite

Tests all components of the DEX OHLCV download system.
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.services.geckoterminal_ohlcv import (
    parse_interval,
    interval_to_seconds,
    convert_ohlcv_to_dataframe,
    load_existing_parquet,
    merge_and_sort,
    GeckoTerminalOhlcvService
)
from core.data_sources.geckoterminal import GeckoTerminalDataSource
from core.data_paths import data_paths


class TestSuite:
    """Comprehensive test suite for DEX OHLCV system."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Record test result."""
        if condition:
            print(f"  ✓ {name}")
            self.passed += 1
        else:
            print(f"  ✗ {name}")
            if error_msg:
                print(f"    Error: {error_msg}")
            self.failed += 1
            self.errors.append((name, error_msg))
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print("\n" + "="*80)
        print("Test Summary")
        print("="*80)
        print(f"Total: {total} tests")
        print(f"✓ Passed: {self.passed}")
        print(f"✗ Failed: {self.failed}")
        
        if self.errors:
            print("\nFailed Tests:")
            for name, error in self.errors:
                print(f"  - {name}")
                if error:
                    print(f"    {error}")
        
        print("="*80)
        return self.failed == 0


def test_unit_interval_parsing():
    """Test 1: Unit test for interval parsing."""
    print("\n" + "="*80)
    print("Test 1: Interval Parsing")
    print("="*80)
    
    suite = TestSuite()
    
    # Test valid intervals
    test_cases = [
        ("1m", ("minute", 1)),
        ("5m", ("minute", 5)),
        ("15m", ("minute", 15)),
        ("1h", ("hour", 1)),
        ("4h", ("hour", 4)),
        ("12h", ("hour", 12)),
        ("1d", ("day", 1))
    ]
    
    for interval, expected in test_cases:
        try:
            result = parse_interval(interval)
            suite.test(
                f"parse_interval('{interval}') == {expected}",
                result == expected,
                f"Got {result}"
            )
        except Exception as e:
            suite.test(f"parse_interval('{interval}')", False, str(e))
    
    # Test invalid intervals
    invalid_cases = ["2m", "30m", "2h", "3d", "invalid", "", "1x"]
    
    for interval in invalid_cases:
        try:
            parse_interval(interval)
            suite.test(f"parse_interval('{interval}') raises ValueError", False, "No exception raised")
        except ValueError:
            suite.test(f"parse_interval('{interval}') raises ValueError", True)
        except Exception as e:
            suite.test(f"parse_interval('{interval}') raises ValueError", False, f"Wrong exception: {e}")
    
    # Test interval_to_seconds
    seconds_cases = [
        ("1m", 60),
        ("5m", 300),
        ("15m", 900),
        ("1h", 3600),
        ("4h", 14400),
        ("1d", 86400)
    ]
    
    for interval, expected_seconds in seconds_cases:
        try:
            result = interval_to_seconds(interval)
            suite.test(
                f"interval_to_seconds('{interval}') == {expected_seconds}",
                result == expected_seconds,
                f"Got {result}"
            )
        except Exception as e:
            suite.test(f"interval_to_seconds('{interval}')", False, str(e))
    
    return suite.summary()


def test_unit_data_conversion():
    """Test 2: Unit test for data conversion."""
    print("\n" + "="*80)
    print("Test 2: Data Conversion")
    print("="*80)
    
    suite = TestSuite()
    
    # Test with sample OHLCV data
    now = int(datetime.now(timezone.utc).timestamp())
    ohlcv_list = [
        [now - 300, 100.0, 105.0, 98.0, 103.0, 1000.0],
        [now - 240, 103.0, 107.0, 102.0, 106.0, 1200.0],
        [now - 180, 106.0, 110.0, 105.0, 109.0, 1500.0]
    ]
    
    try:
        df = convert_ohlcv_to_dataframe(ohlcv_list, {})
        
        # Check DataFrame is not empty
        suite.test("DataFrame is not empty", not df.empty)
        
        # Check row count
        suite.test("DataFrame has 3 rows", len(df) == 3, f"Got {len(df)} rows")
        
        # Check columns
        expected_cols = ['open', 'high', 'low', 'close', 'volume',
                        'quote_asset_volume', 'n_trades',
                        'taker_buy_base_volume', 'taker_buy_quote_volume']
        has_all_cols = all(col in df.columns for col in expected_cols)
        suite.test("DataFrame has all required columns", has_all_cols)
        
        # Check index is DatetimeIndex
        suite.test("Index is DatetimeIndex", isinstance(df.index, pd.DatetimeIndex))
        
        # Check index has timezone
        suite.test("Index has UTC timezone", df.index.tz is not None)
        
        # Check sorted
        suite.test("DataFrame is sorted", df.index.is_monotonic_increasing)
        
        # Check no duplicates
        suite.test("No duplicate timestamps", df.index.is_unique)
        
        # Check placeholder columns are 0
        suite.test("quote_asset_volume is 0", (df['quote_asset_volume'] == 0).all())
        suite.test("n_trades is 0", (df['n_trades'] == 0).all())
        suite.test("taker_buy_base_volume is 0", (df['taker_buy_base_volume'] == 0).all())
        suite.test("taker_buy_quote_volume is 0", (df['taker_buy_quote_volume'] == 0).all())
        
        # Check OHLCV values
        suite.test("Open values correct", df['open'].iloc[0] == 100.0)
        suite.test("High values correct", df['high'].iloc[0] == 105.0)
        suite.test("Low values correct", df['low'].iloc[0] == 98.0)
        suite.test("Close values correct", df['close'].iloc[0] == 103.0)
        suite.test("Volume values correct", df['volume'].iloc[0] == 1000.0)
        
    except Exception as e:
        suite.test("convert_ohlcv_to_dataframe", False, str(e))
    
    return suite.summary()


def test_unit_merge_and_sort():
    """Test 3: Unit test for merge and sort."""
    print("\n" + "="*80)
    print("Test 3: Merge and Sort")
    print("="*80)
    
    suite = TestSuite()
    
    try:
        # Create two DataFrames with overlap
        now = datetime.now(timezone.utc)
        
        # Existing data: 5 timestamps
        existing_data = {
            'open': [100, 101, 102, 103, 104],
            'high': [105, 106, 107, 108, 109],
            'low': [98, 99, 100, 101, 102],
            'close': [103, 104, 105, 106, 107],
            'volume': [1000, 1100, 1200, 1300, 1400],
            'quote_asset_volume': [0, 0, 0, 0, 0],
            'n_trades': [0, 0, 0, 0, 0],
            'taker_buy_base_volume': [0, 0, 0, 0, 0],
            'taker_buy_quote_volume': [0, 0, 0, 0, 0]
        }
        existing_index = pd.DatetimeIndex([
            now - timedelta(minutes=20),
            now - timedelta(minutes=15),
            now - timedelta(minutes=10),
            now - timedelta(minutes=5),
            now
        ], tz='UTC')
        existing_df = pd.DataFrame(existing_data, index=existing_index)
        
        # New data: 3 timestamps with overlap
        new_data = {
            'open': [103, 104, 105],
            'high': [108, 109, 110],
            'low': [101, 102, 103],
            'close': [106, 107, 108],
            'volume': [1300, 1400, 1500],
            'quote_asset_volume': [0, 0, 0],
            'n_trades': [0, 0, 0],
            'taker_buy_base_volume': [0, 0, 0],
            'taker_buy_quote_volume': [0, 0, 0]
        }
        new_index = pd.DatetimeIndex([
            now - timedelta(minutes=5),
            now,
            now + timedelta(minutes=5)
        ], tz='UTC')
        new_df = pd.DataFrame(new_data, index=new_index)
        
        # Merge
        merged = merge_and_sort(existing_df, new_df)
        
        # Check merged DataFrame
        suite.test("Merge produced DataFrame", not merged.empty)
        suite.test("Merged has 6 unique timestamps", len(merged) == 6, f"Got {len(merged)}")
        suite.test("Merged is sorted", merged.index.is_monotonic_increasing)
        suite.test("Merged has no duplicates", merged.index.is_unique)
        suite.test("Merged has timezone", merged.index.tz is not None)
        
        # Check overlap resolution (should keep last value)
        overlap_time = now
        if overlap_time in merged.index:
            suite.test(
                "Overlap resolved (kept last)",
                merged.loc[overlap_time, 'close'] == 107,  # New value
                f"Got {merged.loc[overlap_time, 'close']}"
            )
        
    except Exception as e:
        suite.test("merge_and_sort", False, str(e))
    
    return suite.summary()


async def test_integration_download_single_pool():
    """Test 4: Integration test - download data for single pool."""
    print("\n" + "="*80)
    print("Test 4: Integration Test - Single Pool Download")
    print("="*80)
    
    suite = TestSuite()
    
    try:
        # Check if pool mapping exists
        mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
        
        if not mapping_file.exists():
            print("  ⚠️  Pool mapping not found. Run pool mapping first:")
            print("     python scripts/build_pool_mapping.py --network base --connector gate_io")
            return False
        
        # Load pool mapping
        df = pd.read_parquet(mapping_file)
        top_pools = df[df['rank'] == 1].head(1)  # Just 1 pool for testing
        
        if top_pools.empty:
            print("  ⚠️  No pools found in mapping")
            return False
        
        pool = top_pools.iloc[0]
        trading_pair = pool['trading_pair']
        pool_address = pool['pool_address']
        
        print(f"  Testing with pool: {trading_pair} ({pool_address[:10]}...)")
        
        # Initialize data source
        gt_ds = GeckoTerminalDataSource(rate_limit_sleep=1.0)
        
        # Download 1 day of 5m data
        end_time = int(datetime.now(timezone.utc).timestamp())
        start_time = end_time - (1 * 86400)  # 1 day
        
        print(f"  Downloading 1 day of 5m data...")
        candles = await gt_ds.get_candles(
            network="base",
            pool_address=pool_address,
            trading_pair=trading_pair,
            interval="5m",
            start_time=start_time,
            end_time=end_time
        )
        
        # Check candles
        suite.test("Candles object returned", candles is not None)
        suite.test("Candles has data", not candles.data.empty, "No data returned")
        
        if not candles.data.empty:
            suite.test(
                f"Downloaded data (got {len(candles.data)} candles)",
                len(candles.data) > 0
            )
            
            # Save to parquet
            print(f"  Saving to parquet...")
            gt_ds.dump_candles_cache()
            
            # Verify file created
            expected_file = data_paths.candles_dir / f"geckoterminal_base|{trading_pair}|5m.parquet"
            suite.test("Parquet file created", expected_file.exists())
            
            if expected_file.exists():
                # Verify file content
                loaded_df = pd.read_parquet(expected_file)
                suite.test("Loaded DataFrame not empty", not loaded_df.empty)
                suite.test("Loaded data matches downloaded", len(loaded_df) >= len(candles.data))
                
                # Check schema
                expected_cols = ['open', 'high', 'low', 'close', 'volume',
                               'quote_asset_volume', 'n_trades',
                               'taker_buy_base_volume', 'taker_buy_quote_volume']
                has_all_cols = all(col in loaded_df.columns for col in expected_cols)
                suite.test("Parquet has correct schema", has_all_cols)
                
                # Check data quality
                suite.test("No NaN values", not loaded_df.isnull().any().any())
                suite.test("Index is unique", loaded_df.index.is_unique)
                suite.test("Index is sorted", loaded_df.index.is_monotonic_increasing)
                suite.test("Index has timezone", loaded_df.index.tz is not None)
                
                print(f"  ✓ File saved: {expected_file.name}")
                print(f"  ✓ Data range: {loaded_df.index.min()} to {loaded_df.index.max()}")
                print(f"  ✓ Total candles: {len(loaded_df)}")
        
    except Exception as e:
        suite.test("Single pool download", False, str(e))
        import traceback
        traceback.print_exc()
    
    return suite.summary()


async def test_integration_incremental_download():
    """Test 5: Integration test - incremental download."""
    print("\n" + "="*80)
    print("Test 5: Integration Test - Incremental Download")
    print("="*80)
    
    suite = TestSuite()
    
    try:
        # Check if pool mapping exists
        mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
        
        if not mapping_file.exists():
            print("  ⚠️  Pool mapping not found. Skipping incremental test.")
            return False
        
        # Load pool mapping
        df = pd.read_parquet(mapping_file)
        top_pools = df[df['rank'] == 1].head(1)
        
        if top_pools.empty:
            print("  ⚠️  No pools found")
            return False
        
        pool = top_pools.iloc[0]
        trading_pair = pool['trading_pair']
        pool_address = pool['pool_address']
        
        # Check if data exists from previous test
        parquet_file = data_paths.candles_dir / f"geckoterminal_base|{trading_pair}|5m.parquet"
        
        if not parquet_file.exists():
            print(f"  ⚠️  No existing data found. Run test 4 first.")
            return False
        
        # Load existing data
        existing_df = pd.read_parquet(parquet_file)
        initial_count = len(existing_df)
        initial_end = existing_df.index.max()
        
        print(f"  Existing data: {initial_count} candles")
        print(f"  Last timestamp: {initial_end}")
        
        # Initialize data source and load cache
        gt_ds = GeckoTerminalDataSource(rate_limit_sleep=1.0)
        gt_ds.load_candles_cache()
        
        # Download incremental data (from last timestamp - overlap)
        end_time = int(datetime.now(timezone.utc).timestamp())
        start_time = int(initial_end.timestamp()) - (10 * 300)  # 10 candles overlap for 5m
        
        print(f"  Downloading incremental data...")
        candles = await gt_ds.get_candles(
            network="base",
            pool_address=pool_address,
            trading_pair=trading_pair,
            interval="5m",
            start_time=start_time,
            end_time=end_time
        )
        
        # Save
        gt_ds.dump_candles_cache()
        
        # Load merged data
        merged_df = pd.read_parquet(parquet_file)
        final_count = len(merged_df)
        
        print(f"  Merged data: {final_count} candles")
        
        # Check incremental behavior
        suite.test(
            "Data was added",
            final_count >= initial_count,
            f"Count decreased: {initial_count} -> {final_count}"
        )
        
        suite.test("No duplicates after merge", merged_df.index.is_unique)
        suite.test("Still sorted after merge", merged_df.index.is_monotonic_increasing)
        suite.test("No NaN after merge", not merged_df.isnull().any().any())
        
        new_candles = final_count - initial_count
        print(f"  ✓ Added {new_candles} new candles")
        
    except Exception as e:
        suite.test("Incremental download", False, str(e))
        import traceback
        traceback.print_exc()
    
    return suite.summary()


async def test_data_validation():
    """Test 6: Data validation - check quality of downloaded data."""
    print("\n" + "="*80)
    print("Test 6: Data Validation")
    print("="*80)
    
    suite = TestSuite()
    
    try:
        # Find all DEX parquet files
        pattern = "geckoterminal_*.parquet"
        files = list(data_paths.candles_dir.glob(pattern))
        
        if not files:
            print("  ⚠️  No DEX data files found. Run previous tests first.")
            return False
        
        print(f"  Found {len(files)} DEX data files")
        
        for file in files:
            print(f"\n  Validating: {file.name}")
            
            df = pd.read_parquet(file)
            
            # Basic checks
            suite.test(f"{file.name}: Not empty", not df.empty)
            suite.test(f"{file.name}: Has data", len(df) > 0)
            
            # Schema checks
            expected_cols = ['open', 'high', 'low', 'close', 'volume',
                           'quote_asset_volume', 'n_trades',
                           'taker_buy_base_volume', 'taker_buy_quote_volume']
            has_all_cols = all(col in df.columns for col in expected_cols)
            suite.test(f"{file.name}: Correct schema", has_all_cols)
            
            # Data quality checks
            suite.test(f"{file.name}: No NaN", not df.isnull().any().any())
            suite.test(f"{file.name}: Unique timestamps", df.index.is_unique)
            suite.test(f"{file.name}: Sorted timestamps", df.index.is_monotonic_increasing)
            suite.test(f"{file.name}: Has timezone", df.index.tz is not None)
            
            # Check for gaps (allow 50% tolerance)
            if len(df) > 1:
                # Extract interval from filename
                interval_str = file.stem.split('|')[-1]
                expected_gap = interval_to_seconds(interval_str)
                
                time_diff = df.index.to_series().diff().dropna()
                actual_gaps = time_diff.dt.total_seconds()
                
                # Count significant gaps (more than 1.5x expected)
                significant_gaps = (actual_gaps > expected_gap * 1.5).sum()
                gap_ratio = significant_gaps / len(time_diff) if len(time_diff) > 0 else 0
                
                suite.test(
                    f"{file.name}: Reasonable continuity",
                    gap_ratio < 0.5,  # Less than 50% gaps
                    f"Gap ratio: {gap_ratio:.2%}"
                )
            
            # OHLC validity
            suite.test(f"{file.name}: High >= Low", (df['high'] >= df['low']).all())
            suite.test(f"{file.name}: High >= Open", (df['high'] >= df['open']).all())
            suite.test(f"{file.name}: High >= Close", (df['high'] >= df['close']).all())
            suite.test(f"{file.name}: Low <= Open", (df['low'] <= df['open']).all())
            suite.test(f"{file.name}: Low <= Close", (df['low'] <= df['close']).all())
            
            # Positive values
            suite.test(f"{file.name}: Positive prices", (df[['open', 'high', 'low', 'close']] > 0).all().all())
            suite.test(f"{file.name}: Non-negative volume", (df['volume'] >= 0).all())
            
            print(f"    Range: {df.index.min()} to {df.index.max()}")
            print(f"    Count: {len(df)} candles")
            print(f"    Price: ${df['close'].min():.4f} - ${df['close'].max():.4f}")
        
    except Exception as e:
        suite.test("Data validation", False, str(e))
        import traceback
        traceback.print_exc()
    
    return suite.summary()


async def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("🧪 DEX OHLCV System - Comprehensive Test Suite")
    print("="*80)
    print()
    
    all_passed = True
    
    # Unit tests
    print("\n" + "━"*80)
    print("UNIT TESTS")
    print("━"*80)
    
    all_passed &= test_unit_interval_parsing()
    all_passed &= test_unit_data_conversion()
    all_passed &= test_unit_merge_and_sort()
    
    # Integration tests
    print("\n" + "━"*80)
    print("INTEGRATION TESTS")
    print("━"*80)
    
    all_passed &= await test_integration_download_single_pool()
    all_passed &= await test_integration_incremental_download()
    
    # Data validation
    print("\n" + "━"*80)
    print("DATA VALIDATION")
    print("━"*80)
    
    all_passed &= await test_data_validation()
    
    # Final summary
    print("\n" + "="*80)
    print("🎯 FINAL RESULT")
    print("="*80)
    
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nThe DEX OHLCV system is working correctly.")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease review the failed tests above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

