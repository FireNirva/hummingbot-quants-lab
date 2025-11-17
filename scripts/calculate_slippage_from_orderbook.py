#!/usr/bin/env python3
"""
基于真实订单簿数据精确计算 CEX 滑点

数据源：Crypto Lake (https://crypto-lake.com)
数据类型：book_1m 或 deep_book_1m

使用方法：
1. 订阅 Crypto Lake
2. 下载目标交易对的订单簿数据
3. 使用本脚本计算不同交易规模的精确滑点
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


class OrderBookSlippageCalculator:
    """基于真实订单簿的滑点计算器"""
    
    def __init__(self, orderbook_file: str):
        """
        初始化计算器
        
        Args:
            orderbook_file: Crypto Lake 订单簿数据文件路径
                           支持 book_1m.parquet 或 deep_book_1m.parquet
        """
        self.orderbook_file = Path(orderbook_file)
        self.df = None
        self.is_deep_book = 'deep_book' in orderbook_file
        
    def load_data(self) -> bool:
        """加载订单簿数据"""
        if not self.orderbook_file.exists():
            print(f"❌ 文件不存在: {self.orderbook_file}")
            return False
        
        try:
            self.df = pd.read_parquet(self.orderbook_file)
            print(f"✅ 加载订单簿数据: {len(self.df)} 个快照")
            print(f"   时间范围: {self.df['received_time'].min()} 到 {self.df['received_time'].max()}")
            return True
        except Exception as e:
            print(f"❌ 加载失败: {e}")
            return False
    
    def parse_snapshot_standard(self, row: pd.Series) -> Tuple[List[float], List[float], List[float], List[float]]:
        """
        解析标准订单簿快照（book_1m - 20 档）
        
        Returns:
            (bid_prices, bid_sizes, ask_prices, ask_sizes)
        """
        bid_prices = []
        bid_sizes = []
        ask_prices = []
        ask_sizes = []
        
        for i in range(20):
            bid_price = row.get(f'bid_{i}_price')
            bid_size = row.get(f'bid_{i}_size')
            ask_price = row.get(f'ask_{i}_price')
            ask_size = row.get(f'ask_{i}_size')
            
            if pd.notna(bid_price) and pd.notna(bid_size) and bid_size > 0:
                bid_prices.append(bid_price)
                bid_sizes.append(bid_size)
            
            if pd.notna(ask_price) and pd.notna(ask_size) and ask_size > 0:
                ask_prices.append(ask_price)
                ask_sizes.append(ask_size)
        
        return bid_prices, bid_sizes, ask_prices, ask_sizes
    
    def parse_snapshot_deep(self, row: pd.Series) -> Tuple[List[float], List[float], List[float], List[float]]:
        """
        解析深度订单簿快照（deep_book_1m - 1000+ 档）
        
        Returns:
            (bid_prices, bid_sizes, ask_prices, ask_sizes)
        """
        bid_prices = row['bid_prices']
        bid_sizes = row['bid_sizes']
        ask_prices = row['ask_prices']
        ask_sizes = row['ask_sizes']
        
        return bid_prices, bid_sizes, ask_prices, ask_sizes
    
    def calculate_buy_slippage(
        self, 
        ask_prices: List[float], 
        ask_sizes: List[float], 
        trade_size_quote: float
    ) -> Dict:
        """
        计算买入订单的滑点（吃掉卖单）
        
        Args:
            ask_prices: 卖单价格列表（升序）
            ask_sizes: 卖单数量列表（基础货币）
            trade_size_quote: 交易规模（报价货币，如 USDT）
        
        Returns:
            {
                'avg_price': 平均成交价,
                'best_price': 最佳价格（ask_0）,
                'slippage_pct': 滑点百分比,
                'filled_completely': 是否完全成交,
                'levels_consumed': 消耗的价格档位数
            }
        """
        if not ask_prices or trade_size_quote <= 0:
            return None
        
        best_price = ask_prices[0]
        remaining_value = trade_size_quote
        total_base = 0.0  # 买到的基础货币数量
        total_cost = 0.0  # 总花费（报价货币）
        levels_consumed = 0
        
        for price, size in zip(ask_prices, ask_sizes):
            if remaining_value <= 0:
                break
            
            # 当前档位可以买到的价值
            available_value = price * size
            
            if available_value <= remaining_value:
                # 吃掉整个档位
                total_base += size
                total_cost += available_value
                remaining_value -= available_value
                levels_consumed += 1
            else:
                # 只吃掉部分
                partial_base = remaining_value / price
                total_base += partial_base
                total_cost += remaining_value
                remaining_value = 0
                levels_consumed += 1
        
        # 计算结果
        filled_completely = (remaining_value <= 0)
        avg_price = total_cost / total_base if total_base > 0 else best_price
        slippage_pct = ((avg_price - best_price) / best_price) * 100
        
        return {
            'avg_price': avg_price,
            'best_price': best_price,
            'slippage_pct': slippage_pct,
            'filled_completely': filled_completely,
            'levels_consumed': levels_consumed,
            'total_base_bought': total_base,
            'total_cost': total_cost,
        }
    
    def calculate_sell_slippage(
        self, 
        bid_prices: List[float], 
        bid_sizes: List[float], 
        trade_size_base: float
    ) -> Dict:
        """
        计算卖出订单的滑点（吃掉买单）
        
        Args:
            bid_prices: 买单价格列表（降序）
            bid_sizes: 买单数量列表（基础货币）
            trade_size_base: 交易规模（基础货币，如 BTC）
        
        Returns:
            同 calculate_buy_slippage
        """
        if not bid_prices or trade_size_base <= 0:
            return None
        
        best_price = bid_prices[0]
        remaining_base = trade_size_base
        total_revenue = 0.0  # 总收入（报价货币）
        levels_consumed = 0
        
        for price, size in zip(bid_prices, bid_sizes):
            if remaining_base <= 0:
                break
            
            if size <= remaining_base:
                # 吃掉整个档位
                total_revenue += price * size
                remaining_base -= size
                levels_consumed += 1
            else:
                # 只吃掉部分
                total_revenue += price * remaining_base
                remaining_base = 0
                levels_consumed += 1
        
        # 计算结果
        filled_completely = (remaining_base <= 0)
        total_base_sold = trade_size_base - remaining_base
        avg_price = total_revenue / total_base_sold if total_base_sold > 0 else best_price
        slippage_pct = ((best_price - avg_price) / best_price) * 100  # 注意：卖出时是负滑点
        
        return {
            'avg_price': avg_price,
            'best_price': best_price,
            'slippage_pct': slippage_pct,
            'filled_completely': filled_completely,
            'levels_consumed': levels_consumed,
            'total_base_sold': total_base_sold,
            'total_revenue': total_revenue,
        }
    
    def analyze_trade_size_impact(
        self, 
        trade_sizes_usd: List[float],
        side: str = 'buy',
        sample_size: int = 100
    ) -> pd.DataFrame:
        """
        分析不同交易规模对滑点的影响
        
        Args:
            trade_sizes_usd: 要测试的交易规模列表（USD）
            side: 'buy' 或 'sell'
            sample_size: 采样快照数量
        
        Returns:
            DataFrame with columns: trade_size, avg_slippage, max_slippage, unfilled_rate
        """
        if self.df is None or len(self.df) == 0:
            print("❌ 请先加载数据")
            return pd.DataFrame()
        
        # 随机采样
        sample_df = self.df.sample(min(sample_size, len(self.df)))
        
        results = []
        
        for trade_size in trade_sizes_usd:
            slippages = []
            unfilled_count = 0
            
            for _, row in sample_df.iterrows():
                # 解析订单簿快照
                if self.is_deep_book:
                    bid_prices, bid_sizes, ask_prices, ask_sizes = self.parse_snapshot_deep(row)
                else:
                    bid_prices, bid_sizes, ask_prices, ask_sizes = self.parse_snapshot_standard(row)
                
                # 计算滑点
                if side == 'buy':
                    result = self.calculate_buy_slippage(ask_prices, ask_sizes, trade_size)
                else:
                    # 对于卖出，需要先将 USD 转换为基础货币数量
                    best_bid = bid_prices[0] if bid_prices else 0
                    trade_size_base = trade_size / best_bid if best_bid > 0 else 0
                    result = self.calculate_sell_slippage(bid_prices, bid_sizes, trade_size_base)
                
                if result:
                    slippages.append(result['slippage_pct'])
                    if not result['filled_completely']:
                        unfilled_count += 1
            
            # 统计
            if slippages:
                results.append({
                    'trade_size_usd': trade_size,
                    'avg_slippage_pct': np.mean(slippages),
                    'median_slippage_pct': np.median(slippages),
                    'max_slippage_pct': np.max(slippages),
                    'std_slippage_pct': np.std(slippages),
                    'unfilled_rate_pct': (unfilled_count / len(slippages)) * 100,
                })
        
        return pd.DataFrame(results)
    
    def recommend_optimal_size(
        self, 
        max_slippage_pct: float = 0.5,
        side: str = 'buy'
    ) -> Dict:
        """
        推荐最优交易规模（基于最大可接受滑点）
        
        Args:
            max_slippage_pct: 最大可接受滑点（%）
            side: 'buy' 或 'sell'
        
        Returns:
            {
                'optimal_size_usd': 推荐交易规模,
                'expected_slippage_pct': 预期滑点,
                'confidence': 置信度
            }
        """
        # 测试不同规模
        test_sizes = np.logspace(1, 5, 20)  # $10 到 $100K
        
        print(f"\n🔍 正在测试 {len(test_sizes)} 个交易规模...")
        df_impact = self.analyze_trade_size_impact(test_sizes, side=side, sample_size=50)
        
        if df_impact.empty:
            return None
        
        # 找到滑点小于阈值的最大规模
        acceptable = df_impact[df_impact['avg_slippage_pct'] <= max_slippage_pct]
        
        if acceptable.empty:
            print(f"⚠️  所有测试规模的滑点都超过 {max_slippage_pct}%")
            best = df_impact.iloc[0]
        else:
            best = acceptable.iloc[-1]  # 最大的可接受规模
        
        return {
            'optimal_size_usd': best['trade_size_usd'],
            'expected_slippage_pct': best['avg_slippage_pct'],
            'max_slippage_pct': best['max_slippage_pct'],
            'confidence': 100 - best['unfilled_rate_pct'],
        }


def main():
    parser = argparse.ArgumentParser(
        description="基于真实订单簿计算 CEX 滑点",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：

1. 分析单个交易规模的滑点：
   python scripts/calculate_slippage_from_orderbook.py \\
     --file data/crypto_lake/BINANCE/BTC-USDT/book_1m.parquet \\
     --size 1000 \\
     --side buy

2. 推荐最优交易规模（最大滑点 0.3%）：
   python scripts/calculate_slippage_from_orderbook.py \\
     --file data/crypto_lake/BINANCE/BTC-USDT/deep_book_1m.parquet \\
     --recommend \\
     --max-slippage 0.3

3. 批量分析不同规模：
   python scripts/calculate_slippage_from_orderbook.py \\
     --file data/crypto_lake/BINANCE/BTC-USDT/book_1m.parquet \\
     --batch "100,500,1000,5000,10000" \\
     --side buy

数据获取：
1. 访问 https://crypto-lake.com
2. 订阅 For individuals 计划（$70/月，300GB）
3. 使用 lakeapi 下载数据：
   
   pip install lakeapi
   
   import lakeapi
   from datetime import datetime
   
   df = lakeapi.load_data(
       table='book_1m',
       start=datetime(2024, 1, 1),
       end=datetime(2024, 1, 7),
       symbols=['BTC-USDT'],
       exchanges=['BINANCE']
   )
   df.to_parquet('book_1m.parquet')
        """
    )
    
    parser.add_argument('--file', type=str, required=True, 
                        help='订单簿数据文件（Parquet 格式）')
    parser.add_argument('--size', type=float, help='单次交易规模（USD）')
    parser.add_argument('--side', type=str, default='buy', choices=['buy', 'sell'],
                        help='交易方向')
    parser.add_argument('--recommend', action='store_true', 
                        help='推荐最优交易规模')
    parser.add_argument('--max-slippage', type=float, default=0.5,
                        help='最大可接受滑点（%%，默认 0.5）')
    parser.add_argument('--batch', type=str, 
                        help='批量分析多个规模（逗号分隔，如 "100,500,1000"）')
    
    args = parser.parse_args()
    
    # 创建计算器
    calc = OrderBookSlippageCalculator(args.file)
    
    if not calc.load_data():
        return 1
    
    # 模式 1: 推荐最优规模
    if args.recommend:
        print(f"\n{'='*80}")
        print(f"🎯 推荐最优交易规模（最大滑点: {args.max_slippage}%）")
        print(f"{'='*80}\n")
        
        result = calc.recommend_optimal_size(
            max_slippage_pct=args.max_slippage,
            side=args.side
        )
        
        if result:
            print(f"💰 推荐规模: ${result['optimal_size_usd']:,.2f}")
            print(f"📊 预期滑点: {result['expected_slippage_pct']:.4f}%")
            print(f"📈 最大滑点: {result['max_slippage_pct']:.4f}%")
            print(f"✅ 成功率: {result['confidence']:.1f}%")
    
    # 模式 2: 批量分析
    elif args.batch:
        sizes = [float(x.strip()) for x in args.batch.split(',')]
        
        print(f"\n{'='*80}")
        print(f"📊 批量滑点分析")
        print(f"{'='*80}\n")
        
        df_impact = calc.analyze_trade_size_impact(sizes, side=args.side)
        
        print("\n规模 (USD) | 平均滑点 | 中位滑点 | 最大滑点 | 未成交率")
        print("─" * 80)
        for _, row in df_impact.iterrows():
            print(f"${row['trade_size_usd']:>9,.0f} | {row['avg_slippage_pct']:>8.4f}% | "
                  f"{row['median_slippage_pct']:>8.4f}% | {row['max_slippage_pct']:>8.4f}% | "
                  f"{row['unfilled_rate_pct']:>7.2f}%")
    
    # 模式 3: 单次分析
    elif args.size:
        print(f"\n{'='*80}")
        print(f"📊 交易规模分析: ${args.size:,.2f} ({args.side})")
        print(f"{'='*80}\n")
        
        df_impact = calc.analyze_trade_size_impact([args.size], side=args.side, sample_size=100)
        
        if not df_impact.empty:
            row = df_impact.iloc[0]
            print(f"平均滑点: {row['avg_slippage_pct']:.4f}%")
            print(f"中位滑点: {row['median_slippage_pct']:.4f}%")
            print(f"最大滑点: {row['max_slippage_pct']:.4f}%")
            print(f"滑点标准差: {row['std_slippage_pct']:.4f}%")
            print(f"未成交率: {row['unfilled_rate_pct']:.2f}%")
    
    else:
        print("❌ 请指定 --size, --batch 或 --recommend")
        return 1
    
    print(f"\n{'='*80}\n")
    return 0


if __name__ == "__main__":
    exit(main())

