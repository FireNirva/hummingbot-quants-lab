# 📊 Gate.io 订单簿数据结构详解

> **完整解析 Gate.io 订单簿 API 返回的数据格式和 Update ID (Sequence Number)**

---

## 🎯 Gate.io 订单簿数据结构

Gate.io 提供两种方式获取订单簿数据：REST API 和 WebSocket。

---

## 📡 **方式 1: REST API**

### **API 端点**

```
GET https://api.gateio.ws/api/v4/spot/order_book
```

### **请求参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `currency_pair` | string | ✅ | 交易对（如 `BTC_USDT`） |
| `limit` | integer | ❌ | 返回档位数（默认10，最大100） |
| `with_id` | boolean | **✅ 关键** | 是否返回 `update_id`（默认false） |

### **返回数据结构**

#### **不带 `with_id=true`（默认）**

```json
{
  "asks": [
    ["19549.74", "0.5"],     // [价格, 数量]
    ["19549.75", "0.8"],
    ...
  ],
  "bids": [
    ["19549.73", "0.342"],
    ["19549.72", "0.4"],
    ...
  ]
}
```

**❌ 问题**：没有 `update_id`，无法追踪数据版本！

#### **带 `with_id=true`（推荐）** ✅

```json
{
  "id": 548631456,            // 🔑 Update ID (类似 sequence_number)
  "current": 1666051200,      // 当前时间戳（秒）
  "update": 1666051199,       // 更新时间戳（秒）
  "asks": [
    ["19549.74", "0.5"],
    ["19549.75", "0.8"],
    ...
  ],
  "bids": [
    ["19549.73", "0.342"],
    ["19549.72", "0.4"],
    ...
  ]
}
```

**✅ 包含**：
- `id`: **Update ID**（订单簿更新序列号）
- `current`: 当前时间戳
- `update`: 订单簿最后更新时间
- `asks`: 卖盘
- `bids`: 买盘

---

## 🔌 **方式 2: WebSocket API**

### **连接 URL**

```
wss://api.gateio.ws/ws/v4/
```

### **订阅消息**

```json
{
  "time": 1666051200,
  "channel": "spot.order_book_update",
  "event": "subscribe",
  "payload": ["BTC_USDT", "20", "100ms"]
  // [交易对, 深度档位, 更新频率]
}
```

### **返回数据结构**

```json
{
  "time": 1666051200,
  "time_ms": 1666051200016,
  "channel": "spot.order_book_update",
  "event": "update",
  "result": {
    "t": 1666051200016,       // 时间戳（毫秒）
    "e": "depthUpdate",       // 事件类型
    "E": 1666051200,          // 事件时间（秒）
    "s": "BTC_USDT",          // 交易对
    "U": 548631456,           // 🔑 First update ID
    "u": 548631456,           // 🔑 Last update ID
    "b": [                    // 买盘更新
      ["19549.73", "0.342"]
    ],
    "a": [                    // 卖盘更新
      ["19549.74", "0.5"]
    ]
  }
}
```

**关键字段**：
- `U`: **First update ID**（第一个更新序列号）
- `u`: **Last update ID**（最后一个更新序列号）
- 如果 `U == u`，表示这是单个更新
- 如果 `U < u`，表示这个消息包含多个更新

---

## 🔍 **Update ID 的特点**

### **1. 递增性**

```python
# REST API 调用序列
Request 1: id = 548631456
Request 2: id = 548631789  # 增加了 333
Request 3: id = 548632001  # 增加了 212

# 每次请求的 id 都会递增
```

### **2. 不连续性**

```python
# REST API 的 id 不一定连续（因为是快照，不是每次变化）
Request 1: id = 548631456
Request 2: id = 548631789  # 跳过了 548631457 ~ 548631788
                           # 这期间可能有多次订单簿变化

# WebSocket 的 U/u 是连续的（每次变化都推送）
Update 1: U=548631456, u=548631456
Update 2: U=548631457, u=548631457  # 连续
Update 3: U=548631458, u=548631458  # 连续
```

### **3. 全局唯一性**

```python
# 同一交易对的 update_id 在全局唯一且递增
BTC_USDT: 548631456 → 548631789 → 548632001
ETH_USDT: 329874123 → 329874456 → 329874789

# 不同交易对有独立的 update_id 序列
```

