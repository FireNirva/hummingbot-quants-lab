# MongoDB Pool Screener 数据存储结构

本文档详细说明 Pool Screener（池子筛选器）如何在 MongoDB 中存储数据。

---

## 📊 核心存储策略

### 存储方式：时间序列追加（Time-Series Append）

**关键特点：**
- ✅ **每次执行插入新文档**（不覆盖）
- ✅ **保留历史记录**（时间序列数据）
- ✅ **支持趋势分析**（可追踪池子变化）
- ✅ **独立的执行记录**（每个任务执行都有唯一 ID）

**存储位置：**
```
数据库：quants_lab
集合：  pools
```

---

## 🗄️ 文档结构

### 顶层文档结构

每次运行 Pool Screener 任务会在 `pools` 集合中插入**一个新文档**：

```javascript
{
  "_id": ObjectId("..."),                    // MongoDB 自动生成的文档 ID
  "timestamp": ISODate("2025-10-05T10:30:00Z"),  // 筛选执行时间（UTC）
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",  // 唯一的执行 ID
  
  // 原始热门池子数据（清洗后，未筛选）
  "trending_pools": [
    { /* pool object 1 */ },
    { /* pool object 2 */ },
    // ... 最多 20 个池子
  ],
  
  // 筛选后的热门池子（符合配置条件）
  "filtered_trending_pools": [
    { /* filtered pool object 1 */ },
    { /* filtered pool object 2 */ },
    // ... 符合条件的池子
  ],
  
  // 原始新池子数据（清洗后，未筛选）
  "new_pools": [
    { /* pool object 1 */ },
    { /* pool object 2 */ },
    // ... 最多 20 个池子
  ],
  
  // 筛选后的新池子（符合配置条件）
  "filtered_new_pools": [
    { /* filtered pool object 1 */ },
    { /* filtered pool object 2 */ },
    // ... 符合条件的池子
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| `_id` | ObjectId | MongoDB 自动生成的唯一标识 | `ObjectId("507f1f77bcf86cd799439011")` |
| `timestamp` | ISODate | 任务执行的 UTC 时间戳 | `ISODate("2025-10-05T10:30:00Z")` |
| `execution_id` | String (UUID) | 任务执行的唯一标识符 | `"550e8400-e29b-41d4-a716-446655440000"` |
| `trending_pools` | Array | GeckoTerminal API 返回的热门池子（已清洗） | `[{...}, {...}]` |
| `filtered_trending_pools` | Array | 符合筛选条件的热门池子 | `[{...}]` |
| `new_pools` | Array | GeckoTerminal API 返回的新池子（已清洗） | `[{...}, {...}]` |
| `filtered_new_pools` | Array | 符合筛选条件的新池子 | `[{...}]` |

---

## 🏊 单个池子对象结构

每个池子对象（在 `*_pools` 数组中）包含以下字段：

### 基础信息

```javascript
{
  // GeckoTerminal 原始字段
  "id": "base_uniswap-v3_0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
  "type": "pool",
  "name": "WETH / USDC 0.01%",  // 池子名称（包含费率）
  "address": "0x4c36388be6f416a29c8d8eee81c771ce6be14b18",
  
  // 价格信息
  "base_token_price_usd": "3260.45",
  "quote_token_price_usd": "1.0",
  "base_token_price_native_currency": "1.0",
  "quote_token_price_native_currency": "0.000306748",
  
  // 池子统计
  "reserve_in_usd": "8326274.123",      // 流动性（USD）
  "fdv_usd": "784144285.456",           // 完全稀释估值（USD）
  "market_cap_usd": "784144285.456",    // 市值（USD）
  
  // 交易数据
  "volume_usd_h24": "158589434.234",    // 24小时交易量（USD）
  "transactions_h24_buys": 12345,       // 24小时买单笔数
  "transactions_h24_sells": 11234,      // 24小时卖单笔数
  "transactions_h1_buys": 523,          // 1小时买单笔数
  "transactions_h1_sells": 498,         // 1小时卖单笔数
  
  // 价格变化
  "price_change_percentage_h1": 0.52,   // 1小时价格变化百分比
  "price_change_percentage_h24": 2.34,  // 24小时价格变化百分比
  
  // 时间戳
  "pool_created_at": "2023-08-15T10:30:00Z",  // 池子创建时间
  
  // 关联 ID
  "dex_id": "uniswap-v3-base",
  "base_token_id": "base_0x4200000000000000000000000000000000000006",
  "quote_token_id": "base_0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  "network_id": "base",
  
  // 解析后的字段（由 clean_pools 添加）
  "base": "WETH",                       // 基础代币符号
  "quote": "USDC 0.01%",               // 报价代币符号（含费率）
  
  // 计算字段（由 clean_pools 添加）
  "volume_liquidity_ratio": 19.05,      // 交易量/流动性比率
  "fdv_liquidity_ratio": 94.18,         // FDV/流动性比率
  "fdv_volume_ratio": 4.94              // FDV/交易量比率
}
```

### 字段分类

#### 📌 标识字段
- `id`: 池子的全局唯一标识（格式：`{network}_{dex}_{address}`）
- `address`: 池子的区块链地址
- `name`: 池子的人类可读名称

#### 💰 金融指标
- `reserve_in_usd`: **流动性**（池子中的总价值）
- `fdv_usd`: **完全稀释估值**（假设所有代币都流通的市值）
- `market_cap_usd`: **实际市值**
- `volume_usd_h24`: **24小时交易量**

#### 📊 交易活动
- `transactions_h24_buys/sells`: 24小时内的买卖笔数
- `transactions_h1_buys/sells`: 1小时内的买卖笔数

#### 📈 价格变动
- `price_change_percentage_h1`: 1小时价格变化
- `price_change_percentage_h24`: 24小时价格变化

#### 🔗 关联信息
- `dex_id`: DEX 标识（如 `uniswap-v3-base`）
- `network_id`: 区块链网络（如 `base`, `ethereum`）
- `base_token_id`, `quote_token_id`: 代币的全局 ID

#### 🧮 计算指标（自动添加）
- `volume_liquidity_ratio`: 活跃度指标（高值 = 高交易/低流动性）
- `fdv_liquidity_ratio`: 估值/流动性比率
- `fdv_volume_ratio`: 估值/交易量比率

---

## 🔄 数据更新策略

### 策略说明

**Pool Screener 采用追加策略（Append-Only）：**

```
任务执行 1 → 插入文档 1 (timestamp: T1)
任务执行 2 → 插入文档 2 (timestamp: T2)  ✅ 不覆盖文档 1
任务执行 3 → 插入文档 3 (timestamp: T3)  ✅ 不覆盖文档 1, 2
...
```

### 为什么不覆盖？

**优点：**
1. ✅ **历史追踪**: 可以看到池子在不同时间的状态变化
2. ✅ **趋势分析**: 支持分析交易量、流动性的历史趋势
3. ✅ **数据审计**: 保留完整的执行记录
4. ✅ **容错性**: 即使某次执行失败，历史数据不受影响
5. ✅ **时间序列**: 支持绘制时间序列图表

**缺点：**
1. ❌ **存储增长**: 数据量随时间线性增长
2. ❌ **查询复杂**: 需要按时间戳排序获取最新数据

### 数据增长估算

**示例计算（Base 链 USDC 池子筛选）：**

```
单次执行数据量:
  - trending_pools: 20 个池子
  - new_pools: 20 个池子
  - 每个池子: ~2KB
  - 单次文档大小: ~80KB

