# Provider API | TON | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/ton/provider#deviceinfo  
**抓取时间:** 2025-05-27 07:33:05  
**字数:** 1229

## 导航路径
DApp 连接钱包 > TON > Provider API

## 目录
- 什么是 Injected provider API？
- 特别说明
- 获取注入的对象
- deviceInfo
- walletInfo
- protocolVersion
- connect
- restoreConnection
- send
- listen
- on / off

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
特别说明
#
OKX Wallet 的 TON API 完全符合
Ton Connect 协议
的规范。
Dapp 可以使用
TON Connect SDK
来更方便地接入 OKX Wallet 。
获取注入的对象
#
OKX Wallet 按照 TON Connect 协议的规范向 Dapp 中注入如下属性：
window
.
okxTonWallet
.
tonconnect
其指向的对象的数据结构如下：
interface
TonConnectBridge
{
deviceInfo
:
DeviceInfo
;
walletInfo
?
:
WalletInfo
;
protocolVersion
:
number
;
connect
(
protocolVersion
:
number
,
message
:
ConnectRequest
)
:
Promise
<
ConnectEvent
>
;
restoreConnection
(
)
:
Promise
<
ConnectEvent
>
;
send
(
message
:
AppRequest
)
:
Promise
<
WalletResponse
>
;
listen
(
callback
:
(
event
:
WalletEvent
)
=>
void
)
:
(
)
=>
void
;
}
deviceInfo
#
用于获取设备信息，数据结构如下：
{
platform
:
'browser'
,
appName
:
'OKX Wallet'
,
appVersion
:
'3.3.19'
,
maxProtocolVersion
:
2
,
features
:
[
'SendTransaction'
,
{
name
:
'SendTransaction'
,
maxMessages
:
4
,
}
,
]
,
}
platform
：设备平台
appName
：钱包名称
appVersion
：钱包版本
maxProtocolVersion
：支持的最大协议版本
features
：钱包支持的特性
walletInfo
#
用于获取钱包信息，数据结构如下：
{
name
:
'OKX Wallet'
,
app_name
:
'okxTonWallet'
,
image
:
'https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png'
,
about_url
:
'https://web3.okx.com/web3'
,
platforms
:
[
'chrome'
,
'firefox'
,
'safari'
]
,
}
name
：钱包名称
app_name
：钱包应用唯一标识
image
：钱包图标
about_url
：钱包介绍页面
platforms
：钱包支持的平台
protocolVersion
#
OKX Wallet 支持的 Ton Connect 的版本，目前为 2 。
connect
#
连接钱包的方法，连接钱包时，也可以对钱包进行签名验证。
connect
(
protocolVersion
:
number
,
message
:
ConnectRequest
)
:
Promise
<
ConnectEvent
>
;
入参
#
protocolVersion
：Dapp 期望钱包支持的 Ton Connect 的版本，如果钱包暂未支持该版本，会直接返回错误
message
: 连接钱包的请求信息
message 入参
type
ConnectRequest
=
{
manifestUrl
:
string
;
items
:
ConnectItem
[
]
,
// 与应用共享的数据项
}
type
ConnectItem
=
TonAddressItem
|
TonProofItem
type
TonAddressItem
=
{
name
:
"ton_addr"
;
}
type
TonProofItem
=
{
name
:
"ton_proof"
;
payload
:
string
;
// 任意载荷，例如 nonce + 过期时间戳。
}
manifestUrl
：Dapp 的 manifest.json 文件的 URL，该文件中包含 Dapp 的元信息，数据结构如下：
{
"url"
:
"<app-url>"
,
// 必填
"name"
:
"<app-name>"
,
// 必填
"iconUrl"
:
"<app-icon-url>"
,
// 必填
"termsOfUseUrl"
:
"<terms-of-use-url>"
,
// 可选
"privacyPolicyUrl"
:
"<privacy-policy-url>"
// 可选
}
items
：请求钱包的指令列表，目前支持两个指令：
ton_addr
：获取用户的地址、公钥等信息
ton_proof
：对钱包进行签名验证
返回值
#
返回一个 Promise 对象，Promise 对象的结果为
ConnectEvent
，数据结构如下：
type
ConnectEvent
=
ConnectEventSuccess
|
ConnectEventError
;
type
ConnectEventSuccess
=
{
event
:
"connect"
;
id
:
number
;
// 递增的事件计数器
payload
:
{
items
:
ConnectItemReply
[
]
;
device
:
DeviceInfo
;
}
}
type
ConnectEventError
=
{
event
:
"connect_error"
,
id
:
number
;
// 递增的事件计数器
payload
:
{
code
:
number
;
message
:
string
;
}
}
// 与 window.okxTonWallet.tonconnect 对象上的 deviceInfo 完全相同
type
DeviceInfo
=
{
platform
:
"iphone"
|
"ipad"
|
"android"
|
"windows"
|
"mac"
|
"linux"
;
appName
:
string
;
appVersion
:
string
;
maxProtocolVersion
:
number
;
features
:
Feature
[
]
;
}
type
Feature
=
{
name
:
'SendTransaction'
,
maxMessages
:
number
}
// `maxMessages` 是钱包支持的一次 `SendTransaction` 中的最大消息数
type
ConnectItemReply
=
TonAddressItemReply
|
TonProofItemReply
;
// 由钱包返回的不受信任的数据。
// 如果您需要保证用户拥有此地址和公钥，您需要额外请求 ton_proof。
type
TonAddressItemReply
=
{
name
:
"ton_addr"
;
address
:
string
;
// TON 地址原始 (`0:<hex>`)
network
:
NETWORK
;
// 网络 global_id
publicKey
:
string
;
// HEX 字符串，不带 0x
walletStateInit
:
string
;
// Base64（不安全 URL）编码的钱包合约的 stateinit cell
}
type
TonProofItemReply
=
{
name
:
"ton_proof"
;
proof
:
{
timestamp
:
string
;
// 签名操作的 64 位 unix epoch 时间（秒）
domain
:
{
lengthBytes
:
number
;
// AppDomain 长度
value
:
string
;
// 应用域名（作为 url 部分，无编码）
}
;
signature
:
string
;
// base64 编码的签名
payload
:
string
;
// 请求中的载荷
}
}
// 目前仅支持主网
enum
NETWORK
{
MAINNET
=
'-239'
,
TESTNET
=
'-3'
}
示例
#
只是获取用户的地址、公钥等信息：
const
result
=
await
window
.
okxTonWallet
.
tonconnect
.
connect
(
2
,
{
manifestUrl
:
'https://example.com/manifest.json'
,
items
:
[
{
name
:
'ton_addr'
}
]
}
)
if
(
result
.
event
===
'connect'
)
{
console
.
log
(
result
.
payload
.
items
[
0
]
.
address
)
}
else
{
console
.
log
(
result
.
payload
.
message
)
}
获取用户地址、公钥等信息，同时对钱包进行签名验证：
const
result
=
await
window
.
okxTonWallet
.
tonconnect
.
connect
(
2
,
{
manifestUrl
:
'https://example.com/manifest.json'
,
items
:
[
{
name
:
'ton_addr'
}
,
{
name
:
'ton_proof'
,
payload
:
'123'
}
]
}
)
if
(
result
.
event
===
'connect'
)
{
console
.
log
(
result
.
payload
.
items
[
0
]
.
address
)
console
.
log
(
result
.
payload
.
items
[
1
]
.
proof
)
}
else
{
console
.
log
(
result
.
payload
.
message
)
}
restoreConnection
#
恢复连接的方法，只会返回
ton_addr
指令的结果，如果无法连接钱包，则返回错误。
restoreConnection
(
)
:
Promise
<
ConnectEvent
>
;
示例
#
const
result
=
await
window
.
okxTonWallet
.
tonconnect
.
restoreConnection
(
)
if
(
result
.
event
===
'connect'
)
{
console
.
log
(
result
.
payload
.
items
[
0
]
.
address
)
}
else
{
console
.
log
(
result
.
payload
.
message
)
}
send
#
向钱包发送消息的方法：
send
(
message
:
AppRequest
)
:
Promise
<
WalletResponse
>
;
入参
#
message
：发送给钱包的消息体
message 入参
interface
AppRequest
{
method
:
string
;
params
:
string
[
]
;
id
:
string
;
}
method
：消息的名称，目前支持
sendTransaction
和
disconnect
params
：消息的参数
id
：递增的标识符，允许匹配请求和响应
sendTransaction 消息
#
用于签署并广播交易。
入参：
interface
SendTransactionRequest
{
method
:
'sendTransaction'
;
params
:
[
<
transaction
-
payload
>
]
;
id
:
string
;
}
其中
<transaction-payload>
是具有以下属性的 JSON：
valid_until
（整数，可选）：unix 时间戳。该时刻之后交易将无效。
network
（NETWORK，可选）：目前仅支持主网
from
（以 wc:hex 格式的字符串，可选）- DApp打算从中发送交易的发送者地址。
messages
（信息数组）：1-4 条从钱包合约到其他账户的输出消息。所有消息按顺序发送出去，但钱包无法保证消息会按相同顺序被传递和执行。
消息结构：
address
（字符串）：消息目的地
amount
（小数字符串）：要发送的纳币数量。
payload
（base64 编码的字符串，可选）：以 Base64 编码的原始cell BoC。
stateInit
（base64 编码的字符串，可选）：以 Base64 编码的原始cell BoC。
示例：
{
"valid_until"
:
1658253458
,
"network"
:
"-239"
,
"from"
:
"0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f"
,
"messages"
:
[
{
"address"
:
"0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F"
,
"amount"
:
"20000000"
,
"stateInit"
:
"base64bocblahblahblah=="
// 部署合约
}
,
{
"address"
:
"0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3"
,
"amount"
:
"60000000"
,
"payload"
:
"base64bocblahblahblah=="
// 将 nft 转移至新部署的账户 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F
}
]
}
返回值：
type
SendTransactionResponse
=
SendTransactionResponseSuccess
|
SendTransactionResponseError
;
interface
SendTransactionResponseSuccess
{
result
:
<
boc
>
;
id
:
string
;
}
interface
SendTransactionResponseError
{
error
:
{
code
:
number
;
message
:
string
}
;
id
:
string
;
}
其中
result
是签名后的签名串。
disconnect 消息
#
用于断开钱包连接。
入参：
interface
DisconnectRequest
{
method
:
'disconnect'
;
params
:
[
]
;
id
:
string
;
}
返回值：
type
DisconnectResponse
=
DisconnectResponseSuccess
|
DisconnectResponseError
;
interface
DisconnectResponseSuccess
{
result
:
{
}
;
id
:
string
;
}
interface
DisconnectResponseError
{
error
:
{
code
:
number
;
message
:
string
}
;
id
:
string
;
}
listen
#
监听钱包事件的方法。
listen
(
callback
:
(
event
:
WalletEvent
)
=>
void
)
:
(
)
=>
void
;
入参
#
callback
：事件监听的回调函数
interface
WalletEvent
{
event
:
WalletEventName
;
id
:
number
;
// 递增的事件计数器
payload
:
<
event
-
payload
>
;
// 每个事件特定的载荷
}
type
WalletEventName
=
'connect'
|
'connect_error'
|
'disconnect'
;
返回值
#
返回一个函数，用于取消监听。
on / off
#
这是专属于 OKX Wallet 的非标准 API，设计该 API 主要是为了支持 accountChanged 事件，可以让 Dapp 响应插件内的钱包切换
添加/移除事件监听，目前支持的事件有：
connect
: 钱包已连接的事件
disconnect
：当用户断开连接时会触发该事件
accountChanged
：当用户切换账户时会触发该事件
const
accountChanged
=
(
)
=>
{
}
window
.
okxTonWallet
.
tonconnect
.
on
(
'accountChanged'
,
accountChanged
)
window
.
okxTonWallet
.
tonconnect
.
off
(
'accountChanged'
,
accountChanged
)

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="特别说明" id="特别说明">特别说明<a class="index_header-anchor__Xqb+L" href="#特别说明" style="opacity:0">#</a></h2>
<p>OKX Wallet 的 TON API 完全符合 <a class="items-center" href="https://docs.ton.org/mandarin/develop/dapps/ton-connect/protocol/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Ton Connect 协议<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 的规范。</p>
<p>Dapp 可以使用 <a class="items-center" href="https://docs.ton.org/mandarin/develop/dapps/ton-connect/developers" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">TON Connect SDK<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 来更方便地接入 OKX Wallet 。</p>
<h2 data-content="获取注入的对象" id="获取注入的对象">获取注入的对象<a class="index_header-anchor__Xqb+L" href="#获取注入的对象" style="opacity:0">#</a></h2>
<p>OKX Wallet 按照 TON Connect 协议的规范向 Dapp 中注入如下属性：</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span>
</code></pre></div>
<p>其指向的对象的数据结构如下：</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">interface</span> <span class="token class-name">TonConnectBridge</span> <span class="token punctuation">{</span>
    deviceInfo<span class="token operator">:</span> DeviceInfo<span class="token punctuation">;</span>
    walletInfo<span class="token operator">?</span><span class="token operator">:</span> WalletInfo<span class="token punctuation">;</span>
    protocolVersion<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
    <span class="token function">connect</span><span class="token punctuation">(</span>protocolVersion<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">,</span> message<span class="token operator">:</span> ConnectRequest<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>ConnectEvent<span class="token operator">&gt;</span><span class="token punctuation">;</span>
    <span class="token function">restoreConnection</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>ConnectEvent<span class="token operator">&gt;</span><span class="token punctuation">;</span>
    <span class="token function">send</span><span class="token punctuation">(</span>message<span class="token operator">:</span> AppRequest<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>WalletResponse<span class="token operator">&gt;</span><span class="token punctuation">;</span>
    <span class="token function">listen</span><span class="token punctuation">(</span><span class="token function-variable function">callback</span><span class="token operator">:</span> <span class="token punctuation">(</span>event<span class="token operator">:</span> WalletEvent<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="deviceInfo" id="deviceinfo">deviceInfo<a class="index_header-anchor__Xqb+L" href="#deviceinfo" style="opacity:0">#</a></h2>
<p>用于获取设备信息，数据结构如下：</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token punctuation">{</span>
    <span class="token literal-property property">platform</span><span class="token operator">:</span> <span class="token string">'browser'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">appName</span><span class="token operator">:</span> <span class="token string">'OKX Wallet'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">appVersion</span><span class="token operator">:</span> <span class="token string">'3.3.19'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">maxProtocolVersion</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
    <span class="token literal-property property">features</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token string">'SendTransaction'</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">'SendTransaction'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">maxMessages</span><span class="token operator">:</span> <span class="token number">4</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<ul>
<li><code>platform</code>：设备平台</li>
<li><code>appName</code>：钱包名称</li>
<li><code>appVersion</code>：钱包版本</li>
<li><code>maxProtocolVersion</code>：支持的最大协议版本</li>
<li><code>features</code>：钱包支持的特性</li>
</ul>
<h2 data-content="walletInfo" id="walletinfo">walletInfo<a class="index_header-anchor__Xqb+L" href="#walletinfo" style="opacity:0">#</a></h2>
<p>用于获取钱包信息，数据结构如下：</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token punctuation">{</span>
    <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">'OKX Wallet'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">app_name</span><span class="token operator">:</span> <span class="token string">'okxTonWallet'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">image</span><span class="token operator">:</span> <span class="token string">'https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">about_url</span><span class="token operator">:</span> <span class="token string">'https://web3.okx.com/web3'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">platforms</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'chrome'</span><span class="token punctuation">,</span> <span class="token string">'firefox'</span><span class="token punctuation">,</span> <span class="token string">'safari'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<ul>
<li><code>name</code>：钱包名称</li>
<li><code>app_name</code>：钱包应用唯一标识</li>
<li><code>image</code>：钱包图标</li>
<li><code>about_url</code>：钱包介绍页面</li>
<li><code>platforms</code>：钱包支持的平台</li>
</ul>
<h2 data-content="protocolVersion" id="protocolversion">protocolVersion<a class="index_header-anchor__Xqb+L" href="#protocolversion" style="opacity:0">#</a></h2>
<p>OKX Wallet 支持的 Ton Connect 的版本，目前为 2 。</p>
<h2 data-content="connect" id="connect">connect<a class="index_header-anchor__Xqb+L" href="#connect" style="opacity:0">#</a></h2>
<p>连接钱包的方法，连接钱包时，也可以对钱包进行签名验证。</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token function">connect</span><span class="token punctuation">(</span>protocolVersion<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">,</span> message<span class="token operator">:</span> ConnectRequest<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>ConnectEvent<span class="token operator">&gt;</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="入参">入参<a class="index_header-anchor__Xqb+L" href="#入参" style="opacity:0">#</a></h3>
<ul>
<li><code>protocolVersion</code>：Dapp 期望钱包支持的 Ton Connect 的版本，如果钱包暂未支持该版本，会直接返回错误</li>
<li><code>message</code>: 连接钱包的请求信息</li>
</ul>
<p><strong>message 入参</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">type</span> <span class="token class-name">ConnectRequest</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  manifestUrl<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  items<span class="token operator">:</span> ConnectItem<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token comment">// 与应用共享的数据项</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">ConnectItem</span> <span class="token operator">=</span> TonAddressItem <span class="token operator">|</span> TonProofItem

<span class="token keyword">type</span> <span class="token class-name">TonAddressItem</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  name<span class="token operator">:</span> <span class="token string">"ton_addr"</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">TonProofItem</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  name<span class="token operator">:</span> <span class="token string">"ton_proof"</span><span class="token punctuation">;</span>
  payload<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// 任意载荷，例如 nonce + 过期时间戳。</span>
<span class="token punctuation">}</span>
</code></pre></div>
<ul>
<li><code>manifestUrl</code>：Dapp 的 manifest.json 文件的 URL，该文件中包含 Dapp 的元信息，数据结构如下：<!-- -->
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
      <span class="token property">"url"</span><span class="token operator">:</span> <span class="token string">"&lt;app-url&gt;"</span><span class="token punctuation">,</span>                        <span class="token comment">// 必填</span>
      <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"&lt;app-name&gt;"</span><span class="token punctuation">,</span>                      <span class="token comment">// 必填</span>
      <span class="token property">"iconUrl"</span><span class="token operator">:</span> <span class="token string">"&lt;app-icon-url&gt;"</span><span class="token punctuation">,</span>               <span class="token comment">// 必填</span>
      <span class="token property">"termsOfUseUrl"</span><span class="token operator">:</span> <span class="token string">"&lt;terms-of-use-url&gt;"</span><span class="token punctuation">,</span>     <span class="token comment">// 可选</span>
      <span class="token property">"privacyPolicyUrl"</span><span class="token operator">:</span> <span class="token string">"&lt;privacy-policy-url&gt;"</span> <span class="token comment">// 可选</span>
    <span class="token punctuation">}</span>
</code></pre></div>
</li>
<li><code>items</code>：请求钱包的指令列表，目前支持两个指令：<!-- -->
<ul>
<li><code>ton_addr</code>：获取用户的地址、公钥等信息</li>
<li><code>ton_proof</code>：对钱包进行签名验证</li>
</ul>
</li>
</ul>
<h3 id="返回值">返回值<a class="index_header-anchor__Xqb+L" href="#返回值" style="opacity:0">#</a></h3>
<p>返回一个 Promise 对象，Promise 对象的结果为 <code>ConnectEvent</code>，数据结构如下：</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">type</span> <span class="token class-name">ConnectEvent</span> <span class="token operator">=</span> ConnectEventSuccess <span class="token operator">|</span> ConnectEventError<span class="token punctuation">;</span>

<span class="token keyword">type</span> <span class="token class-name">ConnectEventSuccess</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  event<span class="token operator">:</span> <span class="token string">"connect"</span><span class="token punctuation">;</span>
  id<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> <span class="token comment">// 递增的事件计数器</span>
  payload<span class="token operator">:</span> <span class="token punctuation">{</span>
      items<span class="token operator">:</span> ConnectItemReply<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
      device<span class="token operator">:</span> DeviceInfo<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">ConnectEventError</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  event<span class="token operator">:</span> <span class="token string">"connect_error"</span><span class="token punctuation">,</span>
  id<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> <span class="token comment">// 递增的事件计数器</span>
  payload<span class="token operator">:</span> <span class="token punctuation">{</span>
      code<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
      message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// 与 window.okxTonWallet.tonconnect 对象上的 deviceInfo 完全相同</span>
<span class="token keyword">type</span> <span class="token class-name">DeviceInfo</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  platform<span class="token operator">:</span> <span class="token string">"iphone"</span> <span class="token operator">|</span> <span class="token string">"ipad"</span> <span class="token operator">|</span> <span class="token string">"android"</span> <span class="token operator">|</span> <span class="token string">"windows"</span> <span class="token operator">|</span> <span class="token string">"mac"</span> <span class="token operator">|</span> <span class="token string">"linux"</span><span class="token punctuation">;</span>
  appName<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  appVersion<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  maxProtocolVersion<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
  features<span class="token operator">:</span> Feature<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">Feature</span> <span class="token operator">=</span> <span class="token punctuation">{</span> name<span class="token operator">:</span> <span class="token string">'SendTransaction'</span><span class="token punctuation">,</span> maxMessages<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token punctuation">}</span> <span class="token comment">// `maxMessages` 是钱包支持的一次 `SendTransaction` 中的最大消息数</span>

<span class="token keyword">type</span> <span class="token class-name">ConnectItemReply</span> <span class="token operator">=</span> TonAddressItemReply <span class="token operator">|</span> TonProofItemReply<span class="token punctuation">;</span>

<span class="token comment">// 由钱包返回的不受信任的数据。</span>
<span class="token comment">// 如果您需要保证用户拥有此地址和公钥，您需要额外请求 ton_proof。</span>
<span class="token keyword">type</span> <span class="token class-name">TonAddressItemReply</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  name<span class="token operator">:</span> <span class="token string">"ton_addr"</span><span class="token punctuation">;</span>
  address<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// TON 地址原始 (`0:&lt;hex&gt;`)</span>
  network<span class="token operator">:</span> <span class="token constant">NETWORK</span><span class="token punctuation">;</span> <span class="token comment">// 网络 global_id</span>
  publicKey<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// HEX 字符串，不带 0x</span>
  walletStateInit<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// Base64（不安全 URL）编码的钱包合约的 stateinit cell</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">TonProofItemReply</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
  name<span class="token operator">:</span> <span class="token string">"ton_proof"</span><span class="token punctuation">;</span>
  proof<span class="token operator">:</span> <span class="token punctuation">{</span>
    timestamp<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// 签名操作的 64 位 unix epoch 时间（秒）</span>
    domain<span class="token operator">:</span> <span class="token punctuation">{</span>
      lengthBytes<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> <span class="token comment">// AppDomain 长度</span>
      value<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>  <span class="token comment">// 应用域名（作为 url 部分，无编码）</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    signature<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// base64 编码的签名</span>
    payload<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// 请求中的载荷</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// 目前仅支持主网</span>
<span class="token keyword">enum</span> <span class="token constant">NETWORK</span> <span class="token punctuation">{</span>
  <span class="token constant">MAINNET</span> <span class="token operator">=</span> <span class="token string">'-239'</span><span class="token punctuation">,</span>
  <span class="token constant">TESTNET</span> <span class="token operator">=</span> <span class="token string">'-3'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h3 id="示例">示例<a class="index_header-anchor__Xqb+L" href="#示例" style="opacity:0">#</a></h3>
<p>只是获取用户的地址、公钥等信息：</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">manifestUrl</span><span class="token operator">:</span> <span class="token string">'https://example.com/manifest.json'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">items</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">'ton_addr'</span> <span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>

<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">event</span> <span class="token operator">===</span> <span class="token string">'connect'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">items</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">address</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>获取用户地址、公钥等信息，同时对钱包进行签名验证：</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">manifestUrl</span><span class="token operator">:</span> <span class="token string">'https://example.com/manifest.json'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">items</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span> <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">'ton_addr'</span> <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span> <span class="token literal-property property">name</span><span class="token operator">:</span> <span class="token string">'ton_proof'</span><span class="token punctuation">,</span> <span class="token literal-property property">payload</span><span class="token operator">:</span> <span class="token string">'123'</span> <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>

<span class="token keyword control-flow">if</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">event</span> <span class="token operator">===</span> <span class="token string">'connect'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">items</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">address</span><span class="token punctuation">)</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">items</span><span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">proof</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="restoreConnection" id="restoreconnection">restoreConnection<a class="index_header-anchor__Xqb+L" href="#restoreconnection" style="opacity:0">#</a></h2>
<p>恢复连接的方法，只会返回 <code>ton_addr</code> 指令的结果，如果无法连接钱包，则返回错误。</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token function">restoreConnection</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>ConnectEvent<span class="token operator">&gt;</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="示例">示例<a class="index_header-anchor__Xqb+L" href="#示例" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span><span class="token punctuation">.</span><span class="token method function property-access">restoreConnection</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token keyword control-flow">if</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">event</span> <span class="token operator">===</span> <span class="token string">'connect'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">items</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">address</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span><span class="token property-access">payload</span><span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="send" id="send">send<a class="index_header-anchor__Xqb+L" href="#send" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法：</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token function">send</span><span class="token punctuation">(</span>message<span class="token operator">:</span> AppRequest<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>WalletResponse<span class="token operator">&gt;</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="入参">入参<a class="index_header-anchor__Xqb+L" href="#入参" style="opacity:0">#</a></h3>
<ul>
<li><code>message</code>：发送给钱包的消息体</li>
</ul>
<p><strong>message 入参</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">interface</span> <span class="token class-name">AppRequest</span> <span class="token punctuation">{</span>
    method<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    params<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<ul>
<li><code>method</code>：消息的名称，目前支持 <code>sendTransaction</code> 和 <code>disconnect</code></li>
<li><code>params</code>：消息的参数</li>
<li><code>id</code>：递增的标识符，允许匹配请求和响应</li>
</ul>
<h3 id="sendtransaction-消息">sendTransaction 消息<a class="index_header-anchor__Xqb+L" href="#sendtransaction-消息" style="opacity:0">#</a></h3>
<p>用于签署并广播交易。</p>
<p><strong>入参：</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">interface</span> <span class="token class-name">SendTransactionRequest</span> <span class="token punctuation">{</span>
    method<span class="token operator">:</span> <span class="token string">'sendTransaction'</span><span class="token punctuation">;</span>
    params<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token operator">&lt;</span>transaction<span class="token operator">-</span>payload<span class="token operator">&gt;</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>其中 <code>&lt;transaction-payload&gt;</code> 是具有以下属性的 JSON：</p>
<ul>
<li><code>valid_until</code>（整数，可选）：unix 时间戳。该时刻之后交易将无效。</li>
<li><code>network</code>（NETWORK，可选）：目前仅支持主网</li>
<li><code>from</code>（以 wc:hex 格式的字符串，可选）- DApp打算从中发送交易的发送者地址。</li>
<li><code>messages</code>（信息数组）：1-4 条从钱包合约到其他账户的输出消息。所有消息按顺序发送出去，但钱包无法保证消息会按相同顺序被传递和执行。</li>
</ul>
<p>消息结构：</p>
<ul>
<li><code>address</code>（字符串）：消息目的地</li>
<li><code>amount</code>（小数字符串）：要发送的纳币数量。</li>
<li><code>payload</code>（base64 编码的字符串，可选）：以 Base64 编码的原始cell BoC。</li>
<li><code>stateInit</code>（base64 编码的字符串，可选）：以 Base64 编码的原始cell BoC。</li>
</ul>
<p>示例：</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"valid_until"</span><span class="token operator">:</span> <span class="token number">1658253458</span><span class="token punctuation">,</span>
  <span class="token property">"network"</span><span class="token operator">:</span> <span class="token string">"-239"</span><span class="token punctuation">,</span>
  <span class="token property">"from"</span><span class="token operator">:</span> <span class="token string">"0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f"</span><span class="token punctuation">,</span>
  <span class="token property">"messages"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F"</span><span class="token punctuation">,</span>
      <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"20000000"</span><span class="token punctuation">,</span>
      <span class="token property">"stateInit"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">// 部署合约</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span><span class="token punctuation">{</span>
      <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3"</span><span class="token punctuation">,</span>
      <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"60000000"</span><span class="token punctuation">,</span>
      <span class="token property">"payload"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">// 将 nft 转移至新部署的账户 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>返回值：</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">type</span> <span class="token class-name">SendTransactionResponse</span> <span class="token operator">=</span> SendTransactionResponseSuccess <span class="token operator">|</span> SendTransactionResponseError<span class="token punctuation">;</span>

<span class="token keyword">interface</span> <span class="token class-name">SendTransactionResponseSuccess</span> <span class="token punctuation">{</span>
    result<span class="token operator">:</span> <span class="token operator">&lt;</span>boc<span class="token operator">&gt;</span><span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>

<span class="token punctuation">}</span>

<span class="token keyword">interface</span> <span class="token class-name">SendTransactionResponseError</span> <span class="token punctuation">{</span>
   error<span class="token operator">:</span> <span class="token punctuation">{</span> code<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> message<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
   id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>其中 <code>result</code> 是签名后的签名串。</p>
<h3 id="disconnect-消息">disconnect 消息<a class="index_header-anchor__Xqb+L" href="#disconnect-消息" style="opacity:0">#</a></h3>
<p>用于断开钱包连接。</p>
<p><strong>入参：</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">interface</span> <span class="token class-name">DisconnectRequest</span> <span class="token punctuation">{</span>
    method<span class="token operator">:</span> <span class="token string">'disconnect'</span><span class="token punctuation">;</span>
    params<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>返回值：</strong></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">type</span> <span class="token class-name">DisconnectResponse</span> <span class="token operator">=</span> DisconnectResponseSuccess <span class="token operator">|</span> DisconnectResponseError<span class="token punctuation">;</span>

<span class="token keyword">interface</span> <span class="token class-name">DisconnectResponseSuccess</span> <span class="token punctuation">{</span>
    result<span class="token operator">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>

<span class="token punctuation">}</span>

<span class="token keyword">interface</span> <span class="token class-name">DisconnectResponseError</span> <span class="token punctuation">{</span>
   error<span class="token operator">:</span> <span class="token punctuation">{</span> code<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> message<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
   id<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="listen" id="listen">listen<a class="index_header-anchor__Xqb+L" href="#listen" style="opacity:0">#</a></h2>
<p>监听钱包事件的方法。</p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token function">listen</span><span class="token punctuation">(</span><span class="token function-variable function">callback</span><span class="token operator">:</span> <span class="token punctuation">(</span>event<span class="token operator">:</span> WalletEvent<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="入参">入参<a class="index_header-anchor__Xqb+L" href="#入参" style="opacity:0">#</a></h3>
<ul>
<li><code>callback</code>：事件监听的回调函数</li>
</ul>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">interface</span> <span class="token class-name">WalletEvent</span> <span class="token punctuation">{</span>
    event<span class="token operator">:</span> WalletEventName<span class="token punctuation">;</span>
    id<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> <span class="token comment">// 递增的事件计数器</span>
    payload<span class="token operator">:</span> <span class="token operator">&lt;</span>event<span class="token operator">-</span>payload<span class="token operator">&gt;</span><span class="token punctuation">;</span> <span class="token comment">// 每个事件特定的载荷</span>
<span class="token punctuation">}</span>

<span class="token keyword">type</span> <span class="token class-name">WalletEventName</span> <span class="token operator">=</span> <span class="token string">'connect'</span> <span class="token operator">|</span> <span class="token string">'connect_error'</span> <span class="token operator">|</span> <span class="token string">'disconnect'</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="返回值">返回值<a class="index_header-anchor__Xqb+L" href="#返回值" style="opacity:0">#</a></h3>
<p>返回一个函数，用于取消监听。</p>
<h2 data-content="on / off" id="on-/-off">on / off<a class="index_header-anchor__Xqb+L" href="#on-/-off" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R4tbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R4tbf:">这是专属于 OKX Wallet 的非标准 API，设计该 API 主要是为了支持 accountChanged 事件，可以让 Dapp 响应插件内的钱包切换</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p>添加/移除事件监听，目前支持的事件有：</p>
<ul>
<li><code>connect</code>: 钱包已连接的事件</li>
<li><code>disconnect</code>：当用户断开连接时会触发该事件</li>
<li><code>accountChanged</code>：当用户切换账户时会触发该事件</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">accountChanged</span> <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>
<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'accountChanged'</span><span class="token punctuation">,</span> accountChanged<span class="token punctuation">)</span>
<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxTonWallet</span><span class="token punctuation">.</span><span class="token property-access">tonconnect</span><span class="token punctuation">.</span><span class="token method function property-access">off</span><span class="token punctuation">(</span><span class="token string">'accountChanged'</span><span class="token punctuation">,</span> accountChanged<span class="token punctuation">)</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "TON",
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
    "Provider API"
  ],
  "toc": [
    "什么是 Injected provider API？",
    "特别说明",
    "获取注入的对象",
    "deviceInfo",
    "walletInfo",
    "protocolVersion",
    "connect",
    "restoreConnection",
    "send",
    "listen",
    "on / off"
  ]
}
```

</details>
