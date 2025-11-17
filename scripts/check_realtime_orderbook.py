#!/usr/bin/env python3
"""
实时检查订单簿采集状态

使用方法：
    python scripts/check_realtime_orderbook.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime, timedelta, timezone
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots
from core.data_paths import data_paths


def check_realtime_status():
    """检查实时采集状态"""
    
    print("=" * 80)
    print("📊 Gate.io 订单簿实时采集状态")
    print("=" * 80)
    print()
    
    # Gate.io 交易对
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    total_records = 0
    
    for pair in gate_pairs:
        print(f"📋 {pair}:")
        
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty:
                print(f"   ⚠️ 无数据")
                continue
            
            # 基本信息
            print(f"   📊 总记录数: {len(df)}")
            total_records += len(df)
            
            # 时间范围
            if 'timestamp' in df.columns:
                first_time = df['timestamp'].min()
                last_time = df['timestamp'].max()
                duration = last_time - first_time
                
                print(f"   ⏰ 第一条: {first_time}")
                print(f"   ⏰ 最后一条: {last_time}")
                print(f"   ⏱️ 持续时间: {duration}")
                
                # 计算采集频率
                if len(df) > 1:
                    time_diffs = df['timestamp'].diff().dropna()
                    avg_interval = time_diffs.mean()
                    print(f"   📈 平均间隔: {avg_interval.total_seconds():.2f} 秒")
            
            # Update ID 信息
            if 'update_id' in df.columns and len(df) > 0:
                print(f"   🔢 Update ID 范围: {df['update_id'].min():.0f} - {df['update_id'].max():.0f}")
                
                # 检查 Update ID 递增情况
                if len(df) > 1:
                    df_sorted = df.sort_values('timestamp')
                    id_diffs = df_sorted['update_id'].diff().dropna()
                    
                    increasing = (id_diffs > 0).sum()
                    decreasing = (id_diffs < 0).sum()
                    equal = (id_diffs == 0).sum()
                    
                    if decreasing > 0 or equal > 0:
                        print(f"   ⚠️ Update ID 变化: ↑{increasing} ↓{decreasing} ={equal}")
                    else:
                        print(f"   ✅ Update ID: 全部递增")
            
            # 价格信息
            if 'best_bid_price' in df.columns and 'best_ask_price' in df.columns:
                latest = df.iloc[-1]
                print(f"   💰 最新买价: {latest['best_bid_price']:.6f}")
                print(f"   💰 最新卖价: {latest['best_ask_price']:.6f}")
                spread = (latest['best_ask_price'] - latest['best_bid_price']) / latest['best_bid_price'] * 100
                print(f"   📊 价差: {spread:.3f}%")
            
            print()
            
        except Exception as e:
            print(f"   ❌ 错误: {e}")
            print()
    
    print("-" * 80)
    print(f"📈 总计: {total_records} 条记录")
    print("=" * 80)
    print()


def check_recent_activity():
    """检查最近的采集活动"""
    
    print("=" * 80)
    print("🕐 最近 5 分钟的采集活动")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'IRON-USDT']  # 检查两个代表性的交易对
    
    # 使用 UTC 时区（与数据文件的时区一致）
    now = datetime.now(timezone.utc)
    five_min_ago = now - timedelta(minutes=5)
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty:
                continue
            
            # 筛选最近 5 分钟的数据
            recent = df[df['timestamp'] >= five_min_ago]
            
            if len(recent) > 0:
                print(f"📋 {pair}: {len(recent)} 条记录")
                
                # 显示最后几条
                print("   最近 3 条记录:")
                for i, row in recent.tail(3).iterrows():
                    print(f"      {row['timestamp']}: Update ID {row['update_id']:.0f}, "
                          f"Bid {row['best_bid_price']:.6f}, Ask {row['best_ask_price']:.6f}")
                print()
        
        except Exception as e:
            print(f"   ❌ {pair}: {e}")
    
    print("=" * 80)
    print()


def check_data_quality():
    """检查数据质量问题"""
    
    print("=" * 80)
    print("🔍 数据质量分析")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty or len(df) < 2:
                continue
            
            print(f"📋 {pair}:")
            
            # 检查重复的 timestamp
            dup_time = df[df.duplicated(subset=['timestamp'], keep=False)]
            if len(dup_time) > 0:
                print(f"   ⚠️ 重复时间戳: {len(dup_time)} 条")
            
            # 检查重复的 update_id
            dup_id = df[df.duplicated(subset=['update_id'], keep=False)]
            if len(dup_id) > 0:
                print(f"   ⚠️ 重复 Update ID: {len(dup_id)} 条")
            
            # 检查 Update ID 乱序
            df_sorted = df.sort_values('timestamp')
            non_increasing = 0
            for i in range(1, len(df_sorted)):
                if df_sorted.iloc[i]['update_id'] <= df_sorted.iloc[i-1]['update_id']:
                    non_increasing += 1
            
            if non_increasing > 0:
                print(f"   ⚠️ Update ID 非递增: {non_increasing} 处")
            
            # 如果有问题，显示详情
            if len(dup_time) > 0 or len(dup_id) > 0 or non_increasing > 0:
                print(f"   💡 建议: 数据可能包含测试采集和正式采集，可考虑清理后重新采集")
            else:
                print(f"   ✅ 数据质量良好")
            
            print()
            
        except Exception as e:
            print(f"   ❌ {pair}: {e}")
            print()
    
    print("=" * 80)
    print()


def main():
    """主函数"""
    print()
    print("🔍 开始检查订单簿实时采集状态...")
    print()
    
    # 检查实时状态
    check_realtime_status()
    
    # 检查最近活动
    check_recent_activity()
    
    # 检查数据质量
    check_data_quality()
    
    print("=" * 80)
    print("✅ 检查完成")
    print("=" * 80)
    print()
    
    print("💡 提示:")
    print("   • 如果发现数据质量问题（重复、乱序），可能是因为包含了测试数据")
    print("   • 清理方法: rm app/data/raw/orderbook_snapshots/*")
    print("   • 然后重新启动采集服务")
    print()


if __name__ == "__main__":
    main()

