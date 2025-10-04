# UI | Ton | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-ton-ui#设置tonproof  
**抓取时间:** 2025-05-27 06:41:16  
**字数:** 854

## 导航路径
DApp 连接钱包 > Ton > UI

## 目录
- 通过npm安装
- 初始化
- 监听钱包状态变化
- 连接钱包
- 设置tonProof
- 关闭连接弹窗
- 获取当前连接的Wallet和WalletInfo
- 断开钱包连接
- 发送交易
- 设置ui配置项
- 监听事件
- Event事件
- 错误码

---

UI
#
在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运营在 Telegram内，则用户可以选择唤起移动端App钱包或者停留在Telegram并唤起欧易 Telegram Mini 钱包。
如果您之前使用过Ton Connect，可以继续使用此文档连接，可以减少开发成本。
如果您之前使用过OKX Connect，可以跳转去使用ProviderUI进行连接，可以减少开发成本，并且可以支持多个网络同时请求。
ProviderUI
通过npm安装
#
npm install @okxconnect/ui
初始化
#
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作
new OKXTonConnectUI(dappMetaData, buttonRootId, actionsConfiguration, uiPreferences, language, restoreConnection)
请求参数
metaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。
buttonRootId - string: 用于附加钱包连接按钮的 HTML 元素 ID。如果没有传递，则不会出现按钮;
actionsConfiguration - object
modals - ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式。
returnStrategy -string 'none' |
${string}://${string}
; 指定当用户签署/拒绝请求时深层链接的返回策略，如果是在tg中，可以配置tg://resolve
tmaReturnUrl -string 'back' | 'none' |
${string}://${string}
; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出dapp；none 表示签名后不做处理；默认为back；
uiPreferences -object
theme - Theme 可以是：THEME.DARK, THEME.LIGHT, "SYSTEM"
language - "en_US" | "ru_RU" | "zh_CN" | "ar_AE" | "cs_CZ" | "de_DE" | "es_ES" | "es_LAT" | "fr_FR" | "id_ID" | "it_IT" | "nl_NL" | "pl_PL" | "pt_BR" | "pt_PT" | "ro_RO" | "tr_TR" | "uk_UA" | "vi_VN";
, 默认为en_US
restoreConnection?: boolean - 是否自动回复之前的连接；
返回值
OKXTonConnectUI
示例
import
{
OKXTonConnectUI
}
from
"@okxconnect/ui"
;
const
okxTonConnectUI
=
new
OKXTonConnectUI
(
{
dappMetaData
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
,
buttonRootId
:
'button-root'
,
actionsConfiguration
:
{
returnStrategy
:
'none'
,
tmaReturnUrl
:
'back'
}
,
uiPreferences
:
{
theme
:
THEME
.
LIGHT
}
,
language
:
'en_US'
,
restoreConnection
:
true
}
)
;
监听钱包状态变化
#
钱包状态有：连接成功、恢复连接成功、断开连接等，都可以用此方法获取状态。
方法详情同OKXTonConnect.onStatusChange
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
okxTonConnectUI
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
当不再需要监听更新时，调用unsubscribe节省资源。
unsubscribe
(
)
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数，
“连接按钮”（添加于buttonRootId）会自动处理点击并调用连接，
如果没有添加buttonRootId 的话，需要调用此方法。
await okxTonConnectUI.openModal();
示例
okxTonConnectUI
.
openModal
(
)
;
设置tonProof
#
添加连接签名参数,
如果需要设置tonProof，请在准备好tonProof 参数之前，设置state:'loading',
在准备好之后，将state设置为 'ready'并添加value;
也可以通过设置setConnectRequestParameters(null) 移除掉loading 状态
示例
okxtonConnectUI
.
setConnectRequestParameters
(
{
state
:
'loading'
}
)
;
const
tonProofPayload
:
string
|
null
=
await
fetchTonProofPayloadFromBackend
(
)
;
if
(
!
tonProofPayload
)
{
okxtonConnectUI
.
setConnectRequestParameters
(
null
)
;
}
else
{
okxtonConnectUI
.
setConnectRequestParameters
(
{
state
:
"ready"
,
value
:
{
tonProof
:
tonProofPayload
}
}
)
;
}
关闭连接弹窗
#
示例
okxTonConnectUI
.
closeModal
(
)
;
获取当前连接的Wallet和WalletInfo
#
获取当前是否有连接钱包，以及已连接的钱包的相关信息
示例
const
currentWallet
=
okxTonConnectUI
.
wallet
;
const
currentAccount
=
okxTonConnectUI
.
account
;
const
isConnected
=
okxTonConnectUI
.
connected
;
断开钱包连接
#
示例
okxTonConnectUI
.
disconnect
(
)
发送交易
#
向钱包发送消息的方法：
sendTransaction(transaction, actionConfigurationRequest): Promise<SendTransactionResponse>
请求参数
transaction - object,
参数同OKXTonConnect.sendTransaction的transaction
actionConfigurationRequest - object
modals : ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，默认为'before'
returnStrategy -string 'none' |
${string}://${string}
; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取init方法传递的 returnStrategy，默认为 ‘none’
tmaReturnUrl -string 'back' | 'none' |
${string}://${string}
; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出dapp；none 表示签名后不做处理；默认为back；
返回值
Promise -
{boc: string}
: 签名结果
示例
import
{
OKXConnectError
,
OKX_CONNECT_ERROR_CODES
}
from
"@okxconnect/core"
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
okxTonConnectUI
.
sendTransaction
(
transactionRequest
,
{
modals
:
'all'
,
tmaReturnUrl
:
'back'
}
)
.
then
(
(
result
)
=>
{
let
boc
=
result
.
boc
}
)
.
catch
(
(
error
)
=>
{
if
(
error
instanceof
OKXConnectError
&&
error
.
code
==
OKX_CONNECT_ERROR_CODES
.
USER_REJECTS_ERROR
)
{
//userReject;
}
else
{
//other error;
}
}
)
设置ui配置项
#
支持修改主题，文字语言设置，也可以在初始化的时候添加这些配置
示例
okxTonConnectUI
.
uiOptions
=
{
language
:
'zh_CN'
,
uiPreferences
:
{
theme
:
THEME
.
DARK
}
}
;
监听事件
#
在以下事件发生时，会发送对应事件通知，Dapp可以根据需要添加监听，来处理对应的逻辑
event事件
事件名称
触发时机
OKX_UI_CONNECTION_STARTED
当用户开始连接钱包时
OKX_UI_CONNECTION_COMPLETED
当用户成功连接钱包时
OKX_UI_CONNECTION_ERROR
当用户取消连接或连接过程中出现错误时
OKX_UI_CONNECTION_RESTORING_STARTED
当 dApp 开始恢复连接时
OKX_UI_CONNECTION_RESTORING_COMPLETED
当 dApp 成功恢复连接时
OKX_UI_CONNECTION_RESTORING_ERROR
当 dApp 无法恢复连接时
OKX_UI_DISCONNECTION
当用户开始断开钱包连接时
OKX_UI_TRANSACTION_SENT_FOR_SIGNATURE
当用户发送交易以供签名时
OKX_UI_TRANSACTION_SIGNED
当用户成功签署交易时
OKX_UI_TRANSACTION_SIGNING_FAILED
当用户取消交易签名或签名过程中出现错误时
示例
import
{
OKX_UI_CONNECTION_AND_TRANSACTION_EVENT
}
from
"@okxconnect/ui"
;
window
.
addEventListener
(
OKX_UI_CONNECTION_AND_TRANSACTION_EVENT
.
OKX_UI_CONNECTION_STARTED
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
在连接，交易，断开连接的过程中可能抛出的异常
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
<div class="routes_md__xWlGF"><!--$--><h1 id="ui">UI<a class="index_header-anchor__Xqb+L" href="#ui" style="opacity:0">#</a></h1>
<p>在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运营在 Telegram内，则用户可以选择唤起移动端App钱包或者停留在Telegram并唤起欧易 Telegram Mini 钱包。</p>
<p>如果您之前使用过Ton Connect，可以继续使用此文档连接，可以减少开发成本。</p>
<p>如果您之前使用过OKX Connect，可以跳转去使用ProviderUI进行连接，可以减少开发成本，并且可以支持多个网络同时请求。</p>
<a class="flex justify-start items-center index_card__Pvw5e" href="/zh-hans/build/dev-docs/sdks/app-connect-ton-provider-ui"><i aria-hidden="true" class="icon iconfont okx-defi-okc-tf-contract index_icon__jz5er" role="img"></i><div class="index_head__iMYf1"><div class="truncate index_title__Tcv0Y">ProviderUI</div></div></a>
<h2 data-content="通过npm安装" id="通过npm安装">通过npm安装<a class="index_header-anchor__Xqb+L" href="#通过npm安装" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/ui</code></pre></div>
<h2 data-content="初始化" id="初始化">初始化<a class="index_header-anchor__Xqb+L" href="#初始化" style="opacity:0">#</a></h2>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作</p>
<p><code>new OKXTonConnectUI(dappMetaData, buttonRootId, actionsConfiguration, uiPreferences, language, restoreConnection)</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>metaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。</li>
</ul>
</li>
<li>buttonRootId - string: 用于附加钱包连接按钮的 HTML 元素 ID。如果没有传递，则不会出现按钮;</li>
<li>actionsConfiguration - object<!-- -->
<ul>
<li>modals - ('before' | 'success' | 'error')[] | 'all'  交易过程中的提醒界面展示模式。</li>
<li>returnStrategy -string 'none' | <code>${string}://${string}</code>; 指定当用户签署/拒绝请求时深层链接的返回策略，如果是在tg中，可以配置tg://resolve</li>
<li>tmaReturnUrl -string 'back' | 'none' | <code>${string}://${string}</code>; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出dapp；none 表示签名后不做处理；默认为back；</li>
</ul>
</li>
<li>uiPreferences -object<!-- -->
<ul>
<li>theme -  Theme 可以是：THEME.DARK, THEME.LIGHT, "SYSTEM"</li>
</ul>
</li>
<li>language - "en_US" | "ru_RU" | "zh_CN" | "ar_AE" | "cs_CZ" | "de_DE" | "es_ES" | "es_LAT" | "fr_FR" | "id_ID" | "it_IT" | "nl_NL" | "pl_PL" | "pt_BR" | "pt_PT" | "ro_RO" | "tr_TR" | "uk_UA" | "vi_VN";
, 默认为en_US</li>
<li>restoreConnection?: boolean - 是否自动回复之前的连接；</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>OKXTonConnectUI</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXTonConnectUI <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/ui"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> okxTonConnectUI <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXTonConnectUI</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    dappMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        name<span class="token operator">:</span> <span class="token string">"application name"</span><span class="token punctuation">,</span>
        icon<span class="token operator">:</span> <span class="token string">"application icon url"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    buttonRootId<span class="token operator">:</span> <span class="token string">'button-root'</span><span class="token punctuation">,</span>
    actionsConfiguration<span class="token operator">:</span><span class="token punctuation">{</span>
        returnStrategy<span class="token operator">:</span><span class="token string">'none'</span><span class="token punctuation">,</span>
        tmaReturnUrl<span class="token operator">:</span><span class="token string">'back'</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
        theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">LIGHT</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    language<span class="token operator">:</span> <span class="token string">'en_US'</span><span class="token punctuation">,</span>
    restoreConnection<span class="token operator">:</span> <span class="token boolean">true</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="监听钱包状态变化" id="监听钱包状态变化">监听钱包状态变化<a class="index_header-anchor__Xqb+L" href="#监听钱包状态变化" style="opacity:0">#</a></h2>
<p>钱包状态有：连接成功、恢复连接成功、断开连接等，都可以用此方法获取状态。
<a href="/zh-hans/build/docs/sdks/app-connect-ton-sdk#%E7%9B%91%E5%90%AC%E9%92%B1%E5%8C%85%E7%8A%B6%E6%80%81%E5%8F%98%E5%8C%96">方法详情同OKXTonConnect.onStatusChange</a></p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> Wallet <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/tonsdk"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> unsubscribe <span class="token operator">=</span> okxTonConnectUI<span class="token punctuation">.</span><span class="token function">onStatusChange</span><span class="token punctuation">(</span><span class="token punctuation">(</span>walletInfo<span class="token operator">:</span> Wallet <span class="token operator">|</span> <span class="token keyword">null</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Connection status:'</span><span class="token punctuation">,</span> walletInfo<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>err<span class="token operator">:</span> OKXConnectError<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Connection status:'</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">)</span>
</code></pre></div>
<p>当不再需要监听更新时，调用unsubscribe节省资源。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token function">unsubscribe</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数，
“连接按钮”（添加于buttonRootId）会自动处理点击并调用连接，
如果没有添加buttonRootId 的话，需要调用此方法。</p>
<p><code>await okxTonConnectUI.openModal();</code></p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxTonConnectUI<span class="token punctuation">.</span><span class="token function">openModal</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="设置tonProof" id="设置tonproof">设置tonProof<a class="index_header-anchor__Xqb+L" href="#设置tonproof" style="opacity:0">#</a></h2>
<p>添加连接签名参数,
如果需要设置tonProof，请在准备好tonProof 参数之前，设置state:'loading',
在准备好之后，将state设置为 'ready'并添加value;
也可以通过设置setConnectRequestParameters(null) 移除掉loading 状态</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxtonConnectUI<span class="token punctuation">.</span><span class="token function">setConnectRequestParameters</span><span class="token punctuation">(</span><span class="token punctuation">{</span> state<span class="token operator">:</span> <span class="token string">'loading'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> tonProofPayload<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token keyword">null</span> <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">fetchTonProofPayloadFromBackend</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>tonProofPayload<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  okxtonConnectUI<span class="token punctuation">.</span><span class="token function">setConnectRequestParameters</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
  okxtonConnectUI<span class="token punctuation">.</span><span class="token function">setConnectRequestParameters</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    state<span class="token operator">:</span> <span class="token string">"ready"</span><span class="token punctuation">,</span>
    value<span class="token operator">:</span> <span class="token punctuation">{</span> tonProof<span class="token operator">:</span> tonProofPayload <span class="token punctuation">}</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="关闭连接弹窗" id="关闭连接弹窗">关闭连接弹窗<a class="index_header-anchor__Xqb+L" href="#关闭连接弹窗" style="opacity:0">#</a></h2>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxTonConnectUI<span class="token punctuation">.</span><span class="token function">closeModal</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取当前连接的Wallet和WalletInfo" id="获取当前连接的wallet和walletinfo">获取当前连接的Wallet和WalletInfo<a class="index_header-anchor__Xqb+L" href="#获取当前连接的wallet和walletinfo" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包，以及已连接的钱包的相关信息</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> currentWallet  <span class="token operator">=</span> okxTonConnectUI<span class="token punctuation">.</span>wallet<span class="token punctuation">;</span>
<span class="token keyword">const</span> currentAccount <span class="token operator">=</span> okxTonConnectUI<span class="token punctuation">.</span>account<span class="token punctuation">;</span>
<span class="token keyword">const</span> isConnected    <span class="token operator">=</span> okxTonConnectUI<span class="token punctuation">.</span>connected<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxTonConnectUI<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="发送交易" id="发送交易">发送交易<a class="index_header-anchor__Xqb+L" href="#发送交易" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法：</p>
<p><code>sendTransaction(transaction, actionConfigurationRequest): Promise&lt;SendTransactionResponse&gt;</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>
<p>transaction - object, <a href="/zh-hans/build/dev-docs/web3/build/docs/sdks/app-connect-ton-sdk#%E5%8F%91%E9%80%81%E4%BA%A4%E6%98%93">参数同OKXTonConnect.sendTransaction的transaction</a></p>
</li>
<li>
<p>actionConfigurationRequest - object</p>
<ul>
<li>modals : ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，默认为'before'</li>
<li>returnStrategy -string 'none' | <code>${string}://${string}</code>; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取init方法传递的 returnStrategy，默认为 ‘none’</li>
<li>tmaReturnUrl -string 'back' | 'none' | <code>${string}://${string}</code>; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出dapp；none 表示签名后不做处理；默认为back；</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - <code>{boc: string}</code>: 签名结果</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXConnectError<span class="token punctuation">,</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span> <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/core"</span><span class="token punctuation">;</span>

<span class="token keyword">let</span> transactionRequest <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"validUntil"</span><span class="token operator">:</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token number">1000</span> <span class="token operator">+</span> <span class="token number">360</span><span class="token punctuation">,</span>
    <span class="token string-property property">"from"</span><span class="token operator">:</span> <span class="token string">"0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"messages"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"20000000"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"stateInit"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">//deploy contract</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span>
            <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"60000000"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"payload"</span><span class="token operator">:</span> <span class="token string">"base64bocblahblahblah=="</span> <span class="token comment">//transfer nft to new deployed account 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

okxTonConnectUI<span class="token punctuation">.</span><span class="token function">sendTransaction</span><span class="token punctuation">(</span>transactionRequest<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    modals<span class="token operator">:</span> <span class="token string">'all'</span><span class="token punctuation">,</span>
    tmaReturnUrl<span class="token operator">:</span> <span class="token string">'back'</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span>result<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">let</span> boc <span class="token operator">=</span> result<span class="token punctuation">.</span>boc
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">OKXConnectError</span> <span class="token operator">&amp;&amp;</span> error<span class="token punctuation">.</span>code <span class="token operator">==</span> <span class="token constant">OKX_CONNECT_ERROR_CODES</span><span class="token punctuation">.</span><span class="token constant">USER_REJECTS_ERROR</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token comment">//userReject;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        <span class="token comment">//other error;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>

</code></pre></div>
<h2 data-content="设置ui配置项" id="设置ui配置项">设置ui配置项<a class="index_header-anchor__Xqb+L" href="#设置ui配置项" style="opacity:0">#</a></h2>
<p>支持修改主题，文字语言设置，也可以在初始化的时候添加这些配置</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxTonConnectUI<span class="token punctuation">.</span>uiOptions <span class="token operator">=</span> <span class="token punctuation">{</span>
  language<span class="token operator">:</span> <span class="token string">'zh_CN'</span><span class="token punctuation">,</span>
  uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
    theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">DARK</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="监听事件" id="监听事件">监听事件<a class="index_header-anchor__Xqb+L" href="#监听事件" style="opacity:0">#</a></h2>
<p>在以下事件发生时，会发送对应事件通知，Dapp可以根据需要添加监听，来处理对应的逻辑</p>
<p><strong>event事件</strong></p>
<div class="index_table__kvZz5"><table><thead><tr><th>事件名称</th><th>触发时机</th></tr></thead><tbody><tr><td>OKX_UI_CONNECTION_STARTED</td><td>当用户开始连接钱包时</td></tr><tr><td>OKX_UI_CONNECTION_COMPLETED</td><td>当用户成功连接钱包时</td></tr><tr><td>OKX_UI_CONNECTION_ERROR</td><td>当用户取消连接或连接过程中出现错误时</td></tr><tr><td>OKX_UI_CONNECTION_RESTORING_STARTED</td><td>当 dApp 开始恢复连接时</td></tr><tr><td>OKX_UI_CONNECTION_RESTORING_COMPLETED</td><td>当 dApp 成功恢复连接时</td></tr><tr><td>OKX_UI_CONNECTION_RESTORING_ERROR</td><td>当 dApp 无法恢复连接时</td></tr><tr><td>OKX_UI_DISCONNECTION</td><td>当用户开始断开钱包连接时</td></tr><tr><td>OKX_UI_TRANSACTION_SENT_FOR_SIGNATURE</td><td>当用户发送交易以供签名时</td></tr><tr><td>OKX_UI_TRANSACTION_SIGNED</td><td>当用户成功签署交易时</td></tr><tr><td>OKX_UI_TRANSACTION_SIGNING_FAILED</td><td>当用户取消交易签名或签名过程中出现错误时</td></tr></tbody></table></div>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> <span class="token constant">OKX_UI_CONNECTION_AND_TRANSACTION_EVENT</span> <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/ui"</span><span class="token punctuation">;</span>

window<span class="token punctuation">.</span><span class="token function">addEventListener</span><span class="token punctuation">(</span><span class="token constant">OKX_UI_CONNECTION_AND_TRANSACTION_EVENT</span><span class="token punctuation">.</span><span class="token constant">OKX_UI_CONNECTION_STARTED</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>event<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>event <span class="token keyword">instanceof</span> <span class="token class-name">CustomEvent</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Transaction init'</span><span class="token punctuation">,</span> event<span class="token punctuation">.</span>detail<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
<p>在连接，交易，断开连接的过程中可能抛出的异常</p>
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
    "UI"
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
    "通过npm安装",
    "初始化",
    "监听钱包状态变化",
    "连接钱包",
    "设置tonProof",
    "关闭连接弹窗",
    "获取当前连接的Wallet和WalletInfo",
    "断开钱包连接",
    "发送交易",
    "设置ui配置项",
    "监听事件",
    "Event事件",
    "错误码"
  ]
}
```

</details>