---

## 🛠️ **如何在 QuantsLab 中添加 Update ID**

### **Step 1: 修改 OrderBookSnapshotTask**

当前代码只保存价格和数量，需要添加 `update_id` 字段。

#### **原始代码 (app/tasks/data_collection/orderbook_snapshot_task.py)**

```python
async def _collect_orderbook_snapshot(self, trading_pair: str) -> bool:
    # 当前实现
    orderbook = await self.connector.get_order_book(formatted_pair)
    
    snapshot_data = {
        'timestamp': timestamp,
        'exchange': self.connector_name,
        'trading_pair': trading_pair,
        'best_bid_price': float(bids[0].price),
        # ... 其他字段
    }
```

#### **修改后的代码（添加 update_id）**

```python
async def _collect_orderbook_snapshot(self, trading_pair: str) -> bool:
    """采集单个交易对的订单簿快照（包含 update_id）"""
    try:
        formatted_pair = trading_pair.replace('-', '_')
        
        # ========================================
        # 🆕 方式 1: 通过 Hummingbot 连接器（如果支持）
        # ========================================
        try:
            orderbook = await self.connector.get_order_book(formatted_pair)
            
            # 检查是否有 update_id
            update_id = None
            if hasattr(orderbook, 'update_id'):
                update_id = orderbook.update_id
            elif hasattr(orderbook, 'last_update_id'):
                update_id = orderbook.last_update_id
            
            # 如果 Hummingbot 不提供 update_id，直接调用 Gate.io API
            if update_id is None:
                update_id = await self._get_update_id_from_api(formatted_pair)
        
        except Exception as e:
            logger.warning(f"Failed to get orderbook via Hummingbot: {e}")
            # Fallback: 直接使用 Gate.io API
            orderbook, update_id = await self._get_orderbook_with_id(formatted_pair)
        
        # ========================================
        # 提取数据
        # ========================================
        timestamp = datetime.now(timezone.utc)
        bids = orderbook.bid_entries()[:self.depth_limit]
        asks = orderbook.ask_entries()[:self.depth_limit]
        
        # 构建数据（添加 update_id）
        snapshot_data = {
            'timestamp': timestamp,
            'update_id': update_id,  # 🆕 添加 update_id
            'exchange': self.connector_name,
            'trading_pair': trading_pair,
            'best_bid_price': float(bids[0].price) if bids else None,
            'best_bid_amount': float(bids[0].amount) if bids else None,
            'best_ask_price': float(asks[0].price) if asks else None,
            'best_ask_amount': float(asks[0].amount) if asks else None,
            'bid_prices': [float(entry.price) for entry in bids],
            'bid_amounts': [float(entry.amount) for entry in bids],
            'ask_prices': [float(entry.price) for entry in asks],
            'ask_amounts': [float(entry.amount) for entry in asks],
        }
        
        await self._save_snapshot(snapshot_data)
        
        logger.debug(f"✅ {trading_pair}: Collected with update_id={update_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ {trading_pair}: {e}")
        return False


async def _get_update_id_from_api(self, formatted_pair: str) -> int:
    """
    直接调用 Gate.io API 获取 update_id
    
    用于 Hummingbot 连接器不提供 update_id 的情况
    """
    import aiohttp
    
    url = "https://api.gateio.ws/api/v4/spot/order_book"
    params = {
        "currency_pair": formatted_pair,
        "limit": 1,  # 只需要 1 档来获取 update_id
        "with_id": "true"  # 🔑 关键参数
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Gate.io API error: {response.status}")
            
            data = await response.json()
            
            if 'id' in data:
                return data['id']
            else:
                logger.warning(f"No update_id in response for {formatted_pair}")
                return None


async def _get_orderbook_with_id(self, formatted_pair: str):
    """
    直接使用 Gate.io API 获取订单簿（带 update_id）
    
    返回: (orderbook_dict, update_id)
    """
    import aiohttp
    
    url = "https://api.gateio.ws/api/v4/spot/order_book"
    params = {
        "currency_pair": formatted_pair,
        "limit": self.depth_limit,
        "with_id": "true"
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != 200:
                raise Exception(f"Gate.io API error: {response.status}")
            
            data = await response.json()
            
            # 转换为类似 Hummingbot 的格式（简化）
            class SimpleOrderBook:
                def __init__(self, bids, asks):
                    self._bids = bids
                    self._asks = asks
                
                def bid_entries(self):
                    class Entry:
                        def __init__(self, price, amount):
                            self.price = price
                            self.amount = amount
                    return [Entry(float(b[0]), float(b[1])) for b in self._bids]
                
                def ask_entries(self):
                    class Entry:
                        def __init__(self, price, amount):
                            self.price = price
                            self.amount = amount
                    return [Entry(float(a[0]), float(a[1])) for a in self._asks]
            
            orderbook = SimpleOrderBook(data['bids'], data['asks'])
            update_id = data.get('id')
            
            return orderbook, update_id
```

