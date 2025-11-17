# Token 映射指南

## 📖 概述

本文档介绍如何处理 CEX（中心化交易所）和 DEX（去中心化交易所）之间的 token 名称差异问题。

### 常见场景

| CEX Token | DEX Token | 原因 |
|-----------|-----------|------|
| IRON | wIRON | Wrapped version |
| ETH | WETH | Wrapped Ether |
| BTC | WBTC | Wrapped Bitcoin |
| USDC | USDbC | Bridge version (Base) |

---

## 🎯 问题描述

在进行 CEX-DEX 池子映射时，某些 token 在 CEX 和 DEX 上使用不同的名称：

**示例问题**：
- CEX 上叫 `IRON-USDT`
- DEX 上叫 `wIRON / USDC`
- 直接搜索 "IRON" 找不到池子 ❌

**解决方案**：使用 Token 映射配置文件 ✅

---

## 🔧 配置 Token 映射

### 1. 编辑配置文件

编辑 `config/token_mapping.yml`：

```yaml
# CEX-DEX Token 名称映射配置

# Base 生态 Wrapped Tokens
IRON: wIRON
ETH: WETH
BTC: WBTC

# 其他特殊命名案例
USDC: USDbC   # Base 链上的 USDC 桥接版本
```

### 2. 配置格式

```yaml
CEX_SYMBOL: DEX_SYMBOL
```

- **CEX_SYMBOL**: 中心化交易所使用的代币符号
- **DEX_SYMBOL**: 去中心化交易所使用的代币符号
- 如果 token 在 CEX 和 DEX 中名称相同，无需添加映射

---

## 🚀 使用方法

### CLI 脚本方式

```bash
# 1. 添加映射到 config/token_mapping.yml
vim config/token_mapping.yml

# 2. 运行池子映射（自动使用映射）
python scripts/build_pool_mapping.py \
  --network base \
  --connector gate_io \
  --pairs IRON-USDT \
  --top-n 3
```

**输出示例**：
```
Loaded 1 token mappings from config/token_mapping.yml
Token mapping: IRON -> wIRON
Found 3 pools for IRON (total: 4)
```

### Task 方式

配置文件会自动加载，无需额外配置：

```bash
python cli.py trigger-task \
  --task base_pool_mapping \
  --config config/pool_mapping_base.yml
```

---

## 📊 验证映射结果

### 1. 检查原始搜索结果

```bash
cat app/data/raw/geckoterminal/search_pools/base/IRON-USDT.json
```

输出示例：
```json
{
  "query": "IRON",
  "network": "base",
  "pools_found": 3,
  "pools": [
    {
      "pool_address": "0x9941dfa4...",
      "name": "wIRON / USDC",
      "dex_id": "aerodrome-base",
      "reserve_usd": 195782.6477
    }
  ]
}
```

### 2. 检查映射数据

```bash
python scripts/view_parquet.py \
  app/data/processed/pool_mappings/base_gate_io_pool_map.parquet \
  --filter "trading_pair == 'IRON-USDT'"
```

---

## 🔍 工作原理

### 流程图

```
1. 读取配置
   ↓
   config/token_mapping.yml
   IRON: wIRON

2. 查找映射
   ↓
   IRON -> wIRON

3. 使用映射后的名称搜索
   ↓
   GeckoTerminal API: search/pools?query=wIRON

4. 过滤池子
   ↓
   只保留 base token = "wIRON" 的池子

5. 保存结果
   ↓
   trading_pair: IRON-USDT (保持CEX名称)
   实际池子: wIRON / USDC
```

### 关键点

1. **CEX 名称保持不变**：映射数据中 `trading_pair` 仍然是 `IRON-USDT`
2. **DEX 名称用于搜索**：API 查询使用 `wIRON`
3. **自动过滤**：只保留 base token 匹配的池子
4. **向后兼容**：未映射的 token 直接使用原名称

---

## 💡 高级用法

### 1. 自定义映射文件位置

在代码中指定映射文件：

```python
from core.services.pool_mapping import PoolMappingService

async with PoolMappingService(token_mapping_file="custom_path.yml") as service:
    pools = await service.search_pool_for_pair("IRON", "base")
```

### 2. 批量添加映射

