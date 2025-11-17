#!/usr/bin/env python3
"""
流动性与资金规模分析工具

功能：
1. 获取DEX池子的流动性深度（TVL）
2. 计算不同交易金额的滑点
3. 评估最优资金规模
4. 预估套利收益
"""
import sys
from pathlib import Path
import asyncio

import numpy as np
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_paths import data_paths
from geckoterminal_py import GeckoTerminalAsyncClient


class LiquidityAnalyzer:
    """流动性与资金规模分析器"""
    
    def __init__(self):
        self.gt_client = None
        
    async def initialize(self):
        """初始化异步客户端"""
        self.gt_client = GeckoTerminalAsyncClient()
    
    async def close(self):
        """关闭客户端"""
        if self.gt_client:
            await self.gt_client.close()
    
    async def get_pool_liquidity(self, network: str, pool_address: str):
        """
        获取池子的流动性信息
        
        Returns:
            dict: {
                'reserve_usd': float,  # 总锁仓量（USD）
                'base_reserve': float,  # Base token储备
                'quote_reserve': float, # Quote token储备
                'fee_rate': float       # 交易费率
            }
        """
        try:
            response = await self.gt_client.api_request(
                'GET', 
                f'/networks/{network}/pools/{pool_address}'
            )
            
            data = response.get('data', {})
            attributes = data.get('attributes', {})
            
            return {
                'reserve_usd': float(attributes.get('reserve_in_usd', 0)),
                'name': attributes.get('name', 'Unknown'),
                'base_token_price': float(attributes.get('base_token_price_usd', 0)),
                'quote_token_price': float(attributes.get('quote_token_price_usd', 0)),
                'fee_rate': 0.003  # 默认0.3%，实际需要从pool信息获取
            }
        except Exception as e:
            print(f"⚠️  获取流动性失败: {e}")
            return None
    
    def calculate_uniswap_v2_slippage(self, trade_amount_usd: float, reserve_usd: float) -> float:
        """
        计算Uniswap V2模型的滑点
        
        公式：slippage = 1 - sqrt(1 - x/R)
        其中 x = 交易金额, R = 储备金额
        
        Args:
            trade_amount_usd: 交易金额（USD）
            reserve_usd: 池子储备（USD）
        
        Returns:
            float: 滑点百分比
        """
        if reserve_usd == 0:
            return 100.0
        
        ratio = trade_amount_usd / reserve_usd
        
        # 如果交易金额超过储备的50%，滑点会非常大
        if ratio >= 0.5:
            return 100.0
        
        # 简化公式：对于小额交易，slippage ≈ x/R
        # 精确公式：slippage = 1 - sqrt(1 - x/R)
        slippage = (1 - np.sqrt(1 - ratio)) * 100
        
        return slippage
    
    def find_optimal_trade_size(self, reserve_usd: float, max_slippage_pct: float = 1.0):
        """
        找到在给定滑点限制下的最优交易金额
        
        Args:
            reserve_usd: 池子储备（USD）
            max_slippage_pct: 最大允许滑点（%）
        
        Returns:
            float: 最优交易金额（USD）
        """
        # 反向计算：给定滑点，求交易金额
        # slippage = 1 - sqrt(1 - x/R)
        # x = R * (1 - (1 - slippage)^2)
        
        slippage_ratio = max_slippage_pct / 100
        optimal_amount = reserve_usd * (1 - (1 - slippage_ratio) ** 2)
        
        return optimal_amount
    
    def calculate_profit(self, trade_amount: float, spread_pct: float, 
                        slippage_pct: float, fee_rate: float = 0.003, 
                        gas_fee: float = 0.01):
        """
        计算单次套利利润
        
        Args:
            trade_amount: 交易金额
            spread_pct: 价差（%）
            slippage_pct: 滑点（%）
            fee_rate: 交易费率（默认0.3%）
            gas_fee: Gas费（USD）
        
        Returns:
            dict: {
                'gross_profit': 毛利润,
                'net_profit': 净利润,
                'net_profit_pct': 净利润率（%）
            }
        """
        gross_profit = trade_amount * spread_pct / 100
        
        # 扣除成本
        slippage_cost = trade_amount * slippage_pct / 100
        fee_cost = trade_amount * fee_rate
        
        net_profit = gross_profit - slippage_cost - fee_cost - gas_fee
        net_profit_pct = (net_profit / trade_amount) * 100
        
        return {
            'gross_profit': gross_profit,
            'slippage_cost': slippage_cost,
            'fee_cost': fee_cost,
            'gas_cost': gas_fee,
            'net_profit': net_profit,
            'net_profit_pct': net_profit_pct
        }


