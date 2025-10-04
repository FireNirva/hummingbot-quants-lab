#!/usr/bin/env python3
"""
OKX文档爬虫快速启动脚本
"""

import argparse
import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    parser = argparse.ArgumentParser(description='OKX DEX API 文档爬虫')
    parser.add_argument('--mode', choices=['basic', 'advanced'], default='advanced',
                       help='爬虫模式: basic(基础版) 或 advanced(增强版，默认)')
    parser.add_argument('--output', default='data/okx_docs',
                       help='输出目录 (默认: data/okx_docs)')
    parser.add_argument('--concurrent', type=int, default=2,
                       help='最大并发数 (默认: 2)')
    parser.add_argument('--delay-min', type=float, default=3.0,
                       help='最小延迟秒数 (默认: 3.0)')
    parser.add_argument('--delay-max', type=float, default=6.0,
                       help='最大延迟秒数 (默认: 6.0)')
    parser.add_argument('--no-selenium', action='store_true',
                       help='禁用Selenium (仅对增强版有效)')
    parser.add_argument('--no-headless', action='store_true',
                       help='显示浏览器窗口 (仅对增强版有效)')
    parser.add_argument('--proxy', type=str,
                       help='代理服务器 (格式: http://proxy:port)')
    parser.add_argument('--verbose', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    print(f"🚀 启动OKX文档爬虫 ({args.mode}模式)")
    print(f"📁 输出目录: {args.output}")
    print(f"⚡ 并发数: {args.concurrent}")
    print(f"⏱️  延迟范围: {args.delay_min}-{args.delay_max}秒")
    
    if args.mode == 'basic':
        from okx_docs_crawler import OKXDocsCrawler, CrawlConfig
        
        config = CrawlConfig(
            output_dir=args.output,
            max_concurrent=args.concurrent,
            delay_range=(args.delay_min, args.delay_max)
        )
        
        async def run_basic():
            async with OKXDocsCrawler(config) as crawler:
                await crawler.crawl()
                
        asyncio.run(run_basic())
        
    else:  # advanced mode
        from okx_docs_crawler_advanced import AdvancedOKXDocsCrawler, AdvancedCrawlConfig
        
        config = AdvancedCrawlConfig(
            output_dir=args.output,
            max_concurrent=args.concurrent,
            delay_range=(args.delay_min, args.delay_max),
            use_selenium=not args.no_selenium,
            headless=not args.no_headless,
            proxy=args.proxy
        )
        
        if args.verbose:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
            
        print(f"🔧 使用Selenium: {config.use_selenium}")
        if config.use_selenium:
            print(f"👁️  无头模式: {config.headless}")
        if config.proxy:
            print(f"🌐 代理: {config.proxy}")
            
        async def run_advanced():
            async with AdvancedOKXDocsCrawler(config) as crawler:
                await crawler.crawl()
                
        asyncio.run(run_advanced())
    
    print("✅ 爬取完成!")
    print(f"📄 查看结果: {args.output}/crawl_report.md")

if __name__ == "__main__":
    main() 