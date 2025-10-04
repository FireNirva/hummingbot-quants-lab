# Provider API | starknet | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/starknet/provider#provider-api  
**抓取时间:** 2025-05-27 06:31:02  
**字数:** 424

## 导航路径
DApp 连接钱包 > starknet > Provider API

## 目录
- 什么是 Injected provider API？
- 获取注入的对象
- 注入对象的属性和方法
- 连接钱包的简单示例
- 合约调用
- 签名消息

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
获取注入的对象
#
Dapp 可以通过两种方式访问注入的对象，分别是：
window.okxwallet.starknet
window.starknet_okxwallet
这两个属性都指向同一个对象，提供两个方式是为了方便 Dapp 使用。
如果 Dapp 希望直接访问欧易 Web3 钱包注入的 Starknet 对象，可以直接使用
window.okxwallet.starknet
或者
window.starknet_okxwallet
，从而避免意外引用到其他钱包注入的 Starknet 对象。
如果 Dapp 使用了
get-starknet
这种第三方工具库，也可以完全支持。
注入对象的属性和方法
#
name
- string：钱包的名称，值为 'OKX Wallet'
icon
- string：钱包的图标
version
- string：版本号
isConnected
- boolean:：当前钱包是否已连接上
selectedAddress
- string：用户当前选中的钱包地址
account
- Account：访问账户对象，继承自 starknet.js 的
Account
，实例上的具体属性和方法，可参考 starknet.js 的文档
chainId
- string：仅支持主网，值为
SN_MAIN
provider
- Provider：访问 provider 对象，使用的是 starknet.js 的
RpcProvider
，实例上的具体属性和方法，可参考 starknet.js 的文档
enable
- () => [string]：用于连接钱包，成功调用后，会唤起欧易 Web3 钱包连接钱包页面，用户可以决定是否连接当前 DApp，如果用户同意，将会返回选中地址的单项数组
on
- (event, callback) => void：添加事件监听
accountsChanged
事件：当用户切换账户时会触发该事件，并返回新地址的数组；当断开连接时，会返回空数组。
off
- (event, callback) => void：移除事件监听
连接钱包的简单示例
#
async
function
connect
(
)
{
if
(
window
.
okxwallet
.
starknet
.
isConnected
)
{
return
}
try
{
const
[
address
]
=
await
window
.
okxwallet
.
starknet
.
enable
(
)
console
.
log
(
address
)
console
.
log
(
window
.
okxwallet
.
starknet
.
account
)
console
.
log
(
window
.
okxwallet
.
starknet
.
selectedAddress
)
console
.
log
(
window
.
okxwallet
.
starknet
.
isConnected
)
window
.
okxwallet
.
starknet
.
on
(
'accountsChanged'
,
(
[
addr
]
)
=>
{
if
(
addr
)
{
console
.
log
(
'switched address'
)
}
else
{
console
.
log
(
'disconnected'
)
}
}
)
}
catch
(
e
)
{
console
.
error
(
e
)
}
}
合约调用
#
window.okxwallet.starknet.account.execute(transactions [, abi])
执行一个或多个调用。如果只有一个调用，则
transactions
就是一个对象，其包含的属性会在下面说明。如果有多个调用，则是一个对象的数组。
参数
#
transactions
对象的结构如下：
contractAddress
- string：合约的地址
entrypoint
- string：合约的入口点
calldata
- array：调用数据
signature
- array：签名
abi
- 合约的 abi，可选的
返回值
#
result
- object
transaction_hash
- string：交易的 hash
const
transaction
=
{
"contractAddress"
:
"0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
,
"calldata"
:
[
"3055261660830722006547698919883585605584552967779072711973046411977660833095"
,
"100000000000000"
,
"0"
]
,
"entrypoint"
:
"transfer"
}
const
result
=
await
window
.
okxwallet
.
starknet
.
account
.
execute
(
transaction
)
签名消息
#
window.okxwallet.starknet.account.signMessage(data)
参数
#
data
- object：要签名的对象
返回值
#
signature
- string[]：签名的结果，包含两项
let
data
=
{
"domain"
:
{
"name"
:
"OKX"
,
"chainId"
:
"SN_MAIN"
,
"version"
:
"0.0.1"
}
,
"types"
:
{
"StarkNetDomain"
:
[
{
"name"
:
"name"
,
"type"
:
"felt"
}
]
,
"Message"
:
[
{
"name"
:
"message"
,
"type"
:
"felt"
}
]
}
,
"primaryType"
:
"Message"
,
"message"
:
{
"message"
:
"hello"
}
}
const
[
r
,
s
]
=
await
window
.
okxwallet
.
starknet
.
account
.
signMessage
(
data
)
starknet.account
和
starknet.provider
上的其他属性和方法，请查看
starknet.js
文档。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="获取注入的对象" id="获取注入的对象">获取注入的对象<a class="index_header-anchor__Xqb+L" href="#获取注入的对象" style="opacity:0">#</a></h2>
<p>Dapp 可以通过两种方式访问注入的对象，分别是：</p>
<ul>
<li><code>window.okxwallet.starknet</code></li>
<li><code>window.starknet_okxwallet</code></li>
</ul>
<p>这两个属性都指向同一个对象，提供两个方式是为了方便 Dapp 使用。</p>
<p>如果 Dapp 希望直接访问欧易 Web3 钱包注入的 Starknet 对象，可以直接使用 <code>window.okxwallet.starknet</code> 或者 <code>window.starknet_okxwallet</code> ，从而避免意外引用到其他钱包注入的 Starknet 对象。</p>
<p>如果 Dapp 使用了 <a class="items-center" href="https://github.com/starknet-io/get-starknet" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">get-starknet<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 这种第三方工具库，也可以完全支持。</p>
<h2 data-content="注入对象的属性和方法" id="注入对象的属性和方法">注入对象的属性和方法<a class="index_header-anchor__Xqb+L" href="#注入对象的属性和方法" style="opacity:0">#</a></h2>
<ol>
<li><code>name</code> - string：钱包的名称，值为 'OKX Wallet'</li>
<li><code>icon</code> - string：钱包的图标</li>
<li><code>version</code> - string：版本号</li>
<li><code>isConnected</code> - boolean:：当前钱包是否已连接上</li>
<li><code>selectedAddress</code> - string：用户当前选中的钱包地址</li>
<li><code>account</code> - Account：访问账户对象，继承自 starknet.js 的 <a class="items-center" href="https://www.starknetjs.com/docs/API/#account" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Account<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> ，实例上的具体属性和方法，可参考 starknet.js 的文档</li>
<li><code>chainId</code> - string：仅支持主网，值为 <code>SN_MAIN</code></li>
<li><code>provider</code> - Provider：访问 provider 对象，使用的是 starknet.js 的 <a class="items-center" href="https://www.starknetjs.com/docs/API/classes/RpcProvider" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">RpcProvider<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> ，实例上的具体属性和方法，可参考 starknet.js 的文档</li>
<li><code>enable</code> - () =&gt; [string]：用于连接钱包，成功调用后，会唤起欧易 Web3 钱包连接钱包页面，用户可以决定是否连接当前 DApp，如果用户同意，将会返回选中地址的单项数组</li>
<li><code>on</code> - (event, callback) =&gt; void：添加事件监听<!-- -->
<ul>
<li><code>accountsChanged</code> 事件：当用户切换账户时会触发该事件，并返回新地址的数组；当断开连接时，会返回空数组。</li>
</ul>
</li>
<li><code>off</code> - (event, callback) =&gt; void：移除事件监听</li>
</ol>
<h2 data-content="连接钱包的简单示例" id="连接钱包的简单示例">连接钱包的简单示例<a class="index_header-anchor__Xqb+L" href="#连接钱包的简单示例" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span><span class="token punctuation">(</span><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">isConnected</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">return</span>
    <span class="token punctuation">}</span>

    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> <span class="token punctuation">[</span>address<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>address<span class="token punctuation">)</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">account</span><span class="token punctuation">)</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">selectedAddress</span><span class="token punctuation">)</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">isConnected</span><span class="token punctuation">)</span>

        <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter"><span class="token punctuation">[</span>addr<span class="token punctuation">]</span></span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>addr<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'switched address'</span><span class="token punctuation">)</span>
            <span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'disconnected'</span><span class="token punctuation">)</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="合约调用" id="合约调用">合约调用<a class="index_header-anchor__Xqb+L" href="#合约调用" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.starknet.account.execute(transactions [, abi])</code></p>
