#!/bin/bash
# 启动MEXC和Gate.io两个collectors（多端口监控）
# 最后更新: 2025-11-22

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🚀 启动双Collector监控系统                           ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 停止现有collectors
echo "Step 1: 停止现有collectors..."
pkill -f "cli.py serve.*orderbook_tick"
sleep 3
echo "   ✅ 已停止"
echo ""

# 启动MEXC collector (端口8001)
echo "Step 2: 启动MEXC collector (端口8001)..."
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
nohup python cli.py serve \
  --config config/orderbook_tick_mexc_websocket.yml \
  --host 0.0.0.0 \
  --port 8001 \
  > /tmp/mexc_collector.log 2>&1 &
MEXC_PID=$!
echo "   ✅ MEXC PID: $MEXC_PID"
echo "   📊 Metrics: http://localhost:8001/metrics"
sleep 3

# 启动Gate.io collector (端口8002)
echo ""
echo "Step 3: 启动Gate.io collector (端口8002)..."
nohup python cli.py serve \
  --config config/orderbook_tick_gateio.yml \
  --host 0.0.0.0 \
  --port 8002 \
  > /tmp/gateio_collector.log 2>&1 &
GATEIO_PID=$!
echo "   ✅ Gate.io PID: $GATEIO_PID"
echo "   📊 Metrics: http://localhost:8002/metrics"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 等待初始化
echo "Step 4: 等待collectors初始化 (30秒)..."
for i in {30..1}; do
    echo -ne "   ⏳ $i秒...\r"
    sleep 1
done
echo "   ✅ 初始化完成        "
echo ""

# 验证metrics
echo "Step 5: 验证metrics端点..."
echo ""

echo "   📊 MEXC (8001):"
if curl -s http://localhost:8001/metrics | grep -q "orderbook_collector_messages_received_total{exchange=\"mexc\""; then
    MEXC_COUNT=$(curl -s http://localhost:8001/metrics | grep "orderbook_collector_messages_received_total{exchange=\"mexc\"" | wc -l | tr -d ' ')
    echo "      ✅ Metrics正常！找到 $MEXC_COUNT 个指标"
    curl -s http://localhost:8001/metrics | grep "orderbook_collector_messages_received_total{exchange=\"mexc\"" | head -2 | sed 's/^/      /'
else
    echo "      ⚠️  还没有数据，可能需要更多时间..."
fi

echo ""
echo "   📊 Gate.io (8002):"
if curl -s http://localhost:8002/metrics | grep -q "orderbook_collector_messages_received_total{exchange=\"gate_io\""; then
    GATEIO_COUNT=$(curl -s http://localhost:8002/metrics | grep "orderbook_collector_messages_received_total{exchange=\"gate_io\"" | wc -l | tr -d ' ')
    echo "      ✅ Metrics正常！找到 $GATEIO_COUNT 个指标"
    curl -s http://localhost:8002/metrics | grep "orderbook_collector_messages_received_total{exchange=\"gate_io\"" | head -2 | sed 's/^/      /'
else
    echo "      ⚠️  还没有数据，可能需要更多时间..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 双Collector系统启动完成！"
echo ""
echo "🌐 访问地址:"
echo "   • MEXC Metrics:     http://localhost:8001/metrics"
echo "   • Gate.io Metrics:  http://localhost:8002/metrics"
echo "   • Prometheus:       http://localhost:9090"
echo "   • Grafana:          http://localhost:3000"
echo ""
echo "📊 查看实时日志:"
echo "   • MEXC:    tail -f /tmp/mexc_collector.log | grep '✅ Metrics recorded'"
echo "   • Gate.io: tail -f /tmp/gateio_collector.log | grep '✅ Metrics recorded'"
echo ""
echo "🔧 验证Prometheus Targets:"
echo "   open http://localhost:9090/targets"
echo ""
echo "📄 文档:"
echo "   docs/MULTI_MACHINE_MONITORING_GUIDE.md"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

