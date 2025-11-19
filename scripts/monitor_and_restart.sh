#!/bin/bash
# 监控容器状态，异常时自动重启

IMAGE_NAME="hummingbot/quants-lab"
CONFIG="config/orderbook_snapshot_gateio.yml"
CHECK_INTERVAL=60  # 检查间隔（秒）
MAX_RESTARTS=5     # 最大重启次数（连续）
RESTART_COUNT=0
LOG_DIR="logs/crash_logs"

# 创建日志目录
mkdir -p $LOG_DIR

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║        🔄 Docker 容器监控和自动重启服务                    ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "配置信息:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  镜像名称: $IMAGE_NAME"
echo "  配置文件: $CONFIG"
echo "  检查间隔: ${CHECK_INTERVAL}秒"
echo "  最大重启: ${MAX_RESTARTS}次"
echo "  日志目录: $LOG_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "按 Ctrl+C 停止监控"
echo ""

# 捕获 Ctrl+C
trap 'echo ""; echo "🛑 监控服务已停止"; exit 0' INT TERM

while true; do
    # 检查容器是否运行
    CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME)
    
    if [ -z "$CONTAINER_ID" ]; then
        echo "⚠️  [$(date '+%Y-%m-%d %H:%M:%S')] 容器未运行"
        
        # 查找最近停止的容器
        LAST_CONTAINER=$(docker ps -aq --filter ancestor=$IMAGE_NAME --latest)
        
        if [ -n "$LAST_CONTAINER" ]; then
            # 记录退出代码
            EXIT_CODE=$(docker inspect $LAST_CONTAINER --format='{{.State.ExitCode}}' 2>/dev/null || echo "unknown")
            echo "   退出代码: $EXIT_CODE"
            
            # 保存错误日志
            LOG_FILE="$LOG_DIR/crash_$(date +%Y%m%d_%H%M%S)_exit${EXIT_CODE}.log"
            docker logs $LAST_CONTAINER > "$LOG_FILE" 2>&1
            echo "   错误日志已保存: $LOG_FILE"
            
            # 分析错误类型
            if grep -qi "mongodb" "$LOG_FILE"; then
                echo "   🔍 检测到 MongoDB 相关错误"
            fi
            if grep -qi "memory\|oom" "$LOG_FILE"; then
                echo "   🔍 检测到内存相关错误"
            fi
            if grep -qi "connection\|timeout" "$LOG_FILE"; then
                echo "   🔍 检测到网络连接错误"
            fi
        fi
        
        # 检查重启次数
        if [ $RESTART_COUNT -ge $MAX_RESTARTS ]; then
            echo ""
            echo "╔════════════════════════════════════════════════════════════╗"
            echo "║                                                            ║"
            echo "║   ❌ 已达到最大重启次数 ($MAX_RESTARTS)                    ║"
            echo "║                                                            ║"
            echo "║   监控服务已停止，请手动检查问题！                          ║"
            echo "║                                                            ║"
            echo "╚════════════════════════════════════════════════════════════╝"
            echo ""
            echo "💡 建议操作:"
            echo "   1. 查看错误日志: ls -lht $LOG_DIR"
            echo "   2. 运行健康检查: ./scripts/check_docker_health.sh"
            echo "   3. 检查系统资源: docker stats"
            echo ""
            exit 1
        fi
        
        # 重启容器
        RESTART_COUNT=$((RESTART_COUNT + 1))
        echo ""
        echo "🔄 尝试重启容器 (第 ${RESTART_COUNT}/${MAX_RESTARTS} 次)"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # 重启前等待一下，避免快速失败
        if [ $RESTART_COUNT -gt 1 ]; then
            WAIT_TIME=$((RESTART_COUNT * 10))
            echo "   等待 ${WAIT_TIME}秒后重启..."
            sleep $WAIT_TIME
        fi
        
        make run-tasks config=$CONFIG > /dev/null 2>&1
        
        # 等待容器启动
        echo "   等待容器启动..."
        sleep 10
        
        # 验证启动成功
        NEW_CONTAINER=$(docker ps -q --filter ancestor=$IMAGE_NAME)
        if [ -n "$NEW_CONTAINER" ]; then
            echo "✅ 容器重启成功: $NEW_CONTAINER"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        else
            echo "❌ 容器重启失败"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
        echo ""
    else
        # 容器正常运行
        if [ $RESTART_COUNT -gt 0 ]; then
            echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 容器恢复正常运行 (ID: $CONTAINER_ID)"
            echo "   重置重启计数器"
            echo ""
            RESTART_COUNT=0
        fi
        
        # 检查数据文件更新（可选）
        LATEST_FILE=$(ls -t app/data/raw/orderbook_snapshots/*.parquet 2>/dev/null | head -1)
        if [ -n "$LATEST_FILE" ]; then
            FILE_AGE=$(( $(date +%s) - $(stat -f %m "$LATEST_FILE" 2>/dev/null || stat -c %Y "$LATEST_FILE" 2>/dev/null || echo 0) ))
            if [ $FILE_AGE -gt 120 ]; then
                echo "⚠️  [$(date '+%Y-%m-%d %H:%M:%S')] 数据文件超过 2 分钟未更新 (${FILE_AGE}秒)"
                echo "   容器可能已挂起，考虑重启"
            fi
        fi
    fi
    
    # 等待下次检查
    sleep $CHECK_INTERVAL
done

