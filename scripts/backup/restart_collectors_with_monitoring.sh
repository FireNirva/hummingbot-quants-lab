#!/bin/bash
# 重启真实的collector，开启监控

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🔄 重启Collector (开启Prometheus监控)                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
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

# Step 3: 重启collector (后台运行)
echo "Step 3: 重启collectors (集成监控)..."
echo ""

# Gate.io collector
echo "   🚀 启动Gate.io collector..."
cd /Users/alice/Dropbox/投资/量化交易/quants-lab
nohup python cli.py run-tasks --config config/orderbook_tick_gateio.yml > /tmp/gateio_collector.log 2>&1 &
GATEIO_PID=$!
echo "      ✅ Gate.io PID: $GATEIO_PID"

sleep 2

# MEXC collector
echo "   🚀 启动MEXC collector..."
nohup python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml > /tmp/mexc_collector.log 2>&1 &
MEXC_PID=$!
echo "      ✅ MEXC PID: $MEXC_PID"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 4: 等待collectors初始化
echo "Step 4: 等待collectors初始化 (15秒)..."
for i in {15..1}; do
    echo -ne "   ⏳ $i秒...\r"
    sleep 1
done
echo "   ✅ 初始化完成        "
echo ""

# Step 5: 验证metrics端点
echo "Step 5: 验证metrics端点..."
if curl -s http://localhost:8000/metrics | grep -q "orderbook_collector"; then
    echo "   ✅ Metrics端点正常工作！"
    echo ""
    echo "   📊 采样数据："
    curl -s http://localhost:8000/metrics | grep "orderbook_collector_messages_received_total{" | head -3
else
    echo "   ⚠️  Metrics端点还没有数据，可能需要更多时间..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 6: 显示进程信息
echo "Step 6: 运行中的collector进程："
echo ""
ps aux | grep -E "(orderbook_tick.*yml)" | grep -v grep | awk '{print "   ✅ " $2 " - " $11 " " $12 " " $13 " " $14}'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ 所有collectors已重启并集成监控！"
echo ""
echo "🌐 访问地址："
echo "   • Metrics:    http://localhost:8000/metrics"
echo "   • Dashboard:  http://localhost:3000/d/orderbook-collection-v1/orderbook-collection-monitor"
echo "   • Prometheus: http://localhost:9090"
echo ""
echo "📊 查看实时日志："
echo "   • Gate.io:  tail -f /tmp/gateio_collector.log"
echo "   • MEXC:     tail -f /tmp/mexc_collector.log"
echo ""
echo "💡 提示："
echo "   - 等待30-60秒让数据开始流入"
echo "   - 刷新Grafana Dashboard查看真实数据"
echo "   - Dashboard会自动每5秒刷新"
echo ""

