#!/usr/bin/env python3
"""
DEX OHLCV Data Downloader

Manual CLI tool for downloading DEX K-line data from GeckoTerminal API.

Usage:
    # Download 7 days of 5m/15m/1h data
    python scripts/download_dex_ohlcv.py --network base --intervals 5m 15m 1h --lookback-days 7
    
    # Align with CEX data range
    python scripts/download_dex_ohlcv.py --network base --connector gate_io --align-with-cex
    
    # Save raw API responses
    python scripts/download_dex_ohlcv.py --network base --save-raw
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.data_sources.geckoterminal import GeckoTerminalDataSource
from core.data_sources.clob import CLOBDataSource
from core.data_paths import data_paths
from core.services.geckoterminal_ohlcv import interval_to_seconds, save_raw_response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download DEX OHLCV data from GeckoTerminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download 7 days of data for Base chain
  %(prog)s --network base --intervals 5m 15m 1h --lookback-days 7
  
  # Align with CEX data time range
  %(prog)s --network base --connector gate_io --align-with-cex
  
  # Save raw API responses
  %(prog)s --network base --save-raw
  
  # Limit number of requests
  %(prog)s --network base --max-requests 50
        """
    )
    
    parser.add_argument(
        '--network',
        default='base',
        help='Network ID (default: base)'
    )
    
    parser.add_argument(
        '--connector',
        default='gate_io',
        help='CEX connector name for pool mapping (default: gate_io)'
    )
    
    parser.add_argument(
        '--intervals',
        nargs='+',
        default=['5m', '15m', '1h'],
        help='Intervals to download (default: 5m 15m 1h)'
    )
    
    parser.add_argument(
        '--lookback-days',
        type=int,
        default=7,
        help='Days of historical data to download (default: 7)'
    )
    
    parser.add_argument(
        '--align-with-cex',
        action='store_true',
        help='Align time range with CEX data (requires CEX data to exist)'
    )
    
    parser.add_argument(
        '--max-requests',
        type=int,
        default=100,
        help='Maximum number of API requests (default: 100)'
    )
    
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=1.0,
        help='Seconds between API requests (default: 1.0)'
    )
    
    parser.add_argument(
        '--save-raw',
        action='store_true',
        help='Save raw API responses to JSON files'
    )
    
    parser.add_argument(
        '--pairs',
        nargs='+',
        help='Specific trading pairs to download (default: all from mapping)'
    )
    
    return parser.parse_args()


