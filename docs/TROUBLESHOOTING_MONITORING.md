# 监控系统故障排查指南

## 问题1: Grafana看不到某个交易所的数据

### 症状
- MEXC数据可见，但Gate.io数据消失
- 或反之

### 诊断步骤

#### 1. 检查Collector进程
```bash
ps aux | grep "cli.py serve" | grep -v grep
```

**期望结果**: 应该看到所有collectors都在运行
```
alice  22802  python cli.py serve --config config/orderbook_tick_mexc_websocket.yml --host 0.0.0.0 --port 8001
alice  22842  python cli.py serve --config config/orderbook_tick_gateio.yml --host 0.0.0.0 --port 8002
```

#### 2. 检查端口
```bash
lsof -i :8001
lsof -i :8002
```

#### 3. 检查Metrics端点
```bash
# MEXC
curl -s http://localhost:8001/metrics | grep "orderbook_collector_messages_received_total" | wc -l

# Gate.io
curl -s http://localhost:8002/metrics | grep "orderbook_collector_messages_received_total" | wc -l
```

**期望结果**: 应该返回 >0 的数字

#### 4. 检查Prometheus Targets
```bash
curl -s http://localhost:9090/api/v1/targets | python3 -m json.tool
```

或访问: http://localhost:9090/targets

**期望结果**: 应该看到以下targets，状态都是UP:
- `orderbook-collector-mexc` → `http://host.docker.internal:8001/metrics`
- `orderbook-collector-gateio` → `http://host.docker.internal:8002/metrics`

#### 5. 验证Prometheus能查询数据
```bash
# Gate.io
curl -s -G http://localhost:9090/api/v1/query \
  --data-urlencode 'query=orderbook_collector_messages_received_total{exchange="gate_io"}' \
  | python3 -m json.tool

# MEXC
curl -s -G http://localhost:9090/api/v1/query \
  --data-urlencode 'query=orderbook_collector_messages_received_total{exchange="mexc"}' \
  | python3 -m json.tool
```

### 常见原因和解决方案

#### 原因1: Collector进程未启动
**解决方案**: 启动缺失的collector
```bash
# MEXC (端口8001)
python cli.py serve --config config/orderbook_tick_mexc_websocket.yml \
  --host 0.0.0.0 --port 8001 > /tmp/mexc_collector.log 2>&1 &

# Gate.io (端口8002)
python cli.py serve --config config/orderbook_tick_gateio.yml \
  --host 0.0.0.0 --port 8002 > /tmp/gateio_collector.log 2>&1 &
```

#### 原因2: Prometheus配置未更新
**症状**: Prometheus targets只显示8000端口

**解决方案**: 重启监控栈
```bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
docker-compose -f docker-compose.monitoring.yml down
docker-compose -f docker-compose.monitoring.yml up -d
```

**重要**: 修改Prometheus配置后，必须完全重启监控栈（`down`然后`up -d`），而不是仅仅`restart`。

#### 原因3: Prometheus还在抓取旧数据
**解决方案**: 等待30秒让Prometheus抓取新数据

#### 原因4: /metrics端点未实现
**症状**: curl返回 `{"detail":"Not Found"}`

**解决方案**: 确保`core/tasks/api.py`包含以下代码:
```python
from prometheus_client import REGISTRY, generate_latest
from fastapi.responses import PlainTextResponse

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(REGISTRY)
```

---

## 问题2: Grafana Dashboard显示"No Data"

### 诊断步骤

1. **检查时间范围**: 确保选择了正确的时间范围（如"Last 5 minutes"）
2. **刷新Dashboard**: 点击右上角的刷新按钮🔄
3. **检查Panel Query**: 编辑panel，查看PromQL查询是否正确
4. **在Prometheus中验证**: 直接在Prometheus Graph中测试查询

### 解决方案

#### 修复Panel查询
正确的查询示例：
```promql
# 消息接收率
rate(orderbook_collector_messages_received_total[1m])

# 按交易所分组
sum by(exchange) (rate(orderbook_collector_messages_received_total[1m]))

# 特定交易所
rate(orderbook_collector_messages_received_total{exchange="gate_io"}[1m])
```

