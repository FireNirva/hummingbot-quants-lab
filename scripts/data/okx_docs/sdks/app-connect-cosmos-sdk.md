# SDK | Cosmos | 连接App或Mini钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/app-connect-cosmos-sdk#判断钱包是否已连接  
**抓取时间:** 2025-05-27 07:30:50  
**字数:** 927

## 导航路径
DApp 连接钱包 > Cosmos > SDK

## 目录
- 安装及初始化
- 连接钱包
- 判断钱包是否已连接
- 准备交易
- 获取账户信息
- 签署消息
- 签署交易 signAmino
- 签署交易 signDirect
- 断开钱包连接
- Event事件
- 错误码

---

SDK
#
安装及初始化
#
请确保更新到 6.94.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:
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
namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， COSMOS系的key为"cosmos"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；
chains: string[]; 链id信息,
defaultChain?: string; 默认链
optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， COSMOS系的key为"cosmos"，如果对应的链信息钱包不支持，依然可以连接；
chains: string[]; 链id信息,
defaultChain?: string; 默认链
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
dappInfo: object DApp 信息；
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
cosmos
:
{
chains
:
[
"cosmos:cosmoshub-4"
,
// "cosmos:osmosis-1"
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
首先创建一个OKXCosmosProvider对象，构造函数传入OKXUniversalProvider
import
{
OKXCosmosProvider
}
from
"@okxconnect/universal-provider"
;
let
okxCosmosProvider
=
new
OKXCosmosProvider
(
okxUniversalProvider
)
获取账户信息
#
okxCosmosProvider.getAccount(chainId);
请求参数
chainId: 请求的链，如cosmos:cosmoshub-4, cosmos:osmosis-1
返回值
Object
algo: "secp256k1",
address: string 钱包地址,
bech32Address: string 钱包地址,
pubKey: Uint8Array 公钥,
示例
let
result
=
okxCosmosProvider
.
getAccount
(
"cosmos:cosmoshub-4"
)
//返回结构
{
"algo"
:
"secp256k1"
,
"address"
:
"cosmos1u6lts9ng4etxj0zdaxsada6zgl8dudpg3ygvjw"
,
"bech32Address"
:
"cosmos1u6lts9ng4etxj0zdaxsada6zgl8dudpg3ygvjw"
,
"pubKey"
:
{
"0"
:
2
,
"1"
:
68
,
"2"
:
110
,
...
"32"
:
144
}
}
签署消息
#
okxCosmosProvider.signArbitrary(chain, signerAddress, message);
请求参数
chain - string, 请求执行方法的链
signerAddress - string 签名钱包地址
message - string 需要签名的消息。
返回值
Promise - object
pub_key : object
type:string 公钥类型
value:string 公钥
signature: string 签名结果
示例
let
chain
=
"cosmos:cosmoshub-4"
let
signStr
=
"data need to sign ..."
let
result
=
okxCosmosProvider
.
signArbitrary
(
chain
,
signStr
)
//返回结构: {"pub_key":{"type":"tendermint/PubKeySecp256k1","value":"AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"},"signature":"YSyndEFlHYTWpSXsn28oolZpKim/BnmCVD0hZfvPQHQV3Bc0B0EU77CKE6LpV+PUJn19d1skAQy/bXyzppnuxw=="}
签署交易 signAmino
#
okxCosmosProvider.signAmino(chainId: string, signerAddress: string, signDoc: StdSignDoc, signOptions?: object);
请求参数
chainId - string, 请求签名执行的链，必传参数
signerAddress - string,钱包地址
signDoc - object，交易信息 按照固定格式签名，类似 cosmjs 的 OfflineSigner 的 signAmino 方法 参数就是对象，signDoc 就是一个固定格式
返回值
Promise - Object
signed - object,交易信息
signature -object,签名结果
示例
let
signDoc
=
{
"chain_id"
:
"osmosis-1"
,
"account_number"
:
"630104"
,
"sequence"
:
"480"
,
"fee"
:
{
"gas"
:
"683300"
,
"amount"
:
[
{
"denom"
:
"uosmo"
,
"amount"
:
"2818"
}
]
}
,
"msgs"
:
[
{
"type"
:
"osmosis/poolmanager/swap-exact-amount-in"
,
"value"
:
{
"sender"
:
"osmo1u6lts9ng4etxj0zdaxsada6zgl8dudpgelmuyu"
,
"routes"
:
[
{
"pool_id"
:
"1096"
,
"token_out_denom"
:
"ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4"
}
,
{
"pool_id"
:
"611"
,
"token_out_denom"
:
"ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
}
]
,
"token_in"
:
{
"denom"
:
"uosmo"
,
"amount"
:
"100"
}
,
"token_out_min_amount"
:
"8"
}
}
]
,
"memo"
:
"FE"
,
"timeout_height"
:
"23603788"
,
"signOptions"
:
{
"useOneClickTrading"
:
false
,
"preferNoSetFee"
:
true
,
"fee"
:
{
"gas"
:
"683300"
,
"amount"
:
[
{
"denom"
:
"uosmo"
,
"amount"
:
"2818"
}
]
}
}
}
let
res
=
await
provider
.
signAmino
(
"cosmos:osmosis-1"
,
provider
.
getAccount
(
"cosmos:osmosis-1"
)
.
address
,
signDoc
)
/**
 返回结构:
{
"signed":
{
"chain_id": "osmosis-1",
 "account_number": "630104",
 "sequence": "480",
 "fee":
{
"amount": [
{
"amount": "12500",
 "denom": "uosmo"
}
],
 "gas": "500000"
}
,
 "msgs": [
{
"type": "osmosis/poolmanager/swap-exact-amount-in",
 "value":
{
"sender": "osmo1u6lts9ng4etxj0zdaxsada6zgl8dudpgelmuyu",
 "routes": [
{
"pool_id": "1096",
 "token_out_denom": "ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4"
}
,
{
"pool_id": "611",
 "token_out_denom": "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
}
],
 "token_in":
{
"denom": "uosmo",
 "amount": "100"
}
,
 "token_out_min_amount": "8"
}
}
],
 "memo": "FE",
 "timeout_height": "23603788",
 "signOptions":
{
"useOneClickTrading": false,
 "preferNoSetFee": true,
 "fee":
{
"gas": "683300",
 "amount": [
{
"denom": "uosmo",
 "amount": "2818"
}
]
}
}
}
,
 "signature":
{
"pub_key":
{
"type": "tendermint/PubKeySecp256k1",
 "value": "AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"
}
,
 "signature": "2Brt/w+1U3C+tIbsI//pv9zTYca9WlBd1eKm/Gde5MFaRagmxtsn6h2beP7+4R4MDav7r1G+0Nxd5arB0qVfUw=="
}
}
*/
签署交易 signDirect
#
okxCosmosProvider.signDirect(chainId, signerAddress, signDoc, signOptions?);
请求参数
chainId - string, 请求签名执行的链，必传参数，
signerAddress - string, 钱包地址
signDoc - object 交易数据
bodyBytes ,Uint8Array
authInfoBytes, Uint8Array
chainId, string
accountNumber, string
返回值
Promise - Object
signed - object,交易信息
signature -object,签名结果
示例
let
signDoc
=
{
"bodyBytes"
:
Uint8Array
,
"authInfoBytes"
:
Uint8Array
,
"chainId"
:
"osmosis-1"
,
"accountNumber"
:
"630104"
,
}
let
res
=
await
provider
.
signDirect
(
"cosmos:osmosis-1"
,
provider
.
getAccount
(
"cosmos:osmosis-1"
)
.
address
,
signDoc
)
/**
 返回结构同
{
"signed":
{
"bodyBytes":
{
"type": "Buffer",
 "data": [
 10, 193, 1, 10, 41, ...]
}
,
 "authInfoBytes":
{
"0": 10,
 "1": 81,
 ...
}
,
 "chainId": "osmosis-1",
 "accountNumber": "630104"
}
,
 "signature":
{
"pub_key":
{
"type": "tendermint/PubKeySecp256k1",
 "value": "AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"
}
,
 "signature": "YpX2kGmbZYVxUqK8y9OCweJNgZkS4WaS79nBDfOJaTgowPfY0gSbXSQeRLlif2SIkBqcwTNSItBqb5M7a6K30g=="
}
}
*/
断开钱包连接
#
断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包。
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
<p>请确保更新到 6.94.0或以后版本，即可开始接入：将 OKX Connect 集成到您的 DApp 中，可以使用 npm:</p>
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
<li>namespaces - [namespace: string]: ConnectNamespace ; 请求连接的可选信息， COSMOS系的key为"cosmos"，如果请求的链中，有任何一个链钱包不支持的话，钱包会拒绝连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息,</li>
<li>defaultChain?: string; 默认链</li>
</ul>
</li>
<li>optionalNamespaces - [namespace: string]: ConnectNamespace; 请求连接的可选信息， COSMOS系的key为"cosmos"，如果对应的链信息钱包不支持，依然可以连接；<!-- -->
<ul>
<li>chains: string[]; 链id信息,<!-- -->
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
<li>dappInfo: object DApp 信息；<!-- -->
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
        cosmos<span class="token operator">:</span> <span class="token punctuation">{</span>
            chains<span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token string">"cosmos:cosmoshub-4"</span><span class="token punctuation">,</span>
                  <span class="token comment">// "cosmos:osmosis-1"</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
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
<p>首先创建一个OKXCosmosProvider对象，构造函数传入OKXUniversalProvider</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> OKXCosmosProvider <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@okxconnect/universal-provider"</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> okxCosmosProvider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXCosmosProvider</span><span class="token punctuation">(</span>okxUniversalProvider<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxCosmosProvider.getAccount(chainId);</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId: 请求的链，如cosmos:cosmoshub-4, cosmos:osmosis-1</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Object<!-- -->
<ul>
<li>algo: "secp256k1",</li>
<li>address: string 钱包地址,</li>
<li>bech32Address: string 钱包地址,</li>
<li>pubKey: Uint8Array 公钥,</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> result <span class="token operator">=</span> okxCosmosProvider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"cosmos:cosmoshub-4"</span><span class="token punctuation">)</span>
<span class="token comment">//返回结构</span>
<span class="token punctuation">{</span>
    <span class="token string-property property">"algo"</span><span class="token operator">:</span> <span class="token string">"secp256k1"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"cosmos1u6lts9ng4etxj0zdaxsada6zgl8dudpg3ygvjw"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"bech32Address"</span><span class="token operator">:</span> <span class="token string">"cosmos1u6lts9ng4etxj0zdaxsada6zgl8dudpg3ygvjw"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"pubKey"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"0"</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
        <span class="token string-property property">"1"</span><span class="token operator">:</span> <span class="token number">68</span><span class="token punctuation">,</span>
        <span class="token string-property property">"2"</span><span class="token operator">:</span> <span class="token number">110</span><span class="token punctuation">,</span>
        <span class="token operator">...</span>
        <span class="token string-property property">"32"</span><span class="token operator">:</span> <span class="token number">144</span>
     <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签署消息" id="签署消息">签署消息<a class="index_header-anchor__Xqb+L" href="#签署消息" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxCosmosProvider.signArbitrary(chain, signerAddress, message);</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chain - string, 请求执行方法的链</li>
<li>signerAddress - string 签名钱包地址</li>
<li>message - string 需要签名的消息。</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>pub_key : object<!-- -->
<ul>
<li>type:string 公钥类型</li>
<li>value:string 公钥</li>
</ul>
</li>
<li>signature: string 签名结果</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> chain <span class="token operator">=</span> <span class="token string">"cosmos:cosmoshub-4"</span>
<span class="token keyword">let</span> signStr <span class="token operator">=</span> <span class="token string">"data need to sign ..."</span>

<span class="token keyword">let</span> result <span class="token operator">=</span> okxCosmosProvider<span class="token punctuation">.</span><span class="token function">signArbitrary</span><span class="token punctuation">(</span>chain<span class="token punctuation">,</span> signStr<span class="token punctuation">)</span>
<span class="token comment">//返回结构: {"pub_key":{"type":"tendermint/PubKeySecp256k1","value":"AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"},"signature":"YSyndEFlHYTWpSXsn28oolZpKim/BnmCVD0hZfvPQHQV3Bc0B0EU77CKE6LpV+PUJn19d1skAQy/bXyzppnuxw=="}</span>
</code></pre></div>
<h2 data-content="签署交易 signAmino" id="签署交易-signamino">签署交易 signAmino<a class="index_header-anchor__Xqb+L" href="#签署交易-signamino" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxCosmosProvider.signAmino(chainId: string, signerAddress: string, signDoc: StdSignDoc, signOptions?: object);</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>
<p>chainId - string, 请求签名执行的链，必传参数</p>
</li>
<li>
<p>signerAddress - string,钱包地址</p>
</li>
<li>
<p>signDoc - object，交易信息 按照固定格式签名，类似 cosmjs 的 OfflineSigner 的 signAmino 方法 参数就是对象，signDoc 就是一个固定格式
<em><strong>返回值</strong></em></p>
</li>
<li>
<p>Promise - Object</p>
<ul>
<li>signed - object,交易信息</li>
<li>signature -object,签名结果</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> signDoc <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"chain_id"</span><span class="token operator">:</span> <span class="token string">"osmosis-1"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"account_number"</span><span class="token operator">:</span> <span class="token string">"630104"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"sequence"</span><span class="token operator">:</span> <span class="token string">"480"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"fee"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"gas"</span><span class="token operator">:</span> <span class="token string">"683300"</span><span class="token punctuation">,</span> <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span><span class="token string-property property">"denom"</span><span class="token operator">:</span> <span class="token string">"uosmo"</span><span class="token punctuation">,</span> <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"2818"</span><span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token string-property property">"msgs"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
        <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"osmosis/poolmanager/swap-exact-amount-in"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"value"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token string-property property">"sender"</span><span class="token operator">:</span> <span class="token string">"osmo1u6lts9ng4etxj0zdaxsada6zgl8dudpgelmuyu"</span><span class="token punctuation">,</span>
            <span class="token string-property property">"routes"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
                <span class="token string-property property">"pool_id"</span><span class="token operator">:</span> <span class="token string">"1096"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"token_out_denom"</span><span class="token operator">:</span> <span class="token string">"ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
                <span class="token string-property property">"pool_id"</span><span class="token operator">:</span> <span class="token string">"611"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"token_out_denom"</span><span class="token operator">:</span> <span class="token string">"ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"</span>
            <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token string-property property">"token_in"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"denom"</span><span class="token operator">:</span> <span class="token string">"uosmo"</span><span class="token punctuation">,</span> <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"100"</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token string-property property">"token_out_min_amount"</span><span class="token operator">:</span> <span class="token string">"8"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"memo"</span><span class="token operator">:</span> <span class="token string">"FE"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"timeout_height"</span><span class="token operator">:</span> <span class="token string">"23603788"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"signOptions"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"useOneClickTrading"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token string-property property">"preferNoSetFee"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
        <span class="token string-property property">"fee"</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token string-property property">"gas"</span><span class="token operator">:</span> <span class="token string">"683300"</span><span class="token punctuation">,</span> <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span><span class="token string-property property">"denom"</span><span class="token operator">:</span> <span class="token string">"uosmo"</span><span class="token punctuation">,</span> <span class="token string-property property">"amount"</span><span class="token operator">:</span> <span class="token string">"2818"</span><span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signAmino</span><span class="token punctuation">(</span><span class="token string">"cosmos:osmosis-1"</span><span class="token punctuation">,</span> provider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"cosmos:osmosis-1"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address<span class="token punctuation">,</span> signDoc<span class="token punctuation">)</span>


<span class="token doc-comment comment">/**
    返回结构:
    <span class="token punctuation">{</span>
    "signed": <span class="token punctuation">{</span>
    "chain_id": "osmosis-1",
    "account_number": "630104",
    "sequence": "480",
    "fee": <span class="token punctuation">{</span>
    "amount": [
    <span class="token punctuation">{</span>
    "amount": "12500",
    "denom": "uosmo"
    <span class="token punctuation">}</span>
    ],
    "gas": "500000"
    <span class="token punctuation">}</span>,
    "msgs": [
    <span class="token punctuation">{</span>
    "type": "osmosis/poolmanager/swap-exact-amount-in",
    "value": <span class="token punctuation">{</span>
    "sender": "osmo1u6lts9ng4etxj0zdaxsada6zgl8dudpgelmuyu",
    "routes": [
    <span class="token punctuation">{</span>
    "pool_id": "1096",
    "token_out_denom": "ibc/987C17B11ABC2B20019178ACE62929FE9840202CE79498E29FE8E5CB02B7C0A4"
    <span class="token punctuation">}</span>,
    <span class="token punctuation">{</span>
    "pool_id": "611",
    "token_out_denom": "ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
    <span class="token punctuation">}</span>
    ],
    "token_in": <span class="token punctuation">{</span>
    "denom": "uosmo",
    "amount": "100"
    <span class="token punctuation">}</span>,
    "token_out_min_amount": "8"
    <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
    ],
    "memo": "FE",
    "timeout_height": "23603788",
    "signOptions": <span class="token punctuation">{</span>
    "useOneClickTrading": false,
    "preferNoSetFee": true,
    "fee": <span class="token punctuation">{</span>
    "gas": "683300",
    "amount": [
    <span class="token punctuation">{</span>
        "denom": "uosmo",
        "amount": "2818"
    <span class="token punctuation">}</span>
    ]
    <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>,
    "signature": <span class="token punctuation">{</span>
    "pub_key": <span class="token punctuation">{</span>
    "type": "tendermint/PubKeySecp256k1",
    "value": "AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"
    <span class="token punctuation">}</span>,
    "signature": "2Brt/w+1U3C+tIbsI//pv9zTYca9WlBd1eKm/Gde5MFaRagmxtsn6h2beP7+4R4MDav7r1G+0Nxd5arB0qVfUw=="
    <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
 */</span>
</code></pre></div>
<h2 data-content="签署交易 signDirect" id="签署交易-signdirect">签署交易 signDirect<a class="index_header-anchor__Xqb+L" href="#签署交易-signdirect" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-unknown"><code class="language-unknown">okxCosmosProvider.signDirect(chainId, signerAddress, signDoc, signOptions?);</code></pre></div>
<p><em><strong>请求参数</strong></em></p>
<ul>
<li>chainId - string, 请求签名执行的链，必传参数，</li>
<li>signerAddress - string, 钱包地址</li>
<li>signDoc - object 交易数据<!-- -->
<ul>
<li>bodyBytes ,Uint8Array</li>
<li>authInfoBytes, Uint8Array</li>
<li>chainId, string</li>
<li>accountNumber, string</li>
</ul>
</li>
</ul>
<p><em><strong>返回值</strong></em></p>
<ul>
<li>Promise - Object<!-- -->
<ul>
<li>signed - object,交易信息</li>
<li>signature -object,签名结果</li>
</ul>
</li>
</ul>
<p><em><strong>示例</strong></em></p>
<div class="remark-highlight"><pre class="language-ts"><code class="language-ts"><span class="token keyword">let</span> signDoc <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">"bodyBytes"</span><span class="token operator">:</span> Uint8Array<span class="token punctuation">,</span>
    <span class="token string-property property">"authInfoBytes"</span><span class="token operator">:</span> Uint8Array<span class="token punctuation">,</span>
    <span class="token string-property property">"chainId"</span><span class="token operator">:</span> <span class="token string">"osmosis-1"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"accountNumber"</span><span class="token operator">:</span> <span class="token string">"630104"</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
<span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> provider<span class="token punctuation">.</span><span class="token function">signDirect</span><span class="token punctuation">(</span><span class="token string">"cosmos:osmosis-1"</span><span class="token punctuation">,</span> provider<span class="token punctuation">.</span><span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token string">"cosmos:osmosis-1"</span><span class="token punctuation">)</span><span class="token punctuation">.</span>address<span class="token punctuation">,</span> signDoc<span class="token punctuation">)</span>


<span class="token doc-comment comment">/**
    返回结构同
    <span class="token punctuation">{</span>
    "signed": <span class="token punctuation">{</span>
    "bodyBytes": <span class="token punctuation">{</span>
    "type": "Buffer",
    "data": [
    10, 193, 1, 10, 41, ...]
    <span class="token punctuation">}</span>,
    "authInfoBytes": <span class="token punctuation">{</span>
    "0": 10,
    "1": 81,
    ...
    <span class="token punctuation">}</span>,
    "chainId": "osmosis-1",
    "accountNumber": "630104"
    <span class="token punctuation">}</span>,
    "signature": <span class="token punctuation">{</span>
    "pub_key": <span class="token punctuation">{</span>
    "type": "tendermint/PubKeySecp256k1",
    "value": "AkRuGelKwOg+qJbScSUHV36zn73S1q6fD8C5dZ8furqQ"
    <span class="token punctuation">}</span>,
    "signature": "YpX2kGmbZYVxUqK8y9OCweJNgZkS4WaS79nBDfOJaTgowPfY0gSbXSQeRLlif2SIkBqcwTNSItBqb5M7a6K30g=="
    <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
 */</span>
</code></pre></div>
<h2 data-content="断开钱包连接" id="断开钱包连接">断开钱包连接<a class="index_header-anchor__Xqb+L" href="#断开钱包连接" style="opacity:0">#</a></h2>
<p>断开已连接钱包,并删除当前会话,如果要切换连接钱包,请先断开当前钱包。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxUniversalProvider<span class="token punctuation">.</span><span class="token function">disconnect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "Cosmos",
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
    "SDK",
    "UI",
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
    "获取账户信息",
    "签署消息",
    "签署交易 signAmino",
    "签署交易 signDirect",
    "断开钱包连接",
    "Event事件",
    "错误码"
  ]
}
```

</details>
