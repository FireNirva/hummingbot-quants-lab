# 📚 QuantsLab 文档索引

本目录包含 QuantsLab 项目的所有文档。文档按功能分类，方便查找。

---

## 📖 **快速开始**

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目总览和文档目录 |
| [QUICK_START_DATA_COLLECTION.md](QUICK_START_DATA_COLLECTION.md) | 数据采集快速入门 |
| [QUICK_START_32PAIRS.md](QUICK_START_32PAIRS.md) | 32 个交易对快速分析 |
| [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) | 完整工作流程指南 |

---

## 🔧 **订单簿采集系统**

### 核心指南
| 文档 | 说明 |
|------|------|
| [ORDERBOOK_COLLECTION_GUIDE.md](ORDERBOOK_COLLECTION_GUIDE.md) | 订单簿采集完整指南 |
| [START_ORDERBOOK_COLLECTION.md](START_ORDERBOOK_COLLECTION.md) | 订单簿采集快速启动 |
| [QUICKSTART_5S_ORDERBOOK.md](QUICKSTART_5S_ORDERBOOK.md) | 5 秒高频采集快速入门 |
| [HIGH_FREQUENCY_ORDERBOOK_SETUP.md](HIGH_FREQUENCY_ORDERBOOK_SETUP.md) | 高频采集详细设置 |

### 实现和优化
| 文档 | 说明 |
|------|------|
| [ORDERBOOK_IMPLEMENTATION_EXPLAINED.md](ORDERBOOK_IMPLEMENTATION_EXPLAINED.md) | 订单簿采集实现原理 |
| [ORDERBOOK_SEQUENCE_NUMBER_EXPLAINED.md](ORDERBOOK_SEQUENCE_NUMBER_EXPLAINED.md) | Sequence Number 详解 |
| [UPDATE_ID_DUPLICATE_EXPLAINED.md](UPDATE_ID_DUPLICATE_EXPLAINED.md) | Update ID 重复原因分析 |
| [ORDERBOOK_UPDATE_ID_ANALYSIS.md](ORDERBOOK_UPDATE_ID_ANALYSIS.md) | Update ID 深度分析 |
| [LIQUIDITY_ANALYSIS_SUMMARY.md](LIQUIDITY_ANALYSIS_SUMMARY.md) | 流动性分析总结 |

### 数据管理
| 文档 | 说明 |
|------|------|
| [ORDERBOOK_DATA_PARTITIONING.md](ORDERBOOK_DATA_PARTITIONING.md) | 数据分区策略 |
| [ORDERBOOK_TIMEZONE_EXPLAINED.md](ORDERBOOK_TIMEZONE_EXPLAINED.md) | 时区说明 |
| [TIMEZONE_VISUAL_GUIDE.md](TIMEZONE_VISUAL_GUIDE.md) | 时区可视化指南 |
| [ORDERBOOK_CLEANUP_GUIDE.md](ORDERBOOK_CLEANUP_GUIDE.md) | 数据清理指南 |

### 性能和监控
| 文档 | 说明 |
|------|------|
| [ORDERBOOK_5S_FIX.md](ORDERBOOK_5S_FIX.md) | 5 秒采集间隔修复 |
| [ORDERBOOK_PRECISION_OPTIMIZATION.md](ORDERBOOK_PRECISION_OPTIMIZATION.md) | 采集精度优化 |
| [DELAY_ANALYSIS.md](DELAY_ANALYSIS.md) | 延迟分析 |
| [ORDERBOOK_MONITORING_FIXED.md](ORDERBOOK_MONITORING_FIXED.md) | 监控脚本修复 |
| [ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md](ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md) | 采样频率指南 |

### 任务管理
| 文档 | 说明 |
|------|------|
| [ORDERBOOK_TASK_MANAGEMENT.md](ORDERBOOK_TASK_MANAGEMENT.md) | 任务管理完整指南 |
| [STOP_TASKS_QUICK_GUIDE.md](STOP_TASKS_QUICK_GUIDE.md) | 停止任务快速参考 |

