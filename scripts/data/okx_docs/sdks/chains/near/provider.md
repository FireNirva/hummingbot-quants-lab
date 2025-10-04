# Provider API | near | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/near/provider#什么是-injected-provider-api？  
**抓取时间:** 2025-05-27 06:19:17  
**字数:** 647

## 导航路径
DApp 连接钱包 > near > Provider API

## 目录
- 什么是 Injected provider API？
- 获取注入的对象
- 连接钱包
- signMessage
- 合约交互
- 事件

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
获取注入的对象
#
Dapp 可以通过如下方式访问注入的对象：
window.okxwallet.near
- 推荐
window.near
连接钱包
#
requestSignIn()
#
/**
*
@param
{
String
}
contractId
contract account id
*
@param
{
Array
}
methodNames
methods on the contract should be allowed to be called.
*
@returns
{
accountId
,
accessKey
}
accountId and signed in access key
*/
window
.
okxwallet
.
near
.
requestSignIn
(
{
contractId
=
''
,
methodNames
=
[
]
}
)
:
Promise
<
Result
>
仅获取 accountId
#
不传 contractId 和 methodNames 只会获取到用户的 NEAR 地址.
try
{
const
{
accountId
}
=
window
.
okxwallet
.
near
.
requestSignIn
(
)
;
}
catch
(
_
)
{
// something error
}
返回值示例:
{
"accountId"
:
"efad2c...9dae"
,
}
获取 accessKey
#
传入 contractId 和 methodNames, 钱包会返回 accessKey
const
contractId
=
'wrap.near'
;
const
methodNames
=
[
'ft_metadata'
]
;
try
{
const
{
accountId
,
accessKey
}
=
window
.
okxwallet
.
near
.
requestSignIn
(
{
contractId
,
methodNames
}
)
;
}
catch
(
_
)
{
// something error
}
返回值示例:
{
"accountId"
:
"efad2c...9dae"
,
"accessKey"
:
{
"secretKey"
:
"5S9Ngi...Uku6"
,
"publicKey"
:
"ed25519:9RivAy...Hxc8"
}
}
signOut()
#
断开钱包连接
window
.
okxwallet
.
near
.
signOut
(
)
:
void
;
isSignedIn()
#
判断当前账户是否处于连接中状态
window
.
okxwallet
.
near
.
isSignedIn
(
)
:
boolean
;
getAccountId()
#
获取当前连接的 accountId
window
.
okxwallet
.
near
.
getAccountId
(
)
:
string
;
signMessage
#
near
.
signMessage
(
{
message
:
string
,
recipient
:
string
,
nonce
:
Buffer
}
)
:
Response
;
签名, 示例:
const
message
=
{
message
:
'hello world'
,
recipient
:
'test.testnet'
,
nonce
:
Buffer
.
from
(
"4268ebc14ff247f5450d4a8682bec3729a06d268f83b0cb363083ab05b65486b"
,
"hex"
)
}
const
result
=
await
window
.
okxwallet
.
near
.
signMessage
(
message
)
;
返回值示例:
{
"accountId"
:
"efad2c...9dae"
,
"publicKey"
:
"ed25519:H8bbdL...ucKF"
,
"signature"
:
"zYbw0Z+YabpZTnYA1REkvAX5KeXt/qRgHkorYfjRR5dD5keySfFuWGMafkfi/RPUpG1EAqbUf9VFt4tTBebcDQ=="
}
合约交互
#
signAndSendTransaction()
#
near
.
signAndSendTransaction
(
{
receiverId
:
string
,
actions
:
Action
[
]
}
)
:
Response
;
签名并广播交易, 示例:
const
tx
=
{
receiverId
:
'wrap.near'
,
actions
:
[
{
methodName
:
'near_deposit'
,
args
:
{
}
,
deposit
:
'1250000000000000000000'
,
}
,
]
,
}
const
result
=
await
window
.
okxwallet
.
near
.
signAndSendTransaction
(
tx
)
;
返回值示例:
{
"method"
:
"signAndSendTransaction"
,
"txHash"
:
"2bNbuT...UdSA"
,
"code"
:
0
}
注意: dapp 需要通过 txHash 获取交易广播的结果
requestSignTransactions()
#
near
.
requestSignTransactions
(
{
transactions
:
Transaction
[
]
}
)
:
Response
;
批量签名交易, 示例:
const
transactions
=
[
{
receiverId
:
'wrap.near'
,
actions
:
[
{
methodName
:
'near_deposit'
,
args
:
{
}
,
deposit
:
'1000000000000000'
,
}
,
]
,
}
,
{
receiverId
:
'wrap.near'
,
actions
:
[
{
methodName
:
'ft_transfer'
,
args
:
{
receiver_id
:
'efad2c...9dae'
,
amount
:
'10000000000'
,
}
,
deposit
:
'1'
,
}
,
]
,
}
,
]
const
result
=
await
window
.
okxwallet
.
near
.
signAndSendTransaction
(
{
transactions
}
)
;
返回值示例:
{
"txs"
:
[
{
"signedTx"
:
"QAAAAG...kAoH"
,
"txHash"
:
"71MuUA...KVxt"
}
,
{
"signedTx"
:
"QAAAAG...gksH"
,
"txHash"
:
"8RHzw4...hvLN"
}
]
,
"code"
:
0
,
"method"
:
"requestSignTransactions"
}
注意: 批量签名交易钱包只会签名, 不会广播. dapp 侧需要承接广播的逻辑.
事件
#
signIn
#
连接钱包成功
window
.
okxwallet
.
near
.
on
(
"signIn"
,
(
(
accountId
)
=>
{
// accountId: 当前连接账户的 accountId
}
)
;
signOut
#
连接钱包成功
window
.
okxwallet
.
near
.
on
(
"signIn"
,
(
(
)
=>
{
// do something
}
)
;
accountChanged
#
钱包侧切换了账户
window
.
okxwallet
.
near
.
on
(
"accountChanged"
,
(
(
accountId
)
=>
{
// accountId: 切换后账户的 accountId
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
<h2 data-content="获取注入的对象" id="获取注入的对象">获取注入的对象<a class="index_header-anchor__Xqb+L" href="#获取注入的对象" style="opacity:0">#</a></h2>
<p>Dapp 可以通过如下方式访问注入的对象：</p>
<ul>
<li><code>window.okxwallet.near</code> - 推荐</li>
<li><code>window.near</code></li>
</ul>
<h2 data-content="连接钱包" id="连接钱包">连接钱包<a class="index_header-anchor__Xqb+L" href="#连接钱包" style="opacity:0">#</a></h2>
<h3 id="requestsignin()">requestSignIn()<a class="index_header-anchor__Xqb+L" href="#requestsignin()" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token doc-comment comment">/**
* <span class="token keyword">@param</span> <span class="token class-name"><span class="token punctuation">{</span>String<span class="token punctuation">}</span></span> <span class="token parameter">contractId</span> contract account id
* <span class="token keyword">@param</span> <span class="token class-name"><span class="token punctuation">{</span>Array<span class="token punctuation">}</span></span> <span class="token parameter">methodNames</span> methods on the contract should be allowed to be called.
* <span class="token keyword">@returns</span> <span class="token class-name"><span class="token punctuation">{</span> accountId<span class="token punctuation">,</span> accessKey <span class="token punctuation">}</span></span> accountId and signed in access key
*/</span>
<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">requestSignIn</span><span class="token punctuation">(</span><span class="token punctuation">{</span> contractId <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">,</span> methodNames <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token known-class-name class-name">Promise</span><span class="token operator">&lt;</span><span class="token maybe-class-name">Result</span><span class="token operator">&gt;</span>
</code></pre></div>
<h4 id="仅获取-accountid">仅获取 accountId<a class="index_header-anchor__Xqb+L" href="#仅获取-accountid" style="opacity:0">#</a></h4>
<p>不传 contractId 和 methodNames 只会获取到用户的 NEAR 地址.</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> accountId <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">requestSignIn</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>_<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// something error</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>返回值示例:</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"accountId"</span><span class="token operator">:</span> <span class="token string">"efad2c...9dae"</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h4 id="获取-accesskey">获取 accessKey<a class="index_header-anchor__Xqb+L" href="#获取-accesskey" style="opacity:0">#</a></h4>
<p>传入 contractId 和 methodNames, 钱包会返回 accessKey</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> contractId <span class="token operator">=</span> <span class="token string">'wrap.near'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> methodNames <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token string">'ft_metadata'</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> accountId<span class="token punctuation">,</span> accessKey <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">requestSignIn</span><span class="token punctuation">(</span><span class="token punctuation">{</span> contractId<span class="token punctuation">,</span> methodNames <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>_<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// something error</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>返回值示例:</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"accountId"</span><span class="token operator">:</span> <span class="token string">"efad2c...9dae"</span><span class="token punctuation">,</span>
    <span class="token property">"accessKey"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"secretKey"</span><span class="token operator">:</span> <span class="token string">"5S9Ngi...Uku6"</span><span class="token punctuation">,</span>
        <span class="token property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"ed25519:9RivAy...Hxc8"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h3 id="signout()">signOut()<a class="index_header-anchor__Xqb+L" href="#signout()" style="opacity:0">#</a></h3>
<p>断开钱包连接</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">signOut</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token keyword">void</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="issignedin()">isSignedIn()<a class="index_header-anchor__Xqb+L" href="#issignedin()" style="opacity:0">#</a></h3>
<p>判断当前账户是否处于连接中状态</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">isSignedIn</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> boolean<span class="token punctuation">;</span>
</code></pre></div>
<h3 id="getaccountid()">getAccountId()<a class="index_header-anchor__Xqb+L" href="#getaccountid()" style="opacity:0">#</a></h3>
<p>获取当前连接的 accountId</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">getAccountId</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> string<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="signMessage" id="signmessage">signMessage<a class="index_header-anchor__Xqb+L" href="#signmessage" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-js"><code class="language-js">near<span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">message</span><span class="token operator">:</span> string<span class="token punctuation">,</span> <span class="token literal-property property">recipient</span><span class="token operator">:</span> string<span class="token punctuation">,</span> <span class="token literal-property property">nonce</span><span class="token operator">:</span> <span class="token maybe-class-name">Buffer</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token maybe-class-name">Response</span><span class="token punctuation">;</span>
</code></pre></div>
<p>签名, 示例:</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> message <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">message</span><span class="token operator">:</span> <span class="token string">'hello world'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">recipient</span><span class="token operator">:</span> <span class="token string">'test.testnet'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">nonce</span><span class="token operator">:</span> <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span><span class="token string">"4268ebc14ff247f5450d4a8682bec3729a06d268f83b0cb363083ab05b65486b"</span><span class="token punctuation">,</span> <span class="token string">"hex"</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>返回值示例:</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"accountId"</span><span class="token operator">:</span> <span class="token string">"efad2c...9dae"</span><span class="token punctuation">,</span>
    <span class="token property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"ed25519:H8bbdL...ucKF"</span><span class="token punctuation">,</span>
    <span class="token property">"signature"</span><span class="token operator">:</span> <span class="token string">"zYbw0Z+YabpZTnYA1REkvAX5KeXt/qRgHkorYfjRR5dD5keySfFuWGMafkfi/RPUpG1EAqbUf9VFt4tTBebcDQ=="</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="合约交互" id="合约交互">合约交互<a class="index_header-anchor__Xqb+L" href="#合约交互" style="opacity:0">#</a></h2>
<h3 id="signandsendtransaction()">signAndSendTransaction()<a class="index_header-anchor__Xqb+L" href="#signandsendtransaction()" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js">near<span class="token punctuation">.</span><span class="token method function property-access">signAndSendTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">receiverId</span><span class="token operator">:</span> string<span class="token punctuation">,</span> <span class="token literal-property property">actions</span><span class="token operator">:</span> <span class="token maybe-class-name">Action</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token maybe-class-name">Response</span><span class="token punctuation">;</span>
</code></pre></div>
<p>签名并广播交易, 示例:</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> tx <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">receiverId</span><span class="token operator">:</span> <span class="token string">'wrap.near'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">actions</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token literal-property property">methodName</span><span class="token operator">:</span> <span class="token string">'near_deposit'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">args</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token literal-property property">deposit</span><span class="token operator">:</span> <span class="token string">'1250000000000000000000'</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">signAndSendTransaction</span><span class="token punctuation">(</span>tx<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>返回值示例:</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"method"</span><span class="token operator">:</span> <span class="token string">"signAndSendTransaction"</span><span class="token punctuation">,</span>
    <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"2bNbuT...UdSA"</span><span class="token punctuation">,</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token number">0</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>注意: dapp 需要通过 txHash 获取交易广播的结果</p>
<h3 id="requestsigntransactions()">requestSignTransactions()<a class="index_header-anchor__Xqb+L" href="#requestsigntransactions()" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js">near<span class="token punctuation">.</span><span class="token method function property-access">requestSignTransactions</span><span class="token punctuation">(</span><span class="token punctuation">{</span><span class="token literal-property property">transactions</span><span class="token operator">:</span> <span class="token maybe-class-name">Transaction</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token maybe-class-name">Response</span><span class="token punctuation">;</span>
</code></pre></div>
<p>批量签名交易, 示例:</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> transactions <span class="token operator">=</span> <span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
    <span class="token literal-property property">receiverId</span><span class="token operator">:</span> <span class="token string">'wrap.near'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">actions</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">methodName</span><span class="token operator">:</span> <span class="token string">'near_deposit'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">args</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">deposit</span><span class="token operator">:</span> <span class="token string">'1000000000000000'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token literal-property property">receiverId</span><span class="token operator">:</span> <span class="token string">'wrap.near'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">actions</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">methodName</span><span class="token operator">:</span> <span class="token string">'ft_transfer'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">args</span><span class="token operator">:</span> <span class="token punctuation">{</span>
          <span class="token literal-property property">receiver_id</span><span class="token operator">:</span> <span class="token string">'efad2c...9dae'</span><span class="token punctuation">,</span>
          <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'10000000000'</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">deposit</span><span class="token operator">:</span> <span class="token string">'1'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">]</span>

<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">signAndSendTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span> transactions <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>返回值示例:</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"txs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"signedTx"</span><span class="token operator">:</span> <span class="token string">"QAAAAG...kAoH"</span><span class="token punctuation">,</span>
            <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"71MuUA...KVxt"</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span>
            <span class="token property">"signedTx"</span><span class="token operator">:</span> <span class="token string">"QAAAAG...gksH"</span><span class="token punctuation">,</span>
            <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"8RHzw4...hvLN"</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
    <span class="token property">"method"</span><span class="token operator">:</span> <span class="token string">"requestSignTransactions"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>注意: 批量签名交易钱包只会签名, 不会广播. dapp 侧需要承接广播的逻辑.</p>
<h2 data-content="事件" id="事件">事件<a class="index_header-anchor__Xqb+L" href="#事件" style="opacity:0">#</a></h2>
<h3 id="signin">signIn<a class="index_header-anchor__Xqb+L" href="#signin" style="opacity:0">#</a></h3>
<p>连接钱包成功</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">"signIn"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">accountId</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// accountId: 当前连接账户的 accountId</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="signout">signOut<a class="index_header-anchor__Xqb+L" href="#signout" style="opacity:0">#</a></h3>
<p>连接钱包成功</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">"signIn"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// do something</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="accountchanged">accountChanged<a class="index_header-anchor__Xqb+L" href="#accountchanged" style="opacity:0">#</a></h3>
<p>钱包侧切换了账户</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">near</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">"accountChanged"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">accountId</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// accountId: 切换后账户的 accountId</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "near",
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
    "获取注入的对象",
    "连接钱包",
    "signMessage",
    "合约交互",
    "事件"
  ]
}
```

</details>