async def analyze_pair_capital_requirement(pair: str, network: str = "base"):
    """分析单个交易对的资金需求"""
    
    print(f"\n{'='*80}")
    print(f"💰 {pair} 资金需求分析")
    print(f"{'='*80}\n")
    
    # 1. 加载pool mapping
    mapping_file = data_paths.processed_dir / "pool_mappings" / f"{network}_gate_io_pool_map.parquet"
    if not mapping_file.exists():
        print(f"❌ 未找到pool mapping文件: {mapping_file}")
        return
    
    df_mapping = pd.read_parquet(mapping_file)
    pool_info = df_mapping[df_mapping['trading_pair'] == pair]
    
    if pool_info.empty:
        print(f"❌ 未找到 {pair} 的pool映射")
        return
    
    pool_address = pool_info.iloc[0]['pool_address']
    print(f"📍 Pool地址: {pool_address}")
    
    # 2. 获取流动性数据
    analyzer = LiquidityAnalyzer()
    await analyzer.initialize()
    
    try:
        liquidity = await analyzer.get_pool_liquidity(network, pool_address)
        
        if not liquidity:
            print("❌ 无法获取流动性数据")
            return
        
        print(f"💧 流动性信息:")
        print(f"   池子名称: {liquidity['name']}")
        print(f"   总锁仓量: ${liquidity['reserve_usd']:,.0f}")
        print(f"   交易费率: {liquidity['fee_rate']*100:.2f}%")
        
        # 3. 加载价差数据
        spread_file = data_paths.spread_analysis_dir / f"spread_analysis_{pair}_1m.parquet"
        if not spread_file.exists():
            print(f"\n⚠️  未找到价差分析数据，请先运行:")
            print(f"   python scripts/analyze_cex_dex_spread.py --pair {pair}")
            return
        
        df_spread = pd.read_parquet(spread_file)
        real_trades = df_spread[~df_spread['dex_is_filled']]
        executable = real_trades[real_trades['is_executable']]
        
        avg_spread = real_trades['price_diff_pct'].abs().mean()
        print(f"\n📊 价差信息:")
        print(f"   平均价差: {avg_spread:.2f}%")
        print(f"   可执行机会: {len(executable)} 次")
        
        # 4. 计算不同交易金额的滑点和利润
        print(f"\n💹 滑点与利润分析:")
        print(f"{'─'*80}")
        print(f"{'交易金额':>12} | {'滑点':>8} | {'毛利润':>10} | {'净利润':>10} | {'净利润率':>10} | {'建议':>10}")
        print(f"{'─'*80}")
        
        trade_amounts = [100, 500, 1000, 5000, 10000, 50000, 100000]
        best_profit = -float('inf')
        best_amount = 0
        
        for amount in trade_amounts:
            slippage = analyzer.calculate_uniswap_v2_slippage(
                amount, 
                liquidity['reserve_usd'] / 2  # 单边储备约为总量的一半
            )
            
            profit = analyzer.calculate_profit(
                amount, 
                avg_spread, 
                slippage,
                liquidity['fee_rate']
            )
            
            # 判断建议
            recommendation = ""
            if profit['net_profit'] > 0 and slippage < 1.0:
                recommendation = "✓ 推荐"
                if profit['net_profit'] > best_profit:
                    best_profit = profit['net_profit']
                    best_amount = amount
            elif slippage >= 1.0:
                recommendation = "⚠️ 滑点大"
            elif profit['net_profit'] <= 0:
                recommendation = "✗ 不盈利"
            
            print(f"${amount:>10,.0f} | {slippage:>7.2f}% | "
                  f"${profit['gross_profit']:>9.2f} | "
                  f"${profit['net_profit']:>9.2f} | "
                  f"{profit['net_profit_pct']:>9.2f}% | "
                  f"{recommendation}")
        
        # 5. 最优交易金额建议
        optimal_1pct = analyzer.find_optimal_trade_size(liquidity['reserve_usd'] / 2, 1.0)
        optimal_05pct = analyzer.find_optimal_trade_size(liquidity['reserve_usd'] / 2, 0.5)
        
        print(f"\n🎯 最优交易金额:")
        print(f"   1%滑点限制: ${optimal_1pct:,.0f}")
        print(f"   0.5%滑点限制: ${optimal_05pct:,.0f}")
        
        if best_amount > 0:
            print(f"\n💰 建议交易金额: ${best_amount:,.0f}")
            print(f"   单次预期利润: ${best_profit:.2f}")
            
            # 计算所需总资金
            if len(executable) > 0:
                opportunities_per_day = len(executable) / 7  # 假设数据是7天的
                print(f"\n📅 机会频率: 约 {opportunities_per_day:.1f} 次/天")
                
                # 如果机会频繁（每天>10次），可以用较小资金滚动
                if opportunities_per_day > 10:
                    suggested_capital = best_amount * 2  # 2倍余量
                    print(f"\n💼 建议总资金: ${suggested_capital:,.0f}")
                    print(f"   （机会频繁，可滚动操作）")
                else:
                    suggested_capital = best_amount * 5  # 5倍余量
                    print(f"\n💼 建议总资金: ${suggested_capital:,.0f}")
                    print(f"   （机会较少，需要更多资金并行操作）")
                
                daily_profit = best_profit * opportunities_per_day
                monthly_profit = daily_profit * 30
                roi_monthly = (monthly_profit / suggested_capital) * 100
                
                print(f"\n📈 预期收益:")
                print(f"   日均利润: ${daily_profit:.2f}")
                print(f"   月度利润: ${monthly_profit:.2f}")
                print(f"   月度ROI: {roi_monthly:.2f}%")
        else:
            print(f"\n⚠️  所有交易金额均不盈利")
            print(f"   原因可能:")
            print(f"   • 价差太小（{avg_spread:.2f}%）")
            print(f"   • 流动性不足（${liquidity['reserve_usd']:,.0f}）")
            print(f"   • 手续费过高（{liquidity['fee_rate']*100:.2f}%）")
    
    finally:
        await analyzer.close()


