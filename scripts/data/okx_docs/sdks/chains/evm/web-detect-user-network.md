# 获取 chainId  | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/web-detect-user-network  
**抓取时间:** 2025-05-27 06:14:40  
**字数:** 158

## 导航路径
DApp 连接钱包 > EVM > 获取 chainId

## 目录
- 什么是连接钱包
- 支持的网络
- 接入前提
- EVM 兼容链
- Bitcoin 兼容链
- Solana 兼容链
- TON
- SUI
- Aptos/Movement
- Cosmos 系/Sei
- Tron
- Starknet
- 常见问题
- 接入前提
- EVM 兼容链
- 获取钱包地址
- 获取 chainId
- 添加代币
- 签名交易
- 智能合约交互
- 切换网络
- Provider API
- Bitcoin 兼容链
- Tron
- Solana 兼容链
- TON
- Aptos/Movement
- Cosmos 系/Sei
- SUI
- Stacks
- Starknet
- Cardano
- Nostr
- NEAR
- WAX
- 设置图标

---

获取 chainId
#
所有的远程过程调用 (RPC) 请求都会提交给当前连接的网络，所以准确地获取用户的链 ID 在 EVM 系的应用开发中至关重要。
使用
eth_chainId
方法监测用户当前的链 ID。侦听
chainChanged
事件以监测用户更改网络的时间。
下方示例代码可用来获取当前网络以及用户更改网络的时间：
const
chainId
=
await
window
.
ethereum
.
request
(
{
method
:
'eth_chainId'
}
)
;
window
.
ethereum
.
on
(
'chainChanged'
,
handleChainChanged
)
;
function
handleChainChanged
(
chainId
)
{
// We recommend reloading the page, unless you must do otherwise.
window
.
location
.
reload
(
)
;
}
链 ID
#
这些是欧易默认支持的以太坊链的 ID。
更多信息请咨询
chainid.network
。
十六进制
十进制
网络
0x1
1
Ethereum Main Network (Mainnet)
0x2711
10001
ETHW
0x42
66
OKT Chain Mainnet
0x38
56
Binance Smart Chain Mainnet
0x89
137
Matic Mainnet
0xa86a
43114
Avax Mainnet
0xfa
250
Fantom Mainnet
0xa4b1
42161
Arbitrum Mainnet
0xa
10
Optimism Mainnet
0x19
25
Cronos Mainnet
0x2019
8217
Klaytn Mainnet
0x141
321
KCC Mainnet
0x440
1088
Metis Mainnet
0x120
288
Boba Mainnet
0x64
100
Gnosis Mainnet
0x505
1285
Moonriver Mainnet
0x504
1284
Moonbeam Mainnet
0x406
1030
Conflux eSpace

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="获取-chainid">获取 chainId<a class="index_header-anchor__Xqb+L" href="#获取-chainid" style="opacity:0">#</a></h1>
<p>所有的远程过程调用 (RPC) 请求都会提交给当前连接的网络，所以准确地获取用户的链 ID 在 EVM 系的应用开发中至关重要。</p>
<p>使用<code>eth_chainId</code> 方法监测用户当前的链 ID。侦听<code>chainChanged</code> 事件以监测用户更改网络的时间。</p>
<p>下方示例代码可用来获取当前网络以及用户更改网络的时间：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">ethereum</span><span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'eth_chainId'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">ethereum</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'chainChanged'</span><span class="token punctuation">,</span> handleChainChanged<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">function</span> <span class="token function">handleChainChanged</span><span class="token punctuation">(</span><span class="token parameter">chainId</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// We recommend reloading the page, unless you must do otherwise.</span>
  <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">location</span><span class="token punctuation">.</span><span class="token method function property-access">reload</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h3 id="链-id">链 ID<a class="index_header-anchor__Xqb+L" href="#链-id" style="opacity:0">#</a></h3>
<p>这些是欧易默认支持的以太坊链的 ID。</p>
<p>更多信息请咨询 <a class="items-center" href="https://chainid.network" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">chainid.network<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>十六进制</th><th>十进制</th><th>网络</th></tr></thead><tbody><tr><td>0x1</td><td>1</td><td>Ethereum Main Network (Mainnet)</td></tr><tr><td>0x2711</td><td>10001</td><td>ETHW</td></tr><tr><td>0x42</td><td>66</td><td>OKT Chain Mainnet</td></tr><tr><td>0x38</td><td>56</td><td>Binance Smart Chain Mainnet</td></tr><tr><td>0x89</td><td>137</td><td>Matic Mainnet</td></tr><tr><td>0xa86a</td><td>43114</td><td>Avax Mainnet</td></tr><tr><td>0xfa</td><td>250</td><td>Fantom Mainnet</td></tr><tr><td>0xa4b1</td><td>42161</td><td>Arbitrum Mainnet</td></tr><tr><td>0xa</td><td>10</td><td>Optimism Mainnet</td></tr><tr><td>0x19</td><td>25</td><td>Cronos Mainnet</td></tr><tr><td>0x2019</td><td>8217</td><td>Klaytn Mainnet</td></tr><tr><td>0x141</td><td>321</td><td>KCC Mainnet</td></tr><tr><td>0x440</td><td>1088</td><td>Metis Mainnet</td></tr><tr><td>0x120</td><td>288</td><td>Boba Mainnet</td></tr><tr><td>0x64</td><td>100</td><td>Gnosis Mainnet</td></tr><tr><td>0x505</td><td>1285</td><td>Moonriver Mainnet</td></tr><tr><td>0x504</td><td>1284</td><td>Moonbeam Mainnet</td></tr><tr><td>0x406</td><td>1030</td><td>Conflux eSpace</td></tr></tbody></table></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
    "获取 chainId"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Solana 兼容链",
    "TON",
    "SUI",
    "Aptos/Movement",
    "Cosmos 系/Sei",
    "Tron",
    "Starknet",
    "常见问题",
    "接入前提",
    "EVM 兼容链",
    "获取钱包地址",
    "获取 chainId",
    "添加代币",
    "签名交易",
    "智能合约交互"
  ],
  "toc": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Solana 兼容链",
    "TON",
    "SUI",
    "Aptos/Movement",
    "Cosmos 系/Sei",
    "Tron",
    "Starknet",
    "常见问题",
    "接入前提",
    "EVM 兼容链",
    "获取钱包地址",
    "获取 chainId",
    "添加代币",
    "签名交易",
    "智能合约交互",
    "切换网络",
    "Provider API",
    "Bitcoin 兼容链",
    "Tron",
    "Solana 兼容链",
    "TON",
    "Aptos/Movement",
    "Cosmos 系/Sei",
    "SUI",
    "Stacks",
    "Starknet",
    "Cardano",
    "Nostr",
    "NEAR",
    "WAX",
    "设置图标"
  ]
}
```

</details>
