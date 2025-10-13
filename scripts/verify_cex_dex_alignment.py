#!/usr/bin/env python3
"""
验证 CEX-DEX 数据时间对齐

检查下载的 DEX 数据是否与 CEX 数据正确对齐，包括：
1. 时间范围对齐
2. 数据完整性
3. 重叠时间段的数据对比
"""
import sys
from pathlib import Path

import pandas as pd
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_paths import data_paths


def verify_pair_alignment(trading_pair: str, interval: str = "1m"):
    """
    验证单个交易对的 CEX-DEX 对齐情况。
    
    Args:
        trading_pair: 交易对名称，如 "AERO-USDT"
        interval: 时间间隔，默认 "1m"
    """
    print("\n" + "="*80)
    print(f"📊 验证 {trading_pair} - {interval}")
    print("="*80)
    
    # 读取 CEX 数据
    cex_file = data_paths.candles_dir / f"gate_io|{trading_pair}|{interval}.parquet"
    dex_file = data_paths.candles_dir / f"geckoterminal_base|{trading_pair}|{interval}.parquet"
    
    if not cex_file.exists():
        print(f"⚠️  CEX 文件不存在: {cex_file.name}")
        return False
    
    if not dex_file.exists():
        print(f"⚠️  DEX 文件不存在: {dex_file.name}")
        return False
    
    # 读取数据
    cex_df = pd.read_parquet(cex_file)
    dex_df = pd.read_parquet(dex_file)
    
    print(f"\n📁 文件信息:")
    print(f"  CEX: {cex_file.name}")
    print(f"  DEX: {dex_file.name}")
    
    # 1. 基本统计
    print(f"\n1️⃣  基本统计:")
    print(f"  CEX K线数: {len(cex_df):,} 根")
    print(f"  DEX K线数: {len(dex_df):,} 根")
    print(f"  差异: {len(cex_df) - len(dex_df):,} 根 ({(len(dex_df)/len(cex_df)*100):.1f}% 覆盖率)")
    
    # 2. 时间范围对比
    print(f"\n2️⃣  时间范围对比:")
    cex_start, cex_end = cex_df.index.min(), cex_df.index.max()
    dex_start, dex_end = dex_df.index.min(), dex_df.index.max()
    
    print(f"  CEX 范围:")
    print(f"    开始: {cex_start}")
    print(f"    结束: {cex_end}")
    print(f"    持续: {(cex_end - cex_start).total_seconds() / 86400:.2f} 天")
    
    print(f"  DEX 范围:")
    print(f"    开始: {dex_start}")
    print(f"    结束: {dex_end}")
    print(f"    持续: {(dex_end - dex_start).total_seconds() / 86400:.2f} 天")
    
    # 检查对齐
    start_aligned = abs((cex_start - dex_start).total_seconds()) < 300  # 5分钟内
    end_aligned = abs((cex_end - dex_end).total_seconds()) < 300
    
    print(f"\n  时间对齐检查:")
    print(f"    开始时间对齐: {'✅ 是' if start_aligned else '❌ 否'} (差 {(dex_start - cex_start).total_seconds()/60:.1f} 分钟)")
    print(f"    结束时间对齐: {'✅ 是' if end_aligned else '❌ 否'} (差 {(dex_end - cex_end).total_seconds()/60:.1f} 分钟)")
    
    # 3. 重叠区域分析
    print(f"\n3️⃣  重叠区域分析:")
    
    # 找到共同时间段
    common_start = max(cex_start, dex_start)
    common_end = min(cex_end, dex_end)
    
    cex_common = cex_df[(cex_df.index >= common_start) & (cex_df.index <= common_end)]
    dex_common = dex_df[(dex_df.index >= common_start) & (dex_df.index <= common_end)]
    
    print(f"  共同时间段: {common_start} 至 {common_end}")
    print(f"  CEX 共同K线: {len(cex_common):,} 根")
    print(f"  DEX 共同K线: {len(dex_common):,} 根")
    
    # 4. 数据完整性检查
    print(f"\n4️⃣  数据完整性检查:")
    
    # 找到 CEX 有但 DEX 没有的时间戳
    missing_in_dex = cex_common.index.difference(dex_common.index)
    coverage_rate = (len(dex_common) / len(cex_common) * 100) if len(cex_common) > 0 else 0
    
    print(f"  CEX 中的时间戳: {len(cex_common):,}")
    print(f"  DEX 中的时间戳: {len(dex_common):,}")
    print(f"  DEX 缺失时间戳: {len(missing_in_dex):,}")
    print(f"  覆盖率: {coverage_rate:.2f}%")
    
    if len(missing_in_dex) > 0:
        print(f"\n  ⚠️  DEX 数据存在间隙（这是 DEX 的正常现象）:")
        print(f"     前 5 个缺失时间: {list(missing_in_dex[:5])}")
    
    # 5. 价格对比（共同时间戳）
    print(f"\n5️⃣  价格对比（共同时间戳）:")
    
    # 合并数据
    merged = cex_common.join(dex_common, how='inner', rsuffix='_dex')
    
    if len(merged) > 0:
        print(f"  共同时间戳数: {len(merged):,}")
        
        # 计算价格差异
        price_diff = ((merged['close_dex'] - merged['close']) / merged['close'] * 100).abs()
        
        print(f"\n  收盘价差异统计:")
        print(f"    平均: {price_diff.mean():.4f}%")
        print(f"    中位数: {price_diff.median():.4f}%")
        print(f"    最大: {price_diff.max():.4f}%")
        print(f"    最小: {price_diff.min():.4f}%")
        
        # 显示示例
        print(f"\n  示例对比（最近 3 个时间点）:")
        for idx in merged.tail(3).index:
            cex_close = merged.loc[idx, 'close']
            dex_close = merged.loc[idx, 'close_dex']
            diff_pct = (dex_close - cex_close) / cex_close * 100
            print(f"    {idx}: CEX=${cex_close:.6f}, DEX=${dex_close:.6f}, 差异={diff_pct:+.4f}%")
    else:
        print(f"  ⚠️  没有共同的时间戳！")
    
    # 6. 总结
    print(f"\n6️⃣  验证总结:")
    
    all_checks_passed = (
        start_aligned and
        end_aligned and
        coverage_rate >= 50.0 and  # 至少 50% 覆盖率
        len(dex_df) > 100  # 至少有 100 根K线
    )
    
    if all_checks_passed:
        print(f"  ✅ 时间对齐验证通过")
        print(f"  ✅ 数据质量良好")
        print(f"  ✅ DEX 数据覆盖率: {coverage_rate:.1f}%")
    else:
        print(f"  ⚠️  发现以下问题:")
        if not start_aligned:
            print(f"     - 开始时间未对齐")
        if not end_aligned:
            print(f"     - 结束时间未对齐")
        if coverage_rate < 50.0:
            print(f"     - 覆盖率过低: {coverage_rate:.1f}%")
        if len(dex_df) <= 100:
            print(f"     - DEX 数据过少")
    
    return all_checks_passed


