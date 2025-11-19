# 📊 MongoDB 在 QuantsLab 中的作用详解

## 🎯 快速回答

**MongoDB 在本项目中的作用：**
1. **存储任务执行历史** - 记录每次任务的运行状态、耗时、结果
2. **存储池子筛选结果** - 保存 DEX 池子筛选的时间序列数据
3. **存储元数据和配置** - 任务调度信息、筛选器结果等结构化数据

**为什么使用 MongoDB？**
- 灵活的文档结构（无需预定义 schema）
- 适合存储元数据和结构化数据
- 支持时间序列查询和聚合分析

**重要：** MongoDB **不存储**交易数据、K线数据、订单簿数据（这些存储在 Parquet 文件中）

---

## 🗄️ MongoDB 存储的数据详解

### 1. 任务执行历史 (`task_executions` 集合)

这是 MongoDB 在项目中的**核心作用**。

#### 📝 存储内容

记录每一次任务执行的完整信息：

```json
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_name": "orderbook_snapshot_gateio",
  "status": "completed",                           // completed | failed | running
  "started_at": ISODate("2024-11-18T05:00:00Z"),
  "completed_at": ISODate("2024-11-18T05:00:05Z"),
  "duration_seconds": 5.2,
  "result_data": {
    "status": "completed",
    "stats": {
      "pairs_processed": 6,
      "snapshots_collected": 6,
      "errors": 0
    }
  },
  "error_message": null,
  "error_traceback": null
}
```

#### 🎯 用途

- **监控任务运行状态** - 查看哪些任务正在运行、已完成或失败
- **分析任务性能** - 统计任务平均耗时、成功率
- **故障排查** - 查看失败任务的错误信息和堆栈
- **历史回溯** - 追踪某个时间段的任务执行情况

#### 💡 实际应用场景

```python
# 查询最近失败的任务
db.task_executions.find({
    "status": "failed",
    "started_at": {"$gte": ISODate("2024-11-18T00:00:00Z")}
}).sort({"started_at": -1})

# 统计任务平均耗时
db.task_executions.aggregate([
    {"$match": {"task_name": "orderbook_snapshot_gateio"}},
    {"$group": {
        "_id": null,
        "avg_duration": {"$avg": "$duration_seconds"},
        "total_runs": {"$sum": 1}
    }}
])
```

---

### 2. DEX 池子筛选结果 (`pools` 集合)

#### 📝 存储内容

记录每次池子筛选任务的结果（时间序列数据）：

```json
{
  "_id": ObjectId("..."),
  "timestamp": ISODate("2024-11-18T00:00:00Z"),
  "execution_id": "uuid-string",
  "network": "base",
  
  // 热门池子（未筛选）
  "trending_pools": [
    {
      "name": "VIRTUAL/WETH",
      "address": "0x1234...",
      "dex_id": "uniswap-v3",
      "fdv_usd": 125000000,
      "volume_usd_h24": 8500000,
      "reserve_in_usd": 2300000,
      "volume_liquidity_ratio": 3.7,
      "price_change_percentage_h24": 5.2
    }
    // ... 最多 20 个
  ],
  
  // 筛选后的热门池子（符合条件）
  "filtered_trending_pools": [
    // 只包含通过筛选条件的池子
  ],
  
  // 新池子（未筛选）
  "new_pools": [...],
  
  // 筛选后的新池子
  "filtered_new_pools": [...]
}
```

#### 🎯 用途

- **追踪池子变化** - 观察某个池子的流动性、交易量随时间的变化
- **趋势分析** - 分析哪些池子持续热门
- **回测数据** - 为交易策略提供历史池子数据
- **监控新池子** - 发现新出现的高潜力池子

#### 💡 实际应用场景

```python
# 查询某个池子的历史数据
db.pools.find({
    "trending_pools.address": "0x1234...",
    "timestamp": {
        "$gte": ISODate("2024-11-01T00:00:00Z"),
        "$lte": ISODate("2024-11-18T00:00:00Z")
    }
}).sort({"timestamp": 1})

# 统计最近 7 天最热门的池子
db.pools.aggregate([
    {"$match": {
        "timestamp": {"$gte": ISODate("2024-11-11T00:00:00Z")}
    }},
    {"$unwind": "$trending_pools"},
    {"$group": {
        "_id": "$trending_pools.name",
        "avg_volume": {"$avg": "$trending_pools.volume_usd_h24"},
        "count": {"$sum": 1}
    }},
    {"$sort": {"avg_volume": -1}},
    {"$limit": 10}
])
```

---

### 3. 任务调度信息 (`task_schedules` 集合)

#### 📝 存储内容

管理任务的运行状态，防止重复执行：

```json
{
  "_id": ObjectId("..."),
  "task_name": "orderbook_snapshot_gateio",
  "is_running": true,
  "current_execution_id": "uuid-string",
  "created_at": ISODate("2024-11-18T00:00:00Z"),
  "updated_at": ISODate("2024-11-18T05:00:00Z")
}
```

