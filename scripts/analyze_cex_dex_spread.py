#!/usr/bin/env python3
"""
CEX-DEX 价差分析工具

支持两种分析模式：
1. 连续时间轴（补全后）：宏观观测价差趋势
2. 事件时间（仅实际交易）：评估真实可套利性
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_paths import data_paths
from core.utils.dex_data_fill import (
    align_dex_to_cex,
    create_spread_dataframe,
    get_spread_statistics
)


def analyze_pair_spread(trading_pair: str, interval: str = "1m", volume_threshold: float = 100.0, connector: str = "gate_io", network: str = "base"):
    """
    分析单个交易对的 CEX-DEX 价差。
    
    Args:
        trading_pair: 交易对名称，如 "AERO-USDT"
        interval: 时间间隔
        volume_threshold: DEX 成交量阈值（用于可执行性过滤）
        connector: CEX 连接器名称（如 "gate_io", "mexc"）
        network: DEX 网络名称（如 "base"）
    """
    print("\n" + "="*80)
    print(f"📊 CEX-DEX 价差分析: {trading_pair} ({interval})")
    print(f"   CEX: {connector} | DEX: {network}")
    print("="*80)
    print()
    
    # 1. 加载数据
    print("📁 加载数据...")
    cex_file = data_paths.candles_dir / f"{connector}|{trading_pair}|{interval}.parquet"
    dex_file = data_paths.candles_dir / f"geckoterminal_{network}|{trading_pair}|{interval}.parquet"
    
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
    print("    → CEX 买入，DEX 卖出")
    print(f"  DEX→CEX: {arb_full['dex_to_cex']:,} 次 ({arb_full['dex_to_cex']/total_full*100:.2f}%)")
    print("    → DEX 买入，CEX 卖出")
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


def load_trading_pairs_from_config(config_file: str = "config/base_ecosystem_downloader_full.yml"):
    """
    从配置文件中加载交易对列表。
    
    Args:
        config_file: 配置文件路径（相对于项目根目录）
    
    Returns:
        交易对列表
    """
    config_path = project_root / config_file
    
    if not config_path.exists():
        print(f"⚠️  配置文件不存在: {config_path}")
        return []
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 从 YAML 中提取 trading_pairs
        tasks = config.get('tasks', {})
        for task_name, task_config in tasks.items():
            task_data = task_config.get('config', {})
            if 'trading_pairs' in task_data:
                pairs = task_data['trading_pairs']
                print(f"✅ 从配置文件加载了 {len(pairs)} 个交易对")
                return pairs
        
        print("⚠️  配置文件中未找到 trading_pairs")
        return []
    
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return []


def get_volume_multiplier(volume: float) -> float:
    """
    成交量评分系数（倒U型曲线）
    
    太低和太高的成交量都会降低评分：
    - < $100K: 无法套利，评分归零 ×0
    - $100K - $500K: 流动性不足，评分×0.5-0.8
    - $500K - $10M: 最佳区间，评分×1.0 ✅
    - $10M - $50M: 竞争加剧，评分×0.8-0.5
    - > $50M: 极度竞争，评分×0.3
    
    Args:
        volume: 总成交量（USD）
    
    Returns:
        评分系数 (0.0 - 1.0)
    """
    if volume < 100_000:
        # 极低流动性：< $100K
        # 无法套利，直接归零
        return 0.0
    
    elif volume < 500_000:
        # 低流动性：$100K - $500K
        # 线性增加 0.5 → 0.8
        return 0.5 + (volume - 100_000) / 400_000 * 0.3
    
    elif volume <= 10_000_000:
        # 最佳区间：$500K - $10M
        # 最高评分×1.0
        return 1.0
    
    elif volume <= 50_000_000:
        # 高流动性：$10M - $50M
        # 线性降低 0.8 → 0.5
        return 0.8 - (volume - 10_000_000) / 40_000_000 * 0.3
    
    else:
        # 极高流动性：> $50M
        # 竞争非常激烈，评分×0.3
        return 0.3


def compare_multiple_pairs(config_file: str = None, interval: str = "1m", connector: str = "gate_io", network: str = "base"):
    """
    对比多个交易对的套利潜力。
    
    Args:
        config_file: 配置文件路径（可选），如不提供则使用默认配置
        interval: 时间间隔（如 "1m", "5m"）
        connector: CEX 连接器名称（如 "gate_io", "mexc"）
        network: DEX 网络名称（如 "base"）
    """
    print("\n" + "="*80)
    print(f"📊 多交易对套利潜力对比 ({interval})")
    print(f"   CEX: {connector} | DEX: {network}")
    print("="*80)
    print()
    
    # 从配置文件加载交易对
    if config_file:
        pairs = load_trading_pairs_from_config(config_file)
    else:
        pairs = load_trading_pairs_from_config()
    
    if not pairs:
        print("❌ 未找到交易对列表，使用默认列表")
        pairs = ["AERO-USDT", "VIRTUAL-USDT", "BRETT-USDT", "GPS-USDT"]
    
    print(f"📋 将分析 {len(pairs)} 个交易对 (时间间隔: {interval})")
    print()
    
    results = []
    
    for pair in pairs:
        cex_file = data_paths.candles_dir / f"{connector}|{pair}|{interval}.parquet"
        dex_file = data_paths.candles_dir / f"geckoterminal_{network}|{pair}|{interval}.parquet"
        
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
    
    # 检查是否有有效结果
    if not results:
        print("❌ 错误：没有找到任何有效的交易对数据")
        print()
        print("可能的原因：")
        print("  1. DEX 数据还未下载")
        print("  2. CEX 数据文件命名格式不匹配")
        print("  3. 交易对配置有误")
        print()
        print("📋 预期文件格式：")
        print(f"   CEX: {connector}|PAIR-USDT|{interval}.parquet")
        print(f"   DEX: geckoterminal_{network}|PAIR-USDT|{interval}.parquet")
        return
    
    # 显示对比表格
    df_results = pd.DataFrame(results)
    
    print("交易对对比:")
    print("-"*80)
    for _, row in df_results.iterrows():
        # 处理 NaN 值
        dex_coverage = row['dex_coverage'] if not pd.isna(row['dex_coverage']) else 0
        avg_spread = row['avg_spread'] if not pd.isna(row['avg_spread']) else 0
        executable_ops = row['executable_ops'] if not pd.isna(row['executable_ops']) else 0
        total_volume = row['total_volume'] if not pd.isna(row['total_volume']) else 0
        
        # 如果价差为 0 或 NaN，显示为 "N/A"
        if pd.isna(row['avg_spread']) or row['avg_spread'] == 0:
            spread_str = "   N/A"
        else:
            spread_str = f"{avg_spread:5.2f}%"
        
        print(f"{row['pair']:15s} | "
              f"覆盖率: {dex_coverage:5.1f}% | "
              f"平均价差: {spread_str} | "
              f"可执行机会: {executable_ops:5.0f} 次 | "
              f"总成交量: ${total_volume:,.0f}")
    print()
    
    # 推荐排序（最终优化版 + 成交量阈值）
    print("💡 推荐排序（综合评分 - 最终优化版 V4）:")
    print("   核心理念: 抓住本质 + 成交量倒U型优化")
    print("   评分公式: score = (价差×10 + 机会数/10) × 成交量系数")
    print()
    print("   🎯 核心要素:")
    print("      1. 价差 → 决定每次能赚多少（最重要！）")
    print("      2. 机会数 → 决定能赚多少次（很重要！）")
    print("      3. 成交量系数 → 倒U型曲线（太低或太高都降低排名）")
    print()
    print("   📊 成交量阈值:")
    print("      • < $100K:       评分×0 ❌ （无法套利，直接归零）")
    print("      • $100K - $500K: 评分×0.5-0.8 （低流动性）")
    print("      • $500K - $10M:  评分×1.0 ✅ （最佳区间）")
    print("      • $10M - $50M:   评分×0.8-0.5 （竞争加剧）")
    print("      • > $50M:        评分×0.3 （极度竞争）")
    print()
    
    # 最终优化的评分公式 V4：添加成交量阈值
    # score = (价差 × 10 + 机会数 / 10) × volume_multiplier
    # 
    # 成交量系数：倒U型曲线
    # - 太低（<$100K）：流动性不足，惩罚×0.3
    # - 适中（$500K-$10M）：最佳区间，保持×1.0
    # - 太高（>$50M）：竞争激烈，惩罚×0.3
    
    # 计算成交量系数
    df_results['volume_multiplier'] = df_results['total_volume'].apply(get_volume_multiplier)
    
    # 基础评分
    df_results['base_score'] = (
        df_results['avg_spread'] * 10 +      # 价差：决定盈利空间
        df_results['executable_ops'] / 10     # 机会数：决定交易频次
    )
    
    # 最终评分 = 基础评分 × 成交量系数
    df_results['score'] = df_results['base_score'] * df_results['volume_multiplier']
    
    # 处理 NaN 值：如果评分或其他字段为 NaN（通常因为数据不足），设置为 0
    df_results = df_results.fillna({
        'avg_spread': 0,
        'executable_ops': 0,
        'base_score': 0,
        'volume_multiplier': 0,
        'score': 0
    })
    
    df_sorted = df_results.sort_values('score', ascending=False)
    
    for i, (_, row) in enumerate(df_sorted.iterrows(), 1):
        # 评分区间调整为更合理的刻度
        # 处理 NaN 或无穷大的情况
        score_val = row['score'] if not pd.isna(row['score']) and not np.isinf(row['score']) else 0
        rating = "⭐" * min(5, int(score_val / 10))
        
        # 添加流动性警告（仅提示，不影响评分）
        warnings = []
        if row['total_volume'] < 100_000:  # <$100K
            warnings.append("❌无法套利")
        if row['dex_coverage'] < 1.0:  # <1%
            warnings.append("⚠️极低覆盖")
        if pd.isna(row['avg_spread']) or row['avg_spread'] == 0:
            warnings.append("⚠️数据不足")
        warning_str = f" {' '.join(warnings)}" if warnings else ""
        
        print(f"  {i:2d}. {row['pair']:15s} {rating:10s} (评分: {score_val:6.1f}){warning_str}")
    
    print()
    
    # 显示评分组成明细（前 5 名）
    print("🔍 评分明细（前 5 名）:")
    print("-"*80)
    for i, (_, row) in enumerate(df_sorted.head(5).iterrows(), 1):
        # 处理可能的 NaN 值
        avg_spread = row['avg_spread'] if not pd.isna(row['avg_spread']) else 0
        executable_ops = row['executable_ops'] if not pd.isna(row['executable_ops']) else 0
        base_score = row['base_score'] if not pd.isna(row['base_score']) else 0
        volume_mult = row['volume_multiplier'] if not pd.isna(row['volume_multiplier']) else 0
        final_score = row['score'] if not pd.isna(row['score']) else 0
        dex_coverage = row['dex_coverage'] if not pd.isna(row['dex_coverage']) else 0
        
        spread_contrib = avg_spread * 10
        ops_contrib = executable_ops / 10
        
        print(f"{i}. {row['pair']}")
        print(f"   价差贡献: {spread_contrib:6.1f}分 (avg_spread={avg_spread:.2f}%)")
        print(f"   机会贡献: {ops_contrib:6.1f}分 (executable_ops={executable_ops:.0f}次)")
        print(f"   基础评分: {base_score:6.1f}分")
        print(f"   成交量系数: {volume_mult:.2f}x (volume=${row['total_volume']:,.0f})")
        print(f"   最终评分: {final_score:6.1f}分 = {base_score:.1f} × {volume_mult:.2f}")
        print(f"   覆盖率: {dex_coverage:.1f}%")
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
    parser.add_argument('--config', type=str, 
                       default='config/base_ecosystem_downloader_full.yml',
                       help='配置文件路径（用于 --compare-all）')
    parser.add_argument('--connector', type=str, default='gate_io',
                       help='CEX 连接器名称（如 gate_io, mexc）')
    parser.add_argument('--network', type=str, default='base',
                       help='DEX 网络名称（如 base）')
    
    args = parser.parse_args()
    
    if args.compare_all:
        compare_multiple_pairs(config_file=args.config, interval=args.interval, 
                              connector=args.connector, network=args.network)
    else:
        success = analyze_pair_spread(args.pair, args.interval, args.volume_threshold,
                                     connector=args.connector, network=args.network)
        
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

