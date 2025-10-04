#!/usr/bin/env python3
"""
OKX文档爬虫测试脚本
用于验证爬虫基本功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def test_basic_crawler():
    """测试基础爬虫"""
    print("🧪 测试基础爬虫...")
    
    try:
        from scripts.okx_docs_crawler import OKXDocsCrawler, CrawlConfig
        
        config = CrawlConfig(
            output_dir="data/test_okx_basic",
            max_concurrent=1,
            delay_range=(1, 2)
        )
        
        async with OKXDocsCrawler(config) as crawler:
            # 只测试首页
            html = await crawler.fetch_page(config.start_url)
            if html:
                content = crawler.extract_content(html, config.start_url)
                print(f"✅ 基础爬虫测试成功")
                print(f"   标题: {content['title']}")
                print(f"   内容长度: {len(content['text'])} 字符")
                return True
            else:
                print("❌ 基础爬虫测试失败：无法获取页面内容")
                return False
                
    except Exception as e:
        print(f"❌ 基础爬虫测试失败：{e}")
        return False

async def test_advanced_crawler():
    """测试增强爬虫"""
    print("🧪 测试增强爬虫...")
    
    try:
        from scripts.okx_docs_crawler_advanced import AdvancedOKXDocsCrawler, AdvancedCrawlConfig
        
        config = AdvancedCrawlConfig(
            output_dir="data/test_okx_advanced",
            max_concurrent=1,
            delay_range=(1, 2),
            use_selenium=False,  # 先测试不使用Selenium
            headless=True
        )
        
        async with AdvancedOKXDocsCrawler(config) as crawler:
            # 只测试首页
            html = await crawler.fetch_page(config.start_url)
            if html:
                content = crawler.extract_content(html, config.start_url)
                print(f"✅ 增强爬虫测试成功（无Selenium）")
                print(f"   标题: {content['title']}")
                print(f"   内容长度: {len(content['text'])} 字符")
                return True
            else:
                print("❌ 增强爬虫测试失败：无法获取页面内容")
                return False
                
    except Exception as e:
        print(f"❌ 增强爬虫测试失败：{e}")
        return False

async def test_selenium_crawler():
    """测试Selenium功能"""
    print("🧪 测试Selenium功能...")
    
    try:
        from scripts.okx_docs_crawler_advanced import AdvancedOKXDocsCrawler, AdvancedCrawlConfig
        
        config = AdvancedCrawlConfig(
            output_dir="data/test_okx_selenium",
            max_concurrent=1,
            delay_range=(1, 2),
            use_selenium=True,
            headless=True
        )
        
        async with AdvancedOKXDocsCrawler(config) as crawler:
            if not crawler.driver_pool:
                print("⚠️  Selenium测试跳过：无法创建Chrome驱动")
                print("   请确保已安装Chrome浏览器和ChromeDriver")
                return None
                
            # 测试Selenium获取页面
            html = await crawler.fetch_with_selenium(config.start_url)
            if html:
                content = crawler.extract_content(html, config.start_url)
                print(f"✅ Selenium测试成功")
                print(f"   标题: {content['title']}")
                print(f"   内容长度: {len(content['text'])} 字符")
                return True
            else:
                print("❌ Selenium测试失败：无法获取页面内容")
                return False
                
    except Exception as e:
        print(f"❌ Selenium测试失败：{e}")
        return False

def check_dependencies():
    """检查依赖包"""
    print("🔍 检查依赖包...")
    
    required_packages = [
        'aiohttp',
        'aiofiles', 
        'bs4',  # beautifulsoup4的导入名是bs4
        'lxml'
    ]
    
    optional_packages = [
        'selenium',
        'fake_useragent'
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"❌ {package} (必需)")
            
    for package in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            missing_optional.append(package)
            print(f"⚠️  {package} (可选)")
    
    if missing_required:
        print(f"\n❌ 缺少必需依赖: {', '.join(missing_required)}")
        print("请运行: pip install " + " ".join(missing_required))
        return False
        
    if missing_optional:
        print(f"\n⚠️  缺少可选依赖: {', '.join(missing_optional)}")
        print("建议运行: pip install " + " ".join(missing_optional))
        
    return True

async def main():
    """主测试函数"""
    print("🚀 OKX文档爬虫测试开始\n")
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装必需的依赖包")
        return
        
    print("\n" + "="*50)
    
    # 测试基础爬虫
    basic_result = await test_basic_crawler()
    
    print("\n" + "="*50)
    
    # 测试增强爬虫
    advanced_result = await test_advanced_crawler()
    
    print("\n" + "="*50)
    
    # 测试Selenium
    selenium_result = await test_selenium_crawler()
    
    print("\n" + "="*50)
    print("📊 测试结果汇总:")
    print(f"   基础爬虫: {'✅ 通过' if basic_result else '❌ 失败'}")
    print(f"   增强爬虫: {'✅ 通过' if advanced_result else '❌ 失败'}")
    if selenium_result is not None:
        print(f"   Selenium: {'✅ 通过' if selenium_result else '❌ 失败'}")
    else:
        print(f"   Selenium: ⚠️  跳过")
        
    if basic_result or advanced_result:
        print("\n🎉 爬虫基本功能正常，可以开始使用！")
        print("\n使用方法:")
        print("  python scripts/run_okx_crawler.py --mode basic")
        print("  python scripts/run_okx_crawler.py --mode advanced")
    else:
        print("\n❌ 爬虫测试失败，请检查网络连接和依赖安装")

if __name__ == "__main__":
    asyncio.run(main()) 