#### 🎯 用途

- **防止任务重复运行** - 确保同一任务不会同时运行多次
- **任务状态管理** - 标记任务是否正在执行
- **分布式协调** - 在多实例环境下协调任务执行

---

## 🔄 MongoDB 与 Parquet 的分工

QuantsLab 使用**混合存储策略**，根据数据特点选择最佳存储方式：

| 数据类型 | 存储方式 | 原因 |
|---------|---------|------|
| **K线数据** (OHLCV) | ✅ Parquet | 海量时间序列，列式存储高效 |
| **订单簿快照** | ✅ Parquet | 高频数据，写入量大，Parquet 压缩好 |
| **交易数据** (Trades) | ✅ Parquet | 原始交易记录，量大，查询需要列式分析 |
| **资金费率** | ✅ Parquet | 时间序列数据，适合批量分析 |
| **任务执行历史** | ✅ MongoDB | 元数据，灵活查询，复杂聚合 |
| **池子筛选结果** | ✅ MongoDB | 结构化数据，需要时间序列查询 |
| **任务调度状态** | ✅ MongoDB | 实时状态管理，需要原子操作 |

### 为什么不把所有数据都存 MongoDB？

**MongoDB 不适合存储大量时间序列数据的原因：**

1. **存储成本高** 
   - 1 年的 1 分钟 K 线 = 525,600 条记录
   - MongoDB 文档存储开销大（每条记录都有 `_id`、字段名等）
   - Parquet 列式压缩率高（通常压缩比 1:10）

2. **查询性能差**
   - 列式分析（如计算均线）需要扫描大量文档
   - Parquet 列式存储可以只读取需要的列

3. **写入压力大**
   - 订单簿每 5 秒一次快照 = 每天 17,280 次写入
   - MongoDB 写入有 IOPS 限制

4. **分析效率低**
   - Pandas/NumPy 直接读取 Parquet 超快
   - MongoDB 需要先查询再转换为 DataFrame

### 为什么不把元数据也存 Parquet？

**Parquet 不适合存储元数据的原因：**

1. **查询不灵活**
   - 无法做复杂的过滤和聚合（如"查找最近失败的任务"）
   - 需要读取整个文件才能查询

2. **无法原子更新**
   - Parquet 是追加式文件，无法更新单条记录
   - 任务状态管理需要原子操作（如标记任务正在运行）

3. **结构变化困难**
   - 添加新字段需要重写整个文件
   - MongoDB 可以随时添加新字段

---

## 🎯 实际工作流示例

### 场景 1: 订单簿数据采集

```
1. 任务开始
   ├─ MongoDB: 写入任务开始记录 (task_executions)
   │           {"status": "running", "started_at": "2024-11-18T05:00:00Z"}
   │
2. 采集数据
   ├─ Gate.io API: 获取 6 个交易对的订单簿
   │
3. 保存数据
   ├─ Parquet: 写入订单簿快照数据
   │           app/data/raw/orderbook_snapshots/gate_io_VIRTUAL-USDT_20241118.parquet
   │           (实际的订单簿数据)
   │
4. 任务完成
   └─ MongoDB: 更新任务完成记录
               {"status": "completed", "completed_at": "2024-11-18T05:00:05Z",
                "result_data": {"snapshots_collected": 6}}
```

**结果：**
- ✅ **Parquet** 存储了实际的订单簿数据（用于交易分析）
- ✅ **MongoDB** 记录了任务执行情况（用于监控和故障排查）

---

### 场景 2: DEX 池子筛选

```
1. 任务开始
   ├─ MongoDB: 写入任务开始记录
   │
2. 获取池子数据
   ├─ GeckoTerminal API: 获取热门池子和新池子
   │
3. 筛选和保存
   ├─ MongoDB: 保存完整的池子筛选结果
   │           pools 集合 (trending_pools, filtered_trending_pools, ...)
   │
4. 任务完成
   └─ MongoDB: 更新任务执行记录
```

**结果：**
- ✅ **MongoDB** 存储了池子数据（结构化，需要时间序列查询）
- ❌ **不使用 Parquet**（数据量小，需要灵活查询）

---

## 📊 MongoDB 数据量估算

### 任务执行历史

**假设：**
- 6 个订单簿采集任务（Gate.io + MEXC）
- 每 5 秒运行一次
- 每天执行次数 = 6 × (86400 / 5) = 103,680 次

**每月数据量：**
- 每条记录约 1 KB
- 每月数据 = 103,680 × 30 × 1 KB ≈ **3 GB**

### 池子筛选结果

**假设：**
- 每小时筛选一次
- 每次 20 个热门池子 + 20 个新池子
- 每个池子约 500 字节

