# 多机器部署监控指南

**目标**: 让多个数据收集程序（可能在不同机器上）的metrics都能在Grafana中显示

**更新时间**: 2025-11-22

---

## 🎯 解决方案概述

当前已实现：
- ✅ MEXC collector正在运行，metrics在8000端口可访问
- ✅ Metrics正在被记录（每个交易对的消息数、处理延迟等）
- ✅ Prometheus已配置为抓取多个端点
- ⚠️  Gate.io collector暂时未启动（可以用相同方式启动）

---

## 📊 当前架构

```
┌─────────────────┐      :8000     ┌──────────────┐      :9090      ┌─────────┐
│  MEXC Collector │◄────────────────│  Prometheus  │◄────────────────│ Grafana │
│   (Machine 1)   │    scrape       │   (Docker)   │    query        │ :3000   │
└─────────────────┘                 └──────────────┘                 └─────────┘
                                            ▲
                                            │ :8001
┌─────────────────┐                        │
│ Gate.io         │◄───────────────────────┘
│ Collector       │    scrape
│ (Machine 1/2)   │
└─────────────────┘
```

---

## ✅ 当前工作状态

### MEXC Collector (端口8000)
```bash
# 查看metrics
curl http://localhost:8000/metrics | grep mexc

# 示例输出：
orderbook_collector_messages_received_total{exchange="mexc",message_type="diff",symbol="IRON-USDT"} 1116.0
orderbook_collector_messages_received_total{exchange="mexc",message_type="diff",symbol="AUKI-USDT"} 951.0
...
```

**进程信息**:
- PID: 6328
- 命令: `python cli.py serve --config config/orderbook_tick_mexc_websocket.yml --host 0.0.0.0 --port 8000`
- 状态: ✅ 运行正常，正在采集数据
- Metrics端点: http://localhost:8000/metrics

---

## 🔧 启动新的Collector

### 方案1: 同一台机器上运行多个Collector（使用不同端口）

```bash
# Gate.io collector (端口8002)
nohup python cli.py serve \
  --config config/orderbook_tick_gateio.yml \
  --host 0.0.0.0 \
  --port 8002 \
  > /tmp/gateio_collector.log 2>&1 &

# Binance collector (端口8003)
nohup python cli.py serve \
  --config config/orderbook_tick_binance.yml \
  --host 0.0.0.0 \
  --port 8003 \
  > /tmp/binance_collector.log 2>&1 &
```

### 方案2: 不同机器上运行Collector（推荐用于生产环境）

**Machine 1** (192.168.1.10):
```bash
# MEXC collector
python cli.py serve \
  --config config/orderbook_tick_mexc_websocket.yml \
  --host 0.0.0.0 \
  --port 8000
```

**Machine 2** (192.168.1.11):
```bash
# Gate.io collector
python cli.py serve \
  --config config/orderbook_tick_gateio.yml \
  --host 0.0.0.0 \
  --port 8000
```

**Machine 3** (192.168.1.12):
```bash
# Binance collector
python cli.py serve \
  --config config/orderbook_tick_binance.yml \
  --host 0.0.0.0 \
  --port 8000
```

---

## 📝 更新Prometheus配置

编辑 `config/prometheus/prometheus_multiport.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # 本地MEXC collector
  - job_name: 'orderbook-collector-mexc'
    static_configs:
      - targets: ['host.docker.internal:8000']
        labels:
          collector: 'mexc'
          machine: 'local'
          
  # 本地Gate.io collector
  - job_name: 'orderbook-collector-gateio'
    static_configs:
      - targets: ['host.docker.internal:8002']
        labels:
          collector: 'gateio'
          machine: 'local'
          
  # 远程机器上的collectors
  - job_name: 'orderbook-collector-remote'
    static_configs:
      - targets: 
          - '192.168.1.10:8000'  # Machine 1 MEXC
          - '192.168.1.11:8000'  # Machine 2 Gate.io
          - '192.168.1.12:8000'  # Machine 3 Binance
        labels:
          environment: 'production'
```

重启Prometheus:
```bash
docker-compose -f docker-compose.monitoring.yml restart prometheus
```

---

## 🔍 验证配置

### 1. 检查Collector是否运行

```bash
# 检查进程
ps aux | grep "cli.py serve" | grep -v grep

# 检查端口
lsof -i :8000
lsof -i :8002
lsof -i :8003
```

### 2. 测试Metrics端点

```bash
# MEXC
curl http://localhost:8000/metrics | grep orderbook_collector

# Gate.io
curl http://localhost:8002/metrics | grep orderbook_collector

# 远程机器
curl http://192.168.1.10:8000/metrics | grep orderbook_collector
```

### 3. 检查Prometheus Targets

访问: http://localhost:9090/targets

应该看到所有配置的targets，状态为"UP"。

### 4. 在Grafana中查询

打开Grafana Dashboard: http://localhost:3000

使用PromQL查询:
```promql
# 所有exchangeの消息总数
sum by (exchange) (orderbook_collector_messages_received_total)

# 特定exchange的消息速率
rate(orderbook_collector_messages_received_total{exchange="mexc"}[5m])
```

---

## 🎯 当前可用的Metrics

MEXC collector当前正在导出以下metrics：

