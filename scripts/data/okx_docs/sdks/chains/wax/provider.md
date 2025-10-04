# Provider API | WAX | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/wax/provider#provider-api  
**抓取时间:** 2025-05-27 06:32:54  
**字数:** 435

## 导航路径
DApp 连接钱包 > WAX > Provider API

## 目录
- 什么是 Injected provider API？
- 特别说明
- 连接钱包并获取账户信息
- 是否已连接钱包
- 获取钱包信息
- 签名交易
- 添加/移除事件监听

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
特别说明
#
OKX Wallet 的 WAX API 完全兼容
Scatter 协议
，下面的 API 和示例都是基于该协议的，具体使用详情，开发者可以参考 Scatter 协议的文档。
连接钱包并获取账户信息
#
import
ScatterJS
from
'@scatterjs/core'
;
import
ScatterEOS
from
'@scatterjs/eosjs2'
;
ScatterJS
.
plugins
(
new
ScatterEOS
(
)
)
;
ScatterJS
.
login
(
)
.
then
(
identity
=>
{
const
account
=
identity
.
accounts
[
0
]
console
.
log
(
account
)
}
)
是否已连接钱包
#
确定钱包是否已连接。
import
ScatterJS
from
'@scatterjs/core'
;
import
ScatterEOS
from
'@scatterjs/eosjs2'
;
ScatterJS
.
plugins
(
new
ScatterEOS
(
)
)
;
const
isConnected
=
ScatterJS
.
isConnected
(
)
console
.
log
(
isConnected
)
获取钱包信息
#
获取当前连接的钱包信息，如果没有连接到钱包，则会返回
null
。
import
ScatterJS
from
'@scatterjs/core'
;
import
ScatterEOS
from
'@scatterjs/eosjs2'
;
ScatterJS
.
plugins
(
new
ScatterEOS
(
)
)
;
const
isConnected
=
ScatterJS
.
isConnected
(
)
if
(
isConnected
)
{
const
identity
=
ScatterJS
.
account
(
)
const
account
=
identity
.
accounts
[
0
]
console
.
log
(
account
)
}
签名交易
#
签署交易时，需要用到
eosjs
这个库。
import
ScatterJS
from
'@scatterjs/core'
;
import
ScatterEOS
from
'@scatterjs/eosjs2'
;
import
{
JsonRpc
,
Api
}
from
'eosjs'
;
ScatterJS
.
plugins
(
new
ScatterEOS
(
)
)
;
const
network
=
ScatterJS
.
Network
.
fromJson
(
{
blockchain
:
'wax'
,
chainId
:
'1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4'
,
host
:
'nodes.get-scatter.com'
,
port
:
443
,
protocol
:
'https'
}
)
;
const
rpc
=
new
JsonRpc
(
network
.
fullhost
(
)
)
;
ScatterJS
.
connect
(
'YourAppName'
,
{
network
}
)
.
then
(
connected
=>
{
if
(
!
connected
)
return
console
.
error
(
'no scatter'
)
;
const
eos
=
ScatterJS
.
eos
(
network
,
Api
,
{
rpc
}
)
;
ScatterJS
.
login
(
)
.
then
(
identity
=>
{
if
(
!
identity
)
return
console
.
error
(
'no identity'
)
;
const
account
=
identity
.
accounts
[
0
]
eos
.
transact
(
{
actions
:
[
]
}
)
.
then
(
res
=>
{
console
.
log
(
'sent: '
,
res
)
;
}
)
.
catch
(
err
=>
{
console
.
error
(
'error: '
,
err
)
;
}
)
;
}
)
;
}
)
;
添加/移除事件监听
#
添加/移除事件监听，目前支持的事件有：
connect
: 钱包已连接的事件
accountChanged
：当用户切换账户时会触发该事件
disconnect
：当用户断开连接时会触发该事件
import
ScatterJS
from
'@scatterjs/core'
;
const
connect
=
(
)
=>
{
}
ScatterJS
.
on
(
'connect'
,
connect
)
ScatterJS
.
off
(
'connect'
,
connect
)

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="特别说明" id="特别说明">特别说明<a class="index_header-anchor__Xqb+L" href="#特别说明" style="opacity:0">#</a></h2>
<p>OKX Wallet 的 WAX API 完全兼容 <a class="items-center" href="https://github.com/GetScatter/scatter-js" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Scatter 协议<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>，下面的 API 和示例都是基于该协议的，具体使用详情，开发者可以参考 Scatter 协议的文档。</p>
<h2 data-content="连接钱包并获取账户信息" id="连接钱包并获取账户信息">连接钱包并获取账户信息<a class="index_header-anchor__Xqb+L" href="#连接钱包并获取账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterJS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/core'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterEOS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/eosjs2'</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">plugins</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">ScatterEOS</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">login</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token parameter">identity</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> account <span class="token operator">=</span> identity<span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>account<span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="是否已连接钱包" id="是否已连接钱包">是否已连接钱包<a class="index_header-anchor__Xqb+L" href="#是否已连接钱包" style="opacity:0">#</a></h2>
<p>确定钱包是否已连接。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterJS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/core'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterEOS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/eosjs2'</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">plugins</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">ScatterEOS</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> isConnected <span class="token operator">=</span> <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">isConnected</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>isConnected<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取钱包信息" id="获取钱包信息">获取钱包信息<a class="index_header-anchor__Xqb+L" href="#获取钱包信息" style="opacity:0">#</a></h2>
<p>获取当前连接的钱包信息，如果没有连接到钱包，则会返回 <code>null</code> 。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterJS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/core'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterEOS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/eosjs2'</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">plugins</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">ScatterEOS</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> isConnected <span class="token operator">=</span> <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">isConnected</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>isConnected<span class="token punctuation">)</span> <span class="token punctuation">{</span>
   <span class="token keyword">const</span> identity <span class="token operator">=</span> <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
   <span class="token keyword">const</span> account <span class="token operator">=</span> identity<span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>
   <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>account<span class="token punctuation">)</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签名交易" id="签名交易">签名交易<a class="index_header-anchor__Xqb+L" href="#签名交易" style="opacity:0">#</a></h2>
