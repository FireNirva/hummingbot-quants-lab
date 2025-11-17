#!/usr/bin/env python3
"""
检查订单簿数据质量

使用方法：
    python scripts/check_orderbook_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from app.tasks.data_collection.orderbook_snapshot_task import (
    load_orderbook_snapshots,
    validate_update_ids
)
from core.data_paths import data_paths


def check_file_details():
    """检查所有订单簿数据文件的详细信息"""
    
    print("=" * 80)
    print("📊 订单簿数据文件检查报告")
    print("=" * 80)
    print()
    
    # 数据目录
    data_dir = data_paths.raw_dir / "orderbook_snapshots"
    
    if not data_dir.exists():
        print(f"❌ 数据目录不存在: {data_dir}")
        return
    
    # 列出所有文件
    files = sorted(data_dir.glob("*.parquet"))
    
    print(f"📁 数据目录: {data_dir}")
    print(f"📄 文件总数: {len(files)}")
    print()
    
    if not files:
        print("⚠️ 没有找到数据文件")
        return
    
    print("-" * 80)
    print()
    
    # 检查每个文件
    for file in files:
        print(f"📋 文件: {file.name}")
        print(f"   大小: {file.stat().st_size / 1024:.2f} KB")
        
        try:
            # 读取文件
            df = pd.read_parquet(file)
            
            print(f"   记录数: {len(df)} 条")
            print()
            
            # 显示列信息
            print("   📊 数据列:")
            for col in df.columns:
                dtype = df[col].dtype
                null_count = df[col].isna().sum()
                print(f"      • {col}: {dtype} (空值: {null_count})")
            print()
            
            # 显示第一条记录的详细信息
            if len(df) > 0:
                first_record = df.iloc[0]
                
                print("   📝 第一条记录:")
                print(f"      • Timestamp: {first_record['timestamp']}")
                print(f"      • Update ID: {first_record.get('update_id', 'N/A')}")
                print(f"      • Exchange: {first_record['exchange']}")
                print(f"      • Trading Pair: {first_record['trading_pair']}")
                print(f"      • Best Bid: {first_record.get('best_bid_price', 'N/A')}")
                print(f"      • Best Ask: {first_record.get('best_ask_price', 'N/A')}")
                
                # 检查订单簿深度
                if 'bid_prices' in df.columns:
                    bid_prices = first_record['bid_prices']
                    if isinstance(bid_prices, list):
                        print(f"      • Bid 档位数: {len(bid_prices)}")
                        print(f"      • Bid 价格范围: {min(bid_prices):.6f} - {max(bid_prices):.6f}")
                
                if 'ask_prices' in df.columns:
                    ask_prices = first_record['ask_prices']
                    if isinstance(ask_prices, list):
                        print(f"      • Ask 档位数: {len(ask_prices)}")
                        print(f"      • Ask 价格范围: {min(ask_prices):.6f} - {max(ask_prices):.6f}")
            
            print()
            
            # 验证 update_id
            if 'update_id' in df.columns:
                print("   🔍 Update ID 验证:")
                report = validate_update_ids(df)
                print(f"      • 质量评分: {report['quality_score']:.1f}/100")
                print(f"      • Null 值: {report.get('null_count', 0)}")
                print(f"      • 非递增: {len(report.get('non_increasing', []))}")
                print(f"      • 重复: {len(report.get('duplicates', []))}")
            
            print()
            print("-" * 80)
            print()
            
        except Exception as e:
            print(f"   ❌ 读取错误: {e}")
            print()
            print("-" * 80)
            print()


def check_data_by_exchange():
    """按交易所分组检查数据"""
    
    print("=" * 80)
    print("📊 按交易所汇总")
    print("=" * 80)
    print()
    
    # Gate.io 数据
    print("🏦 Gate.io 数据:")
    gate_pairs = ['VIRTUAL-USDT', 'LMTS-USDT', 'BNKR-USDT', 'PRO-USDT', 'IRON-USDT', 'MIGGLES-USDT']
    
    for pair in gate_pairs:
        try:
            df = load_orderbook_snapshots('gate_io', pair)
            if not df.empty:
                print(f"   ✅ {pair}: {len(df)} 条记录")
                if 'update_id' in df.columns:
                    print(f"      Update ID: {df['update_id'].min():.0f} - {df['update_id'].max():.0f}")
                if 'timestamp' in df.columns:
                    print(f"      时间范围: {df['timestamp'].min()} - {df['timestamp'].max()}")
            else:
                print(f"   ⚠️ {pair}: 无数据")
        except Exception as e:
            print(f"   ❌ {pair}: 错误 - {e}")
    
    print()
    
    # MEXC 数据
    print("🏦 MEXC 数据:")
    mexc_pairs = ['AUKI-USDT', 'SERV-USDT', 'IRON-USDT']
    
    for pair in mexc_pairs:
        try:
            df = load_orderbook_snapshots('mexc', pair)
            if not df.empty:
                print(f"   ✅ {pair}: {len(df)} 条记录")
                if 'update_id' in df.columns:
                    print(f"      Update ID: {df['update_id'].min():.0f} - {df['update_id'].max():.0f}")
                if 'timestamp' in df.columns:
                    print(f"      时间范围: {df['timestamp'].min()} - {df['timestamp'].max()}")
            else:
                print(f"   ⚠️ {pair}: 无数据")
        except Exception as e:
            print(f"   ❌ {pair}: 错误 - {e}")
    
    print()
    print("=" * 80)


def main():
    """主函数"""
    print()
    print("🔍 开始检查订单簿数据...")
    print()
    
    # 检查文件详情
    check_file_details()
    
    # 按交易所汇总
    check_data_by_exchange()
    
    print()
    print("=" * 80)
    print("✅ 检查完成")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()

