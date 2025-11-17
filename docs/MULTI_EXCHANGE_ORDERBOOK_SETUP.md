# 📊 多交易所订单簿采集设置指南

> **支持 Gate.io 和 MEXC 同时采集订单簿数据**

---

## 🎯 配置总览

### **你的采集配置**

| 交易所 | 交易对数量 | 交易对列表 |
|--------|-----------|-----------|
| **Gate.io** | 6 个 | VIRTUAL-USDT, LMTS-USDT, BNKR-USDT, PRO-USDT, IRON-USDT, MIGGLES-USDT |
| **MEXC** | 3 个 | AUKI-USDT, SERV-USDT, IRON-USDT |
| **总计** | 9 个 | 2 个交易所 |

---

## 📁 配置文件

### **1. Gate.io 配置**

**文件**: `config/orderbook_snapshot_gateio.yml`

```yaml
tasks:
  orderbook_snapshot_gateio:
    enabled: true
    task_class: app.tasks.data_collection.orderbook_snapshot_task.OrderBookSnapshotTask
    
    schedule:
      type: frequency
      frequency_seconds: 5  # 每5秒采集一次
      timezone: UTC
    
    config:
      connector_name: "gate_io"
      trading_pairs:
        - "VIRTUAL-USDT"
        - "LMTS-USDT"
        - "BNKR-USDT"
        - "PRO-USDT"
        - "IRON-USDT"
        - "MIGGLES-USDT"
      depth_limit: 100
```

### **2. MEXC 配置**

**文件**: `config/orderbook_snapshot_mexc.yml`

```yaml
tasks:
  orderbook_snapshot_mexc:
    enabled: true
    task_class: app.tasks.data_collection.orderbook_snapshot_task.OrderBookSnapshotTask
    
    schedule:
      type: frequency
      frequency_seconds: 5  # 每5秒采集一次
      timezone: UTC
    
    config:
      connector_name: "mexc"
      trading_pairs:
        - "AUKI-USDT"
        - "SERV-USDT"
        - "IRON-USDT"
      depth_limit: 100
```

---

## 🔧 代码更新

### **支持的交易所**

| 交易所 | API 端点 | 格式 | Update ID 字段 |
|--------|---------|------|---------------|
| **Gate.io** | `api.gateio.ws/api/v4/spot/order_book` | BTC_USDT | `id` |
| **MEXC** | `api.mexc.com/api/v3/depth` | BTCUSDT | `lastUpdateId` |

### **交易对格式转换**

```python
# 配置文件中统一使用: "BTC-USDT"

# Gate.io: BTC-USDT → BTC_USDT
formatted_pair = trading_pair.replace('-', '_')

# MEXC: BTC-USDT → BTCUSDT
formatted_pair = trading_pair.replace('-', '')
```

### **数据格式统一**

所有交易所的返回数据都统一为：

```python
{
    'id': 548631456,           # update_id (序列号)
    'bids': [["price", "amount"], ...],
    'asks': [["price", "amount"], ...]
}
```

---

## 🚀 启动采集

### **方式 1: 单独启动**

```bash
# 启动 Gate.io 采集
python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml

# 在另一个终端启动 MEXC 采集
python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
```

### **方式 2: systemd 服务（推荐）**

#### **创建 Gate.io 服务**

```bash
sudo nano /etc/systemd/system/orderbook-gateio.service
```

```ini
[Unit]
Description=OrderBook Collection - Gate.io
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/home/alice/quants-lab
ExecStart=/home/alice/miniconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_gateio.yml
Restart=always
RestartSec=10
StandardOutput=append:/home/alice/quants-lab/logs/orderbook_gateio.log
StandardError=append:/home/alice/quants-lab/logs/orderbook_gateio.log

[Install]
WantedBy=multi-user.target
```

#### **创建 MEXC 服务**

```bash
sudo nano /etc/systemd/system/orderbook-mexc.service
```

```ini
[Unit]
Description=OrderBook Collection - MEXC
After=network.target

[Service]
Type=simple
User=alice
WorkingDirectory=/home/alice/quants-lab
ExecStart=/home/alice/miniconda3/envs/quants-lab/bin/python cli.py run-tasks --config config/orderbook_snapshot_mexc.yml
Restart=always
RestartSec=10
StandardOutput=append:/home/alice/quants-lab/logs/orderbook_mexc.log
StandardError=append:/home/alice/quants-lab/logs/orderbook_mexc.log

[Install]
WantedBy=multi-user.target
```

#### **启动服务**

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start orderbook-gateio
sudo systemctl start orderbook-mexc

# 设置开机自启
sudo systemctl enable orderbook-gateio
sudo systemctl enable orderbook-mexc

# 查看状态
sudo systemctl status orderbook-gateio
sudo systemctl status orderbook-mexc
```

---

## 📊 监控和验证

### **查看实时日志**

```bash
# Gate.io 日志
tail -f ~/quants-lab/logs/orderbook_gateio.log

