#!/usr/bin/env python3
"""
CEX-DEX 价差可视化工具

生成价差分析图表，支持：
1. 价差时序图（双曲线：连续 vs 事件时间）
2. 价差分布直方图
3. 流动性-价差散点图
"""
import sys
from pathlib import Path

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_paths import data_paths

# 延迟导入 matplotlib，如果未安装给出友好提示
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    
    # 配置中文字体
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
except ImportError:
    print("❌ matplotlib 未安装")
    print("   请运行: conda install -n quants-lab matplotlib")
    sys.exit(1)


def plot_spread_timeseries(spread_df: pd.DataFrame, trading_pair: str, interval: str):
    """
    绘制价差时序图（双曲线）。
    
    Args:
        spread_df: 价差数据
        trading_pair: 交易对名称
        interval: 时间间隔
    """
    if len(spread_df) == 0:
        print(f"⚠️  {trading_pair} 数据为空，跳过时序图")
        return
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), gridspec_kw={'height_ratios': [3, 1]})
    
    # 上图：价差时序
    # 曲线 1: 连续价差（含补全）
    ax1.plot(spread_df.index, spread_df['price_diff_pct'], 
            color='lightgray', linewidth=0.5, linestyle='--', 
            label='连续价差（含补全）', alpha=0.6)
    
    # 曲线 2: 实际交易价差
    real_trades = spread_df[~spread_df['dex_is_filled']]
    ax1.scatter(real_trades.index, real_trades['price_diff_pct'], 
               c='blue', s=1, label='实际交易', alpha=0.6)
    
    # 标注套利阈值
    ax1.axhline(y=0.5, color='green', linestyle=':', linewidth=1, alpha=0.7, label='套利阈值 +0.5%')
    ax1.axhline(y=-0.5, color='red', linestyle=':', linewidth=1, alpha=0.7, label='套利阈值 -0.5%')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5, alpha=0.3)
    
    ax1.set_ylabel('价差 (%)', fontsize=12)
    ax1.set_title(f'{trading_pair} CEX-DEX 价差时序图 ({interval})', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 下图：DEX 成交量
    if len(real_trades) > 1:
        bar_width = mdates.date2num(real_trades.index[1]) - mdates.date2num(real_trades.index[0])
    else:
        bar_width = 0.0007  # 约 1 分钟的宽度
    
    ax2.bar(real_trades.index, real_trades['dex_volume'], 
           width=bar_width,
           color='purple', alpha=0.5, label='DEX 成交量')
    
    ax2.set_xlabel('时间 (UTC)', fontsize=12)
    ax2.set_ylabel('DEX 成交量 (USD)', fontsize=12)
    ax2.legend(loc='upper right', fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    # 格式化 x 轴
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # 保存
    output_file = data_paths.plots_dir / f"spread_timeseries_{trading_pair}_{interval}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ 时序图已保存: {output_file}")
    
    plt.close()


def plot_spread_distribution(spread_df: pd.DataFrame, trading_pair: str, interval: str):
    """
    绘制价差分布直方图。
    
    Args:
        spread_df: 价差数据
        trading_pair: 交易对名称
        interval: 时间间隔
    """
    if len(spread_df) == 0:
        print(f"⚠️  {trading_pair} 数据为空，跳过分布图")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # 左图：全部数据（含补全）
    ax1.hist(spread_df['price_diff_pct'], bins=100, color='lightgray', 
            alpha=0.7, edgecolor='black', linewidth=0.5)
    ax1.axvline(x=0.5, color='green', linestyle='--', linewidth=2, label='套利阈值 +0.5%')
    ax1.axvline(x=-0.5, color='red', linestyle='--', linewidth=2, label='套利阈值 -0.5%')
    ax1.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax1.set_xlabel('价差 (%)', fontsize=12)
    ax1.set_ylabel('频数', fontsize=12)
    ax1.set_title('价差分布（含补全数据）', fontsize=13, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # 右图：仅实际交易
    real_trades = spread_df[~spread_df['dex_is_filled']]
    ax2.hist(real_trades['price_diff_pct'], bins=100, color='blue', 
            alpha=0.7, edgecolor='black', linewidth=0.5)
    ax2.axvline(x=0.5, color='green', linestyle='--', linewidth=2, label='套利阈值 +0.5%')
    ax2.axvline(x=-0.5, color='red', linestyle='--', linewidth=2, label='套利阈值 -0.5%')
    ax2.axvline(x=0, color='black', linestyle='-', linewidth=1)
    ax2.set_xlabel('价差 (%)', fontsize=12)
    ax2.set_ylabel('频数', fontsize=12)
    ax2.set_title('价差分布（仅实际交易）', fontsize=13, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # 保存
    output_file = data_paths.plots_dir / f"spread_distribution_{trading_pair}_{interval}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ 分布图已保存: {output_file}")
    
    plt.close()


def plot_liquidity_spread_scatter(spread_df: pd.DataFrame, trading_pair: str, interval: str):
    """
    绘制流动性-价差散点图。
    
    Args:
        spread_df: 价差数据
        trading_pair: 交易对名称
        interval: 时间间隔
    """
    if len(spread_df) == 0:
        print(f"⚠️  {trading_pair} 数据为空，跳过散点图")
        return
    
    # 仅实际交易
    real_trades = spread_df[~spread_df['dex_is_filled']].copy()
    
    if len(real_trades) == 0:
        print(f"⚠️  {trading_pair} 无实际交易数据，跳过散点图")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # 散点图，颜色表示套利方向
    colors = []
    for _, row in real_trades.iterrows():
        if row['arb_direction'] == 'cex_to_dex':
            colors.append('green')
        elif row['arb_direction'] == 'dex_to_cex':
            colors.append('red')
        else:
            colors.append('gray')
    
    scatter = ax.scatter(real_trades['dex_volume'], 
                        real_trades['price_diff_pct'].abs(), 
                        c=colors, s=20, alpha=0.5)
    
    # 添加套利阈值线
    ax.axhline(y=0.5, color='orange', linestyle='--', linewidth=2, 
              label='套利阈值 0.5%')
    
    ax.set_xlabel('DEX 成交量 (USD)', fontsize=12)
    ax.set_ylabel('价差绝对值 (%)', fontsize=12)
    ax.set_title(f'{trading_pair} 流动性-价差关系 ({interval})', 
                fontsize=14, fontweight='bold')
    ax.set_xscale('log')  # 对数刻度
    ax.grid(True, alpha=0.3)
    
    # 图例
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='CEX→DEX 套利'),
        Patch(facecolor='red', label='DEX→CEX 套利'),
        Patch(facecolor='gray', label='平衡区')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    plt.tight_layout()
    
    # 保存
    output_file = data_paths.plots_dir / f"liquidity_spread_{trading_pair}_{interval}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✅ 流动性图已保存: {output_file}")
    
    plt.close()