---

### **Step 2: 数据验证函数**

添加验证 `update_id` 的工具函数：

```python
def validate_update_ids(df: pd.DataFrame) -> dict:
    """
    验证订单簿数据的 update_id 完整性
    
    Args:
        df: 订单簿 DataFrame（包含 update_id 列）
    
    Returns:
        验证报告字典
    """
    report = {
        'total_records': len(df),
        'gaps': [],
        'duplicates': [],
        'quality_score': 100.0
    }
    
    if 'update_id' not in df.columns:
        report['error'] = 'No update_id column found'
        report['quality_score'] = 0
        return report
    
    # 检查 NaN
    null_count = df['update_id'].isna().sum()
    if null_count > 0:
        report['null_count'] = null_count
        report['quality_score'] -= (null_count / len(df)) * 50
    
    # 过滤有效的 update_id
    df_valid = df.dropna(subset=['update_id'])
    
    if len(df_valid) < 2:
        return report
    
    # 检查缺失
    for i in range(1, len(df_valid)):
        current_id = df_valid.iloc[i]['update_id']
        prev_id = df_valid.iloc[i-1]['update_id']
        
        # Gate.io REST API 的 update_id 不一定连续
        # 但我们可以检测是否递增
        if current_id <= prev_id:
            report['gaps'].append({
                'index': i,
                'timestamp': df_valid.iloc[i]['timestamp'],
                'prev_id': prev_id,
                'current_id': current_id,
                'issue': 'non-increasing' if current_id == prev_id else 'decreasing'
            })
    
    # 检查重复
    duplicate_ids = df_valid[df_valid.duplicated(subset=['update_id'], keep=False)]
    if len(duplicate_ids) > 0:
        report['duplicates'] = duplicate_ids.to_dict('records')
    
    # 计算质量评分
    issue_count = len(report['gaps']) + len(report['duplicates'])
    if issue_count > 0:
        report['quality_score'] -= min(50, (issue_count / len(df_valid)) * 100)
    
    return report


# 使用示例
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots

df = load_orderbook_snapshots('gate_io', 'IRON-USDT', '20241110', '20241116')
report = validate_update_ids(df)

print(f"📊 Update ID 验证报告")
print(f"   总记录: {report['total_records']}")
print(f"   质量评分: {report['quality_score']:.1f}/100")

if report.get('null_count', 0) > 0:
    print(f"   ⚠️ 缺失 update_id: {report['null_count']} 条")

if report['gaps']:
    print(f"   ⚠️ 异常序列: {len(report['gaps'])} 处")

if report['duplicates']:
    print(f"   ⚠️ 重复 update_id: {len(report['duplicates'])} 条")
```

---

## 📊 **数据存储格式（更新后）**

### **Parquet 文件结构**

```python
# 文件名: gate_io_IRON_USDT_20241116.parquet

timestamp                update_id   exchange  trading_pair  best_bid_price  best_ask_price
2024-11-16 12:00:00+00:00  548631456  gate_io   IRON-USDT     0.2675         0.2697
2024-11-16 12:00:05+00:00  548631789  gate_io   IRON-USDT     0.2674         0.2698
2024-11-16 12:00:10+00:00  548632001  gate_io   IRON-USDT     0.2673         0.2699
...
```

