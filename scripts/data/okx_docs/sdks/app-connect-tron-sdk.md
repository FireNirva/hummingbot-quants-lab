# SDK | Tron | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-tron-sdk#sdk  
**抓取时间:** 2025-05-27 07:03:09  
**字数:** 683

## 导航路径
DApp 连接钱包 > Tron > SDK

## 目录
- 安装及初始化
- 连接钱包
- 准备交易
- 获取账户信息
- 签署消息
- 签署消息V2
- 签署交易 signTransaction
- 签署交易并广播上链 signAndSendTransaction
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
安装及初始化
#
请确保更新到 6.96.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/universal-provider
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
,
}
)
连接钱包
#
连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数;
okxUniversalProvider.connect(connectParams: ConnectParams);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， TRON的key为"tron"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， TRON的key为"tron"，如果对应的链信息钱包不支持，依然可以连接；
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
tron
:
{
chains
:
[
"tron:mainnet"
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
首先创建一个OKXTronProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXTronProvider
}
from
"@okxconnect/universal-provider"
;
let
okxTronProvider
=
new
OKXTronProvider
(
okxUniversalProvider
)
获取账户信息
#
okxTronProvider.getAccount(chainId?)
请求参数
chainId: 请求的链，如tron:mainnet
返回值
Object
address: string 钱包地址
示例
let
result
=
okxTronProvider
.
getAccount
(
"tron:mainnet"
)
//返回结构
{
"address"
:
"THyDJCGXYnwCSYNQeGYW98pptEVSHwaYx7"
}
签署消息
#
okxTronProvider.signMessage(message, chainId?)
请求参数
message - string 需要签名的消息。
chainId? - string, 请求执行方法的链,如tron:mainnet
返回值
Promise - string 签名结果
示例
let
chainId
=
"tron:mainnet"
let
signStr
=
"data need to sign ..."
let
result
=
okxTronProvider
.
signMessage
(
signStr
,
chainId
)
//返回:0xfc9003b1c8e68fdc93409aad911af274de1987130a36516f1c7c9353716463bf42bb400e0d6bffd4adface92dd3a01079ba32f8aebe3db1d5914f084b9f802711c
签署消息V2
#
okxTronProvider.signMessageV2(message, chainId?)
请求参数
message - string 需要签名的消息。
chainId - string, 请求执行方法的链, 如tron:mainnet
返回值
Promise - string 签名结果
示例
let
chainId
=
"tron:mainnet"
let
signStr
=
"data need to sign ..."
let
result
=
okxTronProvider
.
signMessageV2
(
signStr
,
chainId
)
//返回:0xfc9003b1c8e68fdc93409aad911af274de1987130a36516f1c7c9353716463bf42bb400e0d6bffd4adface92dd3a01079ba32f8aebe3db1d5914f084b9f802711c
签署交易 signTransaction
#
okxTronProvider.signTransaction(transaction: any, chainId?: string)
请求参数
transaction - object，交易信息 按照固定格式签名，可通过TronWeb.transactionBuilder生成
chainId? - string, 请求签名执行的链，非必传参数, 如tron:mainnet
返回值
Promise - Object 签名后的交易
示例
let
tronWeb
=
new
TronWeb
(
{
"fullHost"
:
'https://api.trongrid.io'
,
"headers"
:
{
}
,
"privateKey"
:
''
}
)
let
address
=
okxTronProvider
.
getAccount
(
"tron:mainnet"
)
.
address
const
transaction
=
await
tronWeb
.
transactionBuilder
.
sendTrx
(
"TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"
,
1000
,
address
)
;
let
res
=
await
okxTronProvider
.
signTransaction
(
transaction
,
"tron:mainnet"
)
/**返回结果
{
"visible": true,
 "txID": "cf93bbfb0152d832fcdb1c65cb12a979eab5a631de1b3d7d6437757e1b16ed40",
 "raw_data":
{
"contract": [
{
"parameter":
{
"type_url": "type.googleapis.com/protocol.TransferContract",
 "value":
{
"amount": 1000,
 "contract_address": "",
 "owner_address": "THyDJCGXYnwCSYNQeGYW98pptEVSHwaYx7",
 "to_address": "TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"
}
}
,
 "type": "TransferContract"
}
],
 "expiration": 1732073850000,
 "ref_block_bytes": "7ecf",
 "ref_block_hash": "7b3a6bc87d9edb9e",
 "timestamp": 1732073790000
}
,
 "raw_data_hex": "0a027ecf22087b3a6bc87d9edb9e40908996bdb4325a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a154157c140be01fa2bbabf7f055ab879d0c05725293c12154144295a45f811a9d595562562a2e27685291a715818e80770b0b492bdb432",
 "signature": ["239b402a7605199c6969f6f4da37a355452bd942c222adfc625721d18a1fff3223f92c1d8eaf5856c0e41ce80761fd2adb80d026276d6710ad183a713af7a78d00"]
}
*/
签署交易并广播上链 signAndSendTransaction
#
okxTronProvider.signAndSendTransaction(transaction, chainId?)
请求参数
transaction - object，交易信息 按照固定格式签名，可通过TronWeb.transactionBuilder生成
chainId - string, 请求签名执行的链，非必传参数，如tron:mainnet
返回值
Promise - string 交易hash
示例
let
tronWeb
=
new
TronWeb
(
{
"fullHost"
:
'https://api.trongrid.io'
,
"headers"
:
{
}
,
"privateKey"
:
''
}
)
let
address
=
okxTronProvider
.
getAccount
(
"tron:mainnet"
)
.
address
const
transaction
=
await
tronWeb
.
transactionBuilder
.
sendTrx
(
"TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"
,
1000
,
address
)
;
//转账TRX
let
res
=
await
okxTronProvider
.
signAndSendTransaction
(
transaction
,
"tron:mainnet"
)
//返回值：50a47e450024c079510a39433e28de0bcac8406d731aadab7d772998dfce2aab
断开钱包连接
#
断开已连接钱包，并删除当前会话，如果要切换连接钱包，请先断开当前钱包
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
<p>请确保更新到 6.96.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/universal-provider</code></pre></div>
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
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数;</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalProvider.connect(connectParams: ConnectParams);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， TRON的key为"tron"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， TRON的key为"tron"，如果对应的链信息钱包不支持，依然可以连接；<!-- -->
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
<li>redirect?:string, 连接成功后的跳转参数
<strong>示例</strong></li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> okxUniversalProvider<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
        tron<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token string">"tron:mainnet"</span><span class="token punctuation">,</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>首先创建一个OKXTronProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXTronProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxTronProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXTronProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxTronProvider.getAccount(chainId?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId: 请求的链，如tron:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> result <span class="token operator">=</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"tron:mainnet"</span><span class="token punctuation">)</span>
<span class="token comment">//返回结构</span>
<span class="token punctuation">{</span>
    <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"THyDJCGXYnwCSYNQeGYW98pptEVSHwaYx7"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签署消息" id="签署消息">签署消息<a class="index_header-anchor__Xqb+L" href="#签署消息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxTronProvider.signMessage(message, chainId?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>message - string 需要签名的消息。</li>
<li>chainId? - string, 请求执行方法的链,如tron:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 签名结果</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chainId <span class="token operator">=</span> <span class="token string">"tron:mainnet"</span>
<span class="token keyword">let</span> signStr <span class="token operator">=</span> <span class="token string">"data need to sign ..."</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>signStr<span class="token punctuation">,</span> chainId<span class="token punctuation">)</span>
<span class="token comment">//返回:0xfc9003b1c8e68fdc93409aad911af274de1987130a36516f1c7c9353716463bf42bb400e0d6bffd4adface92dd3a01079ba32f8aebe3db1d5914f084b9f802711c</span>
</code></pre></div>
<h2 data-content="签署消息V2" id="签署消息v2">签署消息V2<a class="index_header-anchor__Xqb+L" href="#签署消息v2" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxTronProvider.signMessageV2(message, chainId?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>message - string 需要签名的消息。</li>
<li>chainId - string, 请求执行方法的链, 如tron:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 签名结果</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chainId <span class="token operator">=</span> <span class="token string">"tron:mainnet"</span>
<span class="token keyword">let</span> signStr <span class="token operator">=</span> <span class="token string">"data need to sign ..."</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">signMessageV2</span><span class="token punctuation">(</span>signStr<span class="token punctuation">,</span> chainId<span class="token punctuation">)</span>
<span class="token comment">//返回:0xfc9003b1c8e68fdc93409aad911af274de1987130a36516f1c7c9353716463bf42bb400e0d6bffd4adface92dd3a01079ba32f8aebe3db1d5914f084b9f802711c</span>
</code></pre></div>
<h2 data-content="签署交易 signTransaction" id="签署交易-signtransaction">签署交易 signTransaction<a class="index_header-anchor__Xqb+L" href="#签署交易-signtransaction" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxTronProvider.signTransaction(transaction: any, chainId?: string)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>
<p>transaction - object，交易信息 按照固定格式签名，可通过TronWeb.transactionBuilder生成</p>
</li>
<li>
<p>chainId? - string, 请求签名执行的链，非必传参数, 如tron:mainnet
<em><strong>返回值</strong></em></p>
</li>
<li>
<p>Promise - Object 签名后的交易</p>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> tronWeb <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TronWeb</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token string-property property">"fullHost"</span><span class="token operator">:</span> <span class="token string">'https://api.trongrid.io'</span><span class="token punctuation">,</span>
    <span class="token string-property property">"headers"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string-property property">"privateKey"</span><span class="token operator">:</span> <span class="token string">''</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token keyword">let</span> address <span class="token operator">=</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"tron:mainnet"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">await</span> tronWeb<span class="token punctuation">.</span>transactionBuilder<span class="token punctuation">.</span><span class="token function">sendTrx</span><span class="token punctuation">(</span><span class="token string">"TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"</span><span class="token punctuation">,</span> <span class="token number">1000</span><span class="token punctuation">,</span> address<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">,</span><span class="token string">"tron:mainnet"</span><span class="token punctuation">)</span>

<span class="token doc-comment comment">/**返回结果
 <span class="token punctuation">{</span>
 "visible": true,
 "txID": "cf93bbfb0152d832fcdb1c65cb12a979eab5a631de1b3d7d6437757e1b16ed40",
 "raw_data": <span class="token punctuation">{</span>
 "contract": [<span class="token punctuation">{</span>
 "parameter": <span class="token punctuation">{</span>
 "type_url": "type.googleapis.com/protocol.TransferContract",
 "value": <span class="token punctuation">{</span>
 "amount": 1000,
 "contract_address": "",
 "owner_address": "THyDJCGXYnwCSYNQeGYW98pptEVSHwaYx7",
 "to_address": "TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"
 <span class="token punctuation">}</span>
 <span class="token punctuation">}</span>,
 "type": "TransferContract"
 <span class="token punctuation">}</span>],
 "expiration": 1732073850000,
 "ref_block_bytes": "7ecf",
 "ref_block_hash": "7b3a6bc87d9edb9e",
 "timestamp": 1732073790000
 <span class="token punctuation">}</span>,
 "raw_data_hex": "0a027ecf22087b3a6bc87d9edb9e40908996bdb4325a66080112620a2d747970652e676f6f676c65617069732e636f6d2f70726f746f636f6c2e5472616e73666572436f6e747261637412310a154157c140be01fa2bbabf7f055ab879d0c05725293c12154144295a45f811a9d595562562a2e27685291a715818e80770b0b492bdb432",
 "signature": ["239b402a7605199c6969f6f4da37a355452bd942c222adfc625721d18a1fff3223f92c1d8eaf5856c0e41ce80761fd2adb80d026276d6710ad183a713af7a78d00"]
 <span class="token punctuation">}</span>
 */</span>
</code></pre></div>
<h2 data-content="签署交易并广播上链 signAndSendTransaction" id="签署交易并广播上链-signandsendtransaction">签署交易并广播上链 signAndSendTransaction<a class="index_header-anchor__Xqb+L" href="#签署交易并广播上链-signandsendtransaction" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxTronProvider.signAndSendTransaction(transaction, chainId?)</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>transaction - object，交易信息 按照固定格式签名，可通过TronWeb.transactionBuilder生成</li>
<li>chainId - string, 请求签名执行的链，非必传参数，如tron:mainnet</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - string 交易hash</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> tronWeb <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TronWeb</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token string-property property">"fullHost"</span><span class="token operator">:</span> <span class="token string">'https://api.trongrid.io'</span><span class="token punctuation">,</span>
    <span class="token string-property property">"headers"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string-property property">"privateKey"</span><span class="token operator">:</span> <span class="token string">''</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token keyword">let</span> address <span class="token operator">=</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"tron:mainnet"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">await</span> tronWeb<span class="token punctuation">.</span>transactionBuilder<span class="token punctuation">.</span><span class="token function">sendTrx</span><span class="token punctuation">(</span><span class="token string">"TGBcVLMnVtvJzjPWZpPiYBgwwb7th1w3BF"</span><span class="token punctuation">,</span> <span class="token number">1000</span><span class="token punctuation">,</span> address<span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">//转账TRX</span>
<span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxTronProvider<span class="token punctuation">.</span><span class="token function">signAndSendTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">,</span> <span class="token string">"tron:mainnet"</span><span class="token punctuation">)</span>
<span class="token comment">//返回值：50a47e450024c079510a39433e28de0bcac8406d731aadab7d772998dfce2aab</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包，并删除当前会话，如果要切换连接钱包，请先断开当前钱包</p>
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
    "Tron",
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
    "SDK",
    "UI",
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
    "准备交易",
    "获取账户信息",
    "签署消息",
    "签署消息V2",
    "签署交易 signTransaction",
    "签署交易并广播上链 signAndSendTransaction",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
