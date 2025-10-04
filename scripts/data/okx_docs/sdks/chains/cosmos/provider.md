# Provider API | cosmos | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/cosmos/provider#签名信息  
**抓取时间:** 2025-05-27 07:18:29  
**字数:** 992

## 导航路径
DApp 连接钱包 > cosmos > Provider API

## 目录
- 什么是 Injected provider API？
- 连接账户
- 签名交易
- 签名信息
- 事件

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
Note
: Cosmos 接入仅支持欧易 Web3 钱包插件端。
连接账户
#
#
window.okxwallet.keplr.enable(chainIds)
描述
如果插件当前被锁定，
window.keplr.enable（chainIds）
方法请求解锁插件。如果用户未授予该网页的权限，它将要求用户授予该网页访问
Keplr
的权限。
enable
方法可以接收一个或多个链id作为数组。当传递链id数组时，你可以同时请求尚未授权的所有链的权限。
如果用户取消解锁或拒绝权限，将抛出错误。
enable
(
chainIds
:
string
|
string
[
]
)
:
Promise
<
void
>
例子
在
codeopen
中打开。
Connect Cosmos
HTML
JavaScript
<
button
class
=
"
connectCosmosButton
"
>
Connect Cosmos
</
button
>
const
connectCosmosButton
=
document
.
querySelector
(
'.connectCosmosButton'
)
;
connectCosmosButton
.
addEventListener
(
'click'
,
async
(
)
=>
{
try
{
const
chainId
=
"cosmoshub-4"
;
// Enabling before using the Keplr is recommended.
// This method will ask the user whether to allow access if they haven't visited this website.
// Also, it will request that the user unlock the wallet if the wallet is locked.
await
window
.
okxwallet
.
keplr
.
enable
(
chainId
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
;
}
}
)
;
签名交易
#
#
window.okxwallet.keplr.signAmino(chainId, signer, signDoc)
描述
按照固定格式签名，类似 cosmjs 的 OfflineSigner 的 signAmino 方法
参数就是对象，signDoc 就是一个固定格式
window
.
okxwallet
.
keplr
.
signAmino
(
chainId
:
string
,
signer
:
string
,
signDoc
:
StdSignDoc
,
signOptions
:
any
)
:
Promise
<
AminoSignResponse
>
例子
在
codeopen
中打开。
Connect Cosmos
Send Transaction
HTML
JavaScript
<
button
class
=
"
connectCosmosButton btn
"
>
Connect Cosmos
</
button
>
<
button
class
=
"
signTransactionButton btn
"
>
Sign Transaction
</
button
>
const
connectCosmosButton
=
document
.
querySelector
(
'.connectCosmosButton'
)
;
const
signTransactionButton
=
document
.
querySelector
(
'.signTransactionButton'
)
;
signTransactionButton
.
addEventListener
(
'click'
,
async
(
)
=>
{
try
{
const
res
=
const
res
=
await
window
.
okxwallet
.
keplr
.
signAmino
(
"osmosis-1"
,
"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"
,
{
account_number
:
"707744"
,
chain_id
:
"osmosis-1"
,
fee
:
{
gas
:
"500000"
,
amount
:
[
{
denom
:
"uosmo"
,
amount
:
"12500"
}
]
}
,
memo
:
""
,
msgs
:
[
{
type
:
"osmosis/gamm/swap-exact-amount-in"
,
value
:
{
routes
:
[
{
pool_id
:
"795"
,
token_out_denom
:
"uosmo"
}
,
{
pool_id
:
"1"
,
token_out_denom
:
"ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"
}
]
,
sender
:
"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"
,
token_in
:
{
amount
:
"10000"
,
denom
:
"ibc/2DA9C149E9AD2BD27FEFA635458FB37093C256C1A940392634A16BEA45262604"
}
,
token_out_min_amount
:
"553"
}
}
]
,
sequence
:
"54"
}
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
}
}
)
;
connectCosmosButton
.
addEventListener
(
'click'
,
async
(
)
=>
{
try
{
const
chainId
=
"cosmoshub-4"
;
// Enabling before using the Keplr is recommended.
// This method will ask the user whether to allow access if they haven't visited this website.
// Also, it will request that the user unlock the wallet if the wallet is locked.
const
res
=
await
window
.
keplr
.
enable
(
chainId
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
;
}
}
)
;
签名信息
#
#
window.okxwallet.keplr.signArbitrary(chainId, signer, data)
描述
签名任意信息，相当于之前几个链的
signMessage(any)
。
signArbitrary
(
chainId
:
string
,
signer
:
string
,
data
:
string
|
Uint8Array
)
:
Promise
<
StdSignature
>
;
verifyArbitrary
(
chainId
:
string
,
signer
:
string
,
data
:
string
|
Uint8Array
,
signature
:
StdSignature
)
:
Promise
<
boolean
>
;
例子
在
codeopen
中打开。
Connect Cosmos
Sign Message
HTML
JavaScript
<
button
class
=
"
connectCosmosButton btn
"
>
Connect Cosmos
</
button
>
<
button
class
=
"
signMessageButton btn
"
>
Sign Message
</
button
>
const
connectCosmosButton
=
document
.
querySelector
(
'.connectCosmosButton'
)
;
const
signMessageButton
=
document
.
querySelector
(
'.signMessageButton'
)
;
signMessageButton
.
addEventListener
(
'click'
,
async
(
)
=>
{
try
{
const
res
=
const
res
=
await
window
.
okxwallet
.
keplr
.
signArbitrary
(
"osmosis-1"
,
"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"
,
'test cosmos'
}
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
}
}
)
;
connectCosmosButton
.
addEventListener
(
'click'
,
async
(
)
=>
{
try
{
const
chainId
=
"cosmoshub-4"
;
// Enabling before using the Keplr is recommended.
// This method will ask the user whether to allow access if they haven't visited this website.
// Also, it will request that the user unlock the wallet if the wallet is locked.
const
res
=
await
window
.
keplr
.
enable
(
chainId
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
;
}
}
)
;
事件
#
成功连接
连接到欧易 Web3 钱包可以通过调用
window.okxwallet.keplr.enable(chainId)
。 当用户接受连接请求时，会触发连接事件。
用法
window
.
okxwallet
.
keplr
.
on
(
"connect"
,
(
)
=>
console
.
log
(
"connected!"
)
)
;
例子
在
codeopen
中打开。
Connect Cosmos
Result:
Cannot read properties of undefined (reading 'keplr')
HTML
JavaScript
<
button
class
=
"
connectCosmosButton
"
>
Connect Cosmos
</
button
>
const
connectCosmosButton
=
document
.
querySelector
(
'.connectCosmosButton'
)
;
window
.
okxwallet
.
keplr
.
on
(
"connect"
,
(
)
=>
console
.
log
(
"connected!"
)
)
;
connectCosmosButton
.
addEventListener
(
'click'
,
(
)
=>
{
try
{
const
chainId
=
"cosmoshub-4"
;
// Enabling before using the Keplr is recommended.
// This method will ask the user whether to allow access if they haven't visited this website.
// Also, it will request that the user unlock the wallet if the wallet is locked.
const
res
=
await
window
.
okxwallet
.
keplr
.
enable
(
chainId
)
;
console
.
log
(
res
)
;
}
catch
(
error
)
{
console
.
log
(
error
)
;
}
}
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<p><strong>Note</strong>: Cosmos 接入仅支持欧易 Web3 钱包插件端。</p>
<h2 data-content="连接账户" id="连接账户">连接账户<a class="index_header-anchor__Xqb+L" href="#连接账户" style="opacity:0">#</a></h2>
<p>#<code>window.okxwallet.keplr.enable(chainIds)</code></p>
<p><strong>描述</strong></p>
<p>如果插件当前被锁定，<code>window.keplr.enable（chainIds）</code>方法请求解锁插件。如果用户未授予该网页的权限，它将要求用户授予该网页访问 <code>Keplr</code> 的权限。
<code>enable</code> 方法可以接收一个或多个链id作为数组。当传递链id数组时，你可以同时请求尚未授权的所有链的权限。
如果用户取消解锁或拒绝权限，将抛出错误。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token function">enable</span><span class="token punctuation">(</span>chainIds<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token builtin">string</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token keyword">void</span><span class="token operator">&gt;</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/qBMRrEo" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Cosmos</span></button></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":Rpbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":Rpbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":Rpbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectCosmosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Cosmos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":Rpbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectCosmosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectCosmosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectCosmosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">"cosmoshub-4"</span><span class="token punctuation">;</span>
    <span class="token comment">// Enabling before using the Keplr is recommended.</span>
    <span class="token comment">// This method will ask the user whether to allow access if they haven't visited this website.</span>
    <span class="token comment">// Also, it will request that the user unlock the wallet if the wallet is locked.</span>
    <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span>chainId<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="签名交易" id="签名交易">签名交易<a class="index_header-anchor__Xqb+L" href="#签名交易" style="opacity:0">#</a></h2>
<p>#<code>window.okxwallet.keplr.signAmino(chainId, signer, signDoc)</code></p>
<p><strong>描述</strong></p>
<p>按照固定格式签名，类似 cosmjs 的 OfflineSigner 的 signAmino 方法</p>
<p>参数就是对象，signDoc 就是一个固定格式</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>keplr<span class="token punctuation">.</span><span class="token function">signAmino</span><span class="token punctuation">(</span>chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> signer<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> signDoc<span class="token operator">:</span> StdSignDoc<span class="token punctuation">,</span> signOptions<span class="token operator">:</span> <span class="token builtin">any</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>AminoSignResponse<span class="token operator">&gt;</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/PodWmJm" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Cosmos</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Send Transaction</span></button><div></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R1dbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R1dbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R1dbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectCosmosButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Cosmos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>signTransactionButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Sign Transaction<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R1dbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectCosmosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectCosmosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> signTransactionButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.signTransactionButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

signTransactionButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span>  <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">signAmino</span><span class="token punctuation">(</span>
      <span class="token string">"osmosis-1"</span><span class="token punctuation">,</span>
      <span class="token string">"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">account_number</span><span class="token operator">:</span> <span class="token string">"707744"</span><span class="token punctuation">,</span>
        <span class="token literal-property property">chain_id</span><span class="token operator">:</span> <span class="token string">"osmosis-1"</span><span class="token punctuation">,</span>
        <span class="token literal-property property">fee</span><span class="token operator">:</span> <span class="token punctuation">{</span>
          <span class="token literal-property property">gas</span><span class="token operator">:</span> <span class="token string">"500000"</span><span class="token punctuation">,</span>
          <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
              <span class="token literal-property property">denom</span><span class="token operator">:</span> <span class="token string">"uosmo"</span><span class="token punctuation">,</span>
              <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">"12500"</span>
            <span class="token punctuation">}</span>
          <span class="token punctuation">]</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">memo</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token literal-property property">msgs</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">"osmosis/gamm/swap-exact-amount-in"</span><span class="token punctuation">,</span>
            <span class="token literal-property property">value</span><span class="token operator">:</span> <span class="token punctuation">{</span>
              <span class="token literal-property property">routes</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                  <span class="token literal-property property">pool_id</span><span class="token operator">:</span> <span class="token string">"795"</span><span class="token punctuation">,</span>
                  <span class="token literal-property property">token_out_denom</span><span class="token operator">:</span> <span class="token string">"uosmo"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                  <span class="token literal-property property">pool_id</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                  <span class="token literal-property property">token_out_denom</span><span class="token operator">:</span>
                    <span class="token string">"ibc/27394FB092D2ECCD56123C74F36E4C1F926001CEADA9CA97EA622B25F41E5EB2"</span>
                <span class="token punctuation">}</span>
              <span class="token punctuation">]</span><span class="token punctuation">,</span>
              <span class="token literal-property property">sender</span><span class="token operator">:</span> <span class="token string">"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"</span><span class="token punctuation">,</span>
              <span class="token literal-property property">token_in</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">"10000"</span><span class="token punctuation">,</span>
                <span class="token literal-property property">denom</span><span class="token operator">:</span>
                  <span class="token string">"ibc/2DA9C149E9AD2BD27FEFA635458FB37093C256C1A940392634A16BEA45262604"</span>
              <span class="token punctuation">}</span><span class="token punctuation">,</span>
              <span class="token literal-property property">token_out_min_amount</span><span class="token operator">:</span> <span class="token string">"553"</span>
            <span class="token punctuation">}</span>
          <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token literal-property property">sequence</span><span class="token operator">:</span> <span class="token string">"54"</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectCosmosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">"cosmoshub-4"</span><span class="token punctuation">;</span>
    <span class="token comment">// Enabling before using the Keplr is recommended.</span>
    <span class="token comment">// This method will ask the user whether to allow access if they haven't visited this website.</span>
    <span class="token comment">// Also, it will request that the user unlock the wallet if the wallet is locked.</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span>chainId<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="签名信息" id="签名信息">签名信息<a class="index_header-anchor__Xqb+L" href="#签名信息" style="opacity:0">#</a></h2>
<p>#<code>window.okxwallet.keplr.signArbitrary(chainId, signer, data)</code></p>
<p><strong>描述</strong></p>
<p>签名任意信息，相当于之前几个链的 <code>signMessage(any)</code>。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token function">signArbitrary</span><span class="token punctuation">(</span>
    chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    signer<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    data<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> Uint8Array
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>StdSignature<span class="token operator">&gt;</span><span class="token punctuation">;</span>
<span class="token function">verifyArbitrary</span><span class="token punctuation">(</span>
    chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    signer<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    data<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> Uint8Array<span class="token punctuation">,</span>
    signature<span class="token operator">:</span> StdSignature
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">boolean</span><span class="token operator">&gt;</span><span class="token punctuation">;</span>

</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/NWLdgKL" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="send-tx-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Cosmos</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Sign Message</span></button><div></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R1vbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R1vbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R1vbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectCosmosButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Cosmos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>signMessageButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Sign Message<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R1vbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectCosmosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectCosmosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> signMessageButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.signMessageButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

signMessageButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span>  <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">signArbitrary</span><span class="token punctuation">(</span>
      <span class="token string">"osmosis-1"</span><span class="token punctuation">,</span>
      <span class="token string">"osmo1sxqwesgp7253fdv985csvz95fwc0q53ulldggl"</span><span class="token punctuation">,</span>
      <span class="token string">'test cosmos'</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectCosmosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">"cosmoshub-4"</span><span class="token punctuation">;</span>
    <span class="token comment">// Enabling before using the Keplr is recommended.</span>
    <span class="token comment">// This method will ask the user whether to allow access if they haven't visited this website.</span>
    <span class="token comment">// Also, it will request that the user unlock the wallet if the wallet is locked.</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span>chainId<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="事件" id="事件">事件<a class="index_header-anchor__Xqb+L" href="#事件" style="opacity:0">#</a></h2>
<p><strong>成功连接</strong></p>
<p>连接到欧易 Web3 钱包可以通过调用 <code>window.okxwallet.keplr.enable(chainId)</code>。 当用户接受连接请求时，会触发连接事件。</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>keplr<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"connected!"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/QWVdpzp" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Cosmos</span></button><p class="feedback-wrapper"><strong>Result: </strong> Cannot read properties of undefined (reading 'keplr')</p></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R2hbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R2hbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R2hbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectCosmosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Cosmos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R2hbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectCosmosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectCosmosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">"connect"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"connected!"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectCosmosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">"cosmoshub-4"</span><span class="token punctuation">;</span>
    <span class="token comment">// Enabling before using the Keplr is recommended.</span>
    <span class="token comment">// This method will ask the user whether to allow access if they haven't visited this website.</span>
    <span class="token comment">// Also, it will request that the user unlock the wallet if the wallet is locked.</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">keplr</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span>chainId<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "cosmos",
    "Provider API"
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
    "常见问题",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Tron",
    "Solana 兼容链",
    "TON",
    "Aptos/Movement"
  ],
  "toc": [
    "什么是 Injected provider API？",
    "连接账户",
    "签名交易",
    "签名信息",
    "事件"
  ]
}
```

</details>
