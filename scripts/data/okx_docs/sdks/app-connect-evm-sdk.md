# SDK | EVM兼容链 | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-evm-sdk#sdk  
**抓取时间:** 2025-05-27 06:58:26  
**字数:** 1046

## 导航路径
DApp 连接钱包 > EVM兼容链 > SDK

## 目录
- 安装及初始化
- 连接钱包
- 判断钱包是否已连接
- 准备交易
- 使用RPC
- 设置默认网络
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
安装及初始化
#
请确保更新OKX App到 6.88.0 版本或以后版本，即可开始接入：
将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/universal-provider
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。
OKXUniversalProvider.init({DAppMetaData: {name, icon}})
请求参数
DAppMetaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。
返回值
OKXUniversalProvider
示例
import
{
OKXUniversalProvider
}
from
"@okxconnect/universal-provider"
;
const
okxUniversalProvider
=
await
OKXUniversalProvider
.
init
(
{
DAppMetaData
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
}
)
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数;
okxUniversalProvider.connect(connectParams: ConnectParams);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；
chains: string[]; 链id信息,
defaultChain?: string; 默认链
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。
chains: string[]; 链id信息,
defaultChain?: string; 默认链
rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；
sessionConfig: object
redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"
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
redirect?:string, 连接成功后的跳转参数；
示例
var
session
=
await
okxUniversalProvider
.
connect
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
)
判断钱包是否已连接
#
获取当前是否有连接钱包;
返回值
boolean
示例
okxUniversalProvider
.
connected
(
)
;
准备交易
#
向钱包发送消息的方法，支持签名，交易;
okxUniversalProvider.request(requestArguments, chain);
请求参数
requestArguments - object
method: string; 请求的方法名，
params?: unknown[] | Record
<string, unknown>
| object | undefined; 请求的方法对应的参数；
redirect -string 'none' |
${string}://${string}
; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取connect方法传递的 redirect，默认为 ‘none’
chain: string, 请求方法执行的链，建议传该参数，如果未传的话，会被设置为当前的defaultChain；
返回值
根据不同方法的执行结果，会返回不同的参数，具体参数参照下面的示例；
personal_sign
Promise - string 签名结果；
eth_signTypedData_v4
Promise - string 签名结果
eth_sendTransaction
Promise - string hash
eth_accounts
Promise - string[] 返回默认chainId的地址;
eth_requestAccounts
Promise - string[] 返回默认chainId的地址;
eth_chainId
Promise - number 返回默认链id;
wallet_switchEthereumChain
Promise - null
wallet_addEthereumChain
Promise - null
wallet_watchAsset
Promise - boolean 添加成功
示例
let
chain
=
'eip155:1'
var
data
=
{
}
// 在chain链上执行 personalSign，
// params 数组中，第一个参数为 Challenge 必选；
// 第二个参数 hex encoded address 为可选项
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
okxUniversalProvider
.
request
(
data
,
chain
)
//personalSignResult: 0xe8d34297c33a61"
// 在chain链上执行 eth_signTypedData_v4
// params 数组中，第一个参数为 地址 是可选项；
// 第二个参数是TypedData 必传
data
=
{
"method"
:
"eth_signTypedData_v4"
,
"params"
:
[
"0x00000"
,
{
"domain"
:
{
"name"
:
"Ether Mail"
,
"version"
:
"1"
,
"chainId"
:
1
,
"verifyingContract"
:
"0xcccccccccccccccccccccccccccccccccccccccc"
}
,
"message"
:
{
"from"
:
{
"name"
:
"Cow"
,
"wallet"
:
"0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"
}
,
"to"
:
{
"name"
:
"Bob"
,
"wallet"
:
"0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"
}
,
"contents"
:
"Hello, Bob!"
}
,
"primaryType"
:
"Mail"
,
"types"
:
{
"EIP712Domain"
:
[
{
"name"
:
"name"
,
"type"
:
"string"
}
,
{
"name"
:
"version"
,
"type"
:
"string"
}
,
{
"name"
:
"chainId"
,
"type"
:
"uint256"
}
,
{
"name"
:
"verifyingContract"
,
"type"
:
"address"
}
]
,
"Person"
:
[
{
"name"
:
"name"
,
"type"
:
"string"
}
,
{
"name"
:
"wallet"
,
"type"
:
"address"
}
]
,
"Mail"
:
[
{
"name"
:
"from"
,
"type"
:
"Person"
}
,
{
"name"
:
"to"
,
"type"
:
"Person"
}
,
{
"name"
:
"contents"
,
"type"
:
"string"
}
]
}
}
]
}
var
signTypeV4Result
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
//signTypeV4Result: "0xa8bb3c6b33a119d..."
// 在chain链上执行 sendTransaction,
data
=
{
"method"
:
"eth_sendTransaction"
,
"params"
:
[
{
to
:
"0x4B..."
,
from
:
"0xDe..."
,
gas
:
"0x76c0"
,
value
:
"0x8ac7230489e80000"
,
data
:
"0x"
,
gasPrice
:
"0x4a817c800"
}
]
}
var
sendTransactionResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
// "0x1ccf2c4a3d689067fc2ac..."
// 获取默认链的地址信息；
data
=
{
"method"
:
"eth_requestAccounts"
}
var
ethRequestAccountsResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
// ["0xf2f3e73b..."]
// 获取默认链信息；
data
=
{
"method"
:
"eth_chainId"
}
var
chainIdResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
//chainIdResult 1
// 切换链；
data
=
{
"method"
:
"wallet_switchEthereumChain"
,
"params"
:
[
{
chainId
:
"0x1"
}
]
}
var
switchResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
// switchResult null
// 添加链
data
=
{
"method"
:
"wallet_addEthereumChain"
,
"params"
:
[
{
"blockExplorerUrls"
:
[
"https://explorer.fuse.io"
]
,
"chainId"
:
"0x7a"
,
"chainName"
:
"Fuse"
,
"nativeCurrency"
:
{
"name"
:
"Fuse"
,
"symbol"
:
"FUSE"
,
"decimals"
:
18
}
,
"rpcUrls"
:
[
"https://rpc.fuse.io"
]
}
]
}
var
addEthereumChainResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
//addEthereumChainResult null
// 在chain链 watchAsset 添加币种
data
=
{
"method"
:
"wallet_watchAsset"
,
"params"
:
[
{
"type"
:
"ERC20"
,
"options"
:
{
"address"
:
"0xeB51D9A39AD5EEF215dC0Bf39a8821ff804A0F01"
,
"symbol"
:
"LGNS"
,
"image"
:
"https://polygonscan.com/token/images/originlgns_32.png"
,
"decimals"
:
9
}
}
]
}
var
watchAssetResult
=
await
okxUniversalProvider
.
request
(
data
,
chain
)
// watchAssetResult
// true/false
使用RPC
#
当EVM系的 request 中 method 无法满足需求时，可通过配置 RPC 实现更多功能，在连接钱包connect()时,RPC配置在rpcMap中。
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
设置默认网络
#
在连接多个网络的状况下,如果开发者没有明确指定当前操作所在网络,则通过默认网络进行交互
示例
okxUniversalProvider
.
setDefaultChain
(
"eip155:1"
)
断开钱包连接
#
断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包
okxUniversalProvider
.
disconnect
(
)
;
Event事件
#
// 生成 universalLink
okxUniversalProvider
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
okxUniversalProvider
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
okxUniversalProvider
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
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新OKX App到 6.88.0 版本或以后版本，即可开始接入：</p>
<p>将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/universal-provider</code></pre></div>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。</p>
<p><code>OKXUniversalProvider.init({DAppMetaData: {name, icon}})</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>DAppMetaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>OKXUniversalProvider</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span>OKXUniversalProvider<span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> okxUniversalProvider <span class="token operator">=</span> <span class="token keyword">await</span> OKXUniversalProvider<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    DAppMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        name<span class="token operator">:</span> <span class="token string">"application name"</span><span class="token punctuation">,</span>
        icon<span class="token operator">:</span> <span class="token string">"application icon url"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数;</p>
