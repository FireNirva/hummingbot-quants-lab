#!/usr/bin/env python3
"""
自动下载 Crypto Lake 订单簿数据

用于套利分析的精确滑点计算

使用前需要：
1. 订阅 Crypto Lake: https://crypto-lake.com/pricing
2. 安装 lakeapi: pip install lakeapi
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import yaml


def download_orderbook_data(
    symbols: list,
    exchange: str = 'MEXC',
    table: str = 'deep_book_1m',
    days: int = 7,
    output_dir: str = 'data/crypto_lake'
):
    """
    下载订单簿数据
    
    Args:
        symbols: 交易对列表，如 ['BTC-USDT', 'ETH-USDT']
        exchange: 交易所名称（MEXC, BINANCE, GATEIO 等）
        table: 数据类型（deep_book_1m, book_1m, trades）
        days: 下载天数
        output_dir: 输出目录
    """
    try:
        import lakeapi
    except ImportError:
        print("❌ 未安装 lakeapi，请运行：pip install lakeapi")
        return False
    
    print(f"\n{'='*80}")
    print(f"📥 Crypto Lake 数据下载")
    print(f"{'='*80}\n")
    print(f"交易所: {exchange}")
    print(f"数据类型: {table}")
    print(f"交易对数量: {len(symbols)}")
    print(f"天数: {days}")
    print(f"\n开始下载...\n")
    
    # 设置时间范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    success_count = 0
    total_size_mb = 0
    
    for i, symbol in enumerate(symbols, 1):
        print(f"[{i}/{len(symbols)}] 📦 {symbol}")
        
        try:
            # 下载数据
            df = lakeapi.load_data(
                table=table,
                start=start_date,
                end=end_date,
                symbols=[symbol],
                exchanges=[exchange.upper()]
            )
            
            if df.empty:
                print(f"  ⚠️  无数据")
                continue
            
            # 保存文件
            output_path = Path(output_dir) / exchange / symbol / f'{table}.parquet'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(output_path)
            
            # 统计
            file_size_mb = output_path.stat().st_size / 1024 / 1024
            total_size_mb += file_size_mb
            snapshots = len(df)
            
            print(f"  ✅ {snapshots:,} 个快照，{file_size_mb:.1f} MB")
            print(f"  📁 {output_path}")
            
            success_count += 1
            
        except Exception as e:
            print(f"  ❌ 失败: {e}")
    
    print(f"\n{'='*80}")
    print(f"✅ 下载完成")
    print(f"{'='*80}\n")
    print(f"成功: {success_count}/{len(symbols)} 个交易对")
    print(f"总大小: {total_size_mb:.1f} MB")
    print(f"\n💡 下一步：运行滑点计算器")
    print(f"python scripts/calculate_slippage_from_orderbook.py \\")
    print(f"  --file {output_dir}/{exchange}/{symbols[0]}/{table}.parquet \\")
    print(f"  --recommend\n")
    
    return success_count > 0


def load_symbols_from_config(config_file: str) -> list:
    """从配置文件加载交易对列表"""
    config_path = Path(config_file)
    
    if not config_path.exists():
        print(f"❌ 配置文件不存在: {config_file}")
        return []
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # 获取交易对列表
    trading_pairs = config.get('tasks', [{}])[0].get('config', {}).get('trading_pairs', [])
    
    # 转换格式：IRON-USDT → IRON-USDT (已经是正确格式)
    return trading_pairs


def main():
    parser = argparse.ArgumentParser(
        description="下载 Crypto Lake 订单簿数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

1. 下载单个交易对（7 天深度订单簿）:
   python scripts/download_crypto_lake_data.py \\
     --symbols IRON-USDT \\
     --exchange MEXC \\
     --days 7

2. 从配置文件批量下载:
   python scripts/download_crypto_lake_data.py \\
     --config config/mexc_base_ecosystem_downloader.yml \\
     --exchange MEXC

3. 下载标准订单簿（数据量更小）:
   python scripts/download_crypto_lake_data.py \\
     --symbols IRON-USDT,AUKI-USDT \\
     --exchange MEXC \\
     --table book_1m \\
     --days 30

4. 下载交易数据（验证用）:
   python scripts/download_crypto_lake_data.py \\
     --symbols IRON-USDT \\
     --exchange MEXC \\
     --table trades \\
     --days 7

支持的交易所:
- MEXC
- GATEIO (Gate.io)
- BINANCE
- COINBASE
- OKX
- BYBIT
完整列表: https://crypto-lake.com/coverage

支持的数据类型:
- deep_book_1m: 深度订单簿（~1000 档）⭐推荐
- book_1m: 标准订单簿（20 档）
- trades: 交易数据
- candles: 1分钟蜡烛图

订阅链接: https://crypto-lake.com/pricing
        """
    )
    
    parser.add_argument('--symbols', type=str, 
                        help='交易对（逗号分隔），如 "BTC-USDT,ETH-USDT"')
    parser.add_argument('--config', type=str,
                        help='配置文件路径（自动读取交易对列表）')
    parser.add_argument('--exchange', type=str, default='MEXC',
                        help='交易所名称（默认: MEXC）')
    parser.add_argument('--table', type=str, default='deep_book_1m',
                        choices=['deep_book_1m', 'book_1m', 'trades', 'candles'],
                        help='数据类型（默认: deep_book_1m）')
    parser.add_argument('--days', type=int, default=7,
                        help='下载天数（默认: 7）')
    parser.add_argument('--output', type=str, default='data/crypto_lake',
                        help='输出目录（默认: data/crypto_lake）')
    
    args = parser.parse_args()
    
    # 获取交易对列表
    if args.config:
        symbols = load_symbols_from_config(args.config)
        if not symbols:
            return 1
    elif args.symbols:
        symbols = [s.strip() for s in args.symbols.split(',')]
    else:
        print("❌ 请指定 --symbols 或 --config")
        parser.print_help()
        return 1
    
    # 执行下载
    success = download_orderbook_data(
        symbols=symbols,
        exchange=args.exchange,
        table=args.table,
        days=args.days,
        output_dir=args.output
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