#### 重新导入Dashboard
如果dashboard配置有问题，重新导入：
```bash
# 登录Grafana
# Dashboards → Import → Upload JSON file
# 选择: config/grafana/dashboards/orderbook-collection-dashboard.json
```

---

## 问题3: Docker容器无法启动

### 症状
```
Error: port is already allocated
```

### 解决方案
找到并停止占用端口的进程：
```bash
# 查找占用端口的进程
lsof -i :9090  # Prometheus
lsof -i :3000  # Grafana

# 停止进程
kill -9 <PID>
```

或使用不同的端口（修改`docker-compose.monitoring.yml`）。

---

## 问题4: Metrics数据为0或不增长

### 诊断步骤

1. **检查Collector日志**:
```bash
tail -f /tmp/mexc_collector.log | grep "✅ Metrics recorded"
tail -f /tmp/gateio_collector.log | grep "✅ Metrics recorded"
```

2. **检查WebSocket连接**:
```bash
tail -f /tmp/gateio_collector.log | grep "Connected"
```

3. **验证交易对配置**:
```bash
cat config/orderbook_tick_gateio.yml | grep -A 10 "pairs:"
```

### 常见原因

#### 原因1: WebSocket连接断开
**解决方案**: Collector会自动重连，等待1-2分钟

#### 原因2: 交易对配置错误
**解决方案**: 检查config文件中的交易对格式是否正确
- Gate.io: `VIRTUAL_USDT`（下划线）
- MEXC: `VIRTUALUSDT`（无分隔符）

#### 原因3: 交易量低
**解决方案**: 这是正常的。低流动性交易对可能几分钟才有一次更新。

---

## 快速恢复命令

### 完全重启监控系统
```bash
#!/bin/bash
cd /Users/alice/Dropbox/投资/量化交易/quants-lab

# 停止所有
pkill -f "cli.py serve"
docker-compose -f docker-compose.monitoring.yml down

# 重新启动
sleep 3

# 启动collectors
./scripts/start_both_collectors.sh

# 启动监控栈
docker-compose -f docker-compose.monitoring.yml up -d

# 等待初始化
sleep 30

echo "✅ 系统已重启"
echo "📊 验证: http://localhost:9090/targets"
echo "📈 Grafana: http://localhost:3000"
```

### 验证系统健康
```bash
#!/bin/bash

echo "=== Collectors ==="
ps aux | grep "cli.py serve" | grep -v grep | wc -l | awk '{print "Running: " $1 " collectors"}'

echo ""
echo "=== Ports ==="
lsof -i :8001 | grep LISTEN | awk '{print "8001 (MEXC): ✅"}'
lsof -i :8002 | grep LISTEN | awk '{print "8002 (Gate.io): ✅"}'

echo ""
echo "=== Prometheus Targets ==="
curl -s http://localhost:9090/api/v1/targets | python3 -c "
import json, sys
data = json.load(sys.stdin)
for t in data['data']['activeTargets']:
    job = t['labels']['job']
    health = t['health']
    emoji = '✅' if health == 'up' else '❌'
    print(f'{emoji} {job}: {health}')
"

echo ""
echo "=== Data Count ==="
curl -s -G http://localhost:9090/api/v1/query \
  --data-urlencode 'query=count(orderbook_collector_messages_received_total)' \
  | python3 -c "import json, sys; print(f\"Total metrics: {json.load(sys.stdin)['data']['result'][0]['value'][1]}\")"
```

---

## 联系和参考

- **完整文档**: `docs/MULTI_MACHINE_MONITORING_GUIDE.md`
- **配置文件**: 
  - `config/prometheus/prometheus_multiport.yml`
  - `docker-compose.monitoring.yml`
- **启动脚本**: `scripts/start_both_collectors.sh`

---

## 版本历史

- **2025-11-22**: 初始版本
  - 添加Prometheus配置未更新的故障排查
  - 添加/metrics端点故障排查
  - 添加完整重启脚本