<p><code>okxUniversalProvider.connect(connectParams: ConnectParams);</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息， EVM系的key为"eip155"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息,</li>
<li>defaultChain?: string; 默认链</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，如果对应的链信息钱包不支持，依然可以连接；如果需要连接自定义网络的话，可以将自定义网络的请求添加到此参数中，如果钱包中已经有该自定义网络，则会在请求结果 session 中返回该自定义链的信息；如果钱包不支持的话，请求结果session 中无该自定义链信息，可以再次调用 request 方法，method 设置为 wallet_addEthereumChain，添加该自定义链。<!-- -->
<ul>
<li>chains: string[]; 链id信息,</li>
<li>defaultChain?: string; 默认链</li>
<li>rpcMap?: [chainId: string]: string; rpc 信息，配置了rpc url才能请求链上rpc信息，仅支持EVM系，配置RPC的链必须包含在chains中；</li>
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
<li>redirect?:string, 连接成功后的跳转参数；</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
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
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="判断钱包是否已连接" id="判断钱包是否已连接">判断钱包是否已连接<a class="index_header-anchor__Xqb+L" href="#判断钱包是否已连接" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包;</p>
<p><strong>返回值</strong></p>
<ul>
<li>boolean</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">connected</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法，支持签名，交易;</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalProvider.request(requestArguments, chain);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>requestArguments - object<!-- -->
<ul>
<li>method: string; 请求的方法名，</li>
<li>params?: unknown[]  | Record<code>&lt;string, unknown&gt;</code> | object | undefined; 请求的方法对应的参数；</li>
<li>redirect -string 'none' | <code>${string}://${string}</code>; App 钱包中，用户签署或拒绝请求时深层链接的返回策略，如果是Telegram中的Mini App，可以配置tg://resolve，如果这里没有配置的话，会取connect方法传递的 redirect，默认为 ‘none’</li>
</ul>
</li>
<li>chain: string, 请求方法执行的链，建议传该参数，如果未传的话，会被设置为当前的defaultChain；</li>
</ul>
<p><strong>返回值</strong></p>
<p>根据不同方法的执行结果，会返回不同的参数，具体参数参照下面的示例；</p>
<ul>
<li>
<p>personal_sign</p>
<ul>
<li>Promise - string 签名结果；</li>
</ul>
</li>
<li>
<p>eth_signTypedData_v4</p>
<ul>
<li>Promise - string 签名结果</li>
</ul>
</li>
<li>
<p>eth_sendTransaction</p>
<ul>
<li>Promise - string hash</li>
</ul>
</li>
<li>
<p>eth_accounts</p>
<ul>
<li>Promise - string[] 返回默认chainId的地址;</li>
</ul>
</li>
<li>
<p>eth_requestAccounts</p>
<ul>
<li>Promise - string[] 返回默认chainId的地址;</li>
</ul>
</li>
<li>
<p>eth_chainId</p>
<ul>
<li>Promise - number 返回默认链id;</li>
</ul>
</li>
<li>
<p>wallet_switchEthereumChain</p>
<ul>
<li>Promise - null</li>
</ul>
</li>
<li>
<p>wallet_addEthereumChain</p>
<ul>
<li>Promise - null</li>
</ul>
</li>
<li>
<p>wallet_watchAsset</p>
<ul>
<li>Promise - boolean 添加成功</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">'eip155:1'</span>
<span class="token keyword">var</span> data <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token punctuation">}</span>

