# UI | EVM兼容链 | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-evm-ui#获取当前连接的会话信息  
**抓取时间:** 2025-05-27 07:13:59  
**字数:** 1046

## 导航路径
DApp 连接钱包 > EVM兼容链 > UI

## 目录
- 通过npm安装
- 初始化
- 连接钱包
- 连接钱包并签名
- 判断钱包是否已连接
- 准备交易
- 使用RPC
- 关闭连接弹窗
- 监听连接弹窗状态变化
- 获取当前连接的会话信息
- 设置ui配置项
- 设置默认网络
- 断开钱包连接
- Event事件
- 错误码

---

UI
#
在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运行在 Telegram内，则用户可以选择唤起欧易 App 钱包或者停留在Telegram并唤起欧易 Telegram Mini 钱包。
通过npm安装
#
npm install @okxconnect/ui
初始化
#
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。
OKXUniversalConnectUI.init(DAppMetaData, actionsConfiguration, uiPreferences, language, restoreConnection)
请求参数
DAppMetaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。
actionsConfiguration - object
modals - ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，默认为'before'
returnStrategy -string 'none' |
${string}://${string}
; 针对app 钱包，指定当用户签署/拒绝请求时深层链接的返回策略，如果是在telegram中，可以配置tg://resolve；
tmaReturnUrl -string 'back' | 'none' |
${string}://${string}
; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出DApp；none 表示签名后不做处理；默认为back；
uiPreferences -object
theme - Theme 可以是：THEME.DARK, THEME.LIGHT, "SYSTEM"
language - "en_US" | "ru_RU" | "zh_CN" | "ar_AE" | "cs_CZ" | "de_DE" | "es_ES" | "es_LAT" | "fr_FR" | "id_ID" | "it_IT" | "nl_NL" | "pl_PL" | "pt_BR" | "pt_PT" | "ro_RO" | "tr_TR" | "uk_UA" | "vi_VN";
, 默认为en_US
restoreConnection?: boolean - 是否自动回复之前的连接；
返回值
OKXUniversalConnectUI
示例
import
{
OKXUniversalConnectUI
}
from
"@okxconnect/ui"
;
const
universalUi
=
await
OKXUniversalConnectUI
.
init
(
{
DAppMetaData
:
{
icon
:
"https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png"
,
name
:
"OKX Connect Demo"
}
,
actionsConfiguration
:
{
returnStrategy
:
'tg://resolve'
,
modals
:
'all'
,
tmaReturnUrl
:
'back'
}
,
language
:
"en_US"
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
}
)
;
// 连接OKX插件钱包后，切换插件钱包，会触发该事件；
universalUi
.
on
(
"accountChanged"
,
(
session
)
=>
{
if
(
session
)
{
console
.
log
(
`
accountChanged
`
,
JSON
.
stringify
(
session
)
)
;
}
}
)
;
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数，
await universalUi.openModal(connectParams: ConnectParams);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；
chains: string[]; 链id信息，EIP155中定义的十进制数字，比如以太坊是eip155:1,
defaultChain?: string; 默认链
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。
chains: string[]; 链id信息,
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识；
namespaces:
Record<string, Namespace>
; 成功连接的namespace 信息；
chains: string[]; 连接的链信息；
accounts: string[]; 连接的账户信息；
methods: string[]; 当前namespace下，钱包支持的方法；
defaultChain?: string; 当前会话的默认链
sessionConfig?: SessionConfig
DAppInfo: object DApp 信息；
name:string
icon:string
示例
var
session
=
await
universalUi
.
openModal
(
{
namespaces
:
{
eip155
:
{
// 请按需组合需要的链id传入，多条链就传入多个
chains
:
[
"eip155:1"
,
"eip155:137"
]
,
defaultChain
:
"1"
,
rpcMap
:
{
"137"
:
"https://polygon.drpc.org"
}
}
}
,
optionalNamespaces
:
{
eip155
:
{
chains
:
[
"eip155:43114"
]
}
}
}
)
连接钱包并签名
#
连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调；
await universalUi.openModalAndSign(connectParams: ConnectParams,signRequest: RequestParams[]);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；
chains: string[]; 链id信息，EIP155中定义的十进制数字，比如以太坊是eip155:1,
defaultChain?: string; 默认链
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。
chains: string[]; 链id信息,
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法；
method: string; 请求的方法名称,EVM系支持的方法有："personal_sign"；
chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中；
params: unknown[] | Record
<string, unknown>
| object | undefined; 请求的方法对应的参数；
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识；
namespaces:
Record<string, Namespace>
; 成功连接的namespace 信息；
chains: string[]; 连接的链信息；
accounts: string[]; 连接的账户信息；
methods: string[]; 当前namespace下，钱包支持的方法；
defaultChain?: string; 当前会话的默认链
sessionConfig?: SessionConfig
DAppInfo: object DApp 信息；
name:string
icon:string
示例
// 先添加签名结果监听
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
var
session
=
await
universalUi
.
openModalAndSign
(
{
namespaces
:
{
eip155
:
{
// 请按需组合需要的链id传入，多条链就传入多个
chains
:
[
"eip155:1"
,
"eip155:137"
]
,
defaultChain
:
"1"
,
rpcMap
:
{
"137"
:
"https://polygon.drpc.org"
}
}
}
,
optionalNamespaces
:
{
eip155
:
{
chains
:
[
"eip155:43114"
]
}
}
,
sessionConfig
:
{
redirect
:
"tg://resolve"
}
}
,
[
{
method
:
"personal_sign"
,
chainId
:
"eip155:1"
,
params
:
[
"0x4d7920656d61696c206973206a6f686e40646f652e636f6d202d2031373237353937343537313336"
,
]
,
}
]
)
判断钱包是否已连接
#
获取当前是否有连接钱包;
返回值
boolean
示例
universalUi
.
connected
(
)
;
准备交易
#
向钱包发送消息的方法，支持签名，交易;
universalUi.request(requestArguments, chain, actionConfigurationRequest);
请求参数
requestArguments - object
method: string; 请求的方法名，
params?: unknown[] | Record
<string, unknown>
| object | undefined; 请求的方法对应的参数；
chain: string; 请求方法执行的链，建议传该参数，如果未传的话，会被设置为当前的defaultChain；
actionConfigurationRequest - object
modals : ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，如果request 没有设置该参数的，取init 时候添加的参数，如果init 没有也设置该参数，则取默认值：'before',
tmaReturnUrl -string 'back' | 'none' |
${string}://${string}
; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出DApp；none 表示签名后不做处理；默认为back；
returnStrategy -string 'none' |
${string}://${string}
; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取init方法传递的 returnStrategy，默认为 ‘none’
返回值
返回参数详情同EVM兼容链的发送签名和交易
示例
示例同EVM兼容链的发送签名和交易
let
chain
=
'eip155:1'
var
data
=
{
}
data
=
{
"method"
:
"personal_sign"
,
"params"
:
[
"0x506c65617365207369676e2074686973206d65737361676520746f20636f6e6669726d20796f7572206964656e746974792e"
,
"0x4B0897b0513FdBeEc7C469D9aF4fA6C0752aBea7"
]
}
var
personalSignResult
=
await
universalUi
.
request
(
data
,
chain
,
'all'
)
//personalSignResult: 0xe8d34297c33a61"
使用RPC
#
当EVM系的 request 中 method 无法满足需求时，可通过配置 RPC 实现更多功能，在连接钱包openModal或者openModalAndSign时,RPC配置在rpcMap中。
示例
//查询交易Hash的详细信息
let
rpcData
=
{
method
:
"eth_getTransactionByHash"
,
params
:
[
"0xd62fa4ea3cf7ee3bf6f5302b764490730186ed6a567c283517e8cb3c36142e1a"
]
,
}
;
let
result
=
await
universalUi
.
request
(
rpcData
,
"eip155:137"
)
关闭连接弹窗
#
示例
universalUi
.
closeModal
(
)
;
监听连接弹窗状态变化
#
示例
const
unsubscribe
=
universalUi
.
onModalStateChange
(
(
state
)
=>
{
}
)
不需要监听的时候移除监听
unsubscribe
(
)
获取当前连接的会话信息
#
获取当前是否有连接钱包，以及已连接的钱包的相关信息；
示例
universalUi
.
session
;
设置ui配置项
#
支持修改主题，文字语言设置，也可以在初始化的时候添加这些配置；
示例
universalUi
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
设置默认网络
#
在连接多个网络的状况下,如果开发者没有明确指定当前操作所在网络,则通过默认网络进行交互。
'setDefaultChain(chain)'
示例
universalUi
.
setDefaultChain
(
"eip155:1"
)
断开钱包连接
#
示例
universalUi
.
disconnect
(
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
// session 信息变更（例如添加自定义链）会触发该事件；
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
// 连接OKX插件钱包后，切换插件钱包，会触发该事件；
universalUi
.
on
(
"accountChanged"
,
(
session
)
=>
{
if
(
session
)
{
console
.
log
(
`
accountChanged
`
,
JSON
.
stringify
(
session
)
)
;
}
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
<p>在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运行在 Telegram内，则用户可以选择唤起欧易 App 钱包或者停留在Telegram并唤起欧易 Telegram Mini 钱包。</p>
<h2 data-content="通过npm安装" id="通过npm安装">通过npm安装<a class="index_header-anchor__Xqb+L" href="#通过npm安装" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/ui</code></pre></div>
<h2 data-content="初始化" id="初始化">初始化<a class="index_header-anchor__Xqb+L" href="#初始化" style="opacity:0">#</a></h2>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">OKXUniversalConnectUI.init(DAppMetaData, actionsConfiguration, uiPreferences, language, restoreConnection)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>DAppMetaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。</li>
</ul>
</li>
<li>actionsConfiguration - object<!-- -->
<ul>
<li>modals - ('before' | 'success' | 'error')[] | 'all'  交易过程中的提醒界面展示模式，默认为'before'</li>
<li>returnStrategy -string 'none' | <code>${string}://${string}</code>; 针对app 钱包，指定当用户签署/拒绝请求时深层链接的返回策略，如果是在telegram中，可以配置tg://resolve；</li>
<li>tmaReturnUrl -string 'back' | 'none' | <code>${string}://${string}</code>; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出DApp；none 表示签名后不做处理；默认为back；</li>
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
<li>OKXUniversalConnectUI</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXUniversalConnectUI <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/ui"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> universalUi <span class="token operator">=</span> <span class="token keyword">await</span> OKXUniversalConnectUI<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  DAppMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
    icon<span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png"</span><span class="token punctuation">,</span>
    name<span class="token operator">:</span> <span class="token string">"OKX Connect Demo"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  actionsConfiguration<span class="token operator">:</span> <span class="token punctuation">{</span>
    returnStrategy<span class="token operator">:</span> <span class="token string">'tg://resolve'</span><span class="token punctuation">,</span>
    modals<span class="token operator">:</span><span class="token string">'all'</span><span class="token punctuation">,</span>
    tmaReturnUrl<span class="token operator">:</span><span class="token string">'back'</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  language<span class="token operator">:</span> <span class="token string">"en_US"</span><span class="token punctuation">,</span>
  uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
    theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">LIGHT</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 连接OKX插件钱包后，切换插件钱包，会触发该事件；</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"accountChanged"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">accountChanged </span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数，</p>
<p><code>await universalUi.openModal(connectParams: ConnectParams);</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息，EIP155中定义的十进制数字，比如以太坊是eip155:1,</li>
<li>defaultChain?: string; 默认链</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。<!-- -->
<ul>
<li>chains: string[]; 链id信息,</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise<code>&lt;SessionTypes.Struct | undefined&gt;</code>
<ul>
<li>topic: string; 会话标识；</li>
<li>namespaces: <code>Record&lt;string, Namespace&gt;</code>; 成功连接的namespace 信息；<!-- -->
<ul>
<li>chains: string[]; 连接的链信息；</li>
<li>accounts: string[]; 连接的账户信息；</li>
<li>methods: string[]; 当前namespace下，钱包支持的方法；</li>
<li>defaultChain?: string; 当前会话的默认链</li>
</ul>
</li>
<li>sessionConfig?: SessionConfig<!-- -->
<ul>
<li>DAppInfo: object DApp 信息；<!-- -->
<ul>
<li>name:string</li>
<li>icon:string</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">openModal</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
    eip155<span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token comment">// 请按需组合需要的链id传入，多条链就传入多个</span>
      chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"eip155:1"</span><span class="token punctuation">,</span><span class="token string">"eip155:137"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      defaultChain<span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
      rpcMap<span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"137"</span><span class="token operator">:</span><span class="token string">"https://polygon.drpc.org"</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  optionalNamespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
    eip155<span class="token operator">:</span> <span class="token punctuation">{</span>
      chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"eip155:43114"</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包并签名" id="连接钱包并签名">连接钱包并签名<a class="index_header-anchor__Xqb+L" href="#连接钱包并签名" style="opacity:0">#</a></h2>
<p>连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调；</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">await universalUi.openModalAndSign(connectParams: ConnectParams,signRequest: RequestParams[]);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息，EIP155中定义的十进制数字，比如以太坊是eip155:1,</li>
<li>defaultChain?: string; 默认链</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。<!-- -->
<ul>
<li>chains: string[]; 链id信息,</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
</ul>
</li>
</ul>
</li>
<li>signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法；<!-- -->
<ul>
<li>method: string;  请求的方法名称,EVM系支持的方法有："personal_sign"；</li>
<li>chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中；</li>
<li>params: unknown[] | Record<code>&lt;string, unknown&gt;</code> | object | undefined; 请求的方法对应的参数；</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise<code>&lt;SessionTypes.Struct | undefined&gt;</code>
<ul>
<li>topic: string; 会话标识；</li>
<li>namespaces: <code>Record&lt;string, Namespace&gt;</code>; 成功连接的namespace 信息；<!-- -->
<ul>
<li>chains: string[]; 连接的链信息；</li>
<li>accounts: string[]; 连接的账户信息；</li>
<li>methods: string[]; 当前namespace下，钱包支持的方法；</li>
<li>defaultChain?: string; 当前会话的默认链</li>
</ul>
</li>
<li>sessionConfig?: SessionConfig<!-- -->
<ul>
<li>DAppInfo: object DApp 信息；<!-- -->
<ul>
<li>name:string</li>
<li>icon:string
<strong>示例</strong></li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 先添加签名结果监听</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect_signResponse"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">openModalAndSign</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
    eip155<span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token comment">// 请按需组合需要的链id传入，多条链就传入多个</span>
      chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"eip155:1"</span><span class="token punctuation">,</span><span class="token string">"eip155:137"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      defaultChain<span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
      rpcMap<span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"137"</span><span class="token operator">:</span><span class="token string">"https://polygon.drpc.org"</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  optionalNamespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
    eip155<span class="token operator">:</span> <span class="token punctuation">{</span>
      chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"eip155:43114"</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
    redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span><span class="token punctuation">[</span><span class="token punctuation">{</span>
  method<span class="token operator">:</span> <span class="token string">"personal_sign"</span><span class="token punctuation">,</span>
  chainId<span class="token operator">:</span> <span class="token string">"eip155:1"</span><span class="token punctuation">,</span>
  params<span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token string">"0x4d7920656d61696c206973206a6f686e40646f652e636f6d202d2031373237353937343537313336"</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="判断钱包是否已连接" id="判断钱包是否已连接">判断钱包是否已连接<a class="index_header-anchor__Xqb+L" href="#判断钱包是否已连接" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包;</p>
<p><strong>返回值</strong></p>
<ul>
<li>boolean</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">connected</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法，支持签名，交易;</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">universalUi.request(requestArguments, chain, actionConfigurationRequest);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>requestArguments - object<!-- -->
<ul>
<li>method: string; 请求的方法名，</li>
<li>params?: unknown[]  | Record<code>&lt;string, unknown&gt;</code> | object | undefined; 请求的方法对应的参数；</li>
</ul>
</li>
<li>chain: string; 请求方法执行的链，建议传该参数，如果未传的话，会被设置为当前的defaultChain；</li>
<li>actionConfigurationRequest - object<!-- -->
<ul>
<li>modals : ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，如果request 没有设置该参数的，取init 时候添加的参数，如果init 没有也设置该参数，则取默认值：'before',</li>
<li>tmaReturnUrl -string 'back' | 'none' | <code>${string}://${string}</code>; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出DApp；none 表示签名后不做处理；默认为back；</li>
<li>returnStrategy -string 'none' | <code>${string}://${string}</code>; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取init方法传递的 returnStrategy，默认为 ‘none’</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<p><a href="/zh-hans/build/docs/sdks/app-connect-evm-sdk#%E5%8F%91%E9%80%81%E7%AD%BE%E5%90%8D%E5%92%8C%E4%BA%A4%E6%98%93">返回参数详情同EVM兼容链的发送签名和交易</a></p>
<p><strong>示例</strong></p>
<p><a href="/zh-hans/build/docs/sdks/app-connect-evm-sdk#%E5%8F%91%E9%80%81%E7%AD%BE%E5%90%8D%E5%92%8C%E4%BA%A4%E6%98%93">示例同EVM兼容链的发送签名和交易</a></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">'eip155:1'</span>
<span class="token keyword">var</span> data <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>

data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"personal_sign"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"0x506c65617365207369676e2074686973206d65737361676520746f20636f6e6669726d20796f7572206964656e746974792e"</span><span class="token punctuation">,</span>
        <span class="token string">"0x4B0897b0513FdBeEc7C469D9aF4fA6C0752aBea7"</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> personalSignResult <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">,</span><span class="token string">'all'</span><span class="token punctuation">)</span>
<span class="token comment">//personalSignResult:   0xe8d34297c33a61"</span>

</code></pre></div>
<h2 data-content="使用RPC" id="使用rpc">使用RPC<a class="index_header-anchor__Xqb+L" href="#使用rpc" style="opacity:0">#</a></h2>
<p>当EVM系的 request 中 method 无法满足需求时，可通过配置 RPC 实现更多功能，在连接钱包openModal或者openModalAndSign时,RPC配置在rpcMap中。</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">//查询交易Hash的详细信息</span>
<span class="token keyword">let</span> rpcData <span class="token operator">=</span> <span class="token punctuation">{</span>
  method<span class="token operator">:</span> <span class="token string">"eth_getTransactionByHash"</span><span class="token punctuation">,</span>
  params<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"0xd62fa4ea3cf7ee3bf6f5302b764490730186ed6a567c283517e8cb3c36142e1a"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>rpcData<span class="token punctuation">,</span><span class="token string">"eip155:137"</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="关闭连接弹窗" id="关闭连接弹窗">关闭连接弹窗<a class="index_header-anchor__Xqb+L" href="#关闭连接弹窗" style="opacity:0">#</a></h2>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">closeModal</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="监听连接弹窗状态变化" id="监听连接弹窗状态变化">监听连接弹窗状态变化<a class="index_header-anchor__Xqb+L" href="#监听连接弹窗状态变化" style="opacity:0">#</a></h2>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> unsubscribe <span class="token operator">=</span> universalUi<span class="token punctuation">.</span><span class="token function">onModalStateChange</span><span class="token punctuation">(</span><span class="token punctuation">(</span>state<span class="token punctuation">)</span><span class="token operator">=&gt;</span><span class="token punctuation">{</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<p>不需要监听的时候移除监听</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token function">unsubscribe</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取当前连接的会话信息" id="获取当前连接的会话信息">获取当前连接的会话信息<a class="index_header-anchor__Xqb+L" href="#获取当前连接的会话信息" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包，以及已连接的钱包的相关信息；</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span>session<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="设置ui配置项" id="设置ui配置项">设置ui配置项<a class="index_header-anchor__Xqb+L" href="#设置ui配置项" style="opacity:0">#</a></h2>
<p>支持修改主题，文字语言设置，也可以在初始化的时候添加这些配置；</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span>uiOptions <span class="token operator">=</span> <span class="token punctuation">{</span>
  language<span class="token operator">:</span> <span class="token string">'zh_CN'</span><span class="token punctuation">,</span>
  uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
    theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">DARK</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="设置默认网络" id="设置默认网络">设置默认网络<a class="index_header-anchor__Xqb+L" href="#设置默认网络" style="opacity:0">#</a></h2>
<p>在连接多个网络的状况下,如果开发者没有明确指定当前操作所在网络,则通过默认网络进行交互。</p>
<p>'setDefaultChain(chain)'</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">setDefaultChain</span><span class="token punctuation">(</span><span class="token string">"eip155:1"</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 生成 universalLink</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"display_uri"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>uri<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>uri<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// session 信息变更（例如添加自定义链）会触发该事件；</span>
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

<span class="token comment">// 连接OKX插件钱包后，切换插件钱包，会触发该事件；</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"accountChanged"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">accountChanged </span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
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
    "EVM兼容链",
    "UI"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "SDK",
    "UI",
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
    "Solana 兼容链"
  ],
  "toc": [
    "通过npm安装",
    "初始化",
    "连接钱包",
    "连接钱包并签名",
    "判断钱包是否已连接",
    "准备交易",
    "使用RPC",
    "关闭连接弹窗",
    "监听连接弹窗状态变化",
    "获取当前连接的会话信息",
    "设置ui配置项",
    "设置默认网络",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