### 消息统计
- `orderbook_collector_messages_received_total` - 接收的消息总数
- `orderbook_collector_messages_processed_total` - 处理的消息总数
- `orderbook_collector_messages_failed_total` - 失败的消息总数

### 序列监控
- `orderbook_collector_sequence_gaps_total` - 序列号间隙数量

### 数据写入
- `orderbook_collector_ticks_written_total` - 写入的tick总数
- `orderbook_collector_files_written_total` - 写入的文件数

### 延迟监控
- `orderbook_collector_message_processing_latency` - 消息处理延迟

### 连接状态
- `orderbook_collector_connection_status` - 连接状态
- `orderbook_collector_last_message_timestamp` - 最后消息时间戳

---

## 💡 最佳实践

### 1. 端口分配规范

建议使用以下端口分配策略：

**同一机器**:
- 8000: MEXC
- 8001: Gate.io (预留)
- 8002: Binance
- 8003: Bybit
- 8004-8099: 其他exchanges

**不同机器**:
- 每台机器使用统一端口8000
- 通过机器IP区分不同的collectors

### 2. 防火墙配置

确保Prometheus服务器能访问collector的metrics端口：

```bash
# 在collector机器上开放端口
sudo ufw allow 8000/tcp
sudo firewall-cmd --add-port=8000/tcp --permanent
```

### 3. 监控Collector健康状态

在Prometheus中设置告警规则：

```yaml
groups:
  - name: collector_health
    rules:
      - alert: CollectorDown
        expr: up{job=~"orderbook-collector-.*"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Collector {{ $labels.instance }} is down"
```

### 4. 日志管理

使用统一的日志目录：

```bash
# 本地日志
/tmp/gateio_collector.log
/tmp/mexc_collector.log

# 生产环境日志
/var/log/quants-lab/gateio_collector.log
/var/log/quants-lab/mexc_collector.log
```

### 5. 进程管理

生产环境建议使用supervisor或systemd管理collector进程：

**Systemd示例** (`/etc/systemd/system/mexc-collector.service`):
```ini
[Unit]
Description=MEXC Orderbook Collector
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/path/to/quants-lab
ExecStart=/path/to/python cli.py serve --config config/orderbook_tick_mexc_websocket.yml --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl enable mexc-collector
sudo systemctl start mexc-collector
sudo systemctl status mexc-collector
```

---

## 🚀 快速启动脚本

保存为 `scripts/start_all_collectors.sh`:

```bash
#!/bin/bash

# MEXC (端口8000)
nohup python cli.py serve \
  --config config/orderbook_tick_mexc_websocket.yml \
  --host 0.0.0.0 --port 8000 \
  > /tmp/mexc_collector.log 2>&1 &
echo "MEXC started (PID: $!)"

# Gate.io (端口8002)
nohup python cli.py serve \
  --config config/orderbook_tick_gateio.yml \
  --host 0.0.0.0 --port 8002 \
  > /tmp/gateio_collector.log 2>&1 &
echo "Gate.io started (PID: $!)"

# 等待启动
sleep 10

# 验证
echo ""
echo "Checking collectors..."
curl -s http://localhost:8000/health
curl -s http://localhost:8002/health
```

---

## 📊 当前系统状态

**截至 2025-11-22 23:50**:

| Collector | 端口 | 状态 | Metrics | 交易对数 |
|-----------|------|------|---------|----------|
| MEXC      | 8000 | ✅ 运行中 | ✅ 可用 | 6 |
| Gate.io   | -    | ⏸️ 未启动 | - | - |

**下一步**:
1. ✅ MEXC metrics正常导出
2. ⏳ 启动Gate.io collector在另一个端口
3. ⏳ 验证Grafana可以显示两个collectors的数据

---

## 🐛 故障排查

### 问题1: Metrics端点返回空

**症状**: `curl http://localhost:8000/metrics` 没有数据

**解决**:
```bash
# 1. 检查collector是否正在采集数据
tail -f /tmp/mexc_collector.log | grep "Metrics recorded"

# 2. 等待更长时间（至少30秒）让collector建立连接和接收数据

# 3. 检查配置文件中的交易对是否正确
```

### 问题2: Prometheus无法抓取metrics

**症状**: Prometheus targets显示"DOWN"

**解决**:
```bash
# 1. 检查网络连接
ping host.docker.internal

# 2. 检查防火墙
sudo ufw status

# 3. 测试从Prometheus容器内部访问
docker exec -it quants-lab-prometheus wget -O- http://host.docker.internal:8000/metrics
```

### 问题3: Grafana看不到数据

**症状**: Dashboard显示"No Data"

**解决**:
```bash
# 1. 检查Prometheus是否有数据
# 访问: http://localhost:9090/graph
# 查询: orderbook_collector_messages_received_total

# 2. 检查Grafana数据源配置
# Settings -> Data Sources -> Prometheus
# URL应该是: http://prometheus:9090

# 3. 刷新Dashboard或等待15秒（scrape interval）
```

---

## 📞 支持

如有问题，请查看：
- Prometheus logs: `docker logs quants-lab-prometheus`
- Grafana logs: `docker logs quants-lab-grafana`
- Collector logs: `/tmp/*_collector.log`

---

**文档维护**: Alice
**最后更新**: 2025-11-22