**新增字段**：
- `update_id`: Gate.io 订单簿更新序列号（类似 Crypto Lake 的 `sequence_number`）

---

## 🎯 **使用示例**

### **读取并验证数据**

```python
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots

# 读取数据
df = load_orderbook_snapshots(
    connector_name='gate_io',
    trading_pair='IRON-USDT',
    start_date='20241110',
    end_date='20241116'
)

# 检查 update_id
print(f"包含 update_id: {'update_id' in df.columns}")
print(f"Update ID 范围: {df['update_id'].min()} - {df['update_id'].max()}")
print(f"Update ID 缺失: {df['update_id'].isna().sum()} 条")

# 按 update_id 排序（确保顺序）
df_sorted = df.sort_values('update_id')

# 验证数据质量
report = validate_update_ids(df_sorted)
print(f"数据质量: {report['quality_score']:.1f}/100")
```

---

## 💡 **关键注意事项**

### **1. REST API vs WebSocket 的差异**

| 特性 | REST API | WebSocket |
|------|----------|-----------|
| **Update ID** | `id` (快照ID) | `U`/`u` (增量更新ID) |
| **连续性** | ❌ 不连续（采样） | ✅ 连续（每次变化） |
| **用途** | 定期采集快照 | 实时流式更新 |
| **频率** | 你控制（如每5秒） | 交易所推送（100ms级） |

**对于你的场景（5秒采集）**：REST API 的 `id` 足够了！

### **2. 必须使用 `with_id=true`**

```python
# ❌ 错误：没有 update_id
response = requests.get(
    "https://api.gateio.ws/api/v4/spot/order_book",
    params={"currency_pair": "BTC_USDT"}
)

# ✅ 正确：包含 update_id
response = requests.get(
    "https://api.gateio.ws/api/v4/spot/order_book",
    params={
        "currency_pair": "BTC_USDT",
        "with_id": "true"  # 🔑 关键
    }
)
```

### **3. Update ID 的递增性**

```python
# Gate.io REST API 的 update_id 不保证连续
# 但保证递增（新的快照总是有更大的 id）

ID 序列: 100 → 150 → 200 → 205 → 300
         ↑     ↑     ↑     ↑     ↑
      合理  合理  合理  合理  合理

ID 序列: 100 → 150 → 140 ← ❌ 异常（递减）
ID 序列: 100 → 150 → 150 ← ⚠️ 重复（可能的网络问题）
```

---

## 🚀 **下一步行动**

### **1. 运行测试脚本**

```bash
python scripts/test_gateio_orderbook_structure.py
```

这会显示：
- ✅ Gate.io API 的实际返回数据
- ✅ `update_id` 字段的值
- ✅ Hummingbot 连接器的支持情况

### **2. 修改 OrderBookSnapshotTask**

根据测试结果，更新 `app/tasks/data_collection/orderbook_snapshot_task.py`：
- 添加 `update_id` 字段采集
- 实现 fallback 逻辑（Hummingbot vs 直接API）

### **3. 重新采集数据**

```bash
# 停止旧的采集任务
sudo systemctl stop orderbook-collector

# 清理旧数据（可选）
rm -rf app/data/raw/orderbook_snapshots/*

# 启动新的采集任务
sudo systemctl start orderbook-collector
```

### **4. 验证新数据**

```python
# 读取新采集的数据
df = load_orderbook_snapshots('gate_io', 'IRON-USDT')

# 验证 update_id
assert 'update_id' in df.columns, "缺少 update_id 列"
assert df['update_id'].notna().all(), "存在 null update_id"

print("✅ 数据包含有效的 update_id!")
```

---

## 📚 **参考资料**

- [Gate.io REST API 文档](https://www.gate.io/docs/developers/apiv4/en/#retrieve-order-book)
- [Gate.io WebSocket 文档](https://www.gate.io/docs/developers/apiv4/ws/en/#order-book-channel)
- [Crypto Lake 数据格式](https://crypto-lake.com/docs/schema)

---

**🎉 现在你知道如何在 QuantsLab 中添加 Gate.io 的 `update_id` 了！** 

这将让你的订单簿数据具有**可追踪性和完整性验证能力**，就像 Crypto Lake 的 `sequence_number` 一样！✨

