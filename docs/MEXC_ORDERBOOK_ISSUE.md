# MEXC 订单簿采集问题诊断报告

## 📋 问题描述

MEXC 订单簿采集任务无法执行，持续报错：
```
WARNING:core.tasks.orchestrator:Task orderbook_snapshot_mexc is already running in another instance
```

## 🔍 诊断过程

### 测试 1: 检查是否是容器冲突
- **操作**: 同时运行 Gate.io 和 MEXC 容器
- **结果**: MEXC 报错，Gate.io 正常
- **结论**: 可能是容器冲突

### 测试 2: 检查是否是 MongoDB 数据残留
- **操作**: 清空 MongoDB `task_schedules` 集合
- **结果**: 问题仍然存在
- **结论**: 不是数据残留问题

### 测试 3: 隔离测试 MEXC 容器
- **操作**: 停止 Gate.io，只运行 MEXC
- **结果**: ❌ **问题仍然存在！**
- **结论**: **这是 MEXC 任务自身的问题**

## 🎯 根本原因分析

MEXC 任务在 MongoDB 中创建 `is_running=true` 记录后，**从未成功完成执行**，导致：

1. ⏰ **第 0 秒**: 容器启动，调度器开始运行
2. ⏰ **第 0.5 秒**: 第一次尝试执行任务
   - 检查 MongoDB，没有记录
   - 创建记录：`{task_name: 'orderbook_snapshot_mexc', is_running: true}`
   - 开始执行任务...
3. ⏰ **第 5 秒**: 第二次调度（任务还没完成）
   - 检查 MongoDB，发现 `is_running=true`
   - ❌ 报错："already running in another instance"
4. ⏰ **第 10 秒, 15 秒, 20 秒...**: 持续报错

## 🔧 可能的原因

### 原因 1: MEXC API 连接失败 (最可能)

MEXC 交易所的 API 可能：
- 🌐 网络不可达
- 🔐 需要 API 密钥（但配置中没有）
- 🚫 IP 被限流或封禁
- ⏰ 响应超时

**验证方法**:
```bash
# 测试 MEXC API 连接
curl -I https://api.mexc.com/api/v3/ping

# 测试订单簿 API
curl "https://api.mexc.com/api/v3/depth?symbol=AUKIUSDT&limit=100"
```

### 原因 2: MEXC 连接器未正确实现

`CLOBDataSource` 可能没有完全支持 MEXC：
- 缺少 MEXC 特定的 API 适配
- 订单簿格式解析错误
- 交易对格式不匹配（AUKI-USDT vs AUKIUSDT）

### 原因 3: 任务初始化失败但未抛出异常

任务在 `_collect_orderbook_snapshot` 方法中失败，但：
- 异常被捕获但未正确处理
- MongoDB 状态未清理
- 任务被标记为"运行中"但实际已停止

### 原因 4: 异步任务死锁

Python asyncio 相关问题：
- Semaphore 死锁
- Event loop 阻塞
- 异步任务未正确等待

## 💡 解决方案

### 方案 1: 测试 MEXC API 连接

```bash
# 从容器内测试
docker exec c38be1e5a7fe curl -I https://api.mexc.com/api/v3/ping

# 测试订单簿
docker exec c38be1e5a7fe curl "https://api.mexc.com/api/v3/depth?symbol=AUKIUSDT&limit=10"
```

### 方案 2: 添加详细日志

修改 `app/tasks/data_collection/orderbook_snapshot_task.py`，在关键位置添加日志：

```python
async def run(self, context: TaskContext) -> TaskResult:
    logger.info(f"🚀 任务开始执行: {context.task_name}")
    logger.info(f"📝 执行ID: {context.execution_id}")
    
    try:
        # ...现有代码...
        logger.info(f"✅ 任务执行成功")
        return TaskResult(...)
    except Exception as e:
        logger.error(f"❌ 任务执行失败: {e}", exc_info=True)
        raise
    finally:
        logger.info(f"🏁 任务结束")
```

### 方案 3: 使用 NoOpTaskStorage（临时绕过）

在 MEXC 容器中禁用 MongoDB：

```bash
# 停止 MEXC 容器
docker stop c38be1e5a7fe

# 启动时不设置 MONGO_URI
docker run --rm -d \
  --network host \
  -v $(PWD)/app/data:/quants-lab/app/data \
  -v $(PWD)/config:/quants-lab/config \
  --name mexc-orderbook \
  hummingbot/quants-lab \
  conda run -n quants-lab python3 cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
```

### 方案 4: 检查 MEXC 交易对格式

MEXC 可能使用不同的交易对格式：
- 配置: `AUKI-USDT`
- API 需要: `AUKIUSDT` (无连字符)

修改 `config/orderbook_snapshot_mexc.yml`:
```yaml
trading_pairs:
  - "AUKIUSDT"  # 无连字符
  - "SERVUSDT"
  - "IRONUSDT"
```

### 方案 5: 增加任务超时和重试间隔

修改 `config/orderbook_snapshot_mexc.yml`:
```yaml
schedule:
  frequency_hours: 0.002778  # 10 秒（增加到 10 秒）

timeout_seconds: 600  # 增加到 10 分钟
```

## 📊 下一步行动

1. ✅ **首先测试 MEXC API 连接**
2. ✅ 检查交易对格式
3. ✅ 添加详细日志
4. ✅ 如果 API 不可达，考虑放弃 MEXC 或使用其他数据源

## 📝 相关文件

- 配置: `config/orderbook_snapshot_mexc.yml`
- 任务实现: `app/tasks/data_collection/orderbook_snapshot_task.py`
- 数据源: `core/data_sources/clob.py`
- 调度器: `core/tasks/orchestrator.py`
- 存储: `core/tasks/storage.py`

---

**创建时间**: 2024-11-19
**状态**: 🔍 正在诊断

