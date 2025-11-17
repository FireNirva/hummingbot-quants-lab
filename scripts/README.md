# 🛠️ QuantsLab 脚本索引

本目录包含 QuantsLab 项目的所有可执行脚本。脚本按功能分类，方便查找和使用。

---

## 📖 **快速参考**

### **最常用脚本**

```bash
# 数据采集
bash scripts/run_complete_analysis.sh          # 完整 CEX-DEX 分析流程
python scripts/import_freqtrade_data.py        # 导入 Freqtrade 数据
python scripts/download_dex_ohlcv.py          # 下载 DEX OHLCV 数据

# 订单簿采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
python scripts/check_realtime_orderbook.py     # 检查订单簿实时状态
python scripts/monitor_orderbook_liquidity.py  # 监控流动性

# 套利分析
python scripts/analyze_cex_dex_spread.py --compare-all  # 价差分析
python scripts/calculate_optimal_trade_size.py          # 最优交易规模
```

---

## 📊 **数据采集**

### CEX 数据采集

| 脚本 | 说明 | 用法 |
|------|------|------|
| `import_freqtrade_data.py` | 从 Freqtrade 导入 CEX 历史数据 | `python scripts/import_freqtrade_data.py --config config/gateio_USDT_downloader_full.yml --days 7` |
| `quick_start.py` | 快速开始数据采集 | `python scripts/quick_start.py` |

### DEX 数据采集

| 脚本 | 说明 | 用法 |
|------|------|------|
| `download_dex_ohlcv.py` | 下载 DEX OHLCV 数据 | `python scripts/download_dex_ohlcv.py --network base --days 3` |
| `run_dex_download_now.py` | 立即运行 DEX 下载 | `python scripts/run_dex_download_now.py` |
| `optimize_aero_download.py` | 优化 Aerodrome 下载 | `python scripts/optimize_aero_download.py` |
| `debug_dex_data.py` | 调试 DEX 数据 | `python scripts/debug_dex_data.py` |

### 池子映射

| 脚本 | 说明 | 用法 |
|------|------|------|
| `build_pool_mapping.py` | 构建 CEX-DEX 池子映射 | `python scripts/build_pool_mapping.py --connector gate_io --network base` |

---

## 🔧 **订单簿采集**

### 采集管理

| 脚本 | 说明 | 用法 |
|------|------|------|
| `check_realtime_orderbook.py` | 检查订单簿实时采集状态 | `python scripts/check_realtime_orderbook.py` |
| `check_orderbook_data.py` | 检查订单簿数据质量 | `python scripts/check_orderbook_data.py` |
| `monitor_orderbook_collection.py` | 监控订单簿采集健康度 | `python scripts/monitor_orderbook_collection.py` |
| `monitor_orderbook_liquidity.py` | 分析订单簿流动性 | `python scripts/monitor_orderbook_liquidity.py` |
| `query_orderbook_by_date.py` | 按日期查询订单簿 | `python scripts/query_orderbook_by_date.py --date 20251117` |
| `get_realtime_orderbook.py` | 获取实时订单簿（API） | `python scripts/get_realtime_orderbook.py IRON-USDT gate_io` |

### Shell 监控脚本

| 脚本 | 说明 | 用法 |
|------|------|------|
| `monitor_orderbook_live.sh` | 实时监控订单簿（详细） | `bash scripts/monitor_orderbook_live.sh` |
| `monitor_orderbook_simple.sh` | 实时监控订单簿（简单） | `bash scripts/monitor_orderbook_simple.sh` |

### 任务控制

| 脚本 | 说明 | 用法 |
|------|------|------|
| `restart_orderbook_gateio.sh` | 重启 Gate.io 订单簿采集 | `bash scripts/restart_orderbook_gateio.sh` |
| `stop_all_orderbook.sh` | 停止所有订单簿采集 | `bash scripts/stop_all_orderbook.sh` |
| `stop_orderbook_tasks.sh` | 交互式停止任务 | `bash scripts/stop_orderbook_tasks.sh` |
| `status_orderbook_tasks.sh` | 查看任务状态 | `bash scripts/status_orderbook_tasks.sh` |
| `clean_and_restart.sh` | 清理并重启采集 | `bash scripts/clean_and_restart.sh` |
| `quick_restart.sh` | 快速重启 | `bash scripts/quick_restart.sh` |
| `optimize_and_restart.sh` | 优化后重启 | `bash scripts/optimize_and_restart.sh` |
| `switch_to_optimized_orderbook.sh` | 切换到优化配置 | `bash scripts/switch_to_optimized_orderbook.sh` |

