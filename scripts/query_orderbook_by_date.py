#!/usr/bin/env python3
"""
按日期查询订单簿数据示例

使用方法：
    # 查询单天
    python scripts/query_orderbook_by_date.py --pair VIRTUAL-USDT --date 20251116
    
    # 查询日期范围
    python scripts/query_orderbook_by_date.py --pair VIRTUAL-USDT --start 20251110 --end 20251116
    
    # 查询所有数据
    python scripts/query_orderbook_by_date.py --pair VIRTUAL-USDT
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots


def main():
    parser = argparse.ArgumentParser(description='按日期查询订单簿数据')
    parser.add_argument('--exchange', default='gate_io', help='交易所名称')
    parser.add_argument('--pair', required=True, help='交易对（如 VIRTUAL-USDT）')
    parser.add_argument('--date', help='查询单天数据（YYYYMMDD格式）')
    parser.add_argument('--start', help='开始日期（YYYYMMDD格式）')
    parser.add_argument('--end', help='结束日期（YYYYMMDD格式）')
    
    args = parser.parse_args()
    
    # 处理参数
    if args.date:
        start_date = args.date
        end_date = args.date
        print(f"🔍 查询 {args.pair} 在 {args.date} 的数据...")
    elif args.start and args.end:
        start_date = args.start
        end_date = args.end
        print(f"🔍 查询 {args.pair} 从 {args.start} 到 {args.end} 的数据...")
    else:
        start_date = None
        end_date = None
        print(f"🔍 查询 {args.pair} 的所有数据...")
    
    print()
    
    # 加载数据
    try:
        df = load_orderbook_snapshots(
            connector_name=args.exchange,
            trading_pair=args.pair,
            start_date=start_date,
            end_date=end_date
        )
        
        if df.empty:
            print("❌ 没有找到数据")
            return
        
        # 显示统计信息
        print("=" * 80)
        print("📊 数据统计")
        print("=" * 80)
        print()
        
        print(f"记录总数: {len(df):,} 条")
        print(f"时间范围: {df['timestamp'].min()} 至 {df['timestamp'].max()}")
        print(f"时长: {df['timestamp'].max() - df['timestamp'].min()}")
        print()
        
        # 按天统计
        df['date'] = df['timestamp'].dt.date
        daily_counts = df.groupby('date').size()
        
        print(f"包含天数: {len(daily_counts)} 天")
        print()
        
        print("每天记录数:")
        for date, count in daily_counts.items():
            print(f"  {date}: {count:,} 条")
        print()
        
        # 价格统计
        print("价格统计:")
        print(f"  最佳买价: {df['best_bid_price'].min():.6f} - {df['best_bid_price'].max():.6f}")
        print(f"  最佳卖价: {df['best_ask_price'].min():.6f} - {df['best_ask_price'].max():.6f}")
        print(f"  平均价差: {((df['best_ask_price'] - df['best_bid_price']) / df['best_bid_price'] * 100).mean():.3f}%")
        print()
        
        # Update ID 统计
        if 'update_id' in df.columns:
            print("Update ID 统计:")
            print(f"  范围: {df['update_id'].min():.0f} - {df['update_id'].max():.0f}")
            print(f"  增长: {df['update_id'].max() - df['update_id'].min():.0f}")
            print()
        
        # 显示前几条记录
        print("=" * 80)
        print("📋 前 5 条记录")
        print("=" * 80)
        print()
        
        for i, row in df.head(5).iterrows():
            print(f"记录 {i+1}:")
            print(f"  时间: {row['timestamp']}")
            print(f"  买价: {row['best_bid_price']:.6f} (数量: {row['best_bid_amount']:.4f})")
            print(f"  卖价: {row['best_ask_price']:.6f} (数量: {row['best_ask_amount']:.4f})")
            if 'update_id' in df.columns:
                print(f"  Update ID: {row['update_id']:.0f}")
            print()
        
        print("=" * 80)
        print("✅ 查询完成")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

