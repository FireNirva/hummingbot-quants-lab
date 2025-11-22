#!/usr/bin/env python3
"""
检查MEXC历史数据的内容和类型
"""

import pandas as pd
from pathlib import Path
import sys

def check_mexc_data():
    data_dir = Path("app/data/raw/orderbook_ticks")
    
    print("=" * 80)
    print("📊 MEXC历史数据分析")
    print("=" * 80)
    print()
    
    # 找到所有MEXC分区
    mexc_partitions = sorted([d for d in data_dir.iterdir() if d.is_dir() and 'mexc' in d.name.lower()])
    
    if not mexc_partitions:
        print("❌ 未找到MEXC数据分区")
        return
    
    print(f"找到 {len(mexc_partitions)} 个MEXC分区")
    print()
    
    # 按日期分组
    by_date = {}
    for partition in mexc_partitions:
        date = partition.name.split('_')[-1]
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(partition)
    
    # 分析每天的数据
    print("━" * 80)
    print("📅 按日期统计:")
    print("━" * 80)
    print()
    
    total_files = 0
    total_rows = 0
    
    for date in sorted(by_date.keys()):
        partitions = by_date[date]
        date_files = 0
        date_rows = 0
        date_size = 0
        
        print(f"📆 {date}")
        print(f"   分区数: {len(partitions)}")
        
        for partition in partitions:
            parquet_files = list(partition.glob("*.parquet"))
            date_files += len(parquet_files)
            
            # 计算大小
            partition_size = sum(f.stat().st_size for f in parquet_files)
            date_size += partition_size
            
            # 读取第一个文件来检查数据类型
            if parquet_files and len(parquet_files) > 0:
                try:
                    sample_file = parquet_files[0]
                    df = pd.read_parquet(sample_file)
                    date_rows += len(df)
                    
                    # 只对第一个分区显示详细信息
                    if partition == partitions[0]:
                        print(f"\n   📄 样本文件: {sample_file.name}")
                        print(f"      Columns: {list(df.columns)}")
                        print(f"      Rows: {len(df)}")
                        
                        # 检查是否是snapshot还是diff
                        if 'snapshot_flag' in df.columns:
                            snapshot_count = df['snapshot_flag'].sum()
                            diff_count = len(df) - snapshot_count
                            print(f"      Snapshot rows: {snapshot_count}")
                            print(f"      Diff rows: {diff_count}")
                            print(f"      类型: {'✅ Tick Diff数据' if diff_count > 0 else '⚠️ 仅Snapshot数据'}")
                        
                        # 显示时间范围
                        if 'timestamp' in df.columns:
                            print(f"      时间范围: {df['timestamp'].min()} → {df['timestamp'].max()}")
                        
                        # 显示交易对
                        if 'trading_pair' in df.columns:
                            print(f"      交易对: {df['trading_pair'].unique()}")
                
                except Exception as e:
                    print(f"   ⚠️  读取失败: {e}")
        
        print(f"\n   总计:")
        print(f"      文件数: {date_files}")
        print(f"      总大小: {date_size / 1024 / 1024:.2f} MB")
        print()
        
        total_files += date_files
        total_rows += date_rows
    
    print("━" * 80)
    print("📊 总体统计:")
    print("━" * 80)
    print(f"   总分区数: {len(mexc_partitions)}")
    print(f"   总文件数: {total_files}")
    print(f"   覆盖天数: {len(by_date)}")
    print()
    
    # 检查最新数据
    print("━" * 80)
    print("🔍 最新数据检查 (今天):")
    print("━" * 80)
    print()
    
    latest_date = max(by_date.keys())
    latest_partitions = by_date[latest_date]
    
    for partition in latest_partitions:
        symbol = partition.name.split('_')[1]
        parquet_files = sorted(partition.glob("*.parquet"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if parquet_files:
            latest_file = parquet_files[0]
            latest_time = pd.Timestamp.fromtimestamp(latest_file.stat().st_mtime)
            
            print(f"   {symbol:20s} - 最后更新: {latest_time.strftime('%H:%M:%S')}")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    check_mexc_data()