**每月数据量：**
- 每次记录 = 40 × 500 bytes = 20 KB
- 每月数据 = 24 × 30 × 20 KB ≈ **14 MB**

**总计：** 每月约 **3 GB** MongoDB 数据（主要是任务执行历史）

---

## 🔧 如何查看 MongoDB 数据

### 使用 MongoDB Compass（GUI）

```bash
# 连接字符串
mongodb://admin:admin@localhost:27017

# 数据库
quants_lab
```

### 使用命令行

```bash
# 进入 MongoDB 容器
docker exec -it quants-lab-mongodb-1 mongosh -u admin -p admin

# 切换到 quants_lab 数据库
use quants_lab

# 查看所有集合
show collections

# 查询任务执行历史
db.task_executions.find().sort({started_at: -1}).limit(5)

# 查询池子数据
db.pools.find().sort({timestamp: -1}).limit(1)

# 统计任务数量
db.task_executions.countDocuments()
```

### 使用 Python

```python
from core.database_manager import db_manager
import asyncio

async def query_mongodb():
    # 获取 MongoDB 客户端
    client = await db_manager.get_mongodb_client()
    db = client.get_database("quants_lab")
    
    # 查询最近 10 次任务执行
    executions = db["task_executions"].find().sort("started_at", -1).limit(10)
    
    async for execution in executions:
        print(f"Task: {execution['task_name']}")
        print(f"Status: {execution['status']}")
        print(f"Duration: {execution.get('duration_seconds', 'N/A')}s")
        print("---")

asyncio.run(query_mongodb())
```

---

## 🤔 常见问题

### Q1: 为什么订单簿数据不存 MongoDB？

**A:** 订单簿数据量太大：
- 每 5 秒采集 6 个交易对 = 每天 103,680 次
- 每次快照约 100 个价格档位 × 2 (买+卖) = 200 条记录
- 每天总记录数 = 103,680 × 200 = **2,073万条**

如果存 MongoDB：
- 存储成本高（每条记录有开销）
- 查询慢（需要扫描大量文档）
- 分析不便（无法利用 Pandas 列式优化）

**Parquet 优势：**
- 高压缩比（1:10）
- 快速列式查询
- 直接加载到 Pandas

---

### Q2: 如果不需要监控任务，可以不用 MongoDB 吗？

**A:** 可以！这就是我们刚实现的 **NoOpTaskStorage** 模式。

```bash
# 取消 MONGO_URI
unset MONGO_URI

# 运行任务（不需要 MongoDB）
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
```

**适用场景：**
- ✅ 本地开发和调试
- ✅ 只需要数据采集（不需要监控）
- ✅ 资源受限环境

**限制：**
- ❌ 无法查看任务执行历史
- ❌ 无法使用 API 查询任务状态
- ❌ 无法进行任务性能分析

详见：[无 MongoDB 模式运行指南](./NO_MONGODB_MODE.md)

---

### Q3: MongoDB 的 `pools` 集合会不会越来越大？

**A:** 会，但增长速度可控：

- 每小时一次池子筛选 = 每天 24 条记录
- 每条约 20 KB
- 每年数据 = 24 × 365 × 20 KB ≈ **175 MB**

**管理策略：**

```javascript
// 删除 90 天前的池子数据
db.pools.deleteMany({
    "timestamp": {
        "$lt": new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)
    }
})

// 或者创建 TTL 索引（自动清理）
db.pools.createIndex(
    {"timestamp": 1},
    {expireAfterSeconds: 7776000}  // 90 天
)
```

---

### Q4: 为什么不用 PostgreSQL 或 MySQL？

**A:** MongoDB 的优势：

1. **灵活的 schema** - 任务结果可能有不同的字段
2. **嵌套文档** - 池子数据是嵌套结构，MongoDB 原生支持
3. **聚合管道** - 强大的数据分析能力
4. **易于扩展** - 添加新字段无需 ALTER TABLE

PostgreSQL/MySQL 更适合：
- 强类型约束的数据
- 事务性操作
- 复杂的 JOIN 查询

---

## 📚 总结

| 方面 | 详情 |
|------|------|
| **主要作用** | 存储任务执行历史、池子筛选结果、任务调度信息 |
| **为什么用** | 灵活的文档结构、适合元数据存储、支持复杂查询 |
| **不存储** | K线数据、订单簿数据、交易数据（这些在 Parquet） |
| **数据量** | 每月约 3 GB（主要是任务执行历史） |
| **可选性** | 订单簿采集等任务可以不依赖 MongoDB 运行 |
| **适用场景** | 需要监控、故障排查、历史分析时使用 |

---

**相关文档：**
- [数据存储策略详解](./DATA_STORAGE_STRATEGY.md)
- [MongoDB 池子数据存储](./MONGODB_POOL_STORAGE.md)
- [无 MongoDB 模式运行指南](./NO_MONGODB_MODE.md)

---

**最后更新**: 2024-11-18

