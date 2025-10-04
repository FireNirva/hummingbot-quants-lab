# UI | Bitcoin兼容链 | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-bitcoin-ui#signpsbt  
**抓取时间:** 2025-05-27 07:35:09  
**字数:** 1139

## 导航路径
DApp 连接钱包 > Bitcoin兼容链 > UI

## 目录
- 安装及初始化
- 连接钱包
- 连接钱包并签名
- 判断钱包是否已连接
- 准备交易
- 获取钱包账户信息
- 签名
- 发送Bitcoin
- signPsbt
- signPsbts
- 签名且广播 signAndPushPsbt
- 断开钱包连接
- Event事件
- 错误码

---

UI
#
安装及初始化
#
请确保更新OKX App到 6.92.0版本或以后版本，即可开始接入：
将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/ui
npm install @okxconnect/universal-provider
连接钱包之前，需要先创建一个可以提供UI界面的对象，用于后续连接钱包、发送交易等操作。
OKXUniversalConnectUI.init(dappMetaData, actionsConfiguration, uiPreferences, language)
请求参数
dappMetaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url
actionsConfiguration - object
modals - ('before' | 'success' | 'error')[] | 'all' 交易过程中的提醒界面展示模式，默认为'before'
returnStrategy -string 'none' |
${string}://${string}
; 针对app 钱包，指定当用户签署/拒绝请求时深层链接的返回策略，如果是在telegram中，可以配置tg://resolve
tmaReturnUrl -string 'back' | 'none' |
${string}://${string}
; Telegram Mini Wallet 钱包中，用户签署/拒绝请求时深层链接的返回策略，一般配置back,表示签名后关闭钱包，会自动展示出dapp；none 表示签名后不做处理；默认为back；
uiPreferences -object
theme - Theme 可以是：THEME.DARK, THEME.LIGHT, "SYSTEM"
language - "en_US" | "ru_RU" | "zh_CN" | "ar_AE" | "cs_CZ" | "de_DE" | "es_ES" | "es_LAT" | "fr_FR" | "id_ID" | "it_IT" | "nl_NL" | "pl_PL" | "pt_BR" | "pt_PT" | "ro_RO" | "tr_TR" | "uk_UA" | "vi_VN";
, 默认为en_US
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
okxUniversalConnectUI
=
await
OKXUniversalConnectUI
.
init
(
{
dappMetaData
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
"all"
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
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数
okxUniversalConnectUI.connect(connectParams: ConnectParams)
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， EVM系的key为"eip155"，BTC系的key为"btc"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，BTC系的key为"btc"，如果对应的链信息钱包不支持，依然可以连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
sessionConfig: object
redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识；
namespaces:
Record<string, Namespace>
; 成功连接的namespace 信息
chains: string[]; 连接的链信息
accounts: string[]; 连接的账户信息
methods: string[]; 当前namespace下，钱包支持的方法
defaultChain?: string; 当前会话的默认链
sessionConfig?: SessionConfig
dappInfo: object DApp 信息
name:string
icon:string
redirect?:string, 连接成功后的跳转参数
示例
var
session
=
await
okxUniversalConnectUI
.
connect
(
{
namespaces
:
{
btc
:
{
chains
:
[
"btc:mainnet"
,
// "fractal:mainnet"
]
,
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
)
连接钱包并签名
#
连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调
await okxUniversalConnectUI.openModalAndSign(connectParams: ConnectParams, signRequest: RequestParams[])
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息，BTC系的key为"btc"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，BTC系的key为"btc"，如果对应的链信息钱包不支持，依然可以连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
sessionConfig: object
redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"
signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法
method: string; 请求的方法名称, BTC系支持的方法有："btc_signMessage"
chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中
params: unknown[] | Record
<string, unknown>
| object | undefined; 请求的方法对应的参数
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识；
namespaces:
Record<string, Namespace>
; 成功连接的namespace 信息
chains: string[]; 连接的链信息
accounts: string[]; 连接的账户信息
methods: string[]; 当前namespace下，钱包支持的方法
defaultChain?: string; 当前会话的默认链
sessionConfig?: SessionConfig
dappInfo: object DApp 信息
name:string
icon:string
示例
// 先添加签名结果监听
okxUniversalConnectUI
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
okxUniversalConnectUI
.
openModalAndSign
(
{
namespaces
:
{
btc
:
{
chains
:
[
"btc:mainnet"
,
// "fractal:mainnet"
]
,
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
"btc_signMessage"
,
chainId
:
"btc:mainnet"
,
params
:
{
message
:
"Welcome to BTC"
}
}
]
)
判断钱包是否已连接
#
获取当前是否有连接钱包
返回值
boolean
示例
universalUi
.
connected
(
)
准备交易
#
首先创建一个OKXBtcProvider对象，构造函数传入okxUniversalConnectUI
import
{
OKXBtcProvider
}
from
"@okxconnect/universal-provider"
;
let
okxBtcProvider
=
new
OKXBtcProvider
(
okxUniversalConnectUI
)
获取钱包账户信息
#
okxBtcProvider.getAccount(chainId)
请求参数
chainId: 请求的链，如btc:mainnet, fractal:mainnet
返回值
Object
address: string 钱包地址
publicKey: string 公钥
示例
let
result
=
okxBtcProvider
.
getAccount
(
"btc:mainnet"
)
//返回结构
{
"address"
:
"038936b367d47b3796b430a31694320918afdc458d81dea9bb7dd35c0aad8bc694"
,
"publicKey"
:
"03cbaedc26f03fd3ba02fc936f338e980c9e2172c5e23128877ed46827e935296f"
}
签名
#
okxBtcProvider.signMessage(chain, message, type?)
请求参数
chain - string, 请求执行方法的链
signStr - string 需要签名的消息
type - (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"
返回值
Promise - string: 签名结果
示例
let
chain
=
"btc:mainnet"
let
signStr
=
"data need to sign ..."
let
result
=
okxBtcProvider
.
signMessage
(
chain
,
signStr
)
//返回结构: "H83jZpulbMDDGUiTA4M8QNChmWwaKxwPCm8U5EBvftKlSMMzuvtVxBHlygtof5NBbdSVPiAtCvOUwZmz2vViHHU="
发送Bitcoin
#
okxBtcProvider.sendBitcoin(chainId, toAddress, satoshis, options)
请求参数
chainId - string, 请求签名执行的链，必传参数，如btc:mainnet
toAddress - string, string, 接收的地址
satoshis - number, 发送的聪数量
options - Object (可选)
feeRate - number (可选) 自定义费率
返回值
Promise - string 交易哈希
示例
let
chain
=
"btc:mainnet"
let
toAddress
=
'1NKnZ3uAuQLnmE...4u1efwCgTiAxBn'
let
satoshis
=
17000
let
options
=
{
feeRate
:
16
}
let
result
=
okxBtcProvider
.
sendBitcoin
(
chain
,
toAddress
,
satoshis
,
options
)
/**
返回结构:
"ff18d01ef6abed3b7fd23247a1fc457ca...f49b6bb4529a19a5fb637f18ce2e"
*/
signPsbt
#
okxBtcProvider.signPsbt(chainId, psbtHex, options)
请求参数
chain - string, 请求签名执行的链，必传参数，如btc:mainnet
psbtHex - string, 要签名的 psbt 的十六进制字符串
options:
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名
返回值
Promise - string 已签名psbt的十六进制字符串
示例
let
chain
=
"btc:mainnet"
let
psbtHex
=
""
let
options
=
{
autoFinalized
:
false
}
let
result
=
okxBtcProvider
.
signPsbt
(
chain
,
psbtHex
,
options
)
/**
返回结构:
"cHNidP8BAP0GAQIAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA/////yjWH1Uvx225V01diYYZ2i5jVAORF4nLWUWCg5bBaLQwAAAAAAD/////AwEAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AIb9jA0AAAAiUSDwUTBk/h5bXDG+3/Q7lD8vEhHRSrKJFockGxONIUiI4wAAAAAAAQErAQAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQETQD9magM5RHYbdRd4KZ70FfVEAW5hw3rLjrocWIyn2Gi2P2c6Gri0E/S/wREhgjM8u5zQ3GrpcSaC8KhCRxBq5/oBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABASsBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1ARNA83DNEJj5u/mgUoOhCWL07enXpb6RX/WfEBh97tyrXLlA/e0CowU1fpgrKn+PQ+9Z/5/EXGwcr1UkYaqBJ0ZpKQEXIA1UE650qVNSIp6+ZnMap1Vynpjxdsw5N89XTd8TIs4WAAEBK+gDAAAAAAAAIlEg8FEwZP4eW1wxvt/0O5Q/LxIR0UqyiRaHJBsTjSFIiOMBAwSDAAAAARNBZcHpcb6YDNWF+eIcFckjF1c8C83uRmEhS/8jJQOBFkIQol8hBCTYXOFAaeu6/4o2MsS20iITiM/rAOAOBZkXC4MBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSCJNrNn1Hs3lrQwoxaUMgkYr9xFjYHeqbt901wKrYvGlAA="
*/
signPsbts
#
okxBtcProvider.signPsbts(chainId, psbtHexs, options)
请求参数
chainId - string, 请求签名执行的链，必传参数，如btc:mainnet
psbtHex - string[], 要签名的 psbt 的十六进制字符串
options - object[]
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名
返回值
Promise - string[] 已签名 psbt 的十六进制字符串
示例
let
chain
=
"btc:mainnet"
let
psbtHexs
=
[
""
]
let
options
=
[
{
autoFinalized
:
false
}
]
let
result
=
okxBtcProvider
.
signPsbts
(
chain
,
psbtHexs
,
options
)
/**
返回结构:
["cHNidP8BAP0GAQIAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA/////yjWH1Uvx225V01diYYZ2i5jVAORF4nLWUWCg5bBaLQwAAAAAAD/////AwEAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AIb9jA0AAAAiUSDwUTBk/h5bXDG+3/Q7lD8vEhHRSrKJFockGxONIUiI4wAAAAAAAQErAQAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQETQD9magM5RHYbdRd4KZ70FfVEAW5hw3rLjrocWIyn2Gi2P2c6Gri0E/S/wREhgjM8u5zQ3GrpcSaC8KhCRxBq5/oBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABASsBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1ARNA83DNEJj5u/mgUoOhCWL07enXpb6RX/WfEBh97tyrXLlA/e0CowU1fpgrKn+PQ+9Z/5/EXGwcr1UkYaqBJ0ZpKQEXIA1UE650qVNSIp6+ZnMap1Vynpjxdsw5N89XTd8TIs4WAAEBK+gDAAAAAAAAIlEg8FEwZP4eW1wxvt/0O5Q/LxIR0UqyiRaHJBsTjSFIiOMBAwSDAAAAARNBZcHpcb6YDNWF+eIcFckjF1c8C83uRmEhS/8jJQOBFkIQol8hBCTYXOFAaeu6/4o2MsS20iITiM/rAOAOBZkXC4MBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSCJNrNn1Hs3lrQwoxaUMgkYr9xFjYHeqbt901wKrYvGlAA="]
*/
签名且广播 signAndPushPsbt
#
App required: >= 6.93.0
okxBtcProvider.signAndPushPsbt(chainId, psbtHex, options)
请求参数
chain - string, 请求签名执行的链，必传参数，如btc:mainnet
psbtHex - string, 要签名的 psbt 的十六进制字符串
options: - object
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名
返回值
Promise - object
txhash 交易hash
signature 已签名 psbt 的十六进制字符串
示例
let
chain
=
"btc:mainnet"
let
psbtHex
=
""
let
options
=
{
autoFinalized
:
false
}
let
result
=
okxBtcProvider
.
signAndPushPsbt
(
chain
,
psbtHex
,
options
)
/**
 返回结构:
{
txhash: "",
 signature: ""
}
*/
断开钱包连接
#
断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包
okxUniversalConnectUI
.
disconnect
(
)
Event事件
#
// 生成 universalLink
okxUniversalConnectUI
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
okxUniversalConnectUI
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
okxUniversalConnectUI
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
okxUniversalConnectUI
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
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新OKX App到 6.92.0版本或以后版本，即可开始接入：</p>
<p>将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/ui
npm install @okxconnect/universal-provider</code></pre></div>
<p>连接钱包之前，需要先创建一个可以提供UI界面的对象，用于后续连接钱包、发送交易等操作。</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">OKXUniversalConnectUI.init(dappMetaData, actionsConfiguration, uiPreferences, language)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>dappMetaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url</li>
</ul>
</li>
<li>actionsConfiguration - object<!-- -->
<ul>
<li>modals - ('before' | 'success' | 'error')[] | 'all'  交易过程中的提醒界面展示模式，默认为'before'</li>
<li>returnStrategy -string 'none' | <code>${string}://${string}</code>; 针对app 钱包，指定当用户签署/拒绝请求时深层链接的返回策略，如果是在telegram中，可以配置tg://resolve</li>
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
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>OKXUniversalConnectUI</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXUniversalConnectUI <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/ui"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> okxUniversalConnectUI <span class="token operator">=</span> <span class="token keyword">await</span> OKXUniversalConnectUI<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    dappMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        icon<span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png"</span><span class="token punctuation">,</span>
        name<span class="token operator">:</span> <span class="token string">"OKX Connect Demo"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    actionsConfiguration<span class="token operator">:</span> <span class="token punctuation">{</span>
        returnStrategy<span class="token operator">:</span> <span class="token string">'tg://resolve'</span><span class="token punctuation">,</span>
        modals<span class="token operator">:</span><span class="token string">"all"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    language<span class="token operator">:</span> <span class="token string">"en_US"</span><span class="token punctuation">,</span>
    uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
        theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">LIGHT</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalConnectUI.connect(connectParams: ConnectParams)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， EVM系的key为"eip155"，BTC系的key为"btc"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，BTC系的key为"btc"，如果对应的链信息钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>sessionConfig: object<!-- -->
<ul>
<li>redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"</li>
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
<li>namespaces: <code>Record&lt;string, Namespace&gt;</code>; 成功连接的namespace 信息<!-- -->
<ul>
<li>chains: string[]; 连接的链信息</li>
<li>accounts: string[]; 连接的账户信息</li>
<li>methods: string[]; 当前namespace下，钱包支持的方法</li>
<li>defaultChain?: string; 当前会话的默认链</li>
</ul>
</li>
<li>sessionConfig?: SessionConfig<!-- -->
<ul>
<li>dappInfo: object DApp 信息<!-- -->
<ul>
<li>name:string</li>
<li>icon:string</li>
</ul>
</li>
<li>redirect?:string, 连接成功后的跳转参数</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
        btc<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token string">"btc:mainnet"</span><span class="token punctuation">,</span>
                  <span class="token comment">// "fractal:mainnet"</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包并签名" id="连接钱包并签名">连接钱包并签名<a class="index_header-anchor__Xqb+L" href="#连接钱包并签名" style="opacity:0">#</a></h2>
<p>连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">await okxUniversalConnectUI.openModalAndSign(connectParams: ConnectParams, signRequest: RequestParams[])</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息，BTC系的key为"btc"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，BTC系的key为"btc"，如果对应的链信息钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>sessionConfig: object<!-- -->
<ul>
<li>redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"</li>
</ul>
</li>
</ul>
</li>
<li>signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法<!-- -->
<ul>
<li>method: string;  请求的方法名称, BTC系支持的方法有："btc_signMessage"</li>
<li>chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中</li>
<li>params: unknown[] | Record<code>&lt;string, unknown&gt;</code> | object | undefined; 请求的方法对应的参数</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise<code>&lt;SessionTypes.Struct | undefined&gt;</code>
<ul>
<li>topic: string; 会话标识；</li>
<li>namespaces: <code>Record&lt;string, Namespace&gt;</code>; 成功连接的namespace 信息<!-- -->
<ul>
<li>chains: string[]; 连接的链信息</li>
<li>accounts: string[]; 连接的账户信息</li>
<li>methods: string[]; 当前namespace下，钱包支持的方法</li>
<li>defaultChain?: string; 当前会话的默认链</li>
</ul>
</li>
<li>sessionConfig?: SessionConfig<!-- -->
<ul>
<li>dappInfo: object DApp 信息<!-- -->
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
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 先添加签名结果监听</span>
okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect_signResponse"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">openModalAndSign</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
            btc<span class="token operator">:</span> <span class="token punctuation">{</span>
                chains<span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token string">"btc:mainnet"</span><span class="token punctuation">,</span>
                    <span class="token comment">// "fractal:mainnet"</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
            redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            method<span class="token operator">:</span> <span class="token string">"btc_signMessage"</span><span class="token punctuation">,</span>
            chainId<span class="token operator">:</span> <span class="token string">"btc:mainnet"</span><span class="token punctuation">,</span>
            params<span class="token operator">:</span> <span class="token punctuation">{</span>
                message<span class="token operator">:</span> <span class="token string">"Welcome to BTC"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
<span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="判断钱包是否已连接" id="判断钱包是否已连接">判断钱包是否已连接<a class="index_header-anchor__Xqb+L" href="#判断钱包是否已连接" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包</p>
<p><strong>返回值</strong></p>
<ul>
<li>boolean</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">connected</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>首先创建一个OKXBtcProvider对象，构造函数传入okxUniversalConnectUI</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXBtcProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxBtcProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXBtcProvider</span><span class="token punctuation">(</span>okxUniversalConnectUI<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取钱包账户信息" id="获取钱包账户信息">获取钱包账户信息<a class="index_header-anchor__Xqb+L" href="#获取钱包账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.getAccount(chainId)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId: 请求的链，如btc:mainnet, fractal:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址</li>
<li>publicKey: string 公钥</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"btc:mainnet"</span><span class="token punctuation">)</span>
<span class="token comment">//返回结构</span>
<span class="token punctuation">{</span>
    <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"038936b367d47b3796b430a31694320918afdc458d81dea9bb7dd35c0aad8bc694"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"03cbaedc26f03fd3ba02fc936f338e980c9e2172c5e23128877ed46827e935296f"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签名" id="签名">签名<a class="index_header-anchor__Xqb+L" href="#签名" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.signMessage(chain, message, type?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chain - string, 请求执行方法的链</li>
<li>signStr - string 需要签名的消息</li>
<li>type -  (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string: 签名结果</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"btc:mainnet"</span>
<span class="token keyword">let</span> signStr <span class="token operator">=</span> <span class="token string">"data need to sign ..."</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> signStr<span class="token punctuation">)</span>
<span class="token comment">//返回结构: "H83jZpulbMDDGUiTA4M8QNChmWwaKxwPCm8U5EBvftKlSMMzuvtVxBHlygtof5NBbdSVPiAtCvOUwZmz2vViHHU="</span>
</code></pre></div>
<h2 data-content="发送Bitcoin" id="发送bitcoin">发送Bitcoin<a class="index_header-anchor__Xqb+L" href="#发送bitcoin" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.sendBitcoin(chainId, toAddress, satoshis, options)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId - string, 请求签名执行的链，必传参数，如btc:mainnet</li>
<li>toAddress - string, string, 接收的地址</li>
<li>satoshis - number, 发送的聪数量</li>
<li>options - Object  (可选)<!-- -->
<ul>
<li>feeRate - number (可选) 自定义费率</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 交易哈希</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"btc:mainnet"</span>
<span class="token keyword">let</span> toAddress <span class="token operator">=</span> <span class="token string">'1NKnZ3uAuQLnmE...4u1efwCgTiAxBn'</span>
<span class="token keyword">let</span> satoshis <span class="token operator">=</span> <span class="token number">17000</span>
<span class="token keyword">let</span> options <span class="token operator">=</span> <span class="token punctuation">{</span>
    feeRate<span class="token operator">:</span> <span class="token number">16</span>
<span class="token punctuation">}</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">sendBitcoin</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> toAddress<span class="token punctuation">,</span> satoshis<span class="token punctuation">,</span> options<span class="token punctuation">)</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment">    返回结构:</span>
<span class="token doc-comment comment">    "ff18d01ef6abed3b7fd23247a1fc457ca...f49b6bb4529a19a5fb637f18ce2e"</span>
<span class="token doc-comment comment"> */</span>
</code></pre></div>
<h2 data-content="signPsbt" id="signpsbt">signPsbt<a class="index_header-anchor__Xqb+L" href="#signpsbt" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.signPsbt(chainId, psbtHex, options)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chain - string, 请求签名执行的链，必传参数，如btc:mainnet</li>
<li>psbtHex - string, 要签名的 psbt 的十六进制字符串</li>
<li>options:<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
<li>disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 已签名psbt的十六进制字符串</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"btc:mainnet"</span>
<span class="token keyword">let</span> psbtHex <span class="token operator">=</span> <span class="token string">""</span>
<span class="token keyword">let</span> options <span class="token operator">=</span> <span class="token punctuation">{</span> autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span> <span class="token punctuation">}</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">signPsbt</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> psbtHex<span class="token punctuation">,</span> options<span class="token punctuation">)</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment">    返回结构:</span>
<span class="token doc-comment comment">    "cHNidP8BAP0GAQIAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA/////yjWH1Uvx225V01diYYZ2i5jVAORF4nLWUWCg5bBaLQwAAAAAAD/////AwEAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AIb9jA0AAAAiUSDwUTBk/h5bXDG+3/Q7lD8vEhHRSrKJFockGxONIUiI4wAAAAAAAQErAQAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQETQD9magM5RHYbdRd4KZ70FfVEAW5hw3rLjrocWIyn2Gi2P2c6Gri0E/S/wREhgjM8u5zQ3GrpcSaC8KhCRxBq5/oBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABASsBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1ARNA83DNEJj5u/mgUoOhCWL07enXpb6RX/WfEBh97tyrXLlA/e0CowU1fpgrKn+PQ+9Z/5/EXGwcr1UkYaqBJ0ZpKQEXIA1UE650qVNSIp6+ZnMap1Vynpjxdsw5N89XTd8TIs4WAAEBK+gDAAAAAAAAIlEg8FEwZP4eW1wxvt/0O5Q/LxIR0UqyiRaHJBsTjSFIiOMBAwSDAAAAARNBZcHpcb6YDNWF+eIcFckjF1c8C83uRmEhS/8jJQOBFkIQol8hBCTYXOFAaeu6/4o2MsS20iITiM/rAOAOBZkXC4MBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSCJNrNn1Hs3lrQwoxaUMgkYr9xFjYHeqbt901wKrYvGlAA="</span>
<span class="token doc-comment comment"> */</span>
</code></pre></div>
<h2 data-content="signPsbts" id="signpsbts">signPsbts<a class="index_header-anchor__Xqb+L" href="#signpsbts" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.signPsbts(chainId, psbtHexs, options)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId - string, 请求签名执行的链，必传参数，如btc:mainnet</li>
<li>psbtHex - string[], 要签名的 psbt 的十六进制字符串</li>
<li>options - object[]<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
<li>disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string[] 已签名 psbt 的十六进制字符串</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"btc:mainnet"</span>
<span class="token keyword">let</span> psbtHexs <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">""</span><span class="token punctuation">]</span>
<span class="token keyword">let</span> options <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span> <span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">signPsbts</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> psbtHexs<span class="token punctuation">,</span> options<span class="token punctuation">)</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment">    返回结构:</span>
<span class="token doc-comment comment">    ["cHNidP8BAP0GAQIAAAADAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP////8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAA/////yjWH1Uvx225V01diYYZ2i5jVAORF4nLWUWCg5bBaLQwAAAAAAD/////AwEAAAAAAAAAIlEgwSVNrUCq6hIeU+DOwJmGNi9s1CInltGUjJR5GzUoHLUBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1AIb9jA0AAAAiUSDwUTBk/h5bXDG+3/Q7lD8vEhHRSrKJFockGxONIUiI4wAAAAAAAQErAQAAAAAAAAAiUSDBJU2tQKrqEh5T4M7AmYY2L2zUIieW0ZSMlHkbNSgctQETQD9magM5RHYbdRd4KZ70FfVEAW5hw3rLjrocWIyn2Gi2P2c6Gri0E/S/wREhgjM8u5zQ3GrpcSaC8KhCRxBq5/oBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABASsBAAAAAAAAACJRIMElTa1AquoSHlPgzsCZhjYvbNQiJ5bRlIyUeRs1KBy1ARNA83DNEJj5u/mgUoOhCWL07enXpb6RX/WfEBh97tyrXLlA/e0CowU1fpgrKn+PQ+9Z/5/EXGwcr1UkYaqBJ0ZpKQEXIA1UE650qVNSIp6+ZnMap1Vynpjxdsw5N89XTd8TIs4WAAEBK+gDAAAAAAAAIlEg8FEwZP4eW1wxvt/0O5Q/LxIR0UqyiRaHJBsTjSFIiOMBAwSDAAAAARNBZcHpcb6YDNWF+eIcFckjF1c8C83uRmEhS/8jJQOBFkIQol8hBCTYXOFAaeu6/4o2MsS20iITiM/rAOAOBZkXC4MBFyANVBOudKlTUiKevmZzGqdVcp6Y8XbMOTfPV03fEyLOFgABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSBhbicyOEDuDCrkNNmYJn+BFwmIupR3943NAPwkeifbQAABBSCJNrNn1Hs3lrQwoxaUMgkYr9xFjYHeqbt901wKrYvGlAA="]</span>
<span class="token doc-comment comment"> */</span>
</code></pre></div>
<h2 data-content="签名且广播 signAndPushPsbt" id="签名且广播-signandpushpsbt">签名且广播 signAndPushPsbt<a class="index_header-anchor__Xqb+L" href="#签名且广播-signandpushpsbt" style="opacity:0">#</a></h2>
<blockquote>
<p>App required: &gt;= 6.93.0</p>
</blockquote>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxBtcProvider.signAndPushPsbt(chainId, psbtHex, options)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chain - string, 请求签名执行的链，必传参数，如btc:mainnet</li>
<li>psbtHex - string, 要签名的 psbt 的十六进制字符串</li>
<li>options: - object<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
<li>disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>txhash 交易hash</li>
<li>signature 已签名 psbt 的十六进制字符串</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"btc:mainnet"</span>
<span class="token keyword">let</span> psbtHex <span class="token operator">=</span> <span class="token string">""</span>
<span class="token keyword">let</span> options <span class="token operator">=</span> <span class="token punctuation">{</span> autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span> <span class="token punctuation">}</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> okxBtcProvider<span class="token punctuation">.</span><span class="token function">signAndPushPsbt</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> psbtHex<span class="token punctuation">,</span> options<span class="token punctuation">)</span>

<span class="token doc-comment comment">/**
    返回结构:
    <span class="token punctuation">{</span>
        txhash: "",
        signature: ""
    <span class="token punctuation">}</span>
 */</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 生成 universalLink</span>
okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"display_uri"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>uri<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>uri<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// session 信息变更会触发该事件；</span>
okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_update"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 断开连接会触发该事件；</span>
okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_delete"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>topic<span class="token punctuation">}</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>topic<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 连接并签名时,签名结果会触发该事件;</span>
okxUniversalConnectUI<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect_signResponse"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>signResponse<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
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
    "Bitcoin兼容链",
    "UI"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "SDK",
    "UI",
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
    "安装及初始化",
    "连接钱包",
    "连接钱包并签名",
    "判断钱包是否已连接",
    "准备交易",
    "获取钱包账户信息",
    "签名",
    "发送Bitcoin",
    "signPsbt",
    "signPsbts",
    "签名且广播 signAndPushPsbt",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