### 多交易所支持
| 文档 | 说明 |
|------|------|
| [MULTI_EXCHANGE_ORDERBOOK_SETUP.md](MULTI_EXCHANGE_ORDERBOOK_SETUP.md) | 多交易所订单簿采集 |
| [MULTI_EXCHANGE_SETUP_SUMMARY.md](MULTI_EXCHANGE_SETUP_SUMMARY.md) | 多交易所设置总结 |

---

## 📊 **数据采集**

### 数据源
| 文档 | 说明 |
|------|------|
| [DATA_COLLECTION_GUIDE.md](DATA_COLLECTION_GUIDE.md) | 数据采集完整指南 |
| [DATA_COLLECTION_FLOW.md](DATA_COLLECTION_FLOW.md) | 数据采集流程 |
| [DATA_STORAGE_STRATEGY.md](DATA_STORAGE_STRATEGY.md) | 数据存储策略 |

### GeckoTerminal API
| 文档 | 说明 |
|------|------|
| [GECKOTERMINAL_API_USAGE.md](GECKOTERMINAL_API_USAGE.md) | GeckoTerminal API 使用 |
| [GECKOTERMINAL_API_REFERENCE.md](GECKOTERMINAL_API_REFERENCE.md) | GeckoTerminal API 参考 |
| [geckoterminal_api.md](geckoterminal_api.md) | GeckoTerminal API 文档 |

### 交易所 API
| 文档 | 说明 |
|------|------|
| [GATEIO_API_RATE_LIMITS.md](GATEIO_API_RATE_LIMITS.md) | Gate.io API 限流说明 |
| [GATEIO_PUBLIC_API_VS_PRIVATE_API.md](GATEIO_PUBLIC_API_VS_PRIVATE_API.md) | Gate.io 公共和私有 API |
| [GATEIO_ORDERBOOK_STRUCTURE.md](GATEIO_ORDERBOOK_STRUCTURE.md) | Gate.io 订单簿结构 |
| [GATEIO_ORDERBOOK_SUMMARY.md](GATEIO_ORDERBOOK_SUMMARY.md) | Gate.io 订单簿总结 |
| [API_KEY_ANSWER.md](API_KEY_ANSWER.md) | API Key 使用说明 |

### 外部数据源
| 文档 | 说明 |
|------|------|
| [CRYPTO_LAKE_INTEGRATION.md](CRYPTO_LAKE_INTEGRATION.md) | Crypto Lake 集成 |
| [CRYPTO_LAKE_QUICKSTART.md](CRYPTO_LAKE_QUICKSTART.md) | Crypto Lake 快速入门 |
| [ALTERNATIVE_DATA_SOURCES.md](ALTERNATIVE_DATA_SOURCES.md) | 替代数据源 |
| [check_tardis_coverage.md](check_tardis_coverage.md) | Tardis 覆盖检查 |

---

## 💰 **套利策略**

### DEX-CEX 套利
| 文档 | 说明 |
|------|------|
| [DEX_CEX_ARBITRAGE_STRATEGY.md](DEX_CEX_ARBITRAGE_STRATEGY.md) | DEX-CEX 套利策略 |
| [BASE_ARBITRAGE_GUIDE.md](BASE_ARBITRAGE_GUIDE.md) | Base 链套利指南 |
| [ARBITRAGE_DATA_STRATEGY.md](ARBITRAGE_DATA_STRATEGY.md) | 套利数据策略 |

### 评分和优化
| 文档 | 说明 |
|------|------|
| [FINAL_SCORING_RESULTS.md](FINAL_SCORING_RESULTS.md) | 最终评分结果 |
| [V4_VOLUME_THRESHOLD_OPTIMIZATION.md](V4_VOLUME_THRESHOLD_OPTIMIZATION.md) | V4 成交量阈值优化 |
| [QUICK_REFERENCE_TRADE_SIZE.md](QUICK_REFERENCE_TRADE_SIZE.md) | 交易规模快速参考 |

