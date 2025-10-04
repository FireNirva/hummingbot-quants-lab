# SDK | Aptos | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-aptos-sdk#错误码  
**抓取时间:** 2025-05-27 07:07:46  
**字数:** 782

## 导航路径
DApp 连接钱包 > Aptos > SDK

## 目录
- 安装及初始化
- 连接钱包
- 判断钱包是否已连接
- 准备交易
- 获取钱包地址及publicKey
- 签名
- 签单笔交易
- 签多笔交易并上链
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
安装及初始化
#
请确保更新到 6.92.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/aptos-provider
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。
OKXUniversalProvider.init({dappMetaData: {name, icon}})
请求参数
dappMetaData - object
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
}
)
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数
okxUniversalProvider.connect(connectParams: ConnectParams)
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，EVM系的key为"eip155"，Aptos系的key为"aptos"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，Aptos系的key为"aptos"
，如果对应的链信息钱包不支持，依然可以连接
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
okxUniversalProvider
.
connect
(
{
namespaces
:
{
aptos
:
{
chains
:
[
"aptos:mainnet"
,
// aptos mainnet
// "movement:mainnet",// movement mainnet
// "movement:testnet",// movement testnet
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
判断钱包是否已连接
#
获取当前是否有连接钱包
返回值
boolean
示例
okxUniversalProvider
.
connected
(
)
准备交易
#
首先创建一个OKXAptosProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXAptosProvider
}
from
"@okxconnect/aptos-provider"
;
let
okxAptosProvider
=
new
OKXAptosProvider
(
okxUniversalProvider
)
获取钱包地址及publicKey
#
okxAptosProvider.getAccount(chain)
请求参数
chain: string, 获取钱包地址的链Id,不传则默认取第一个连接的aptos系地址
返回值
Object
address: string 钱包地址
publicKey: string 公钥
签名
#
okxAptosProvider.signMessage(message, chain)
请求参数
message - object
address?: boolean; // Should we include the address of the account in the message
application?: boolean; // Should we include the domain of the DApp
chainId?: boolean; // Should we include the current chain id the wallet is connected to
message: string; // The message to be signed and displayed to the user
nonce: string; // A nonce the DApp should generate
chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数
返回值
Promise - object
address: string;
application: string;
chainId: number;
fullMessage: string; // The message that was generated to sign
message: string; // The message passed in by the user
nonce: string;
prefix: string; // Should always be APTOS
signature: string; // The signed full message
签单笔交易
#
okxAptosProvider.signTransaction(transaction, chain)
请求参数
transaction - object | SimpleTransaction 交易数据对象
chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数
返回值
Promise - Buffer 签名buffer
签多笔交易并上链
#
okxAptosProvider.signAndSubmitTransaction(transactions, chain)
请求参数
transactions - object | SimpleTransaction 交易数据对象
chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数
返回值
Promise - string 交易hash
示例
//签名消息
let
data
=
{
address
:
true
,
application
:
true
,
chainId
:
true
,
message
:
"Hello OKX"
,
nonce
:
"1234"
}
let
provider
=
new
OKXAptosProvider
(
window
.
provider
)
let
message
=
await
provider
.
signMessage
(
data
,
"aptos:mainnet"
)
//返回值 {"address":"0x2acddad65c27c6e5b568b398f0d1d01ebb8b55466461bbd51c1e42763a92fdfe","application":"http://192.168.101.13","chainId":"aptos:mainnet","fullMessage":"APTOS\naddress: 0x2acddad65c27c6e5b568b398f0d1d01ebb8b55466461bbd51c1e42763a92fdfe\napplication: http://192.168.101.13\nchainId: aptos:mainnet\nmessage: 123 签名测试!\nnonce: 1234","message":"123 签名测试!","nonce":"1234","prefix":"APTOS","signature":"0xef4e587f537b80a2f4e424079984b80e130c92d939a92225764be00ed36486521e8857b8a222de4023c5f4d2e9fd2f62c26ca8a43694660583c8a5d4328da303","verified":true}
//签名交易并上链
const
config
=
new
AptosConfig
(
{
network
:
Network
.
MAINNET
}
)
;
const
aptos
=
new
Aptos
(
config
)
;
//支持通过@aptos-labs/ts-sdk创建的交易
const
transaction
=
await
aptos
.
transaction
.
build
.
simple
(
{
sender
:
"0x07897a0496703c27954fa3cc8310f134dd1f7621edf5e88b5bf436e4af70cfc6"
,
data
:
{
function
:
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::swap_exact_coin_for_coin_x1"
,
typeArguments
:
[
"0x1::aptos_coin::AptosCoin"
,
"0x111ae3e5bc816a5e63c2da97d0aa3886519e0cd5e4b046659fa35796bd11542a::stapt_token::StakedApt"
,
"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"
,
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"
]
,
functionArguments
:
[
"10000"
,
[
"9104"
]
,
[
"5"
]
,
[
"true"
]
]
,
}
,
}
)
;
let
result1
=
await
provider
.
signAndSubmitTransaction
(
transaction
,
"aptos:mainnet"
)
//同时支持下方数据格式的交易
let
transactionData
=
{
"arguments"
:
[
"100000"
,
[
"0"
,
"0"
,
"10533"
]
,
[
"10"
,
"5"
,
"5"
]
,
[
"false"
,
"false"
,
"true"
]
]
,
"function"
:
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::swap_exact_coin_for_coin_x3"
,
"type"
:
"entry_function_payload"
,
"type_arguments"
:
[
"0x1::aptos_coin::AptosCoin"
,
"0x73eb84966be67e4697fc5ae75173ca6c35089e802650f75422ab49a8729704ec::coin::DooDoo"
,
"0x53a30a6e5936c0a4c5140daed34de39d17ca7fcae08f947c02e979cef98a3719::coin::LSD"
,
"0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC"
,
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::CurveV1"
,
"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"
,
"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"
,
"0x54cb0bb2c18564b86e34539b9f89cfe1186e39d89fce54e1cd007b8e61673a85::bin_steps::X80"
,
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"
,
"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"
]
}
let
result2
=
await
provider
.
signAndSubmitTransaction
(
transactionData
,
"movement:testnet"
)
断开钱包连接
#
断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包
okxUniversalProvider
.
disconnect
(
)
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
// session 信息变更会触发该事件；
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
<div class="routes_md__xWlGF"><!--$--><h1 id="sdk">SDK<a class="index_header-anchor__Xqb+L" href="#sdk" style="opacity:0">#</a></h1>
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新到 6.92.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/aptos-provider</code></pre></div>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作。</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">OKXUniversalProvider.init({dappMetaData: {name, icon}})</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>dappMetaData - object<!-- -->
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
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXUniversalProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> okxUniversalProvider <span class="token operator">=</span> <span class="token keyword">await</span> OKXUniversalProvider<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    dappMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        name<span class="token operator">:</span> <span class="token string">"application name"</span><span class="token punctuation">,</span>
        icon<span class="token operator">:</span> <span class="token string">"application icon url"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalProvider.connect(connectParams: ConnectParams)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，EVM系的key为"eip155"，Aptos系的key为"aptos"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，Aptos系的key为"aptos"
，如果对应的链信息钱包不支持，依然可以连接<!-- -->
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
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
        aptos<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"aptos:mainnet"</span><span class="token punctuation">,</span> <span class="token comment">// aptos mainnet</span>
                  <span class="token comment">// "movement:mainnet",// movement mainnet</span>
                  <span class="token comment">//  "movement:testnet",// movement testnet</span>

            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="判断钱包是否已连接" id="判断钱包是否已连接">判断钱包是否已连接<a class="index_header-anchor__Xqb+L" href="#判断钱包是否已连接" style="opacity:0">#</a></h2>
<p>获取当前是否有连接钱包</p>
<p><strong>返回值</strong></p>
<ul>
<li>boolean</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">connected</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>首先创建一个OKXAptosProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXAptosProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/aptos-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxAptosProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXAptosProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取钱包地址及publicKey" id="获取钱包地址及publickey">获取钱包地址及publicKey<a class="index_header-anchor__Xqb+L" href="#获取钱包地址及publickey" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxAptosProvider.getAccount(chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>chain: string, 获取钱包地址的链Id,不传则默认取第一个连接的aptos系地址</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址</li>
<li>publicKey: string 公钥</li>
</ul>
</li>
</ul>
<h2 data-content="签名" id="签名">签名<a class="index_header-anchor__Xqb+L" href="#签名" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxAptosProvider.signMessage(message, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>message - object<!-- -->
<ul>
<li>address?: boolean; // Should we include the address of the account in the message</li>
<li>application?: boolean; // Should we include the domain of the DApp</li>
<li>chainId?: boolean; // Should we include the current chain id the wallet is connected to</li>
<li>message: string; // The message to be signed and displayed to the user</li>
<li>nonce: string; // A nonce the DApp should generate</li>
</ul>
</li>
<li>chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>address: string;</li>
<li>application: string;</li>
<li>chainId: number;</li>
<li>fullMessage: string; // The message that was generated to sign</li>
<li>message: string; // The message passed in by the user</li>
<li>nonce: string;</li>
<li>prefix: string; // Should always be APTOS</li>
<li>signature: string; // The signed full message</li>
</ul>
</li>
</ul>
<h2 data-content="签单笔交易" id="签单笔交易">签单笔交易<a class="index_header-anchor__Xqb+L" href="#签单笔交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxAptosProvider.signTransaction(transaction, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transaction - object | SimpleTransaction 交易数据对象</li>
<li>chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - Buffer 签名buffer</li>
</ul>
<h2 data-content="签多笔交易并上链" id="签多笔交易并上链">签多笔交易并上链<a class="index_header-anchor__Xqb+L" href="#签多笔交易并上链" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxAptosProvider.signAndSubmitTransaction(transactions, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transactions - object | SimpleTransaction 交易数据对象</li>
<li>chain: string, 请求签名执行的链，建议传递此参数；连接多条链时为必传参数</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string 交易hash</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">//签名消息</span>
<span class="token keyword">let</span> data <span class="token operator">=</span> <span class="token punctuation">{</span>
    address<span class="token operator">:</span><span class="token boolean">true</span><span class="token punctuation">,</span>
    application<span class="token operator">:</span><span class="token boolean">true</span><span class="token punctuation">,</span>
    chainId<span class="token operator">:</span><span class="token boolean">true</span><span class="token punctuation">,</span>
    message<span class="token operator">:</span><span class="token string">"Hello OKX"</span><span class="token punctuation">,</span>
    nonce<span class="token operator">:</span><span class="token string">"1234"</span>
<span class="token punctuation">}</span>

<span class="token keyword">let</span> provider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXAptosProvider</span><span class="token punctuation">(</span>window<span class="token punctuation">.</span>provider<span class="token punctuation">)</span>
<span class="token keyword">let</span> message <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>data<span class="token punctuation">,</span> <span class="token string">"aptos:mainnet"</span><span class="token punctuation">)</span>

<span class="token comment">//返回值 {"address":"0x2acddad65c27c6e5b568b398f0d1d01ebb8b55466461bbd51c1e42763a92fdfe","application":"http://192.168.101.13","chainId":"aptos:mainnet","fullMessage":"APTOS\naddress: 0x2acddad65c27c6e5b568b398f0d1d01ebb8b55466461bbd51c1e42763a92fdfe\napplication: http://192.168.101.13\nchainId: aptos:mainnet\nmessage: 123 签名测试!\nnonce: 1234","message":"123 签名测试!","nonce":"1234","prefix":"APTOS","signature":"0xef4e587f537b80a2f4e424079984b80e130c92d939a92225764be00ed36486521e8857b8a222de4023c5f4d2e9fd2f62c26ca8a43694660583c8a5d4328da303","verified":true}</span>

<span class="token comment">//签名交易并上链</span>
<span class="token keyword">const</span> config <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">AptosConfig</span><span class="token punctuation">(</span><span class="token punctuation">{</span> network<span class="token operator">:</span> Network<span class="token punctuation">.</span><span class="token constant">MAINNET</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> aptos <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Aptos</span><span class="token punctuation">(</span>config<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">//支持通过@aptos-labs/ts-sdk创建的交易</span>
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">await</span> aptos<span class="token punctuation">.</span>transaction<span class="token punctuation">.</span>build<span class="token punctuation">.</span><span class="token function">simple</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    sender<span class="token operator">:</span> <span class="token string">"0x07897a0496703c27954fa3cc8310f134dd1f7621edf5e88b5bf436e4af70cfc6"</span><span class="token punctuation">,</span>
    data<span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token keyword">function</span><span class="token operator">:</span> <span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::swap_exact_coin_for_coin_x1"</span><span class="token punctuation">,</span>
        typeArguments<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"0x1::aptos_coin::AptosCoin"</span><span class="token punctuation">,</span> <span class="token string">"0x111ae3e5bc816a5e63c2da97d0aa3886519e0cd5e4b046659fa35796bd11542a::stapt_token::StakedApt"</span><span class="token punctuation">,</span> <span class="token string">"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"</span><span class="token punctuation">,</span> <span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        functionArguments<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"10000"</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token string">"9104"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token string">"5"</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token string">"true"</span><span class="token punctuation">]</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> result1 <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signAndSubmitTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">,</span> <span class="token string">"aptos:mainnet"</span><span class="token punctuation">)</span>

<span class="token comment">//同时支持下方数据格式的交易</span>
<span class="token keyword">let</span> transactionData <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"arguments"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"100000"</span><span class="token punctuation">,</span><span class="token punctuation">[</span><span class="token string">"0"</span><span class="token punctuation">,</span><span class="token string">"0"</span><span class="token punctuation">,</span><span class="token string">"10533"</span><span class="token punctuation">]</span><span class="token punctuation">,</span><span class="token punctuation">[</span><span class="token string">"10"</span><span class="token punctuation">,</span><span class="token string">"5"</span><span class="token punctuation">,</span><span class="token string">"5"</span><span class="token punctuation">]</span><span class="token punctuation">,</span><span class="token punctuation">[</span><span class="token string">"false"</span><span class="token punctuation">,</span><span class="token string">"false"</span><span class="token punctuation">,</span><span class="token string">"true"</span><span class="token punctuation">]</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"function"</span><span class="token operator">:</span> <span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::swap_exact_coin_for_coin_x3"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"entry_function_payload"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"type_arguments"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"0x1::aptos_coin::AptosCoin"</span><span class="token punctuation">,</span><span class="token string">"0x73eb84966be67e4697fc5ae75173ca6c35089e802650f75422ab49a8729704ec::coin::DooDoo"</span><span class="token punctuation">,</span><span class="token string">"0x53a30a6e5936c0a4c5140daed34de39d17ca7fcae08f947c02e979cef98a3719::coin::LSD"</span><span class="token punctuation">,</span><span class="token string">"0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC"</span><span class="token punctuation">,</span><span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::CurveV1"</span><span class="token punctuation">,</span><span class="token string">"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"</span><span class="token punctuation">,</span><span class="token string">"0x0163df34fccbf003ce219d3f1d9e70d140b60622cb9dd47599c25fb2f797ba6e::curves::Uncorrelated"</span><span class="token punctuation">,</span><span class="token string">"0x54cb0bb2c18564b86e34539b9f89cfe1186e39d89fce54e1cd007b8e61673a85::bin_steps::X80"</span><span class="token punctuation">,</span><span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"</span><span class="token punctuation">,</span><span class="token string">"0x80273859084bc47f92a6c2d3e9257ebb2349668a1b0fb3db1d759a04c7628855::router::BinStepV0V05"</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>
<span class="token keyword">let</span> result2 <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signAndSubmitTransaction</span><span class="token punctuation">(</span>transactionData<span class="token punctuation">,</span> <span class="token string">"movement:testnet"</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 生成 universalLink</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"display_uri"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>uri<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>uri<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// session 信息变更会触发该事件；</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_update"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 断开连接会触发该事件；</span>
okxUniversalProvider<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"session_delete"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>topic<span class="token punctuation">}</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>topic<span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "Aptos",
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
    "SUI",
    "Aptos/Movement",
    "SDK",
    "UI",
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
    "获取钱包地址及publicKey",
    "签名",
    "签单笔交易",
    "签多笔交易并上链",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
