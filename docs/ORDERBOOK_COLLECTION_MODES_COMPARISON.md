# Orderbook Data Collection - 全模式对比

## 📊 概览

QuantsLab 现在支持多种 orderbook 数据采集模式，适用于不同的交易场景和性能需求。

## 🎯 可用模式

| 模式 | 交易所 | 协议 | 格式 | 频率 | 数据量 | 适用场景 |
|------|--------|------|------|------|--------|----------|
| **Tick Diff (WebSocket)** | Gate.io | WS | JSON | 实时 | 最大 | 高频交易、做市 |
| **Tick Diff (WebSocket)** | MEXC | WS | Protobuf | 100ms | 大 | 高频交易、做市 |
| **Snapshot (REST)** | Gate.io | HTTP | JSON | 可配置 | 中 | 回测、监控 |
| **Snapshot (REST)** | MEXC | HTTP | JSON | 10s | 中 | 回测、监控 |

## 📐 详细对比

### 1. WebSocket Tick Diff 模式

#### Gate.io WebSocket

```yaml
# config/orderbook_tick_gateio.yml
tasks:
  orderbook_tick_gateio:
    config:
      connector_name: "gate_io"
      trading_pairs:
        - "BTC-USDT"
        - "ETH-USDT"
```

**特点:**
- ✅ 超高频：< 100ms 延迟
- ✅ JSON 格式：易于调试
- ✅ 增量更新：diff 数据
- ✅ 序列号：gap 检测
- ✅ 符号格式：`BTC-USDT` (带连字符)

**数据示例:**
```json
{
  "channel": "spot.order_book_update",
  "event": "update",
  "result": {
    "s": "BTC_USDT",
    "u": 48776310,
    "b": [["10000.1", "0.1"]],
    "a": [["10001.1", "0.1"]]
  }
}
```

#### MEXC WebSocket (新增! 🎉)

```yaml
# config/orderbook_tick_mexc_websocket.yml
tasks:
  orderbook_tick_mexc:
    config:
      connector_name: "mexc"
      trading_pairs:
        - "BTCUSDT"
        - "ETHUSDT"
```

**特点:**
- ✅ 高频：100ms 批次
- ✅ Protobuf 格式：高效二进制
- ✅ 增量更新：diff 数据
- ✅ 版本号：fromVersion/toVersion
- ✅ 符号格式：`BTCUSDT` (无连字符)

**数据示例 (解析后):**
```python
{
  "channel": "spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT",
  "symbol": "BTCUSDT",
  "sendtime": 1736411507002,
  "result": {
    "bids": [["92877.58", "123.45"]],
    "asks": [["92880.12", "67.89"]],
    "fromVersion": "10589632359",
    "toVersion": "10589632360"
  }
}
```

### 2. REST Snapshot 模式

#### Gate.io REST

```yaml
# config/orderbook_snapshot_gateio.yml
tasks:
  orderbook_snapshot_gateio:
    schedule:
      frequency_hours: 0.000278  # 1秒
    config:
      connector_name: "gate_io"
      depth_limit: 100
```

**特点:**
- ✅ 可配置频率：1秒-1小时
- ✅ 完整快照：每次全量数据
- ✅ 简单稳定：HTTP 请求
- ✅ 易于实现：REST API

#### MEXC REST

```yaml
# config/orderbook_tick_mexc.yml  (实际是 REST snapshot)
tasks:
  orderbook_snapshot_mexc:
    schedule:
      frequency_hours: 0.002778  # 10秒
    config:
      connector_name: "mexc"
      depth_limit: 100
```

**特点:**
- ✅ 高频快照：10秒间隔
- ✅ 完整数据：100档深度
- ✅ 稳定可靠：REST API
- ✅ 易于部署：无需 WebSocket

## 🔍 数据格式对比

### Long-table vs Wide-table

#### Long-table (WebSocket Tick Diff)

```
timestamp            | exchange | trading_pair | update_id | side | price   | amount
---------------------|----------|--------------|-----------|------|---------|--------
2025-11-19 10:00:00  | gate_io  | BTC-USDT     | 123456    | bid  | 10000.1 | 0.5
2025-11-19 10:00:00  | gate_io  | BTC-USDT     | 123456    | bid  | 10000.0 | 0.0
2025-11-19 10:00:00  | gate_io  | BTC-USDT     | 123456    | ask  | 10001.0 | 0.3
```

**优势:**
- 每行 = 一个价格档位变化
- 增量更新高效
- 查询速度快
- 易于时间序列分析

#### Wide-table (REST Snapshot)

```
timestamp            | exchange | symbol    | bids                      | asks                      
---------------------|----------|-----------|---------------------------|---------------------------
2025-11-19 10:00:00  | mexc     | BTCUSDT   | [[10000, 0.5], [9999...]] | [[10001, 0.3], [10002...]]
```

**优势:**
- 每行 = 完整 orderbook
- 数据完整性好
- 易于重建 orderbook
- 适合低频场景

## 📊 性能对比

### 数据密度

```
模式                      | 更新频率      | 数据点/分钟 | 数据量级
--------------------------|---------------|-------------|----------
Gate.io WebSocket Tick    | < 100ms       | 600+        | 最大
MEXC WebSocket Tick       | 100ms         | 600         | 大
Gate.io REST Snapshot     | 1-60秒        | 1-60        | 中
MEXC REST Snapshot        | 10秒          | 6           | 中
```