每小时执行 5 个任务（5种费率）:
  - 小时增长: 80KB × 5 = 400KB
  - 日增长: 400KB × 24 = 9.6MB
  - 月增长: 9.6MB × 30 = 288MB
  - 年增长: 288MB × 12 = 3.5GB
```

### 数据清理建议

**定期清理旧数据：**

```javascript
// 删除 30 天前的数据
db.pools.deleteMany({
  timestamp: { 
    $lt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) 
  }
})

// 或者只保留最近 N 条记录
const recentDocs = db.pools.find().sort({timestamp: -1}).limit(1000).toArray()
const recentIds = recentDocs.map(doc => doc._id)
db.pools.deleteMany({
  _id: { $nin: recentIds }
})
```

---

## 🔍 数据查询示例

### 1. 获取最新的筛选结果

```python
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://admin:admin@localhost:27017/quants_lab?authSource=admin')
db = client['quants_lab']

# 获取最新的一次执行结果
latest = db.pools.find_one({}, sort=[('timestamp', -1)])

print(f"执行时间: {latest['timestamp']}")
print(f"筛选到的热门池子: {len(latest['filtered_trending_pools'])} 个")
print(f"筛选到的新池子: {len(latest['filtered_new_pools'])} 个")

# 获取所有符合条件的池子
all_pools = latest['filtered_trending_pools'] + latest['filtered_new_pools']
for pool in all_pools:
    print(f"  {pool['name']}: ${pool['volume_usd_h24']:,.0f} 24h volume")
