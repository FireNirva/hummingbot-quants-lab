#!/usr/bin/env python3
"""
调试OKX页面结构
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

async def analyze_page():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get('https://web3.okx.com/zh-hans/build/dev-docs/', headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            print('=== 页面基本信息 ===')
            print('页面标题:', soup.find('title').get_text() if soup.find('title') else 'None')
            print('Body内容长度:', len(soup.find('body').get_text()) if soup.find('body') else 0)
            print('HTML总长度:', len(html))
            
            print('\n=== JavaScript检测 ===')
            print('是否包含React:', 'React' in html)
            print('是否包含__NEXT_DATA__:', '__NEXT_DATA__' in html)
            print('是否包含Vue:', 'Vue' in html)
            print('是否包含Angular:', 'angular' in html.lower())
            print('Script标签数量:', len(soup.find_all('script')))
            
            print('\n=== 内容容器分析 ===')
            selectors = [
                'main', '.content', '.docs', '[class*="content"]', 'article',
                '.documentation', '.markdown-body', '#app', '[id*="app"]',
                '.container', '[class*="container"]', '.page', '[class*="page"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    print(f'找到 {selector}: {len(elements)} 个元素')
                    for i, elem in enumerate(elements[:2]):
                        text = elem.get_text(strip=True)
                        if text:
                            print(f'  元素{i+1} (长度{len(text)}): {text[:100]}...')
                        else:
                            print(f'  元素{i+1}: 空内容')
                            
            print('\n=== 所有class名称 ===')
            all_classes = set()
            for elem in soup.find_all(class_=True):
                if isinstance(elem['class'], list):
                    all_classes.update(elem['class'])
                else:
                    all_classes.add(elem['class'])
            
            print('前20个class名称:', sorted(list(all_classes))[:20])
            
            print('\n=== 所有id名称 ===')
            all_ids = set()
            for elem in soup.find_all(id=True):
                all_ids.add(elem['id'])
            print('所有id:', sorted(list(all_ids)))
            
            # 保存原始HTML用于分析
            with open('debug_okx_page.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print('\n原始HTML已保存到 debug_okx_page.html')

if __name__ == "__main__":
    asyncio.run(analyze_page()) 