<p>执行一个或多个调用。如果只有一个调用，则 <code>transactions</code> 就是一个对象，其包含的属性会在下面说明。如果有多个调用，则是一个对象的数组。</p>
<h3 id="参数">参数<a class="index_header-anchor__Xqb+L" href="#参数" style="opacity:0">#</a></h3>
<p><code>transactions</code> 对象的结构如下：</p>
<ul>
<li><code>contractAddress</code> - string：合约的地址</li>
<li><code>entrypoint</code> - string：合约的入口点</li>
<li><code>calldata</code> - array：调用数据</li>
<li><code>signature</code> - array：签名</li>
</ul>
<p><code>abi</code> - 合约的 abi，可选的</p>
<h3 id="返回值">返回值<a class="index_header-anchor__Xqb+L" href="#返回值" style="opacity:0">#</a></h3>
<ul>
<li><code>result</code> - object<!-- -->
<ul>
<li><code>transaction_hash</code> - string：交易的 hash</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"contractAddress"</span><span class="token operator">:</span> <span class="token string">"0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"calldata"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"3055261660830722006547698919883585605584552967779072711973046411977660833095"</span><span class="token punctuation">,</span>
        <span class="token string">"100000000000000"</span><span class="token punctuation">,</span>
        <span class="token string">"0"</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"entrypoint"</span><span class="token operator">:</span> <span class="token string">"transfer"</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">account</span><span class="token punctuation">.</span><span class="token method function property-access">execute</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="签名消息" id="签名消息">签名消息<a class="index_header-anchor__Xqb+L" href="#签名消息" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.starknet.account.signMessage(data)</code></p>