# MEXC 日志
tail -f ~/quants-lab/logs/orderbook_mexc.log
```

### **验证数据采集**

```python
from app.tasks.data_collection.orderbook_snapshot_task import load_orderbook_snapshots

# 验证 Gate.io 数据
df_gateio_virtual = load_orderbook_snapshots('gate_io', 'VIRTUAL-USDT')
df_gateio_iron = load_orderbook_snapshots('gate_io', 'IRON-USDT')

print(f"Gate.io VIRTUAL-USDT: {len(df_gateio_virtual)} 条记录")
print(f"Gate.io IRON-USDT: {len(df_gateio_iron)} 条记录")

# 验证 MEXC 数据
df_mexc_auki = load_orderbook_snapshots('mexc', 'AUKI-USDT')
df_mexc_iron = load_orderbook_snapshots('mexc', 'IRON-USDT')

print(f"MEXC AUKI-USDT: {len(df_mexc_auki)} 条记录")
print(f"MEXC IRON-USDT: {len(df_mexc_iron)} 条记录")

# 检查 update_id
print(f"\nGate.io IRON Update ID 范围: {df_gateio_iron['update_id'].min()} - {df_gateio_iron['update_id'].max()}")
print(f"MEXC IRON Update ID 范围: {df_mexc_iron['update_id'].min()} - {df_mexc_iron['update_id'].max()}")
```

---

## 📈 速率限制分析

### **Gate.io**

```
配置：6 个交易对，每 5 秒采集一次
请求量：6 次/5秒 = 12 次/10秒
限制：100 次/10秒
使用率：12% ✅ 非常安全
```

### **MEXC**

```
配置：3 个交易对，每 5 秒采集一次
请求量：3 次/5秒 = 6 次/10秒
限制：50 次/秒（MEXC 限制）
使用率：<1% ✅ 非常安全
```

### **总计**

```
总交易对：9 个
总请求量：18 次/10秒
两个交易所独立限制，不冲突 ✅
```

---

## 💾 数据存储

### **存储位置**

```
app/data/raw/orderbook_snapshots/
├── gate_io_VIRTUAL_USDT_20241116.parquet
├── gate_io_LMTS_USDT_20241116.parquet
├── gate_io_BNKR_USDT_20241116.parquet
├── gate_io_PRO_USDT_20241116.parquet
├── gate_io_IRON_USDT_20241116.parquet
├── gate_io_MIGGLES_USDT_20241116.parquet
├── mexc_AUKI_USDT_20241116.parquet
├── mexc_SERV_USDT_20241116.parquet
└── mexc_IRON_USDT_20241116.parquet
```

### **数据格式**

```python
# 统一的数据结构
{
    'timestamp': datetime,
    'update_id': 548631456,    # Gate.io: id, MEXC: lastUpdateId
    'exchange': 'gate_io' or 'mexc',
    'trading_pair': 'IRON-USDT',
    'best_bid_price': 0.2675,
    'best_ask_price': 0.2697,
    'bid_prices': [...],
    'ask_prices': [...]
}
```

---

## ⚠️ 重要提示

### **1. IRON-USDT 在两个交易所都有**

- Gate.io: `gate_io_IRON_USDT_*.parquet`
- MEXC: `mexc_IRON_USDT_*.parquet`

读取时需要指定交易所：

```python
# Gate.io 的 IRON-USDT
df_gate = load_orderbook_snapshots('gate_io', 'IRON-USDT')

# MEXC 的 IRON-USDT
df_mexc = load_orderbook_snapshots('mexc', 'IRON-USDT')
```

### **2. API Key**

- ✅ Gate.io：无需 API Key（公共 API）
- ✅ MEXC：无需 API Key（公共 API）

### **3. 并发控制**

每个交易所独立使用 `Semaphore(8)`，不会互相干扰。

---

## 🧪 测试

### **创建测试脚本**

```bash
python scripts/test_multi_exchange_orderbook.py
```

---

## ✅ 检查清单

启动前确认：
- [ ] 配置文件已更新（Gate.io 6个，MEXC 3个）
- [ ] 代码已支持 MEXC
- [ ] 日志目录已创建
- [ ] systemd 服务已配置

启动后验证：
- [ ] Gate.io 服务正常运行
- [ ] MEXC 服务正常运行
- [ ] 数据文件正在生成
- [ ] update_id 正常递增
- [ ] 无错误日志

---

## 📚 相关文档

- [Gate.io API 文档](https://www.gate.io/docs/developers/apiv4/)
- [MEXC API 文档](https://mexcdevelop.github.io/apidocs/spot_v3_en/)
- [订单簿数据结构](ORDERBOOK_UPDATE_ID_CHANGELOG.md)

---

**🎉 配置完成！现在你可以同时从 Gate.io 和 MEXC 采集订单簿数据！** ✨