---

## 🗄️ **数据库**

| 文档 | 说明 |
|------|------|
| [MONGODB_POOL_STORAGE.md](MONGODB_POOL_STORAGE.md) | MongoDB 池子存储 |

---

## ☁️ **部署**

### AWS 部署
| 文档 | 说明 |
|------|------|
| [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md) | AWS 部署完整指南 |
| [AWS_QUICK_REFERENCE.md](AWS_QUICK_REFERENCE.md) | AWS 快速参考 |
| [AWS_STORAGE_CALCULATION.md](AWS_STORAGE_CALCULATION.md) | AWS 存储计算 |

---

## 🐛 **故障排除**

| 文档 | 说明 |
|------|------|
| [KNOWN_ISSUES.md](KNOWN_ISSUES.md) | 已知问题 |
| [BUGFIX_SUMMARY.md](BUGFIX_SUMMARY.md) | Bug 修复总结 |
| [TEST_RESULTS.md](TEST_RESULTS.md) | 测试结果 |

---

## 📝 **变更日志**

| 文档 | 说明 |
|------|------|
| [ORDERBOOK_UPDATE_ID_CHANGELOG.md](ORDERBOOK_UPDATE_ID_CHANGELOG.md) | Update ID 变更日志 |
| [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) | 更新总结 |

---

## 📂 **目录结构**

```
docs/
├── INDEX.md                              # 本索引文件
├── README.md                             # 文档总览
│
├── 📖 快速开始/
│   ├── QUICK_START_DATA_COLLECTION.md
│   ├── QUICK_START_32PAIRS.md
│   └── WORKFLOW_GUIDE.md
│
├── 🔧 订单簿采集/
│   ├── ORDERBOOK_COLLECTION_GUIDE.md
│   ├── START_ORDERBOOK_COLLECTION.md
│   ├── QUICKSTART_5S_ORDERBOOK.md
│   ├── HIGH_FREQUENCY_ORDERBOOK_SETUP.md
│   ├── ORDERBOOK_IMPLEMENTATION_EXPLAINED.md
│   ├── ORDERBOOK_SEQUENCE_NUMBER_EXPLAINED.md
│   ├── UPDATE_ID_DUPLICATE_EXPLAINED.md
│   ├── ORDERBOOK_UPDATE_ID_ANALYSIS.md
│   ├── LIQUIDITY_ANALYSIS_SUMMARY.md
│   ├── ORDERBOOK_DATA_PARTITIONING.md
│   ├── ORDERBOOK_TIMEZONE_EXPLAINED.md
│   ├── TIMEZONE_VISUAL_GUIDE.md
│   ├── ORDERBOOK_CLEANUP_GUIDE.md
│   ├── ORDERBOOK_5S_FIX.md
│   ├── ORDERBOOK_PRECISION_OPTIMIZATION.md
│   ├── DELAY_ANALYSIS.md
│   ├── ORDERBOOK_MONITORING_FIXED.md
│   ├── ORDERBOOK_SAMPLING_FREQUENCY_GUIDE.md
│   ├── ORDERBOOK_TASK_MANAGEMENT.md
│   ├── STOP_TASKS_QUICK_GUIDE.md
│   ├── MULTI_EXCHANGE_ORDERBOOK_SETUP.md
│   └── MULTI_EXCHANGE_SETUP_SUMMARY.md
│
├── 📊 数据采集/
│   ├── DATA_COLLECTION_GUIDE.md
│   ├── DATA_COLLECTION_FLOW.md
│   ├── DATA_STORAGE_STRATEGY.md
│   ├── GECKOTERMINAL_API_USAGE.md
│   ├── GECKOTERMINAL_API_REFERENCE.md
│   ├── geckoterminal_api.md
│   ├── GATEIO_API_RATE_LIMITS.md
│   ├── GATEIO_PUBLIC_API_VS_PRIVATE_API.md
│   ├── GATEIO_ORDERBOOK_STRUCTURE.md
│   ├── GATEIO_ORDERBOOK_SUMMARY.md
│   ├── API_KEY_ANSWER.md
│   ├── CRYPTO_LAKE_INTEGRATION.md
│   ├── CRYPTO_LAKE_QUICKSTART.md
│   ├── ALTERNATIVE_DATA_SOURCES.md
│   └── check_tardis_coverage.md
│
├── 💰 套利策略/
│   ├── DEX_CEX_ARBITRAGE_STRATEGY.md
│   ├── BASE_ARBITRAGE_GUIDE.md
│   ├── ARBITRAGE_DATA_STRATEGY.md
│   ├── FINAL_SCORING_RESULTS.md
│   ├── V4_VOLUME_THRESHOLD_OPTIMIZATION.md
│   └── QUICK_REFERENCE_TRADE_SIZE.md
│
├── 🗄️ 数据库/
│   └── MONGODB_POOL_STORAGE.md
│
├── ☁️ 部署/
│   ├── AWS_DEPLOYMENT_GUIDE.md
│   ├── AWS_QUICK_REFERENCE.md
│   └── AWS_STORAGE_CALCULATION.md
│
├── 🐛 故障排除/
│   ├── KNOWN_ISSUES.md
│   ├── BUGFIX_SUMMARY.md
│   └── TEST_RESULTS.md
│
└── 📝 变更日志/
    ├── ORDERBOOK_UPDATE_ID_CHANGELOG.md
    └── UPDATE_SUMMARY.md
```

