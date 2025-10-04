#!/usr/bin/env python3
"""
OKX DEX API 文档爬虫 - 增强版
支持JavaScript渲染和更强的反爬虫能力
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
class AdvancedCrawlConfig:
    """高级爬虫配置"""
    base_url: str = "https://web3.okx.com"
    start_url: str = "https://web3.okx.com/zh-hans/build/dev-docs/"
    output_dir: str = "data/okx_docs"
    max_concurrent: int = 3  # 降低并发数，避免被检测
    delay_range: tuple = (2, 5)  # 增加延迟
    timeout: int = 30
    max_retries: int = 3
    use_selenium: bool = True  # 是否使用Selenium处理JavaScript
    headless: bool = True  # 是否无头模式
    
    # 代理配置（可选）
    proxy: Optional[str] = None
    
    def __post_init__(self):
        self.ua = UserAgent()

class AdvancedOKXDocsCrawler:
    """高级OKX文档爬虫"""
    
    def __init__(self, config: AdvancedCrawlConfig = None):
        self.config = config or AdvancedCrawlConfig()
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self.driver_pool: List[webdriver.Chrome] = []
        
        # 创建输出目录
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        
    def create_driver(self) -> webdriver.Chrome:
        """创建Chrome驱动"""
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
        
        # 窗口大小随机化
        width = random.randint(1200, 1920)
        height = random.randint(800, 1080)
        options.add_argument(f'--window-size={width},{height}')
        
        # 代理配置
        if self.config.proxy:
            options.add_argument(f'--proxy-server={self.config.proxy}')
            
        # 其他反检测配置
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-plugins')
        options.add_argument('--disable-images')  # 禁用图片加载，提高速度
        
        try:
            driver = webdriver.Chrome(options=options)
            
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
            limit=50,
            limit_per_host=5,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
        
        # 预创建Selenium驱动池
        if self.config.use_selenium:
            for _ in range(min(3, self.config.max_concurrent)):
                try:
                    driver = self.create_driver()
                    self.driver_pool.append(driver)
                except Exception as e:
                    logger.warning(f"创建驱动失败: {e}")
                    
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
        # 关闭所有驱动
        for driver in self.driver_pool:
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"关闭驱动失败: {e}")
                
    def get_random_headers(self) -> Dict[str, str]:
        """获取随机请求头"""
        return {
            'User-Agent': self.config.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': random.choice([
                'zh-CN,zh;q=0.9,en;q=0.8',
                'en-US,en;q=0.9,zh;q=0.8',
                'zh-CN,zh;q=0.8,en;q=0.7'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': random.choice(['none', 'same-origin', 'cross-site']),
            'Cache-Control': random.choice(['max-age=0', 'no-cache']),
        }
        
    async def fetch_with_selenium(self, url: str) -> Optional[str]:
        """使用Selenium获取页面内容"""
        if not self.driver_pool:
            logger.error("没有可用的Selenium驱动")
            return None
            
        driver = random.choice(self.driver_pool)
        
        try:
            logger.info(f"使用Selenium获取: {url}")
            
            # 随机延迟
            await asyncio.sleep(random.uniform(*self.config.delay_range))
            
            # 访问页面
            driver.get(url)
            
            # 等待页面加载
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # 模拟人类行为
            await self.simulate_human_behavior(driver)
            
            # 等待动态内容加载
            await asyncio.sleep(random.uniform(2, 4))
            
            # 获取页面源码
            html = driver.page_source
            logger.info(f"Selenium成功获取: {url}")
            return html
            
        except TimeoutException:
            logger.error(f"Selenium超时: {url}")
        except WebDriverException as e:
            logger.error(f"Selenium错误: {url}, {e}")
        except Exception as e:
            logger.error(f"Selenium未知错误: {url}, {e}")
            
        return None
        
    async def simulate_human_behavior(self, driver):
        """模拟人类行为"""
        try:
            # 随机滚动
            scroll_count = random.randint(1, 3)
            for _ in range(scroll_count):
                scroll_y = random.randint(100, 500)
                driver.execute_script(f"window.scrollBy(0, {scroll_y});")
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
            # 随机移动鼠标（通过JavaScript）
            x = random.randint(100, 800)
            y = random.randint(100, 600)
            driver.execute_script(f"""
                var event = new MouseEvent('mousemove', {{
                    clientX: {x},
                    clientY: {y}
                }});
                document.dispatchEvent(event);
            """)
            
        except Exception as e:
            logger.debug(f"模拟人类行为失败: {e}")
            
    async def fetch_with_aiohttp(self, url: str, retries: int = 0) -> Optional[str]:
        """使用aiohttp获取页面内容"""
        try:
            headers = self.get_random_headers()
            
            # 随机延迟
            await asyncio.sleep(random.uniform(*self.config.delay_range))
            
            logger.info(f"使用aiohttp获取: {url}")
            
            async with self.session.get(url, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    logger.info(f"aiohttp成功获取: {url}")
                    return content
                elif response.status == 429:  # 请求过于频繁
                    logger.warning(f"请求频率限制: {url}")
                    await asyncio.sleep(random.uniform(10, 20))
                    if retries < self.config.max_retries:
                        return await self.fetch_with_aiohttp(url, retries + 1)
                else:
                    logger.error(f"HTTP错误 {response.status}: {url}")
                    
        except Exception as e:
            logger.error(f"aiohttp请求失败: {url}, 错误: {e}")
            if retries < self.config.max_retries:
                await asyncio.sleep(random.uniform(3, 8))
                return await self.fetch_with_aiohttp(url, retries + 1)
                
        return None
        
    async def fetch_page(self, url: str) -> Optional[str]:
        """智能获取页面内容"""
        # 首先尝试aiohttp
        html = await self.fetch_with_aiohttp(url)
        
        # 如果失败或内容不完整，使用Selenium
        if not html or self.needs_selenium(html):
            if self.config.use_selenium:
                html = await self.fetch_with_selenium(url)
                
        return html
        
    def needs_selenium(self, html: str) -> bool:
        """判断是否需要使用Selenium"""
        if not html:
            return True
            
        # 检查是否包含大量JavaScript或动态加载标识
        js_indicators = [
            'document.createElement',
            'React.createElement',
            'Vue.createApp',
            'angular.module',
            '__NEXT_DATA__',
            'window.__INITIAL_STATE__'
        ]
        
        return any(indicator in html for indicator in js_indicators)
        
    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """从HTML中提取相关链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        # 查找所有链接
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if self.is_docs_url(full_url):
                links.add(full_url)
                
        # 查找导航菜单和侧边栏链接
        nav_selectors = [
            'nav a[href]',
            '.sidebar a[href]',
            '.menu a[href]',
            '.navigation a[href]',
            '.toc a[href]',
            '.docs-nav a[href]',
            '[class*="nav"] a[href]',
            '[class*="menu"] a[href]',
            '[class*="sidebar"] a[href]',
            '[data-testid*="nav"] a[href]'
        ]
        
        for selector in nav_selectors:
            for link in soup.select(selector):
                if link.get('href'):
                    full_url = urljoin(base_url, link['href'])
                    if self.is_docs_url(full_url):
                        links.add(full_url)
                        
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
            '/api/', '/auth/', '/login', '/register', '/logout'
        ]
        
        path_lower = parsed.path.lower()
        if any(pattern in path_lower for pattern in excluded_patterns):
            return False
            
        return True
        
    def extract_content(self, html: str, url: str) -> Dict[str, str]:
        """提取页面主要内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()
            
        # 尝试找到主要内容区域
        content_selectors = [
            'main',
            '.content',
            '.main-content',
            '.documentation',
            '.docs-content',
            '.markdown-body',
            '[class*="content"]',
            'article',
            '.post-content',
            '#content'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content and main_content.get_text(strip=True):
                break
                
        if not main_content:
            main_content = soup.find('body') or soup
            
        # 提取标题
        title = self.extract_title(soup)
        
        # 提取文本内容
        text_content = main_content.get_text(separator='\n', strip=True)
        
        # 清理文本内容
        text_content = self.clean_text(text_content)
        
        # 提取HTML内容（保留格式）
        html_content = str(main_content)
        
        return {
            'title': title,
            'text': text_content,
            'html': html_content,
            'url': url,
            'word_count': len(text_content.split()),
            'extract_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def extract_title(self, soup: BeautifulSoup) -> str:
        """提取页面标题"""
        # 尝试多种方式获取标题
        title_selectors = [
            'title',
            'h1',
            '.page-title',
            '.doc-title',
            '[class*="title"]',
            'meta[property="og:title"]'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    title = element.get('content', '')
                else:
                    title = element.get_text(strip=True)
                    
                if title:
                    return title
                    
        return "未知标题"
        
    def clean_text(self, text: str) -> str:
        """清理文本内容"""
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
        ]
        
        for pattern in patterns_to_remove:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
        return text.strip()
        
    async def save_content(self, content: Dict[str, str], url: str):
        """保存内容到文件"""
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
        
        # 准备markdown内容
        markdown_content = f"""# {content['title']}

