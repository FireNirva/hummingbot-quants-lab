# MEXC WebSocket + Protobuf 实现指南

## 📋 概述

根据 MEXC 官方文档，WebSocket API 使用 **Protocol Buffers (protobuf)** 格式推送数据，这比标准 JSON 格式复杂。

## 🔑 关键信息

### WebSocket 端点
```
正确: wss://wbs-api.mexc.com/ws
错误: wss://wbs.mexc.com/ws  ⬅️ 之前用错了！
```

### 订阅格式

#### 增量深度更新（推荐）
```json
{
    "method": "SUBSCRIPTION",
    "params": ["spot@public.aggre.depth.v3.api.pb@100ms@BTCUSDT"]
}
```

#### 限量深度快照（5/10/20档）
```json
{
    "method": "SUBSCRIPTION",
    "params": ["spot@public.limit.depth.v3.api.pb@BTCUSDT@20"]
}
```

## 🚨 重大挑战：Protobuf 格式

### 问题

MEXC WebSocket 不推送 JSON，而是推送二进制 protobuf 数据：

```python
# 普通交易所 (Gate.io)
{"channel": "spot.order_book_update", "bids": [...]}  # JSON 格式 ✅

# MEXC
b'\x08\x01\x12\x1c\x08\x02\x10...'  # 二进制 protobuf ❌ 需要特殊解析
```

### 实现复杂度

| 步骤 | 复杂度 | 说明 |
|------|--------|------|
| 1. 下载 .proto 文件 | ⭐ | https://github.com/mexcdevelop/websocket-proto |
| 2. 安装 protobuf 编译器 | ⭐⭐ | `pip install protobuf` + protoc 工具 |
| 3. 生成 Python 代码 | ⭐⭐ | `protoc *.proto --python_out=.` |
| 4. 集成到现有代码 | ⭐⭐⭐ | 修改 WebSocketClient 解析逻辑 |
| 5. 测试和调试 | ⭐⭐⭐ | 二进制数据难以调试 |

## 🎯 推荐方案对比

### 方案 A：REST 高频轮询（当前方案）✅

```yaml
优势:
├─ ✅ 实现简单，无需 protobuf
├─ ✅ 稳定可靠，易于调试
├─ ✅ 10秒频率足够大多数场景
└─ ✅ 已测试通过，生产就绪

劣势:
└─ ⚠️ 延迟较高（10秒 vs 100ms）

适用场景:
├─ 套利分析（10秒足够）
├─ 流动性监控
├─ 中低频交易策略
└─ 数据收集和分析
```

### 方案 B：WebSocket + Protobuf（高级方案）⚡

```yaml
优势:
├─ ✅ 实时性好（100ms更新）
├─ ✅ 数据粒度细
└─ ✅ 与 Gate.io 模式一致

劣势:
├─ ❌ 实现复杂度高
├─ ❌ 需要 protobuf 依赖
├─ ❌ 调试困难
├─ ❌ 维护成本高
└─ ❌ 开发时间长（估计2-3天）

适用场景:
├─ 超高频交易
├─ 市场微观结构研究
└─ 对延迟极度敏感的应用
```

## 💡 建议

### 短期（立即可用）

**继续使用 REST 模式**，因为：

1. ✅ **已经工作**：测试通过，可立即使用
2. ✅ **足够用**：10秒对大多数应用足够
3. ✅ **稳定性**：REST API 比 WebSocket 更可靠
4. ✅ **易维护**：团队熟悉 REST，调试简单

```bash
# 立即开始使用
python cli.py run-tasks --config config/orderbook_tick_mexc.yml
```

### 长期（可选升级）

如果未来确实需要 100ms 实时数据，可以实现 WebSocket + Protobuf 方案。

## 📝 如果要实现 WebSocket + Protobuf

### 1. 安装依赖

```bash
# 安装 protobuf
pip install protobuf

# 安装 protoc 编译器（macOS）
brew install protobuf
```

### 2. 下载 .proto 文件

```bash
git clone https://github.com/mexcdevelop/websocket-proto
cd websocket-proto
```

### 3. 生成 Python 代码

```bash
protoc *.proto --python_out=core/data_sources/mexc_proto/
```

### 4. 修改 WebSocketClient

```python
# core/data_sources/websocket_client.py

import core.data_sources.mexc_proto.PushDataV3ApiWrapper_pb2 as mexc_proto

async def _message_loop(self):
    while self.running:
        message_bytes = await self.ws.recv()
        
        if self.exchange == "mexc":
            # Protobuf 解析
            wrapper = mexc_proto.PushDataV3ApiWrapper()
            wrapper.ParseFromString(message_bytes)
            
            # 转换为字典
            message = {
                'channel': wrapper.channel,
                'symbol': wrapper.symbol,
                'sendtime': wrapper.sendTime,
                # ... 解析 bids/asks
            }
        else:
            # JSON 解析（Gate.io）
            message = json.loads(message_bytes)
        
        await self.on_message(message)
```

### 5. 更新配置

```yaml
# config/orderbook_tick_mexc_websocket.yml
config:
  connector_name: "mexc"
  use_websocket: true  # 启用 WebSocket
  websocket_format: "protobuf"  # 使用 protobuf
```

## 📊 性能对比（预估）

| 指标 | REST 模式 | WebSocket + Protobuf |
|------|-----------|----------------------|
| 延迟 | 10秒 | 100ms |
| 实现时间 | ✅ 完成 | ~2-3天 |
| 复杂度 | ⭐ | ⭐⭐⭐⭐ |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 维护成本 | 低 | 高 |
| 数据量 | 适中 | 大 |
| 带宽消耗 | 低 | 中 |

## 🎓 最佳实践

### 何时使用 REST 模式

✅ **推荐使用 REST 的场景**：
- 套利监控（价差变化 > 1秒可接受）
- 流动性分析
- 每日数据报表
- 回测数据收集
- 中低频交易策略

### 何时需要 WebSocket

⚡ **必须使用 WebSocket 的场景**：
- 高频交易（订单响应 < 1秒）
- 市场微观结构研究
- Tick-by-tick 分析
- 毫秒级套利

## 🔮 未来路线图

### Phase 1: REST 模式（已完成）✅
- [x] REST API 集成
- [x] 10秒高频采集
- [x] 测试验证
- [x] 文档完善

### Phase 2: WebSocket + JSON（可选）
- [ ] 尝试其他 WebSocket 端点
- [ ] 探索是否有 JSON 格式的流

### Phase 3: WebSocket + Protobuf（高级）
- [ ] Protobuf 集成
- [ ] 100ms 实时采集
- [ ] 性能优化

## 📚 参考资料

- [MEXC WebSocket 官方文档](https://mexcdevelop.github.io/apidocs/spot_v3_en/#websocket-market-streams)
- [MEXC Protobuf 文件](https://github.com/mexcdevelop/websocket-proto)
- [Protocol Buffers 官方文档](https://developers.google.com/protocol-buffers)

## ✅ 结论

**当前的 REST 模式是最佳选择**：

1. ✅ 已经工作且测试通过
2. ✅ 满足90%的应用场景
3. ✅ 易于维护和调试
4. ✅ 生产就绪

**WebSocket + Protobuf 可以作为未来优化**，但非必需。

---

最后更新: 2024-11-19  
作者: Alice  
状态: REST 模式生产就绪，WebSocket 方案待实现