---

## 🔍 **按主题查找**

### 🚀 我想开始使用 QuantsLab
→ [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
→ [QUICK_START_DATA_COLLECTION.md](QUICK_START_DATA_COLLECTION.md)

### 📊 我想采集订单簿数据
→ [ORDERBOOK_COLLECTION_GUIDE.md](ORDERBOOK_COLLECTION_GUIDE.md)
→ [START_ORDERBOOK_COLLECTION.md](START_ORDERBOOK_COLLECTION.md)
→ [QUICKSTART_5S_ORDERBOOK.md](QUICKSTART_5S_ORDERBOOK.md)

### 🔧 我遇到 Update ID 重复问题
→ [UPDATE_ID_DUPLICATE_EXPLAINED.md](UPDATE_ID_DUPLICATE_EXPLAINED.md)
→ [LIQUIDITY_ANALYSIS_SUMMARY.md](LIQUIDITY_ANALYSIS_SUMMARY.md)

### 💰 我想做 DEX-CEX 套利
→ [DEX_CEX_ARBITRAGE_STRATEGY.md](DEX_CEX_ARBITRAGE_STRATEGY.md)
→ [BASE_ARBITRAGE_GUIDE.md](BASE_ARBITRAGE_GUIDE.md)
→ [ARBITRAGE_DATA_STRATEGY.md](ARBITRAGE_DATA_STRATEGY.md)

### ☁️ 我想部署到 AWS
→ [AWS_DEPLOYMENT_GUIDE.md](AWS_DEPLOYMENT_GUIDE.md)
→ [AWS_QUICK_REFERENCE.md](AWS_QUICK_REFERENCE.md)

### 🐛 我遇到问题了
→ [KNOWN_ISSUES.md](KNOWN_ISSUES.md)
→ [BUGFIX_SUMMARY.md](BUGFIX_SUMMARY.md)

### 🛠️ 我想管理运行中的任务
→ [ORDERBOOK_TASK_MANAGEMENT.md](ORDERBOOK_TASK_MANAGEMENT.md)
→ [STOP_TASKS_QUICK_GUIDE.md](STOP_TASKS_QUICK_GUIDE.md)

---

## 📅 **文档更新时间**

本索引最后更新: 2025-11-17

---

## 💡 **贡献**

如果你创建了新的文档，请记得更新本索引文件！

---

**Happy Quanting! 🚀📈**

