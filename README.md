# QuantsLab - CEX-DEX 跨交易所套利系统 🚀

QuantsLab 是一个专业的加密货币量化交易研究框架，专注于 **CEX-DEX 跨交易所套利**和**高频订单簿数据采集**。

## 🎯 **项目解决的核心问题**

### **1. CEX-DEX 套利机会识别** 💰
- ✅ 实时监控 CEX（Gate.io, MEXC）和 DEX（Uniswap, Aerodrome）价差
- ✅ 自动筛选和排名套利机会
- ✅ 考虑流动性、滑点和手续费的真实利润计算
- ✅ 支持 Base、BSC、Solana 等多链 DEX

### **2. 高频订单簿数据采集** 📊
- ✅ 5秒间隔的实时订单簿快照（100档深度）
- ✅ 多交易所支持（Gate.io, MEXC）
- ✅ 数据完整性验证（sequence number 追踪）
- ✅ 自动数据分区和清理
- ✅ 流动性实时监控和分析

### **3. 最优交易规模计算** 📈
- ✅ 基于订单簿深度的滑点计算
- ✅ 综合考虑 CEX 和 DEX 的流动性
- ✅ 最大化净利润的交易规模优化
- ✅ 批量分析多个交易对

### **4. 数据采集和管理** 🗄️
- ✅ 自动化数据采集任务调度
- ✅ 增量更新和智能缓存
- ✅ Parquet 高性能存储
- ✅ 数据质量监控和验证

### **5. 实时监控和告警** 📊 **NEW!**
- ✅ Prometheus + Grafana 完整监控栈
- ✅ 20+ 自定义监控指标（消息率、延迟、buffer状态）
- ✅ 实时可视化Dashboard（交易所、交易对级别）
- ✅ Alertmanager 多级告警系统
- ✅ 支持多机器分布式部署监控

### **6. 云部署支持** ☁️
- ✅ AWS EC2 一键部署脚本
- ✅ systemd 服务管理
- ✅ CloudWatch 监控集成
- ✅ 自动化备份和清理

---

## 📚 **文档结构**

### **核心文档**

#### **快速开始**
- [WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) - 完整工作流程指南
- [QUICK_START_DATA_COLLECTION.md](docs/QUICK_START_DATA_COLLECTION.md) - 数据采集快速入门
- [QUICK_START_32PAIRS.md](docs/QUICK_START_32PAIRS.md) - 32 个交易对快速分析

#### **订单簿采集系统**
- [ORDERBOOK_COLLECTION_GUIDE.md](docs/ORDERBOOK_COLLECTION_GUIDE.md) - 订单簿采集完整指南
- [QUICKSTART_5S_ORDERBOOK.md](docs/QUICKSTART_5S_ORDERBOOK.md) - 5 秒高频采集快速入门
- [HIGH_FREQUENCY_ORDERBOOK_SETUP.md](docs/HIGH_FREQUENCY_ORDERBOOK_SETUP.md) - 高频采集详细设置
- [ORDERBOOK_UPDATE_ID_ANALYSIS.md](docs/ORDERBOOK_UPDATE_ID_ANALYSIS.md) - Update ID 和流动性分析
- [LIQUIDITY_ANALYSIS_SUMMARY.md](docs/LIQUIDITY_ANALYSIS_SUMMARY.md) - 流动性分析总结

#### **监控和告警系统** 📊 **NEW!**
- [SPRINT4_MONITORING_AND_ANALYSIS.md](docs/SPRINT4_MONITORING_AND_ANALYSIS.md) - 监控系统完整指南
- [MULTI_MACHINE_MONITORING_GUIDE.md](docs/MULTI_MACHINE_MONITORING_GUIDE.md) - 多机器部署指南
- [TROUBLESHOOTING_MONITORING.md](docs/TROUBLESHOOTING_MONITORING.md) - 故障排查手册

#### **套利策略**
- [DEX_CEX_ARBITRAGE_STRATEGY.md](docs/DEX_CEX_ARBITRAGE_STRATEGY.md) - DEX-CEX 套利策略
- [BASE_ARBITRAGE_GUIDE.md](docs/BASE_ARBITRAGE_GUIDE.md) - Base 链套利指南
- [ARBITRAGE_DATA_STRATEGY.md](docs/ARBITRAGE_DATA_STRATEGY.md) - 套利数据策略
- [QUICK_REFERENCE_TRADE_SIZE.md](docs/QUICK_REFERENCE_TRADE_SIZE.md) - 交易规模快速参考

#### **数据采集**
- [DATA_COLLECTION_GUIDE.md](docs/DATA_COLLECTION_GUIDE.md) - 数据采集完整指南
- [GECKOTERMINAL_API_USAGE.md](docs/GECKOTERMINAL_API_USAGE.md) - GeckoTerminal API 使用
- [GATEIO_API_RATE_LIMITS.md](docs/GATEIO_API_RATE_LIMITS.md) - Gate.io API 限流说明

