# DEX-CEX 套利策略规划文档

> **策略目标：** 在 DEX 和 CEX 之间寻找价格差异，执行套利交易  
> **创建日期：** 2025-10-05  
> **状态：** 规划阶段

---

## 📋 目录

1. [策略概述](#策略概述)
2. [两种实现思路对比](#两种实现思路对比)
3. [推荐方案](#推荐方案)
4. [完整流程设计](#完整流程设计)
5. [技术实现细节](#技术实现细节)
6. [风险和挑战](#风险和挑战)
7. [下一步行动](#下一步行动)

---

## 策略概述

### 核心逻辑

在 DEX 和 CEX 之间寻找同一交易对的价格差异，当价差大于交易成本时执行套利。

```
套利机会 = |DEX价格 - CEX价格| - (Gas费 + CEX手续费 + 滑点)
```

### 套利类型

1. **DEX买入 → CEX卖出**
   - DEX 价格 < CEX 价格
   - 在 DEX 买入，转到 CEX 卖出

2. **CEX买入 → DEX卖出**
   - CEX 价格 < DEX 价格
   - 在 CEX 买入，转到 DEX 卖出

### 关键指标

| 指标 | 说明 | 目标值 |
|-----|------|-------|
| **价差百分比** | (价差 / 平均价格) × 100% | > 0.5% |
| **DEX 流动性** | 池子中的 USD 价值 | > $100K |
| **DEX 交易量** | 24h 交易量 | > $50K |
| **CEX 交易量** | 24h 交易量 | > $100K |
| **交易成本** | Gas + 手续费 + 滑点 | < 0.3% |

---

## 两种实现思路对比

### 思路 A：DEX First（Pool Screener → CEX）

**流程：**
```
1. Pool Screener 筛选 DEX 池子
   ↓
2. 获取 DEX 池子的代币对
   ↓
3. 在 CEX 查找对应交易对
   ↓
4. 计算价差
   ↓
5. 评估可行性
```

**优势：**
- ✅ DEX 数据完整（流动性、交易量、价格）
- ✅ 可以筛选高质量池子
- ✅ 避免低流动性 DEX 池子
- ✅ 适合发现新的套利机会

**劣势：**
- ❌ DEX 池子数量巨大（Base 链 > 1000 个）
- ❌ 大部分 DEX 代币在 CEX 不存在
- ❌ 需要大量 API 调用检查 CEX 交易对
- ❌ 效率低，浪费资源

**适用场景：**
- 探索性分析
- 发现新币种套利机会
- 不关心实时性

---

### 思路 B：CEX First（CEX → DEX Search）⭐️

**流程：**
```
1. 获取 CEX 支持的交易对列表
   ↓
2. 用 GeckoTerminal Search API 查找对应 DEX 池子
   ↓
3. 筛选 DEX 池子（流动性、交易量）
   ↓
4. 计算价差
   ↓
5. 评估可行性
```

**优势：**
- ✅ CEX 交易对有限（币安 ~500 个 USDT 对）
- ✅ 确保 CEX 对手方存在
- ✅ 高效，减少无效查询
- ✅ 适合实际交易执行
- ✅ 易于自动化和监控

**劣势：**
- ❌ 可能错过一些新币种机会
- ❌ 依赖 CEX 交易对列表

**适用场景：**
- 实际套利交易
- 自动化监控
- 资源有限的情况

---

## 推荐方案

### 🎯 推荐：思路 B（CEX First）

**原因：**

1. **效率更高**
   - CEX 交易对是已知且有限的（~500个）
   - 避免查询大量不可交易的 DEX 池子

2. **实用性强**
   - 确保 CEX 对手方存在
   - 减少无效套利机会

3. **易于实现**
   - CEX API 获取交易对列表
   - GeckoTerminal Search API 查找对应池子
   - 筛选和计算价差

4. **成本可控**
   - API 调用次数可预测
   - 适合速率限制（30次/分钟）

---

## 完整流程设计

### 阶段 1：数据收集

#### 1.1 获取 CEX 交易对列表

**目标：** 获取币安（或其他 CEX）所有 USDT 交易对

**实现：**
```python
import ccxt

exchange = ccxt.binance()
markets = exchange.load_markets()

# 筛选 USDT 交易对
usdt_pairs = [
    symbol for symbol in markets.keys()
    if '/USDT' in symbol and markets[symbol]['active']
]

# 结果示例
# ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', ...]
```

**输出：**
- CEX 交易对列表（~500 个）
- 保存为：`data/cex_trading_pairs.json`

---

#### 1.2 查找对应的 DEX 池子

**目标：** 为每个 CEX 交易对找到对应的 DEX 池子

**实现：**
```python
from geckoterminal_py import GeckoTerminalAsyncClient

gt = GeckoTerminalAsyncClient()

async def find_dex_pools(base_token: str, quote_token: str, network: str = "base"):
    """
    搜索 DEX 池子
    
    Args:
        base_token: 基础代币（如 BTC, ETH）
        quote_token: 报价代币（如 USDC, USDT）
        network: 网络（base, ethereum, solana）
    
    Returns:
        匹配的池子列表
    """
    # 搜索基础代币的池子
    results = await gt.search_pools(
        query=base_token,
        network=network
    )
    
    # 筛选包含报价代币的池子
    matching_pools = []
    for pool in results['data']:
        pool_name = pool['attributes']['name']
        if quote_token in pool_name:
            matching_pools.append(pool)
    
    return matching_pools

# 使用示例
pools = await find_dex_pools("BTC", "USDC", "base")
```

**筛选条件：**
- ✅ 池子名称包含 CEX 的两个代币
- ✅ 流动性 > $100K
- ✅ 24h 交易量 > $50K
- ✅ 池子年龄 > 7 天

**输出：**
- DEX 池子列表（每个 CEX 交易对对应 0-N 个池子）
- 保存为：`data/dex_pools_matched.json`

---

### 阶段 2：价差分析

#### 2.1 获取实时价格

**CEX 价格：**
```python
# 使用 ccxt 获取 CEX 价格
ticker = exchange.fetch_ticker('BTC/USDT')
cex_price = ticker['last']
```

**DEX 价格：**
```python
# 从 GeckoTerminal 获取池子价格
pool_data = await gt.get_pool(network="base", pool_address="0x...")
dex_price = float(pool_data['data']['attributes']['base_token_price_usd'])
```

#### 2.2 计算价差

```python
def calculate_price_difference(cex_price: float, dex_price: float) -> dict:
    """
    计算价差
    
    Returns:
        {
            'absolute_diff': 绝对价差,
            'percentage_diff': 百分比价差,
            'direction': 套利方向（'dex_to_cex' 或 'cex_to_dex'）
        }
    """
    absolute_diff = abs(cex_price - dex_price)
    avg_price = (cex_price + dex_price) / 2
    percentage_diff = (absolute_diff / avg_price) * 100
    
    # 确定套利方向
    if dex_price < cex_price:
        direction = 'dex_to_cex'  # DEX 买入，CEX 卖出
    else:
        direction = 'cex_to_dex'  # CEX 买入，DEX 卖出
    
    return {
        'absolute_diff': absolute_diff,
        'percentage_diff': percentage_diff,
        'direction': direction,
        'cex_price': cex_price,
        'dex_price': dex_price
    }
```

**输出：**
- 价差分析结果
- 保存为：`data/price_differences.json`

---

### 阶段 3：可行性评估

#### 3.1 交易成本估算

```python
def estimate_trading_cost(
    network: str,
    trade_amount_usd: float,
    dex_pool_liquidity: float
) -> dict:
    """
    估算交易成本
    
    Returns:
        {
            'gas_fee_usd': Gas 费用,
            'cex_fee_percentage': CEX 手续费百分比,
            'slippage_percentage': 预估滑点,
            'total_cost_percentage': 总成本百分比
        }
    """
    # Gas 费用（根据网络）
    gas_fees = {
        'base': 0.1,      # Base 链 Gas 费很低
        'ethereum': 15,   # 以太坊主网较高
        'arbitrum': 0.5,  # Arbitrum 较低
        'optimism': 0.5   # Optimism 较低
    }
    gas_fee_usd = gas_fees.get(network, 5)
    
    # CEX 手续费（币安现货）
    cex_fee_percentage = 0.1  # 0.1%
    
    # DEX 滑点估算（基于交易量占流动性比例）
    trade_ratio = trade_amount_usd / dex_pool_liquidity
    if trade_ratio < 0.01:  # < 1%
        slippage = 0.1
    elif trade_ratio < 0.05:  # 1-5%
        slippage = 0.3
    else:
        slippage = 0.5
    
    # 总成本
    gas_fee_percentage = (gas_fee_usd / trade_amount_usd) * 100
    total_cost = gas_fee_percentage + cex_fee_percentage + slippage
    
    return {
        'gas_fee_usd': gas_fee_usd,
        'gas_fee_percentage': gas_fee_percentage,
        'cex_fee_percentage': cex_fee_percentage,
        'slippage_percentage': slippage,
        'total_cost_percentage': total_cost
    }
```

#### 3.2 可行性判断

```python
def is_arbitrage_feasible(
    price_diff_percentage: float,
    total_cost_percentage: float,
    min_profit_percentage: float = 0.5
) -> dict:
    """
    判断套利是否可行
    
    Args:
        price_diff_percentage: 价差百分比
        total_cost_percentage: 总成本百分比
        min_profit_percentage: 最小利润要求
    
    Returns:
        {
            'is_feasible': 是否可行,
            'net_profit_percentage': 净利润百分比,
            'reason': 原因
        }
    """
    net_profit = price_diff_percentage - total_cost_percentage
    
    if net_profit >= min_profit_percentage:
        return {
            'is_feasible': True,
            'net_profit_percentage': net_profit,
            'reason': f'Net profit {net_profit:.2f}% exceeds minimum {min_profit_percentage}%'
        }
    else:
        return {
            'is_feasible': False,
            'net_profit_percentage': net_profit,
            'reason': f'Net profit {net_profit:.2f}% below minimum {min_profit_percentage}%'
        }
```

**输出：**
- 可行性评估结果
- 保存为：`data/feasibility_results.json`

---

### 阶段 4：监控和执行

#### 4.1 实时监控

```python
async def monitor_arbitrage_opportunities(
    trading_pairs: list,
    network: str = "base",
    check_interval: int = 10  # 秒
):
    """
    实时监控套利机会
    """
    while True:
        opportunities = []
        
        for pair in trading_pairs:
            # 获取价格
            cex_price = get_cex_price(pair)
            dex_pools = await find_dex_pools(pair['base'], pair['quote'], network)
            
            for pool in dex_pools:
                dex_price = get_dex_price(pool)
                
                # 计算价差
                diff = calculate_price_difference(cex_price, dex_price)
                
                # 评估成本
                cost = estimate_trading_cost(
                    network=network,
                    trade_amount_usd=1000,
                    dex_pool_liquidity=pool['liquidity']
                )
                
                # 判断可行性
                feasibility = is_arbitrage_feasible(
                    diff['percentage_diff'],
                    cost['total_cost_percentage']
                )
                
                if feasibility['is_feasible']:
                    opportunities.append({
                        'pair': pair,
                        'pool': pool,
                        'diff': diff,
                        'cost': cost,
                        'feasibility': feasibility,
                        'timestamp': datetime.now()
                    })
        
        # 记录和通知
        if opportunities:
            log_opportunities(opportunities)
            send_notification(opportunities)
        
        await asyncio.sleep(check_interval)
```

#### 4.2 执行流程（手动/自动）

**DEX买入 → CEX卖出：**
```
1. 在 DEX 使用 Swap 合约买入代币
2. 等待交易确认（~1-5秒）
3. 将代币转到 CEX 充值地址
4. 等待 CEX 到账（~10-60秒）
5. 在 CEX 市价卖出
```

**CEX买入 → DEX卖出：**
```
1. 在 CEX 市价买入代币
2. 从 CEX 提现到钱包（~1-10分钟）
3. 在 DEX 使用 Swap 合约卖出
4. 收到 USDT/USDC
```

---

## 技术实现细节

### 数据结构设计

#### CEX-DEX 交易对映射

```python
@dataclass
class TradingPairMapping:
    """CEX-DEX 交易对映射"""
    # CEX 信息
    cex_symbol: str              # 'BTC/USDT'
    cex_base: str                # 'BTC'
    cex_quote: str               # 'USDT'
    
    # DEX 信息
    dex_network: str             # 'base'
    dex_pools: List[Dict]        # 匹配的池子列表
    
    # 状态
    is_matched: bool             # 是否找到匹配池子
    last_updated: datetime       # 最后更新时间

@dataclass
class ArbitrageOpportunity:
    """套利机会"""
    pair_mapping: TradingPairMapping
    
    # 价格
    cex_price: float
    dex_price: float
    price_diff_percentage: float
    direction: str  # 'dex_to_cex' or 'cex_to_dex'
    
    # 成本
    gas_fee_usd: float
    total_cost_percentage: float
    
    # 可行性
    net_profit_percentage: float
    is_feasible: bool
    
    # 池子信息
    pool_address: str
    pool_liquidity_usd: float
    pool_volume_24h_usd: float
    
    # 时间戳
    timestamp: datetime
```

### 任务实现

#### Task 1: CEX-DEX 配对任务

**文件：** `app/tasks/data_collection/cex_dex_pair_matcher.py`

```python
class CexDexPairMatcherTask(BaseTask):
    """匹配 CEX 交易对和 DEX 池子"""
    
    async def execute(self, context: TaskContext):
        # 1. 获取 CEX 交易对
        cex_pairs = self.get_cex_trading_pairs()
        
        # 2. 为每个交易对查找 DEX 池子
        mappings = []
        for pair in cex_pairs:
            dex_pools = await self.find_dex_pools(pair)
            mapping = TradingPairMapping(
                cex_symbol=pair,
                dex_pools=dex_pools,
                is_matched=len(dex_pools) > 0
            )
            mappings.append(mapping)
        
        # 3. 保存到 MongoDB
        await self.save_mappings(mappings)
        
        return {
            'total_pairs': len(cex_pairs),
            'matched_pairs': sum(1 for m in mappings if m.is_matched),
            'total_pools': sum(len(m.dex_pools) for m in mappings)
        }
```

#### Task 2: 价差分析任务

**文件：** `app/tasks/analysis/arbitrage_scanner.py`

```python
class ArbitrageScannerTask(BaseTask):
    """扫描套利机会"""
    
    async def execute(self, context: TaskContext):
        # 1. 加载配对关系
        mappings = await self.load_mappings()
        
        # 2. 获取实时价格并计算价差
        opportunities = []
        for mapping in mappings:
            if not mapping.is_matched:
                continue
            
            cex_price = await self.get_cex_price(mapping.cex_symbol)
            
            for pool in mapping.dex_pools:
                dex_price = await self.get_dex_price(pool)
                
                # 计算价差
                diff = calculate_price_difference(cex_price, dex_price)
                
                # 评估可行性
                cost = estimate_trading_cost(
                    network=mapping.dex_network,
                    trade_amount_usd=1000,
                    dex_pool_liquidity=pool['liquidity']
                )
                
                feasibility = is_arbitrage_feasible(
                    diff['percentage_diff'],
                    cost['total_cost_percentage']
                )
                
                if feasibility['is_feasible']:
                    opportunity = ArbitrageOpportunity(
                        pair_mapping=mapping,
                        cex_price=cex_price,
                        dex_price=dex_price,
                        price_diff_percentage=diff['percentage_diff'],
                        direction=diff['direction'],
                        gas_fee_usd=cost['gas_fee_usd'],
                        total_cost_percentage=cost['total_cost_percentage'],
                        net_profit_percentage=feasibility['net_profit_percentage'],
                        is_feasible=True,
                        pool_address=pool['address'],
                        pool_liquidity_usd=pool['liquidity'],
                        pool_volume_24h_usd=pool['volume_24h'],
                        timestamp=datetime.now()
                    )
                    opportunities.append(opportunity)
        
        # 3. 保存机会到 MongoDB
        await self.save_opportunities(opportunities)
        
        # 4. 发送通知（如果有机会）
        if opportunities:
            await self.send_notification(opportunities)
        
        return {
            'opportunities_found': len(opportunities),
            'total_scanned': len(mappings)
        }
```

### 配置文件

**文件：** `config/cex_dex_arbitrage.yml`

```yaml
tasks:
  # 阶段 1: 配对任务（每天运行一次）
  cex_dex_pair_matcher:
    enabled: true
    task_class: app.tasks.data_collection.cex_dex_pair_matcher.CexDexPairMatcherTask
    
    schedule:
      type: frequency
      frequency_hours: 24.0  # 每天更新一次配对关系
      timezone: UTC
    
    max_retries: 3
    retry_delay_seconds: 300
    timeout_seconds: 1800
    
    config:
      # CEX 配置
      exchange: "binance"  # 或 'okx', 'bybit'
      quote_currencies: ["USDT", "USDC"]
      
      # DEX 配置
      networks: ["base", "arbitrum", "optimism"]
      min_pool_liquidity: 100000  # $100K
      min_pool_volume_24h: 50000  # $50K
      min_pool_age_days: 7
    
    tags:
      - arbitrage
      - pair_matching

  # 阶段 2: 套利扫描（每分钟运行一次）
  arbitrage_scanner:
    enabled: true
    task_class: app.tasks.analysis.arbitrage_scanner.ArbitrageScannerTask
    
    schedule:
      type: frequency
      frequency_hours: 0.0167  # 每分钟（1/60）
      timezone: UTC
    
    max_retries: 2
    retry_delay_seconds: 10
    timeout_seconds: 60
    
    config:
      # 交易参数
      trade_amount_usd: 1000  # 测试金额
      min_profit_percentage: 0.5  # 最低利润要求 0.5%
      
      # 通知配置
      notify_on_opportunity: true
      notification_channels: ["telegram", "discord"]
      
      # 过滤条件
      max_cost_percentage: 0.5  # 最大成本 0.5%
      min_pool_liquidity: 50000  # 降低要求到 $50K
    
    tags:
      - arbitrage
      - scanner
      - realtime
```

---

## 风险和挑战

### 1. 技术风险

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| **价格延迟** | 价格变化导致套利失败 | 使用 WebSocket 实时价格 |
| **Gas 费波动** | 成本超出预期 | 动态 Gas 费估算 |
| **交易失败** | 交易未确认或失败 | 设置合理的 Gas Limit 和 slippage |
| **网络拥堵** | 交易延迟 | 选择低 Gas 费的链（Base, Arbitrum）|

### 2. 市场风险

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| **流动性不足** | 大额交易导致高滑点 | 限制单笔交易金额 |
| **价格剧烈波动** | 套利窗口消失 | 快速执行，设置止损 |
| **竞争对手** | 其他套利者抢先交易 | 优化执行速度 |

### 3. 操作风险

| 风险 | 影响 | 缓解措施 |
|-----|------|---------|
| **资金被卡** | 提现延迟导致无法及时套利 | 在多个 CEX 准备资金 |
| **API 限制** | 超过速率限制 | 使用付费 API，增加限制处理 |
| **人为错误** | 错误配置或操作 | 充分测试，使用测试网 |

---

## 下一步行动

### 第一阶段：验证可行性（1-2 周）

**目标：** 证明策略在理论上可行

- [ ] **任务 1.1：** 实现 CEX 交易对获取
  - 使用 ccxt 库获取币安 USDT 交易对
  - 保存到 JSON 文件

- [ ] **任务 1.2：** 实现 DEX 池子搜索
  - 使用 GeckoTerminal Search API
  - 匹配 CEX 交易对

- [ ] **任务 1.3：** 历史数据分析
  - 收集 1 周的价格数据
  - 分析历史价差
  - 统计套利机会频率

- [ ] **任务 1.4：** 成本估算验证
  - 实际测试小额交易
  - 记录真实 Gas 费和滑点
  - 验证成本模型

**输出：**
- 可行性报告
- 历史套利机会统计
- 成本模型验证结果

---

### 第二阶段：原型开发（2-3 周）

**目标：** 开发自动化监控系统

- [ ] **任务 2.1：** 开发配对任务
  - 实现 `CexDexPairMatcherTask`
  - 配置文件和数据库设计

- [ ] **任务 2.2：** 开发扫描任务
  - 实现 `ArbitrageScannerTask`
  - 价差计算和可行性评估

- [ ] **任务 2.3：** 实时监控系统
  - WebSocket 接入 CEX 价格
  - 实时计算价差
  - 通知系统（Telegram/Discord）

- [ ] **任务 2.4：** 数据可视化
  - Jupyter Notebook 分析
  - 价差趋势图表
  - 套利机会统计

**输出：**
- 自动化监控系统
- 实时通知功能
- 数据分析 Notebook

---

### 第三阶段：测试和优化（2-3 周）

**目标：** 在测试网验证完整流程

- [ ] **任务 3.1：** 测试网部署
  - 在 Base Goerli 测试网测试
  - 验证 DEX Swap 流程

- [ ] **任务 3.2：** 模拟交易
  - 纸上交易（Paper Trading）
  - 记录每笔模拟交易结果

- [ ] **任务 3.3：** 性能优化
  - 减少 API 调用次数
  - 优化价格获取速度
  - 提高扫描效率

- [ ] **任务 3.4：** 风险控制
  - 设置止损机制
  - 单笔交易金额限制
  - 异常情况处理

**输出：**
- 测试报告
- 优化后的系统
- 风险控制机制

---

### 第四阶段：小规模实盘（1-2 周）

**目标：** 用小资金验证实盘效果

- [ ] **任务 4.1：** 资金准备
  - CEX 充值（建议 $1000-5000）
  - 钱包准备 Gas 费

- [ ] **任务 4.2：** 小额交易测试
  - 单笔 $100-500
  - 记录每笔交易
  - 分析盈亏

- [ ] **任务 4.3：** 数据收集和分析
  - 实际成本统计
  - 盈利率分析
  - 问题总结

**输出：**
- 实盘测试报告
- 真实收益数据
- 改进建议

---

## 附录

### A. 推荐工具和库

**Python 库：**
- `ccxt` - 统一的 CEX API 接口
- `web3.py` - 以太坊交互
- `geckoterminal_py` - GeckoTerminal API 客户端
- `pandas` - 数据分析
- `asyncio` - 异步编程

**服务：**
- **GeckoTerminal** - DEX 数据
- **币安 API** - CEX 数据
- **Infura/Alchemy** - 区块链节点
- **Telegram Bot** - 通知

### B. 参考资源

- [GeckoTerminal API 文档](./GECKOTERMINAL_API_REFERENCE.md)
- [ccxt 文档](https://docs.ccxt.com/)
- [Uniswap V3 文档](https://docs.uniswap.org/)
- [Web3.py 文档](https://web3py.readthedocs.io/)

### C. 成本估算参考

**不同网络的 Swap Gas 费：**

| 网络 | Gas 费（USD）| 适合金额 |
|-----|-------------|----------|
| Ethereum | $15-50 | > $10,000 |
| Arbitrum | $0.5-2 | > $500 |
| Optimism | $0.5-2 | > $500 |
| Base | $0.1-0.5 | > $200 |
| Polygon | $0.05-0.2 | > $100 |

**CEX 手续费：**
- 币安现货：0.1%（VIP 0）
- OKX 现货：0.1%
- Bybit 现货：0.1%

**提现费用：**
- USDT (ERC-20): ~$1-10
- USDT (Base): ~$0.5-2
- USDT (TRC-20): ~$1

---

**最后更新：** 2025-10-05  
**下次审查：** 完成第一阶段后  
**负责人：** Alice