```

### 2. 获取特定任务的所有历史记录

```python
# 获取最近 10 次执行的结果
recent_results = list(db.pools.find({}).sort("timestamp", -1).limit(10))

for result in recent_results:
    timestamp = result['timestamp']
    trending_count = len(result['filtered_trending_pools'])
    new_count = len(result['filtered_new_pools'])
    print(f"{timestamp}: {trending_count} trending, {new_count} new")
```

### 3. 分析池子的时间序列数据

```python
import pandas as pd

# 获取特定池子的历史数据
pool_address = "0x4c36388be6f416a29c8d8eee81c771ce6be14b18"

# 查询所有包含该池子的文档
results = db.pools.find({}).sort("timestamp", -1).limit(100)

# 提取该池子的历史数据
pool_history = []
for result in results:
    all_pools = result['trending_pools'] + result['new_pools']
    for pool in all_pools:
        if pool['address'] == pool_address:
            pool_history.append({
                'timestamp': result['timestamp'],
                'volume': float(pool['volume_usd_h24']),
                'liquidity': float(pool['reserve_in_usd']),
                'ratio': pool.get('volume_liquidity_ratio', 0)
            })

# 转换为 DataFrame 进行分析
df = pd.DataFrame(pool_history)
df = df.sort_values('timestamp')

print(df.describe())
```

### 4. 查询特定时间范围的数据

```python
from datetime import datetime, timedelta

# 查询最近 24 小时的数据
yesterday = datetime.utcnow() - timedelta(hours=24)
recent_docs = db.pools.find({
    'timestamp': {'$gte': yesterday}
}).sort('timestamp', -1)

for doc in recent_docs:
    print(f"{doc['timestamp']}: {doc['execution_id']}")
```

### 5. 统计数据

```python
# 统计总文档数
total_docs = db.pools.count_documents({})
print(f"总执行次数: {total_docs}")

# 统计数据库大小
stats = db.command("collStats", "pools")
print(f"Collection 大小: {stats['size'] / 1024 / 1024:.2f} MB")
print(f"文档数量: {stats['count']}")
print(f"平均文档大小: {stats['avgObjSize'] / 1024:.2f} KB")

# 按日期统计执行次数
pipeline = [
    {
        '$group': {
            '_id': {
                '$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}
            },
            'count': {'$sum': 1}
        }
    },
    {'$sort': {'_id': -1}},
    {'$limit': 30}
]

daily_stats = list(db.pools.aggregate(pipeline))
for stat in daily_stats:
    print(f"{stat['_id']}: {stat['count']} 次执行")
```

---

## 🏗️ 索引优化建议

### 创建索引

为了提高查询性能，建议创建以下索引：

```python
# 1. 时间戳索引（最常用）
db.pools.create_index([('timestamp', -1)])

# 2. 执行 ID 索引（用于追踪特定执行）
db.pools.create_index([('execution_id', 1)])

# 3. 复合索引（时间戳 + 执行 ID）
db.pools.create_index([('timestamp', -1), ('execution_id', 1)])

# 查看索引
db.pools.list_indexes()
```

### 索引效果

**无索引：**
```
查询最新 100 条: ~500ms
```

**有索引：**
```
查询最新 100 条: ~5ms  (100x faster)
```

---

## 📐 数据结构对比

### vs Parquet（CLOB 数据）

| 特性 | MongoDB (Pool Screener) | Parquet (CLOB) |
|-----|------------------------|----------------|
| 数据类型 | 快照数据（池子状态） | 时间序列（K线、交易） |
| 更新频率 | 低（1小时一次） | 高（实时/分钟级） |
| 数据量 | 小（~100KB/次） | 大（GB级别） |
| 查询模式 | 最新/最近 N 条 | 时间范围查询 |
| 存储方式 | 文档追加 | 列式存储 |
| 适用场景 | 市场概览、池子筛选 | 技术分析、回测 |

### vs 关系数据库

| 特性 | MongoDB | MySQL/PostgreSQL |
|-----|---------|------------------|
| Schema | 灵活（Schema-less） | 固定（需定义表结构） |
| 嵌套数据 | 原生支持 | 需要 JOIN |
| 横向扩展 | 容易（Sharding） | 困难 |
| 数组支持 | 原生支持 | 需序列化 |
| 适用场景 | 非结构化/半结构化 | 结构化数据 |

---

## 🔧 最佳实践

### 1. 数据写入

```python
# ✅ 推荐：使用事务（如果需要）
async with await client.start_session() as session:
    async with session.start_transaction():
        await db.pools.insert_one(document, session=session)
        await db.task_logs.insert_one(log_document, session=session)

