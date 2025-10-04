# OKX文档爬虫使用指南

## 🎯 功能特点

✅ **解决React SPA问题**：使用Selenium等待JavaScript渲染完成  
✅ **智能内容提取**：针对OKX文档结构优化的内容提取器  
✅ **反检测机制**：随机User-Agent、延迟、模拟用户行为  
✅ **结构化输出**：同时生成Markdown和JSON格式  
✅ **完整导航信息**：保留面包屑、侧边栏、目录结构  

## 🚀 基本使用

### 1. 快速开始

```bash
# 运行爬虫（后台模式）
python okx_docs_crawler_improved.py

# 监控进度
python monitor_crawl.py
```

### 2. 自定义配置运行

```python
from okx_docs_crawler_improved import ImprovedOKXDocsCrawler, ImprovedCrawlConfig
import asyncio

# 自定义配置
config = ImprovedCrawlConfig(
    start_url="https://web3.okx.com/zh-hans/build/dev-docs/",
    output_dir="data/my_okx_docs",
    max_concurrent=1,        # 并发数（建议保持1）
    delay_range=(8, 15),     # 延迟范围（秒）
    use_selenium=True,       # 使用Selenium
    headless=True,           # 无头模式
    page_load_timeout=30     # 页面加载超时
)

# 运行爬虫
async def main():
    async with ImprovedOKXDocsCrawler(config) as crawler:
        await crawler.crawl()

asyncio.run(main())
```

## 📁 输出结构

```
data/okx_docs/
├── zh-hans/
│   └── build/
│       ├── dev-docs.md          # 首页文档
│       ├── dev-docs.json        # 首页元数据
│       └── dev-docs/
│           └── dex-api/
│               ├── dex-trade-api-introduction.md
│               ├── dex-trade-api-introduction.json
│               ├── dex-market-api-introduction.md
│               └── ...
├── crawl_stats.json             # 爬取统计
└── crawl_report.md              # 详细报告
```

## 📄 文件格式说明

### Markdown文件 (.md)
```markdown
# 页面标题

**URL:** 原始链接
**抓取时间:** 2025-05-27 00:04:00
**字数:** 88

## 导航路径
DEX API > 首页 > 什么是 DEX API

## 目录
- 介绍
- 为什么选择 OKX DEX API？

---

[文档正文内容]

---

<details>
<summary>原始HTML内容</summary>
[原始HTML代码]
</details>

<details>
<summary>导航信息</summary>
[JSON格式的导航数据]
</details>
```

### JSON文件 (.json)
```json
{
  "title": "页面标题",
  "text": "纯文本内容",
  "html": "原始HTML",
  "url": "页面URL",
  "navigation": {
    "breadcrumbs": ["面包屑导航"],
    "sidebar_links": ["侧边栏链接"],
    "toc": ["目录项"]
  },
  "word_count": 88,
  "extract_time": "2025-05-27 00:04:00"
}
```

## ⚙️ 配置参数详解

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `start_url` | OKX文档首页 | 开始爬取的URL |
| `output_dir` | `data/okx_docs` | 输出目录 |
| `max_concurrent` | 1 | 并发数（建议保持1避免被检测） |
| `delay_range` | (5, 10) | 请求间隔（秒） |
| `timeout` | 60 | HTTP超时时间 |
| `use_selenium` | True | 是否使用Selenium |
| `headless` | True | 是否无头模式 |
| `page_load_timeout` | 30 | 页面加载超时 |

## 🔧 常用命令

### 检查爬取状态
```bash
# 查看已爬取的文件数量
find data/okx_docs -name "*.md" | wc -l

# 查看最新爬取的文件
ls -lt data/okx_docs/zh-hans/build/dev-docs/dex-api/ | head -5

# 查看爬取统计
cat data/okx_docs/crawl_stats.json
```

### 重新开始爬取
```bash
# 清理之前的结果
rm -rf data/okx_docs

# 重新运行
python okx_docs_crawler_improved.py
```

### 只爬取特定页面
```python
# 测试单个页面
python test_improved_crawler.py
```

## 📊 监控和管理

### 实时监控
```bash
python monitor_crawl.py
```

监控输出示例：
```
🔍 监控OKX文档爬取进度...
📁 输出目录: data\okx_docs
============================================================
⏰ 00:09:39 | 📄 已爬取: 37 页面 | ⏱️ 用时: 285秒
📝 最新文件: dex-approve-transaction.md
📊 统计信息:
   - 成功: 37 页面
   - 失败: 2 页面
   - 成功率: 94.9%
```

### 查看爬取报告
```bash
# 查看详细报告
cat data/okx_docs/crawl_report.md

# 查看统计信息
python -c "import json; print(json.dumps(json.load(open('data/okx_docs/crawl_stats.json')), indent=2, ensure_ascii=False))"
```

## 🛠️ 故障排除

### 常见问题

1. **Chrome驱动问题**
   ```bash
   # 安装/更新Chrome驱动
   pip install --upgrade selenium
   # 或手动下载对应版本的chromedriver
   ```

2. **内存不足**
   ```python
   # 降低并发数
   config.max_concurrent = 1
   # 增加延迟
   config.delay_range = (10, 20)
   ```

3. **被反爬虫检测**
   ```python
   # 增加延迟
   config.delay_range = (15, 30)
   # 使用代理（需要额外配置）
   ```

4. **页面加载超时**
   ```python
   # 增加超时时间
   config.page_load_timeout = 60
   config.timeout = 120
   ```

### 调试模式

```bash
# 运行调试脚本
python debug_okx_page.py

# 查看详细日志
python okx_docs_crawler_improved.py 2>&1 | tee crawl.log
```

## 📈 性能优化建议

1. **网络环境**：使用稳定的网络连接
2. **系统资源**：确保有足够的内存（建议4GB+）
3. **并发控制**：保持`max_concurrent=1`避免被检测
4. **延迟设置**：根据网络情况调整`delay_range`
5. **定期清理**：删除不需要的临时文件

## 🎯 使用技巧

### 1. 批量处理
```bash
# 爬取完成后批量转换格式
for file in data/okx_docs/**/*.md; do
    echo "处理: $file"
    # 你的处理逻辑
done
```

### 2. 内容搜索
```bash
# 在所有文档中搜索关键词
grep -r "API" data/okx_docs/ --include="*.md"

# 统计词频
cat data/okx_docs/**/*.md | tr ' ' '\n' | sort | uniq -c | sort -nr | head -20
```

### 3. 数据分析
```python
import json
from pathlib import Path

# 分析爬取的数据
docs_dir = Path("data/okx_docs")
json_files = list(docs_dir.rglob("*.json"))

total_words = 0
for file in json_files:
    if file.name != "crawl_stats.json":
        data = json.loads(file.read_text(encoding='utf-8'))
        total_words += data.get('word_count', 0)

print(f"总字数: {total_words}")
print(f"平均每页字数: {total_words / len(json_files):.0f}")
```

## 📞 支持

如果遇到问题：
1. 查看 `crawl_stats.json` 中的错误信息
2. 检查 `crawl_report.md` 中的详细报告
3. 运行 `python test_improved_crawler.py` 进行诊断

---

**注意**：请遵守网站的robots.txt和使用条款，合理使用爬虫工具。 