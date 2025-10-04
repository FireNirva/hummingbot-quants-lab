# SDK | Ton | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-ton-sdk#断开连接  
**抓取时间:** 2025-05-27 07:33:46  
**字数:** 1125

## 导航路径
DApp 连接钱包 > Ton > SDK

## 目录
- 安装SDK
- 初始化
- 连接钱包
- 恢复连接
- 断开连接
- 判断当前是否连接
- 发送交易
- 监听钱包状态变化
- 监听事件
- 获取账户信息
- 获取钱包信息
- Event事件
- 错误码

---

SDK
#
如果您之前使用过Ton Connect，可以继续使用此文档连接，可以减少开发成本。
如果您之前使用过OKX Connect，可以跳转去使用ProviderSDK进行连接，可以减少开发成本，并且可以支持多个网络同时请求。
ProviderSDK
安装SDK
#
可以通过cdn或者npm安装SDK
通过cdn安装
将如下代码添加到HTML文件中，也可以将latest替换为特定的版本号例如1.6.1。
<script src="https://unpkg.com/@okxconnect/tonsdk@latest/dist/okxconnect_tonsdk.min.js"></script>
引入后，OKXTonConnectSDK会作为全局对象可以直接引用
<script> const connector = new OKXTonConnectSDK.OKXTonConnect(); </script>
通过npm安装
npm install @okxconnect/tonsdk
初始化
#
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作
new OKXTonConnect({metaData: {name, icon}})
请求参数
metaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。
返回值
okxTonConnect - OKXTonConnect
示例
import
{
OKXTonConnect
}
from
"@okxconnect/tonsdk"
;
const
okxTonConnect
=
new
OKXTonConnect
(
{
metaData
:
{
name
:
"application name"
,
icon
:
"application icon url"
}
}
)
;
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数
connect(request): Promise<string>;
请求参数
request - object (可选)
tonProof - string (可选) : 签名信息
redirect - string (可选) : 处理完钱包事件，返回的app 所需要的deeplink，例如：在 Telegram 环境下，此字段需要传递 Telegram
的deeplink，当在钱包签名完成后，OKX App 会通过此deeplink 打开 Telegram 程序，非Telegram环境建议不设置
openUniversalLink - boolean (可选) : 连接钱包时,是否通过 Universal link 唤起 OKX App 客户端；设置为 true
的情况下，用户发起连接钱包时，会拉起 OKX App 客户端，并弹出确认页面，如果手机未安装 OKX App 客户端，跳转到下载页
返回值
Promise - string: PC 网页端可以根据该字段生成二维码，OKX App 客户端在 web3 中扫描生成的二维码，连接 DApp
建议
在手机浏览器或者手机 Telegram 环境下设置 openUniversalLink 为 true
在 PC 浏览器环境下设置 openUniversalLink 为 false，并根据返回的 universalLink 生成二维码，可以用 OKX App 客户端扫码连接，在连接成功后，取消二维码弹窗
示例
import
{
OKXConnectError
}
from
"@okxconnect/tonsdk"
;
try
{
okxTonConnect
.
connect
(
{
tonProof
:
"signmessage"
,
redirect
:
"tg://resolve"
,
openUniversalLink
:
true
}
)
}
catch
(
error
)
{
if
(
error
instanceof
OKXConnectError
)
{
if
(
error
.
code
===
OKX_CONNECT_ERROR_CODES
.
USER_REJECTS_ERROR
)
{
alert
(
'User reject'
)
;
}
else
if
(
error
.
code
===
OKX_CONNECT_ERROR_CODES
.
ALREADY_CONNECTED_ERROR
)
{
alert
(
'Already connected'
)
;
}
else
{
alert
(
'Unknown error happened'
)
;
}
}
else
{
alert
(
'Unknown error happened'
)
;
}
}
恢复连接
#
如果用户之前连接过钱包，在再次进入或页面刷新时可调用此方法，用来恢复之前的连接状态
restoreConnection(): Promise<void>
请求参数
无
返回值
无
示例
okxTonConnect
.
restoreConnection
(
)
断开连接
#
断开已连接钱包，并删除当前会话，如果要切换连接钱包，请先断开当前钱包
示例
import
{
OKX_CONNECT_ERROR_CODES
}
from
"@okxconnect/tonsdk"
;
try
{
await
okxTonConnect
.
disconnect
(
)
}
catch
(
error
)
{
if
(
error
instanceof
OKXConnectError
)
{
switch
(
error
.
code
)
{
case
OKX_CONNECT_ERROR_CODES
.
NOT_CONNECTED_ERROR
:
alert
(
'Not connected'
)
;
break
;
default
:
alert
(
'Unknown error happened'
)
;
break
;
}
}
else
{
alert
(
'Unknown error happened'
)
;
}
}
判断当前是否连接
#
获取当前是否有连接钱包
示例
var
connect
:
boolean
=
okxTonConnect
.
connected
(
)
发送交易
#
向钱包发送消息的方法：
sendTransaction(transaction, options): Promise<SendTransactionResponse>
请求参数
transaction - object
validUntil - number :unix 时间戳。该时刻之后交易将无效
from - string (可选): DApp发送交易的发送者地址，默认为当前连接的钱包地址；
messages - object[] : （信息数组）： 1-4 条从钱包合约到其他账户的输出消息。所有消息按顺序发送出去，但
钱包无法保证消息会按相同顺序被传递和执行
address - string : 消息目的地
amount - string : 要发送的数量
stateInit - string (可选) : 以 Base64 编码的原始cell BoC
payload - string (可选): 以 Base64 编码的原始cell BoC
options - object
onRequestSent - () => void : 当签名请求发送后，该方法会被调用
返回值
Promise -
{boc: string}
: 签名结果
示例
import
{
OKXConnectError
}
from
"@okxconnect/tonsdk"
;
let
transactionRequest
=
{
"validUntil"
:
Date
.
now
(
)
/
1000
+
360
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
//deploy contract
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
//transfer nft to new deployed account 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F
}
]
}
let
requestOptions
=
{
onRequestSent
:
(
)
=>
{
//requestMsgSend
}
}
try
{
const
result
=
await
okxTonConnect
.
sendTransaction
(
transactionRequest
,
requestOptions
)
;
}
catch
(
error
)
{
if
(
error
instanceof
OKXConnectError
)
{
switch
(
error
.
code
)
{
case
OKX_CONNECT_ERROR_CODES
.
USER_REJECTS_ERROR
:
alert
(
'You rejected the transaction.'
)
;
break
;
case
OKX_CONNECT_ERROR_CODES
.
NOT_CONNECTED_ERROR
:
alert
(
'Not connected'
)
;
break
;
default
:
alert
(
'Unknown error happened'
)
;
break
;
}
}
else
{
alert
(
'Unknown error happened'
)
;
}
}
监听钱包状态变化
#
钱包状态有：连接成功、恢复连接成功、断开连接等，都可以用此方法获取状态
onStatusChange( callback: (walletInfo) => void, errorsHandler?: (err) => void ): () => void;
请求参数
callback - (walletInfo) => void : 钱包状态发生变化时候，该callback 会被调用
walletinfo - object
device - object
appName - string : 钱包名称
platform - string : 钱包的平台，（android,ios）
appVersion - string : 钱包版本号
maxProtocolVersion - number :
features - string[] : 支持的方法，当前版本是 sendTransaction
account - Account
address - string : TON address raw (
0:<hex>
)
chain - "-239"
walletStateInit - string : Base64 (not url safe) encoded stateinit cell for the wallet contract
publicKey - string : HEX string without 0x
connectItems - object
name - string : "ton_proof"
proof - object
timestamp - number : 时间戳
domain - object
lengthBytes - number : AppDomain Length
value - string : app domain name (as url part, without encoding)
payload - string: Base64-encoded signature
signature - string: payload from the request
errorsHandler - (err: OKXConnectError) => void : 钱包状态发生变化出现异常的时候，该errorsHandler 会被调用
err - TonConnectError
code - number
message - string
返回值
() => void : 当不再需要监听更新时，执行该方法以节省资源
示例
import
{
Wallet
}
from
"@okxconnect/tonsdk"
;
const
unsubscribe
=
okxTonConnect
.
onStatusChange
(
(
walletInfo
:
Wallet
|
null
)
=>
{
console
.
log
(
'Connection status:'
,
walletInfo
)
;
}
,
(
err
:
OKXConnectError
)
=>
{
console
.
log
(
'Connection status:'
,
err
)
;
}
)
当不再需要监听更新时，调用unsubscribe节省资源
unsubscribe
(
)
监听事件
#
在以下事件发生时，会发送对应事件通知，Dapp可以根据需要添加监听，来处理对应的逻辑
event事件
事件名称
触发时机
OKX_TON_CONNECTION_STARTED
当用户开始连接钱包时
OKX_TON_CONNECTION_COMPLETED
当用户成功连接钱包时
OKX_TON_CONNECTION_ERROR
当用户取消连接或连接过程中出现错误时
OKX_TON_CONNECTION_RESTORING_STARTED
当 dApp 开始恢复连接时
OKX_TON_CONNECTION_RESTORING_COMPLETED
当 dApp 成功恢复连接时
OKX_TON_CONNECTION_RESTORING_ERROR
当 dApp 无法恢复连接时
OKX_TON_DISCONNECTION
当用户开始断开钱包连接时
OKX_TON_TRANSACTION_SENT_FOR_SIGNATURE
当用户发送交易以供签名时
OKX_TON_TRANSACTION_SIGNED
当用户成功签署交易时
OKX_TON_TRANSACTION_SIGNING_FAILED
当用户取消交易签名或签名过程中出现错误时
示例
import
{
OKX_TON_CONNECTION_AND_TRANSACTION_EVENT
}
from
"@okxconnect/tonsdk"
;
window
.
addEventListener
(
OKX_TON_CONNECTION_AND_TRANSACTION_EVENT
.
OKX_TON_CONNECTION_STARTED
,
(
event
)
=>
{
if
(
event
instanceof
CustomEvent
)
{
console
.
log
(
'Transaction init'
,
event
.
detail
)
;
}
}
)
;
获取账户信息
#
获取当前连接的 account
示例
import
{
Account
}
from
"@okxconnect/tonsdk"
;
var
connect
:
Account
=
okxTonConnect
.
account
(
)
获取钱包信息
#
获取当前连接的 wallet
示例
import
{
Wallet
}
from
"@okxconnect/tonsdk"
;
var
connect
:
Wallet
=
okxTonConnect
.
wallet
(
)
Event事件
#
// 生成 universalLink
universalUi
.
on
(
"display_uri"
,
(
uri
)
=>
{
console
.
log
(
uri
)
;
}
)
;
// session 信息变更会触发该事件；
universalUi
.
on
(
"session_update"
,
(
session
)
=>
{
console
.
log
(
JSON
.
stringify
(
session
)
)
;
}
)
;
// 断开连接会触发该事件；
universalUi
.
on
(
"session_delete"
,
(
{
topic
}
)
=>
{
console
.
log
(
topic
)
;
}
)
;
// 连接并签名时,签名结果会触发该事件;
universalUi
.
on
(
"connect_signResponse"
,
(
signResponse
)
=>
{
console
.
log
(
signResponse
)
;
}
)
;
错误码
#
在连接，交易，断开连接的过程中可能抛出的异常;
异常
错误码
描述
OKX_CONNECT_ERROR_CODES.UNKNOWN_ERROR
未知异常
OKX_CONNECT_ERROR_CODES.ALREADY_CONNECTED_ERROR
钱包已连接
OKX_CONNECT_ERROR_CODES.NOT_CONNECTED_ERROR
钱包未连接
OKX_CONNECT_ERROR_CODES.USER_REJECTS_ERROR
用户拒绝
OKX_CONNECT_ERROR_CODES.METHOD_NOT_SUPPORTED
方法不支持
OKX_CONNECT_ERROR_CODES.CHAIN_NOT_SUPPORTED
链不支持
OKX_CONNECT_ERROR_CODES.WALLET_NOT_SUPPORTED
钱包不支持
OKX_CONNECT_ERROR_CODES.CONNECTION_ERROR
连接异常
export
enum
OKX_CONNECT_ERROR_CODES
{
UNKNOWN_ERROR
=
0
,
ALREADY_CONNECTED_ERROR
=
11
,
NOT_CONNECTED_ERROR
=
12
,
USER_REJECTS_ERROR
=
300
,
METHOD_NOT_SUPPORTED
=
400
,
CHAIN_NOT_SUPPORTED
=
500
,
WALLET_NOT_SUPPORTED
=
600
,
CONNECTION_ERROR
=
700
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="sdk">SDK<a class="index_header-anchor__Xqb+L" href="#sdk" style="opacity:0">#</a></h1>
<p>如果您之前使用过Ton Connect，可以继续使用此文档连接，可以减少开发成本。</p>
<p>如果您之前使用过OKX Connect，可以跳转去使用ProviderSDK进行连接，可以减少开发成本，并且可以支持多个网络同时请求。</p>
<a class="flex justify-start items-center index_card__Pvw5e" href="/zh-hans/build/dev-docs/sdks/app-connect-ton-provider-sdk"><i aria-hidden="true" class="icon iconfont okx-defi-okc-tf-contract index_icon__jz5er" role="img"></i><div class="index_head__iMYf1"><div class="truncate index_title__Tcv0Y">ProviderSDK</div></div></a>
<h2 data-content="安装SDK" id="安装sdk">安装SDK<a class="index_header-anchor__Xqb+L" href="#安装sdk" style="opacity:0">#</a></h2>
<p>可以通过cdn或者npm安装SDK</p>
<p><strong>通过cdn安装</strong>
将如下代码添加到HTML文件中，也可以将latest替换为特定的版本号例如1.6.1。</p>
<p><code>&lt;script src="https://unpkg.com/@okxconnect/tonsdk@latest/dist/okxconnect_tonsdk.min.js"&gt;&lt;/script&gt;</code></p>
<p>引入后，OKXTonConnectSDK会作为全局对象可以直接引用</p>
<p><code>&lt;script&gt; const connector = new OKXTonConnectSDK.OKXTonConnect(); &lt;/script&gt;</code></p>
<p><strong>通过npm安装</strong></p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/tonsdk</code></pre></div>
<h2 data-content="初始化" id="初始化">初始化<a class="index_header-anchor__Xqb+L" href="#初始化" style="opacity:0">#</a></h2>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作</p>
<p><code>new OKXTonConnect({metaData: {name, icon}})</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>metaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>okxTonConnect - OKXTonConnect</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXTonConnect <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> okxTonConnect <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXTonConnect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    metaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        name<span class="token operator">:</span> <span class="token string">"application name"</span><span class="token punctuation">,</span>
        icon<span class="token operator">:</span> <span class="token string">"application icon url"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<p><code>connect(request): Promise&lt;string&gt;;</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>request - object (可选)<!-- -->
<ul>
<li>tonProof - string (可选) : 签名信息</li>
<li>redirect - string (可选) : 处理完钱包事件，返回的app 所需要的deeplink，例如：在 Telegram 环境下，此字段需要传递 Telegram
的deeplink，当在钱包签名完成后，OKX App 会通过此deeplink 打开 Telegram 程序，非Telegram环境建议不设置</li>
<li>openUniversalLink - boolean (可选) : 连接钱包时,是否通过 Universal link 唤起 OKX App 客户端；设置为 true
的情况下，用户发起连接钱包时，会拉起 OKX App 客户端，并弹出确认页面，如果手机未安装 OKX App 客户端，跳转到下载页</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string: PC 网页端可以根据该字段生成二维码，OKX App 客户端在 web3 中扫描生成的二维码，连接 DApp</li>
</ul>
<p><strong>建议</strong></p>
<ul>
<li>在手机浏览器或者手机 Telegram 环境下设置 openUniversalLink 为 true</li>
<li>在 PC 浏览器环境下设置 openUniversalLink 为 false，并根据返回的 universalLink 生成二维码，可以用 OKX App 客户端扫码连接，在连接成功后，取消二维码弹窗</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXConnectError <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">try</span> <span class="token punctuation">{</span>
    okxTonConnect<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        tonProof<span class="token operator">:</span> <span class="token string">"signmessage"</span><span class="token punctuation">,</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span><span class="token punctuation">,</span>
        openUniversalLink<span class="token operator">:</span> <span class="token boolean">true</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">OKXConnectError</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">USER_REJECTS_ERROR</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'User reject'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">ALREADY_CONNECTED_ERROR</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Already connected'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
            <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="恢复连接" id="恢复连接">恢复连接<a class="index_header-anchor__Xqb+L" href="#恢复连接" style="opacity:0">#</a></h2>
<p>如果用户之前连接过钱包，在再次进入或页面刷新时可调用此方法，用来恢复之前的连接状态</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">restoreConnection(): Promise&lt;void&gt;</code></pre></div>
<p><strong>请求参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<p>无</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxTonConnect<span class="token punctuation">.</span><span class="token function">restoreConnection</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="断开连接" id="断开连接">断开连接<a class="index_header-anchor__Xqb+L" href="#断开连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包，并删除当前会话，如果要切换连接钱包，请先断开当前钱包</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span> <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">await</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">OKXConnectError</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">switch</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span>code<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">case</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">NOT_CONNECTED_ERROR</span><span class="token operator">:</span>
                <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Not connected'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
            <span class="token keyword">default</span><span class="token operator">:</span>
                <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="判断当前是否连接" id="判断当前是否连接">判断当前是否连接<a class="index_header-anchor__Xqb+L" href="#判断当前是否连接" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> connect<span class="token operator">:</span> <span class="token builtin">boolean</span> <span class="token operator">=</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">connected</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="发送交易" id="发送交易">发送交易<a class="index_header-anchor__Xqb+L" href="#发送交易" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法：</p>
<p><code>sendTransaction(transaction, options): Promise&lt;SendTransactionResponse&gt;</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>transaction - object<!-- -->
<ul>
<li>validUntil - number :unix 时间戳。该时刻之后交易将无效</li>
<li>from - string (可选): DApp发送交易的发送者地址，默认为当前连接的钱包地址；</li>
<li>messages - object[] : （信息数组）： 1-4 条从钱包合约到其他账户的输出消息。所有消息按顺序发送出去，但
钱包无法保证消息会按相同顺序被传递和执行<!-- -->
<ul>
<li>address - string : 消息目的地</li>
<li>amount - string : 要发送的数量</li>
<li>stateInit - string (可选) : 以 Base64 编码的原始cell BoC</li>
<li>payload - string (可选): 以 Base64 编码的原始cell BoC</li>
</ul>
</li>
</ul>
</li>
<li>options - object<!-- -->
<ul>
<li>onRequestSent - () =&gt; void : 当签名请求发送后，该方法会被调用</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - <code>{boc: string}</code>: 签名结果</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXConnectError <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">let</span> transactionRequest <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"validUntil"</span><span class="token operator">:</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token number">1000</span> <span class="token operator">+</span> <span class="token number">360</span><span class="token punctuation">,</span>
    <span class="token string-property property">"from"</span><span class="token operator">:</span> <span class="token string">"0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"messages"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"20000000"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"stateInit"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">//deploy contract</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
            <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"60000000"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"payload"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">//transfer nft to new deployed account 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

<span class="token keyword">let</span> requestOptions <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token function-variable function">onRequestSent</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token comment">//requestMsgSend</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">sendTransaction</span><span class="token punctuation">(</span>transactionRequest<span class="token punctuation">,</span> requestOptions<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">OKXConnectError</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">switch</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span>code<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">case</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">USER_REJECTS_ERROR</span><span class="token operator">:</span>
                <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'You rejected the transaction.'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
            <span class="token keyword">case</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">NOT_CONNECTED_ERROR</span><span class="token operator">:</span>
                <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Not connected'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
            <span class="token keyword">default</span><span class="token operator">:</span>
                <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        <span class="token function">alert</span><span class="token punctuation">(</span><span class="token string">'Unknown error happened'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="监听钱包状态变化" id="监听钱包状态变化">监听钱包状态变化<a class="index_header-anchor__Xqb+L" href="#监听钱包状态变化" style="opacity:0">#</a></h2>
<p>钱包状态有：连接成功、恢复连接成功、断开连接等，都可以用此方法获取状态</p>
<p><code>onStatusChange( callback: (walletInfo) =&gt; void, errorsHandler?: (err) =&gt; void ): () =&gt; void;</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>
<p>callback - (walletInfo) =&gt; void : 钱包状态发生变化时候，该callback 会被调用</p>
<ul>
<li>walletinfo - object<!-- -->
<ul>
<li>device - object<!-- -->
<ul>
<li>appName - string : 钱包名称</li>
<li>platform - string : 钱包的平台，（android,ios）</li>
<li>appVersion - string : 钱包版本号</li>
<li>maxProtocolVersion - number :</li>
<li>features - string[] : 支持的方法，当前版本是 sendTransaction</li>
</ul>
</li>
<li>account - Account<!-- -->
<ul>
<li>address - string : TON address raw (<code>0:&lt;hex&gt;</code>)</li>
<li>chain - "-239"</li>
<li>walletStateInit - string : Base64 (not url safe) encoded stateinit cell for the wallet contract</li>
<li>publicKey - string : HEX string without 0x</li>
</ul>
</li>
<li>connectItems - object<!-- -->
<ul>
<li>name - string : "ton_proof"</li>
<li>proof - object<!-- -->
<ul>
<li>timestamp - number : 时间戳</li>
<li>domain - object<!-- -->
<ul>
<li>lengthBytes - number : AppDomain Length</li>
<li>value - string : app domain name (as url part, without encoding)</li>
</ul>
</li>
<li>payload - string: Base64-encoded signature</li>
<li>signature - string: payload from the request</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li>
<p>errorsHandler - (err: OKXConnectError) =&gt; void : 钱包状态发生变化出现异常的时候，该errorsHandler 会被调用</p>
<ul>
<li>err - TonConnectError<!-- -->
<ul>
<li>code - number</li>
<li>message - string</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>() =&gt; void : 当不再需要监听更新时，执行该方法以节省资源</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> Wallet <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> unsubscribe <span class="token operator">=</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">onStatusChange</span><span class="token punctuation">(</span><span class="token punctuation">(</span>walletInfo<span class="token operator">:</span> Wallet <span class="token operator">|</span> <span class="token keyword">null</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Connection status:'</span><span class="token punctuation">,</span> walletInfo<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>err<span class="token operator">:</span> OKXConnectError<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Connection status:'</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">)</span>
</code></pre></div>
<p>当不再需要监听更新时，调用unsubscribe节省资源</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token function">unsubscribe</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="监听事件" id="监听事件">监听事件<a class="index_header-anchor__Xqb+L" href="#监听事件" style="opacity:0">#</a></h2>
<p>在以下事件发生时，会发送对应事件通知，Dapp可以根据需要添加监听，来处理对应的逻辑</p>
<p><strong>event事件</strong></p>
<div class="index_table__kvZz5"><table><thead><tr><th>事件名称</th><th>触发时机</th></tr></thead><tbody><tr><td>OKX_TON_CONNECTION_STARTED</td><td>当用户开始连接钱包时</td></tr><tr><td>OKX_TON_CONNECTION_COMPLETED</td><td>当用户成功连接钱包时</td></tr><tr><td>OKX_TON_CONNECTION_ERROR</td><td>当用户取消连接或连接过程中出现错误时</td></tr><tr><td>OKX_TON_CONNECTION_RESTORING_STARTED</td><td>当 dApp 开始恢复连接时</td></tr><tr><td>OKX_TON_CONNECTION_RESTORING_COMPLETED</td><td>当 dApp 成功恢复连接时</td></tr><tr><td>OKX_TON_CONNECTION_RESTORING_ERROR</td><td>当 dApp 无法恢复连接时</td></tr><tr><td>OKX_TON_DISCONNECTION</td><td>当用户开始断开钱包连接时</td></tr><tr><td>OKX_TON_TRANSACTION_SENT_FOR_SIGNATURE</td><td>当用户发送交易以供签名时</td></tr><tr><td>OKX_TON_TRANSACTION_SIGNED</td><td>当用户成功签署交易时</td></tr><tr><td>OKX_TON_TRANSACTION_SIGNING_FAILED</td><td>当用户取消交易签名或签名过程中出现错误时</td></tr></tbody></table></div>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> <span class="token constant">OKX_TON_CONNECTION_AND_TRANSACTION_EVENT</span> <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

window<span class="token punctuation">.</span><span class="token function">addEventListener</span><span class="token punctuation">(</span><span class="token constant">OKX_TON_CONNECTION_AND_TRANSACTION_EVENT</span><span class="token punctuation">.</span><span class="token constant">OKX_TON_CONNECTION_STARTED</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>event<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>event <span class="token keyword">instanceof</span> <span class="token class-name">CustomEvent</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Transaction init'</span><span class="token punctuation">,</span> event<span class="token punctuation">.</span>detail<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<p>获取当前连接的 account</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> Account <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">var</span> connect<span class="token operator">:</span> Account <span class="token operator">=</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取钱包信息" id="获取钱包信息">获取钱包信息<a class="index_header-anchor__Xqb+L" href="#获取钱包信息" style="opacity:0">#</a></h2>
<p>获取当前连接的 wallet</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> Wallet <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">var</span> connect<span class="token operator">:</span> Wallet <span class="token operator">=</span> okxTonConnect<span class="token punctuation">.</span><span class="token function">wallet</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 生成 universalLink</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"display_uri"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>uri<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>uri<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// session 信息变更会触发该事件；</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_update"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 断开连接会触发该事件；</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_delete"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>topic<span class="token punctuation">}</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>topic<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 连接并签名时,签名结果会触发该事件;</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect_signResponse"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="错误码" id="错误码">错误码<a class="index_header-anchor__Xqb+L" href="#错误码" style="opacity:0">#</a></h2>
<p>在连接，交易，断开连接的过程中可能抛出的异常;</p>
<p><strong>异常</strong></p>
<div class="index_table__kvZz5"><table><thead><tr><th>错误码</th><th>描述</th></tr></thead><tbody><tr><td>OKX_CONNECT_ERROR_CODES.UNKNOWN_ERROR</td><td>未知异常</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.ALREADY_CONNECTED_ERROR</td><td>钱包已连接</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.NOT_CONNECTED_ERROR</td><td>钱包未连接</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.USER_REJECTS_ERROR</td><td>用户拒绝</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.METHOD_NOT_SUPPORTED</td><td>方法不支持</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.CHAIN_NOT_SUPPORTED</td><td>链不支持</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.WALLET_NOT_SUPPORTED</td><td>钱包不支持</td></tr><tr><td>OKX_CONNECT_ERROR_CODES.CONNECTION_ERROR</td><td>连接异常</td></tr></tbody></table></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">export</span> <span class="token keyword">enum</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span> <span class="token punctuation">{</span>
    <span class="token constant">UNKNOWN_ERROR</span> <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">,</span>
    <span class="token constant">ALREADY_CONNECTED_ERROR</span> <span class="token operator">=</span> <span class="token number">11</span><span class="token punctuation">,</span>
    <span class="token constant">NOT_CONNECTED_ERROR</span> <span class="token operator">=</span> <span class="token number">12</span><span class="token punctuation">,</span>
    <span class="token constant">USER_REJECTS_ERROR</span> <span class="token operator">=</span> <span class="token number">300</span><span class="token punctuation">,</span>
    <span class="token constant">METHOD_NOT_SUPPORTED</span> <span class="token operator">=</span> <span class="token number">400</span><span class="token punctuation">,</span>
    <span class="token constant">CHAIN_NOT_SUPPORTED</span> <span class="token operator">=</span> <span class="token number">500</span><span class="token punctuation">,</span>
    <span class="token constant">WALLET_NOT_SUPPORTED</span> <span class="token operator">=</span> <span class="token number">600</span><span class="token punctuation">,</span>
    <span class="token constant">CONNECTION_ERROR</span> <span class="token operator">=</span> <span class="token number">700</span>
<span class="token punctuation">}</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "Ton",
    "SDK"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Solana 兼容链",
    "TON",
    "SDK",
    "UI",
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
    "Solana 兼容链"
  ],
  "toc": [
    "安装SDK",
    "初始化",
    "连接钱包",
    "恢复连接",
    "断开连接",
    "判断当前是否连接",
    "发送交易",
    "监听钱包状态变化",
    "监听事件",
    "获取账户信息",
    "获取钱包信息",
    "Event事件",
    "错误码"
  ]
}
```

</details>
