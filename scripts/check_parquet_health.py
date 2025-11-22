"""
检查 Parquet 文件健康状态

快速扫描所有 Parquet 文件，找出损坏的文件
"""
import os
import sys
from pathlib import Path
import pyarrow.parquet as pq


def check_parquet_file(file_path: Path) -> tuple[bool, str]:
    """检查单个 parquet 文件"""
    try:
        table = pq.read_table(file_path)
        return True, f"{len(table):,} rows"
    except Exception as e:
        return False, str(e)[:100]


def scan_directory(directory: Path):
    """扫描目录下所有 parquet 文件"""
    print(f"🔍 Scanning: {directory}")
    print("="*80)
    
    parquet_files = list(directory.rglob("*.parquet"))
    
    if not parquet_files:
        print("No parquet files found")
        return
    
    print(f"Found {len(parquet_files)} parquet files\n")
    
    healthy = []
    corrupted = []
    
    for file_path in sorted(parquet_files):
        is_healthy, info = check_parquet_file(file_path)
        
        if is_healthy:
            healthy.append(file_path)
            print(f"✅ {file_path.name:<60} {info}")
        else:
            corrupted.append(file_path)
            print(f"❌ {file_path.name:<60} CORRUPTED")
            print(f"   Error: {info}")
    
    print("\n" + "="*80)
    print(f"📊 Summary:")
    print(f"   ✅ Healthy: {len(healthy)}")
    print(f"   ❌ Corrupted: {len(corrupted)}")
    
    if corrupted:
        print(f"\n⚠️  Corrupted files found!")
        print(f"   To fix, delete them and re-run data collection:")
        for file_path in corrupted:
            print(f"   rm {file_path}")


if __name__ == "__main__":
    # Check orderbook snapshots
    data_dir = Path(__file__).parent.parent / "app" / "data" / "raw"
    
    if len(sys.argv) > 1:
        # Custom directory
        data_dir = Path(sys.argv[1])
    
    if not data_dir.exists():
        print(f"❌ Directory not found: {data_dir}")
        sys.exit(1)
    
    scan_directory(data_dir)

