#!/usr/bin/env python3
"""
批量计算所有交易对的最优交易规模

从 spread analysis 结果中读取价差，然后为每个交易对计算最优规模
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from calculate_optimal_trade_size import TradeSizeOptimizer
import pandas as pd
import argparse
import yaml
from pathlib import Path
from core.data_paths import data_paths


def load_spread_data(config_file: str, connector: str) -> pd.DataFrame:
    """从配置文件加载交易对并模拟价差数据"""
    config_path = Path(config_file)
    
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return pd.DataFrame()
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 获取交易对列表
    trading_pairs = config.get('tasks', [{}])[0].get('config', {}).get('trading_pairs', [])
    
    if not trading_pairs:
        print(f"❌ 配置文件中没有找到交易对")
        return pd.DataFrame()
    
    # 这里可以从 spread analysis 结果中读取实际价差
    # 目前使用示例数据
    data = {
        'trading_pair': trading_pairs,
        'avg_spread_pct': [0.0] * len(trading_pairs)  # 占位符
    }
    
    return pd.DataFrame(data)


def batch_optimize(config_file: str, connector: str = "mexc", network: str = "base"):
    """批量优化所有交易对"""
    
    print(f"\n{'='*80}")
    print(f"📊 批量交易规模优化")
    print(f"   配置: {config_file}")
    print(f"   CEX: {connector} | DEX: {network}")
    print(f"{'='*80}\n")
    
    # 手动输入已知的价差数据（从之前的分析结果）
    spreads = {
        'IRON-USDT': 7.87,
        'HINT-USDT': 0.50,
        'AUKI-USDT': 1.04,
        'SERV-USDT': 2.31,
        'IXS-USDT': 2.05,
        'BID-USDT': 0.67,
    }
    
    results = []
    
    for pair, spread in spreads.items():
        print(f"\n{'─'*80}")
        print(f"🔄 分析 {pair} (价差: {spread:.2f}%)")
        print(f"{'─'*80}")
        
        optimizer = TradeSizeOptimizer(
            trading_pair=pair,
            connector=connector,
            network=network
        )
        
        result = optimizer.optimize(price_spread_pct=spread)
        
        if result:
            results.append({
                'trading_pair': pair,
                'spread_pct': spread,
                **result
            })
    
    # 汇总结果
    if not results:
        print("\n❌ 没有成功优化任何交易对")
        return
    
    df = pd.DataFrame(results)
    
    print(f"\n{'='*80}")
    print(f"📊 批量优化汇总")
    print(f"{'='*80}\n")
    
    # 按净利润排序
    df_sorted = df.sort_values('net_profit_usd', ascending=False)
    
    print("排名 | 交易对        | 最优规模     | 净价差  | 单次利润  | ROI")
    print("─" * 80)
    
    for idx, row in df_sorted.iterrows():
        if row['net_profit_usd'] > 0:
            print(f"{idx+1:4d} | {row['trading_pair']:13s} | ${row['optimal_size_usd']:>11,.2f} | "
                  f"{row['net_spread_pct']:>6.2f}% | ${row['net_profit_usd']:>8.2f} | {row['roi_pct']:>5.2f}%")
        else:
            print(f"{idx+1:4d} | {row['trading_pair']:13s} | ${row['optimal_size_usd']:>11,.2f} | "
                  f"{row['net_spread_pct']:>6.2f}% | 💀亏损     | {row['roi_pct']:>5.2f}%")
    
    print(f"\n{'='*80}\n")
    
    # 保存结果
    output_dir = data_paths.processed_dir / "trade_size_optimization"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"{network}_{connector}_optimal_sizes.csv"
    df_sorted.to_csv(output_file, index=False)
    
    print(f"✅ 结果已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="批量计算最优交易规模")
    parser.add_argument('--config', type=str, default='config/mexc_base_ecosystem_downloader.yml',
                        help='配置文件路径')
    parser.add_argument('--connector', type=str, default='mexc', help='CEX 连接器')
    parser.add_argument('--network', type=str, default='base', help='DEX 网络')
    
    args = parser.parse_args()
    
    batch_optimize(args.config, args.connector, args.network)


if __name__ == "__main__":
    main()

