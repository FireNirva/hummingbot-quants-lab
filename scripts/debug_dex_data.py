#!/usr/bin/env python3
"""
调试脚本：检查 GeckoTerminal 上的原始数据

用于诊断为什么下载的 DEX 数据覆盖率低。
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from geckoterminal_py import GeckoTerminalAsyncClient
from core.data_paths import data_paths


async def check_pool_data(network: str, pool_address: str, trading_pair: str):
    """
    检查单个池子的数据情况。
    
    Args:
        network: 网络名称（如 "base"）
        pool_address: 池子地址
        trading_pair: 交易对名称（用于显示）
    """
    print("\n" + "="*80)
    print(f"🔍 调试池子: {trading_pair}")
    print(f"   地址: {pool_address}")
    print("="*80)
    
    client = GeckoTerminalAsyncClient()
    
    # 测试不同的时间范围
    end_time = datetime.now(timezone.utc)
    
    # 测试 1: 最近 1000 个数据点（API 上限）
    print("\n📊 测试 1: 获取最近 1000 个 1m 数据点")
    print("-"*80)
    
    try:
        response = await client.api_request(
            'GET',
            f'/networks/{network}/pools/{pool_address}/ohlcv/minute',
            params={
                'aggregate': 1,
                'limit': 1000,
                'currency': 'usd'
            }
        )
        
        ohlcv_list = response.get('data', {}).get('attributes', {}).get('ohlcv_list', [])
        
        if ohlcv_list:
            print(f"✅ 成功获取 {len(ohlcv_list)} 个数据点")
            
            # 分析时间范围
            timestamps = [item[0] for item in ohlcv_list]
            df = pd.DataFrame(ohlcv_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
            
            print(f"   时间范围: {df['datetime'].min()} 至 {df['datetime'].max()}")
            print(f"   时间跨度: {(df['datetime'].max() - df['datetime'].min()).total_seconds() / 3600:.2f} 小时")
            print(f"   平均间隔: {df['timestamp'].diff().mean():.1f} 秒")
            
            # 检查数据密度
            expected_points = (df['datetime'].max() - df['datetime'].min()).total_seconds() / 60
            actual_points = len(ohlcv_list)
            density = (actual_points / expected_points * 100) if expected_points > 0 else 0
            
            print(f"   数据密度: {density:.1f}% ({actual_points}/{expected_points:.0f})")
            
            # 显示最新几个数据点
            print(f"\n   最新 5 个数据点:")
            for _, row in df.tail(5).iterrows():
                print(f"     {row['datetime']}: close=${row['close']:.6f}, vol={row['volume']:.2f}")
            
            # 分析间隙
            gaps = df['timestamp'].diff()
            large_gaps = gaps[gaps > 300]  # 大于 5 分钟的间隙
            
            if len(large_gaps) > 0:
                print(f"\n   ⚠️  发现 {len(large_gaps)} 个大间隙（>5分钟）:")
                for idx in large_gaps.index[:5]:
                    gap_seconds = gaps.loc[idx]
                    gap_time = df.loc[idx, 'datetime']
                    print(f"     {gap_time}: 间隔 {gap_seconds/60:.1f} 分钟")
            else:
                print(f"\n   ✅ 数据连续，无大间隙")
                
        else:
            print("❌ 未获取到数据")
            
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试 2: 尝试获取更早的数据（使用 before_timestamp）
    print("\n📊 测试 2: 尝试获取更早的历史数据")
    print("-"*80)
    
    if ohlcv_list:
        earliest_ts = timestamps[0]
        before_time = datetime.fromtimestamp(earliest_ts, tz=timezone.utc)
        
        print(f"   从 {before_time} 之前继续获取...")
        
        try:
            response2 = await client.api_request(
                'GET',
                f'/networks/{network}/pools/{pool_address}/ohlcv/minute',
                params={
                    'aggregate': 1,
                    'limit': 1000,
                    'before_timestamp': earliest_ts,
                    'currency': 'usd'
                }
            )
            
            ohlcv_list2 = response2.get('data', {}).get('attributes', {}).get('ohlcv_list', [])
            
            if ohlcv_list2:
                print(f"✅ 又获取了 {len(ohlcv_list2)} 个数据点")
                
                df2 = pd.DataFrame(ohlcv_list2, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df2['datetime'] = pd.to_datetime(df2['timestamp'], unit='s', utc=True)
                
                print(f"   时间范围: {df2['datetime'].min()} 至 {df2['datetime'].max()}")
                print(f"   时间跨度: {(df2['datetime'].max() - df2['datetime'].min()).total_seconds() / 3600:.2f} 小时")
                
                # 计算总覆盖
                all_timestamps = timestamps + [item[0] for item in ohlcv_list2]
                all_df = pd.DataFrame({
                    'timestamp': all_timestamps,
                    'datetime': pd.to_datetime(all_timestamps, unit='s', utc=True)
                }).drop_duplicates().sort_values('timestamp')
                
                total_span = (all_df['datetime'].max() - all_df['datetime'].min()).total_seconds() / 3600
                print(f"\n   总覆盖时间: {total_span:.2f} 小时 ({len(all_df)} 个数据点)")
                
            else:
                print("⚠️  没有更早的数据了")
                
        except Exception as e:
            print(f"❌ API 请求失败: {e}")
    
    await client.close()
    
    # 测试 3: 检查与 CEX 的时间对比
    print("\n📊 测试 3: 与 CEX 数据对比")
    print("-"*80)
    
    # 使用传入的 trading_pair
    cex_file = data_paths.candles_dir / f"gate_io|{trading_pair}|1m.parquet"
    
    if cex_file.exists():
        cex_df = pd.read_parquet(cex_file)
        print(f"✅ 找到 CEX 数据: {trading_pair}")
        print(f"   CEX 时间范围: {cex_df.index.min()} 至 {cex_df.index.max()}")
        print(f"   CEX K线数: {len(cex_df):,}")
        print(f"   CEX 时间跨度: {(cex_df.index.max() - cex_df.index.min()).total_seconds() / 3600:.2f} 小时")
        
        if ohlcv_list:
            # 计算 DEX 数据应该覆盖的时间范围
            dex_start = df['datetime'].min()
            dex_end = df['datetime'].max()
            
            cex_in_range = cex_df[(cex_df.index >= dex_start) & (cex_df.index <= dex_end)]
            
            coverage = len(ohlcv_list) / len(cex_in_range) * 100 if len(cex_in_range) > 0 else 0
            
            print(f"\n   DEX 覆盖率（相同时间段）:")
            print(f"     CEX 在此时间段的K线数: {len(cex_in_range):,}")
            print(f"     DEX 数据点数: {len(ohlcv_list):,}")
            print(f"     覆盖率: {coverage:.1f}%")
    else:
        print(f"⚠️  未找到 CEX 数据: {cex_file.name}")


async def main():
    """主函数。"""
    print("="*80)
    print("🔍 GeckoTerminal DEX 数据调试工具")
    print("="*80)
    
    # 加载池子映射
    mapping_file = data_paths.processed_dir / 'pool_mappings' / 'base_gate_io_pool_map.parquet'
    
    if not mapping_file.exists():
        print(f"\n❌ 池子映射文件不存在: {mapping_file}")
        return 1
    
    df = pd.read_parquet(mapping_file)
    top_pools = df[df['rank'] == 1].sort_values('trading_pair')
    
    print(f"\n找到 {len(top_pools)} 个 rank=1 的池子:")
    for i, (_, pool) in enumerate(top_pools.iterrows(), 1):
        print(f"  {i}. {pool['trading_pair']} (DEX: {pool['dex_id']})")
    print()
    
    # 依次检查每个池子
    for _, pool in top_pools.iterrows():
        await check_pool_data(
            network='base',
            pool_address=pool['pool_address'],
            trading_pair=pool['trading_pair']
        )
        
        # 等待一下，避免触发 API 限制
        await asyncio.sleep(1.5)
    
    print("\n" + "="*80)
    print("✅ 调试完成")
    print("="*80)
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

