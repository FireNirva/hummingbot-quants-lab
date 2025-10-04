#!/usr/bin/env python3
"""
OKX DEX API 文档爬虫
用于爬取 https://web3.okx.com/zh-hans/build/dev-docs/ 下的所有文档内容
"""

import asyncio
import aiohttp
import aiofiles
import time
import random
import json
import os
import re
from urllib.parse import urljoin, urlparse, parse_qs
from pathlib import Path
from typing import Set, List, Dict, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CrawlConfig:
    """爬虫配置"""
    base_url: str = "https://web3.okx.com"
    start_url: str = "https://web3.okx.com/zh-hans/build/dev-docs/"
    output_dir: str = "data/okx_docs"
    max_concurrent: int = 5
    delay_range: tuple = (1, 3)  # 随机延迟范围（秒）
    timeout: int = 30
    max_retries: int = 3
    
    # 请求头配置，模拟真实浏览器
    headers: Dict[str, str] = None
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
            }

class OKXDocsCrawler:
    """OKX文档爬虫"""
    
    def __init__(self, config: CrawlConfig = None):
        self.config = config or CrawlConfig()
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        # 创建输出目录
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)
        
    async def __aenter__(self):
        """异步上下文管理器入口"""
        connector = aiohttp.TCPConnector(
            limit=100,
            limit_per_host=10,
            ttl_dns_cache=300,
            use_dns_cache=True,
        )
        
        timeout = aiohttp.ClientTimeout(total=self.config.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers=self.config.headers
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
            
    async def fetch_page(self, url: str, retries: int = 0) -> Optional[str]:
        """获取页面内容"""
        async with self.semaphore:
            try:
                # 随机延迟，避免被反爬虫检测
                await asyncio.sleep(random.uniform(*self.config.delay_range))
                
                logger.info(f"正在获取: {url}")
                
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        logger.info(f"成功获取: {url}")
                        return content
                    elif response.status == 429:  # 请求过于频繁
                        logger.warning(f"请求频率限制: {url}, 等待更长时间...")
                        await asyncio.sleep(random.uniform(5, 10))
                        if retries < self.config.max_retries:
                            return await self.fetch_page(url, retries + 1)
                    else:
                        logger.error(f"HTTP错误 {response.status}: {url}")
                        
            except asyncio.TimeoutError:
                logger.error(f"请求超时: {url}")
                if retries < self.config.max_retries:
                    logger.info(f"重试 {retries + 1}/{self.config.max_retries}: {url}")
                    await asyncio.sleep(random.uniform(2, 5))
                    return await self.fetch_page(url, retries + 1)
            except Exception as e:
                logger.error(f"请求失败: {url}, 错误: {e}")
                if retries < self.config.max_retries:
                    logger.info(f"重试 {retries + 1}/{self.config.max_retries}: {url}")
                    await asyncio.sleep(random.uniform(2, 5))
                    return await self.fetch_page(url, retries + 1)
                    
        return None
        
    def extract_links(self, html: str, base_url: str) -> Set[str]:
        """从HTML中提取相关链接"""
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        # 查找所有链接
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            
            # 只保留文档相关的链接
            if self.is_docs_url(full_url):
                links.add(full_url)
                
        # 查找导航菜单中的链接
        nav_selectors = [
            'nav a[href]',
            '.sidebar a[href]',
            '.menu a[href]',
            '.navigation a[href]',
            '[class*="nav"] a[href]',
            '[class*="menu"] a[href]',
            '[class*="sidebar"] a[href]'
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
            
        # 排除不需要的文件类型
        excluded_extensions = {'.pdf', '.zip', '.tar', '.gz', '.jpg', '.png', '.gif', '.css', '.js'}
        if any(parsed.path.lower().endswith(ext) for ext in excluded_extensions):
            return False
            
        return True
        
    def extract_content(self, html: str, url: str) -> Dict[str, str]:
        """提取页面主要内容"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除不需要的元素
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
            
        # 尝试找到主要内容区域
        content_selectors = [
            'main',
            '.content',
            '.main-content',
            '.documentation',
            '.docs-content',
            '[class*="content"]',
            'article',
            '.markdown-body'
        ]
        
        main_content = None
        for selector in content_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
                
        if not main_content:
            main_content = soup.find('body') or soup
            
        # 提取标题
        title = ""
        title_element = soup.find('title')
        if title_element:
            title = title_element.get_text().strip()
        else:
            h1 = soup.find('h1')
            if h1:
                title = h1.get_text().strip()
                
        # 提取文本内容
        text_content = main_content.get_text(separator='\n', strip=True)
        
        # 提取HTML内容（保留格式）
        html_content = str(main_content)
        
        return {
            'title': title,
            'text': text_content,
            'html': html_content,
            'url': url
        }
        
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
            
        # 创建子目录
        subdir = Path(self.config.output_dir) / '/'.join(path_parts[:-1]) if len(path_parts) > 1 else Path(self.config.output_dir)
        subdir.mkdir(parents=True, exist_ok=True)
        
        filepath = subdir / filename
        
        # 准备markdown内容
        markdown_content = f"""# {content['title']}

**URL:** {content['url']}
**抓取时间:** {time.strftime('%Y-%m-%d %H:%M:%S')}

---

{content['text']}

---

## 原始HTML

```html
{content['html']}
```
"""
        
        # 保存文件
        async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
            await f.write(markdown_content)
            
        logger.info(f"已保存: {filepath}")
        
        # 同时保存JSON格式
        json_filepath = filepath.with_suffix('.json')
        async with aiofiles.open(json_filepath, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(content, ensure_ascii=False, indent=2))
            
    async def crawl_url(self, url: str) -> Set[str]:
        """爬取单个URL"""
        if url in self.visited_urls:
            return set()
            
        self.visited_urls.add(url)
        
        html = await self.fetch_page(url)
        if not html:
            self.failed_urls.add(url)
            return set()
            
        # 提取内容
        content = self.extract_content(html, url)
        await self.save_content(content, url)
        
        # 提取新链接
        new_links = self.extract_links(html, url)
        return new_links - self.visited_urls
        
    async def crawl(self):
        """开始爬取"""
        logger.info(f"开始爬取OKX文档: {self.config.start_url}")
        
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
            
        # 保存爬取统计
        stats = {
            'total_crawled': len(self.visited_urls),
            'failed_urls': list(self.failed_urls),
            'crawl_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'visited_urls': list(self.visited_urls)
        }
        
        stats_file = Path(self.config.output_dir) / 'crawl_stats.json'
        async with aiofiles.open(stats_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(stats, ensure_ascii=False, indent=2))
            
        logger.info(f"爬取完成! 总计: {len(self.visited_urls)} 页面, 失败: {len(self.failed_urls)} 页面")
        logger.info(f"结果保存在: {self.config.output_dir}")

async def main():
    """主函数"""
    config = CrawlConfig()
    
    async with OKXDocsCrawler(config) as crawler:
        await crawler.crawl()

if __name__ == "__main__":
    asyncio.run(main()) 