### 数据清理

| 脚本 | 说明 | 用法 |
|------|------|------|
| `cleanup_old_orderbook_data.py` | 清理旧订单簿数据 | `python scripts/cleanup_old_orderbook_data.py --days 7 --dry-run` |
| `cleanup_tasks.py` | 清理后台任务 | `python scripts/cleanup_tasks.py` |

---

## 💰 **套利分析**

### 价差分析

| 脚本 | 说明 | 用法 |
|------|------|------|
| `analyze_cex_dex_spread.py` | CEX-DEX 价差分析 | `python scripts/analyze_cex_dex_spread.py --compare-all` |
| `analyze_liquidity_and_capital.py` | 流动性和资金需求分析 | `python scripts/analyze_liquidity_and_capital.py` |
| `plot_spread_analysis.py` | 价差可视化 | `python scripts/plot_spread_analysis.py` |

### 交易规模优化

| 脚本 | 说明 | 用法 |
|------|------|------|
| `calculate_optimal_trade_size.py` | 计算最优交易规模 | `python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io` |
| `batch_optimize_trade_size.py` | 批量优化交易规模 | `python scripts/batch_optimize_trade_size.py --config config/base_ecosystem_downloader_full.yml` |
| `calculate_slippage_from_orderbook.py` | 从订单簿计算滑点 | `python scripts/calculate_slippage_from_orderbook.py` |

---

## 🚀 **完整工作流**

### 一键运行脚本

| 脚本 | 说明 | 用法 |
|------|------|------|
| `run_complete_analysis.sh` | 完整 CEX-DEX 套利分析 | `bash scripts/run_complete_analysis.sh` |
| `run_complete_analysis_manual.sh` | 完整分析（手动环境） | `bash scripts/run_complete_analysis_manual.sh` |
| `run_mexc_analysis.sh` | MEXC 交易所分析 | `bash scripts/run_mexc_analysis.sh` |
| `continue_analysis.sh` | 继续分析 | `bash scripts/continue_analysis.sh` |
| `quick_test_pairs.sh` | 快速测试交易对 | `bash scripts/quick_test_pairs.sh` |

---

## ☁️ **AWS 部署**

| 脚本 | 说明 | 用法 |
|------|------|------|
| `aws_setup.sh` | AWS 服务器初始化 | `bash scripts/aws_setup.sh` |
| `deploy_to_aws.sh` | 本地到 AWS 一键部署 | `bash scripts/deploy_to_aws.sh` |

---

## 🌐 **数据源集成**

### Crypto Lake

| 脚本 | 说明 | 用法 |
|------|------|------|
| `download_crypto_lake_data.py` | 下载 Crypto Lake 数据 | `python scripts/download_crypto_lake_data.py` |
| `test_crypto_lake.py` | 测试 Crypto Lake 连接 | `python scripts/test_crypto_lake.py` |

### OKX 文档爬虫

| 脚本 | 说明 | 用法 |
|------|------|------|
| `okx_docs_crawler.py` | OKX 文档爬虫 | `python scripts/okx_docs_crawler.py` |
| `okx_docs_crawler_advanced.py` | OKX 高级爬虫 | `python scripts/okx_docs_crawler_advanced.py` |
| `okx_docs_crawler_improved.py` | OKX 改进爬虫 | `python scripts/okx_docs_crawler_improved.py` |
| `run_okx_crawler.py` | 运行 OKX 爬虫 | `python scripts/run_okx_crawler.py` |
| `monitor_crawl.py` | 监控爬虫 | `python scripts/monitor_crawl.py` |
| `debug_okx_page.py` | 调试 OKX 页面 | `python scripts/debug_okx_page.py` |

---

## 🔧 **工具脚本**

### 配置生成

| 脚本 | 说明 | 用法 |
|------|------|------|
| `generate_downloader_config.py` | 生成下载器配置 | `python scripts/generate_downloader_config.py` |

### 数据处理

| 脚本 | 说明 | 用法 |
|------|------|------|
| `extract_marked_tokens.py` | 提取标记的代币 | `python scripts/extract_marked_tokens.py` |
| `manual_tokens_to_md.py` | 代币转 Markdown | `python scripts/manual_tokens_to_md.py` |
| `quick_extract.py` | 快速提取 | `python scripts/quick_extract.py` |

### PDF 处理

