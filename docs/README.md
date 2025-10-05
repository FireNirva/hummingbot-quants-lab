# 📚 QuantsLab 文档中心

欢迎来到 QuantsLab 文档中心！这里汇集了所有关键文档和指南。

---

## 🚀 快速开始

### 新手入门（按顺序阅读）

1. **[5分钟快速上手](./QUICK_START_DATA_COLLECTION.md)** ⭐️⭐️⭐️
   - 3步完成第一次数据下载
   - 包含实战示例和故障排查
   - **推荐从这里开始！**

2. **[数据收集完整指南](./DATA_COLLECTION_GUIDE.md)** ⭐️⭐️
   - 详细的系统架构说明
   - 所有数据收集任务类型详解
   - 配置文件编写教程
   - 最佳实践和常见问题

3. **[数据流程详解](./DATA_COLLECTION_FLOW.md)** ⭐️
   - 深入理解内部工作原理
   - 完整的执行流程图
   - 组件交互关系
   - 适合想要深入了解系统的用户

4. **[数据存储策略](./DATA_STORAGE_STRATEGY.md)**
   - 为什么 CLOB 数据用 Parquet 而不是 MongoDB
   - 数据存储架构设计
   - 最佳实践

5. **[已知问题和解决方案](./KNOWN_ISSUES.md)** 🐛
   - Pool Screener 费率匹配问题
   - 源码修改建议
   - 临时解决方案

---

## 📖 文档结构

```
docs/
├── README.md                           ← 你在这里
├── QUICK_START_DATA_COLLECTION.md     ← 🚀 快速上手（推荐起点）
├── DATA_COLLECTION_GUIDE.md           ← 📚 完整指南
├── DATA_COLLECTION_FLOW.md            ← 🔍 流程详解
├── DATA_STORAGE_STRATEGY.md           ← 💾 存储策略
├── KNOWN_ISSUES.md                    ← 🐛 已知问题
└── BASE_ARBITRAGE_GUIDE.md            ← 📊 Base 链套利指南
```

---

## 🎯 按需求查找

### 我想...

#### 快速开始使用
➡️ [5分钟快速上手](./QUICK_START_DATA_COLLECTION.md)

#### 了解有哪些数据源
➡️ [数据收集指南 - 第二章：数据收集任务类型](./DATA_COLLECTION_GUIDE.md#二数据收集任务类型详解)

#### 创建配置文件
➡️ [数据收集指南 - 第五章：如何创建配置](./DATA_COLLECTION_GUIDE.md#五如何创建数据收集配置)

#### 理解任务系统如何工作
➡️ [数据流程详解 - 完整流程图](./DATA_COLLECTION_FLOW.md#完整数据流程图)

#### 解决问题
➡️ [快速上手 - 故障排查](./QUICK_START_DATA_COLLECTION.md#故障排查)  
➡️ [数据收集指南 - 常见问题](./DATA_COLLECTION_GUIDE.md#七常见问题与最佳实践)  
➡️ [已知问题和解决方案](./KNOWN_ISSUES.md) 🆕

#### 查看示例配置
➡️ [数据收集指南 - 实战演练](./DATA_COLLECTION_GUIDE.md#六实战演练)  
➡️ `config/simple_btc_eth_downloader.yml`（项目根目录）

---

## 📝 配置文件示例

项目中提供了多个配置模板：

### 数据收集配置
- `config/template_1_candles_optimization.yml` - K线下载 + 优化流程
- `config/template_2_candles_pools_screener.yml` - K线 + 池子筛选
- `config/simple_btc_eth_downloader.yml` - 简单的 BTC/ETH 下载

### 专用配置
- `config/base_ecosystem_downloader_full.yml` - Base 生态系统
- `config/base_pools_production.yml` - Base 链池子筛选（生产） 🆕
- `config/sol_ecosystem_downloader_full.yml` - Solana 生态系统
- `config/gateio_USDT_downloader_full.yml` - Gate.io USDT 交易对

---

## 🛠️ 常用命令速查

```bash
# 快速测试
python cli.py run app.tasks.data_collection.simple_candles_downloader

# 使用配置运行
python cli.py trigger-task --task task_name --config config_file.yml

# 持续运行（按调度）
python cli.py run-tasks --config config_file.yml

# 列出任务
python cli.py list-tasks --config config_file.yml

# 验证配置
python cli.py validate-config --config config_file.yml

# 启动数据库
make run-db
```

---

## 🎓 学习路径

### 初学者 (第1-2天)
1. ✅ 阅读 [5分钟快速上手](./QUICK_START_DATA_COLLECTION.md)
2. ✅ 运行第一个数据下载任务
3. ✅ 在 Jupyter 中查看下载的数据
4. ✅ 尝试修改配置参数

### 进阶 (第3-7天)
1. ✅ 阅读 [数据收集完整指南](./DATA_COLLECTION_GUIDE.md)
2. ✅ 创建自定义配置文件
3. ✅ 设置定期自动下载
4. ✅ 尝试不同的数据源（DEX池子、资金费率等）

### 高级 (第2周+)
1. ✅ 阅读 [数据流程详解](./DATA_COLLECTION_FLOW.md)
2. ✅ 理解任务系统架构
3. ✅ 创建自定义数据收集任务
4. ✅ 集成到自动化交易流程

---

## 🔗 相关资源

### 项目文档
- [项目主 README](../README.md) - 项目总览和安装指南
- [研究 Notebooks](../research_notebooks/) - Jupyter 示例

### 核心代码
- [任务基类](../core/tasks/base.py) - BaseTask 实现
- [数据源](../core/data_sources/) - 所有数据源实现
- [数据收集任务](../app/tasks/data_collection/) - 具体任务实现

### 外部资源
- [Hummingbot 文档](https://docs.hummingbot.org/) - Hummingbot 官方文档
- [GeckoTerminal API](https://www.geckoterminal.com/dex-api) - DEX 数据 API

---

## 🤝 贡献

发现文档问题或有改进建议？欢迎：
- 提交 GitHub Issue
- 创建 Pull Request
- 在 Discord 社区讨论

---

## 📮 需要帮助？

1. **查看文档**: 先浏览上述文档
2. **搜索代码**: 使用 `grep` 或 IDE 搜索相关代码
3. **运行示例**: 尝试运行配置模板
4. **提问**: 在 GitHub Issues 中提问

---

**祝你使用愉快！Happy Coding! 🚀📊**

*Last updated: 2025-10-05*

