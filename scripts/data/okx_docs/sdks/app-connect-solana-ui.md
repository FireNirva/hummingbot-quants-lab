# UI | Solana兼容链 | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-solana-ui#准备交易  
**抓取时间:** 2025-05-27 07:03:30  
**字数:** 780

## 导航路径
DApp 连接钱包 > Solana兼容链 > UI

## 目录
- 安装及初始化
- 连接钱包
- 连接钱包并签名
- 判断钱包是否已连接
- 准备交易
- 签名
- 签多笔交易
- 签一笔交易并广播上链
- 获取钱包账户信息
- 断开钱包连接
- Event事件
- 错误码

---

UI
#
在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运营在 Telegram内，则用户可以选择停留在Telegram并唤起移动端App钱包或者唤起欧易 Mini 钱包。
安装及初始化
#
请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：
将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
npm install @okxconnect/ui
npm install @okxconnect/solana-provider
连接钱包之前，需要先创建一个可以提供UI界面的对象，用于后续连接钱包、发送交易等操作。
OKXUniversalConnectUI.init(dappMetaData, actionsConfiguration, uiPreferences, language)
请求参数
dappMetaData - object
name - string: 应用名称，不会作为唯一表示
icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。
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
universalUi
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
// 切换插件连接钱包，会触发该事件；
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
连接钱包获取钱包地址，作为标识符和用于签名交易的必要参数
universalUi.openModal(connectParams: ConnectParams)
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
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
// "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet ；
]
,
}
}
}
)
连接钱包并签名
#
连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调
await universalUi.openModalAndSign(connectParams: ConnectParams,signRequest: RequestParams[]);
请求参数
connectParams - ConnectParams
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接
chains: string[]; 链id信息
defaultChain?: string; 默认链
signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法；
method: string; 请求的方法名称, Solana支持的方法有："solana_signMessage"
chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中
params: unknown[] | Record
<string, unknown>
| object | undefined; 请求的方法对应的参数
返回值
Promise
<SessionTypes.Struct | undefined>
topic: string; 会话标识
namespaces:
Record<string, Namespace>
; 成功连接的namespace 信息；
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
// "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet ；
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
chainId
:
"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"
,
method
:
"solana_signMessage"
,
params
:
{
message
:
"Hello Solana"
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
向钱包发送消息的方法，支持签名，交易
首先创建一个OKXSolanaProvider对象，构造函数传入OKXUniversalProviderUI，当调用 OKXSolanaProvider 相关的方法时，actionsConfiguration.mode 的配置会按照init 时候传递的值处理；
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
universalUi
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
okxSolanaProvider.signTransaction(transaction, chain)
请求参数
transaction - Transaction | VersionedTransaction 交易数据对象
chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链
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
获取钱包账户信息
#
okxSolanaProvider.getAccount(chain)
请求参数
chain: string, 获取钱包地址的链Id，不传则默认取第一个连接的svm地址
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
universalUi
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
universalUi
.
disconnect
(
)
Event事件
#
详情同EVM兼容链
错误码
#
详情同EVM兼容链

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="ui">UI<a class="index_header-anchor__Xqb+L" href="#ui" style="opacity:0">#</a></h1>
<p>在 SDK 的基础上，我们也提供了 UI 界面。如果选择通过UI接入，若DApp运营在 Telegram内，则用户可以选择停留在Telegram并唤起移动端App钱包或者唤起欧易 Mini 钱包。</p>
<h2 data-content="安装及初始化" id="安装及初始化">安装及初始化<a class="index_header-anchor__Xqb+L" href="#安装及初始化" style="opacity:0">#</a></h2>
<p>请确保更新OKX App到 6.90.1版本或以后版本，即可开始接入：</p>
<p>将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">npm install @okxconnect/ui
npm install @okxconnect/solana-provider</code></pre></div>
<p>连接钱包之前，需要先创建一个可以提供UI界面的对象，用于后续连接钱包、发送交易等操作。</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">OKXUniversalConnectUI.init(dappMetaData, actionsConfiguration, uiPreferences, language)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>dappMetaData - object<!-- -->
<ul>
<li>name - string: 应用名称，不会作为唯一表示</li>
<li>icon - string: 应用图标的 URL。必须是 PNG、ICO 等格式，不支持 SVG 图标。最好传递指向 180x180px PNG 图标的 url。</li>
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

<span class="token keyword">const</span> universalUi <span class="token operator">=</span> <span class="token keyword">await</span> OKXUniversalConnectUI<span class="token punctuation">.</span><span class="token function">init</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    dappMetaData<span class="token operator">:</span> <span class="token punctuation">{</span>
        icon<span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/assets/imgs/247/58E63FEA47A2B7D7.png"</span><span class="token punctuation">,</span>
        name<span class="token operator">:</span> <span class="token string">"OKX Connect Demo"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    actionsConfiguration<span class="token operator">:</span> <span class="token punctuation">{</span>
        returnStrategy<span class="token operator">:</span> <span class="token string">'tg://resolve'</span><span class="token punctuation">,</span>
        modals<span class="token operator">:</span><span class="token string">"all"</span><span class="token punctuation">,</span>
        tmaReturnUrl<span class="token operator">:</span><span class="token string">'back'</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    language<span class="token operator">:</span> <span class="token string">"en_US"</span><span class="token punctuation">,</span>
    uiPreferences<span class="token operator">:</span> <span class="token punctuation">{</span>
        theme<span class="token operator">:</span> <span class="token constant">THEME</span><span class="token punctuation">.</span><span class="token constant">LIGHT</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 切换插件连接钱包，会触发该事件；</span>
universalUi<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"accountChanged"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">accountChanged </span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>session<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<p>连接钱包获取钱包地址，作为标识符和用于签名交易的必要参数</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">universalUi.openModal(connectParams: ConnectParams)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>connectParams - ConnectParams<!-- -->
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
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
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">var</span> session <span class="token operator">=</span> <span class="token keyword">await</span> universalUi<span class="token punctuation">.</span><span class="token function">openModal</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    namespaces<span class="token operator">:</span> <span class="token punctuation">{</span>
        solana<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"</span><span class="token punctuation">,</span> <span class="token comment">// solana mainnet</span>
            <span class="token comment">//  "sonic:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",// sonic mainnet</span>
            <span class="token comment">//  "solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// solana testnet</span>
            <span class="token comment">//  "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet ；</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="连接钱包并签名" id="连接钱包并签名">连接钱包并签名<a class="index_header-anchor__Xqb+L" href="#连接钱包并签名" style="opacity:0">#</a></h2>
<p>连接钱包获取钱包地址，并对数据进行签名；签名结果会在"connect_signResponse"的event中回调</p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">await universalUi.openModalAndSign(connectParams: ConnectParams,signRequest: RequestParams[]);</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>
<p>connectParams - ConnectParams</p>
<ul>
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的必要信息，Solana系的key为"solana"
，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息，Solana系的key为"solana"
，如果对应的链信息钱包不支持，依然可以连接<!-- -->
<ul>
<li>chains: string[]; 链id信息</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
</ul>
</li>
<li>
<p>signRequest - RequestParams[]; 请求连接并签名的方法, 同时最多只能支持一个方法；</p>
<ul>
<li>method: string;  请求的方法名称, Solana支持的方法有："solana_signMessage"</li>
<li>chainId: string; 执行方法所在的链的ID, 该chainId必须包含在上面的namespaces中</li>
<li>params: unknown[] | Record<code>&lt;string, unknown&gt;</code> | object | undefined; 请求的方法对应的参数
<strong>返回值</strong></li>
</ul>
</li>
<li>
<p>Promise<code>&lt;SessionTypes.Struct | undefined&gt;</code></p>
<ul>
<li>topic: string; 会话标识</li>
<li>namespaces: <code>Record&lt;string, Namespace&gt;</code>; 成功连接的namespace 信息；<!-- -->
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
        solana<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"</span><span class="token punctuation">,</span> <span class="token comment">// solana mainnet</span>
                <span class="token comment">//  "sonic:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp",// sonic mainnet</span>
                <span class="token comment">//  "solana:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// solana testnet</span>
                <span class="token comment">//  "sonic:4uhcVJyU9pJkvQyS88uRDiswHXSCkY3z",// sonic testnet ；</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    sessionConfig<span class="token operator">:</span> <span class="token punctuation">{</span>
        redirect<span class="token operator">:</span> <span class="token string">"tg://resolve"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span><span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
        chainId<span class="token operator">:</span> <span class="token string">"solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp"</span><span class="token punctuation">,</span>
        method<span class="token operator">:</span> <span class="token string">"solana_signMessage"</span><span class="token punctuation">,</span>
        params<span class="token operator">:</span> <span class="token punctuation">{</span>
            message<span class="token operator">:</span> <span class="token string">"Hello Solana"</span>
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
<p>向钱包发送消息的方法，支持签名，交易</p>
<p>首先创建一个OKXSolanaProvider对象，构造函数传入OKXUniversalProviderUI，当调用 OKXSolanaProvider 相关的方法时，actionsConfiguration.mode 的配置会按照init 时候传递的值处理；</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXSolanaProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/solana-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxSolanaProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXSolanaProvider</span><span class="token punctuation">(</span>universalUi<span class="token punctuation">)</span>
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
<p><em><strong>签单笔交易</strong></em></p>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.signTransaction(transaction, chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>transaction - Transaction | VersionedTransaction 交易数据对象</li>
<li>chain: string, 请求签名执行的链，建议传递此参数，连接多条链时为必传参数，连接单条链时则默认为当前链</li>
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
<h2 data-content="获取钱包账户信息" id="获取钱包账户信息">获取钱包账户信息<a class="index_header-anchor__Xqb+L" href="#获取钱包账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxSolanaProvider.getAccount(chain)</code></pre></div>
<p><strong>请求参数</strong></p>
<ul>
<li>chain: string, 获取钱包地址的链Id，不传则默认取第一个连接的svm地址</li>
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
<span class="token keyword">let</span> provider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXSolanaProvider</span><span class="token punctuation">(</span>universalUi<span class="token punctuation">)</span>
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
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">universalUi<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="Event事件" id="event事件">Event事件<a class="index_header-anchor__Xqb+L" href="#event事件" style="opacity:0">#</a></h2>
<p><a href="/zh-hans/build/docs/sdks/app-connect-evm-ui#event%E4%BA%8B%E4%BB%B6">详情同EVM兼容链</a></p>
<h2 data-content="错误码" id="错误码">错误码<a class="index_header-anchor__Xqb+L" href="#错误码" style="opacity:0">#</a></h2>
<p><a href="/zh-hans/build/docs/sdks/app-connect-evm-sdk#%E9%94%99%E8%AF%AF%E7%A0%81">详情同EVM兼容链</a></p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "Solana兼容链",
    "UI"
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
    "连接钱包并签名",
    "判断钱包是否已连接",
    "准备交易",
    "签名",
    "签多笔交易",
    "签一笔交易并广播上链",
    "获取钱包账户信息",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
