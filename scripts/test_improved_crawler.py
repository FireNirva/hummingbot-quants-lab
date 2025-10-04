#!/usr/bin/env python3
"""
测试改进的OKX文档爬虫
"""

import asyncio
import sys
from pathlib import Path
from okx_docs_crawler_improved import ImprovedOKXDocsCrawler, ImprovedCrawlConfig

async def test_single_page():
    """测试单个页面的爬取"""
    print("🧪 测试改进的OKX文档爬虫...")
    
    # 配置测试
    config = ImprovedCrawlConfig(
        start_url="https://web3.okx.com/zh-hans/build/dev-docs/",
        output_dir="data/okx_docs_test",
        max_concurrent=1,
        delay_range=(3, 5),
        use_selenium=True,
        headless=True,
        page_load_timeout=30
    )
    
    try:
        async with ImprovedOKXDocsCrawler(config) as crawler:
            print(f"📄 测试爬取单个页面: {config.start_url}")
            
            # 爬取单个页面
            new_links = await crawler.crawl_url(config.start_url)
            
            print(f"✅ 成功爬取页面")
            print(f"📊 发现新链接: {len(new_links)} 个")
            print(f"💾 输出目录: {config.output_dir}")
            
            # 检查输出文件
            output_path = Path(config.output_dir)
            if output_path.exists():
                files = list(output_path.rglob("*.md"))
                print(f"📁 生成的文件: {len(files)} 个")
                
                for file in files[:3]:  # 显示前3个文件
                    print(f"   - {file}")
                    
                # 显示第一个文件的内容预览
                if files:
                    first_file = files[0]
                    content = first_file.read_text(encoding='utf-8')
                    print(f"\n📖 文件内容预览 ({first_file.name}):")
                    print("=" * 50)
                    print(content[:500] + "..." if len(content) > 500 else content)
                    print("=" * 50)
            
            print(f"\n🎉 测试完成!")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

async def test_content_extraction():
    """测试内容提取功能"""
    print("\n🔍 测试内容提取功能...")
    
    config = ImprovedCrawlConfig()
    crawler = ImprovedOKXDocsCrawler(config)
    
    # 测试HTML内容
    test_html = """
    <html>
    <head><title>什么是 DEX API | 概览 | 首页 | DEX API | DEX API 文档 | 欧易</title></head>
    <body>
        <div class="routes_content__fnVIZ">
            <div class="routes_md__xWlGF">
                <h1>什么是 DEX API</h1>
                <h2>介绍</h2>
                <p>欢迎来到 OKX DEX 开发者文档。</p>
                <p>OKX DEX 是一站式多链跨链聚合交易平台。</p>
            </div>
        </div>
        <div class="index_table-of-content__dpmyB">
            <a href="/link1">概览</a>
            <a href="/link2">开始</a>
        </div>
    </body>
    </html>
    """
    
    content = crawler.extract_content_from_react(test_html, "https://test.com")
    
    print(f"📝 提取的标题: {content['title']}")
    print(f"📊 字数统计: {content['word_count']}")
    print(f"🔗 导航链接: {len(content['navigation']['sidebar_links'])}")
    print(f"📄 文本内容预览: {content['text'][:100]}...")
    
    if content['word_count'] > 0:
        print("✅ 内容提取测试通过")
        return True
    else:
        print("❌ 内容提取测试失败")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始测试改进的OKX文档爬虫")
    
    # 检查依赖
    try:
        from selenium import webdriver
        from fake_useragent import UserAgent
        print("✅ 依赖检查通过")
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install selenium fake-useragent")
        return False
    
    # 运行测试
    tests = [
        ("内容提取功能", test_content_extraction),
        ("单页面爬取", test_single_page),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 运行测试: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试 {test_name} 出错: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print(f"\n{'='*50}")
    print("📊 测试结果汇总")
    print(f"{'='*50}")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{len(results)} 个测试通过")
    
    if passed == len(results):
        print("🎉 所有测试通过! 爬虫已准备就绪")
        print("\n使用方法:")
        print("python okx_docs_crawler_improved.py")
    else:
        print("⚠️  部分测试失败，请检查配置")
    
    return passed == len(results)

if __name__ == "__main__":
    asyncio.run(main()) 