<p>签署交易时，需要用到 <a class="items-center" href="https://www.npmjs.com/package/eosjs" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">eosjs<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 这个库。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterJS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/core'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterEOS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/eosjs2'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span><span class="token maybe-class-name">JsonRpc</span><span class="token punctuation">,</span> <span class="token maybe-class-name">Api</span><span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'eosjs'</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">plugins</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">ScatterEOS</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> network <span class="token operator">=</span> <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Network</span></span><span class="token punctuation">.</span><span class="token method function property-access">fromJson</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">blockchain</span><span class="token operator">:</span><span class="token string">'wax'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">chainId</span><span class="token operator">:</span><span class="token string">'1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">host</span><span class="token operator">:</span><span class="token string">'nodes.get-scatter.com'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">port</span><span class="token operator">:</span><span class="token number">443</span><span class="token punctuation">,</span>
    <span class="token literal-property property">protocol</span><span class="token operator">:</span><span class="token string">'https'</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> rpc <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">JsonRpc</span><span class="token punctuation">(</span>network<span class="token punctuation">.</span><span class="token method function property-access">fullhost</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token string">'YourAppName'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>network<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token parameter">connected</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span><span class="token punctuation">(</span><span class="token operator">!</span>connected<span class="token punctuation">)</span> <span class="token keyword control-flow">return</span> <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'no scatter'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> eos <span class="token operator">=</span> <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">eos</span><span class="token punctuation">(</span>network<span class="token punctuation">,</span> <span class="token maybe-class-name">Api</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>rpc<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">login</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token parameter">identity</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">if</span><span class="token punctuation">(</span><span class="token operator">!</span>identity<span class="token punctuation">)</span> <span class="token keyword control-flow">return</span> <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'no identity'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">const</span> account <span class="token operator">=</span> identity<span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span>

        eos<span class="token punctuation">.</span><span class="token method function property-access">transact</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">actions</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token parameter">res</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'sent: '</span><span class="token punctuation">,</span> res<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span><span class="token parameter">err</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'error: '</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="添加/移除事件监听" id="添加/移除事件监听">添加/移除事件监听<a class="index_header-anchor__Xqb+L" href="#添加/移除事件监听" style="opacity:0">#</a></h2>
<p>添加/移除事件监听，目前支持的事件有：</p>
<ul>
<li><code>connect</code>: 钱包已连接的事件</li>
<li><code>accountChanged</code>：当用户切换账户时会触发该事件</li>
<li><code>disconnect</code>：当用户断开连接时会触发该事件</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ScatterJS</span></span> <span class="token keyword module">from</span> <span class="token string">'@scatterjs/core'</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> <span class="token function-variable function">connect</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'connect'</span><span class="token punctuation">,</span> connect<span class="token punctuation">)</span>
<span class="token maybe-class-name">ScatterJS</span><span class="token punctuation">.</span><span class="token method function property-access">off</span><span class="token punctuation">(</span><span class="token string">'connect'</span><span class="token punctuation">,</span> connect<span class="token punctuation">)</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "WAX",
    "Provider API"
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
    "TON",
    "Aptos/Movement"
  ],
  "toc": [
    "什么是 Injected provider API？",
    "特别说明",
    "连接钱包并获取账户信息",
    "是否已连接钱包",
    "获取钱包信息",
    "签名交易",
    "添加/移除事件监听"
  ]
}
```

</details>