async def compare_all_pairs_capital(network: str = "base"):
    """对比所有交易对的资金需求"""
    
    print(f"\n{'='*80}")
    print(f"💰 多交易对资金需求对比")
    print(f"{'='*80}\n")
    
    # 加载pool mapping
    mapping_file = data_paths.processed_dir / "pool_mappings" / f"{network}_gate_io_pool_map.parquet"
    if not mapping_file.exists():
        print(f"❌ 未找到pool mapping文件")
        return
    
    df_mapping = pd.read_parquet(mapping_file)
    pairs = df_mapping['trading_pair'].unique()
    
    analyzer = LiquidityAnalyzer()
    await analyzer.initialize()
    
    results = []
    
    try:
        for pair in pairs:
            pool_info = df_mapping[df_mapping['trading_pair'] == pair].iloc[0]
            pool_address = pool_info['pool_address']
            
            # 获取流动性
            liquidity = await analyzer.get_pool_liquidity(network, pool_address)
            if not liquidity:
                continue
            
            # 加载价差数据
            spread_file = data_paths.spread_analysis_dir / f"spread_analysis_{pair}_1m.parquet"
            if not spread_file.exists():
                continue
            
            df_spread = pd.read_parquet(spread_file)
            real_trades = df_spread[~df_spread['dex_is_filled']]
            
            if len(real_trades) == 0:
                continue
            
            avg_spread = real_trades['price_diff_pct'].abs().mean()
            
            # 计算最优交易金额（1%滑点限制）
            optimal_amount = analyzer.find_optimal_trade_size(
                liquidity['reserve_usd'] / 2, 
                1.0
            )
            
            # 计算该金额下的利润
            slippage = analyzer.calculate_uniswap_v2_slippage(
                optimal_amount,
                liquidity['reserve_usd'] / 2
            )
            
            profit = analyzer.calculate_profit(
                optimal_amount,
                avg_spread,
                slippage,
                liquidity['fee_rate']
            )
            
            results.append({
                'pair': pair,
                'reserve_usd': liquidity['reserve_usd'],
                'avg_spread': avg_spread,
                'optimal_amount': optimal_amount,
                'net_profit': profit['net_profit'],
                'net_profit_pct': profit['net_profit_pct']
            })
    
    finally:
        await analyzer.close()
    
    # 排序并显示
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('net_profit', ascending=False)
    
    print(f"{'交易对':15s} | {'流动性':>12s} | {'平均价差':>10s} | {'最优金额':>12s} | {'单次利润':>10s} | {'利润率':>8s}")
    print(f"{'─'*80}")
    
    for _, row in df_results.iterrows():
        print(f"{row['pair']:15s} | "
              f"${row['reserve_usd']:>11,.0f} | "
              f"{row['avg_spread']:>9.2f}% | "
              f"${row['optimal_amount']:>11,.0f} | "
              f"${row['net_profit']:>9.2f} | "
              f"{row['net_profit_pct']:>7.2f}%")
    
    print(f"\n💡 说明:")
    print(f"   • 最优金额：1%滑点限制下的最大交易金额")
    print(f"   • 单次利润：扣除滑点、手续费、Gas费后的净利润")
    print(f"   • 流动性高的交易对可以使用更大资金")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='流动性与资金规模分析工具')
    parser.add_argument('--pair', type=str, help='交易对（例如：AERO-USDT）')
    parser.add_argument('--network', type=str, default='base', help='网络（默认：base）')
    parser.add_argument('--compare-all', action='store_true', help='对比所有交易对')
    
    args = parser.parse_args()
    
    if args.compare_all:
        asyncio.run(compare_all_pairs_capital(args.network))
    elif args.pair:
        asyncio.run(analyze_pair_capital_requirement(args.pair, args.network))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

