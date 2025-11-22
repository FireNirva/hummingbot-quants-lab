#!/bin/bash
# 快速检查监控系统状态

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║          🔍 监控系统健康检查                                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 检查metrics端点
echo "1️⃣  检查Metrics端点..."
if curl -s http://localhost:8000/metrics > /dev/null 2>&1; then
    count=$(curl -s http://localhost:8000/metrics | grep -c "^orderbook_collector")
    echo "   ✅ Metrics端点正常 (发现 $count 个指标)"
else
    echo "   ❌ Metrics端点不可访问"
    echo "   💡 请运行: python scripts/test_prometheus_monitoring.py"
fi

echo ""

# 检查Prometheus
echo "2️⃣  检查Prometheus..."
if curl -s http://localhost:9090/-/healthy > /dev/null 2>&1; then
    echo "   ✅ Prometheus运行正常"
else
    echo "   ❌ Prometheus不可访问"
fi

echo ""

# 检查Grafana
echo "3️⃣  检查Grafana..."
if curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "   ✅ Grafana运行正常"
else
    echo "   ❌ Grafana不可访问"
fi

echo ""

# 检查Prometheus targets
echo "4️⃣  检查Prometheus Targets..."
target_status=$(curl -s http://localhost:9090/api/v1/targets 2>/dev/null | grep -o '"job":"orderbook-collector".*"health":"[^"]*"' | grep -o 'health":"[^"]*"' | cut -d'"' -f3)

if [ "$target_status" = "up" ]; then
    echo "   ✅ orderbook-collector target: UP"
elif [ "$target_status" = "down" ]; then
    echo "   ⚠️  orderbook-collector target: DOWN"
    echo "   💡 确保测试脚本正在运行"
else
    echo "   ⚠️  无法获取target状态"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 访问地址："
echo "   • Metrics:     http://localhost:8000/metrics"
echo "   • Prometheus:  http://localhost:9090"
echo "   • Grafana:     http://localhost:3000"
echo ""

# 检查是否所有都正常
if curl -s http://localhost:8000/metrics > /dev/null 2>&1 && \
   curl -s http://localhost:9090/-/healthy > /dev/null 2>&1 && \
   curl -s http://localhost:3000/api/health > /dev/null 2>&1; then
    echo "✅ 所有服务正常运行！"
    if [ "$target_status" = "up" ]; then
        echo "✅ 数据正在收集！"
        echo ""
        echo "👉 现在可以在Grafana中查看Dashboard了！"
    else
        echo "⚠️  测试脚本未运行，请启动："
        echo "   python scripts/test_prometheus_monitoring.py"
    fi
else
    echo "⚠️  部分服务未运行，请检查Docker容器状态"
fi

echo ""

