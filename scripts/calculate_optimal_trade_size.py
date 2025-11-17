#!/usr/bin/env python3
"""
计算 CEX-DEX 套利的最优交易规模

核心逻辑：
1. DEX 滑点计算（基于 AMM 公式）
2. CEX 滑点估算（基于订单簿或成交量）
3. 净利润优化（价差 - 双向滑点 - 手续费）

使用的历史数据：
- DEX: reserve_usd, volume_usd_h24（来自 pool_mapping）
- CEX: volume（来自 OHLCV 数据）
- 价差：来自 spread analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional
import argparse
from core.data_paths import data_paths


class TradeSizeOptimizer:
    """交易规模优化器"""
    
    def __init__(self, trading_pair: str, connector: str = "mexc", network: str = "base"):
        self.trading_pair = trading_pair
        self.connector = connector
        self.network = network
        
        # 默认手续费率
        self.cex_fee_rate = 0.001  # 0.1% (Gate.io/MEXC Maker)
        self.dex_fee_rate = 0.003  # 0.3% (Uniswap V2/V3)
        
    def load_pool_data(self) -> Optional[pd.Series]:
        """加载 DEX 流动性池数据"""
        pool_file = data_paths.processed_dir / "pool_mappings" / f"{self.network}_{self.connector}_pool_map.parquet"
        
        if not pool_file.exists():
            print(f"❌ 未找到 pool mapping: {pool_file}")
            return None
        
        df = pd.read_parquet(pool_file)
        pools = df[df['trading_pair'] == self.trading_pair]
        
        if pools.empty:
            print(f"❌ 未找到 {self.trading_pair} 的池子数据")
            return None
        
        # 选择 rank=1 的池子（最优池）
        best_pool = pools[pools['rank'] == 1].iloc[0] if (pools['rank'] == 1).any() else pools.iloc[0]
        return best_pool
    
    def load_cex_volume(self) -> float:
        """加载 CEX 平均成交量（从 OHLCV 数据）"""
        cex_file = data_paths.candles_dir / f"{self.connector}|{self.trading_pair}|1m.parquet"
        
        if not cex_file.exists():
            print(f"❌ 未找到 CEX 数据: {cex_file}")
            return 0.0
        
        df = pd.read_parquet(cex_file)
        
        # 计算平均每分钟成交量（USD）
        if 'volume' in df.columns and 'close' in df.columns:
            avg_volume_usd = (df['volume'] * df['close']).mean()
            return avg_volume_usd
        
        return 0.0
    
    def calculate_dex_slippage(self, trade_size_usd: float, reserve_usd: float) -> float:
        """
        计算 DEX 滑点（基于 AMM 恒定乘积公式）
        
        对于 Uniswap V2/V3 的简化模型：
        slippage ≈ trade_size / (2 × reserve) × 100%
        
        更精确的公式（考虑恒定乘积）：
        price_impact = 1 - (1 - trade_size / reserve_in)
        
        Args:
            trade_size_usd: 交易规模（美元）
            reserve_usd: 池子储备量（美元）
        
        Returns:
            滑点百分比（如 0.5 表示 0.5%）
        """
        if reserve_usd <= 0:
            return 100.0  # 无流动性
        
        # 简化模型：线性近似（适用于小额交易）
        if trade_size_usd / reserve_usd < 0.01:  # < 1% 池子规模
            slippage = (trade_size_usd / (2 * reserve_usd)) * 100
        else:
            # 精确模型：AMM 恒定乘积公式
            # Δy = (x × Δx) / (X - Δx)  其中 X 是储备量，Δx 是买入量
            ratio = trade_size_usd / reserve_usd
            price_impact = ratio / (1 - ratio)
            slippage = price_impact * 100
        
        return slippage
    
    def calculate_cex_slippage(self, trade_size_usd: float, avg_volume_usd: float) -> float:
        """
        估算 CEX 滑点（基于历史成交量）
        
        假设：
        - 如果交易量 < 平均成交量，滑点很小
        - 如果交易量 > 平均成交量，会吃掉挂单造成滑点
        
        简化模型：
        slippage ≈ (trade_size / avg_volume - 1) × 基准滑点
        
        Args:
            trade_size_usd: 交易规模（美元）
            avg_volume_usd: 平均每分钟成交量（美元）
        
        Returns:
            估算滑点百分比
        """
        if avg_volume_usd <= 0:
            return 10.0  # 无成交量，高滑点
        
        ratio = trade_size_usd / avg_volume_usd
        
        if ratio < 0.1:  # 交易量 < 10% 平均成交量
            return 0.05  # 极小滑点
        elif ratio < 0.5:  # 10% - 50%
            return 0.1 + (ratio - 0.1) * 0.5
        elif ratio < 1.0:  # 50% - 100%
            return 0.3 + (ratio - 0.5) * 1.0
        else:  # > 100%
            return 0.8 + (ratio - 1.0) * 2.0  # 高滑点
    
    def calculate_net_profit(
        self, 
        trade_size_usd: float, 
        price_spread_pct: float,
        reserve_usd: float,
        avg_volume_usd: float
    ) -> Dict:
        """
        计算净利润
        
        净利润 = 价差收益 - DEX滑点 - CEX滑点 - 手续费
        
        Returns:
            包含详细计算结果的字典
        """
        # 计算各项成本
        dex_slippage = self.calculate_dex_slippage(trade_size_usd, reserve_usd)
        cex_slippage = self.calculate_cex_slippage(trade_size_usd, avg_volume_usd)
        total_fees = (self.cex_fee_rate + self.dex_fee_rate) * 100  # 转为百分比
        
        # 净价差
        net_spread_pct = price_spread_pct - dex_slippage - cex_slippage - total_fees
        
        # 净利润（美元）
        net_profit_usd = (net_spread_pct / 100) * trade_size_usd
        
        # ROI
        roi_pct = net_spread_pct
        
        return {
            'trade_size_usd': trade_size_usd,
            'gross_spread_pct': price_spread_pct,
            'dex_slippage_pct': dex_slippage,
            'cex_slippage_pct': cex_slippage,
            'total_fees_pct': total_fees,
            'net_spread_pct': net_spread_pct,
            'net_profit_usd': net_profit_usd,
            'roi_pct': roi_pct,
        }
    
    def find_optimal_size(
        self, 
        price_spread_pct: float,
        reserve_usd: float,
        avg_volume_usd: float,
        max_trade_size_usd: float = 50000
    ) -> Tuple[float, Dict]:
        """
        寻找最优交易规模（使净利润最大化）
        
        策略：
        1. 从小到大扫描不同交易规模
        2. 计算每个规模的净利润
        3. 返回净利润最大的规模
        
        Args:
            price_spread_pct: 价差百分比（如 2.5 表示 2.5%）
            reserve_usd: DEX 池子储备（美元）
            avg_volume_usd: CEX 平均成交量（美元/分钟）
            max_trade_size_usd: 最大交易规模（美元）
        
        Returns:
            (最优规模, 详细计算结果)
        """
        # 生成候选交易规模（对数刻度）
        trade_sizes = np.logspace(1, np.log10(max_trade_size_usd), 100)  # $10 到 $50K
        
        results = []
        for size in trade_sizes:
            result = self.calculate_net_profit(size, price_spread_pct, reserve_usd, avg_volume_usd)
            results.append(result)
        
        # 找到净利润最大的规模
        df_results = pd.DataFrame(results)
        
        # 过滤掉净利润为负的
        df_profitable = df_results[df_results['net_profit_usd'] > 0]
        
        if df_profitable.empty:
            print(f"⚠️  在任何交易规模下都无法盈利（价差太小或流动性不足）")
            best_idx = df_results['net_profit_usd'].idxmax()
            return trade_sizes[best_idx], results[best_idx]
        
        best_idx = df_profitable['net_profit_usd'].idxmax()
        optimal_size = df_profitable.loc[best_idx, 'trade_size_usd']
        optimal_result = df_profitable.loc[best_idx].to_dict()
        
        return optimal_size, optimal_result
    
    def optimize(self, price_spread_pct: float) -> Optional[Dict]:
        """
        执行完整的优化流程
        
        Args:
            price_spread_pct: 观察到的价差百分比
        
        Returns:
            优化结果字典
        """
        print(f"\n{'='*80}")
        print(f"🎯 交易规模优化：{self.trading_pair} ({self.connector} ↔ {self.network} DEX)")
        print(f"{'='*80}\n")
        
        # 1. 加载 DEX 流动性数据
        print("📊 步骤 1：加载 DEX 流动性数据")
        pool_data = self.load_pool_data()
        if pool_data is None:
            return None
        
        reserve_usd = pool_data['reserve_usd']
        dex_id = pool_data['dex_id']
        volume_24h = pool_data['volume_usd_h24']
        
        print(f"   ✓ DEX: {dex_id}")
        print(f"   ✓ 池子储备 (TVL): ${reserve_usd:,.2f}")
        print(f"   ✓ 24h 交易量: ${volume_24h:,.2f}")
        
        # 2. 加载 CEX 成交量
        print(f"\n📊 步骤 2：加载 CEX 成交量")
        avg_volume_usd = self.load_cex_volume()
        print(f"   ✓ 平均每分钟成交量: ${avg_volume_usd:,.2f}")
        
        # 3. 优化交易规模
        print(f"\n🔍 步骤 3：寻找最优交易规模")
        print(f"   ✓ 输入价差: {price_spread_pct:.2f}%")
        
        optimal_size, optimal_result = self.find_optimal_size(
            price_spread_pct=price_spread_pct,
            reserve_usd=reserve_usd,
            avg_volume_usd=avg_volume_usd
        )
        
        # 4. 显示结果
        print(f"\n{'='*80}")
        print(f"✅ 优化结果")
        print(f"{'='*80}\n")
        
        print(f"💰 最优交易规模: ${optimal_size:,.2f}")
        print(f"\n📈 收益分解:")
        print(f"   • 毛价差:      {optimal_result['gross_spread_pct']:>6.2f}%")
        print(f"   • DEX 滑点:   -{optimal_result['dex_slippage_pct']:>6.2f}%")
        print(f"   • CEX 滑点:   -{optimal_result['cex_slippage_pct']:>6.2f}%")
        print(f"   • 手续费:     -{optimal_result['total_fees_pct']:>6.2f}%")
        print(f"   {'─'*40}")
        print(f"   • 净价差:      {optimal_result['net_spread_pct']:>6.2f}%")
        print(f"\n💵 预期净利润: ${optimal_result['net_profit_usd']:,.2f} / 次")
        print(f"📊 ROI: {optimal_result['roi_pct']:.2f}%")
        
        # 风险评估
        print(f"\n⚠️  风险评估:")
        
        # 流动性比率
        liquidity_ratio = optimal_size / reserve_usd * 100
        if liquidity_ratio < 1:
            risk_level = "🟢 低"
        elif liquidity_ratio < 3:
            risk_level = "🟡 中"
        else:
            risk_level = "🔴 高"
        
        print(f"   • 交易占池子比例: {liquidity_ratio:.2f}% ({risk_level})")
        
        # 成交量比率
        volume_ratio = optimal_size / avg_volume_usd
        if volume_ratio < 0.5:
            volume_risk = "🟢 低"
        elif volume_ratio < 2:
            volume_risk = "🟡 中"
        else:
            volume_risk = "🔴 高"
        
        print(f"   • 交易占CEX成交量: {volume_ratio:.1f}x ({volume_risk})")
        
        # 建议
        print(f"\n💡 操作建议:")
        if optimal_result['net_spread_pct'] > 0.5:
            print(f"   ✅ 套利机会良好，建议执行")
            print(f"   📍 建议交易规模: ${optimal_size * 0.8:,.2f} - ${optimal_size:,.2f}")
            print(f"   ⏱️  建议频率: 根据价差出现频率调整")
        elif optimal_result['net_spread_pct'] > 0:
            print(f"   ⚠️  套利空间较小，谨慎执行")
            print(f"   📍 建议交易规模: ${optimal_size * 0.5:,.2f}")
        else:
            print(f"   ❌ 当前价差不足以覆盖成本，不建议执行")
        
        print(f"\n{'='*80}\n")
        
        return {
            'optimal_size_usd': optimal_size,
            'reserve_usd': reserve_usd,
            'avg_volume_usd': avg_volume_usd,
            **optimal_result
        }


def main():
    parser = argparse.ArgumentParser(
        description="计算 CEX-DEX 套利的最优交易规模",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

1. 分析单个交易对（手动输入价差）:
   python scripts/calculate_optimal_trade_size.py --pair IRON-USDT --spread 7.87 --connector mexc

2. 分析 HINT-USDT（价差 0.5%）:
   python scripts/calculate_optimal_trade_size.py --pair HINT-USDT --spread 0.5 --connector mexc

3. 指定最大交易规模:
   python scripts/calculate_optimal_trade_size.py --pair IRON-USDT --spread 7.87 --connector mexc --max-size 100000

数据来源:
- DEX 流动性: app/data/processed/pool_mappings/*.parquet
- CEX 成交量: app/data/cache/candles/*.parquet
- 价差: 来自 analyze_cex_dex_spread.py 的分析结果
        """
    )
    
    parser.add_argument('--pair', type=str, required=True, help='交易对，如 IRON-USDT')
    parser.add_argument('--spread', type=float, required=True, help='观察到的价差百分比，如 7.87')
    parser.add_argument('--connector', type=str, default='mexc', help='CEX 连接器 (默认: mexc)')
    parser.add_argument('--network', type=str, default='base', help='DEX 网络 (默认: base)')
    parser.add_argument('--max-size', type=float, default=50000, help='最大交易规模 USD (默认: 50000)')
    parser.add_argument('--cex-fee', type=float, default=0.001, help='CEX 手续费率 (默认: 0.001 = 0.1%%)')
    parser.add_argument('--dex-fee', type=float, default=0.003, help='DEX 手续费率 (默认: 0.003 = 0.3%%)')
    
    args = parser.parse_args()
    
    # 创建优化器
    optimizer = TradeSizeOptimizer(
        trading_pair=args.pair,
        connector=args.connector,
        network=args.network
    )
    
    # 设置手续费
    optimizer.cex_fee_rate = args.cex_fee
    optimizer.dex_fee_rate = args.dex_fee
    
    # 执行优化
    result = optimizer.optimize(price_spread_pct=args.spread)
    
    if result is None:
        print("❌ 优化失败：无法加载必要数据")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

