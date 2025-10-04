# SDK | Sui | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-sui-sdk#签名personalmessage  
**抓取时间:** 2025-05-27 07:33:25  
**字数:** 720

## 导航路径
DApp 连接钱包 > Sui > SDK

## 目录
- 安装及初始化
- 连接钱包
- 判断钱包是否已连接
- 断开连接
- 准备交易
- 获取账户信息
- 签名Message
- 签名PersonalMessage
- 签交易
- 签交易并广播上链
- Event事件
- 错误码

---

SDK
#
Sui 又称 Sui Network，是第一个从零开始设计，且能够使开发者为十亿 Web3 新用户构建全新体验的 Layer 1 区块链。Sui 可横向扩展，能够高速且低成本地支持多样的 DApp 开发。Sui 开创了通用区块链的先河，为用户带来高吞吐量、超快结算速度、丰富的链上资产、以及用户友好的 Web3 体验。Sui 是区块链技术的一个跨越式的进步，从底层开始设计，以满足加密货币中所有相关方的需求。
安装及初始化
#
请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：
将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/sui-provider
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
const
okxUniversalProvider
=
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
okxUniversalProvider.connect(connectParams: ConnectParams);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Sui系的key为"sui"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，Sui系的key为"sui"
，如果对应的链信息钱包不支持，依然可以连接
chains: string[]; 链id信息
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
sui
:
{
chains
:
[
"sui:mainnet"
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
获取当前是否有连接钱包
返回值
boolean
示例
okxUniversalProvider
.
connected
(
)
断开连接
#
断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包。
示例
okxUniversalProvider
.
disconnect
(
)
准备交易
#
向钱包发送消息的方法，支持签名，交易
首先创建一个OKXSuiProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXSuiProvider
}
from
"@okxconnect/sui-provider"
let
suiProvider
=
new
OKXSuiProvider
(
okxUniversalProvider
)
获取账户信息
#
suiProvider.getAccount();
返回值
Object
address: string 钱包地址
publicKey: string 公钥（需要App 6.92.0以后版本支持）
示例
let
result
=
suiProvider
.
getAccount
(
)
//返回结构
{
"address"
:
"0x7995ca23961fe06d8cea7da58ca751567ce820d7cba77b4a373249034eecca4a"
,
"publicKey"
:
"tUvCYrG22rHKR0c306MxgnhXOSf16Ot6H3GMO7btwDI="
,
}
签名Message
#
suiProvider
.
signMessage
(
input
:
SuiSignMessageInput
)
;
请求参数
SuiSignMessageInput - object
message: Uint8Array
返回值
Promise - object
messageBytes: string
signature: string
签名PersonalMessage
#
suiProvider
.
signPersonalMessage
(
input
:
SuiSignMessageInput
)
;
请求参数
SuiSignMessageInput - object
message: Uint8Array
返回值
Promise - object
bytes: string
signature: string
示例
const
data
=
[
76
,
111
,
103
,
105
,
110
,
32
,
119
,
105
,
116
,
104
,
32
,
66
,
108
,
117
,
101
,
109
,
111
,
118
,
101
]
;
const
uint8Array
=
new
Uint8Array
(
data
)
;
let
input
=
{
message
:
uint8Array
}
let
signResult1
=
await
suiProvider
.
signMessage
(
input
)
let
signResult2
=
await
suiProvider
.
signPersonalMessage
(
input
)
签交易
#
suiProvider
.
signTransaction
(
input
)
请求参数
// txBytes与txSerialize为transactionBlock的序列化
// 和transactionBlock传入一种即可无需同时传入
interface
SuiSignTransactionBlockInput
{
transactionBlock
:
TransactionBlock
;
chain
:
IdentifierString
;
txBytes
:
string
?
;
txSerialize
:
string
?
}
返回值
Promise - object
signature: string,
transactionBlockBytes: string
签交易并广播上链
#
suiProvider
.
signAndExecuteTransaction
(
input
)
请求参数
// txBytes与txSerialize为transactionBlock的序列化
// 和transactionBlock传入一种即可无需同时传入
interface
SuiSignTransactionBlockInput
{
transactionBlock
:
TransactionBlock
;
chain
:
IdentifierString
;
txBytes
:
string
?
;
txSerialize
:
string
?
;
}
返回值
Promise - object
confirmedLocalExecution: bool,
digest: string,
txBytes: string
示例
// 定义要转移的金额和目标地址
const
amount
=
109
;
// 需要转移的金额
const
recipientAddress
=
'0x'
;
// 目标地址
/// 构造一个转账的交易
const
tx
=
new
Transaction
(
)
;
const
[
coin
]
=
tx
.
splitCoins
(
tx
.
gas
,
[
amount
]
)
;
tx
.
transferObjects
(
[
coin
]
,
recipientAddress
)
const
input
=
{
transactionBlock
:
tx
,
chain
:
'sui:mainnet'
,
options
:
{
showEffects
:
true
,
}
}
let
signResult1
=
await
suiProvider
.
signTransaction
(
input
)
let
signResult2
=
await
suiProvider
.
signAndExecuteTransaction
(
input
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
<p>Sui 又称 Sui Network，是第一个从零开始设计，且能够使开发者为十亿 Web3 新用户构建全新体验的 Layer 1 区块链。Sui 可横向扩展，能够高速且低成本地支持多样的 DApp 开发。Sui 开创了通用区块链的先河，为用户带来高吞吐量、超快结算速度、丰富的链上资产、以及用户友好的 Web3 体验。Sui 是区块链技术的一个跨越式的进步，从底层开始设计，以满足加密货币中所有相关方的需求。</p>
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：</p>
<p>将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/sui-provider</code></pre></div>
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
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXUniversalProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span>
<span class="token keyword">const</span> okxUniversalProvider <span class="token operator">=</span> OKXUniversalProvider<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>dappMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        name<span class="token operator">:</span> <span class="token string">"application name"</span><span class="token punctuation">,</span>
        icon<span class="token operator">:</span> <span class="token string">"application icon url"</span>
    <span class="token punctuation">}</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包去获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<p><code>okxUniversalProvider.connect(connectParams: ConnectParams);</code></p>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Sui系的key为"sui"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， EVM系的key为"eip155"，Sui系的key为"sui"
，如果对应的链信息钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
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
        sui<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"sui:mainnet"</span><span class="token punctuation">]</span>
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
<h2 data-content="断开连接" id="断开连接">断开连接<a class="index_header-anchor__Xqb+L" href="#断开连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包。</p>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="准备交易" id="准备交易">准备交易<a class="index_header-anchor__Xqb+L" href="#准备交易" style="opacity:0">#</a></h2>
<p>向钱包发送消息的方法，支持签名，交易</p>
<p>首先创建一个OKXSuiProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXSuiProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/sui-provider"</span>
<span class="token keyword">let</span> suiProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXSuiProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>