def main():
    """主函数 - 验证所有交易对。"""
    print("="*80)
    print("🔍 CEX-DEX 数据对齐验证工具")
    print("="*80)
    
    # 找到所有 DEX 1m 文件
    dex_files = list(data_paths.candles_dir.glob("geckoterminal_base|*-USDT|1m.parquet"))
    
    if not dex_files:
        print("\n❌ 没有找到 DEX 1m 数据文件！")
        print("   请先运行: python scripts/run_dex_cex_aligned.py")
        return 1
    
    print(f"\n找到 {len(dex_files)} 个 DEX 1m 数据文件")
    
    # 提取交易对名称
    pairs = []
    for file in dex_files:
        parts = file.stem.split('|')
        if len(parts) >= 2:
            pairs.append(parts[1])
    
    print(f"交易对: {', '.join(pairs)}")
    
    # 验证每个交易对
    results = {}
    for pair in pairs:
        passed = verify_pair_alignment(pair, "1m")
        results[pair] = passed
    
    # 总结
    print("\n" + "="*80)
    print("🎯 总体验证结果")
    print("="*80)
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n总计: {total_count} 个交易对")
    print(f"通过: {passed_count} 个 ✅")
    print(f"失败: {total_count - passed_count} 个 ❌")
    
    print(f"\n详细结果:")
    for pair, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {pair}: {status}")
    
    if passed_count == total_count:
        print("\n" + "="*80)
        print("✅ 所有交易对的 CEX-DEX 数据对齐验证通过！")
        print("="*80)
        print("\n✨ DEX 数据已成功与 CEX 数据对齐")
        print("   - 时间范围一致")
        print("   - 数据覆盖率良好")
        print("   - 可以开始分析 CEX-DEX 价差")
        return 0
    else:
        print("\n" + "="*80)
        print("⚠️  部分交易对验证未通过")
        print("="*80)
        print("\n请检查上述报告中的具体问题")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

