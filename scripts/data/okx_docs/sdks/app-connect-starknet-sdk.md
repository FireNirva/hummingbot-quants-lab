# SDK | Starknet | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-starknet-sdk#sdk  
**抓取时间:** 2025-05-27 07:32:27  
**字数:** 660

## 导航路径
DApp 连接钱包 > Starknet > SDK

## 目录
- 安装及初始化
- 连接钱包
- 准备交易
- 获取账户信息
- 签署消息
- 签署交易并广播上链 sendTransaction
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
安装及初始化
#
请确保更新OKX App到 6.98.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/universal-provider
连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作
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
,
}
)
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数
okxUniversalProvider.connect(connectParams: ConnectParams)
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， starknet系的key为"starknet"，目前只支持starknet:mainnet，如果请求的链中，有任何一个链当前钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， starknet系的key为"starknet"，目前只支持starknet:mainnet，如果请求的链当前钱包不支持，依然可以连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
sessionConfig: object
redirect: string 连接成功后的跳转参数，如果是Telegram中的Mini App，这里可以设置为Telegram的deeplink: "tg://resolve"
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识
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
starknet
:
{
chains
:
[
"starknet:mainnet"
,
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
准备交易
#
首先创建一个OKXStarknetProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXStarknetProvider
}
from
"@okxconnect/universal-provider"
;
let
okxStarknetProvider
=
new
OKXStarknetProvider
(
okxUniversalProvider
)
获取账户信息
#
okxStarknetProvider.getAccount(chainId)
请求参数
chainId: 请求的链，如starknet:mainnet
返回值
Object
address: string 钱包地址,
pubKey: string 公钥
示例
let
result
=
okxStarknetProvider
.
getAccount
(
"starknet:mainnet"
)
//返回结构
{
address
:
"0x0667ae9b1c3d3ab1dacffd8b23269e9fedf2f8de5c57a35fe0a55f209db59179"
,
pubKey
:
"07c26f0fd90a6847d3de5ce7002dcd9454b45a78d5592ee369c4d7561fa5e5ee"
}
签署消息
#
okxStarknetProvider.signMessage(signerAddress, typedData, chain)
请求参数
signerAddress - string, 钱包地址
typedData - object 需要签名的消息，按照固定格式签名
chain? - string, 请求执行方法的链
返回值
Promise - [string, string] 签名结果r, v
示例
let
chain
=
"starknet:mainnet"
let
address
=
okxStarknetProvider
.
getAccount
(
"starknet:mainnet"
)
.
address
const
signData
=
{
"domain"
:
{
"chainId"
:
"0x534e5f4d41494e"
,
"name"
:
"STRKFarm"
,
"version"
:
"1"
}
,
"message"
:
{
"document"
:
"app.strkfarm.xyz/tnc/v1"
,
"message"
:
"Read and Agree T&C"
}
,
"primaryType"
:
"Tnc"
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
,
{
"name"
:
"version"
,
"type"
:
"felt"
}
,
{
"name"
:
"chainId"
,
"type"
:
"felt"
}
]
,
"Tnc"
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
,
{
"name"
:
"document"
,
"type"
:
"felt"
}
]
}
}
let
result
=
okxStarknetProvider
.
signMessage
(
address
,
signData
,
chain
)
//返回:0x07fcd65fded07c7daaa79a818a39c5236562914a5d48fa7fad268fac609faa9a,0x0324c3bafc4d0e7e04a3a0b805bf8438f5111e308c4d596daa46fc213b37ebf1
签署交易并广播上链 sendTransaction
#
okxStarknetProvider.sendTransaction(signerAddress, transaction, chainId?)
请求参数
signerAddress - string,钱包地址
transaction - object，交易信息 按照固定格式签名
chainId? - string, 请求签名执行的链
返回值
Promise - string 交易hash
示例
let
val
=
uint256
.
bnToUint256
(
120000000000000000
)
const
transferCalldata
=
CallData
.
compile
(
{
to
:
"0x00b909cefa36ab6bc26f5887a867e46ef162238f0a171b1c2974b665afd4237f"
,
value
:
val
}
)
const
DAITokenAddress
=
"0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3"
const
invokeParams
=
{
calls
:
[
{
contract_address
:
DAITokenAddress
,
entry_point
:
"transfer"
,
calldata
:
transferCalldata
}
]
,
}
let
okxStarknetProvider
=
new
OKXStarknetProvider
(
window
.
provider
)
let
address
=
okxStarknetProvider
.
getAccount
(
"starknet:mainnet"
)
.
address
let
res
=
await
provider
.
sendTransaction
(
this
.
address
,
invokeParams
,
"starknet:mainnet"
)
//返回值：0x515d9de049c43477cee7eaea987ab04995d8dc2a7b3d7a184dca4bcd7224ec2
断开钱包连接
#
断开已连接钱包，并删除当前会话，如果要切换钱包，请先断开当前钱包后重新连接
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
<p>请确保更新OKX App到 6.98.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/universal-provider</code></pre></div>
<p>连接钱包之前，需要先创建一个对象，用于后续连接钱包、发送交易等操作</p>
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
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalProvider.connect(connectParams: ConnectParams)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， starknet系的key为"starknet"，目前只支持starknet:mainnet，如果请求的链中，有任何一个链当前钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，  starknet系的key为"starknet"，目前只支持starknet:mainnet，如果请求的链当前钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息<!-- -->
<ul>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
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
<li>topic: string; 会话标识</li>
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
        starknet<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token string">"starknet:mainnet"</span><span class="token punctuation">,</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>首先创建一个OKXStarknetProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXStarknetProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxStarknetProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXStarknetProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxStarknetProvider.getAccount(chainId)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId: 请求的链，如starknet:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址,</li>