### 带宽占用

```
模式                      | 消息格式  | 单条大小   | 带宽/小时
--------------------------|-----------|------------|----------
Gate.io WebSocket         | JSON      | ~500 bytes | ~1 GB
MEXC WebSocket            | Protobuf  | ~200 bytes | ~400 MB
Gate.io REST              | JSON      | ~5 KB      | ~1-18 MB
MEXC REST                 | JSON      | ~5 KB      | ~10 MB
```

### 延迟

```
模式                      | 网络延迟 | 处理延迟 | 总延迟
--------------------------|----------|----------|--------
WebSocket (实时)          | 10-50ms  | < 5ms    | < 100ms
REST (轮询)               | 50-200ms | < 5ms    | 取决于频率
```

## 🎯 使用场景建议

### 高频交易 / 做市策略

**推荐:** WebSocket Tick Diff

```bash
# 最高性能：Gate.io WebSocket
python cli.py run-tasks --config config/orderbook_tick_gateio.yml

# 或 MEXC WebSocket (如果交易对在 MEXC)
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml
```

**原因:**
- ✅ 实时更新 (< 100ms)
- ✅ 最低延迟
- ✅ 完整的 gap 检测
- ✅ 高数据密度

### 策略回测 / 研究分析

**推荐:** REST Snapshot (中频)

```bash
# Gate.io: 每5秒一次快照
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
# (修改 frequency_hours: 0.001389)

# MEXC: 每10秒一次快照
python cli.py run-tasks --config config/orderbook_tick_mexc.yml
```

**原因:**
- ✅ 数据完整性好
- ✅ 易于重建 orderbook
- ✅ 存储空间合理
- ✅ 足够的时间分辨率

### 市场监控 / 价格追踪

**推荐:** REST Snapshot (低频)

```bash
# 每分钟一次
# frequency_hours: 0.016667
```

**原因:**
- ✅ 低资源占用
- ✅ 稳定可靠
- ✅ 易于部署
- ✅ 满足监控需求

## 🔧 模式切换

### 从 REST 迁移到 WebSocket

**场景:** 研究阶段使用 REST，生产环境切换到 WebSocket

**步骤:**
```bash
# 1. 停止 REST 采集
pkill -f orderbook_snapshot_mexc

# 2. 启动 WebSocket 采集
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml

# 3. 数据读取兼容（统一的 OrderBookTick 格式）
import pyarrow.parquet as pq
df = pq.read_table('app/data/raw/orderbook_ticks/mexc_BTCUSDT_*').to_pandas()
```

### 多模式并行

**场景:** 同时采集多个交易所，使用不同模式

```bash
# Terminal 1: Gate.io WebSocket (最高频)
python cli.py run-tasks --config config/orderbook_tick_gateio.yml

# Terminal 2: MEXC WebSocket (高频)
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml

# Terminal 3: 其他交易所 REST (中频)
python cli.py run-tasks --config config/orderbook_snapshot_other.yml
```

## 📝 配置模板

### 高频 WebSocket 配置

```yaml
tasks:
  orderbook_tick_high_freq:
    enabled: true
    task_class: app.tasks.data_collection.orderbook_tick_collector.OrderBookTickCollector
    
    schedule:
      type: continuous
    
    config:
      connector_name: "mexc"  # or "gate_io"
      trading_pairs: ["BTCUSDT", "ETHUSDT"]
      buffer_size: 500         # 小缓冲，快速写入
      flush_interval: 30       # 30秒刷新
      gap_warning_threshold: 20
```

### 中频 REST 配置

```yaml
tasks:
  orderbook_snapshot_mid_freq:
    enabled: true
    task_class: app.tasks.data_collection.orderbook_snapshot_task.OrderBookSnapshotTask
    
    schedule:
      type: frequency
      frequency_hours: 0.001389  # 5秒
    
    config:
      connector_name: "mexc"  # or "gate_io"
      trading_pairs: ["BTCUSDT", "ETHUSDT"]
      depth_limit: 100
```

## 🎉 总结

### 当前支持矩阵

|  | Gate.io | MEXC |
|---|---------|------|
| **WebSocket Tick** | ✅ | ✅ (新增!) |
| **REST Snapshot** | ✅ | ✅ |
| **数据格式统一** | ✅ | ✅ |
| **Gap 检测** | ✅ | ✅ |
| **生产就绪** | ✅ | ✅ |

### 技术亮点

1. **统一架构**
   - 一套代码，多种模式
   - 统一的数据格式输出
   - 易于扩展

2. **灵活部署**
   - WebSocket 实时流
   - REST 定时快照
   - 可并行运行

3. **高性能**
   - Protobuf 二进制格式
   - Multi-part Parquet
   - 增量追加写入

4. **生产级**
   - 完善的错误处理
   - 序列号 gap 检测
   - 详细的日志和监控

---

**最后更新:** 2025-11-19  
**支持的交易所:** Gate.io, MEXC  
**支持的模式:** WebSocket Tick (2), REST Snapshot (2)  
**状态:** ✅ Production Ready

