#!/bin/bash
# 清理 MongoDB 中的任务锁定状态

TASK_NAME="${1:-orderbook_snapshot_mexc}"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║           🔓 清理任务锁定状态                              ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "任务名称: $TASK_NAME"
echo ""

# 检查 MongoDB 是否运行
if ! docker ps | grep -q mongodb; then
    echo "❌ MongoDB 未运行"
    echo ""
    echo "💡 如果你在使用无 MongoDB 模式，这个错误不应该发生。"
    echo "   可能需要："
    echo "   1. 启动 MongoDB: make run-db"
    echo "   2. 或者确保 .env 中没有设置 MONGO_URI"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 检查当前任务状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker exec mongodb mongosh -u admin -p admin --quiet --eval "
  use quants_lab;
  var task = db.task_schedules.findOne({task_name: '$TASK_NAME'});
  if (task) {
    print('找到任务记录:');
    print('  任务名称: ' + task.task_name);
    print('  运行状态: ' + task.is_running);
    print('  执行ID: ' + (task.current_execution_id || 'N/A'));
    print('  更新时间: ' + task.updated_at);
  } else {
    print('❌ 未找到任务记录');
  }
" 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔧 清理锁定状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 清理任务锁定
RESULT=$(docker exec mongodb mongosh -u admin -p admin --quiet --eval "
  use quants_lab;
  var result = db.task_schedules.updateOne(
    {task_name: '$TASK_NAME'},
    {\$set: {
      is_running: false,
      current_execution_id: null,
      updated_at: new Date()
    }}
  );
  print(result.modifiedCount);
" 2>/dev/null)

if [ "$RESULT" = "1" ]; then
    echo "✅ 成功清理任务锁定状态"
else
    echo "⚠️  未找到需要清理的记录（可能任务不存在）"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 验证清理结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

docker exec mongodb mongosh -u admin -p admin --quiet --eval "
  use quants_lab;
  var task = db.task_schedules.findOne({task_name: '$TASK_NAME'});
  if (task) {
    print('当前状态:');
    print('  任务名称: ' + task.task_name);
    print('  运行状态: ' + task.is_running + ' ✅');
    print('  执行ID: ' + (task.current_execution_id || '无 ✅'));
  } else {
    print('✅ 任务记录已不存在');
  }
" 2>/dev/null

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 清理完成"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 下一步:"
echo "   1. 重启 MEXC 容器"
echo "   2. 或者等待任务自动重试（通常几秒后）"
echo ""
echo "   # 重启命令:"
echo "   docker restart ec09573dbfde"
echo "   # 或"
echo "   docker-compose -f docker-compose-orderbook.yml restart orderbook-mexc"
echo ""