<span class="token comment">// 在chain链上执行 personalSign，</span>
<span class="token comment">// params 数组中，第一个参数为 Challenge 必选；</span>
<span class="token comment">//               第二个参数 hex encoded address 为可选项</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"personal_sign"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"0x506c65617365207369676e2074686973206d65737361676520746f20636f6e6669726d20796f7572206964656e746974792e"</span><span class="token punctuation">,</span>
        <span class="token string">"0x4B0897b0513FdBeEc7C469D9aF4fA6C0752aBea7"</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> personalSignResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">//personalSignResult:   0xe8d34297c33a61"</span>

<span class="token comment">// 在chain链上执行 eth_signTypedData_v4</span>
<span class="token comment">// params 数组中，第一个参数为 地址 是可选项；</span>
<span class="token comment">//               第二个参数是TypedData 必传</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"eth_signTypedData_v4"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"0x00000"</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span>
            <span class="token string-property property">"domain"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"Ether Mail"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"version"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"chainId"</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
                <span class="token string-property property">"verifyingContract"</span><span class="token operator">:</span> <span class="token string">"0xcccccccccccccccccccccccccccccccccccccccc"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token string-property property">"message"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token string-property property">"from"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"Cow"</span><span class="token punctuation">,</span> <span class="token string-property property">"wallet"</span><span class="token operator">:</span> <span class="token string">"0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token string-property property">"to"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"Bob"</span><span class="token punctuation">,</span> <span class="token string-property property">"wallet"</span><span class="token operator">:</span> <span class="token string">"0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token string-property property">"contents"</span><span class="token operator">:</span> <span class="token string">"Hello, Bob!"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token string-property property">"primaryType"</span><span class="token operator">:</span> <span class="token string">"Mail"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"types"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token string-property property">"EIP712Domain"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"name"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"string"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
                    <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"version"</span><span class="token punctuation">,</span>
                    <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"string"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"chainId"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"uint256"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"verifyingContract"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span><span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token string-property property">"Person"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"name"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"string"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"wallet"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span><span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token string-property property">"Mail"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"from"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"Person"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"to"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"Person"</span><span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
                    <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"contents"</span><span class="token punctuation">,</span>
                    <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"string"</span>
                <span class="token punctuation">}</span><span class="token punctuation">]</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> signTypeV4Result <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">//signTypeV4Result: "0xa8bb3c6b33a119d..."</span>

