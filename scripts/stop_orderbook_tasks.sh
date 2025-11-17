#!/bin/bash
# 停止订单簿采集任务

echo "🔍 查找正在运行的订单簿采集任务..."
echo ""

# 查找所有相关进程
PIDS=$(ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✅ 没有发现正在运行的订单簿采集任务"
    echo ""
    exit 0
fi

# 显示找到的进程
echo "📋 找到以下进程："
ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep | while read line; do
    PID=$(echo $line | awk '{print $2}')
    CMD=$(echo $line | awk '{for(i=11;i<=NF;i++) printf "%s ", $i; print ""}')
    echo "   PID $PID: $CMD"
done
echo ""

# 询问确认
read -p "❓ 是否停止这些任务？(y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 正在停止任务..."
    echo ""
    
    for PID in $PIDS; do
        # 先尝试优雅停止 (SIGTERM)
        echo "   • 停止 PID $PID (优雅关闭)..."
        kill $PID 2>/dev/null
        
        # 等待 3 秒
        sleep 3
        
        # 检查进程是否还在运行
        if ps -p $PID > /dev/null 2>&1; then
            echo "   • PID $PID 仍在运行，强制停止 (SIGKILL)..."
            kill -9 $PID 2>/dev/null
        fi
    done
    
    echo ""
    echo "✅ 所有任务已停止"
    echo ""
    
    # 再次检查
    echo "🔍 验证停止状态..."
    REMAINING=$(ps aux | grep -E "cli.py run-tasks.*orderbook_snapshot" | grep -v grep)
    
    if [ -z "$REMAINING" ]; then
        echo "✅ 确认：所有任务已停止"
    else
        echo "⚠️ 警告：以下进程仍在运行："
        echo "$REMAINING"
    fi
else
    echo "❌ 已取消"
fi

echo ""

