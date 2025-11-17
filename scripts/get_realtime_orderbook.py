#!/usr/bin/env python3
"""
实时获取交易所订单簿数据

免费使用 Gate.io 和 MEXC 的公开 API
无需 Crypto Lake 订阅
"""

import requests
from typing import Dict, List, Tuple
import time


class OrderBookFetcher:
    """实时订单簿获取器"""
    
    @staticmethod
    def get_gateio_orderbook(symbol: str, limit: int = 100) -> Dict:
        """
        获取 Gate.io 订单簿
        
        Args:
            symbol: 交易对（如 'IRON_USDT'）
            limit: 深度档位（最大 100）
        
        Returns:
            {
                'bids': [[price, amount], ...],
                'asks': [[price, amount], ...],
                'timestamp': int
            }
        """
        url = "https://api.gateio.ws/api/v4/spot/order_book"
        params = {
            "currency_pair": symbol.replace('-', '_'),
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'bids': [[float(price), float(amount)] for price, amount in data['bids']],
                'asks': [[float(price), float(amount)] for price, amount in data['asks']],
                'timestamp': int(time.time() * 1000)
            }
        except Exception as e:
            print(f"❌ Gate.io 获取失败: {e}")
            return None
    
    @staticmethod
    def get_mexc_orderbook(symbol: str, limit: int = 100) -> Dict:
        """
        获取 MEXC 订单簿
        
        Args:
            symbol: 交易对（如 'IRONUSDT'）
            limit: 深度档位（5, 10, 20, 50, 100, 500, 1000）
        
        Returns:
            同 get_gateio_orderbook
        """
        url = "https://api.mexc.com/api/v3/depth"
        params = {
            "symbol": symbol.replace('-', ''),
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'bids': [[float(price), float(amount)] for price, amount in data['bids']],
                'asks': [[float(price), float(amount)] for price, amount in data['asks']],
                'timestamp': data.get('lastUpdateId', int(time.time() * 1000))
            }
        except Exception as e:
            print(f"❌ MEXC 获取失败: {e}")
            return None
    
    @staticmethod
    def calculate_buy_slippage(asks: List[List[float]], trade_size_usd: float) -> Dict:
        """
        计算买入订单的精确滑点
        
        Args:
            asks: 卖单列表 [[price, amount], ...]
            trade_size_usd: 交易规模（USD）
        
        Returns:
            {
                'avg_price': 平均成交价,
                'best_price': 最佳价格,
                'slippage_pct': 滑点百分比,
                'filled': 是否完全成交
            }
        """
        if not asks or trade_size_usd <= 0:
            return None
        
        best_price = asks[0][0]
        remaining_usd = trade_size_usd
        total_base = 0.0
        total_cost = 0.0
        
        for price, size in asks:
            if remaining_usd <= 0:
                break
            
            available_value = price * size
            
            if available_value <= remaining_usd:
                total_base += size
                total_cost += available_value
                remaining_usd -= available_value
            else:
                partial_base = remaining_usd / price
                total_base += partial_base
                total_cost += remaining_usd
                remaining_usd = 0
        
        filled = (remaining_usd <= 0)
        avg_price = total_cost / total_base if total_base > 0 else best_price
        slippage_pct = ((avg_price - best_price) / best_price) * 100
        
        return {
            'avg_price': avg_price,
            'best_price': best_price,
            'slippage_pct': slippage_pct,
            'filled': filled,
            'total_base': total_base,
            'total_cost': total_cost
        }


def main():
    """示例：获取并分析 IRON-USDT 的订单簿"""
    import argparse
    
    parser = argparse.ArgumentParser(description="实时获取交易所订单簿")
    parser.add_argument('--pair', type=str, default='IRON-USDT', help='交易对（如 IRON-USDT）')
    parser.add_argument('--exchange', type=str, default='gateio', choices=['gateio', 'mexc'],
                        help='交易所')
    parser.add_argument('--size', type=float, default=144, help='测试交易规模（USD）')
    parser.add_argument('--limit', type=int, default=100, help='订单簿深度')
    
    args = parser.parse_args()
    
    print(f"\n{'='*80}")
    print(f"📊 实时订单簿分析")
    print(f"{'='*80}\n")
    print(f"交易对: {args.pair}")
    print(f"交易所: {args.exchange.upper()}")
    print(f"测试规模: ${args.size:,.2f}")
    print(f"订单簿深度: {args.limit} 档\n")
    
    # 获取订单簿
    fetcher = OrderBookFetcher()
    
    if args.exchange == 'gateio':
        orderbook = fetcher.get_gateio_orderbook(args.pair, args.limit)
    else:
        orderbook = fetcher.get_mexc_orderbook(args.pair, args.limit)
    
    if not orderbook:
        print("❌ 获取订单簿失败")
        return 1
    
    # 显示最佳价格
    best_bid = orderbook['bids'][0][0] if orderbook['bids'] else 0
    best_ask = orderbook['asks'][0][0] if orderbook['asks'] else 0
    spread = ((best_ask - best_bid) / best_bid) * 100 if best_bid > 0 else 0
    
    print(f"{'─'*80}")
    print(f"📈 当前市场状态")
    print(f"{'─'*80}\n")
    print(f"最佳买价: ${best_bid:.6f}")
    print(f"最佳卖价: ${best_ask:.6f}")
    print(f"买卖价差: {spread:.4f}%")
    print(f"订单簿档位: Bids {len(orderbook['bids'])} 档, Asks {len(orderbook['asks'])} 档\n")
    
    # 计算滑点
    result = fetcher.calculate_buy_slippage(orderbook['asks'], args.size)
    
    if result:
        print(f"{'─'*80}")
        print(f"💰 买入 ${args.size:,.2f} 的滑点分析")
        print(f"{'─'*80}\n")
        print(f"平均成交价: ${result['avg_price']:.6f}")
        print(f"最佳价格: ${result['best_price']:.6f}")
        print(f"滑点: {result['slippage_pct']:.4f}%")
        print(f"完全成交: {'✅ 是' if result['filled'] else '❌ 否'}")
        print(f"买到数量: {result['total_base']:.4f} {args.pair.split('-')[0]}")
        print(f"总花费: ${result['total_cost']:.2f}\n")
        
        # 对比估算
        print(f"{'─'*80}")
        print(f"🔍 对比分析")
        print(f"{'─'*80}\n")
        print(f"实时精确滑点: {result['slippage_pct']:.4f}% ✅")
        print(f"基础方法估算: ~2-3% ⚠️  (需要验证)")
        print(f"\n💡 使用实时订单簿可以获得最精确的滑点！")
    
    print(f"\n{'='*80}\n")
    return 0


if __name__ == "__main__":
    exit(main())