| 脚本 | 说明 | 用法 |
|------|------|------|
| `pdf_to_markdown.py` | PDF 转 Markdown | `python scripts/pdf_to_markdown.py` |
| `pdf_to_md_ocr.py` | PDF OCR 转 Markdown | `python scripts/pdf_to_md_ocr.py` |
| `easyocr_extract.py` | EasyOCR 提取 | `python scripts/easyocr_extract.py` |

---

## 🧪 **测试脚本**

| 脚本 | 说明 | 用法 |
|------|------|------|
| `test_append.py` | 测试追加功能 | `python scripts/test_append.py` |
| `test_download_now.py` | 测试立即下载 | `python scripts/test_download_now.py` |
| `test_crypto_lake.py` | 测试 Crypto Lake | `python scripts/test_crypto_lake.py` |
| `test_crawler.py` | 测试爬虫 | `python scripts/test_crawler.py` |
| `test_improved_crawler.py` | 测试改进爬虫 | `python scripts/test_improved_crawler.py` |
| `test_gateio_orderbook_structure.py` | 测试 Gate.io 订单簿 | `python scripts/test_gateio_orderbook_structure.py` |
| `test_multi_exchange_orderbook.py` | 测试多交易所订单簿 | `python scripts/test_multi_exchange_orderbook.py` |
| `test_orderbook_rate_limit.py` | 测试订单簿限流 | `python scripts/test_orderbook_rate_limit.py` |
| `test_updated_orderbook.py` | 测试更新的订单簿 | `python scripts/test_updated_orderbook.py` |

---

## 📂 **脚本分类目录**

```
scripts/
├── 📊 数据采集/
│   ├── import_freqtrade_data.py
│   ├── download_dex_ohlcv.py
│   ├── run_dex_download_now.py
│   ├── build_pool_mapping.py
│   └── quick_start.py
│
├── 🔧 订单簿采集/
│   ├── check_realtime_orderbook.py
│   ├── check_orderbook_data.py
│   ├── monitor_orderbook_collection.py
│   ├── monitor_orderbook_liquidity.py
│   ├── get_realtime_orderbook.py
│   ├── cleanup_old_orderbook_data.py
│   └── 任务控制脚本...
│
├── 💰 套利分析/
│   ├── analyze_cex_dex_spread.py
│   ├── calculate_optimal_trade_size.py
│   ├── batch_optimize_trade_size.py
│   ├── calculate_slippage_from_orderbook.py
│   └── analyze_liquidity_and_capital.py
│
├── 🚀 完整工作流/
│   ├── run_complete_analysis.sh
│   ├── run_complete_analysis_manual.sh
│   ├── run_mexc_analysis.sh
│   └── continue_analysis.sh
│
├── ☁️ AWS 部署/
│   ├── aws_setup.sh
│   └── deploy_to_aws.sh
│
└── 🧪 测试/
    └── test_*.py
```

---

## 💡 **使用提示**

### **Python 脚本**

```bash
# 查看帮助
python scripts/[脚本名称].py --help

# 常见参数
--config          # 配置文件路径
--connector       # 交易所名称（gate_io, mexc）
--network         # 区块链网络（base, eth, bsc）
--days            # 天数
--interval        # 时间间隔
--dry-run         # 干运行（预览，不执行）
```

### **Shell 脚本**

```bash
# 添加执行权限
chmod +x scripts/[脚本名称].sh

# 运行
bash scripts/[脚本名称].sh
```

---

## 🔍 **按场景查找**

### 🚀 我想开始数据采集
```bash
bash scripts/run_complete_analysis.sh
```

### 📊 我想采集订单簿
```bash
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &
python scripts/check_realtime_orderbook.py
```

### 💰 我想分析套利机会
```bash
python scripts/analyze_cex_dex_spread.py --compare-all
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5
```

### 🔧 我想监控订单簿采集
```bash
python scripts/monitor_orderbook_liquidity.py
bash scripts/monitor_orderbook_live.sh
```

### 🛠️ 我想管理运行中的任务
```bash
bash scripts/status_orderbook_tasks.sh      # 查看状态
bash scripts/stop_all_orderbook.sh         # 停止所有
bash scripts/restart_orderbook_gateio.sh   # 重启
```

### ☁️ 我想部署到 AWS
```bash
bash scripts/deploy_to_aws.sh
```

---

## 📅 **脚本索引更新时间**

本索引最后更新: 2025-11-17

---

## 💡 **贡献**

如果你创建了新的脚本，请记得更新本索引文件！

---

**Happy Scripting! 🚀📊**

