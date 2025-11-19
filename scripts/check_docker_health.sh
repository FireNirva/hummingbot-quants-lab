#!/bin/bash
# 检查 Docker 容器健康状态

CONTAINER_NAME="quants-lab-orderbook"
IMAGE_NAME="hummingbot/quants-lab"

echo "================================"
echo "🔍 Docker 容器健康检查"
echo "================================"
echo ""

# 查找运行中的容器
CONTAINER_ID=$(docker ps -q --filter ancestor=$IMAGE_NAME)

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ 容器未运行"
    echo ""
    
    # 查找最近停止的容器
    LAST_CONTAINER=$(docker ps -aq --filter ancestor=$IMAGE_NAME --latest)
    
    if [ -n "$LAST_CONTAINER" ]; then
        echo "📋 最近停止的容器: $LAST_CONTAINER"
        echo ""
        
        # 查看退出代码
        EXIT_CODE=$(docker inspect $LAST_CONTAINER --format='{{.State.ExitCode}}')
        echo "退出代码: $EXIT_CODE"
        
        # 解释退出代码
        case $EXIT_CODE in
            0)
                echo "含义: 正常退出"
                ;;
            1)
                echo "含义: 应用错误"
                ;;
            137)
                echo "含义: 被 SIGKILL 杀死（可能是内存不足）"
                ;;
            139)
                echo "含义: 段错误"
                ;;
            143)
                echo "含义: 被 SIGTERM 终止（手动停止）"
                ;;
            *)
                echo "含义: 未知错误"
                ;;
        esac
        echo ""
        
        # 显示最后 50 行日志
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "📜 最后 50 行日志:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker logs --tail 50 $LAST_CONTAINER
        echo ""
        
        # 检查是否有错误关键词
        ERROR_COUNT=$(docker logs $LAST_CONTAINER 2>&1 | grep -i "error\|exception\|failed" | wc -l)
        echo "⚠️  发现 $ERROR_COUNT 个错误/异常信息"
        echo ""
        
        # 显示错误日志
        if [ $ERROR_COUNT -gt 0 ]; then
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "🚨 错误信息汇总:"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            docker logs $LAST_CONTAINER 2>&1 | grep -i "error\|exception\|failed" | tail -20
        fi
    else
        echo "❌ 未找到任何历史容器"
    fi
else
    echo "✅ 容器运行中: $CONTAINER_ID"
    echo ""
    
    # 显示容器信息
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 容器信息:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    docker ps --filter id=$CONTAINER_ID --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
    echo ""
    
    # 检查资源使用
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "💻 资源使用情况:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    docker stats $CONTAINER_ID --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
    echo ""
    
    # 显示最近日志
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📜 最近 20 行日志:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    docker logs --tail 20 $CONTAINER_ID
    echo ""
    
    # 检查最近是否有错误
    RECENT_ERRORS=$(docker logs --since 5m $CONTAINER_ID 2>&1 | grep -i "error\|exception\|failed" | wc -l)
    if [ $RECENT_ERRORS -gt 0 ]; then
        echo "⚠️  最近 5 分钟发现 $RECENT_ERRORS 个错误"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🚨 最近错误信息:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        docker logs --since 5m $CONTAINER_ID 2>&1 | grep -i "error\|exception\|failed" | tail -10
    else
        echo "✅ 最近 5 分钟无错误"
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 常用命令:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  # 查看实时日志"
echo "  docker logs -f \$(docker ps -q --filter ancestor=$IMAGE_NAME)"
echo ""
echo "  # 重启容器"
echo "  make run-tasks config=orderbook_snapshot_gateio.yml"
echo ""
echo "  # 查看数据文件"
echo "  ls -lht app/data/raw/orderbook_snapshots/*.parquet | head -10"
echo ""
echo "================================"

