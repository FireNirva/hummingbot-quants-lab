# Provider API | aptos | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/aptos/provider#连接账户  
**抓取时间:** 2025-05-27 07:11:21  
**字数:** 1764

## 导航路径
DApp 连接钱包 > aptos > Provider API

## 目录
- Aptos-AIP-62
- 什么是 Injected provider API？
- 连接账户
- 获取账户信息
- 获取当前链接的网络
- 签名交易
- 签名信息
- 签名消息验证
- 事件

---

Provider API
#
Aptos-AIP-62
#
AIP-62
标准是Aptos推出的连接钱包的标准，OKX钱包已经支持AIP-62标准.
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
连接账户
#
window.okxwallet.aptos.connect()
描述
通过调用
window.okxwallet.aptos.connect()
连接欧易 Web3 钱包。
当成功调用
window.okxwallet.aptos.connect()
，将会唤起欧易 Web3 钱包连接钱包页面，用户可以决定是否连接当前 DApp，如果用户同意将会返回地址 (
address
) 和公钥 (
public key
)。
try
{
const
response
=
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
console
.
log
(
response
)
;
// { address: string, publicKey: string }
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
// { code: 4001, message: "User rejected the request."}
}
例子
在
codeopen
中打开。
Connect Aptos
Connect result:
"Cannot read properties of undefined (reading 'aptos')"
HTML
JavaScript
<
button
class
=
"
connectAptosButton
"
>
Connect Aptos
</
button
>
const
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
)
;
connectAptosButton
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
response
=
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
console
.
log
(
response
)
;
// { address: string, publicKey: string }
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
// { code: 4001, message: "User rejected the request."}
}
}
)
;
获取账户信息
#
window.okxwallet.aptos.account()
描述
调用
window.okxwallet.aptos.account()
，将会获取当前
Dapp
链接的账户信息，将会返回地址 (
address
) 和公钥 (
public key
)。
const
account
=
await
window
.
okxwallet
.
aptos
.
account
(
)
;
// { address: string, publicKey: string }
例子
在
codeopen
中打开。
Connect Aptos
Connect result:
"Cannot read properties of undefined (reading 'aptos')"
HTML
JavaScript
<
button
class
=
"
connectAptosButton
"
>
Connect Aptos
</
button
>
<
button
class
=
"
accountAptosButton
"
>
Account
</
button
>
const
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
)
;
const
accountAptosButton
=
document
.
querySelector
(
'.accountAptosButton'
)
;
connectAptosButton
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
response
=
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
console
.
log
(
response
)
;
// { address: string, publicKey: string }
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
// { code: 4001, message: "User rejected the request."}
}
}
)
;
accountAptosButton
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
const
account
=
await
window
.
okxwallet
.
aptos
.
account
(
)
;
console
.
log
(
account
)
;
// { address: string, publicKey: string }
}
)
;
获取当前链接的网络
#
window.okxwallet.aptos.network()
描述
调用
window.okxwallet.aptos.network()
，将会获取当前
Dapp
链接的网络信息，将会返回链接的网络名称。
const
network
=
await
window
.
okxwallet
.
aptos
.
network
(
)
;
// 'Mainnet'
// 目前支持的网络： `Mainnet` | `Movement Mainnet` | `Movement Testnet`
enum
Network
{
Mainnet
=
'Mainnet'
MovementMainnet
=
'Movement Mainnet'
MovementTestnet
=
'Movement Testnet'
}
例子
在
codeopen
中打开。
Connect Aptos
Connect result:
"Cannot read properties of undefined (reading 'aptos')"
HTML
JavaScript
<
button
class
=
"
connectAptosButton
"
>
Connect Aptos
</
button
>
<
button
class
=
"
networkAptosButton
"
>
Network
</
button
>
const
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
)
;
const
networkAptosButton
=
document
.
querySelector
(
'.networkAptosButton'
)
;
connectAptosButton
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
response
=
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
console
.
log
(
response
)
;
// { address: string, publicKey: string }
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
// { code: 4001, message: "User rejected the request."}
}
}
)
;
networkAptosButton
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
const
network
=
await
window
.
okxwallet
.
aptos
.
network
(
)
;
console
.
log
(
network
)
;
// 'Mainnet'
}
)
;
签名交易
#
window.okxwallet.aptos.signAndSubmitTransaction(transaction)
描述
在欧易 Web3 钱包中通过调用
window.okxwallet.aptos.signAndSubmitTransaction(transaction)
方法来发起一笔 Aptos 链上交易，这个方法将会返回一个待确认的交易信息给 DApp
const
transaction
=
{
arguments
:
[
address
,
'717'
]
,
function
:
'0x1::coin::transfer'
,
type
:
'entry_function_payload'
,
type_arguments
:
[
'0x1::aptos_coin::AptosCoin'
]
,
}
;
try
{
const
pendingTransaction
=
await
window
.
okxwallet
.
aptos
.
signAndSubmitTransaction
(
transaction
)
;
const
client
=
new
AptosClient
(
'https://fullnode.mainnet.aptoslabs.com/'
)
;
const
txn
=
await
client
.
waitForTransactionWithResult
(
pendingTransaction
.
hash
,
)
;
}
catch
(
error
)
{
// see "Errors"
}
当然也可以通过
window.okxwallet.aptos.signTransaction(transaction)
仅仅是签名交易，而不发起上链操作，此方法将返回一个签名的Buffer
提示
重要提醒：这个方法并不常用，而且对用户来说也非常的不安全，建议不要使用这个方法
const
transaction
=
{
arguments
:
[
address
,
'717'
]
,
function
:
'0x1::coin::transfer'
,
type
:
'entry_function_payload'
,
type_arguments
:
[
'0x1::aptos_coin::AptosCoin'
]
,
}
;
try
{
const
signTransaction
=
await
window
.
okxwallet
.
aptos
.
signTransaction
(
transaction
)
;
}
catch
(
error
)
{
// see "Errors"
}
例子
在
codeopen
中打开。
Connect Aptos
Send Transaction
HTML
JavaScript
<
button
class
=
"
connectAptosButton btn
"
>
Connect Aptos
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
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
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
let
address
=
''
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
transaction
=
{
arguments
:
[
address
,
'717'
]
,
function
:
'0x1::coin::transfer'
,
type
:
'entry_function_payload'
,
type_arguments
:
[
'0x1::aptos_coin::AptosCoin'
]
,
}
;
const
pendingTransaction
=
await
window
.
okxwallet
.
aptos
.
signAndSubmitTransaction
(
transaction
)
;
console
.
log
(
pendingTransaction
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
connectAptosButton
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
console
.
log
(
res
)
;
const
res
=
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
address
=
res
.
address
;
}
)
;
签名信息
#
window.okxwallet.aptos.signMessage(message)
描述
DApp 可以通过调用
window.okxwallet.aptos.signMessage(message)
来签名一段消息，当用户同意这个操作后，欧易 Web3 钱包将返回签名成功的信息、签名信息、入参和返回信息。结构如下：
参数
interface
SignMessagePayload
{
address
?
:
boolean
;
// Should we include the address of the account in the message
application
?
:
boolean
;
// Should we include the domain of the DApp
chainId
?
:
boolean
;
// Should we include the current chain id the wallet is connected to
message
:
string
;
// The message to be signed and displayed to the user
nonce
:
string
;
// A nonce the DApp should generate
}
返回值
interface
SignMessageResponse
{
address
:
string
;
application
:
string
;
chainId
:
number
;
fullMessage
:
string
;
// The message that was generated to sign
message
:
string
;
// The message passed in by the user
nonce
:
string
;
prefix
:
string
;
// Should always be APTOS
signature
:
string
;
// The signed full message
}
例子
在
codeopen
中打开。
Connect Aptos
Sign Message
HTML
JavaScript
<
button
class
=
"
connectAptosButton btn
"
>
Connect Aptos
</
button
>
<
button
class
=
"
signButton btn
"
>
Sign Message
</
button
>
const
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
)
;
const
signButton
=
document
.
querySelector
(
'.signButton'
)
;
const
signMessagePayload
=
{
message
:
'hello okx'
,
nonce
:
'okx'
}
;
signButton
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
signMessage
=
await
window
.
okxwallet
.
aptos
.
signMessage
(
signMessagePayload
)
console
.
log
(
signMessage
)
;
// {"signature": string, "prefix": "APTOS", "fullMessage": "APTOS nonce: okx message: hello okx", "message": "hello okx", "nonce": "okx" }
}
catch
(
error
)
{
// see "Errors"
}
}
)
;
connectAptosButton
.
addEventListener
(
'click'
,
(
)
=>
{
connetAccount
(
)
;
}
)
;
async
function
connetAccount
(
)
{
const
res
=
await
window
.
okxwallet
.
aptos
.
connect
(
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
签名消息验证
#
import
nacl
from
'tweetnacl'
;
const
message
=
'hello'
;
const
nonce
=
'random_string'
;
try
{
const
response
=
await
window
.
okxwallet
.
aptos
.
signMessage
(
{
message
,
nonce
,
}
)
;
const
{
publicKey
}
=
await
window
.
okxwallet
.
aptos
.
account
(
)
;
// Remove the 0x prefix
const
key
=
publicKey
!
.
slice
(
2
,
66
)
;
const
verified
=
nacl
.
sign
.
detached
.
verify
(
Buffer
.
from
(
response
.
fullMessage
)
,
Buffer
.
from
(
response
.
signature
,
'hex'
)
,
Buffer
.
from
(
key
,
'hex'
)
,
)
;
console
.
log
(
verified
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
error
(
error
)
;
}
事件
#
账户切换
当用户在切换欧易 Web3 钱包的时候，需要监听钱包切换事件：
onAccountChange
提示
重要提醒：用户切换的钱包的时候，目前账户必须有
Aptos
地址时才会触发。
let
currentAccount
=
await
window
.
okxwallet
.
aptos
.
account
(
)
;
// event listener for disconnecting
window
.
okxwallet
.
aptos
.
onAccountChange
(
(
newAccount
)
=>
{
// If the new account has already connected to your app then the newAccount will be returned
if
(
newAccount
)
{
currentAccount
=
newAccount
;
}
else
{
// Otherwise you will need to ask to connect to the new account
currentAccount
=
window
.
okxwallet
.
aptos
.
connect
(
)
;
}
}
)
;
onNetworkChange()
DApp 需要确保用户链接的是目标网络，因此需要获取当前网络、切换网络以及网络切换监听。
// 当前dapp链接的网络
let
network
=
await
window
.
okxwallet
.
aptos
.
network
(
)
;
// 监听链接的网络发生变化
window
.
bitkeep
.
aptos
.
onNetworkChange
(
(
newNetwork
)
=>
{
network
=
newNetwork
;
// { networkName: 'Mainnet' }
}
)
;
断开连接
当欧易 Web3 钱包断开连接的时候（欧易 Web3 钱包是多链钱包，当用户切换到的钱包不包含
Aptos
相关地址的时候，也会触发该事件）
// get current connection status
let
connectionStatus
=
await
window
.
okxwallet
.
aptos
.
isConnected
(
)
;
// event listener for disconnecting
window
.
okxwallet
.
aptos
.
onDisconnect
(
(
)
=>
{
connectionStatus
=
false
;
}
)
;
例子
在
codeopen
中打开。
Connect Aptos
Connect result:
"Cannot read properties of undefined (reading 'aptos')"
HTML
JavaScript
<
button
class
=
"
connectAptosButton
"
>
Connect Aptos
</
button
>
const
connectAptosButton
=
document
.
querySelector
(
'.connectAptosButton'
)
;
window
.
okxwallet
.
aptos
.
on
(
'connect'
,
(
)
=>
{
console
.
log
(
'got connect event'
)
;
}
)
connectAptosButton
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
await
window
.
okxwallet
.
aptos
.
connect
(
)
;
console
.
log
(
res
)
;
// { address: string, publicKey: string }
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
// { code: 4001, message: "User rejected the request."}
}
}
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="Aptos-AIP-62" id="aptos-aip-62">Aptos-AIP-62<a class="index_header-anchor__Xqb+L" href="#aptos-aip-62" style="opacity:0">#</a></h2>
<p><a class="items-center" href="https://aptos.dev/en/build/sdks/wallet-adapter/wallets" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">AIP-62<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>标准是Aptos推出的连接钱包的标准，OKX钱包已经支持AIP-62标准.</p>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="连接账户" id="连接账户">连接账户<a class="index_header-anchor__Xqb+L" href="#连接账户" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.aptos.connect()</code></p>
<p><strong>描述</strong></p>
<p>通过调用 <code>window.okxwallet.aptos.connect()</code> 连接欧易 Web3 钱包。</p>
<p>当成功调用 <code>window.okxwallet.aptos.connect()</code>，将会唤起欧易 Web3 钱包连接钱包页面，用户可以决定是否连接当前 DApp，如果用户同意将会返回地址 (<code>address</code>) 和公钥 (<code>public key</code>)。</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
  <span class="token punctuation">}</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/NWLbxKx" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><div class="feedback-wrapper"><strong>Connect result: </strong><span style="font-family: monospace;">"Cannot read properties of undefined (reading 'aptos')"</span></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":Rtbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":Rtbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":Rtbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":Rtbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="获取账户信息" id="获取账户信息">获取账户信息<a class="index_header-anchor__Xqb+L" href="#获取账户信息" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.aptos.account()</code></p>