#### **AWS 部署**
- [AWS_DEPLOYMENT_GUIDE.md](docs/AWS_DEPLOYMENT_GUIDE.md) - AWS 部署完整指南
- [AWS_QUICK_REFERENCE.md](docs/AWS_QUICK_REFERENCE.md) - AWS 快速参考
- [AWS_STORAGE_CALCULATION.md](docs/AWS_STORAGE_CALCULATION.md) - AWS 存储计算

**完整文档索引**: [docs/INDEX.md](docs/INDEX.md)

---

## 🛠️ **主要脚本**

### **数据采集**
```bash
# 完整 CEX-DEX 套利分析流程
bash scripts/run_complete_analysis.sh

# 导入 Freqtrade CEX 数据
python scripts/import_freqtrade_data.py --config config/gateio_USDT_downloader_full.yml --days 7

# 下载 DEX 数据
python scripts/download_dex_ohlcv.py --network base --days 3

# 构建 CEX-DEX 池子映射
python scripts/build_pool_mapping.py --connector gate_io --network base
```

### **订单簿采集**
```bash
# 启动订单簿采集（Gate.io）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 检查实时采集状态
python scripts/check_realtime_orderbook.py

# 分析流动性
python scripts/monitor_orderbook_liquidity.py

# 管理任务
bash scripts/status_orderbook_tasks.sh      # 查看状态
bash scripts/stop_all_orderbook.sh         # 停止所有任务
bash scripts/restart_orderbook_gateio.sh   # 重启任务
```

### **监控系统** 📊 **NEW!**
```bash
# 启动完整监控栈（Prometheus + Grafana + Alertmanager）
docker-compose -f docker-compose.monitoring.yml up -d

# 启动多个数据collectors
bash scripts/start_both_collectors.sh

# 访问监控面板
open http://localhost:3000          # Grafana Dashboard
open http://localhost:9090          # Prometheus
open http://localhost:9093          # Alertmanager

# 快速健康检查
bash scripts/quick_check_monitoring.sh

# 查看实时metrics
curl http://localhost:8001/metrics  # MEXC collector
curl http://localhost:8002/metrics  # Gate.io collector
```

### **套利分析**
```bash
# 分析所有交易对的价差
python scripts/analyze_cex_dex_spread.py --compare-all

# 计算最优交易规模
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io

# 批量优化交易规模
python scripts/batch_optimize_trade_size.py --config config/base_ecosystem_downloader_full.yml
```

### **AWS 部署**
```bash
# 本地到 AWS 一键部署
bash scripts/deploy_to_aws.sh
```

**完整脚本索引**: [scripts/README.md](scripts/README.md)

---

## 🚀 **快速开始**

### **1. 安装**

```bash
# 克隆仓库
git clone https://github.com/your-username/quants-lab.git
cd quants-lab

# 创建 Conda 环境
conda env create -f environment.yml
conda activate quants-lab

# 安装包
pip install -e .
```

### **2. CEX 数据采集**

```bash
# 下载 Gate.io 历史数据（7天，1分钟K线）
python scripts/import_freqtrade_data.py \
  --config config/gateio_USDT_downloader_full.yml \
  --days 7
```

### **3. DEX 数据采集**

```bash
# 构建 CEX-DEX 池子映射
python scripts/build_pool_mapping.py --connector gate_io --network base

# 下载 DEX 数据
python scripts/download_dex_ohlcv.py --network base --days 3
```

### **4. 套利分析**

```bash
# 分析价差并生成排名
python scripts/analyze_cex_dex_spread.py --compare-all

# 查看结果
cat app/data/processed/spread_analysis/*.csv
```

### **5. 订单簿采集（可选）**

```bash
# 启动 5 秒高频订单簿采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 监控采集状态
python scripts/check_realtime_orderbook.py
```

---

## 📊 **数据目录结构**

```
app/data/
├── cache/
│   └── candles/                    # 缓存的 OHLCV 数据
│       ├── gate_io|VIRTUAL-USDT|1m.parquet
│       └── geckoterminal_base|VIRTUAL-USDT|1m.parquet
│
├── processed/
│   ├── spread_analysis/            # 价差分析结果
│   ├── pool_mapping/              # CEX-DEX 池子映射
│   └── plots/                     # 可视化图表
│
└── raw/
    └── orderbook_snapshots/       # 订单簿快照（按日期分区）
        ├── gate_io_VIRTUAL-USDT_20251117.parquet
        └── mexc_AUKI-USDT_20251117.parquet
```

---

## 🎯 **使用场景**

### **场景 1：发现套利机会**

