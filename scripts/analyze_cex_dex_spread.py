#!/usr/bin/env python3
"""
CEX-DEX 价差分析工具

支持两种分析模式：
1. 连续时间轴（补全后）：宏观观测价差趋势
2. 事件时间（仅实际交易）：评估真实可套利性
"""
import sys
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_paths import data_paths
from core.utils.dex_data_fill import (
    align_dex_to_cex,
    create_spread_dataframe,
    get_spread_statistics
)


def analyze_pair_spread(trading_pair: str, interval: str = "1m", volume_threshold: float = 100.0):
    """
    分析单个交易对的 CEX-DEX 价差。
    
    Args:
        trading_pair: 交易对名称，如 "AERO-USDT"
        interval: 时间间隔
        volume_threshold: DEX 成交量阈值（用于可执行性过滤）
    """
    print("\n" + "="*80)
    print(f"📊 CEX-DEX 价差分析: {trading_pair} ({interval})")
    print("="*80)
    print()
    
    # 1. 加载数据
    print("📁 加载数据...")
    cex_file = data_paths.candles_dir / f"gate_io|{trading_pair}|{interval}.parquet"
    dex_file = data_paths.candles_dir / f"geckoterminal_base|{trading_pair}|{interval}.parquet"
    
    if not cex_file.exists():
        print(f"❌ CEX 数据不存在: {cex_file.name}")
        return False
    
    if not dex_file.exists():
        print(f"❌ DEX 数据不存在: {dex_file.name}")
        return False
    
    cex_df = pd.read_parquet(cex_file)
    dex_df_raw = pd.read_parquet(dex_file)
    
    print(f"✅ CEX 数据: {len(cex_df):,} 根K线")
    print(f"✅ DEX 数据（原始）: {len(dex_df_raw):,} 根K线")
    print(f"   覆盖率: {len(dex_df_raw)/len(cex_df)*100:.2f}%")
    print()
    
    # 2. 补全 DEX 数据
    print("🔧 补全 DEX 数据...")
    dex_df_filled = align_dex_to_cex(cex_df, dex_df_raw, interval)
    
    n_filled = dex_df_filled['is_filled'].sum()
    print(f"✅ 补全完成: 新增 {n_filled:,} 根蜡烛")
    print()
    
    # 3. 创建价差数据
    print("📈 计算价差...")
    spread_df = create_spread_dataframe(cex_df, dex_df_filled)
    
    # 应用成交量过滤
    spread_df['meets_volume_threshold'] = spread_df['dex_volume'] >= volume_threshold
    
    print(f"✅ 价差数据: {len(spread_df):,} 个时间点")
    print()
    
    # 4. 统计分析 - 模式 1：连续时间轴（含补全）
    print("="*80)
    print("📊 模式 1: 连续时间轴分析（含补全数据）")
    print("="*80)
    print("💡 用途: 宏观观测价差趋势，了解名义套利空间")
    print()
    
    stats_full = get_spread_statistics(spread_df, include_filled=True)
    
    print(f"数据点数: {stats_full['total_points']:,}")
    print(f"平均价差: {stats_full['mean_spread_pct']:+.4f}%")
    print(f"中位价差: {stats_full['median_spread_pct']:+.4f}%")
    print(f"标准差: {stats_full['std_spread_pct']:.4f}%")
    print(f"价差范围: [{stats_full['min_spread_pct']:+.4f}%, {stats_full['max_spread_pct']:+.4f}%]")
    print()
    
    arb_full = stats_full['arb_opportunities']
    total_full = sum(arb_full.values())
    
    print("名义套利机会（价差 > 0.5%）:")
    print(f"  CEX→DEX: {arb_full['cex_to_dex']:,} 次 ({arb_full['cex_to_dex']/total_full*100:.2f}%)")
    print(f"    → CEX 买入，DEX 卖出")
    print(f"  DEX→CEX: {arb_full['dex_to_cex']:,} 次 ({arb_full['dex_to_cex']/total_full*100:.2f}%)")
    print(f"    → DEX 买入，CEX 卖出")
    print(f"  平衡区: {arb_full['neutral']:,} 次 ({arb_full['neutral']/total_full*100:.2f}%)")
    print()
    
    # 5. 统计分析 - 模式 2：事件时间（仅实际交易）
    print("="*80)
    print("📊 模式 2: 事件时间分析（仅 DEX 实际交易）")
    print("="*80)
    print("💡 用途: 评估真实可执行的套利机会")
    print()
    
    stats_real = get_spread_statistics(spread_df, include_filled=False)
    
    print(f"数据点数: {stats_real['total_points']:,} (实际交易)")
    print(f"平均价差: {stats_real['mean_spread_pct']:+.4f}%")
    print(f"中位价差: {stats_real['median_spread_pct']:+.4f}%")
    print(f"标准差: {stats_real['std_spread_pct']:.4f}%")
    print(f"价差范围: [{stats_real['min_spread_pct']:+.4f}%, {stats_real['max_spread_pct']:+.4f}%]")
    print()
    
    arb_real = stats_real['arb_opportunities']
    total_real = sum(arb_real.values())
    
    print("可执行套利机会（DEX 有成交 + 价差 > 0.5%）:")
    print(f"  CEX→DEX: {arb_real['cex_to_dex']:,} 次 ({arb_real['cex_to_dex']/total_real*100:.2f}%)")
    print(f"  DEX→CEX: {arb_real['dex_to_cex']:,} 次 ({arb_real['dex_to_cex']/total_real*100:.2f}%)")
    print(f"  平衡区: {arb_real['neutral']:,} 次 ({arb_real['neutral']/total_real*100:.2f}%)")
    print()
    
    # 6. 成交量过滤分析
    print("="*80)
    print(f"📊 成交量过滤分析（阈值: ${volume_threshold:.0f}）")
    print("="*80)
    print()
    
    volume_filtered = spread_df[
        (~spread_df['dex_is_filled']) & 
        (spread_df['meets_volume_threshold'])
    ]
    
    print(f"满足成交量阈值: {len(volume_filtered):,} / {stats_real['total_points']:,} 次")
    print(f"  ({len(volume_filtered)/stats_real['total_points']*100:.2f}%)")
    print()
    
    if len(volume_filtered) > 0:
        arb_cex_to_dex = len(volume_filtered[volume_filtered['arb_direction'] == 'cex_to_dex'])
        arb_dex_to_cex = len(volume_filtered[volume_filtered['arb_direction'] == 'dex_to_cex'])
        
        print("高流动性套利机会:")
        print(f"  CEX→DEX: {arb_cex_to_dex:,} 次")
        print(f"  DEX→CEX: {arb_dex_to_cex:,} 次")
        print()
    
    # 7. 时间分布分析
    print("="*80)
    print("📊 时间分布分析")
    print("="*80)
    print()
    
    # 按小时统计
    spread_df['hour'] = spread_df.index.hour
    real_trades = spread_df[~spread_df['dex_is_filled']]
    
    hourly_stats = real_trades.groupby('hour').agg({
        'dex_volume': 'sum',
        'price_diff_pct': 'mean'
    }).round(2)
    
    print("每小时统计（仅实际交易）:")
    print(f"  最活跃时段: {hourly_stats['dex_volume'].idxmax()}:00 UTC")
    print(f"  最大成交量: ${hourly_stats['dex_volume'].max():,.0f}")
    print(f"  平均价差最大: {hourly_stats['price_diff_pct'].abs().idxmax()}:00 UTC "
          f"({hourly_stats['price_diff_pct'].abs().max():+.4f}%)")
    print()
    
    # 8. 保存分析结果
    print("💾 保存分析结果...")
    output_file = data_paths.spread_analysis_dir / f"spread_analysis_{trading_pair}_{interval}.parquet"
    spread_df.to_parquet(output_file)
    print(f"✅ 已保存到: {output_file}")
    print()
    
    # 9. 可视化建议
    print("="*80)
    print("📈 可视化建议")
    print("="*80)
    print()
    print("建议创建以下图表:")
    print("  1. 价差时序图（双曲线）:")
    print("     - 曲线1: 连续价差（含补全，灰色虚线）")
    print("     - 曲线2: 实际交易价差（蓝色实线）")
    print("     - 叠加: 成交量柱状图（底部）")
    print()
    print("  2. 价差分布直方图:")
    print("     - 对比补全数据 vs 实际交易数据")
    print("     - 标注套利阈值 (±0.5%)")
    print()
    print("  3. 流动性热力图:")
    print("     - X轴: 时间, Y轴: 价差区间")
    print("     - 颜色: DEX 成交量")
    print()
    
    return True


