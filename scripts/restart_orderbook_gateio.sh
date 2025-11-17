#!/bin/bash
# 重启 Gate.io 订单簿采集服务
# 使用方法: bash scripts/restart_orderbook_gateio.sh

cd "$(dirname "$0")/.."

echo "=" * 80
echo "🔄 重启 Gate.io 订单簿采集服务"
echo "=" * 80
echo ""

# 1. 停止旧服务
echo "1️⃣ 停止旧服务..."
pkill -f "orderbook_snapshot_gateio" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ 已停止旧服务"
    sleep 2
else
    echo "   ℹ️ 没有正在运行的服务"
fi

echo ""

# 2. 清理旧数据（可选）
read -p "是否清理旧数据并重新开始？(y/N): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "2️⃣ 清理旧数据..."
    rm app/data/raw/orderbook_snapshots/gate_io_*.parquet 2>/dev/null
    echo "   ✅ 已清理旧数据"
    echo ""
else
    echo "2️⃣ 保留旧数据，继续追加"
    echo ""
fi

# 3. 启动新服务
echo "3️⃣ 启动新服务..."
echo "   配置: config/orderbook_snapshot_gateio.yml"
echo "   采集间隔: 5 秒"
echo "   交易对: 6 个"
echo ""

# 后台运行
nohup python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml \
  > logs/orderbook_gateio.log 2>&1 &

PID=$!

if [ $? -eq 0 ]; then
    echo "   ✅ 服务已启动 (PID: $PID)"
    echo ""
    
    # 等待几秒，确认服务正常运行
    sleep 3
    
    if ps -p $PID > /dev/null; then
        echo "   ✅ 服务运行正常"
    else
        echo "   ❌ 服务启动失败，请检查日志:"
        echo "      tail -f logs/orderbook_gateio.log"
        exit 1
    fi
else
    echo "   ❌ 服务启动失败"
    exit 1
fi

echo ""
echo "=" * 80
echo "✅ 重启完成"
echo "=" * 80
echo ""

# 显示监控提示
echo "💡 监控命令:"
echo "   • 查看日志: tail -f logs/orderbook_gateio.log"
echo "   • 实时监控: bash scripts/monitor_orderbook_simple.sh 10"
echo "   • 数据检查: python scripts/check_realtime_orderbook.py"
echo ""

# 显示停止命令
echo "🛑 停止服务:"
echo "   kill $PID"
echo "   或者: pkill -f orderbook_snapshot_gateio"
echo ""

echo "🎯 5 分钟后运行数据检查，验证采集间隔是否为 5-6 秒："
echo "   python scripts/check_realtime_orderbook.py | grep '平均间隔'"
echo ""