**URL:** {content['url']}  
**抓取时间:** {content['extract_time']}  
**字数:** {content['word_count']}

---

{content['text']}

---

<details>
<summary>原始HTML内容</summary>

```html
{content['html']}
```

</details>
"""
        
        # 保存markdown文件
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(markdown_content)
            
        logger.info(f"已保存: {filepath}")
        
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
            
            html = await self.fetch_page(url)
            if not html:
                self.failed_urls.add(url)
                return set()
                
            # 提取内容
            content = self.extract_content(html, url)
            
            # 只保存有实际内容的页面
            if content['word_count'] > 50:  # 至少50个词
                await self.save_content(content, url)
            else:
                logger.info(f"跳过内容过少的页面: {url}")
                
            # 提取新链接
            new_links = self.extract_links(html, url)
            return new_links - self.visited_urls
            
    async def crawl(self):
        """开始爬取"""
        logger.info(f"开始爬取OKX文档: {self.config.start_url}")
        logger.info(f"使用Selenium: {self.config.use_selenium}")
        logger.info(f"输出目录: {self.config.output_dir}")
        
        # 待处理的URL队列
        urls_to_crawl = {self.config.start_url}
        
        while urls_to_crawl:
            # 批量处理URL
            current_batch = list(urls_to_crawl)[:self.config.max_concurrent]
            urls_to_crawl -= set(current_batch)
            
            # 并发爬取
            tasks = [self.crawl_url(url) for url in current_batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 收集新发现的链接
            for result in results:
                if isinstance(result, set):
                    urls_to_crawl.update(result)
                elif isinstance(result, Exception):
                    logger.error(f"爬取任务异常: {result}")
                    
            logger.info(f"已处理: {len(self.visited_urls)}, 待处理: {len(urls_to_crawl)}, 失败: {len(self.failed_urls)}")
            
            # 避免过于频繁的请求
            if urls_to_crawl:
                await asyncio.sleep(random.uniform(2, 5))
                
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
                'delay_range': self.config.delay_range
            }
        }
        
        stats_file = Path(self.config.output_dir) / 'crawl_stats.json'
        async with aiofiles.open(stats_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(stats, ensure_ascii=False, indent=2))
            
        # 创建简单的报告
        report = f"""# OKX文档爬取报告

## 统计信息
- 成功爬取: {stats['total_crawled']} 页面
- 失败: {stats['total_failed']} 页面  
- 成功率: {stats['success_rate']:.1f}%
- 爬取时间: {stats['crawl_time']}

## 配置信息
- 使用Selenium: {stats['config']['use_selenium']}
- 最大并发: {stats['config']['max_concurrent']}
- 延迟范围: {stats['config']['delay_range']}秒

## 失败的URL
{chr(10).join(f"- {url}" for url in stats['failed_urls'])}
"""
        
        report_file = Path(self.config.output_dir) / 'crawl_report.md'
        async with aiofiles.open(report_file, 'w', encoding='utf-8') as f:
            await f.write(report)

async def main():
    """主函数"""
    config = AdvancedCrawlConfig(
        max_concurrent=2,  # 保守的并发数
        delay_range=(3, 6),  # 较长的延迟
        use_selenium=True,  # 启用Selenium
        headless=True  # 无头模式
    )
    
    async with AdvancedOKXDocsCrawler(config) as crawler:
        await crawler.crawl()

if __name__ == "__main__":
    asyncio.run(main()) 