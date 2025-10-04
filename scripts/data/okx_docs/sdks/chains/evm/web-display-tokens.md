# 添加代币 | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/web-display-tokens#例子  
**抓取时间:** 2025-05-27 07:27:14  
**字数:** 185

## 导航路径
DApp 连接钱包 > EVM > 添加代币

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

添加代币
#
当用户打开欧易 Web3 钱包时，钱包上会显示各种包括代币的资产。默认情况下，欧易 Web3 钱包会自动检测一些主流的代币并自动显示该代币，但是其他大多数的代币需要用户自行添加。
虽然使用界面上的”添加代币“按钮也能达到此效果，但过程较为繁琐，而且由于涉及到用户与合约地址的互动，成本和出错概率都会增加。
相反，使用
EIP-747
中定义的
wallet_watchAsset API
可以改善用户添加代币时的体验，同时增加安全性。
例子
#
如果您想把推荐代币功能添加到自己的网络应用中，可以参考以下代码：
const
tokenAddress
=
'0xd00981105e61274c8a5cd5a88fe7e037d935b513'
;
const
tokenSymbol
=
'TUT'
;
const
tokenDecimals
=
18
;
const
tokenImage
=
'http://placekitten.com/200/300'
;
try
{
// wasAdded is a boolean. Like any RPC method, an error may be thrown.
const
wasAdded
=
await
okxwallet
.
request
(
{
method
:
'wallet_watchAsset'
,
params
:
{
type
:
'ERC20'
,
// Initially only supports ERC20, but eventually more!
options
:
{
address
:
tokenAddress
,
// The address that the token is at.
symbol
:
tokenSymbol
,
// A ticker symbol or shorthand, up to 5 chars.
decimals
:
tokenDecimals
,
// The number of decimals in the token
image
:
tokenImage
,
// A string url of the token logo
}
,
}
,
}
)
;
if
(
wasAdded
)
{
console
.
log
(
'Thanks for your interest!'
)
;
}
else
{
console
.
log
(
'Your loss!'
)
;
}
}
catch
(
error
)
{
console
.
log
(
error
)
;
}
下面列举了实时的网络应用案例，您输入代币细节后，即可通过一个简单的链接来分享该信息。
Watch Token

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="添加代币">添加代币<a class="index_header-anchor__Xqb+L" href="#添加代币" style="opacity:0">#</a></h1>
<p>当用户打开欧易 Web3 钱包时，钱包上会显示各种包括代币的资产。默认情况下，欧易 Web3 钱包会自动检测一些主流的代币并自动显示该代币，但是其他大多数的代币需要用户自行添加。</p>
<p>虽然使用界面上的”添加代币“按钮也能达到此效果，但过程较为繁琐，而且由于涉及到用户与合约地址的互动，成本和出错概率都会增加。
相反，使用 <a class="items-center" href="https://github.com/ethereum/EIPs/blob/master/EIPS/eip-747.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">EIP-747<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 中定义的 <code>wallet_watchAsset API</code> 可以改善用户添加代币时的体验，同时增加安全性。</p>
<h3 id="例子">例子<a class="index_header-anchor__Xqb+L" href="#例子" style="opacity:0">#</a></h3>
<p>如果您想把推荐代币功能添加到自己的网络应用中，可以参考以下代码：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> tokenAddress <span class="token operator">=</span> <span class="token string">'0xd00981105e61274c8a5cd5a88fe7e037d935b513'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> tokenSymbol <span class="token operator">=</span> <span class="token string">'TUT'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> tokenDecimals <span class="token operator">=</span> <span class="token number">18</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> tokenImage <span class="token operator">=</span> <span class="token string">'http://placekitten.com/200/300'</span><span class="token punctuation">;</span>
<span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token comment">// wasAdded is a boolean. Like any RPC method, an error may be thrown.</span>
  <span class="token keyword">const</span> wasAdded <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'wallet_watchAsset'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'ERC20'</span><span class="token punctuation">,</span> <span class="token comment">// Initially only supports ERC20, but eventually more!</span>
      <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">address</span><span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span> <span class="token comment">// The address that the token is at.</span>
        <span class="token literal-property property">symbol</span><span class="token operator">:</span> tokenSymbol<span class="token punctuation">,</span> <span class="token comment">// A ticker symbol or shorthand, up to 5 chars.</span>
        <span class="token literal-property property">decimals</span><span class="token operator">:</span> tokenDecimals<span class="token punctuation">,</span> <span class="token comment">// The number of decimals in the token</span>
        <span class="token literal-property property">image</span><span class="token operator">:</span> tokenImage<span class="token punctuation">,</span> <span class="token comment">// A string url of the token logo</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>wasAdded<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'Thanks for your interest!'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'Your loss!'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>下面列举了实时的网络应用案例，您输入代币细节后，即可通过一个简单的链接来分享该信息。</p>
<ul>
<li><a class="items-center" href="https://vittominacori.github.io/watch-token/create/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Watch Token<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
</ul><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
    "添加代币"
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
