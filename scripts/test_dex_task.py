#!/usr/bin/env python3
"""
Test DEX Candles Downloader Task

Test the task system integration for DEX OHLCV downloads.
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.tasks import TaskContext, TaskConfig, ScheduleConfig
from app.tasks.data_collection.dex_candles_downloader import DexCandlesDownloader
from core.data_paths import data_paths


async def test_task_minimal():
    """Test task with minimal configuration (1-2 pools only)."""
    print("="*80)
    print("🧪 Testing DEX Candles Downloader Task")
    print("="*80)
    print()
    
    # Check prerequisites
    mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
    
    if not mapping_file.exists():
        print("❌ Pool mapping not found!")
        print("   Please run: python scripts/build_pool_mapping.py --network base --connector gate_io")
        return False
    
    print("✓ Pool mapping found")
    
    # Load mapping and limit to 2 pools for testing
    df = pd.read_parquet(mapping_file)
    top_pools = df[df['rank'] == 1].head(2)
    
    print(f"✓ Testing with {len(top_pools)} pools:")
    for _, pool in top_pools.iterrows():
        print(f"  - {pool['trading_pair']}")
    print()
    
    # Create minimal task config
    config_dict = {
        "name": "test_dex_candles",
        "task_class": "app.tasks.data_collection.dex_candles_downloader.DexCandlesDownloader",
        "enabled": True,
        "schedule": {
            "type": "frequency",
            "frequency_hours": 1.0,
            "timezone": "UTC"
        },
        "config": {
            "network": "base",
            "connector": "gate_io",
            "intervals": ["5m"],  # Only 5m for testing
            "lookback_days": 1,   # Only 1 day
            "start_from_cex": False,
            "rate_limit_sleep": 1.0,
            "max_requests": 10    # Limit requests for testing
        }
    }
    
    # Create TaskConfig
    schedule = ScheduleConfig(**config_dict["schedule"])
    task_config = TaskConfig(
        name=config_dict["name"],
        task_class=config_dict["task_class"],
        enabled=config_dict["enabled"],
        schedule=schedule,
        config=config_dict["config"]
    )
    
    print("✓ Task config created")
    print()
    
    # Create task instance
    task = DexCandlesDownloader(task_config)
    
    print("✓ Task instance created")
    print()
    
    # Create task context
    context = TaskContext(
        task_name="test_dex_candles",
        execution_id="test_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    )
    
    print("✓ Task context created")
    print(f"  Execution ID: {context.execution_id}")
    print()
    
    # Setup task
    print("🔧 Setting up task...")
    try:
        await task.setup(context)
        print("✓ Task setup complete")
        print()
    except Exception as e:
        print(f"❌ Task setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Execute task
    print("🚀 Executing task...")
    print("   (This may take a few minutes...)")
    print()
    
    try:
        result = await task.execute(context)
        print("✓ Task execution complete")
        print()
        
        # Print results
        print("="*80)
        print("📊 Execution Results")
        print("="*80)
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Timestamp: {result.get('timestamp', 'unknown')}")
        print()
        
        stats = result.get('stats', {})
        print("Statistics:")
        print(f"  Total pairs: {stats.get('pairs_total', 0)}")
        print(f"  Success: {stats.get('pairs_success', 0)}")
        print(f"  Failed: {stats.get('pairs_failed', 0)}")
        print(f"  Candles fetched: {stats.get('candles_fetched', 0):,}")
        print(f"  API requests: {stats.get('requests_made', 0)}")
        print()
        
        if stats.get('failed_pairs'):
            print("Failed pairs:")
            for pair in stats['failed_pairs']:
                print(f"  - {pair}")
            print()
        
        # Verify files were created
        print("="*80)
        print("📁 Verifying Output Files")
        print("="*80)
        
        created_files = []
        for _, pool in top_pools.iterrows():
            trading_pair = pool['trading_pair']
            expected_file = data_paths.candles_dir / f"geckoterminal_base|{trading_pair}|5m.parquet"
            
            if expected_file.exists():
                df = pd.read_parquet(expected_file)
                created_files.append((expected_file.name, len(df)))
                print(f"✓ {expected_file.name}: {len(df)} candles")
            else:
                print(f"✗ {expected_file.name}: Not found")
        
        print()
        
        # Success criteria
        success = (
            result.get('status') == 'completed' and
            stats.get('candles_fetched', 0) > 0 and
            len(created_files) > 0
        )
        
        if success:
            print("="*80)
            print("✅ TASK TEST PASSED")
            print("="*80)
            print()
            print("Summary:")
            print(f"  - Downloaded data for {len(created_files)} pairs")
            print(f"  - Total candles: {stats.get('candles_fetched', 0):,}")
            print(f"  - Files created in: {data_paths.candles_dir}")
            print()
            return True
        else:
            print("="*80)
            print("❌ TASK TEST FAILED")
            print("="*80)
            print()
            print("Reasons:")
            if result.get('status') != 'completed':
                print(f"  - Status: {result.get('status')}")
            if stats.get('candles_fetched', 0) == 0:
                print("  - No candles fetched")
            if len(created_files) == 0:
                print("  - No files created")
            print()
            return False
        
    except Exception as e:
        print(f"❌ Task execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        try:
            await task.cleanup(context, None)
            print("✓ Task cleanup complete")
        except:
            pass


async def main():
    """Run task test."""
    success = await test_task_minimal()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