<p><strong>描述</strong></p>
<p>调用 <code>window.okxwallet.aptos.account()</code>，将会获取当前 <code>Dapp</code> 链接的账户信息，将会返回地址 (<code>address</code>) 和公钥 (<code>public key</code>)。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> account <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// { address: string, publicKey: string }</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/lsbwfyzl-the-reactor/pen/QWXpgZo" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><div class="feedback-wrapper"><strong>Connect result: </strong><span style="font-family: monospace;">"Cannot read properties of undefined (reading 'aptos')"</span></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R1fbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R1fbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R1fbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>accountAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Account<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R1fbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> accountAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.accountAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>


accountAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> account <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>account<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token comment">// { address: string, publicKey: string }</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

</code></pre></div></div></div></div>
<h2 data-content="获取当前链接的网络" id="获取当前链接的网络">获取当前链接的网络<a class="index_header-anchor__Xqb+L" href="#获取当前链接的网络" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.aptos.network()</code></p>
<p><strong>描述</strong></p>
<p>调用 <code>window.okxwallet.aptos.network()</code>，将会获取当前 <code>Dapp</code> 链接的网络信息，将会返回链接的网络名称。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> network <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">network</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// 'Mainnet'</span>
</code></pre></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 目前支持的网络： `Mainnet` | `Movement Mainnet` | `Movement Testnet`</span>
<span class="token keyword">enum</span> Network <span class="token punctuation">{</span>
  Mainnet <span class="token operator">=</span> <span class="token string">'Mainnet'</span>
  MovementMainnet <span class="token operator">=</span> <span class="token string">'Movement Mainnet'</span>
  MovementTestnet <span class="token operator">=</span> <span class="token string">'Movement Testnet'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/lsbwfyzl-the-reactor/pen/dyBvzGJ" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><div class="feedback-wrapper"><strong>Connect result: </strong><span style="font-family: monospace;">"Cannot read properties of undefined (reading 'aptos')"</span></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R23bf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R23bf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R23bf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>networkAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Network<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R23bf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> networkAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.networkAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>


networkAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> network <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">network</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>network<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token comment">// 'Mainnet'</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

</code></pre></div></div></div></div>
<h2 data-content="签名交易" id="签名交易">签名交易<a class="index_header-anchor__Xqb+L" href="#签名交易" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.aptos.signAndSubmitTransaction(transaction)</code></p>
<p><strong>描述</strong></p>
<p>在欧易 Web3 钱包中通过调用 <code>window.okxwallet.aptos.signAndSubmitTransaction(transaction)</code> 方法来发起一笔 Aptos 链上交易，这个方法将会返回一个待确认的交易信息给 DApp</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span>address<span class="token punctuation">,</span> <span class="token string">'717'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token keyword">function</span><span class="token operator">:</span> <span class="token string">'0x1::coin::transfer'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'entry_function_payload'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">type_arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'0x1::aptos_coin::AptosCoin'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> pendingTransaction <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">signAndSubmitTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">AptosClient</span><span class="token punctuation">(</span><span class="token string">'https://fullnode.mainnet.aptoslabs.com/'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> txn <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">waitForTransactionWithResult</span><span class="token punctuation">(</span>
      pendingTransaction<span class="token punctuation">.</span><span class="token property-access">hash</span><span class="token punctuation">,</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// see "Errors"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>当然也可以通过 <code>window.okxwallet.aptos.signTransaction(transaction)</code> 仅仅是签名交易，而不发起上链操作，此方法将返回一个签名的Buffer</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R2hbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R2hbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">重要提醒：这个方法并不常用，而且对用户来说也非常的不安全，建议不要使用这个方法</div></div></div></div></div>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span>address<span class="token punctuation">,</span> <span class="token string">'717'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token keyword">function</span><span class="token operator">:</span> <span class="token string">'0x1::coin::transfer'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'entry_function_payload'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">type_arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'0x1::aptos_coin::AptosCoin'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> signTransaction <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// see "Errors"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/qBMqbbJ" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Send Transaction</span></button><div class="feedback-wrapper"></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R2rbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R2rbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R2rbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>signTransactionButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Sign Transaction<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R2rbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> signTransactionButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.signTransactionButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">let</span> address<span class="token operator">=</span><span class="token string">''</span><span class="token punctuation">;</span>

signTransactionButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span>address<span class="token punctuation">,</span> <span class="token string">'717'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token keyword">function</span><span class="token operator">:</span> <span class="token string">'0x1::coin::transfer'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'entry_function_payload'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">type_arguments</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'0x1::aptos_coin::AptosCoin'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> pendingTransaction <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">signAndSubmitTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>pendingTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
   <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
   <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
   address <span class="token operator">=</span> res<span class="token punctuation">.</span><span class="token property-access">address</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="签名信息" id="签名信息">签名信息<a class="index_header-anchor__Xqb+L" href="#签名信息" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.aptos.signMessage(message)</code></p>
<p><strong>描述</strong></p>
<p>DApp 可以通过调用 <code>window.okxwallet.aptos.signMessage(message)</code> 来签名一段消息，当用户同意这个操作后，欧易 Web3 钱包将返回签名成功的信息、签名信息、入参和返回信息。结构如下：</p>
<p><strong>参数</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">SignMessagePayload</span> <span class="token punctuation">{</span>
  address<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">boolean</span><span class="token punctuation">;</span> <span class="token comment">// Should we include the address of the account in the message</span>
  application<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">boolean</span><span class="token punctuation">;</span> <span class="token comment">// Should we include the domain of the DApp</span>
  chainId<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">boolean</span><span class="token punctuation">;</span> <span class="token comment">// Should we include the current chain id the wallet is connected to</span>
  message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// The message to be signed and displayed to the user</span>
  nonce<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// A nonce the DApp should generate</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>返回值</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">SignMessageResponse</span> <span class="token punctuation">{</span>
  address<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  application<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  chainId<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
  fullMessage<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// The message that was generated to sign</span>
  message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// The message passed in by the user</span>
  nonce<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  prefix<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// Should always be APTOS</span>
  signature<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// The signed full message</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/RwYorBP" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Sign Message</span></button><div class="feedback-wrapper"></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R3jbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R3jbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R3jbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>signButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Sign Message<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R3jbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> signButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.signButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> signMessagePayload <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">message</span><span class="token operator">:</span> <span class="token string">'hello okx'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">nonce</span><span class="token operator">:</span> <span class="token string">'okx'</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

signButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> signMessage <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span>signMessagePayload<span class="token punctuation">)</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>signMessage<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// {"signature": string, "prefix": "APTOS", "fullMessage": "APTOS nonce: okx message: hello okx", "message": "hello okx", "nonce": "okx" }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// see "Errors"</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token function">connetAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">connetAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div></div>
<h2 data-content="签名消息验证" id="签名消息验证">签名消息验证<a class="index_header-anchor__Xqb+L" href="#签名消息验证" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword module">import</span> <span class="token imports">nacl</span> <span class="token keyword module">from</span> <span class="token string">'tweetnacl'</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> message <span class="token operator">=</span> <span class="token string">'hello'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token string">'random_string'</span><span class="token punctuation">;</span>

<span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        message<span class="token punctuation">,</span>
        nonce<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> <span class="token punctuation">{</span> publicKey <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Remove the 0x prefix</span>
    <span class="token keyword">const</span> key <span class="token operator">=</span> publicKey<span class="token operator">!</span><span class="token punctuation">.</span><span class="token method function property-access">slice</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">,</span> <span class="token number">66</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> verified <span class="token operator">=</span> nacl<span class="token punctuation">.</span><span class="token property-access">sign</span><span class="token punctuation">.</span><span class="token property-access">detached</span><span class="token punctuation">.</span><span class="token method function property-access">verify</span><span class="token punctuation">(</span>
        <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>response<span class="token punctuation">.</span><span class="token property-access">fullMessage</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>response<span class="token punctuation">.</span><span class="token property-access">signature</span><span class="token punctuation">,</span> <span class="token string">'hex'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>key<span class="token punctuation">,</span> <span class="token string">'hex'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>verified<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="事件" id="事件">事件<a class="index_header-anchor__Xqb+L" href="#事件" style="opacity:0">#</a></h2>
<p><strong>账户切换</strong></p>
<p>当用户在切换欧易 Web3 钱包的时候，需要监听钱包切换事件：<code>onAccountChange</code></p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R3vbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R3vbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">重要提醒：用户切换的钱包的时候，目前账户必须有 <code>Aptos</code> 地址时才会触发。</div></div></div></div></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">let</span> currentAccount <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">account</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// event listener for disconnecting</span>
window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">onAccountChange</span><span class="token punctuation">(</span><span class="token punctuation">(</span>newAccount<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// If the new account has already connected to your app then the newAccount will be returned</span>
  <span class="token keyword">if</span> <span class="token punctuation">(</span>newAccount<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    currentAccount <span class="token operator">=</span> newAccount<span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
    <span class="token comment">// Otherwise you will need to ask to connect to the new account</span>
    currentAccount <span class="token operator">=</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>onNetworkChange()</strong></p>
<p>DApp 需要确保用户链接的是目标网络，因此需要获取当前网络、切换网络以及网络切换监听。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 当前dapp链接的网络</span>
<span class="token keyword">let</span> network <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">network</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 监听链接的网络发生变化</span>
window<span class="token punctuation">.</span>bitkeep<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">onNetworkChange</span><span class="token punctuation">(</span><span class="token punctuation">(</span>newNetwork<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  network <span class="token operator">=</span> newNetwork<span class="token punctuation">;</span> <span class="token comment">// { networkName: 'Mainnet' }</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>断开连接</strong></p>
<p>当欧易 Web3 钱包断开连接的时候（欧易 Web3 钱包是多链钱包，当用户切换到的钱包不包含 <code>Aptos</code> 相关地址的时候，也会触发该事件）</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// get current connection status</span>
<span class="token keyword">let</span> connectionStatus <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">isConnected</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// event listener for disconnecting</span>
window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>aptos<span class="token punctuation">.</span><span class="token function">onDisconnect</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  connectionStatus <span class="token operator">=</span> <span class="token boolean">false</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/PodbZEN" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Aptos</span></button><div class="feedback-wrapper"><strong>Connect result: </strong><span style="font-family: monospace;">"Cannot read properties of undefined (reading 'aptos')"</span></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R4lbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R4lbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R4lbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectAptosButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Aptos<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R4lbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectAptosButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectAptosButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'connect'</span><span class="token punctuation">,</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token arrow operator">=&gt;</span><span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'got connect event'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>

connectAptosButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> res <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">aptos</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
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
    "aptos",
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
    "Aptos-AIP-62",
    "什么是 Injected provider API？",
    "连接账户",
    "获取账户信息",
    "获取当前链接的网络",
    "签名交易",
    "签名信息",
    "签名消息验证",
    "事件"
  ]
}
```

</details>