```bash
# 1. 采集数据
bash scripts/run_complete_analysis.sh

# 2. 查看排名
python scripts/analyze_cex_dex_spread.py --compare-all

# 3. 输出示例
# ⭐⭐⭐⭐⭐ VIRTUAL-USDT    价差: 1.5%  可执行: 85%  评分: 95
# ⭐⭐⭐⭐   BNKR-USDT      价差: 1.2%  可执行: 78%  评分: 82
```

### **场景 2：计算最优交易量**

```bash
# 计算 VIRTUAL-USDT 的最优交易规模
python scripts/calculate_optimal_trade_size.py VIRTUAL-USDT 1.5 --connector gate_io

# 输出示例
# 最优交易规模: $500 USD
# 预期净利润: $7.25 (1.45%)
# CEX 滑点: 0.05%
# DEX 滑点: 0.12%
```

### **场景 3：高频数据采集**

```bash
# 启动 5 秒订单簿采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml &

# 实时监控
watch -n 5 'python scripts/check_realtime_orderbook.py | tail -20'
```

### **场景 4：监控系统** 📊 **NEW!**

```bash
# 1. 启动监控栈
docker-compose -f docker-compose.monitoring.yml up -d

# 2. 启动collectors
bash scripts/start_both_collectors.sh

# 3. 访问Grafana Dashboard
# URL: http://localhost:3000
# 用户名: admin
# 密码: admin123

# 4. 查看实时指标
# - 消息接收率
# - 处理延迟
# - Buffer状态
# - 连接状态
# - 系统资源使用

# 5. 配置告警
# 编辑 config/alert_rules.yml
# 重启Prometheus: docker-compose restart prometheus
```

### **场景 5：部署到 AWS**

```bash
# 一键部署
bash scripts/deploy_to_aws.sh

# 输入你的 AWS 信息
# EC2 IP: 3.xxx.xxx.xxx
# SSH Key: ~/.ssh/your-key.pem
# 自动完成：上传代码、安装依赖、配置服务
```

---

## 🏗️ **项目架构**

```
quants-lab/
├── 📖 docs/                        # 文档（55个）
│   ├── INDEX.md                   # 文档索引
│   ├── 订单簿采集/
│   ├── 套利策略/
│   ├── 数据采集/
│   └── AWS 部署/
│
├── 🛠️ scripts/                     # 脚本（36个）
│   ├── README.md                  # 脚本索引
│   ├── 数据采集/
│   ├── 订单簿采集/
│   ├── 套利分析/
│   └── AWS 部署/
│
├── ⚙️ config/                      # 配置文件
│   ├── orderbook_snapshot_gateio.yml
│   ├── gateio_USDT_downloader_full.yml
│   └── ...
│
├── 🏗️ core/                       # 核心框架
│   ├── data_sources/             # 数据源（CLOB, GeckoTerminal）
│   ├── data_structures/          # 数据结构
│   ├── tasks/                    # 任务系统
│   └── backtesting/              # 回测引擎
│
├── 📱 app/                        # 应用层
│   ├── tasks/                    # 任务实现
│   │   └── data_collection/
│   │       └── orderbook_snapshot_task.py
│   ├── controllers/              # 交易策略
│   └── data/                     # 数据存储
│
└── 🚀 cli.py                     # 命令行工具
```

---

## 📈 **性能指标**

### **数据采集**
- ✅ CEX 数据: 1分钟K线，支持数千个交易对
- ✅ DEX 数据: 1分钟K线，自动池子映射
- ✅ 订单簿: 5秒快照，100档深度
- ✅ 存储效率: Parquet 压缩，节省 70% 空间

### **套利分析**
- ✅ 分析速度: 32个交易对 < 30秒
- ✅ 准确度: 考虑真实滑点和手续费
- ✅ 覆盖率: 支持多链多DEX

### **订单簿采集**
- ✅ 采集精度: 5.00 ± 0.03 秒
- ✅ 数据完整性: 99.8%（sequence number 验证）
- ✅ 并发控制: 8个并发连接（符合 API 限制）

### **监控系统** 📊 **NEW!**
- ✅ 指标采集: 20+ 自定义监控指标
- ✅ 数据刷新: 15秒间隔（可配置）
- ✅ Dashboard响应: < 1秒
- ✅ 告警延迟: < 30秒
- ✅ 数据保留: 30天（可配置）
- ✅ 支持规模: 100+ collectors同时监控

---

## 🐛 **故障排除**

查看 [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md)

---

## 🤝 **贡献**

欢迎提交 Issue 和 Pull Request！

---

## 📄 **许可证**

MIT License

---

## 📧 **联系方式**

- GitHub Issues: [提交问题](https://github.com/your-username/quants-lab/issues)
- 文档: [完整文档](docs/INDEX.md)

---

**Happy Quanting! 🚀📈**
