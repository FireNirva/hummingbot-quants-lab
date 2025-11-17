#!/usr/bin/env python3
"""
订单簿数据清理脚本

用途：
- 自动清理超过指定天数的订单簿数据
- 释放磁盘空间
- 支持干运行模式（预览但不删除）

使用方法：
    # 干运行（预览要删除的文件）
    python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run
    
    # 实际删除
    python scripts/cleanup_old_orderbook_data.py --days 7
    
    # 设置为定时任务（每天凌晨2点清理超过7天的数据）
    0 2 * * * cd /path/to/quants-lab && python scripts/cleanup_old_orderbook_data.py --days 7 >> logs/cleanup.log 2>&1
"""

import argparse
import logging
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.data_paths import data_paths

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_date_from_filename(filename: str) -> datetime:
    """从文件名解析日期
    
    文件名格式: gate_io_IRON_USDT_20241112.parquet
    """
    try:
        # 提取日期部分（最后一个下划线后，.parquet 前）
        date_str = filename.split('_')[-1].replace('.parquet', '')
        return datetime.strptime(date_str, '%Y%m%d').replace(tzinfo=timezone.utc)
    except Exception as e:
        logger.warning(f"无法解析文件名日期: {filename}, 错误: {e}")
        return None


def get_disk_usage(path: Path) -> dict:
    """获取磁盘使用情况"""
    total, used, free = shutil.disk_usage(path)
    return {
        'total_gb': total / (2**30),
        'used_gb': used / (2**30),
        'free_gb': free / (2**30),
        'used_percent': (used / total) * 100
    }


def cleanup_old_files(days_to_keep: int, dry_run: bool = True) -> dict:
    """清理旧文件
    
    Args:
        days_to_keep: 保留最近N天的数据
        dry_run: 如果为True，只预览不删除
        
    Returns:
        清理统计信息
    """
    orderbook_dir = data_paths.raw_dir / "orderbook_snapshots"
    
    if not orderbook_dir.exists():
        logger.error(f"订单簿数据目录不存在: {orderbook_dir}")
        return {'error': 'directory_not_found'}
    
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_to_keep)
    
    logger.info(f"{'[干运行] ' if dry_run else ''}开始清理订单簿数据...")
    logger.info(f"保留策略: 保留最近 {days_to_keep} 天的数据")
    logger.info(f"删除日期: {cutoff_date.strftime('%Y-%m-%d')} 之前")
    logger.info(f"数据目录: {orderbook_dir}")
    
    # 统计信息
    stats = {
        'total_files': 0,
        'old_files': 0,
        'deleted_files': 0,
        'skipped_files': 0,
        'total_size_mb': 0,
        'freed_space_mb': 0,
        'errors': 0,
        'deleted_file_list': [],
        'error_file_list': []
    }
    
    # 遍历所有 parquet 文件
    for file_path in orderbook_dir.glob("*.parquet"):
        stats['total_files'] += 1
        
        # 解析日期
        file_date = parse_date_from_filename(file_path.name)
        
        if file_date is None:
            stats['skipped_files'] += 1
            stats['error_file_list'].append((file_path.name, 'failed_to_parse_date'))
            continue
        
        # 获取文件大小
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        stats['total_size_mb'] += file_size_mb
        
        # 检查是否需要删除
        if file_date < cutoff_date:
            stats['old_files'] += 1
            
            if dry_run:
                logger.info(f"[将删除] {file_path.name} ({file_size_mb:.2f} MB, {file_date.strftime('%Y-%m-%d')})")
                stats['freed_space_mb'] += file_size_mb
                stats['deleted_file_list'].append((file_path.name, file_size_mb, file_date))
            else:
                try:
                    file_path.unlink()
                    logger.info(f"[已删除] {file_path.name} ({file_size_mb:.2f} MB)")
                    stats['deleted_files'] += 1
                    stats['freed_space_mb'] += file_size_mb
                    stats['deleted_file_list'].append((file_path.name, file_size_mb, file_date))
                except Exception as e:
                    logger.error(f"删除失败: {file_path.name}, 错误: {e}")
                    stats['errors'] += 1
                    stats['error_file_list'].append((file_path.name, str(e)))
    
    return stats


