# OKX DEX API 文档爬虫使用说明

本项目提供了两个版本的爬虫来获取 [OKX DEX API 文档](https://web3.okx.com/zh-hans/build/dev-docs/) 的所有内容。

## 爬虫版本

### 1. 基础版本 (`okx_docs_crawler.py`)
- 使用 `aiohttp` 进行HTTP请求
- 适合静态内容网站
- 速度较快，资源消耗少
- 基本的反爬虫机制

### 2. 增强版本 (`okx_docs_crawler_advanced.py`) **推荐**
- 支持JavaScript渲染（Selenium）
- 更强的反爬虫能力
- 智能内容检测
- 模拟人类行为
- 更好的错误处理

## 安装依赖

首先确保安装了所需的依赖包：

```bash
# 更新conda环境
conda env update -f environment.yml

# 或者手动安装
pip install aiohttp aiofiles beautifulsoup4 lxml selenium fake-useragent
```

### Chrome驱动安装

增强版爬虫需要Chrome浏览器和ChromeDriver：

1. **安装Chrome浏览器**
2. **安装ChromeDriver**：
   ```bash
   # Windows (使用chocolatey)
   choco install chromedriver
   
   # macOS (使用homebrew)
   brew install chromedriver
   
   # Linux
   sudo apt-get install chromium-chromedriver
   ```

## 使用方法

### 基础版本
```bash
cd scripts
python okx_docs_crawler.py
```

### 增强版本（推荐）
```bash
cd scripts
python okx_docs_crawler_advanced.py
```

## 配置选项

可以通过修改配置类来自定义爬虫行为：

```python
config = AdvancedCrawlConfig(
    max_concurrent=2,        # 并发数（建议1-3）
    delay_range=(3, 6),      # 请求间隔（秒）
    use_selenium=True,       # 是否使用Selenium
    headless=True,           # 无头模式
    timeout=30,              # 请求超时
    output_dir="data/okx_docs"  # 输出目录
)
```

## 输出结果

爬虫会在 `data/okx_docs/` 目录下创建以下文件：

```
data/okx_docs/
├── index.md                 # 首页内容
├── api/                     # API相关文档
├── guides/                  # 指南文档
├── crawl_stats.json         # 爬取统计
├── crawl_report.md          # 爬取报告
└── ...                      # 其他文档页面
```

每个页面会生成两个文件：
- `.md` 文件：Markdown格式的内容
- `.json` 文件：结构化的元数据

## 反爬虫机制应对

### 1. 请求频率控制
- 随机延迟：2-6秒
- 并发限制：最多3个
- 失败重试：最多3次

### 2. 请求头伪装
- 随机User-Agent
- 完整的浏览器请求头
- 随机Accept-Language

### 3. 行为模拟
- 随机滚动页面
- 鼠标移动模拟
- 页面停留时间

### 4. 技术手段
- Selenium反检测
- 代理支持（可选）
- JavaScript执行

## 常见问题

### Q: 爬虫被检测到怎么办？
A: 
1. 增加延迟时间：`delay_range=(5, 10)`
2. 降低并发数：`max_concurrent=1`
3. 使用代理：`proxy="http://proxy:port"`
4. 启用Selenium：`use_selenium=True`

### Q: Chrome驱动问题
A:
1. 确保Chrome和ChromeDriver版本匹配
2. 将ChromeDriver添加到PATH
3. 检查权限设置

### Q: 内容不完整
A:
1. 使用增强版爬虫
2. 启用Selenium：`use_selenium=True`
3. 增加等待时间

### Q: 速度太慢
A:
1. 使用基础版爬虫
2. 增加并发数：`max_concurrent=5`
3. 减少延迟：`delay_range=(1, 2)`
4. 禁用图片加载

## 注意事项

1. **遵守网站条款**：请确保遵守OKX网站的使用条款
2. **合理使用**：不要过于频繁地请求，避免给服务器造成压力
3. **数据用途**：仅用于学习和研究目的
4. **版权尊重**：尊重原始内容的版权

## 高级配置

### 使用代理
```python
config = AdvancedCrawlConfig(
    proxy="http://username:password@proxy:port"
)
```

### 自定义输出格式
可以修改 `save_content` 方法来自定义输出格式。

### 添加新的内容选择器
在 `extract_content` 方法中添加新的CSS选择器来适应不同的网站结构。

## 监控和调试

爬虫运行时会输出详细的日志信息：
- 成功/失败的URL
- 处理进度
- 错误信息

可以通过修改日志级别来获取更多调试信息：
```python
logging.basicConfig(level=logging.DEBUG)
```

## 扩展功能

爬虫框架支持扩展：
1. 添加新的内容提取器
2. 支持更多文件格式
3. 集成数据库存储
4. 添加内容去重
5. 支持增量更新

## 技术支持

如果遇到问题，请检查：
1. 依赖包是否正确安装
2. Chrome和ChromeDriver版本
3. 网络连接状态
4. 目标网站是否有变化 