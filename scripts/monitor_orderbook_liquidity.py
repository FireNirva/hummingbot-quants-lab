#!/usr/bin/env python3
"""
订单簿流动性监控

用途：
- 分析各交易对的流动性
- 识别重复 Update ID 的比例
- 推荐适合高频交易的币种

使用方法：
    python scripts/monitor_orderbook_liquidity.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from datetime import datetime, timezone
from core.data_paths import data_paths


def analyze_liquidity(trading_pair: str, connector: str = 'gate_io') -> dict:
    """分析单个交易对的流动性
    
    Args:
        trading_pair: 交易对名称
        connector: 交易所名称
        
    Returns:
        流动性分析结果
    """
    orderbook_dir = data_paths.raw_dir / "orderbook_snapshots"
    files = list(orderbook_dir.glob(f"{connector}_{trading_pair}_*.parquet"))
    
    if not files:
        return {'error': 'no_data', 'trading_pair': trading_pair}
    
    # 读取所有文件
    dfs = []
    for file in sorted(files):
        df = pd.read_parquet(file)
        dfs.append(df)
    
    df = pd.concat(dfs, ignore_index=True)
    
    if len(df) == 0:
        return {'error': 'empty_data', 'trading_pair': trading_pair}
    
    # 计算指标
    total_records = len(df)
    
    # Update ID 分析
    if 'update_id' in df.columns:
        unique_updates = df['update_id'].nunique()
        duplicate_records = total_records - unique_updates
        duplicate_rate = (duplicate_records / total_records) * 100
        
        # Update ID 增长速度
        if len(df) > 1:
            df_sorted = df.sort_values('timestamp')
            update_id_growth = df_sorted['update_id'].iloc[-1] - df_sorted['update_id'].iloc[0]
            avg_growth_per_record = update_id_growth / total_records if total_records > 0 else 0
            
            # 计算每秒的变化率
            time_span = (df_sorted['timestamp'].iloc[-1] - df_sorted['timestamp'].iloc[0]).total_seconds()
            updates_per_second = update_id_growth / time_span if time_span > 0 else 0
        else:
            update_id_growth = 0
            avg_growth_per_record = 0
            updates_per_second = 0
    else:
        unique_updates = 0
        duplicate_records = 0
        duplicate_rate = 0
        update_id_growth = 0
        avg_growth_per_record = 0
        updates_per_second = 0
    
    # 时间信息
    first_time = df['timestamp'].min()
    last_time = df['timestamp'].max()
    duration = (last_time - first_time).total_seconds()
    
    # 价格信息
    if 'best_bid_price' in df.columns and 'best_ask_price' in df.columns:
        latest = df.iloc[-1]
        current_price = (latest['best_bid_price'] + latest['best_ask_price']) / 2
        price_volatility = ((df['best_bid_price'].std() + df['best_ask_price'].std()) / 2) / current_price * 100
    else:
        current_price = 0
        price_volatility = 0
    
    # 流动性评分 (0-5 星)
    # 基于 Update ID 每秒增长数
    if updates_per_second >= 100:
        liquidity_score = 5  # 极高流动性
    elif updates_per_second >= 50:
        liquidity_score = 4  # 高流动性
    elif updates_per_second >= 10:
        liquidity_score = 3  # 中等流动性
    elif updates_per_second >= 1:
        liquidity_score = 2  # 低流动性
    elif updates_per_second > 0:
        liquidity_score = 1  # 极低流动性
    else:
        liquidity_score = 0  # 无流动性
    
    return {
        'trading_pair': trading_pair,
        'total_records': total_records,
        'unique_updates': unique_updates,
        'duplicate_records': duplicate_records,
        'duplicate_rate': duplicate_rate,
        'update_id_growth': update_id_growth,
        'avg_growth_per_record': avg_growth_per_record,
        'updates_per_second': updates_per_second,
        'duration_hours': duration / 3600,
        'current_price': current_price,
        'price_volatility': price_volatility,
        'liquidity_score': liquidity_score,
        'first_time': first_time,
        'last_time': last_time,
    }


def print_liquidity_report(results: list):
    """打印流动性报告"""
    
    print("\n" + "=" * 80)
    print("📊 订单簿流动性分析报告")
    print("=" * 80)
    print()
    
    # 过滤有效结果
    valid_results = [r for r in results if 'error' not in r]
    
    if not valid_results:
        print("❌ 没有找到有效数据")
        return
    
    # 按流动性评分排序
    sorted_results = sorted(valid_results, key=lambda x: x['liquidity_score'], reverse=True)
    
    print(f"分析时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"分析币种: {len(valid_results)} 个")
    print()
    
    # 详细表格
    print("-" * 80)
    print(f"{'交易对':<20} {'流动性':<12} {'重复率':<10} {'每秒变化':<15} {'价格波动':<10}")
    print("-" * 80)
    
    for result in sorted_results:
        stars = "⭐" * result['liquidity_score']
        duplicate_rate_str = f"{result['duplicate_rate']:.1f}%"
        updates_per_sec_str = f"{result['updates_per_second']:.1f}/s"
        volatility_str = f"{result['price_volatility']:.2f}%"
        
        print(f"{result['trading_pair']:<20} {stars:<12} {duplicate_rate_str:<10} {updates_per_sec_str:<15} {volatility_str:<10}")
    
    print("-" * 80)
    print()
    
    # 分类统计
    high_liquidity = [r for r in sorted_results if r['liquidity_score'] >= 4]
    medium_liquidity = [r for r in sorted_results if 2 <= r['liquidity_score'] < 4]
    low_liquidity = [r for r in sorted_results if r['liquidity_score'] < 2]
    
    print("📈 流动性分类:")
    print(f"   • 高流动性 (⭐⭐⭐⭐+): {len(high_liquidity)} 个 - 适合高频交易 ✅")
    print(f"   • 中等流动性 (⭐⭐-⭐⭐⭐): {len(medium_liquidity)} 个 - 适合普通交易 ⚠️")
    print(f"   • 低流动性 (⭐-): {len(low_liquidity)} 个 - 不适合频繁交易 ❌")
    print()
    
    # 推荐
    print("💡 推荐采集策略:")
    print()
    
    if high_liquidity:
        print("   ✅ 高流动性币种（建议 5 秒采集）:")
        for r in high_liquidity:
            print(f"      • {r['trading_pair']:<20} (每秒变化 {r['updates_per_second']:.0f} 次)")
        print()
    
    if medium_liquidity:
        print("   ⚠️ 中等流动性币种（建议 15-30 秒采集）:")
        for r in medium_liquidity:
            print(f"      • {r['trading_pair']:<20} (每秒变化 {r['updates_per_second']:.1f} 次)")
        print()
    
    if low_liquidity:
        print("   ❌ 低流动性币种（建议 60 秒采集或移除）:")
        for r in low_liquidity:
            print(f"      • {r['trading_pair']:<20} (每秒变化 {r['updates_per_second']:.2f} 次, 重复率 {r['duplicate_rate']:.0f}%)")
        print()
    
    # 数据质量分析
    print("🔍 数据质量分析:")
    print()
    
    high_duplicate = [r for r in sorted_results if r['duplicate_rate'] > 50]
    if high_duplicate:
        print(f"   ⚠️ 高重复率币种 (>50%): {len(high_duplicate)} 个")
        for r in high_duplicate:
            print(f"      • {r['trading_pair']:<20} 重复率: {r['duplicate_rate']:.1f}%  (流动性太低)")
        print()
    
    # 存储效率分析
    print("💾 存储效率分析:")
    print()
    
    total_records = sum(r['total_records'] for r in sorted_results)
    total_unique = sum(r['unique_updates'] for r in sorted_results)
    total_duplicate = total_records - total_unique
    
    print(f"   • 总记录数: {total_records:,}")
    print(f"   • 唯一记录: {total_unique:,}")
    print(f"   • 重复记录: {total_duplicate:,} ({total_duplicate/total_records*100:.1f}%)")
    print()
    
    if total_duplicate > 0:
        potential_savings = (total_duplicate / total_records) * 100
        print(f"   💡 如果过滤重复，可节省 {potential_savings:.1f}% 的存储空间")
        print()
    
    print("=" * 80)
    print()


def main():
    """主函数"""
    
    # Gate.io 交易对列表
    gate_pairs = [
        'VIRTUAL-USDT',
        'LMTS-USDT',
        'BNKR-USDT',
        'PRO-USDT',
        'IRON-USDT',
        'MIGGLES-USDT'
    ]
    
    print("\n🔍 开始分析订单簿流动性...")
    print()
    
    # 分析所有交易对
    results = []
    for pair in gate_pairs:
        print(f"   分析 {pair}...", end=" ")
        result = analyze_liquidity(pair, 'gate_io')
        
        if 'error' in result:
            print(f"❌ {result['error']}")
        else:
            print(f"✅ ({result['total_records']} 条记录)")
        
        results.append(result)
    
    # 打印报告
    print_liquidity_report(results)
    
    # 检查是否有错误
    errors = [r for r in results if 'error' in r]
    if errors:
        print("⚠️ 以下交易对没有数据:")
        for error in errors:
            print(f"   • {error['trading_pair']}: {error['error']}")
        print()


if __name__ == "__main__":
    main()

