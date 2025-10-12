#!/usr/bin/env python3
"""
CEX交易对到DEX池子映射构建脚本

使用GeckoTerminal API为CEX交易对查找对应的DEX高流动性池子。

示例用法:
    # 自动检测gate_io的所有交易对
    python scripts/build_pool_mapping.py --network base --connector gate_io
    
    # 指定特定交易对
    python scripts/build_pool_mapping.py --network base --pairs AERO-USDT,BRETT-USDT
    
    # 保留top 5池子
    python scripts/build_pool_mapping.py --network base --top-n 5
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

# 添加项目根目录到sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.services.pool_mapping import PoolMappingService
from core.data_paths import data_paths

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='构建CEX交易对到DEX池子的映射',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动检测gate_io的所有交易对
  %(prog)s --network base --connector gate_io
  
  # 指定特定交易对
  %(prog)s --network base --pairs AERO-USDT,BRETT-USDT,VIRTUAL-USDT
  
  # 保留每个交易对的top 5池子
  %(prog)s --network base --connector gate_io --top-n 5
  
  # 自定义输出目录
  %(prog)s --network base --output-dir /custom/path
        """
    )
    
    parser.add_argument(
        '--network',
        type=str,
        default='base',
        help='网络ID（默认: base）'
    )
    
    parser.add_argument(
        '--connector',
        type=str,
        default='gate_io',
        help='CEX连接器名称（默认: gate_io）'
    )
    
    parser.add_argument(
        '--candles-dir',
        type=Path,
        default=None,
        help=f'Candles目录路径（默认: {data_paths.candles_dir}）'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help=f'输出目录路径（默认: {data_paths.processed_dir}）'
    )
    
    parser.add_argument(
        '--top-n',
        type=int,
        default=3,
        help='每个交易对保留的池子数量（默认: 3）'
    )
    
    parser.add_argument(
        '--pairs',
        type=str,
        default=None,
        help='逗号分隔的交易对列表（可选，覆盖自动检测）。例如: AERO-USDT,BRETT-USDT'
    )
    
    return parser.parse_args()


async def main():
    """主函数"""
    args = parse_args()
    
    print("="*80)
    print("🗺️  CEX-DEX池子映射构建工具")
    print("="*80)
    print()
    
    # 显示配置
    print("📋 配置信息:")
    print(f"  - 网络: {args.network}")
    print(f"  - 连接器: {args.connector}")
    print(f"  - Top N: {args.top_n}")
    
    # 确定candles目录
    candles_dir = args.candles_dir if args.candles_dir else data_paths.candles_dir
    print(f"  - Candles目录: {candles_dir}")
    print()
    
    # 初始化服务
    service = PoolMappingService()
    
    try:
        # 1. 获取交易对列表
        if args.pairs:
            # 从命令行参数解析
            pairs = [p.strip() for p in args.pairs.split(',')]
            print(f"📝 使用指定的交易对: {len(pairs)} 个")
            for pair in pairs:
                print(f"   - {pair}")
        else:
            # 自动检测
            print(f"🔍 从 {candles_dir} 自动检测交易对...")
            pairs = service.parse_trading_pairs_from_candles(candles_dir, args.connector)
            
            if not pairs:
                print(f"❌ 错误: 未找到 {args.connector} 的交易对")
                print(f"   请检查目录: {candles_dir}")
                return 1
            
            print(f"✓ 检测到 {len(pairs)} 个交易对:")
            for pair in pairs[:10]:  # 只显示前10个
                print(f"   - {pair}")
            if len(pairs) > 10:
                print(f"   ... 和其他 {len(pairs) - 10} 个交易对")
        
        print()
        
        # 2. 构建映射
        print(f"🔄 开始构建池子映射（这可能需要一些时间）...")
        print(f"   预计耗时: ~{len(pairs) * 0.5:.0f}秒 ({len(pairs)}个交易对 × 0.5秒/个)")
        print()
        
        df, raw_responses = await service.build_mapping(
            pairs, 
            args.network, 
            args.connector, 
            args.top_n
        )
        
        # 3. 保存结果
        print()
        print("💾 保存结果...")
        
        # 保存原始响应
        service.save_raw_responses(raw_responses, args.network)
        
        # 保存映射数据
        output_file = service.save_mapping(df, args.network, args.connector)
        
        # 4. 统计信息
        print()
        print("="*80)
        print("📊 统计摘要")
        print("="*80)
        
        pools_found = len(df)
        pairs_with_pools = df['trading_pair'].nunique() if not df.empty else 0
        pairs_failed = len(pairs) - pairs_with_pools
        
        print(f"  ✓ 处理交易对: {len(pairs)} 个")
        print(f"  ✓ 成功映射: {pairs_with_pools} 个")
        print(f"  ✗ 失败/无结果: {pairs_failed} 个")
        print(f"  ✓ 找到池子: {pools_found} 个")
        print()
        
        # 显示失败的交易对
        if pairs_failed > 0:
            failed_pairs = set(pairs) - set(df['trading_pair'].unique() if not df.empty else [])
            print("⚠️  未找到池子的交易对:")
            for pair in sorted(failed_pairs):
                error_info = raw_responses.get(pair, {})
                if 'error' in error_info:
                    print(f"   - {pair} (错误: {error_info['error']})")
                else:
                    print(f"   - {pair} (无搜索结果)")
            print()
        
        # 显示输出文件位置
        print("📁 输出文件:")
        print(f"  - 原始JSON: {data_paths.raw_dir / 'geckoterminal' / 'search_pools' / args.network}/")
        print(f"  - 映射数据: {output_file}")
        print()
        
        # 显示top池子示例
        if not df.empty:
            print("🏊 示例池子（按流动性排序）:")
            print()
            
            # 获取前3个有池子的交易对
            sample_pairs = df.groupby('trading_pair')['reserve_usd'].max().nlargest(3).index
            
            for pair in sample_pairs:
                pair_data = df[df['trading_pair'] == pair].sort_values('rank')
                top_pool = pair_data.iloc[0]
                
                print(f"  {pair}:")
                print(f"    地址: {top_pool['pool_address'][:10]}...")
                print(f"    DEX: {top_pool['dex_id']}")
                print(f"    流动性: ${top_pool['reserve_usd']:,.0f}")
                print(f"    24h交易量: ${top_pool['volume_usd_h24']:,.0f}")
                print()
        
        print("="*80)
        print("✅ 完成！")
        print("="*80)
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print("⚠️  用户中断")
        return 130
    except Exception as e:
        print()
        print(f"❌ 错误: {e}")
        logger.exception("Error during mapping")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