def main():
    """主函数。"""
    import argparse
    
    parser = argparse.ArgumentParser(description="CEX-DEX 价差可视化工具")
    parser.add_argument('--pair', type=str, default='AERO-USDT', help='交易对名称')
    parser.add_argument('--interval', type=str, default='1m', help='时间间隔')
    
    args = parser.parse_args()
    
    print("="*80)
    print(f"📊 CEX-DEX 价差可视化: {args.pair} ({args.interval})")
    print("="*80)
    print()
    
    # 加载价差数据
    spread_file = data_paths.spread_analysis_dir / f"spread_analysis_{args.pair}_{args.interval}.parquet"
    
    if not spread_file.exists():
        print(f"❌ 价差数据不存在: {spread_file}")
        print("   请先运行: python scripts/analyze_cex_dex_spread.py")
        return 1
    
    print(f"📁 加载数据: {spread_file.name}")
    spread_df = pd.read_parquet(spread_file)
    print(f"✅ 加载 {len(spread_df):,} 个数据点")
    print()
    
    # 生成图表
    print("🎨 生成图表...")
    print()
    
    success_count = 0
    
    try:
        plot_spread_timeseries(spread_df, args.pair, args.interval)
        success_count += 1
    except Exception as e:
        print(f"❌ 时序图生成失败: {e}")
    
    try:
        plot_spread_distribution(spread_df, args.pair, args.interval)
        success_count += 1
    except Exception as e:
        print(f"❌ 分布图生成失败: {e}")
    
    try:
        plot_liquidity_spread_scatter(spread_df, args.pair, args.interval)
        success_count += 1
    except Exception as e:
        print(f"❌ 散点图生成失败: {e}")
    
    if success_count == 0:
        print("\n❌ 所有图表生成失败")
        return 1
    
    print()
    print("="*80)
    print(f"✅ 可视化完成！成功生成 {success_count}/3 个图表")
    print("="*80)
    print()
    print(f"📁 图表保存位置: {data_paths.plots_dir}")
    
    if success_count > 0:
        print("\n生成的图表:")
        if success_count >= 1:
            print(f"  • spread_timeseries_{args.pair}_{args.interval}.png")
        if success_count >= 2:
            print(f"  • spread_distribution_{args.pair}_{args.interval}.png")
        if success_count >= 3:
            print(f"  • liquidity_spread_{args.pair}_{args.interval}.png")
    print()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