<span class="token comment">// 在chain链上执行 sendTransaction,</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"eth_sendTransaction"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            to<span class="token operator">:</span> <span class="token string">"0x4B..."</span><span class="token punctuation">,</span>
            from<span class="token operator">:</span> <span class="token string">"0xDe..."</span><span class="token punctuation">,</span>
            gas<span class="token operator">:</span> <span class="token string">"0x76c0"</span><span class="token punctuation">,</span>
            value<span class="token operator">:</span> <span class="token string">"0x8ac7230489e80000"</span><span class="token punctuation">,</span>
            data<span class="token operator">:</span> <span class="token string">"0x"</span><span class="token punctuation">,</span>
            gasPrice<span class="token operator">:</span> <span class="token string">"0x4a817c800"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> sendTransactionResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">// "0x1ccf2c4a3d689067fc2ac..."</span>

<span class="token comment">// 获取默认链的地址信息；</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"eth_requestAccounts"</span><span class="token punctuation">}</span>
<span class="token keyword">var</span> ethRequestAccountsResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">//  ["0xf2f3e73b..."]</span>

<span class="token comment">// 获取默认链信息；</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span><span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"eth_chainId"</span><span class="token punctuation">}</span>
<span class="token keyword">var</span> chainIdResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">//chainIdResult   1</span>

<span class="token comment">// 切换链；</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"wallet_switchEthereumChain"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            chainId<span class="token operator">:</span> <span class="token string">"0x1"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> switchResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">// switchResult null</span>

<span class="token comment">// 添加链</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"wallet_addEthereumChain"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
        <span class="token string-property property">"blockExplorerUrls"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"https://explorer.fuse.io"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string-property property">"chainId"</span><span class="token operator">:</span> <span class="token string">"0x7a"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Fuse"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"nativeCurrency"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"Fuse"</span><span class="token punctuation">,</span> <span class="token string-property property">"symbol"</span><span class="token operator">:</span> <span class="token string">"FUSE"</span><span class="token punctuation">,</span> <span class="token string-property property">"decimals"</span><span class="token operator">:</span> <span class="token number">18</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token string-property property">"rpcUrls"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"https://rpc.fuse.io"</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> addEthereumChainResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">//addEthereumChainResult   null</span>

<span class="token comment">// 在chain链 watchAsset 添加币种</span>
data <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"method"</span><span class="token operator">:</span> <span class="token string">"wallet_watchAsset"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"params"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
        <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"ERC20"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"options"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0xeB51D9A39AD5EEF215dC0Bf39a8821ff804A0F01"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"symbol"</span><span class="token operator">:</span> <span class="token string">"LGNS"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"image"</span><span class="token operator">:</span> <span class="token string">"https://polygonscan.com/token/images/originlgns_32.png"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"decimals"</span><span class="token operator">:</span> <span class="token number">9</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">var</span> watchAssetResult <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> chain<span class="token punctuation">)</span>
<span class="token comment">// watchAssetResult</span>
<span class="token comment">// true/false</span>

</code></pre></div>
<h2 data-content="使用RPC" id="使用rpc">使用RPC<a class="index_header-anchor__Xqb+L" href="#使用rpc" style="opacity:0">#</a></h2>
<p>当EVM系的 request 中 method 无法满足需求时，可通过配置 RPC 实现更多功能，在连接钱包connect()时,RPC配置在rpcMap中。</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">//查询交易Hash的详细信息</span>
<span class="token keyword">let</span> rpcData <span class="token operator">=</span> <span class="token punctuation">{</span>
    method<span class="token operator">:</span> <span class="token string">"eth_getTransactionByHash"</span><span class="token punctuation">,</span>
    params<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"0xd62fa4ea3cf7ee3bf6f5302b764490730186ed6a567c283517e8cb3c36142e1a"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> result <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">request</span><span class="token punctuation">(</span>rpcData<span class="token punctuation">,</span><span class="token string">"eip155:137"</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="设置默认网络" id="设置默认网络">设置默认网络<a class="index_header-anchor__Xqb+L" href="#设置默认网络" style="opacity:0">#</a></h2>
<p>在连接多个网络的状况下,如果开发者没有明确指定当前操作所在网络,则通过默认网络进行交互</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">setDefaultChain</span><span class="token punctuation">(</span><span class="token string">"eip155:1"</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 生成 universalLink</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"display_uri"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>uri<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>uri<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// session 信息变更（例如添加自定义链）会触发该事件；</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_update"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 断开连接会触发该事件；</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_delete"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>topic<span class="token punctuation">}</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>topic<span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "EVM兼容链",
    "SDK"
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
    "安装及初始化",
    "连接钱包",
    "判断钱包是否已连接",
    "准备交易",
    "使用RPC",
    "设置默认网络",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