def print_summary(stats: dict, disk_before: dict, disk_after: dict = None, dry_run: bool = True):
    """打印清理摘要"""
    print("\n" + "=" * 80)
    print(f"🗑️  订单簿数据清理{'预览' if dry_run else ''}报告 - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print("=" * 80)
    
    # 文件统计
    print(f"\n📊 文件统计:")
    print(f"   • 总文件数: {stats['total_files']}")
    print(f"   • 旧文件数: {stats['old_files']}")
    
    if dry_run:
        print(f"   • 将删除: {stats['old_files']} 个文件")
    else:
        print(f"   • ✅ 已删除: {stats['deleted_files']} 个文件")
        if stats['errors'] > 0:
            print(f"   • ❌ 删除失败: {stats['errors']} 个文件")
    
    if stats['skipped_files'] > 0:
        print(f"   • ⚠️  跳过: {stats['skipped_files']} 个文件（无法解析日期）")
    
    # 空间统计
    print(f"\n💾 空间统计:")
    print(f"   • 数据目录总大小: {stats['total_size_mb']:.2f} MB ({stats['total_size_mb']/1024:.2f} GB)")
    print(f"   • {'将释放' if dry_run else '已释放'}空间: {stats['freed_space_mb']:.2f} MB ({stats['freed_space_mb']/1024:.2f} GB)")
    
    if stats['old_files'] > 0:
        print(f"   • 平均文件大小: {stats['freed_space_mb']/stats['old_files']:.2f} MB")
    
    # 磁盘使用情况
    print(f"\n💿 磁盘使用情况:")
    print(f"   清理前:")
    print(f"      • 总空间: {disk_before['total_gb']:.1f} GB")
    print(f"      • 已使用: {disk_before['used_gb']:.1f} GB ({disk_before['used_percent']:.1f}%)")
    print(f"      • 可用: {disk_before['free_gb']:.1f} GB")
    
    if disk_after:
        print(f"   清理后:")
        print(f"      • 可用: {disk_after['free_gb']:.1f} GB")
        print(f"      • 释放: {disk_after['free_gb'] - disk_before['free_gb']:.2f} GB")
    else:
        print(f"   预计清理后:")
        print(f"      • 可用: {disk_before['free_gb'] + stats['freed_space_mb']/1024:.1f} GB")
    
    # 详细列表（仅显示前10个）
    if stats['deleted_file_list']:
        print(f"\n{'🔍 将删除的文件' if dry_run else '✅ 已删除的文件'} (前10个):")
        for i, (filename, size_mb, file_date) in enumerate(stats['deleted_file_list'][:10], 1):
            print(f"   {i:2d}. {filename:50s} {size_mb:8.2f} MB  {file_date.strftime('%Y-%m-%d')}")
        
        if len(stats['deleted_file_list']) > 10:
            print(f"   ... 还有 {len(stats['deleted_file_list']) - 10} 个文件")
    
    # 错误列表
    if stats['error_file_list']:
        print(f"\n❌ 错误列表:")
        for filename, error in stats['error_file_list']:
            print(f"   • {filename}: {error}")
    
    # 建议
    if dry_run and stats['old_files'] > 0:
        print(f"\n💡 建议:")
        print(f"   确认无误后，运行以下命令执行实际删除:")
        print(f"   python scripts/cleanup_old_orderbook_data.py --days {args.days}")
    elif not dry_run and stats['deleted_files'] > 0:
        print(f"\n✅ 清理完成！")
        print(f"   释放了 {stats['freed_space_mb']/1024:.2f} GB 磁盘空间")
    elif stats['old_files'] == 0:
        print(f"\n✅ 无需清理")
        print(f"   所有文件都在保留期内")
    
    print("\n" + "=" * 80 + "\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='清理旧的订单簿数据文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 预览要删除的文件（不实际删除）
    python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run
    
    # 删除超过7天的数据
    python scripts/cleanup_old_orderbook_data.py --days 7
    
    # 删除超过14天的数据
    python scripts/cleanup_old_orderbook_data.py --days 14
    
    # 查看帮助
    python scripts/cleanup_old_orderbook_data.py --help
        """
    )
    
    parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='保留最近N天的数据（默认: 7）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='干运行模式：预览要删除的文件但不实际删除'
    )
    
    global args
    args = parser.parse_args()
    
    # 获取清理前的磁盘使用情况
    orderbook_dir = data_paths.raw_dir / "orderbook_snapshots"
    disk_before = get_disk_usage(orderbook_dir)
    
    # 执行清理
    stats = cleanup_old_files(days_to_keep=args.days, dry_run=args.dry_run)
    
    if 'error' in stats:
        logger.error(f"清理失败: {stats['error']}")
        sys.exit(1)
    
    # 获取清理后的磁盘使用情况
    disk_after = None if args.dry_run else get_disk_usage(orderbook_dir)
    
    # 打印摘要
    print_summary(stats, disk_before, disk_after, dry_run=args.dry_run)
    
    # 返回状态码
    if stats['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

