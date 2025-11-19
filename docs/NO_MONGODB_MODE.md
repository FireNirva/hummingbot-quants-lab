# 无 MongoDB 模式运行指南

## 📋 概述

从本次更新开始，QuantsLab 支持在**不需要 MongoDB** 的情况下运行某些任务。这对于：
- 本地开发和测试
- 只需要数据采集（写入 Parquet）的任务
- 资源受限的环境

特别适用于订单簿快照采集任务，因为它直接写入 Parquet 文件，不依赖数据库。

---

## 🎯 工作原理

### 传统模式（需要 MongoDB）
```
任务运行 → 连接 MongoDB → 记录执行历史 → 执行任务 → 保存结果到 MongoDB
```

### 无 MongoDB 模式（新功能）
```
任务运行 → 检测无 MongoDB → 使用 NoOpStorage → 执行任务 → 直接写入 Parquet
```

---

## 🚀 使用方法

### 方式 1: 本地运行（推荐）

**不设置 MONGO_URI 环境变量：**

```bash
# 取消 MONGO_URI（如果已设置）
unset MONGO_URI

# 直接运行任务
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

**或者创建一个不含 MONGO_URI 的临时环境：**

```bash
# 创建临时 .env 文件
cp .env .env.backup
grep -v "MONGO_URI" .env > .env.temp
mv .env.temp .env

# 运行任务
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 恢复原始 .env
mv .env.backup .env
```

---

### 方式 2: 使用测试脚本

我们提供了一个便捷的测试脚本：

```bash
chmod +x scripts/test_no_mongodb.sh
./scripts/test_no_mongodb.sh
```

---

## 📊 日志输出对比

### 有 MongoDB 配置时：

```
INFO:core.tasks.runner:Starting QuantsLab Task Runner v2.0
INFO:core.tasks.runner:=== MongoDB Environment Check ===
INFO:core.tasks.runner:MONGO_URI: Configured
INFO:core.tasks.runner:MONGO_DATABASE: quants_lab
INFO:core.tasks.runner:=================================
INFO:core.tasks.runner:Using MongoDB for task execution history
INFO:core.tasks.storage:=== MongoDB Storage Initialization ===
INFO:core.tasks.storage:Successfully connected to MongoDB
```

### 无 MongoDB 配置时：

```
INFO:core.tasks.runner:Starting QuantsLab Task Runner v2.0
INFO:core.tasks.runner:MongoDB not configured - using NoOpTaskStorage
INFO:core.tasks.storage:Using NoOpTaskStorage - task execution history will not be persisted
INFO:app.tasks.data_collection.orderbook_snapshot_task:Starting orderbook snapshot collection for 6 pairs
```

---

## ✅ 适用场景

### 推荐使用无 MongoDB 模式：

1. **本地开发和调试**
   - 快速迭代
   - 不需要启动 MongoDB Docker 容器
   - 减少资源占用

2. **订单簿快照采集**
   - 数据直接写入 Parquet 文件
   - 不需要数据库记录执行历史
   - 纯数据采集任务

3. **资源受限环境**
   - 内存不足以运行 MongoDB
   - 磁盘空间有限
   - 只关注数据输出

### 仍需使用 MongoDB 模式：

1. **需要任务执行历史**
   - 监控任务运行状态
   - 分析任务性能指标
   - 调试任务失败原因

2. **使用 API 服务器**
   - 查询任务状态
   - 获取执行历史
   - 远程管理任务

3. **生产环境**
   - 需要完整的可观测性
   - 多任务协调和依赖管理
   - 长期运行和监控

---

## 🔧 技术实现

### NoOpTaskStorage 类

```python
class NoOpTaskStorage(TaskStorage):
    """No-operation task storage for tasks that don't need persistence."""
    
    async def initialize(self) -> None:
        """Initialize (no-op)."""
        logger.info("Using NoOpTaskStorage - task execution history will not be persisted")
    
    async def save_execution(self, result: TaskResult, context: TaskContext) -> None:
        """Save execution (no-op)."""
        pass
    
    async def get_last_execution(self, task_name: str) -> Optional[TaskExecutionRecord]:
        """Get last execution (always returns None)."""
        return None
```

### 自动检测逻辑

在 `TaskRunner.start()` 方法中：

```python
# Check MongoDB configuration and decide storage type
mongo_uri = os.getenv("MONGO_URI")

if mongo_uri:
    # Use MongoDB storage if configured
    storage = MongoDBTaskStorage()
    logger.info("Using MongoDB for task execution history")
else:
    # Use NoOp storage if MongoDB not configured
    storage = NoOpTaskStorage()
    logger.info("MongoDB not configured - using NoOpTaskStorage")
```

---

## ⚠️ 注意事项

### 功能限制

无 MongoDB 模式下，以下功能**不可用**：

1. **任务执行历史查询**
   - 无法查看过去的执行记录
   - 无法获取任务性能指标

2. **API 服务器功能**
   - 无法通过 API 查询任务状态
   - 无法获取历史执行数据

3. **任务依赖管理**
   - 无法基于历史执行结果判断依赖
   - 无法实现复杂的任务编排

### 数据持久化

虽然没有 MongoDB，但任务生成的数据**仍然会持久化**：

- ✅ Parquet 文件：正常写入 `app/data/raw/orderbook_snapshots/`
- ✅ 数据完整性：不受影响
- ✅ 数据可读性：可以直接读取 Parquet 文件
- ❌ 执行历史：不记录到数据库

---

## 💡 最佳实践

### 开发工作流

```bash
# 1. 本地开发（无 MongoDB）
unset MONGO_URI
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 2. 验证数据文件
ls -lht app/data/raw/orderbook_snapshots/

# 3. 确认无误后，部署到生产环境（有 MongoDB）
# 在 AWS Lightsail 上 .env 配置了 MONGO_URI
git push
ssh aws-lightsail
systemctl restart quants-lab-orderbook-gateio
```

### 混合模式

你可以同时运行：
- **本地（无 MongoDB）**：快速采集数据用于开发
- **AWS（有 MongoDB）**：完整监控和历史记录

两者互不干扰，各自独立运行。

---

## 🎓 总结

| 特性 | 有 MongoDB | 无 MongoDB |
|------|-----------|-----------|
| **任务执行** | ✅ | ✅ |
| **数据采集** | ✅ | ✅ |
| **Parquet 写入** | ✅ | ✅ |
| **执行历史** | ✅ | ❌ |
| **API 查询** | ✅ | ❌ |
| **资源占用** | 高 | 低 |
| **启动速度** | 慢 | 快 |
| **适用场景** | 生产环境 | 本地开发 |

---

## 📚 相关文档

- [订单簿采集指南](./ORDERBOOK_COLLECTION_GUIDE.md)
- [任务系统架构](./README.md)
- [Docker 部署指南](./AWS_LIGHTSAIL_DEPLOYMENT_GUIDE.md)

---

**最后更新**: 2024-11-18