</code></pre></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">suiProvider.getAccount();</code></pre></div>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址</li>
<li>publicKey: string 公钥（需要App 6.92.0以后版本支持）</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> result <span class="token operator">=</span> suiProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

<span class="token comment">//返回结构</span>
<span class="token punctuation">{</span>
    <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0x7995ca23961fe06d8cea7da58ca751567ce820d7cba77b4a373249034eecca4a"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"tUvCYrG22rHKR0c306MxgnhXOSf16Ot6H3GMO7btwDI="</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

</code></pre></div>
<h2 data-content="签名Message" id="签名message">签名Message<a class="index_header-anchor__Xqb+L" href="#签名message" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiProvider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>input<span class="token operator">:</span> SuiSignMessageInput<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>SuiSignMessageInput - object<!-- -->
<ul>
<li>message: Uint8Array</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>messageBytes: string</li>
<li>signature: string</li>
</ul>
</li>
</ul>
<h2 data-content="签名PersonalMessage" id="签名personalmessage">签名PersonalMessage<a class="index_header-anchor__Xqb+L" href="#签名personalmessage" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiProvider<span class="token punctuation">.</span><span class="token function">signPersonalMessage</span><span class="token punctuation">(</span>input<span class="token operator">:</span> SuiSignMessageInput<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>SuiSignMessageInput - object<!-- -->
<ul>
<li>message: Uint8Array</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>bytes: string</li>
<li>signature: string</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token number">76</span><span class="token punctuation">,</span> <span class="token number">111</span><span class="token punctuation">,</span> <span class="token number">103</span><span class="token punctuation">,</span> <span class="token number">105</span><span class="token punctuation">,</span> <span class="token number">110</span><span class="token punctuation">,</span> <span class="token number">32</span><span class="token punctuation">,</span> <span class="token number">119</span><span class="token punctuation">,</span> <span class="token number">105</span><span class="token punctuation">,</span> <span class="token number">116</span><span class="token punctuation">,</span> <span class="token number">104</span><span class="token punctuation">,</span> <span class="token number">32</span><span class="token punctuation">,</span> <span class="token number">66</span><span class="token punctuation">,</span> <span class="token number">108</span><span class="token punctuation">,</span> <span class="token number">117</span><span class="token punctuation">,</span> <span class="token number">101</span><span class="token punctuation">,</span> <span class="token number">109</span><span class="token punctuation">,</span> <span class="token number">111</span><span class="token punctuation">,</span> <span class="token number">118</span><span class="token punctuation">,</span> <span class="token number">101</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> uint8Array <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Uint8Array</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> input <span class="token operator">=</span> <span class="token punctuation">{</span>
    message<span class="token operator">:</span> uint8Array
<span class="token punctuation">}</span>
<span class="token keyword">let</span> signResult1 <span class="token operator">=</span> <span class="token keyword">await</span> suiProvider<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>
<span class="token keyword">let</span> signResult2 <span class="token operator">=</span> <span class="token keyword">await</span> suiProvider<span class="token punctuation">.</span><span class="token function">signPersonalMessage</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>

</code></pre></div>
<h2 data-content="签交易" id="签交易">签交易<a class="index_header-anchor__Xqb+L" href="#签交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiProvider<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>
</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// txBytes与txSerialize为transactionBlock的序列化</span>
<span class="token comment">// 和transactionBlock传入一种即可无需同时传入</span>
<span class="token keyword">interface</span> <span class="token class-name">SuiSignTransactionBlockInput</span> <span class="token punctuation">{</span>
    transactionBlock<span class="token operator">:</span> TransactionBlock<span class="token punctuation">;</span>
    chain<span class="token operator">:</span> IdentifierString<span class="token punctuation">;</span>
    txBytes<span class="token operator">:</span> <span class="token builtin">string</span><span class="token operator">?</span><span class="token punctuation">;</span>
    txSerialize<span class="token operator">:</span> <span class="token builtin">string</span><span class="token operator">?</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>signature: string,</li>
<li>transactionBlockBytes: string</li>
</ul>
</li>
</ul>
<h2 data-content="签交易并广播上链" id="签交易并广播上链">签交易并广播上链<a class="index_header-anchor__Xqb+L" href="#签交易并广播上链" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiProvider<span class="token punctuation">.</span><span class="token function">signAndExecuteTransaction</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>
</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// txBytes与txSerialize为transactionBlock的序列化</span>
<span class="token comment">// 和transactionBlock传入一种即可无需同时传入</span>
<span class="token keyword">interface</span> <span class="token class-name">SuiSignTransactionBlockInput</span> <span class="token punctuation">{</span>
    transactionBlock<span class="token operator">:</span> TransactionBlock<span class="token punctuation">;</span>
    chain<span class="token operator">:</span> IdentifierString<span class="token punctuation">;</span>
    txBytes<span class="token operator">:</span> <span class="token builtin">string</span><span class="token operator">?</span><span class="token punctuation">;</span>
    txSerialize<span class="token operator">:</span> <span class="token builtin">string</span><span class="token operator">?</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>confirmedLocalExecution: bool,</li>
<li>digest: string,</li>
<li>txBytes: string</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 定义要转移的金额和目标地址</span>
<span class="token keyword">const</span> amount <span class="token operator">=</span> <span class="token number">109</span><span class="token punctuation">;</span> <span class="token comment">// 需要转移的金额</span>
<span class="token keyword">const</span> recipientAddress <span class="token operator">=</span> <span class="token string">'0x'</span><span class="token punctuation">;</span> <span class="token comment">// 目标地址</span>

<span class="token comment">/// 构造一个转账的交易</span>
<span class="token keyword">const</span> tx <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Transaction</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">[</span>coin<span class="token punctuation">]</span> <span class="token operator">=</span> tx<span class="token punctuation">.</span><span class="token function">splitCoins</span><span class="token punctuation">(</span>tx<span class="token punctuation">.</span>gas<span class="token punctuation">,</span> <span class="token punctuation">[</span>amount<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
tx<span class="token punctuation">.</span><span class="token function">transferObjects</span><span class="token punctuation">(</span><span class="token punctuation">[</span>coin<span class="token punctuation">]</span><span class="token punctuation">,</span> recipientAddress<span class="token punctuation">)</span>
<span class="token keyword">const</span> input <span class="token operator">=</span> <span class="token punctuation">{</span>
    transactionBlock<span class="token operator">:</span> tx<span class="token punctuation">,</span>
    chain<span class="token operator">:</span> <span class="token string">'sui:mainnet'</span><span class="token punctuation">,</span>
    options<span class="token operator">:</span> <span class="token punctuation">{</span>
        showEffects<span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token keyword">let</span> signResult1 <span class="token operator">=</span> <span class="token keyword">await</span> suiProvider<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>
<span class="token keyword">let</span> signResult2 <span class="token operator">=</span> <span class="token keyword">await</span> suiProvider<span class="token punctuation">.</span><span class="token function">signAndExecuteTransaction</span><span class="token punctuation">(</span>input<span class="token punctuation">)</span>

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
    "Sui",
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
    "SDK",
    "UI",
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
    "断开连接",
    "准备交易",
    "获取账户信息",
    "签名Message",
    "签名PersonalMessage",
    "签交易",
    "签交易并广播上链",
    "Event事件",
    "错误码"
  ]
}
```

</details>
