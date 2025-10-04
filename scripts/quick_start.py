#!/usr/bin/env python3
"""
OKX文档爬虫 - 快速开始
"""

import asyncio
import sys
from pathlib import Path
from okx_docs_crawler_improved import ImprovedOKXDocsCrawler, ImprovedCrawlConfig

async def quick_start():
    """快速开始爬取OKX文档"""
    print("🚀 OKX文档爬虫 - 快速开始")
    print("=" * 50)
    
    # 检查依赖
    try:
        from selenium import webdriver
        from fake_useragent import UserAgent
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install selenium fake-useragent")
        return False
    
    # 配置爬虫
    config = ImprovedCrawlConfig(
        start_url="https://web3.okx.com/zh-hans/build/dev-docs/",
        output_dir="data/okx_docs",
        max_concurrent=1,
        delay_range=(5, 8),
        use_selenium=True,
        headless=True,
        page_load_timeout=30
    )
    
    print(f"📁 输出目录: {config.output_dir}")
    print(f"🌐 开始URL: {config.start_url}")
    print(f"⏱️ 延迟范围: {config.delay_range}秒")
    print(f"🤖 使用Selenium: {config.use_selenium}")
    print()
    
    try:
        async with ImprovedOKXDocsCrawler(config) as crawler:
            print("🔄 开始爬取...")
            await crawler.crawl()
            
        print("🎉 爬取完成!")
        
        # 显示结果
        output_dir = Path(config.output_dir)
        if output_dir.exists():
            md_files = list(output_dir.rglob("*.md"))
            json_files = list(output_dir.rglob("*.json"))
            
            print(f"\n📊 爬取结果:")
            print(f"   - Markdown文件: {len(md_files)} 个")
            print(f"   - JSON文件: {len(json_files)} 个")
            print(f"   - 输出目录: {output_dir}")
            
            # 显示部分文件
            if md_files:
                print(f"\n📄 生成的文档 (前5个):")
                for i, file in enumerate(md_files[:5], 1):
                    size = file.stat().st_size
                    print(f"   {i}. {file.name} ({size} bytes)")
                    
                if len(md_files) > 5:
                    print(f"   ... 还有 {len(md_files) - 5} 个文件")
                    
            # 显示统计文件
            stats_file = output_dir / "crawl_stats.json"
            if stats_file.exists():
                print(f"\n📈 详细统计: {stats_file}")
                
            report_file = output_dir / "crawl_report.md"
            if report_file.exists():
                print(f"📋 详细报告: {report_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ 爬取失败: {e}")
        print("\n🛠️ 故障排除建议:")
        print("1. 检查网络连接")
        print("2. 确保Chrome浏览器已安装")
        print("3. 运行: python test_improved_crawler.py")
        return False

def main():
    """主函数"""
    print("欢迎使用OKX文档爬虫!")
    print("这个工具将帮助你爬取OKX DEX API的完整文档")
    print()
    
    # 询问用户是否继续
    response = input("是否开始爬取? (y/n): ").lower().strip()
    if response not in ['y', 'yes', '是', '']:
        print("已取消")
        return
    
    # 运行爬虫
    success = asyncio.run(quick_start())
    
    if success:
        print("\n🎯 下一步:")
        print("1. 查看生成的文档: data/okx_docs/")
        print("2. 阅读使用指南: README_使用指南.md")
        print("3. 监控进度: python monitor_crawl.py")
    else:
        print("\n❓ 需要帮助?")
        print("1. 查看使用指南: README_使用指南.md")
        print("2. 运行测试: python test_improved_crawler.py")

if __name__ == "__main__":
    main() 