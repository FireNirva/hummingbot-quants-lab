#!/usr/bin/env python3
"""
运行 DEX 下载任务 - 与 CEX 时间对齐

此脚本用于测试 DEX 数据下载并与现有 CEX 数据进行时间对齐。
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


async def run_aligned_download():
    """运行与 CEX 对齐的 DEX 下载任务。"""
    print("="*80)
    print("🚀 DEX 下载任务 - 与 CEX 时间对齐")
    print("="*80)
    print()
    
    # 检查 CEX 数据
    print("📊 检查现有 CEX 数据...")
    cex_files = list(data_paths.candles_dir.glob("gate_io|*-USDT|1m.parquet"))
    
    if not cex_files:
        print("❌ 没有找到 CEX 1m 数据！")
        return False
    
    print(f"✓ 找到 {len(cex_files)} 个 CEX 1m 数据文件")
    
    # 显示一个示例
    example_file = cex_files[0]
    df = pd.read_parquet(example_file)
    pair = example_file.stem.split('|')[1]
    print(f"\n示例 - {pair}:")
    print(f"  时间范围: {df.index.min()} 至 {df.index.max()}")
    print(f"  K线数量: {len(df):,} 根")
    print()
    
    # 检查池子映射
    mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
    
    if not mapping_file.exists():
        print("❌ 池子映射不存在！")
        print("   请先运行: python scripts/build_pool_mapping.py --network base --connector gate_io")
        return False
    
    pool_df = pd.read_parquet(mapping_file)
    top_pools = pool_df[pool_df['rank'] == 1]
    
    print(f"📋 准备下载的池子 ({len(top_pools)} 个):")
    for _, pool in top_pools.iterrows():
        print(f"  • {pool['trading_pair']}")
    print()
    
    # 创建任务配置
    config_dict = {
        "name": "dex_candles_downloader",
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
            "intervals": ["1m"],
            "lookback_days": 7,
            "start_from_cex": True,  # 🔥 关键：启用 CEX 对齐
            "rate_limit_sleep": 1.0,
            "max_requests": 200
        }
    }
    
    schedule = ScheduleConfig(**config_dict["schedule"])
    task_config = TaskConfig(
        name=config_dict["name"],
        task_class=config_dict["task_class"],
        enabled=config_dict["enabled"],
        schedule=schedule,
        config=config_dict["config"]
    )
    
    print("✓ 任务配置创建成功")
    print()
    
    # 创建任务实例
    task = DexCandlesDownloader(task_config)
    
    # 创建任务上下文
    context = TaskContext(
        task_name="dex_candles_downloader",
        execution_id="aligned_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    )
    
    print(f"📝 执行 ID: {context.execution_id}")
    print()
    
    # 设置任务
    print("🔧 设置任务...")
    try:
        await task.setup(context)
        print("✓ 任务设置完成")
        print()
    except Exception as e:
        print(f"❌ 任务设置失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 执行任务
    print("🚀 开始下载 DEX 数据（与 CEX 时间对齐）...")
    print("   ⏳ 这可能需要几分钟，请耐心等待...")
    print()
    
    try:
        result = await task.execute(context)
        print("✓ 任务执行完成")
        print()
        
        # 显示结果
        print("="*80)
        print("📊 下载结果")
        print("="*80)
        print(f"状态: {result.get('status', 'unknown')}")
        print()
        
        stats = result.get('stats', {})
        print("统计:")
        print(f"  总交易对: {stats.get('pairs_total', 0)}")
        print(f"  成功: {stats.get('pairs_success', 0)}")
        print(f"  失败: {stats.get('pairs_failed', 0)}")
        print(f"  获取K线数: {stats.get('candles_fetched', 0):,}")
        print(f"  API 请求数: {stats.get('requests_made', 0)}")
        print()
        
        if stats.get('failed_pairs'):
            print("⚠️  失败的交易对:")
            for pair in stats['failed_pairs']:
                print(f"  • {pair}")
            print()
        
        return result.get('status') == 'completed'
        
    except Exception as e:
        print(f"❌ 任务执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # 清理
        try:
            await task.cleanup(context, None)
        except:
            pass


async def main():
    """主函数。"""
    success = await run_aligned_download()
    
    if success:
        print("="*80)
        print("✅ DEX 数据下载成功！")
        print("="*80)
        print()
        print("📁 数据位置: app/data/cache/candles/")
        print("   文件格式: geckoterminal_base|{交易对}|1m.parquet")
        print()
        print("下一步: 运行验证脚本检查时间对齐")
        print("  python scripts/verify_cex_dex_alignment.py")
        print()
        return 0
    else:
        print("="*80)
        print("❌ DEX 数据下载失败")
        print("="*80)
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

