# 在 Ton 链上搭建兑换应用 | 搭建兑换应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-swap-ton-quick-start#3.2-定义辅助函数  
**抓取时间:** 2025-05-27 05:15:21  
**字数:** 743

## 导航路径
DEX API > 交易 API > 搭建兑换应用 > 在 Ton 链上搭建兑换应用

## 目录
- 1. 设置你的环境
- 2. 请求询价接口，拿到询价数据
- 3. 请求兑换接口，发起交易

---

在 Ton 链上搭建兑换应用
#
在本指南中，我们将用一个示例来展示如何通过欧易 DEX 提供的 API 在 Ton 上用 Ton 兑换 JETTON，这个过程中的步骤包括：
设置你的环境
请求询价接口，获取询价数据
请求兑换接口，发起交易
1. 设置你的环境
#
# --------------------- npm package ---------------------
npm
install
@ton/ton @ton/crypto @ton/core buffer @orbs-network
const
cryptoJS
=
require
(
'crypto-js'
)
;
// Import encryption modules for subsequent encryption calculations
const
{
TonClient
,
WalletContractV4
,
internal
}
=
require
(
"@ton/ton"
)
;
const
{
toNano
,
Cell
}
=
require
(
"@ton/core"
)
;
const
{
mnemonicToPrivateKey
}
=
require
(
"@ton/crypto"
)
;
const
{
getHttpEndpoint
}
=
require
(
"@orbs-network/ton-access"
)
;
// --------------------- environment variable ---------------------
const
apiBaseUrl
=
'https://web3.okx.com/api/v5/dex/aggregator'
;
const
chainId
=
'607'
;
// Native token contract address
const
fromTokenAddress
=
'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'
;
// JETTON token contract address
const
toTokenAddress
=
'EQAQXlWJvGbbFfE8F3oS8s87lIgdovS455IsWFaRdmJetTon'
;
// your wallet address
const
user
=
'UQDoI2kiSNQZxxxxxxxxxxxx6lM2ZSxKkEw3k1'
const
fromAmount
=
'1000000'
// user wallet private key
const
privateKey
=
'xxxxx'
;
// open api Secret key
const
secretkey
=
'xxxxx'
// Get the current time
const
date
=
new
Date
(
)
;
// --------------------- util function ---------------------
function
getAggregatorRequestUrl
(
methodName
,
queryParams
)
{
return
apiBaseUrl
+
methodName
+
'?'
+
(
new
URLSearchParams
(
queryParams
)
)
.
toString
(
)
;
}
// Check https://web3.okx.com/zh-hans/web3/build/docs/waas/rest-authentication for api-key
const
headersParams
=
{
'Content-Type'
:
'application/json'
,
// The api Key obtained from the previous application
'OK-ACCESS-KEY'
:
'xxxxx'
,
'OK-ACCESS-SIGN'
:
cryptoJS
.
enc
.
Base64
.
stringify
(
// The field order of headersParams should be consistent with the order of quoteParams.
// example : quote ==> cryptoJS.HmacSHA256(date.toISOString() + 'GET' + '/api/v5/dex/aggregator/quote?amount=1000000&chainIndex=607&toTokenAddress=EQAQXlWJvGbbFfE8F3oS8s87lIgdovS455IsWFaRdmJetTon&fromTokenAddress=EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c', secretKey)
cryptoJS
.
HmacSHA256
(
date
.
toISOString
(
)
+
'GET'
+
'/api/v5/dex/aggregator/xxx/xxx/xxx'
,
secretKey
)
)
,
// Convert the current time to the desired format
'OK-ACCESS-TIMESTAMP'
:
date
.
toISOString
(
)
,
// The password created when applying for the key
'OK-ACCESS-PASSPHRASE'
:
'xxxxxxx'
,
}
;
提示
暂不支持额外接收地址。
2. 请求询价接口，拿到询价数据
#
2.1 定义询价参数
#
接下来，定义询价参数，获取询价的基础信息和路径列表信息。
const
quoteParams
=
{
amount
:
fromAmount
,
chainId
:
chainId
,
toTokenAddress
:
toTokenAddress
,
fromTokenAddress
:
fromTokenAddress
,
}
;
2.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
getQuote
=
async
(
)
=>
{
const
apiRequestUrl
=
getAggregatorRequestUrl
(
'/quote'
,
quoteParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
)
.
then
(
(
res
)
=>
res
.
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
3. 请求兑换接口，发起交易
#
3.1 定义兑换参数
#
接下来，定义参数，并获取兑换的 tx 信息。
const
swapParams
=
{
chainId
:
1
,
fromTokenAddress
:
fromTokenAddress
,
toTokenAddress
:
toTokenAddress
,
amount
:
'1000000'
,
slippage
:
'0.03'
,
userWalletAddress
:
user
}
;
3.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX 批准交易 API 进行交互。
const
getSwapData
=
async
(
)
=>
{
const
apiRequestUrl
=
getAggregatorRequestUrl
(
'/swap'
,
swapParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
)
.
then
(
(
res
)
=>
res
.
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
3.3 请求兑换接口拿到 tx 信息，发起上链交易
#
let
tx
=
{
"data"
:
"te6cckEBBAEAwAABsA+KfqUAALgW1FkYQkBfXhAIAK3+NxydEq8Qc4csyQ7botOnBqxp3L54Fn7Zof9EjDx5ADoI2kiSNQZdnOIVsRSLrVMtiBySHg0Lt6lM2ZSxKkEwyC592wEBAZ8RMwAAAvrwgIALyzu3/eo7h8wFCa+0XsOg6z0IG/43fUuMnumWS8xS91AD0F/w35CTWUxTWRjefoV+400KRA2jX51X4ezIgmUUY/0AX5sDCAIBAQwDABgAAAABAAAAAAAAA+cKUcDO"
,
"from"
:
"UQDoI2kiSNQZdnOIVsRSLrVMtiBySHg0Lt6lM2ZSxKkEw3k1"
,
"gas"
:
"80234000"
,
"gasPrice"
:
"5000"
,
"maxPriorityFeePerGas"
:
""
,
"minReceiveAmount"
:
"25062412"
,
"to"
:
"UQBXp1W7_UJWvsBrbaO8s-9i8O53s7hNNeZ0XqEEz12i0oDS"
,
"value"
:
"440000000"
}
// This is the response of the /swap endpoint
async
function
sendTx
(
)
{
const
endpoint
=
await
getHttpEndpoint
(
)
;
const
client
=
new
TonClient
(
{
endpoint
}
)
;
const
mnemonic
=
[
'range'
,
'xxxxxx'
]
;
// Your mnemonic words Decimal conversion
const
keyPair
=
await
mnemonicToPrivateKey
(
mnemonic
)
;
const
wallet
=
WalletContractV4
.
create
(
{
workchain
:
0
,
publicKey
:
keyPair
.
publicKey
}
)
;
const
contract
=
client
.
open
(
wallet
)
let
seqno
=
await
contract
.
getSeqno
(
)
;
const
body
=
Cell
.
fromBase64
(
tx
.
data
)
;
const
value
=
tx
.
value
/
Math
.
pow
(
10
,
9
)
;
// Decimal conversion
const
to
=
tx
.
to
;
await
contract
.
sendTransfer
(
{
seqno
,
secretKey
:
keyPair
.
secretKey
,
messages
:
[
internal
(
{
value
:
toNano
(
value
)
,
to
,
body
:
body
,
}
)
]
}
)
;
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="在-ton-链上搭建兑换应用">在 Ton 链上搭建兑换应用<a class="index_header-anchor__Xqb+L" href="#在-ton-链上搭建兑换应用" style="opacity:0">#</a></h1>
<p>在本指南中，我们将用一个示例来展示如何通过欧易 DEX 提供的 API 在 Ton 上用 Ton 兑换 JETTON，这个过程中的步骤包括：</p>
<ol>
<li>设置你的环境</li>
<li>请求询价接口，获取询价数据</li>
<li>请求兑换接口，发起交易</li>
</ol>
<h2 data-content="1. 设置你的环境" id="1.-设置你的环境">1. 设置你的环境<a class="index_header-anchor__Xqb+L" href="#1.-设置你的环境" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token comment"># --------------------- npm package ---------------------</span>
<span class="token function">npm</span> <span class="token function">install</span> @ton/ton @ton/crypto @ton/core buffer @orbs-network
</code></pre></div>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> cryptoJS <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'crypto-js'</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// Import encryption modules for subsequent encryption calculations</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token maybe-class-name">TonClient</span><span class="token punctuation">,</span> <span class="token maybe-class-name">WalletContractV4</span><span class="token punctuation">,</span> internal <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">"@ton/ton"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> toNano<span class="token punctuation">,</span> <span class="token maybe-class-name">Cell</span> <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">"@ton/core"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> mnemonicToPrivateKey <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">"@ton/crypto"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> getHttpEndpoint <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">"@orbs-network/ton-access"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// --------------------- environment variable ---------------------</span>
<span class="token keyword">const</span> apiBaseUrl <span class="token operator">=</span> <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">'607'</span><span class="token punctuation">;</span>
<span class="token comment">// Native token contract address</span>
<span class="token keyword">const</span> fromTokenAddress <span class="token operator">=</span> <span class="token string">'EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c'</span><span class="token punctuation">;</span>
<span class="token comment">// JETTON token contract address</span>
<span class="token keyword">const</span> toTokenAddress <span class="token operator">=</span> <span class="token string">'EQAQXlWJvGbbFfE8F3oS8s87lIgdovS455IsWFaRdmJetTon'</span><span class="token punctuation">;</span>
<span class="token comment">// your wallet address</span>
<span class="token keyword">const</span> user <span class="token operator">=</span> <span class="token string">'UQDoI2kiSNQZxxxxxxxxxxxx6lM2ZSxKkEw3k1'</span>
<span class="token keyword">const</span> fromAmount <span class="token operator">=</span> <span class="token string">'1000000'</span>
<span class="token comment">// user wallet private key</span>
<span class="token keyword">const</span> privateKey <span class="token operator">=</span> <span class="token string">'xxxxx'</span><span class="token punctuation">;</span>
<span class="token comment">// open api Secret key</span>
<span class="token keyword">const</span> secretkey <span class="token operator">=</span> <span class="token string">'xxxxx'</span>
<span class="token comment">// Get the current time</span>
<span class="token keyword">const</span> date <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// --------------------- util function ---------------------</span>
<span class="token keyword">function</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span><span class="token parameter">methodName<span class="token punctuation">,</span> queryParams</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">return</span> apiBaseUrl <span class="token operator">+</span> methodName <span class="token operator">+</span> <span class="token string">'?'</span> <span class="token operator">+</span> <span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>queryParams<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Check https://web3.okx.com/zh-hans/web3/build/docs/waas/rest-authentication for api-key</span>

<span class="token keyword">const</span> headersParams <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">'Content-Type'</span><span class="token operator">:</span> <span class="token string">'application/json'</span><span class="token punctuation">,</span>
    <span class="token comment">// The api Key obtained from the previous application</span>
    <span class="token string-property property">'OK-ACCESS-KEY'</span><span class="token operator">:</span> <span class="token string">'xxxxx'</span><span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-SIGN'</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>
    <span class="token comment">// The field order of headersParams should be consistent with the order of quoteParams.</span>
    <span class="token comment">// example : quote  ==&gt;   cryptoJS.HmacSHA256(date.toISOString() + 'GET' + '/api/v5/dex/aggregator/quote?amount=1000000&amp;chainIndex=607&amp;toTokenAddress=EQAQXlWJvGbbFfE8F3oS8s87lIgdovS455IsWFaRdmJetTon&amp;fromTokenAddress=EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c', secretKey)</span>
        cryptoJS<span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>date<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token string">'GET'</span> <span class="token operator">+</span> <span class="token string">'/api/v5/dex/aggregator/xxx/xxx/xxx'</span><span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token comment">// Convert the current time to the desired format</span>
    <span class="token string-property property">'OK-ACCESS-TIMESTAMP'</span><span class="token operator">:</span> date<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token comment">// The password created when applying for the key</span>
    <span class="token string-property property">'OK-ACCESS-PASSPHRASE'</span><span class="token operator">:</span> <span class="token string">'xxxxxxx'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rdbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rdbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p><strong>暂不支持额外接收地址。</strong></p></div></div></div></div></div>
<h2 data-content="2. 请求询价接口，拿到询价数据" id="2.-请求询价接口，拿到询价数据">2. 请求询价接口，拿到询价数据<a class="index_header-anchor__Xqb+L" href="#2.-请求询价接口，拿到询价数据" style="opacity:0">#</a></h2>
<h3 id="2.1-定义询价参数">2.1 定义询价参数<a class="index_header-anchor__Xqb+L" href="#2.1-定义询价参数" style="opacity:0">#</a></h3>
<ul>
<li>接下来，定义询价参数，获取询价的基础信息和路径列表信息。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> quoteParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">amount</span><span class="token operator">:</span> fromAmount<span class="token punctuation">,</span>
  <span class="token literal-property property">chainId</span><span class="token operator">:</span> chainId<span class="token punctuation">,</span>
  <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> toTokenAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> fromTokenAddress<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="2.2-定义辅助函数">2.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#2.2-定义辅助函数" style="opacity:0">#</a></h3>
<ul>
<li>定义一个辅助函数，用于与 DEX API 进行交互。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getQuote</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> apiRequestUrl <span class="token operator">=</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span><span class="token string">'/quote'</span><span class="token punctuation">,</span> quoteParams<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="3. 请求兑换接口，发起交易" id="3.-请求兑换接口，发起交易">3. 请求兑换接口，发起交易<a class="index_header-anchor__Xqb+L" href="#3.-请求兑换接口，发起交易" style="opacity:0">#</a></h2>
<h3 id="3.1-定义兑换参数">3.1 定义兑换参数<a class="index_header-anchor__Xqb+L" href="#3.1-定义兑换参数" style="opacity:0">#</a></h3>
<ul>
<li>接下来，定义参数，并获取兑换的 tx 信息。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> swapParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
  <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> fromTokenAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> toTokenAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.03'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> user
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="3.2-定义辅助函数">3.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#3.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX 批准交易 API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getSwapData</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> apiRequestUrl <span class="token operator">=</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span><span class="token string">'/swap'</span><span class="token punctuation">,</span> swapParams<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="3.3-请求兑换接口拿到-tx-信息，发起上链交易">3.3 请求兑换接口拿到 tx 信息，发起上链交易<a class="index_header-anchor__Xqb+L" href="#3.3-请求兑换接口拿到-tx-信息，发起上链交易" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">let</span> tx <span class="token operator">=</span> <span class="token punctuation">{</span>
          <span class="token string-property property">"data"</span><span class="token operator">:</span> <span class="token string">"te6cckEBBAEAwAABsA+KfqUAALgW1FkYQkBfXhAIAK3+NxydEq8Qc4csyQ7botOnBqxp3L54Fn7Zof9EjDx5ADoI2kiSNQZdnOIVsRSLrVMtiBySHg0Lt6lM2ZSxKkEwyC592wEBAZ8RMwAAAvrwgIALyzu3/eo7h8wFCa+0XsOg6z0IG/43fUuMnumWS8xS91AD0F/w35CTWUxTWRjefoV+400KRA2jX51X4ezIgmUUY/0AX5sDCAIBAQwDABgAAAABAAAAAAAAA+cKUcDO"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"from"</span><span class="token operator">:</span> <span class="token string">"UQDoI2kiSNQZdnOIVsRSLrVMtiBySHg0Lt6lM2ZSxKkEw3k1"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"gas"</span><span class="token operator">:</span> <span class="token string">"80234000"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"gasPrice"</span><span class="token operator">:</span> <span class="token string">"5000"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"maxPriorityFeePerGas"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
          <span class="token string-property property">"minReceiveAmount"</span><span class="token operator">:</span> <span class="token string">"25062412"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"to"</span><span class="token operator">:</span> <span class="token string">"UQBXp1W7_UJWvsBrbaO8s-9i8O53s7hNNeZ0XqEEz12i0oDS"</span><span class="token punctuation">,</span>
          <span class="token string-property property">"value"</span><span class="token operator">:</span> <span class="token string">"440000000"</span>
<span class="token punctuation">}</span>
<span class="token comment">// This is the response of the /swap endpoint</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">sendTx</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>

    <span class="token keyword">const</span> endpoint <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getHttpEndpoint</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TonClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span> endpoint <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> mnemonic <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'range'</span><span class="token punctuation">,</span> <span class="token string">'xxxxxx'</span><span class="token punctuation">]</span><span class="token punctuation">;</span> <span class="token comment">//   Your mnemonic words  Decimal conversion</span>
    <span class="token keyword">const</span> keyPair <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">mnemonicToPrivateKey</span><span class="token punctuation">(</span>mnemonic<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> wallet <span class="token operator">=</span> <span class="token maybe-class-name">WalletContractV4</span><span class="token punctuation">.</span><span class="token method function property-access">create</span><span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token literal-property property">workchain</span><span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span> <span class="token literal-property property">publicKey</span><span class="token operator">:</span> keyPair<span class="token punctuation">.</span><span class="token property-access">publicKey</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> contract <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token method function property-access">open</span><span class="token punctuation">(</span>wallet<span class="token punctuation">)</span>


    <span class="token keyword">let</span> seqno <span class="token operator">=</span> <span class="token keyword control-flow">await</span> contract<span class="token punctuation">.</span><span class="token method function property-access">getSeqno</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> body <span class="token operator">=</span> <span class="token maybe-class-name">Cell</span><span class="token punctuation">.</span><span class="token method function property-access">fromBase64</span><span class="token punctuation">(</span>tx<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> value <span class="token operator">=</span> tx<span class="token punctuation">.</span><span class="token property-access">value</span> <span class="token operator">/</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> <span class="token number">9</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// Decimal conversion</span>
    <span class="token keyword">const</span> to <span class="token operator">=</span> tx<span class="token punctuation">.</span><span class="token property-access">to</span><span class="token punctuation">;</span>

    <span class="token keyword control-flow">await</span> contract<span class="token punctuation">.</span><span class="token method function property-access">sendTransfer</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        seqno<span class="token punctuation">,</span>
        <span class="token literal-property property">secretKey</span><span class="token operator">:</span> keyPair<span class="token punctuation">.</span><span class="token property-access">secretKey</span><span class="token punctuation">,</span>
        <span class="token literal-property property">messages</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token function">internal</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">value</span><span class="token operator">:</span> <span class="token function">toNano</span><span class="token punctuation">(</span>value<span class="token punctuation">)</span><span class="token punctuation">,</span>
            to<span class="token punctuation">,</span>
            <span class="token literal-property property">body</span><span class="token operator">:</span> body<span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "搭建兑换应用",
    "在 Ton 链上搭建兑换应用"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "在 Solana 链上搭建兑换应用",
    "在 Solana 链上兑换的高级用法",
    "在 EVM 链上搭建兑换应用",
    "在 Sui 链上搭建兑换应用",
    "在 Ton 链上搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "设置分佣",
    "DEX 集成",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "支持的跨链桥",
    "智能合约",
    "错误码",
    "FAQ"
  ],
  "toc": [
    "1. 设置你的环境",
    "2. 请求询价接口，拿到询价数据",
    "3. 请求兑换接口，发起交易"
  ]
}
```

</details>