# ✅ 推荐：批量写入
documents = [doc1, doc2, doc3]
await db.pools.insert_many(documents)

# ❌ 不推荐：逐条写入
for doc in documents:
    await db.pools.insert_one(doc)  # 太慢
```

### 2. 数据查询

```python
# ✅ 推荐：使用投影（只返回需要的字段）
db.pools.find(
    {},
    {'timestamp': 1, 'filtered_trending_pools': 1, '_id': 0}
).sort('timestamp', -1).limit(10)

# ✅ 推荐：使用聚合管道
pipeline = [
    {'$sort': {'timestamp': -1}},
    {'$limit': 10},
    {'$project': {
        'timestamp': 1,
        'pool_count': {
            '$add': [
                {'$size': '$filtered_trending_pools'},
                {'$size': '$filtered_new_pools'}
            ]
        }
    }}
]
results = db.pools.aggregate(pipeline)

# ❌ 不推荐：加载所有数据再处理
all_docs = list(db.pools.find({}))  # 内存爆炸
```

### 3. 数据维护

```python
# ✅ 定期清理旧数据
from datetime import datetime, timedelta

cutoff_date = datetime.utcnow() - timedelta(days=30)
result = db.pools.delete_many({'timestamp': {'$lt': cutoff_date}})
print(f"Deleted {result.deleted_count} old documents")

# ✅ 压缩集合（释放空间）
db.command('compact', 'pools')

# ✅ 监控集合大小
stats = db.command('collStats', 'pools')
size_mb = stats['size'] / 1024 / 1024
print(f"Collection size: {size_mb:.2f} MB")
if size_mb > 1000:  # 超过 1GB
    print("⚠️ Consider archiving old data")
```

---

## 🎯 实际应用场景

### 场景 1：实时监控

```python
# 监控最新的池子变化
while True:
    latest = db.pools.find_one({}, sort=[('timestamp', -1)])
    
    filtered_pools = (
        latest['filtered_trending_pools'] + 
        latest['filtered_new_pools']
    )
    
    for pool in filtered_pools:
        if pool['volume_liquidity_ratio'] > 5.0:
            print(f"🚨 High activity: {pool['name']}")
    
    await asyncio.sleep(3600)  # 每小时检查一次
```

### 场景 2：历史趋势分析

```python
# 分析池子活跃度趋势
results = db.pools.find({}).sort('timestamp', -1).limit(100)

volumes = []
timestamps = []

for result in results:
    total_volume = sum(
        float(p['volume_usd_h24']) 
        for p in result['filtered_trending_pools']
    )
    volumes.append(total_volume)
    timestamps.append(result['timestamp'])

# 绘制趋势图
import matplotlib.pyplot as plt
plt.plot(timestamps, volumes)
plt.title('Total Volume Trend')
plt.show()
```

### 场景 3：套利机会识别

```python
# 识别高交易量/低流动性的池子（套利机会）
latest = db.pools.find_one({}, sort=[('timestamp', -1)])

opportunities = []
for pool in latest['filtered_trending_pools']:
    ratio = pool.get('volume_liquidity_ratio', 0)
    if ratio > 3.0:  # 高活跃度
        opportunities.append({
            'name': pool['name'],
            'ratio': ratio,
            'volume': float(pool['volume_usd_h24']),
            'liquidity': float(pool['reserve_in_usd'])
        })

# 按比率排序
opportunities.sort(key=lambda x: x['ratio'], reverse=True)

print("🎯 Top Arbitrage Opportunities:")
for opp in opportunities[:5]:
    print(f"  {opp['name']}: {opp['ratio']:.2f}x")
```

---

## 📚 相关文档

- [Pool Screener 配置说明](../config/base_pools_production.yml)
- [数据存储策略概述](./DATA_STORAGE_STRATEGY.md)
- [已知问题和解决方案](./KNOWN_ISSUES.md)
- [快速开始指南](./QUICK_START_DATA_COLLECTION.md)

---

**最后更新：** 2025-10-05  
**维护者：** Alice  
**版本：** 1.0


