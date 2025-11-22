#!/bin/bash
# 重启collector，每个使用不同端口暴露metrics（支持多机器部署）

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🔄 重启Collector (多端口Prometheus监控)              ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 架构说明："
echo "   • Gate.io collector  → Metrics at :8000"
echo "   • MEXC collector     → Metrics at :8001"
echo "   • Prometheus抓取两个端点"
echo "   • 支持多机器部署（每台机器独立端口）"
echo ""

# Step 1: 停止测试脚本
echo "Step 1: 停止测试脚本..."
pkill -f test_prometheus_monitoring.py
sleep 2
echo "   ✅ 测试脚本已停止"
echo ""

# Step 2: 停止现有的collector
echo "Step 2: 停止现有的collector进程..."
pkill -f "orderbook_tick_gateio.yml"
pkill -f "orderbook_tick_mexc_websocket.yml"
sleep 3
echo "   ✅ 所有collector已停止"
echo ""

# Step 3: 重启collector (后台运行，不同端口)
echo "Step 3: 重启collectors (每个使用独立端口)..."
echo ""

# Gate.io collector - Port 8000
echo "   🚀 启动Gate.io collector (API: :8000)..."
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
nohup python cli.py serve --config config/orderbook_tick_gateio.yml --host 0.0.0.0 --port 8000 > /tmp/gateio_collector.log 2>&1 &
GATEIO_PID=$!
echo "      ✅ Gate.io PID: $GATEIO_PID"
echo "      ✅ Metrics: http://localhost:8000/metrics"

sleep 3

# MEXC collector - Port 8001
echo "   🚀 启动MEXC collector (API: :8001)..."
nohup python cli.py serve --config config/orderbook_tick_mexc_websocket.yml --host 0.0.0.0 --port 8001 > /tmp/mexc_collector.log 2>&1 &
MEXC_PID=$!
echo "      ✅ MEXC PID: $MEXC_PID"
echo "      ✅ Metrics: http://localhost:8001/metrics"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 4: 等待collectors初始化
echo "Step 4: 等待collectors初始化 (20秒)..."
for i in {20..1}; do
    echo -ne "   ⏳ $i秒...\r"
    sleep 1
done
echo "   ✅ 初始化完成        "
echo ""

# Step 5: 验证metrics端点
echo "Step 5: 验证metrics端点..."
echo ""

echo "   📊 Gate.io (端口8000):"
if curl -s http://localhost:8000/metrics | grep -q "orderbook_collector"; then
    echo "      ✅ Metrics正常！"
    GATEIO_COUNT=$(curl -s http://localhost:8000/metrics | grep "orderbook_collector_messages_received_total{exchange=\"gate_io\"" | wc -l | tr -d ' ')
    echo "      📈 指标数: $GATEIO_COUNT"
else
    echo "      ⚠️  Metrics还没有数据..."
fi

echo ""
echo "   📊 MEXC (端口8001):"
if curl -s http://localhost:8001/metrics | grep -q "orderbook_collector"; then
    echo "      ✅ Metrics正常！"
    MEXC_COUNT=$(curl -s http://localhost:8001/metrics | grep "orderbook_collector_messages_received_total{exchange=\"mexc\"" | wc -l | tr -d ' ')
    echo "      📈 指标数: $MEXC_COUNT"
else
    echo "      ⚠️  Metrics还没有数据..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 6: 更新Prometheus配置
echo "Step 6: 更新Prometheus配置..."

# 确保目录存在
mkdir -p config/prometheus

cat > config/prometheus/prometheus_multiport.yml << 'EOF'
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Gate.io Collector
  - job_name: 'orderbook-collector-gateio'
    static_configs:
      - targets: ['host.docker.internal:8000']
        labels:
          collector: 'gateio'
          instance: 'local'

  # MEXC Collector
  - job_name: 'orderbook-collector-mexc'
    static_configs:
      - targets: ['host.docker.internal:8001']
        labels:
          collector: 'mexc'
          instance: 'local'

  # Node Exporter (系统指标)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
EOF

echo "   ✅ Prometheus配置已更新: config/prometheus/prometheus_multiport.yml"
echo ""

# Step 7: 更新docker-compose使用新配置
echo "Step 7: 更新docker-compose配置..."

# 备份原配置
if [ ! -f docker-compose.monitoring.yml.bak ]; then
    cp docker-compose.monitoring.yml docker-compose.monitoring.yml.bak
fi

# 使用sed更新prometheus配置路径
sed -i '' 's|./config/prometheus.yml|./config/prometheus/prometheus_multiport.yml|g' docker-compose.monitoring.yml
echo "   ✅ docker-compose配置已更新"

# Step 8: 重启Prometheus
echo ""
echo "Step 8: 重启Prometheus容器..."
docker-compose -f docker-compose.monitoring.yml restart prometheus
sleep 5
echo "   ✅ Prometheus已重启"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 所有collectors已重启并集成监控！"
echo ""
echo "🌐 访问地址："
echo "   • Gate.io Metrics:  http://localhost:8000/metrics"
echo "   • MEXC Metrics:     http://localhost:8001/metrics"
echo "   • Prometheus:       http://localhost:9090"
echo "   • Grafana:          http://localhost:3000"
echo ""
echo "📊 查看实时日志："
echo "   • Gate.io:  tail -f /tmp/gateio_collector.log"
echo "   • MEXC:     tail -f /tmp/mexc_collector.log"
echo ""
echo "🔧 验证Prometheus targets："
echo "   open http://localhost:9090/targets"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 多机器部署说明："
echo "   1. 在每台机器上运行collector，使用不同端口"
echo "   2. 更新Prometheus配置，添加所有机器的IP:端口"
echo "   3. 例如："
echo "      Machine1: 192.168.1.10:8000 (Gate.io)"
echo "      Machine2: 192.168.1.11:8000 (MEXC)"
echo "      Machine3: 192.168.1.12:8000 (Binance)"
echo ""