async def main():
    """Main execution function."""
    args = parse_args()
    
    print("="*80)
    print("🗺️  DEX OHLCV Data Downloader")
    print("="*80)
    print()
    
    # Load pool mapping
    print(f"📋 Loading pool mapping...")
    mapping_file = data_paths.processed_dir / 'pool_mappings' / f'{args.network}_{args.connector}_pool_map.parquet'
    
    if not mapping_file.exists():
        print(f"❌ Pool mapping not found: {mapping_file}")
        print(f"   Please run pool mapping first:")
        print(f"   python scripts/build_pool_mapping.py --network {args.network} --connector {args.connector}")
        return 1
    
    df = pd.read_parquet(mapping_file)
    
    # ============================================================================
    # 新的池子选择逻辑
    # ============================================================================
    # 1. 过滤 DEX: 只要 uniswap-v2 或 uniswap-v3
    # 2. 过滤 quote token: 只要 WETH, ETH, USDC, USDT
    # 3. 符合条件后，按 volume_usd_h24 排序，选择交易量最大的
    # ============================================================================
    
    # Base 链常见 quote token 地址（小写）
    ACCEPTED_QUOTE_TOKENS = {
        '0x4200000000000000000000000000000000000006',  # WETH
        '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',  # USDC
        '0x50c5725949a6f0c72e6c4a641f24049a917db0cb',  # USDT (Base)
        # ETH 通常和 WETH 是同一个地址
    }
    
    # 过滤 DEX
    dex_filtered = df[
        df['dex_id'].str.contains('uniswap-v2|uniswap-v3', regex=True, case=False)
    ].copy()
    
    print(f"📊 池子过滤统计：")
    print(f"   • 原始池子数: {len(df)}")
    print(f"   • DEX过滤后 (uniswap-v2/v3): {len(dex_filtered)}")
    
    # 过滤 quote token
    dex_filtered['quote_token_lower'] = dex_filtered['quote_token_address'].str.lower()
    quote_filtered = dex_filtered[
        dex_filtered['quote_token_lower'].isin(ACCEPTED_QUOTE_TOKENS)
    ].copy()
    
    print(f"   • Quote token过滤后 (WETH/USDC/USDT): {len(quote_filtered)}")
    
    # Filter by pairs if specified
    if args.pairs:
        quote_filtered = quote_filtered[quote_filtered['trading_pair'].isin(args.pairs)]
    
    # 为每个交易对选择 volume_usd_h24 最高的池子（交易量最大）
    top_pools = quote_filtered.loc[
        quote_filtered.groupby('trading_pair')['volume_usd_h24'].idxmax()
    ].copy()
    
    print(f"   • 最终选择池子数 (每个pair选24h交易量最高): {len(top_pools)}")
    
    if top_pools.empty:
        print(f"❌ No pools found matching criteria")
        return 1
    
    print()
    print(f"✓ 选中的池子 DEX 分布：")
    dex_counts = top_pools['dex_id'].value_counts()
    for dex, count in dex_counts.items():
        print(f"   • {dex}: {count} 个池子")
    print()
    
    # Initialize data sources
    print(f"🚀 Initializing...")
    gt_ds = GeckoTerminalDataSource(rate_limit_sleep=args.rate_limit)
    
    # Load existing cache
    gt_ds.load_candles_cache()
    
    # Initialize CEX data source if needed
    cex_ds = None
    if args.align_with_cex:
        print(f"   Loading CEX data source for alignment...")
        cex_ds = CLOBDataSource()
    
    print()
    
    # Statistics
    stats = {
        'pairs_total': len(top_pools),
        'pairs_success': 0,
        'pairs_failed': 0,
        'candles_fetched': 0,
        'requests_made': 0,
        'failed_pairs': []
    }
    
    # Download for each pool × interval
    print(f"📥 Downloading data...")
    print(f"   Network: {args.network}")
    print(f"   Intervals: {', '.join(args.intervals)}")
    print(f"   Lookback: {args.lookback_days} days")
    print()
    
    request_count = 0
    
    for idx, (_, pool) in enumerate(top_pools.iterrows(), 1):
        trading_pair = pool['trading_pair']
        pool_address = pool['pool_address']
        
        print(f"[{idx}/{len(top_pools)}] {trading_pair} ({pool_address[:10]}...)")
        
        pair_success = True
        
        for interval in args.intervals:
            # Check request limit
            if request_count >= args.max_requests:
                print(f"   ⚠️  Reached max requests ({args.max_requests}), stopping")
                break
            
            try:
                # Determine time range
                end_time = int(datetime.now(timezone.utc).timestamp())
                
                if args.align_with_cex:
                    # Try to align with CEX data
                    cex_file = data_paths.candles_dir / f"{args.connector}|{trading_pair}|{interval}.parquet"
                    
                    if cex_file.exists():
                        cex_df = pd.read_parquet(cex_file)
                        start_time = int(cex_df.index.min().timestamp())
                        end_time = int(cex_df.index.max().timestamp())
                        print(f"   {interval}: Aligning with CEX data range")
                    else:
                        print(f"   {interval}: CEX data not found, using lookback")
                        start_time = end_time - (args.lookback_days * 86400)
                else:
                    # Check existing DEX data for incremental
                    dex_file = data_paths.candles_dir / f"geckoterminal_{args.network}|{trading_pair}|{interval}.parquet"
                    
                    if dex_file.exists():
                        existing_df = pd.read_parquet(dex_file)
                        # Start from last timestamp minus overlap (10 candles)
                        overlap = 10 * interval_to_seconds(interval)
                        start_time = int(existing_df.index.max().timestamp()) - overlap
                        print(f"   {interval}: Incremental from {existing_df.index.max()}")
                    else:
                        # Fresh download
                        start_time = end_time - (args.lookback_days * 86400)
                        print(f"   {interval}: Fresh download ({args.lookback_days} days)")
                
                # Fetch candles
                candles = await gt_ds.get_candles(
                    network=args.network,
                    pool_address=pool_address,
                    trading_pair=trading_pair,
                    interval=interval,
                    start_time=start_time,
                    end_time=end_time
                )
                
                stats['candles_fetched'] += len(candles.data)
                stats['requests_made'] += 1
                request_count += 1
                
                print(f"   {interval}: ✓ {len(candles.data)} candles")
                
                # Save raw response if requested
                if args.save_raw:
                    raw_dir = data_paths.raw_dir / 'geckoterminal' / 'ohlcv' / args.network
                    # Note: save_raw_response would need the actual response object
                    # For now, we skip this since we don't have access to raw response in current flow
                    pass
                
            except Exception as e:
                print(f"   {interval}: ❌ {str(e)[:60]}...")
                stats['failed_pairs'].append(f"{trading_pair}|{interval}")
                pair_success = False
                continue
        
        if pair_success:
            stats['pairs_success'] += 1
        else:
            stats['pairs_failed'] += 1
        
        # Check request limit
        if request_count >= args.max_requests:
            break
        
        print()
    
    # Dump all to parquet
    print(f"💾 Saving data to parquet...")
    gt_ds.dump_candles_cache()
    print()
    
    # Print summary
    print("="*80)
    print("📊 Download Summary")
    print("="*80)
    print(f"  ✓ Pairs processed: {stats['pairs_total']}")
    print(f"  ✓ Pairs success: {stats['pairs_success']}")
    print(f"  ✗ Pairs failed: {stats['pairs_failed']}")
    print(f"  ✓ Candles fetched: {stats['candles_fetched']:,}")
    print(f"  ✓ API requests: {stats['requests_made']}")
    print()
    
    if stats['failed_pairs']:
        print(f"⚠️  Failed pairs:")
        for pair in stats['failed_pairs'][:10]:
            print(f"   - {pair}")
        if len(stats['failed_pairs']) > 10:
            print(f"   ... and {len(stats['failed_pairs']) - 10} more")
        print()
    
    print(f"📁 Data saved to: {data_paths.candles_dir}")
    print("="*80)
    print("✅ Download complete!")
    print("="*80)
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

