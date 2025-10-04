# 获取 genesisHash | Solana兼容链 | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/solana/web-solana-detect-user-network#获取-genesishash  
**抓取时间:** 2025-05-27 07:25:24  
**字数:** 54

## 导航路径
DApp 连接钱包 > Solana兼容链 > 获取 genesisHash

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
- Bitcoin 兼容链
- Tron
- Solana 兼容链
- Provider API
- 获取 genesisHash
- 切换网络
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

获取 genesisHash
#
window.okxwallet.svm.getNetwork()
所有的远程过程调用 (RPC) 请求都会提交给当前连接的网络，所以准确地获取用户的网络 genesisHash 在 SVM 系的应用开发中至关重要。
使用
window.okxwallet.svm.getNetwork()
方法监测用户当前的网络 genesisHash。
const
{
genesisHash
}
=
await
window
.
okxwallet
.
svm
.
getNetwork
(
)
默认 genesisHash
#
这些是 OKX Wallet 默认支持的SVM链的 genesisHash。
网络
genesisHash
SOL
5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d
SONIC_TESTNET_VONE
E8nY8PG8PEdzANRsv91C2w28Dbw9w3AhLqRYfn5tNv2C
SOONTEST_ETH
E41XcTqezgDG8GzWwnPW8Rjewv2o5UUtskPbuwA52Kjr
ECLIPSE_ETH
EAQLJCV2mh23BsK2P9oYpV5CHVLDNHTxYss3URrNmg3s
SOON_ETH
E8aYS7Vghmf1sZVSsCse9JdFHzccdE9QdpPF5SVNcGxr
SONIC_SOL
9qoRTAHGWBZHYzMJGkt62wBbFRASj6H7CvoNsNyRw2h4
SOON_BNB
8MCzWLHk3FmrdW1gVtZe7NgDefMhYFZfTUmvMANn5r6X

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="获取-genesishash">获取 genesisHash<a class="index_header-anchor__Xqb+L" href="#获取-genesishash" style="opacity:0">#</a></h1>
<p><code>window.okxwallet.svm.getNetwork()</code></p>
<p>所有的远程过程调用 (RPC) 请求都会提交给当前连接的网络，所以准确地获取用户的网络 genesisHash 在 SVM 系的应用开发中至关重要。</p>
<p>使用<code>window.okxwallet.svm.getNetwork()</code> 方法监测用户当前的网络 genesisHash。</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> <span class="token punctuation">{</span> genesisHash <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">svm</span><span class="token punctuation">.</span><span class="token method function property-access">getNetwork</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

</code></pre></div>
<h3 id="默认-genesishash">默认 genesisHash<a class="index_header-anchor__Xqb+L" href="#默认-genesishash" style="opacity:0">#</a></h3>
<p>这些是 OKX Wallet 默认支持的SVM链的 genesisHash。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>网络</th><th>genesisHash</th></tr></thead><tbody><tr><td>SOL</td><td>5eykt4UsFv8P8NJdTREpY1vzqKqZKvdpKuc147dw2N9d</td></tr><tr><td>SONIC_TESTNET_VONE</td><td>E8nY8PG8PEdzANRsv91C2w28Dbw9w3AhLqRYfn5tNv2C</td></tr><tr><td>SOONTEST_ETH</td><td>E41XcTqezgDG8GzWwnPW8Rjewv2o5UUtskPbuwA52Kjr</td></tr><tr><td>ECLIPSE_ETH</td><td>EAQLJCV2mh23BsK2P9oYpV5CHVLDNHTxYss3URrNmg3s</td></tr><tr><td>SOON_ETH</td><td>E8aYS7Vghmf1sZVSsCse9JdFHzccdE9QdpPF5SVNcGxr</td></tr><tr><td>SONIC_SOL</td><td>9qoRTAHGWBZHYzMJGkt62wBbFRASj6H7CvoNsNyRw2h4</td></tr><tr><td>SOON_BNB</td><td>8MCzWLHk3FmrdW1gVtZe7NgDefMhYFZfTUmvMANn5r6X</td></tr></tbody></table></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "Solana兼容链",
    "获取 genesisHash"
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
    "Bitcoin 兼容链",
    "Tron",
    "Solana 兼容链",
    "Provider API",
    "获取 genesisHash"
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
    "Bitcoin 兼容链",
    "Tron",
    "Solana 兼容链",
    "Provider API",
    "获取 genesisHash",
    "切换网络",
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