<li>pubKey: string 公钥</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> result <span class="token operator">=</span> okxStarknetProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"starknet:mainnet"</span><span class="token punctuation">)</span>
<span class="token comment">//返回结构</span>
<span class="token punctuation">{</span>
    address<span class="token operator">:</span><span class="token string">"0x0667ae9b1c3d3ab1dacffd8b23269e9fedf2f8de5c57a35fe0a55f209db59179"</span><span class="token punctuation">,</span>
    pubKey<span class="token operator">:</span><span class="token string">"07c26f0fd90a6847d3de5ce7002dcd9454b45a78d5592ee369c4d7561fa5e5ee"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签署消息" id="签署消息">签署消息<a class="index_header-anchor__Xqb+L" href="#签署消息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxStarknetProvider.signMessage(signerAddress, typedData, chain)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>signerAddress - string, 钱包地址</li>
<li>typedData - object 需要签名的消息，按照固定格式签名</li>
<li>chain? - string, 请求执行方法的链</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - [string, string] 签名结果r, v</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"starknet:mainnet"</span>
<span class="token keyword">let</span> address <span class="token operator">=</span> okxStarknetProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"starknet:mainnet"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address
<span class="token keyword">const</span> signData <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"domain"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"chainId"</span><span class="token operator">:</span> <span class="token string">"0x534e5f4d41494e"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"STRKFarm"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"version"</span><span class="token operator">:</span> <span class="token string">"1"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string-property property">"message"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"document"</span><span class="token operator">:</span> <span class="token string">"app.strkfarm.xyz/tnc/v1"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"message"</span><span class="token operator">:</span> <span class="token string">"Read and Agree T&amp;C"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string-property property">"primaryType"</span><span class="token operator">:</span> <span class="token string">"Tnc"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"types"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"StarkNetDomain"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"name"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"version"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"chainId"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string-property property">"Tnc"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"message"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"document"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"felt"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> okxStarknetProvider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>address<span class="token punctuation">,</span> signData <span class="token punctuation">,</span>chain<span class="token punctuation">)</span>
<span class="token comment">//返回:0x07fcd65fded07c7daaa79a818a39c5236562914a5d48fa7fad268fac609faa9a,0x0324c3bafc4d0e7e04a3a0b805bf8438f5111e308c4d596daa46fc213b37ebf1</span>
</code></pre></div>
<h2 data-content="签署交易并广播上链 sendTransaction" id="签署交易并广播上链-sendtransaction">签署交易并广播上链 sendTransaction<a class="index_header-anchor__Xqb+L" href="#签署交易并广播上链-sendtransaction" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxStarknetProvider.sendTransaction(signerAddress, transaction, chainId?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>signerAddress - string,钱包地址</li>
<li>transaction - object，交易信息 按照固定格式签名</li>
<li>chainId? - string, 请求签名执行的链</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 交易hash</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> val <span class="token operator">=</span> uint256<span class="token punctuation">.</span><span class="token function">bnToUint256</span><span class="token punctuation">(</span><span class="token number">120000000000000000</span><span class="token punctuation">)</span>
<span class="token keyword">const</span> transferCalldata <span class="token operator">=</span> CallData<span class="token punctuation">.</span><span class="token function">compile</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    to<span class="token operator">:</span> <span class="token string">"0x00b909cefa36ab6bc26f5887a867e46ef162238f0a171b1c2974b665afd4237f"</span><span class="token punctuation">,</span>
    value<span class="token operator">:</span> val
<span class="token punctuation">}</span><span class="token punctuation">)</span>

<span class="token keyword">const</span> DAITokenAddress <span class="token operator">=</span> <span class="token string">"0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3"</span>

<span class="token keyword">const</span> invokeParams <span class="token operator">=</span> <span class="token punctuation">{</span>
    calls<span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            contract_address<span class="token operator">:</span> DAITokenAddress<span class="token punctuation">,</span>
            entry_point<span class="token operator">:</span> <span class="token string">"transfer"</span><span class="token punctuation">,</span>
            calldata<span class="token operator">:</span> transferCalldata
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token keyword">let</span> okxStarknetProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXStarknetProvider</span><span class="token punctuation">(</span>window<span class="token punctuation">.</span>provider<span class="token punctuation">)</span>
<span class="token keyword">let</span> address <span class="token operator">=</span> okxStarknetProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"starknet:mainnet"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address
<span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">sendTransaction</span><span class="token punctuation">(</span> <span class="token keyword">this</span><span class="token punctuation">.</span>address<span class="token punctuation">,</span> invokeParams<span class="token punctuation">,</span> <span class="token string">"starknet:mainnet"</span><span class="token punctuation">)</span>
<span class="token comment">//返回值：0x515d9de049c43477cee7eaea987ab04995d8dc2a7b3d7a184dca4bcd7224ec2</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包，并删除当前会话，如果要切换钱包，请先断开当前钱包后重新连接</p>
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
    "Starknet",
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
    "Cosmos 系/Sei",
    "Tron",
    "Starknet",
    "SDK",
    "UI",
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
    "准备交易",
    "获取账户信息",
    "签署消息",
    "签署交易并广播上链 sendTransaction",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
