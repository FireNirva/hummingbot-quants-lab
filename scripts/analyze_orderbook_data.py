#!/usr/bin/env python3
"""
深度分析订单簿数据

使用方法：
    python scripts/analyze_orderbook_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime, timedelta
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots
from core.data_paths import data_paths


def analyze_collection_performance():
    """分析采集性能"""
    
    print("=" * 80)
    print("📊 订单簿采集性能分析")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    results = []
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty or len(df) < 2:
                continue
            
            # 基本统计
            total_records = len(df)
            duration = df['timestamp'].max() - df['timestamp'].min()
            duration_hours = duration.total_seconds() / 3600
            duration_minutes = duration.total_seconds() / 60
            
            # 平均采集间隔
            time_diffs = df['timestamp'].diff().dropna()
            avg_interval = time_diffs.mean().total_seconds()
            min_interval = time_diffs.min().total_seconds()
            max_interval = time_diffs.max().total_seconds()
            
            # Update ID 统计
            update_id_range = df['update_id'].max() - df['update_id'].min()
            unique_update_ids = df['update_id'].nunique()
            duplicate_rate = (1 - unique_update_ids / total_records) * 100
            
            # 价差统计
            df['spread_pct'] = (df['best_ask_price'] - df['best_bid_price']) / df['best_bid_price'] * 100
            avg_spread = df['spread_pct'].mean()
            min_spread = df['spread_pct'].min()
            max_spread = df['spread_pct'].max()
            
            # 价格波动
            price_volatility = ((df['best_bid_price'].std() / df['best_bid_price'].mean()) * 100)
            
            results.append({
                'pair': pair,
                'records': total_records,
                'duration_hours': duration_hours,
                'avg_interval': avg_interval,
                'update_id_range': update_id_range,
                'duplicate_rate': duplicate_rate,
                'avg_spread': avg_spread,
                'price_volatility': price_volatility,
                'records_per_hour': total_records / duration_hours if duration_hours > 0 else 0
            })
            
        except Exception as e:
            print(f"❌ {pair}: {e}")
    
    # 创建 DataFrame 并排序
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('records', ascending=False)
    
    # 显示表格
    print("交易对排名（按记录数）:")
    print()
    print(f"{'排名':<4} {'交易对':<18} {'记录数':<8} {'运行时长':<10} {'每小时记录':<12} {'平均间隔':<10} {'重复率':<8} {'平均价差':<10} {'价格波动'}")
    print("-" * 110)
    
    for i, row in enumerate(df_results.itertuples(), 1):
        duration_str = f"{row.duration_hours:.2f}h"
        
        # 根据重复率设置标记
        dup_mark = "✅" if row.duplicate_rate < 10 else "⚠️" if row.duplicate_rate < 50 else "❌"
        
        print(f"{i:<4} {row.pair:<18} {row.records:<8} {duration_str:<10} {row.records_per_hour:<12.1f} "
              f"{row.avg_interval:<10.2f}s {dup_mark} {row.duplicate_rate:<5.1f}% {row.avg_spread:<10.3f}% {row.price_volatility:.2f}%")
    
    print()
    print("=" * 80)
    print()


def analyze_liquidity():
    """分析流动性指标"""
    
    print("=" * 80)
    print("💧 流动性分析")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    print(f"{'交易对':<18} {'Update ID增长':<15} {'每小时增长':<15} {'流动性评级'}")
    print("-" * 70)
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty or len(df) < 2:
                continue
            
            # Update ID 增长（代表订单簿更新频率）
            update_id_growth = df['update_id'].max() - df['update_id'].min()
            
            # 运行时长
            duration_hours = (df['timestamp'].max() - df['timestamp'].min()).total_seconds() / 3600
            
            # 每小时 Update ID 增长
            updates_per_hour = update_id_growth / duration_hours if duration_hours > 0 else 0
            
            # 流动性评级
            if updates_per_hour > 100000:
                rating = "🔥🔥🔥 极高"
            elif updates_per_hour > 10000:
                rating = "🔥🔥 高"
            elif updates_per_hour > 1000:
                rating = "🔥 中等"
            else:
                rating = "❄️ 低"
            
            print(f"{pair:<18} {update_id_growth:<15,} {updates_per_hour:<15,.0f} {rating}")
            
        except Exception as e:
            print(f"{pair:<18} ❌ {str(e)[:30]}")
    
    print()
    print("说明:")
    print("  • Update ID 增长: 订单簿实际更新次数（不包括我们的采集频率）")
    print("  • 每小时增长越大 = 流动性越好 = 价格发现越活跃")
    print()
    print("=" * 80)
    print()


def analyze_price_movements():
    """分析价格走势"""
    
    print("=" * 80)
    print("📈 价格走势分析")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'IRON-USDT', 'PRO-USDT']  # 选择代表性的交易对
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty:
                continue
            
            # 计算中间价
            df['mid_price'] = (df['best_bid_price'] + df['best_ask_price']) / 2
            
            # 价格统计
            first_price = df.iloc[0]['mid_price']
            last_price = df.iloc[-1]['mid_price']
            highest_price = df['mid_price'].max()
            lowest_price = df['mid_price'].min()
            
            price_change = ((last_price - first_price) / first_price) * 100
            price_range = ((highest_price - lowest_price) / lowest_price) * 100
            
            print(f"📋 {pair}:")
            print(f"   起始价格: ${first_price:.6f}")
            print(f"   最新价格: ${last_price:.6f}")
            print(f"   最高价格: ${highest_price:.6f}")
            print(f"   最低价格: ${lowest_price:.6f}")
            print(f"   价格变化: {price_change:+.2f}%")
            print(f"   价格波幅: {price_range:.2f}%")
            print()
            
        except Exception as e:
            print(f"❌ {pair}: {e}")
            print()
    
    print("=" * 80)
    print()


def analyze_data_quality():
    """分析数据质量"""
    
    print("=" * 80)
    print("✅ 数据质量汇总")
    print("=" * 80)
    print()
    
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    total_records = 0
    total_issues = 0
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            
            if df.empty:
                continue
            
            total_records += len(df)
            
            # 检查空值
            null_count = df.isnull().sum().sum()
            
            # 检查重复时间戳
            dup_timestamp = df.duplicated(subset=['timestamp']).sum()
            
            # 检查重复 Update ID
            dup_update_id = df.duplicated(subset=['update_id']).sum()
            
            issues = null_count + dup_timestamp
            total_issues += issues
            
            status = "✅ 优秀" if issues == 0 else "⚠️ 良好" if issues < 10 else "❌ 需清理"
            
            print(f"{pair:<18} {len(df):<8} 条  空值: {null_count:<4}  重复时间: {dup_timestamp:<4}  {status}")
            
        except Exception as e:
            print(f"{pair:<18} ❌ {e}")
    
    print()
    print(f"总计: {total_records} 条记录")
    
    if total_issues == 0:
        print("🎉 数据质量完美！")
    elif total_issues < 50:
        print("✅ 数据质量良好，可以使用")
    else:
        print("⚠️ 建议清理数据后重新采集")
    
    print()
    print("=" * 80)
    print()


def main():
    """主函数"""
    print()
    print("🔍 开始深度分析订单簿数据...")
    print()
    
    # 性能分析
    analyze_collection_performance()
    
    # 流动性分析
    analyze_liquidity()
    
    # 价格走势
    analyze_price_movements()
    
    # 数据质量
    analyze_data_quality()
    
    print("=" * 80)
    print("✅ 分析完成")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

