#!/usr/bin/env python3
"""
立即测试 SimpleCandlesDownloader 的增量下载功能
"""
import asyncio
import yaml
from pathlib import Path
from datetime import datetime, timezone

# 导入 QuantsLab 组件
from app.tasks.data_collection.simple_candles_downloader import SimpleCandlesDownloader
from core.data_sources.clob import CLOBDataSource

async def test_download():
    """直接运行下载任务"""
    
    print("="*80)
    print(f"开始测试下载 - {datetime.now(timezone.utc)}")
    print("="*80)
    
    # 加载配置
    config_path = "config/base_ecosystem_downloader_full.yml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    task_full_config = config['tasks']['gateio_base_ecosystem_downloader']
    task_config = task_full_config['config']
    
    print(f"\n📋 配置信息:")
    print(f"  - 交易所: {task_config['connector_name']}")
    print(f"  - 交易对数量: {len(task_config['trading_pairs'])}")
    print(f"  - 时间间隔: {task_config['intervals']}")
    print(f"  - 数据保留天数: {task_config.get('days_data_retention', 7)}")
    
    # 初始化下载器
    print(f"\n🚀 初始化下载器...")
    clob = CLOBDataSource()
    downloader = SimpleCandlesDownloader(task_config, clob)
    downloader.setup()
    
    # 执行下载
    print(f"\n📥 开始下载...")
    print(f"时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
    
    try:
        result = await downloader.execute()
        
        print(f"\n✅ 下载完成!")
        print(f"\n📊 结果统计:")
        print(f"  - 处理交易对: {result.get('pairs_processed', 0)}/{result.get('pairs_total', 0)}")
        print(f"  - 处理时间间隔: {result.get('intervals_processed', 0)}")
        print(f"  - 下载K线数量: {result.get('candles_downloaded', 0):,}")
        print(f"  - 错误数量: {result.get('errors', 0)}")
        
        if result.get('errors', 0) > 0:
            print(f"\n⚠️  警告: 有 {result['errors']} 个错误")
        else:
            print(f"\n🎉 所有交易对下载成功！")
            
    except Exception as e:
        print(f"\n❌ 下载失败: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*80}")
    print(f"测试完成 - {datetime.now(timezone.utc)}")
    print(f"{'='*80}")

if __name__ == "__main__":
    asyncio.run(test_download())