```yaml
# Wrapped Tokens
IRON: wIRON
ETH: WETH
BTC: WBTC
SOL: WSOL

# Bridge Versions
USDC: USDbC
DAI: ceDAI
USDT: axlUSDT

# Rebranded Tokens
OLDNAME: NEWNAME
```

### 3. 网络特定映射

如果同一 token 在不同网络上有不同名称，可以创建多个配置文件：

```
config/
  token_mapping_base.yml    # Base 链映射
  token_mapping_arbitrum.yml  # Arbitrum 链映射
  token_mapping_polygon.yml   # Polygon 链映射
```

---

## 🐛 故障排查

### 问题 1: 映射未生效

**症状**：仍然搜索不到池子

**检查步骤**：
1. 确认配置文件路径正确：`config/token_mapping.yml`
2. 检查 YAML 格式是否正确（注意缩进）
3. 查看日志确认映射已加载：
   ```
   INFO - Loaded 1 token mappings from ...
   INFO - Token mapping: IRON -> wIRON
   ```

### 问题 2: 找到了不相关的池子

**症状**：搜索结果中包含错误的 token

**解决方案**：
1. 检查映射是否正确（DEX token 名称是否准确）
2. 系统会自动过滤 base token 不匹配的池子
3. 查看日志中的过滤信息：
   ```
   DEBUG - Skipping pool 'XXX / USDC' - base token 'XXX' != query 'wIRON'
   ```

### 问题 3: 配置文件格式错误

**症状**：加载映射失败

**正确格式**：
```yaml
IRON: wIRON
ETH: WETH
```

**错误格式**：
```yaml
# ❌ 缺少空格
IRON:wIRON

# ❌ 使用了引号（不必要，但不会出错）
"IRON": "wIRON"

# ❌ 缩进错误
  IRON: wIRON
```

---

## 📚 相关文档

- [Pool Mapping Guide](POOL_MAPPING_GUIDE.md) - 池子映射完整指南
- [GeckoTerminal API Usage](GECKOTERMINAL_API_USAGE.md) - API 使用说明
- [Data Storage Strategy](DATA_STORAGE_STRATEGY.md) - 数据存储策略

---

## ❓ 常见问题

### Q1: 如何知道某个 token 在 DEX 上的名称？

**A**: 可以通过以下方式查找：
1. 访问 GeckoTerminal 网站搜索 token
2. 查看 DEX 上的池子名称
3. 查看 token 的智能合约地址和名称

### Q2: 是否需要为所有 token 添加映射？

**A**: 不需要。只为那些 CEX 和 DEX 名称不同的 token 添加映射。大多数 token 名称是一致的。

### Q3: 映射会影响价差分析吗？

**A**: 不会。映射只在池子搜索时使用，价差分析仍然使用 CEX 的 token 名称（如 `IRON-USDT`）。

### Q4: 如何更新映射？

**A**: 直接编辑 `config/token_mapping.yml` 文件，下次运行时会自动加载新配置。

---

## 🎯 最佳实践

1. **集中管理**：将所有映射放在一个配置文件中
2. **添加注释**：说明映射的原因（wrapped, bridge, rebrand）
3. **定期检查**：新增 token 时检查是否需要映射
4. **版本控制**：将 `token_mapping.yml` 纳入 git 管理
5. **团队共享**：确保团队成员使用相同的映射配置

---

## 📝 示例：完整工作流

```bash
# 1. 发现问题：IRON-USDT 搜索不到池子
python scripts/build_pool_mapping.py --pairs IRON-USDT --network base
# 输出: No pools found for IRON on base ❌

# 2. 添加映射
echo "IRON: wIRON" >> config/token_mapping.yml

# 3. 重新搜索
python scripts/build_pool_mapping.py --pairs IRON-USDT --network base
# 输出:
# Loaded 1 token mappings
# Token mapping: IRON -> wIRON
# Found 3 pools for IRON ✅

# 4. 验证结果
python scripts/view_parquet.py \
  app/data/processed/pool_mappings/base_gate_io_pool_map.parquet \
  --filter "trading_pair == 'IRON-USDT'"

# 5. 下载 DEX 数据
python scripts/download_dex_ohlcv.py \
  --network base \
  --connector gate_io \
  --intervals 1m

# 6. 分析价差
python scripts/analyze_cex_dex_spread.py --pair IRON-USDT
```

---

**✅ 现在您可以轻松处理 wrapped tokens 和其他命名差异问题了！**

