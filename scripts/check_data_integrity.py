#!/usr/bin/env python3
"""
数据完整性检查工具

检查 orderbook ticks 数据的完整性和健康状况
"""

import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

def check_parquet_health(base_dir: str = "app/data/raw/orderbook_ticks"):
    """
    检查所有 parquet 文件的健康状况
    
    检查项：
    1. 文件是否可读
    2. 数据行数
    3. 时间范围
    4. 文件大小
    5. 最后修改时间
    """
    print("=" * 80)
    print("📊 Orderbook Ticks 数据完整性检查")
    print("=" * 80)
    print()
    
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"❌ 目录不存在: {base_dir}")
        return
    
    # 按交易所分组统计
    stats = {
        'gate_io': {'valid': 0, 'corrupted': 0, 'total_rows': 0},
        'mexc': {'valid': 0, 'corrupted': 0, 'total_rows': 0}
    }
    
    corrupted_files = []
    
    # 遍历所有分区目录
    for partition_dir in sorted(base_path.iterdir()):
        if not partition_dir.is_dir():
            continue
        
        # 识别交易所
        exchange = 'gate_io' if partition_dir.name.startswith('gate_io') else 'mexc'
        
        print(f"\n📁 {partition_dir.name}")
        print("-" * 80)
        
        # 获取所有 parquet 文件
        parquet_files = sorted(partition_dir.glob("*.parquet"))
        
        if not parquet_files:
            print("   ⚠️  空目录 - 没有 parquet 文件")
            continue
        
        partition_valid = 0
        partition_corrupted = 0
        partition_rows = 0
        
        # 检查每个文件
        for pf in parquet_files:
            try:
                df = pd.read_parquet(pf)
                file_size = pf.stat().st_size / 1024  # KB
                mod_time = datetime.fromtimestamp(pf.stat().st_mtime)
                
                partition_valid += 1
                partition_rows += len(df)
                
                if len(parquet_files) <= 10 or pf == parquet_files[-1]:
                    # 只显示前几个和最后一个文件的详情
                    time_range = ""
                    if len(df) > 0:
                        min_ts = df['timestamp'].min()
                        max_ts = df['timestamp'].max()
                        time_range = f" | 时间: {min_ts.strftime('%H:%M:%S')} → {max_ts.strftime('%H:%M:%S')}"
                    
                    print(f"   ✅ {pf.name}: {len(df):>4} 行 | "
                          f"{file_size:>6.1f} KB | "
                          f"更新: {mod_time.strftime('%H:%M:%S')}"
                          f"{time_range}")
                
            except Exception as e:
                partition_corrupted += 1
                corrupted_files.append((pf, str(e)))
                print(f"   ❌ {pf.name}: 文件损坏 - {e}")
        
        # 显示分区汇总
        if len(parquet_files) > 10:
            print(f"   ... (共 {len(parquet_files)} 个文件，只显示最后一个)")
        
        print(f"\n   📊 分区汇总:")
        print(f"      文件总数: {len(parquet_files)}")
        print(f"      正常文件: {partition_valid} ✅")
        print(f"      损坏文件: {partition_corrupted} ❌")
        print(f"      总数据行: {partition_rows:,} 条")
        
        # 更新统计
        stats[exchange]['valid'] += partition_valid
        stats[exchange]['corrupted'] += partition_corrupted
        stats[exchange]['total_rows'] += partition_rows
    
    # 总体统计
    print("\n" + "=" * 80)
    print("📈 总体统计")
    print("=" * 80)
    
    for exchange, data in stats.items():
        if data['valid'] > 0 or data['corrupted'] > 0:
            print(f"\n{exchange.upper()}:")
            print(f"  正常文件: {data['valid']:>5} ✅")
            print(f"  损坏文件: {data['corrupted']:>5} ❌")
            print(f"  总数据行: {data['total_rows']:>10,} 条")
    
    # 损坏文件处理建议
    if corrupted_files:
        print("\n" + "=" * 80)
        print("⚠️  损坏文件处理建议")
        print("=" * 80)
        print("\n以下文件已损坏，建议删除：\n")
        for file, error in corrupted_files:
            print(f"rm '{file}'")
        print("\n删除后，其他文件仍然完全正常可用。")
    else:
        print("\n✅ 所有文件状态良好！")
    
    print("\n" + "=" * 80)

def check_data_freshness(base_dir: str = "app/data/raw/orderbook_ticks", 
                         max_age_minutes: int = 5):
    """
    检查数据新鲜度（是否仍在更新）
    """
    print("\n" + "=" * 80)
    print("🔄 数据新鲜度检查")
    print("=" * 80)
    print()
    
    base_path = Path(base_dir)
    now = datetime.now()
    
    for partition_dir in sorted(base_path.iterdir()):
        if not partition_dir.is_dir():
            continue
        
        parquet_files = list(partition_dir.glob("*.parquet"))
        if not parquet_files:
            continue
        
        # 找到最新的文件
        latest_file = max(parquet_files, key=lambda p: p.stat().st_mtime)
        mod_time = datetime.fromtimestamp(latest_file.stat().st_mtime)
        age = now - mod_time
        age_seconds = age.total_seconds()
        
        status = "✅" if age_seconds < max_age_minutes * 60 else "⚠️"
        
        print(f"{status} {partition_dir.name}:")
        print(f"   最新文件: {latest_file.name}")
        print(f"   更新时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   距今: {int(age_seconds)}秒 ({age_seconds/60:.1f}分钟)")
        
        if age_seconds >= max_age_minutes * 60:
            print(f"   ⚠️  数据可能已停止更新（超过 {max_age_minutes} 分钟）")
        
        print()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="检查 orderbook ticks 数据完整性")
    parser.add_argument("--dir", default="app/data/raw/orderbook_ticks",
                       help="数据目录路径")
    parser.add_argument("--max-age", type=int, default=5,
                       help="数据新鲜度阈值（分钟）")
    parser.add_argument("--no-freshness", action="store_true",
                       help="跳过新鲜度检查")
    
    args = parser.parse_args()
    
    try:
        check_parquet_health(args.dir)
        
        if not args.no_freshness:
            check_data_freshness(args.dir, args.max_age)
            
    except KeyboardInterrupt:
        print("\n\n⏸️  检查已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 检查失败: {e}")
        sys.exit(1)

