# 数据完整性与恢复机制

## 📋 目录
1. [中断时会发生什么](#中断时会发生什么)
2. [数据损坏风险分析](#数据损坏风险分析)
3. [重新运行的影响](#重新运行的影响)
4. [最佳实践建议](#最佳实践建议)

---

## 🔍 中断时会发生什么

### 正常停止（Ctrl+C）

✅ **安全的停止方式**

```python
# 代码逻辑（orderbook_tick_collector.py）
try:
    # 数据收集循环
    while True:
        await self._stream_loop()
except asyncio.CancelledError:
    logger.info("Task cancelled, shutting down gracefully")
    return {"status": "cancelled"}
finally:
    # cleanup() 方法会被自动调用
    await self.writer.flush_all()  # 刷新所有缓冲区
    await self.ws_client.close()    # 关闭 WebSocket
```

**结果**：
- ✅ 内存中的缓冲数据会被写入磁盘
- ✅ WebSocket 连接正常关闭
- ✅ 已写入的文件完全正常
- ✅ **无数据丢失，无文件损坏**

### 强制终止（Kill -9 或系统崩溃）

⚠️ **非正常停止**

**影响**：
- ❌ 内存缓冲区中的数据会丢失
- ✅ 已经写入磁盘的文件**完全正常**（Parquet 文件已完整）
- ❌ 最后一个 buffer 的数据可能丢失（最多损失 buffer_size 条数据）

**损失估算**：

| 配置 | Buffer Size | Flush Interval | 最大数据损失 |
|------|-------------|----------------|--------------|
| **Gate.io** | 100 条 | 10 秒 | ≤ 100 条或 10 秒数据 |
| **MEXC** | 1000 条 | 60 秒 | ≤ 1000 条或 60 秒数据 |

**为什么损失很小？**
- 系统采用双重触发机制：达到 buffer_size **或** flush_interval 就写入
- 数据会持续写入，不会累积太多

---

## 💾 数据损坏风险分析

### 已完成的 Parquet 文件

✅ **完全安全**

```python
# tick_orderbook_writer.py - flush_buffer() 方法
pq.write_table(
    table,
    part_path,
    compression='snappy',
    use_dictionary=True,
    write_statistics=True
)
```

**Parquet 文件特性**：
- ✅ 原子性写入：要么完全成功，要么完全失败
- ✅ 已完成的文件具有完整的文件头和元数据
- ✅ 中断不会损坏已写入的文件

**实际情况**：
```
app/data/raw/orderbook_ticks/mexc_AUKIUSDT_20251119/
├── part_00001.parquet  ← 完整文件，6.8 KB ✅
├── part_00002.parquet  ← 完整文件，6.7 KB ✅
└── part_00003.parquet  ← 正在写入... ⚠️
```

- ✅ `part_00001.parquet` 和 `part_00002.parquet` **绝对安全**
- ⚠️ 如果在写入 `part_00003.parquet` 时中断：
  - 最坏情况：文件不完整或不存在
  - 损失：最多 buffer_size 条数据
  - 影响：可以删除这个文件，其他文件完全正常

### Parquet 文件的错误检测

如果文件损坏，读取时会报错：

```python
try:
    df = pd.read_parquet('part_00003.parquet')
except Exception as e:
    # 错误示例：
    # "Parquet magic bytes not found in footer"
    # "Invalid parquet file"
    print(f"文件损坏: {e}")
    # 解决方法：删除这个损坏的文件即可
```

---

## 🔄 重新运行的影响

### 文件命名策略

系统使用**递增计数器**来避免覆盖：

```python
# tick_orderbook_writer.py
self.part_counters[key] += 1  # 递增计数器
part_num = self.part_counters[key]
part_filename = f"part_{part_num:05d}.parquet"  # part_00001, part_00002, ...
```

### 同一天重新运行

**场景 1：接续运行（推荐）**

```bash
# 第一次运行（09:00-10:00）
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml
# 生成：part_00001.parquet, part_00002.parquet

# 停止后重新运行（10:05-11:00）
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml
# 生成：part_00003.parquet, part_00004.parquet  ← 从 00003 开始！
```

⚠️ **重要**：计数器**从内存重置**！

```python
self.part_counters: Dict[Tuple[str, str, str], int] = {}  # 内存中的计数器
```

**实际行为**：
- 第一次运行：`part_00001`, `part_00002`, ...
- 重新启动后：计数器从 0 开始，会**尝试覆盖** `part_00001`！

### ⚠️ 数据覆盖风险

**如果同一天内重新运行**：

```
第一次运行：
  part_00001.parquet  (09:00-09:05)  ← 原始数据
  part_00002.parquet  (09:05-09:10)
  
第二次运行（重启后）：
  part_00001.parquet  (10:00-10:05)  ← 覆盖了原始数据！⚠️
  part_00002.parquet  (10:05-10:10)  ← 覆盖了原始数据！⚠️
```

---

## 🛡️ 最佳实践建议

### 1. 正确停止任务

✅ **推荐**：使用 `Ctrl+C` 正常停止
```bash
# 在运行的 Terminal 中按 Ctrl+C
# 等待看到：
# INFO: All buffers flushed
# INFO: Cleanup complete
```

❌ **不推荐**：
- `Ctrl+Z` - 只是暂停，不会清理
- `kill -9 <PID>` - 强制杀掉，数据丢失
- 直接关闭 Terminal - 可能丢失数据

### 2. 避免同日重复运行

**方案 A：使用不同的配置文件**

```yaml
# config/orderbook_tick_mexc_morning.yml
config:
  output_dir: "app/data/raw/orderbook_ticks_morning"  # 不同的目录

# config/orderbook_tick_mexc_afternoon.yml
config:
  output_dir: "app/data/raw/orderbook_ticks_afternoon"  # 不同的目录
```

**方案 B：先备份现有数据**

```bash
# 重新运行前备份
cd app/data/raw/orderbook_ticks
mv mexc_AUKIUSDT_20251119 mexc_AUKIUSDT_20251119_backup_$(date +%H%M%S)

# 然后重新运行
python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml
```

**方案 C：检查并续接（最佳）**

```bash
# 检查最大的 part 编号
ls app/data/raw/orderbook_ticks/mexc_AUKIUSDT_20251119/ | sort | tail -1
# 输出：part_00023.parquet

# 手动修改代码，从 24 开始（不推荐）
# 或者直接连续运行，让系统自动管理
```

### 3. 数据验证脚本

创建一个验证脚本来检查文件完整性：

```python
#!/usr/bin/env python3
"""
验证 Parquet 文件完整性
"""
import pandas as pd
from pathlib import Path

def check_parquet_files(directory):
    """检查目录中所有 parquet 文件"""
    corrupted = []
    valid = []
    
    for file in Path(directory).glob("**/*.parquet"):
        try:
            df = pd.read_parquet(file)
            valid.append((file, len(df)))
            print(f"✅ {file.name}: {len(df)} rows")
        except Exception as e:
            corrupted.append((file, str(e)))
            print(f"❌ {file.name}: {e}")
    
    print(f"\n📊 总计: {len(valid)} 个正常, {len(corrupted)} 个损坏")
    
    if corrupted:
        print("\n⚠️ 损坏的文件：")
        for file, error in corrupted:
            print(f"   {file}: {error}")
            print(f"   建议: rm '{file}'")

if __name__ == "__main__":
    check_parquet_files("app/data/raw/orderbook_ticks")
```

### 4. 长期运行建议

**每天自动重启（推荐）**

```bash
# 使用 cron job 每天凌晨重启
0 0 * * * cd /path/to/quants-lab && pkill -f "orderbook_tick_mexc" && sleep 5 && python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml >> logs/mexc_$(date +\%Y\%m\%d).log 2>&1 &
```

**使用 systemd 或 supervisor 管理**

```ini
# /etc/supervisor/conf.d/mexc_tick_collector.conf
[program:mexc_tick_collector]
command=/path/to/python cli.py run-tasks --config config/orderbook_tick_mexc_websocket.yml
directory=/path/to/quants-lab
user=alice
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
```

### 5. 监控和告警

**检测数据流中断**

```python
# 监控最后更新时间
import os
from datetime import datetime, timedelta

def check_data_freshness(directory, max_age_minutes=5):
    """检查数据是否新鲜"""
    latest_file = max(Path(directory).glob("**/*.parquet"), 
                     key=os.path.getmtime)
    
    file_age = datetime.now() - datetime.fromtimestamp(latest_file.stat().st_mtime)
    
    if file_age > timedelta(minutes=max_age_minutes):
        print(f"⚠️ 数据过期: {latest_file.name} ({file_age.seconds}秒前)")
        # 发送告警
    else:
        print(f"✅ 数据新鲜: {latest_file.name}")
```

---

## 📊 总结

### 数据安全性

| 场景 | 已写入文件 | 缓冲区数据 | 总体风险 |
|------|-----------|-----------|----------|
| **正常停止 (Ctrl+C)** | ✅ 完全安全 | ✅ 自动刷新 | 🟢 **无风险** |
| **强制终止 (Kill -9)** | ✅ 完全安全 | ❌ 丢失 | 🟡 **低风险** |
| **系统崩溃** | ✅ 完全安全 | ❌ 丢失 | 🟡 **低风险** |
| **同日重启** | ⚠️ 可能覆盖 | ✅ 正常 | 🟠 **中风险** |

### 关键要点

1. ✅ **已写入的 Parquet 文件完全安全**，不会损坏
2. ⚠️ **缓冲区数据可能丢失**（最多 buffer_size 条）
3. ⚠️ **同日重启可能覆盖数据**（需要备份或不同目录）
4. ✅ **使用 Ctrl+C 停止最安全**
5. ✅ **损坏的文件很容易识别和删除**

### 推荐做法

- ✅ 使用 `Ctrl+C` 正常停止
- ✅ 每天凌晨自动重启（避免同日覆盖）
- ✅ 定期验证文件完整性
- ✅ 监控数据更新时间
- ✅ 使用进程管理器（supervisor/systemd）

---

**最后更新**：2025-11-19  
**相关文档**：
- [MEXC WebSocket 集成](MEXC_WEBSOCKET_INTEGRATION_SUMMARY.md)
- [数据收集模式对比](ORDERBOOK_COLLECTION_MODES_COMPARISON.md)

