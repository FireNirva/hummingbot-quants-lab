#!/usr/bin/env python3
"""
临时脚本：立即下载 DEX 数据
绕过 trigger-task 的 bug
"""
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app.tasks.data_collection.dex_candles_downloader import DexCandlesDownloader
from core.tasks.base import TaskConfig, ScheduleConfig


async def main():
    """执行 DEX 数据下载"""
    print("="*80)
    print("🚀 开始 DEX 数据下载")
    print("="*80)
    print()
    
    # 创建任务配置（使用 config/dex_candles_base.yml 的配置）
    config = TaskConfig(
        name='manual_dex_download',
        task_class='app.tasks.data_collection.dex_candles_downloader.DexCandlesDownloader',
        enabled=True,
        schedule=ScheduleConfig(
            type='frequency',
            frequency_hours=1.0
        ),
        config={
            'network': 'base',
            'connector': 'gate_io',
            'intervals': ['1m'],
            'lookback_days': 7,
            'start_from_cex': True,      # 从 CEX 数据开始时间对齐
            'rate_limit_sleep': 0.5,     # 加快下载速度
            'max_requests': 200          # 1m 数据需要更多请求
        }
    )
    
    # 创建任务实例
    task = DexCandlesDownloader(config)
    
    try:
        print("📋 初始化任务...")
        task.setup()
        
        print("⬇️  开始下载...")
        await task.execute()
        
        print()
        print("="*80)
        print("✅ DEX 数据下载完成！")
        print("="*80)
        
    except Exception as e:
        print()
        print("="*80)
        print(f"❌ 下载失败: {e}")
        print("="*80)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

