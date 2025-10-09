#!/usr/bin/env python3
"""
Parquet 文件查看工具

使用方法:
  python scripts/view_parquet.py <文件路径>
  python scripts/view_parquet.py app/data/cache/candles/gate_io|VIRTUAL-USDT|1m.parquet
  
或者查看所有文件:
  python scripts/view_parquet.py --all
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

def format_number(num):
    """格式化数字显示"""
    if num >= 1e9:
        return f"{num/1e9:.2f}B"
    elif num >= 1e6:
        return f"{num/1e6:.2f}M"
    elif num >= 1e3:
        return f"{num/1e3:.2f}K"
    else:
        return f"{num:.2f}"

def view_parquet(file_path):
    """查看单个 parquet 文件"""
    try:
        print(f"\n{'='*80}")
        print(f"文件: {file_path}")
        print(f"{'='*80}")
        
        # 读取文件
        df = pd.read_parquet(file_path)
        
        # 基本信息
        print(f"\n📊 基本信息:")
        print(f"  - 总行数: {len(df):,}")
        print(f"  - 列数: {len(df.columns)}")
        print(f"  - 文件大小: {Path(file_path).stat().st_size / 1024:.2f} KB")
        
        # 时间范围
        if 'timestamp' in df.columns or isinstance(df.index, pd.DatetimeIndex):
            time_col = df.index if isinstance(df.index, pd.DatetimeIndex) else df['timestamp']
            print(f"\n📅 时间范围:")
            print(f"  - 开始: {time_col.min()}")
            print(f"  - 结束: {time_col.max()}")
            print(f"  - 跨度: {(time_col.max() - time_col.min()).days} 天")
        
        # 列信息
        print(f"\n📋 数据列:")
        for col in df.columns:
            print(f"  - {col}: {df[col].dtype}")
        
        # 前几行数据
        print(f"\n📈 前 5 行数据:")
        print(df.head().to_string())
        
        # 统计信息
        if len(df.select_dtypes(include=['number']).columns) > 0:
            print(f"\n📊 数据统计:")
            stats = df.describe()
            print(stats.to_string())
        
        # OHLC 特定信息（如果是K线数据）
        if all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']):
            print(f"\n💹 K线数据摘要:")
            print(f"  - 最高价: ${df['high'].max():,.2f}")
            print(f"  - 最低价: ${df['low'].min():,.2f}")
            print(f"  - 平均成交量: {format_number(df['volume'].mean())}")
            print(f"  - 总成交量: {format_number(df['volume'].sum())}")
            if 'quote_asset_volume' in df.columns:
                print(f"  - 总成交额: ${format_number(df['quote_asset_volume'].sum())}")
        
        # 数据完整性
        print(f"\n✅ 数据完整性:")
        missing = df.isnull().sum()
        if missing.sum() == 0:
            print("  - 无缺失值 ✓")
        else:
            print("  - 缺失值:")
            for col, count in missing[missing > 0].items():
                print(f"    {col}: {count} ({count/len(df)*100:.2f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def view_all_candles():
    """查看所有K线数据文件"""
    candles_dir = Path("app/data/cache/candles")
    
    if not candles_dir.exists():
        print(f"❌ 目录不存在: {candles_dir}")
        return
    
    parquet_files = list(candles_dir.glob("*.parquet"))
    
    if not parquet_files:
        print(f"📁 {candles_dir} 目录下没有 parquet 文件")
        return
    
    print(f"\n{'='*80}")
    print(f"找到 {len(parquet_files)} 个 parquet 文件")
    print(f"{'='*80}\n")
    
    # 汇总信息
    summary = []
    for file_path in sorted(parquet_files):
        try:
            df = pd.read_parquet(file_path)
            
            # 解析文件名
            parts = file_path.stem.split('|')
            connector = parts[0] if len(parts) > 0 else 'unknown'
            pair = parts[1] if len(parts) > 1 else 'unknown'
            interval = parts[2] if len(parts) > 2 else 'unknown'
            
            time_col = df.index if isinstance(df.index, pd.DatetimeIndex) else df['timestamp']
            
            summary.append({
                '交易所': connector,
                '交易对': pair,
                '周期': interval,
                '数据量': len(df),
                '开始时间': time_col.min(),
                '结束时间': time_col.max(),
                '文件大小(KB)': f"{file_path.stat().st_size / 1024:.2f}"
            })
        except Exception as e:
            print(f"⚠️  无法读取 {file_path.name}: {e}")
    
    # 打印汇总表格
    if summary:
        summary_df = pd.DataFrame(summary)
        print(summary_df.to_string(index=False))
        print(f"\n总计: {len(summary)} 个文件")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n当前可用的文件:")
        view_all_candles()
        return
    
    if sys.argv[1] == '--all' or sys.argv[1] == '-a':
        view_all_candles()
    elif sys.argv[1] == '--help' or sys.argv[1] == '-h':
        print(__doc__)
    else:
        file_path = sys.argv[1]
        if not Path(file_path).exists():
            print(f"❌ 文件不存在: {file_path}")
            sys.exit(1)
        view_parquet(file_path)

if __name__ == "__main__":
    main()

