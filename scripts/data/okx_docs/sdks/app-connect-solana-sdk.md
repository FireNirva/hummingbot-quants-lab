# SDK | Solana兼容链 | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-solana-sdk#签一笔交易并广播上链  
**抓取时间:** 2025-05-27 07:31:09  
**字数:** 576

## 导航路径
DApp 连接钱包 > Solana兼容链 > SDK

## 目录
- 安装及初始化
- 连接钱包
- 判断钱包是否已连接
- 准备交易
- 签名
- 签单笔交易
- 签多笔交易
- 签一笔交易并广播上链
- 获取钱包地址及PublicKey
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
Solana 是一种高性能的区块链平台，致力于为去中心化应用和加密货币提供快速、安全和可扩展的解决方案。该平台采用了创新的共识算法——Proof of History (PoH)，可以处理高达数万笔交易每秒 (TPS)，同时保持了去中心化和安全性。总的来说，Solana 的目标是通过其独特的技术优势，实现区块链的大规模采用，服务于各种复杂的去中心化应用和全球金融系统。
Sonic是为在Solana上实现主权游戏经济而构建的首个原子SVM链。
安装及初始化
#
请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：
将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/solana-provider
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
连接钱包获取钱包地址，作为标识符和用于签名交易的必要参数
okxUniversalProvider.connect(connectParams: ConnectParams);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接
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
solana
:
{
chains
:
[
"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"
,
// solana mainnet
// "sonic:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",// sonic mainnet
// "solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// solana testnet
// "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet
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
向钱包发送消息的方法，支持签名，交易
首先创建一个OKXSolanaProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXSolanaProvider
}
from
"@okxconnect/solana-provider"
;
let
okxSolanaProvider
=
new
OKXSolanaProvider
(
okxUniversalProvider
)
签名
#
okxSolanaProvider.signMessage(message, chain)
请求参数
message - string 需要签名的消息
chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链
返回值
Promise - object
publicKey:string 钱包地址
signature:Uint8Array 签名结果
签单笔交易
#
okxSolanaProvider.signTransaction(transaction, chain)
请求参数
transaction - Transaction | VersionedTransaction 交易数据对象
chain: string, 请求签名执行的链，建议传递此参，连接多条链时为必传参数，连接单条链时则默认为当前链
返回值
Promise - Transaction | VersionedTransaction 签名后的交易对象
签多笔交易
#
okxSolanaProvider.signAllTransactions(transactions, chain)
请求参数
transactions - [Transaction | VersionedTransaction] 交易数据对象数组
chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链
返回值
Promise - [Transaction | VersionedTransaction] 签名后的交易对象数组
签一笔交易并广播上链
#
okxSolanaProvider.signAndSendTransaction(transaction, chain)
请求参数
transactions - Transaction | VersionedTransaction 交易数据对象
chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链
返回值
Promise - string 交易hash
获取钱包地址及PublicKey
#
okxSolanaProvider.getAccount(chain)
请求参数
chain: string, 获取钱包地址的链id，不传则默认取第一个连接的svm地址
返回值
Object
address: string 钱包地址
publicKey: PublicKey
示例
//在solana mainnet上签名一笔转账交易
let
provider
=
new
OKXSolanaProvider
(
okxUniversalProvider
)
const
transaction
=
new
Transaction
(
{
feePayer
:
new
PublicKey
(
provider
.
getAccount
(
)
.
address
)
,
recentBlockhash
:
"xNWbUfdEPktMsZQHY6Zk5RJqamWFcTKasekjr7c3wFX"
,
}
)
.
add
(
SystemProgram
.
transfer
(
{
fromPubkey
:
new
PublicKey
(
provider
.
getAccount
(
)
.
address
)
,
toPubkey
:
new
PublicKey
(
provider
.
getAccount
(
)
.
address
)
,
lamports
:
1000
,
}
)
)
let
result
=
await
provider
.
signTransaction
(
transaction
,
"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"
)
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
<p>Solana 是一种高性能的区块链平台，致力于为去中心化应用和加密货币提供快速、安全和可扩展的解决方案。该平台采用了创新的共识算法——Proof of History (PoH)，可以处理高达数万笔交易每秒 (TPS)，同时保持了去中心化和安全性。总的来说，Solana 的目标是通过其独特的技术优势，实现区块链的大规模采用，服务于各种复杂的去中心化应用和全球金融系统。</p>
<p>Sonic是为在Solana上实现主权游戏经济而构建的首个原子SVM链。</p>
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：</p>
<p>将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/solana-provider</code></pre></div>
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
<p>连接钱包获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxUniversalProvider.connect(connectParams: ConnectParams);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接</li>
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
        solana<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"</span><span class="token punctuation">,</span> <span class="token comment">// solana mainnet</span>
            <span class="token comment">//  "sonic:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",// sonic mainnet</span>
            <span class="token comment">//  "solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// solana testnet</span>
            <span class="token comment">//  "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet</span>
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
<p>向钱包发送消息的方法，支持签名，交易</p>
<p>首先创建一个OKXSolanaProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXSolanaProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/solana-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxSolanaProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXSolanaProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="签名" id="签名">签名<a class="index_header-anchor__Xqb+L" href="#签名" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.signMessage(message, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>message - string 需要签名的消息</li>
<li>chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>publicKey:string 钱包地址</li>
<li>signature:Uint8Array 签名结果</li>
</ul>
</li>
</ul>
<h2 data-content="签单笔交易" id="签单笔交易">签单笔交易<a class="index_header-anchor__Xqb+L" href="#签单笔交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.signTransaction(transaction, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transaction - Transaction | VersionedTransaction 交易数据对象</li>
<li>chain: string, 请求签名执行的链，建议传递此参，连接多条链时为必传参数，连接单条链时则默认为当前链</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - Transaction | VersionedTransaction 签名后的交易对象</li>
</ul>
<h2 data-content="签多笔交易" id="签多笔交易">签多笔交易<a class="index_header-anchor__Xqb+L" href="#签多笔交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.signAllTransactions(transactions, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transactions - [Transaction | VersionedTransaction] 交易数据对象数组</li>
<li>chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - [Transaction | VersionedTransaction] 签名后的交易对象数组</li>
</ul>
<h2 data-content="签一笔交易并广播上链" id="签一笔交易并广播上链">签一笔交易并广播上链<a class="index_header-anchor__Xqb+L" href="#签一笔交易并广播上链" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.signAndSendTransaction(transaction, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transactions - Transaction | VersionedTransaction 交易数据对象</li>
<li>chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string 交易hash</li>
</ul>
<h2 data-content="获取钱包地址及PublicKey" id="获取钱包地址及publickey">获取钱包地址及PublicKey<a class="index_header-anchor__Xqb+L" href="#获取钱包地址及publickey" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.getAccount(chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>chain: string, 获取钱包地址的链id，不传则默认取第一个连接的svm地址</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Object<!-- -->
<ul>
<li>address: string 钱包地址</li>
<li>publicKey: PublicKey</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">//在solana mainnet上签名一笔转账交易</span>
<span class="token keyword">let</span> provider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXSolanaProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Transaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    feePayer<span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>provider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address<span class="token punctuation">)</span><span class="token punctuation">,</span>
    recentBlockhash<span class="token operator">:</span> <span class="token string">"xNWbUfdEPktMsZQHY6Zk5RJqamWFcTKasekjr7c3wFX"</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">add</span><span class="token punctuation">(</span>SystemProgram<span class="token punctuation">.</span><span class="token function">transfer</span><span class="token punctuation">(</span>
    <span class="token punctuation">{</span>
        fromPubkey<span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>provider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address<span class="token punctuation">)</span><span class="token punctuation">,</span>
        toPubkey<span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>provider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address<span class="token punctuation">)</span><span class="token punctuation">,</span>
        lamports<span class="token operator">:</span> <span class="token number">1000</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">)</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">,</span> <span class="token string">"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"</span><span class="token punctuation">)</span>
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
    "Solana兼容链",
    "SDK"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Solana 兼容链",
    "SDK",
    "UI",
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
    "签名",
    "签单笔交易",
    "签多笔交易",
    "签一笔交易并广播上链",
    "获取钱包地址及PublicKey",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