def compare_multiple_pairs():
    """对比多个交易对的套利潜力。"""
    print("\n" + "="*80)
    print("📊 多交易对套利潜力对比")
    print("="*80)
    print()
    
    pairs = ["AERO-USDT", "VIRTUAL-USDT", "BRETT-USDT", "GPS-USDT"]
    interval = "1m"
    
    results = []
    
    for pair in pairs:
        cex_file = data_paths.candles_dir / f"gate_io|{pair}|{interval}.parquet"
        dex_file = data_paths.candles_dir / f"geckoterminal_base|{pair}|{interval}.parquet"
        
        if not cex_file.exists() or not dex_file.exists():
            continue
        
        cex_df = pd.read_parquet(cex_file)
        dex_df_raw = pd.read_parquet(dex_file)
        dex_df_filled = align_dex_to_cex(cex_df, dex_df_raw, interval)
        spread_df = create_spread_dataframe(cex_df, dex_df_filled)
        
        # 统计
        real_trades = spread_df[~spread_df['dex_is_filled']]
        executable = real_trades[real_trades['is_executable']]
        
        results.append({
            'pair': pair,
            'dex_coverage': len(dex_df_raw) / len(cex_df) * 100,
            'avg_spread': real_trades['price_diff_pct'].abs().mean(),
            'executable_ops': len(executable[executable['arb_direction'] != 'neutral']),
            'total_volume': real_trades['dex_volume'].sum()
        })
    
    # 显示对比表格
    df_results = pd.DataFrame(results)
    
    print("交易对对比:")
    print("-"*80)
    for _, row in df_results.iterrows():
        print(f"{row['pair']:15s} | "
              f"覆盖率: {row['dex_coverage']:5.1f}% | "
              f"平均价差: {row['avg_spread']:5.2f}% | "
              f"可执行机会: {row['executable_ops']:5.0f} 次 | "
              f"总成交量: ${row['total_volume']:,.0f}")
    print()
    
    # 推荐排序
    print("💡 推荐排序（综合评分）:")
    df_results['score'] = (
        df_results['dex_coverage'] * 0.3 +
        df_results['avg_spread'] * 10 +
        df_results['executable_ops'] / 10
    )
    
    df_sorted = df_results.sort_values('score', ascending=False)
    for i, (_, row) in enumerate(df_sorted.iterrows(), 1):
        rating = "⭐" * min(5, int(row['score'] / 20))
        print(f"  {i}. {row['pair']:15s} {rating} (评分: {row['score']:.1f})")
    print()


def main():
    """主函数。"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CEX-DEX 价差分析工具")
    parser.add_argument('--pair', type=str, default='AERO-USDT', help='交易对名称')
    parser.add_argument('--interval', type=str, default='1m', help='时间间隔')
    parser.add_argument('--volume-threshold', type=float, default=100.0, 
                       help='DEX 成交量阈值（USD）')
    parser.add_argument('--compare-all', action='store_true', help='对比所有交易对')
    
    args = parser.parse_args()
    
    if args.compare_all:
        compare_multiple_pairs()
    else:
        success = analyze_pair_spread(args.pair, args.interval, args.volume_threshold)
        
        if not success:
            return 1
    
    print("="*80)
    print("✅ 分析完成！")
    print("="*80)
    print()
    print("📝 关键洞察:")
    print("  • 连续时间轴分析：适合宏观趋势观测")
    print("  • 事件时间分析：反映真实可执行机会")
    print("  • 成交量过滤：确保套利的流动性")
    print("  • 补全数据（is_filled=True）不应参与回测")
    print()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