<h3 id="参数">参数<a class="index_header-anchor__Xqb+L" href="#参数" style="opacity:0">#</a></h3>
<ul>
<li><code>data</code> - object：要签名的对象</li>
</ul>
<h3 id="返回值">返回值<a class="index_header-anchor__Xqb+L" href="#返回值" style="opacity:0">#</a></h3>
<ul>
<li><code>signature</code> - string[]：签名的结果，包含两项</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">let</span> data <span class="token operator">=</span> <span class="token punctuation">{</span>
   <span class="token string-property property">"domain"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
       <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"OKX"</span><span class="token punctuation">,</span>
       <span class="token string-property property">"chainId"</span><span class="token operator">:</span> <span class="token string">"SN_MAIN"</span><span class="token punctuation">,</span>
       <span class="token string-property property">"version"</span><span class="token operator">:</span> <span class="token string">"0.0.1"</span>
   <span class="token punctuation">}</span><span class="token punctuation">,</span>
   <span class="token string-property property">"types"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
       <span class="token string-property property">"StarkNetDomain"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
           <span class="token punctuation">{</span>
               <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"name"</span><span class="token punctuation">,</span>
               <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
           <span class="token punctuation">}</span>
       <span class="token punctuation">]</span><span class="token punctuation">,</span>
       <span class="token string-property property">"Message"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
           <span class="token punctuation">{</span>
               <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"message"</span><span class="token punctuation">,</span>
               <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
           <span class="token punctuation">}</span>
       <span class="token punctuation">]</span>
   <span class="token punctuation">}</span><span class="token punctuation">,</span>
   <span class="token string-property property">"primaryType"</span><span class="token operator">:</span> <span class="token string">"Message"</span><span class="token punctuation">,</span>
   <span class="token string-property property">"message"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
       <span class="token string-property property">"message"</span><span class="token operator">:</span> <span class="token string">"hello"</span>
   <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> <span class="token punctuation">[</span>r<span class="token punctuation">,</span> s<span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">starknet</span><span class="token punctuation">.</span><span class="token property-access">account</span><span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span>
</code></pre></div>
<p><code>starknet.account</code> 和 <code>starknet.provider</code> 上的其他属性和方法，请查看 <a class="items-center" href="https://www.starknetjs.com/docs/API/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">starknet.js<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "starknet",
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
    "获取注入的对象",
    "注入对象的属性和方法",
    "连接钱包的简单示例",
    "合约调用",
    "签名消息"
  ]
}
```

</details>
