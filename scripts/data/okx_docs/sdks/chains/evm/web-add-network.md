# 切换网络 | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/web-add-network#切换网络  
**抓取时间:** 2025-05-27 06:47:27  
**字数:** 503

## 导航路径
DApp 连接钱包 > EVM > 切换网络

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

切换网络
#
wallet_switchEthereumChain
EIP-3326
此方法由
EIP-3326
指定。
描述
此方法询问用户是否要切换到具有指定
chainId
的链上，并返回一个确认值。
与任何确认值出现的场景一样，
wallet_switchEthereumChain
只能作为直接用户操作的结果调用，例如用户单击按钮的时候。
欧易会在以下情况下自动拒绝请求：
链 ID 格式错误
指定链 ID 所属的链尚未添加到欧易
我们建议你与
wallet_addEthereumChain
一起使用：
try
{
await
okxwallet
.
request
(
{
method
:
'wallet_switchEthereumChain'
,
params
:
[
{
chainId
:
'0xf00'
}
]
,
}
)
;
}
catch
(
switchError
)
{
// This error code indicates that the chain has not been added to OKX.
if
(
switchError
.
code
===
4902
)
{
try
{
await
okxwallet
.
request
(
{
method
:
'wallet_addEthereumChain'
,
params
:
[
{
chainId
:
'0xf00'
,
chainName
:
'...'
,
rpcUrls
:
[
'https://...'
]
/* ... */
,
}
,
]
,
}
)
;
}
catch
(
addError
)
{
// handle "add" error
}
}
// handle other "switch" errors
}
参数
Array
SwitchEthereumChainParameter
interface
SwitchEthereumChainParameter
{
chainId
:
string
;
// A 0x-prefixed hexadecimal string
}
链 IDs
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
返回值
null
- 如果此方法请求成功，该方法会返回
null
，否则将会返回一个错误值。
如果错误码（
error.code
）为
4902
，说明请求的链没有被欧易添加，另需要通过
wallet_addEthereumChain
请求添加。
例子
在
codeopen
中打开。
Connect Ethereum
Switch Chain
HTML
JavaScript
<
button
class
=
"
connectEthereumButton btn
"
>
Connect Ethereum
</
button
>
<
button
class
=
"
switchChainButton btn
"
>
Switch Chain
</
button
>
const
connectEthereumButton
=
document
.
querySelector
(
'.connectEthereumButton'
)
;
const
switchChainButton
=
document
.
querySelector
(
'.switchChainButton'
)
;
let
accounts
=
[
]
;
//Sending Ethereum to an address
switchChainButton
.
addEventListener
(
'click'
,
(
)
=>
{
try
{
const
chainId
=
okxwallet
.
chainId
===
"0x42"
?
"0x38"
:
"0x42"
;
await
okxwallet
.
request
(
{
method
:
"wallet_switchEthereumChain"
,
params
:
[
{
chainId
:
chainId
}
]
}
)
;
}
catch
(
switchError
)
{
// This error code indicates that the chain has not been added to OKX Wallet.
if
(
error
.
code
===
4902
)
{
try
{
await
okxwallet
.
request
(
{
method
:
"wallet_addEthereumChain"
,
params
:
[
{
chainId
:
"0xf00"
,
rpcUrl
:
"https://..."
/* ... */
}
]
}
)
;
}
catch
(
addError
)
{
// handle "add" error
}
}
// handle other "switch" errors
}
}
)
;
connectEthereumButton
.
addEventListener
(
'click'
,
(
)
=>
{
getAccount
(
)
;
}
)
;
async
function
getAccount
(
)
{
try
{
accounts
=
await
okxwallet
.
request
(
{
method
:
'eth_requestAccounts'
}
)
;
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
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="切换网络">切换网络<a class="index_header-anchor__Xqb+L" href="#切换网络" style="opacity:0">#</a></h1>
<p><code>wallet_switchEthereumChain</code></p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R5bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R5bf:">EIP-3326</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">此方法由 <a class="items-center" href="https://ethereum-magicians.org/t/eip-3326-wallet-switchethereumchain" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">EIP-3326<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 指定。</div></div></div></div></div>
<p><strong>描述</strong></p>
<p>此方法询问用户是否要切换到具有指定 <code>chainId</code> 的链上，并返回一个确认值。</p>
<p>与任何确认值出现的场景一样，<code>wallet_switchEthereumChain</code> 只能作为直接用户操作的结果调用，例如用户单击按钮的时候。</p>
<p>欧易会在以下情况下自动拒绝请求：</p>
<ul>
<li>链 ID 格式错误</li>
<li>指定链 ID 所属的链尚未添加到欧易</li>
</ul>
<p>我们建议你与 <a class="items-center" href="https://ethereum-magicians.org/t/eip-3085-wallet-addethereumchain/5469" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank"><code>wallet_addEthereumChain</code><i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 一起使用：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'wallet_switchEthereumChain'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'0xf00'</span> <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>switchError<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// This error code indicates that the chain has not been added to OKX.</span>
  <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>switchError<span class="token punctuation">.</span><span class="token property-access">code</span> <span class="token operator">===</span> <span class="token number">4902</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'wallet_addEthereumChain'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
            <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'0xf00'</span><span class="token punctuation">,</span>
            <span class="token literal-property property">chainName</span><span class="token operator">:</span> <span class="token string">'...'</span><span class="token punctuation">,</span>
            <span class="token literal-property property">rpcUrls</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'https://...'</span><span class="token punctuation">]</span> <span class="token comment">/* ... */</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>addError<span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token comment">// handle "add" error</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span>
  <span class="token comment">// handle other "switch" errors</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>参数</strong></p>
<ul>
<li>
<p><code>Array</code></p>
<p><code>SwitchEthereumChainParameter</code></p>
</li>
</ul>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">SwitchEthereumChainParameter</span> <span class="token punctuation">{</span>
  chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// A 0x-prefixed hexadecimal string</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>链 IDs</strong></p>
<p>这些是欧易默认支持的以太坊链的 ID。
更多信息请咨询 <a class="items-center" href="https://chainid.network" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">chainid.network<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>十六进制</th><th>十进制</th><th>网络</th></tr></thead><tbody><tr><td>0x1</td><td>1</td><td>Ethereum Main Network (Mainnet)</td></tr><tr><td>0x2711</td><td>10001</td><td>ETHW</td></tr><tr><td>0x42</td><td>66</td><td>OKT Chain Mainnet</td></tr><tr><td>0x38</td><td>56</td><td>Binance Smart Chain Mainnet</td></tr><tr><td>0x89</td><td>137</td><td>Matic Mainnet</td></tr><tr><td>0xa86a</td><td>43114</td><td>Avax Mainnet</td></tr><tr><td>0xfa</td><td>250</td><td>Fantom Mainnet</td></tr><tr><td>0xa4b1</td><td>42161</td><td>Arbitrum Mainnet</td></tr><tr><td>0xa</td><td>10</td><td>Optimism Mainnet</td></tr><tr><td>0x19</td><td>25</td><td>Cronos Mainnet</td></tr><tr><td>0x2019</td><td>8217</td><td>Klaytn Mainnet</td></tr><tr><td>0x141</td><td>321</td><td>KCC Mainnet</td></tr><tr><td>0x440</td><td>1088</td><td>Metis Mainnet</td></tr><tr><td>0x120</td><td>288</td><td>Boba Mainnet</td></tr><tr><td>0x64</td><td>100</td><td>Gnosis Mainnet</td></tr><tr><td>0x505</td><td>1285</td><td>Moonriver Mainnet</td></tr><tr><td>0x504</td><td>1284</td><td>Moonbeam Mainnet</td></tr><tr><td>0x406</td><td>1030</td><td>Conflux eSpace</td></tr></tbody></table></div>
<p><strong>返回值</strong></p>
<p><code>null</code> - 如果此方法请求成功，该方法会返回 <code>null</code>，否则将会返回一个错误值。</p>
<p>如果错误码（<code>error.code</code>）为 <code>4902</code>，说明请求的链没有被欧易添加，另需要通过 <code>wallet_addEthereumChain</code> 请求添加。</p>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/yLxeRON" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Ethereum</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Switch Chain</span></button></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R1dbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R1dbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R1dbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectEthereumButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Ethereum<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>switchChainButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Switch Chain<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R1dbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectEthereumButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectEthereumButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> switchChainButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.switchChainButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">let</span> accounts <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>

<span class="token comment">//Sending Ethereum to an address</span>
switchChainButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chainId <span class="token operator">=</span> okxwallet<span class="token punctuation">.</span><span class="token property-access">chainId</span> <span class="token operator">===</span> <span class="token string">"0x42"</span> <span class="token operator">?</span> <span class="token string">"0x38"</span> <span class="token operator">:</span> <span class="token string">"0x42"</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"wallet_switchEthereumChain"</span><span class="token punctuation">,</span>
      <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">chainId</span><span class="token operator">:</span> chainId <span class="token punctuation">}</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>switchError<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// This error code indicates that the chain has not been added to OKX Wallet.</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span><span class="token property-access">code</span> <span class="token operator">===</span> <span class="token number">4902</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
          <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"wallet_addEthereumChain"</span><span class="token punctuation">,</span>
          <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">"0xf00"</span><span class="token punctuation">,</span> <span class="token literal-property property">rpcUrl</span><span class="token operator">:</span> <span class="token string">"https://..."</span> <span class="token comment">/* ... */</span> <span class="token punctuation">}</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>addError<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token comment">// handle "add" error</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// handle other "switch" errors</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectEthereumButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span><span class="token punctuation">{</span>
    accounts <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'eth_requestAccounts'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
    "切换网络"
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
