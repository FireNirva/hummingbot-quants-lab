# Changelog

All notable changes to QuantsLab will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Sprint 4 - Monitoring and Alerting System (2025-11-22)

#### Added
- **📊 Prometheus监控集成**
  - 添加了完整的Prometheus metrics导出功能
  - 实现了自定义监控指标(messages_received, messages_processed, buffer_size等)
  - 新增`/metrics`端点到FastAPI服务器
  - 添加了多端口配置支持,允许多个collector独立运行

- **📈 Grafana可视化Dashboard**
  - 创建了Orderbook Collection Monitor dashboard
  - 实时显示消息接收率、处理延迟、buffer状态
  - 支持按交易所、交易对过滤
  - 包含系统资源监控(CPU、内存、磁盘)

- **🔔 Alertmanager告警系统**
  - 实现了多级告警规则(warning/critical)
  - 监控WebSocket连接状态、数据延迟、buffer溢出
  - 支持邮件和Webhook通知
  - 告警分组和静默功能

- **🛠️ 监控相关脚本**
  - `scripts/start_both_collectors.sh` - 启动多个collectors
  - `scripts/quick_check_monitoring.sh` - 快速健康检查
  - `scripts/test_prometheus_monitoring.py` - 监控系统测试

- **📚 监控文档**
  - `docs/SPRINT4_MONITORING_AND_ANALYSIS.md` - Sprint 4完整文档
  - `docs/MULTI_MACHINE_MONITORING_GUIDE.md` - 多机器部署指南
  - `docs/TROUBLESHOOTING_MONITORING.md` - 故障排查手册

#### Changed
- **核心模块更新**
  - `core/tasks/api.py`: 添加了Prometheus metrics端点
  - `app/tasks/data_collection/orderbook_tick_collector.py`: 
    - 集成了完整的metrics记录
    - 添加了详细的性能监控指标
    - 改进了日志输出格式

- **配置文件优化**
  - 新增`config/prometheus/prometheus_multiport.yml` - 多端口Prometheus配置
  - 更新`docker-compose.monitoring.yml` - 完整监控栈配置
  - 添加`config/alert_rules.yml` - 告警规则配置
  - 添加`config/alertmanager.yml` - 告警路由配置

#### Deprecated
- `config/prometheus.yml` - 已移至`config/prometheus.yml.backup`(被prometheus_multiport.yml替代)
- `scripts/restart_collectors_with_monitoring.sh` - 已移至backup目录
- `scripts/restart_collectors_with_monitoring_multiport.sh` - 已移至backup目录

#### Technical Details
- **监控指标**
  - `orderbook_collector_messages_received_total` - 接收的消息总数
  - `orderbook_collector_messages_processed_total` - 处理的消息总数
  - `orderbook_collector_message_processing_latency` - 消息处理延迟
  - `orderbook_collector_buffer_size` - Buffer大小
  - `orderbook_collector_ticks_written_total` - 写入的tick总数
  - `orderbook_collector_files_written_total` - 写入的文件总数
  - `orderbook_collector_sequence_gaps_total` - Sequence gaps总数
  - `orderbook_collector_connection_status` - 连接状态
  - `orderbook_collector_data_freshness_seconds` - 数据新鲜度

- **部署架构**
  - 支持单机多端口部署(8001, 8002, 8003...)
  - 支持多机器分布式部署
  - Docker Compose orchestration
  - 自动化健康检查和重启

- **性能优化**
  - 异步metrics记录,不影响主流程性能
  - 智能buffer管理,减少I/O开销
  - 连接池复用,提高并发能力

#### Bug Fixes
- 修复了FastAPI `/metrics`端点缺失的问题
- 修复了Prometheus配置未正确加载的问题
- 修复了多个collectors同时运行时的端口冲突

#### Breaking Changes
无

#### Migration Guide
如果你正在使用旧的单collector配置:

1. **更新启动方式**:
   ```bash
   # 旧方式 (单个collector, 端口8000)
   python cli.py serve --config config/orderbook_tick_gateio.yml --port 8000
   
   # 新方式 (多个collectors, 不同端口)
   ./scripts/start_both_collectors.sh
   # 或手动指定端口
   python cli.py serve --config config/orderbook_tick_mexc_websocket.yml --port 8001 &
   python cli.py serve --config config/orderbook_tick_gateio.yml --port 8002 &
   ```

2. **更新Prometheus配置**:
   ```bash
   # 使用新的多端口配置
   docker-compose -f docker-compose.monitoring.yml down
   docker-compose -f docker-compose.monitoring.yml up -d
   ```

3. **验证监控系统**:
   ```bash
   # 检查Prometheus targets
   open http://localhost:9090/targets
   
   # 查看Grafana dashboard
   open http://localhost:3000
   ```

详细迁移步骤请参考: `docs/MULTI_MACHINE_MONITORING_GUIDE.md`

---

## [0.3.0] - Sprint 3 - MEXC WebSocket Tick Data Collection (2025-11-21)

### Added
- MEXC交易所的WebSocket tick级别订单簿数据采集
- Protobuf消息解析支持
- Tick-level数据存储(long-table格式)
- Multi-part文件写入策略

详细内容请参考Git历史记录。

---

## [0.2.0] - Sprint 2 - Gate.io Orderbook Snapshot Collection (2025-11-17)

### Added
- Gate.io订单簿快照采集
- 5秒高频采集
- Parquet存储格式
- 自动数据分区

---

## [0.1.0] - Sprint 1 - CEX-DEX Arbitrage System (2025-11-15)

### Added
- 基础CEX-DEX套利系统
- 多交易所数据采集
- 价差分析
- 最优交易规模计算

---

[Unreleased]: https://github.com/your-username/quants-lab/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/your-username/quants-lab/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/your-username/quants-lab/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/your-username/quants-lab/releases/tag/v0.1.0

