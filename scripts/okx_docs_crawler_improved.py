#!/usr/bin/env python3
"""
OKX DEX API 文档爬虫 - 改进版
专门针对React SPA应用优化
"""

import asyncio
import aiohttp
import aiofiles
import time
import random
import json
import os
import re
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Set, List, Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from fake_useragent import UserAgent

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ImprovedCrawlConfig:
    """改进的爬虫配置"""
    base_url: str = "https://web3.okx.com"
    start_url: str = "https://web3.okx.com/zh-hans/build/dev-docs/"
    output_dir: str = "data/okx_docs"
    max_concurrent: int = 1  # 降低并发，避免被检测
    delay_range: tuple = (5, 10)  # 增加延迟
    timeout: int = 60  # 增加超时时间
    max_retries: int = 3
    use_selenium: bool = True
    headless: bool = True
    page_load_timeout: int = 30  # 页面加载超时
    
    def __post_init__(self):
        self.ua = UserAgent()

class ImprovedOKXDocsCrawler:
    """改进的OKX文档爬虫"""
    
    def __init__(self, config: ImprovedCrawlConfig = None):
        self.config = config or ImprovedCrawlConfig()
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self.driver: Optional[webdriver.Chrome] = None
        
        # 创建输出目录
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        
    def create_driver(self) -> webdriver.Chrome:
        """创建优化的Chrome驱动"""
        options = Options()
        
        if self.config.headless:
            options.add_argument('--headless')
            
        # 反检测配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # 随机User-Agent
        user_agent = self.config.ua.random
        options.add_argument(f'--user-agent={user_agent}')
        
        # 窗口大小
        options.add_argument('--window-size=1920,1080')
        
        # 性能优化
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')
        options.add_argument('--disable-javascript-harmony-shipping')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-renderer-backgrounding')
        
        # 内存优化
        options.add_argument('--memory-pressure-off')
        options.add_argument('--max_old_space_size=4096')
        
        try:
            driver = webdriver.Chrome(options=options)
            driver.set_page_load_timeout(self.config.page_load_timeout)
            
            # 执行反检测脚本
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']})")
            
            return driver
        except Exception as e:
            logger.error(f"创建Chrome驱动失败: {e}")
            raise
            
    async def __aenter__(self):
        """异步上下文管理器入口"""
        # 创建HTTP会话
        connector = aiohttp.TCPConnector(
            limit=10,
            limit_per_host=2,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        
        # 创建Selenium驱动
        if self.config.use_selenium:
            try:
                self.driver = self.create_driver()
                logger.info("Selenium驱动创建成功")
            except Exception as e:
                logger.warning(f"创建Selenium驱动失败: {e}")
                self.config.use_selenium = False
                
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logger.warning(f"关闭驱动失败: {e}")
                
    async def fetch_with_selenium(self, url: str) -> Optional[str]:
        """使用Selenium获取页面内容，专门优化React SPA"""
        if not self.driver:
            return None
            
        try:
            logger.info(f"使用Selenium获取: {url}")
            
            # 访问页面
            self.driver.get(url)
            
            # 等待React应用加载完成
            await self.wait_for_react_content()
            
            # 额外等待确保内容完全渲染
            await asyncio.sleep(random.uniform(3, 6))
            
            # 模拟用户行为
            await self.simulate_user_interaction()
            
            # 获取页面源码
            html = self.driver.page_source
            logger.info(f"Selenium成功获取: {url}, 内容长度: {len(html)}")
            return html
            
        except Exception as e:
            logger.error(f"Selenium获取失败: {url}, 错误: {e}")
            return None
            
    async def wait_for_react_content(self):
        """等待React内容加载完成"""
        try:
            # 等待主要内容容器出现
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "routes_content__fnVIZ"))
            )
            
            # 等待文档内容出现
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "routes_md__xWlGF"))
            )
            
            # 等待标题出现
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            
            logger.info("React内容加载完成")
            
        except TimeoutException:
            logger.warning("等待React内容超时，继续处理")
        except Exception as e:
            logger.warning(f"等待React内容时出错: {e}")
            
    async def simulate_user_interaction(self):
        """模拟用户交互"""
        try:
            # 滚动页面
            scroll_count = random.randint(2, 4)
            for i in range(scroll_count):
                scroll_y = random.randint(200, 800)
                self.driver.execute_script(f"window.scrollBy(0, {scroll_y});")
                await asyncio.sleep(random.uniform(0.5, 1.0))
                
            # 滚动到顶部
            self.driver.execute_script("window.scrollTo(0, 0);")
            await asyncio.sleep(1)
            
        except Exception as e:
            logger.debug(f"模拟用户交互失败: {e}")
            
    def extract_content_from_react(self, html: str, url: str) -> Dict[str, str]:
        """从React渲染的HTML中提取内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
            
        # 提取标题
        title = self.extract_title_from_react(soup)
        
        # 提取主要内容 - 针对OKX文档结构优化
        main_content = self.extract_main_content_from_react(soup)
        
        # 提取导航信息
        nav_info = self.extract_navigation_info(soup)
        
        # 提取文本内容
        text_content = main_content.get_text(separator='\n', strip=True) if main_content else ""
        
        # 清理文本内容
        text_content = self.clean_extracted_text(text_content)
        
        # 提取HTML内容
        html_content = str(main_content) if main_content else ""
        
        return {
            'title': title,
            'text': text_content,
            'html': html_content,
            'url': url,
            'navigation': nav_info,
            'word_count': len(text_content.split()),
            'extract_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def extract_title_from_react(self, soup: BeautifulSoup) -> str:
        """从React页面提取标题"""
        # 尝试多种方式获取标题
        title_selectors = [
            'title',
            '.routes_md__xWlGF h1',
            'h1',
            '.doc-content h1',
            '[class*="title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True)
                if title and len(title) > 3:  # 确保标题有意义
                    return title
                    
        return "未知标题"
        
    def extract_main_content_from_react(self, soup: BeautifulSoup):
        """从React页面提取主要内容"""
        # OKX文档的特定选择器
        content_selectors = [
            '.routes_md__xWlGF',  # 主要文档内容
            '.doc-content',
            '.routes_content__fnVIZ',
            'main',
            '.content',
            'article'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                # 检查内容是否有意义
                text = element.get_text(strip=True)
                if len(text) > 100:  # 确保有足够的内容
                    logger.info(f"使用选择器 {selector} 提取到 {len(text)} 字符的内容")
                    return element
                    
        # 如果没有找到合适的内容，返回body
        body = soup.find('body')
        if body:
            logger.warning("使用body作为内容容器")
            return body
            
        return soup
        
    def extract_navigation_info(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """提取导航信息"""
        nav_info = {
            'breadcrumbs': [],
            'sidebar_links': [],
            'toc': []
        }
        
        # 提取面包屑导航
        breadcrumb_selectors = [
            '.okui-breadcrumbs a',
            '.breadcrumb a',
            '[class*="breadcrumb"] a'
        ]
        
        for selector in breadcrumb_selectors:
            links = soup.select(selector)
            if links:
                nav_info['breadcrumbs'] = [link.get_text(strip=True) for link in links]
                break
                
        # 提取侧边栏链接
        sidebar_selectors = [
            '.index_table-of-content__dpmyB a',
            '.sidebar a',
            '[class*="sidebar"] a',
            '[class*="menu"] a'
        ]
        
        for selector in sidebar_selectors:
            links = soup.select(selector)
            if links:
                nav_info['sidebar_links'] = [link.get_text(strip=True) for link in links[:20]]  # 限制数量
                break
                
        # 提取目录
        toc_selectors = [
            '.index_list__VzJHJ a',
            '.toc a',
            '[class*="toc"] a'
        ]
        
        for selector in toc_selectors:
            links = soup.select(selector)
            if links:
                nav_info['toc'] = [link.get_text(strip=True) for link in links]
                break
                
        return nav_info
        
    def clean_extracted_text(self, text: str) -> str:
        """清理提取的文本"""
        # 移除多余的空白字符
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # 移除常见的无用内容
        patterns_to_remove = [
            r'Cookie.*?设置',
            r'隐私.*?政策',
            r'用户.*?协议',
            r'版权.*?所有',
            r'Copyright.*?\d{4}',
            r'登录.*?注册',
            r'下载.*?App'
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
        return text.strip()
        
    def extract_links_from_react(self, html: str, base_url: str) -> Set[str]:
        """从React页面提取链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        # 查找所有链接
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if self.is_docs_url(full_url):
                links.add(full_url)
                
        # 特别查找文档相关的链接
        doc_link_selectors = [
            '.index_table-of-content__dpmyB a[href]',
            '.routes_content__fnVIZ a[href]',
            '.index_card__PinRP[href]',
            '[class*="nav"] a[href]',
            '[class*="menu"] a[href]'
        ]
        
        for selector in doc_link_selectors:
            for link in soup.select(selector):
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    if self.is_docs_url(full_url):
                        links.add(full_url)
                        
        logger.info(f"从 {base_url} 提取到 {len(links)} 个有效链接")
        return links
        
    def is_docs_url(self, url: str) -> bool:
        """判断是否为文档相关URL"""
        parsed = urlparse(url)
        
        # 必须是同域名
        if parsed.netloc != 'web3.okx.com':
            return False
            
        # 必须是文档路径
        if not parsed.path.startswith('/zh-hans/build/dev-docs'):
            return False
            
        # 排除不需要的文件类型和路径
        excluded_patterns = [
            '.pdf', '.zip', '.tar', '.gz', '.jpg', '.png', '.gif', '.css', '.js',
            '/api/', '/auth/', '/login', '/register', '/logout', '#'
        ]
        
        path_lower = parsed.path.lower()
        if any(pattern in path_lower for pattern in excluded_patterns):
            return False
            
        return True
        
    async def save_improved_content(self, content: Dict[str, str], url: str):
        """保存改进的内容格式"""
        # 生成文件名
        parsed = urlparse(url)
        path_parts = [part for part in parsed.path.split('/') if part]
        
        if not path_parts or path_parts[-1] == '':
            filename = 'index'
        else:
            filename = path_parts[-1]
            
        # 清理文件名
        filename = re.sub(r'[^\w\-_.]', '_', filename)
        if not filename.endswith('.md'):
            filename += '.md'
            
        # 创建子目录结构
        if len(path_parts) > 3:  # 跳过 'zh-hans', 'build', 'dev-docs'
            subdir_parts = path_parts[3:-1]
            subdir = Path(self.config.output_dir) / '/'.join(subdir_parts)
        else:
            subdir = Path(self.config.output_dir)
            
        subdir.mkdir(parents=True, exist_ok=True)
        filepath = subdir / filename
        
        # 准备增强的markdown内容
        nav_section = ""
        if content['navigation']['breadcrumbs']:
            nav_section += f"\n## 导航路径\n{' > '.join(content['navigation']['breadcrumbs'])}\n"
            
        if content['navigation']['toc']:
            nav_section += f"\n## 目录\n" + '\n'.join(f"- {item}" for item in content['navigation']['toc']) + "\n"
            
        markdown_content = f"""# {content['title']}

**URL:** {content['url']}  
**抓取时间:** {content['extract_time']}  
**字数:** {content['word_count']}
{nav_section}
---

{content['text']}

---

<details>
<summary>原始HTML内容</summary>

```html
{content['html']}
```

</details>

<details>
<summary>导航信息</summary>

```json
{json.dumps(content['navigation'], ensure_ascii=False, indent=2)}
```

</details>
"""
        
        # 保存markdown文件
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(markdown_content)
            
        logger.info(f"已保存: {filepath} ({content['word_count']} 字)")
        
        # 保存JSON格式的元数据
        json_filepath = filepath.with_suffix('.json')
        async with aiofiles.open(json_filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(content, ensure_ascii=False, indent=2))
            
    async def crawl_url(self, url: str) -> Set[str]:
        """爬取单个URL"""
        async with self.semaphore:
            if url in self.visited_urls:
                return set()
                
            self.visited_urls.add(url)
            
            # 随机延迟
            await asyncio.sleep(random.uniform(*self.config.delay_range))
            
            html = None
            if self.config.use_selenium:
                html = await self.fetch_with_selenium(url)
            
            if not html:
                self.failed_urls.add(url)
                return set()
                
            # 提取内容
            content = self.extract_content_from_react(html, url)
            
            # 只保存有实际内容的页面
            if content['word_count'] > 50:  # 至少50个词
                await self.save_improved_content(content, url)
            else:
                logger.info(f"跳过内容过少的页面: {url} ({content['word_count']} 字)")
                
            # 提取新链接
            new_links = self.extract_links_from_react(html, url)
            return new_links - self.visited_urls
            
    async def crawl(self):
        """开始爬取"""
        logger.info(f"开始爬取OKX文档: {self.config.start_url}")
        logger.info(f"使用Selenium: {self.config.use_selenium}")
        logger.info(f"输出目录: {self.config.output_dir}")
        
        # 待处理的URL队列
        urls_to_crawl = {self.config.start_url}
        
        while urls_to_crawl:
            # 逐个处理URL（降低并发避免被检测）
            current_url = urls_to_crawl.pop()
            
            try:
                new_links = await self.crawl_url(current_url)
                urls_to_crawl.update(new_links)
                
                logger.info(f"已处理: {len(self.visited_urls)}, 待处理: {len(urls_to_crawl)}, 失败: {len(self.failed_urls)}")
                
            except Exception as e:
                logger.error(f"处理URL失败: {current_url}, 错误: {e}")
                self.failed_urls.add(current_url)
                
        # 保存爬取统计
        await self.save_crawl_stats()
        
        logger.info(f"爬取完成! 总计: {len(self.visited_urls)} 页面, 失败: {len(self.failed_urls)} 页面")
        logger.info(f"结果保存在: {self.config.output_dir}")
        
    async def save_crawl_stats(self):
        """保存爬取统计信息"""
        stats = {
            'total_crawled': len(self.visited_urls),
            'total_failed': len(self.failed_urls),
            'success_rate': (len(self.visited_urls) / (len(self.visited_urls) + len(self.failed_urls))) * 100 if (len(self.visited_urls) + len(self.failed_urls)) > 0 else 0,
            'failed_urls': list(self.failed_urls),
            'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'visited_urls': list(self.visited_urls),
            'config': {
                'use_selenium': self.config.use_selenium,
                'max_concurrent': self.config.max_concurrent,
                'delay_range': self.config.delay_range,
                'page_load_timeout': self.config.page_load_timeout
            }
        }
        
        stats_file = Path(self.config.output_dir) / 'crawl_stats.json'
        async with aiofiles.open(stats_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(stats, ensure_ascii=False, indent=2))
            
        # 创建详细报告
        report = f"""# OKX文档爬取报告 - 改进版

## 统计信息
- 成功爬取: {stats['total_crawled']} 页面
- 失败: {stats['total_failed']} 页面  
- 成功率: {stats['success_rate']:.1f}%
- 爬取时间: {stats['crawl_time']}

## 配置信息
- 使用Selenium: {stats['config']['use_selenium']}
- 最大并发: {stats['config']['max_concurrent']}
- 延迟范围: {stats['config']['delay_range']}秒
- 页面加载超时: {stats['config']['page_load_timeout']}秒

## 成功爬取的页面
{chr(10).join(f"- {url}" for url in stats['visited_urls'])}

## 失败的URL
{chr(10).join(f"- {url}" for url in stats['failed_urls'])}

## 使用说明
1. 每个页面都保存为.md和.json两种格式
2. .md文件包含格式化的文档内容
3. .json文件包含结构化的元数据
4. 导航信息和目录结构都被保留
"""
        
        report_file = Path(self.config.output_dir) / 'crawl_report.md'
        async with aiofiles.open(report_file, 'w', encoding='utf-8') as f:
            await f.write(report)

async def main():
    """主函数"""
    config = ImprovedCrawlConfig(
        max_concurrent=1,  # 单线程处理
        delay_range=(8, 15),  # 更长的延迟
        use_selenium=True,
        headless=True,
        page_load_timeout=30
    )
    
    async with ImprovedOKXDocsCrawler(config) as crawler:
        await crawler.crawl()

if __name__ == "__main__":
    asyncio.run(main()) 