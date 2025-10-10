#!/usr/bin/env python3
"""
测试 QuantsLab 的增量追加功能
"""
import pandas as pd
import asyncio
from pathlib import Path
from datetime import datetime, timezone

# 导入 QuantsLab 组件
from core.data_sources.clob import CLOBDataSource

async def test_incremental_append():
    """测试增量追加数据到现有 Parquet 文件"""
    
    print("="*80)
    print("测试 QuantsLab 增量追加功能")
    print("="*80)
    
    # 测试参数
    connector = "gate_io"
    trading_pair = "VIRTUAL-USDT"
    interval = "1m"
    
    # Parquet 文件路径
    cache_dir = Path("app/data/cache/candles")
    parquet_file = cache_dir / f"{connector}|{trading_pair}|{interval}.parquet"
    
    # 1. 读取现有数据
    print(f"\n📊 步骤 1: 读取现有数据")
    print(f"文件: {parquet_file}")
    
    if parquet_file.exists():
        existing_df = pd.read_parquet(parquet_file)
        print(f"✓ 现有数据:")
        print(f"  - 行数: {len(existing_df):,}")
        print(f"  - 时间范围: {existing_df.index.min()} 到 {existing_df.index.max()}")
        
        # 计算时间跨度
        time_span = existing_df.index.max() - existing_df.index.min()
        print(f"  - 跨度: {time_span.total_seconds() / 86400:.2f} 天")
    else:
        print(f"❌ 文件不存在: {parquet_file}")
        return
    
    # 2. 使用 CLOBDataSource 获取最新数据
    print(f"\n📥 步骤 2: 下载最新数据 (0.5天 = 720分钟)")
    
    try:
        clob = CLOBDataSource()
        
        # 计算时间范围：从现在往前0.5天
        end_time = int(datetime.now(timezone.utc).timestamp())
        start_time = end_time - int(0.5 * 24 * 60 * 60)  # 0.5天前
        
        print(f"  - 时间范围: {datetime.fromtimestamp(start_time, timezone.utc)} 到 {datetime.fromtimestamp(end_time, timezone.utc)}")
        
        new_candles = await clob.get_candles(
            connector_name=connector,
            trading_pair=trading_pair,
            interval=interval,
            start_time=start_time,
            end_time=end_time
        )
        
        # Candles 对象的数据在 .data 属性中
        new_candles_df = new_candles.data
        
        if new_candles_df is not None and not new_candles_df.empty:
            print(f"✓ 下载成功:")
            print(f"  - 行数: {len(new_candles_df):,}")
            print(f"  - 时间范围: {new_candles_df.index.min()} 到 {new_candles_df.index.max()}")
        else:
            print(f"❌ 下载失败或无新数据")
            return
            
    except Exception as e:
        print(f"❌ 下载出错: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. 合并数据（模拟 append 行为）
    print(f"\n🔄 步骤 3: 合并数据")
    
    # 统一时区 (确保都是 UTC tz-aware)
    if new_candles_df.index.tz is None:
        new_candles_df.index = pd.to_datetime(new_candles_df.index, utc=True)
    if existing_df.index.tz is None:
        existing_df.index = pd.to_datetime(existing_df.index, utc=True)
    
    # 合并并去重
    combined_df = pd.concat([existing_df, new_candles_df])
    combined_df = combined_df[~combined_df.index.duplicated(keep='last')]
    combined_df = combined_df.sort_index()
    
    print(f"✓ 合并后:")
    print(f"  - 总行数: {len(combined_df):,} (之前: {len(existing_df):,}, 新增: {len(combined_df) - len(existing_df):,})")
    print(f"  - 时间范围: {combined_df.index.min()} 到 {combined_df.index.max()}")
    
    time_span_new = combined_df.index.max() - combined_df.index.min()
    print(f"  - 新跨度: {time_span_new.total_seconds() / 86400:.2f} 天")
    
    # 4. 保存（可选）
    print(f"\n💾 步骤 4: 保存结果")
    
    # 创建备份文件名
    backup_file = cache_dir / f"{connector}|{trading_pair}|{interval}.backup.parquet"
    
    print(f"  - 备份原文件: {backup_file}")
    existing_df.to_parquet(backup_file)
    
    print(f"  - 保存合并数据: {parquet_file}")
    combined_df.to_parquet(parquet_file)
    
    print(f"\n✅ 测试完成！")
    print(f"\n📈 结果总结:")
    print(f"  - 原始数据: {len(existing_df):,} 行")
    print(f"  - 新下载: {len(new_candles_df):,} 行")
    print(f"  - 合并后: {len(combined_df):,} 行")
    print(f"  - 实际新增: {len(combined_df) - len(existing_df):,} 行")
    print(f"  - 时间扩展: {time_span.total_seconds() / 86400:.2f} 天 → {time_span_new.total_seconds() / 86400:.2f} 天")


if __name__ == "__main__":
    asyncio.run(test_incremental_append())

