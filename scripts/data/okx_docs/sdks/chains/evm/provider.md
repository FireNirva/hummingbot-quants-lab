# Provider API | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/provider#wallet_watchasset  
**抓取时间:** 2025-05-27 06:51:39  
**字数:** 943

## 导航路径
DApp 连接钱包 > EVM > Provider API

## 目录
- 什么是 Injected provider API？
- 连接账户
- 添加代币
- 事件

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
连接账户
#
eth_requestAccounts
EIP-1102
此方法由
EIP-1102
指定。
在底层逻辑上，它调用
wallet_requestPermissions
以获得
eth_accounts
权限。由于目前来说
eth_accounts
是唯一的权限，所以你现在仅需此方法。
描述
此方法请求用户提供一个以太坊地址来识别。返回值为一个解析为单个以太坊地址字符串数组的 Promise。如果用户拒绝该请求，Promise 将被拒绝并返回
4001
错误。
该请求会导致一个欧易的弹窗出现。你应该只在响应用户操作时请求账户，比如一个用户在单击按钮的时候。在请求仍处于待处理状态时，你应该始终禁用导致请求被分派的按钮。
如果你无法检索用户的账户，你应该鼓励用户发起账户请求。
返回值
string[]
- 单个十六进制以太坊地址字符串的数组。
例子
在
codeopen
中打开。
Connect Ethereum
HTML
JavaScript
<
button
class
=
"
connectEthereumButton
"
>
Connect Ethereum
</
button
>
const
connectEthereumButton
=
document
.
querySelector
(
'.connectEthereumButton'
)
;
connectEthereumButton
.
addEventListener
(
'click'
,
(
)
=>
{
//Will Start the OKX extension
okxwallet
.
request
(
{
method
:
'eth_requestAccounts'
}
)
;
}
)
;
添加代币
#
Note
: 该功能仅在欧易 Web3 钱包插件端支持。
wallet_watchAsset
#
EIP-747
此方法由
EIP-747
指定。
描述
此方法请求用户在欧易中关注某代币。返回一个布尔值，这个布尔值代表着代币是否已成功添加。
大多数以太坊钱包都支持关注一组代币，这些代币通常来自集中管理的代币注册表。
wallet_watchAsset
让 Web3 应用程序开发人员能够在运行时询问他们的用户去关注他们钱包中的代币。新添加的代币与通过原始方法（例如集中式注册表）添加的代币没有任何区别。
参数
WatchAssetParams
- 要关注的资产的元数据。
interface
WatchAssetParams
{
type
:
'ERC20'
;
// In the future, other standards will be supported
options
:
{
address
:
string
;
// The address of the token contract
'symbol'
:
string
;
// A ticker symbol or shorthand, up to 11 characters
decimals
:
number
;
// The number of token decimals
image
:
string
;
// A string url of the token logo
}
;
}
返回值
boolean
- 如果添加了代币为
true
，否则为
false
。
例子
在
codeopen
中打开。
Connect Ethereum
Add Token
HTML
JavaScript
<
button
class
=
"
connectEthereumButton btn
"
>
Connect Ethereum
</
button
>
<
button
class
=
"
addTokenButton btn
"
>
Add Token
</
button
>
const
ethereumButton
=
document
.
querySelector
(
'.connectEthereumButton'
)
;
const
addTokenButton
=
document
.
querySelector
(
'.addTokenButton'
)
;
addTokenButton
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
await
okxwallet
.
request
(
{
method
:
'wallet_switchEthereumChain'
,
params
:
[
{
chainId
:
'0x1'
}
]
}
)
;
okxwallet
.
request
(
{
method
:
'wallet_watchAsset'
,
params
:
{
type
:
'ERC20'
,
options
:
{
address
:
'0xdac17f958d2ee523a2206206994597c13d831ec7'
,
symbol
:
'USDT'
,
decimals
:
6
,
image
:
'https://foo.io/token-image.svg'
,
}
,
}
,
}
)
.
then
(
(
success
)
=>
{
if
(
success
)
{
console
.
log
(
'USDT successfully added to wallet!'
)
;
}
else
{
throw
new
Error
(
'Something went wrong.'
)
;
}
}
)
.
catch
(
console
.
error
)
;
}
)
;
ethereumButton
.
addEventListener
(
'click'
,
(
)
=>
{
getAccount
(
)
;
}
)
;
function
getAccount
(
)
{
okxwallet
.
request
(
{
method
:
'eth_requestAccounts'
}
)
.
catch
(
(
error
)
=>
{
console
.
log
(
error
)
;
}
)
;
}
事件
#
欧易提供者实现了
Node.js
EventEmitter
API。
本节详细介绍了通过该 API 发出的事件。
网络上有其他各式各样的
EventEmitter
指南可供参考，本指南列出了如下一些事件：
okxwallet
.
on
(
'accountsChanged'
,
(
accounts
)
=>
{
// Handle the new accounts, or lack thereof.
// "accounts" will always be an array, but it can be empty.
}
)
;
okxwallet
.
on
(
'chainChanged'
,
(
chainId
)
=>
{
// Handle the new chain.
// Correctly handling chain changes can be complicated.
// We recommend reloading the page unless you have a very good reason not to.
window
.
location
.
reload
(
)
;
}
)
;
另外，一旦你使用完监听器，请不要忘记将其删除（例如在 React 中卸载组件时）：
function
handleAccountsChanged
(
accounts
)
{
// ...
}
okxwallet
.
on
(
'accountsChanged'
,
handleAccountsChanged
)
;
// Later
okxwallet
.
removeListener
(
'accountsChanged'
,
handleAccountsChanged
)
;
okxwallet.removeListener
的第一个参数是事件名称，第二个参数是对已传递给第一个参数中提到的事件名称的
okxwallet.on
的同一函数的引用。
connect
interface
ConnectInfo
{
chainId
:
string
;
}
okxwallet
.
on
(
'connect'
,
handler
:
(
connectInfo
:
ConnectInfo
)
=>
void
)
;
欧易提供者会在第一次能够向链提交 RPC 请求时发出此事件。我们建议使用
connect
事件处理程序和
okxwallet.isConnected()
方法来确定欧易提供者的连接状态和连接时间。
disconnect
okxwallet
.
on
(
'disconnect'
,
handler
:
(
error
:
ProviderRpcError
)
=>
void
)
;
如果欧易提供者无法向任何链提交 RPC 请求，则会发出此事件。通常，这只会发生在网络连接问题或某些其他不可预见的错误状态下。
一旦发出
disconnect
，提供者直到重新建立与链的连接之前将不会接受任何新请求，建立新连接需要重新加载页面。你还可以使用
okxwallet.isConnected()
方法来确定提供程序是否已断开连接。
accountsChanged
okxwallet
.
on
(
'accountsChanged'
,
handler
:
(
accounts
:
Array
<
string
>
)
=>
void
)
;
每当
eth_accounts
RPC 方法的返回值发生变化时，欧易提供程序都会发出此事件。
eth_accounts
会返回一个为空或包含单个账户地址的数组。返回的地址（如果存在）即为允许调用者访问的最近使用的账户地址。由于调用者由其 URL
origin
标识，所以具有相同来源(origin)的站点会持有相同的权限。
只要用户公开的账户地址发生变化，就会发出
accountsChanged
.
提示
我们计划在不久的将来允许
eth_accounts
数组能够包含多个地址。
chainChanged
提示
欧易的默认链及其链 ID 请参见
Chain IDs section
。
当前连接的链发生变化时，欧易提供者会发出此事件。
所有的 RPC 请求都提交到当前连接的链上。因此，通过侦听此事件来跟踪当前链 ID 是至关重要的。
我们强烈建议在链更改时重新加载页面，当然你也可以通过需求自行选择。
okxwallet
.
on
(
'chainChanged'
,
(
_chainId
)
=>
window
.
location
.
reload
(
)
)
;
message
interface
ProviderMessage
{
type
:
string
;
data
:
unknown
;
}
okxwallet
.
on
(
'message'
,
handler
:
(
message
:
ProviderMessage
)
=>
void
)
;
欧易提供者在有需要通知消费者的消息时发出此事件。消息的种类由
type
字符串标识。
RPC 订阅更新是
message
事件的常见用例。
例如，如果你使用
eth_subscribe
创建订阅，则每个订阅更新都将作为
message
事件发出，其
type
为
eth_subscription
。
例子
在
codeopen
中打开。
Connect Ethereum
Switch Chain
Events:
okxwallet is not defined
HTML
JavaScript
<
button
class
=
"
connectEthereumButton btn
"
>
Connect Ethereum
</
button
>
<
button
class
=
"
switchChainButton btn
"
>
Switch Chain
</
button
>
const
ethereumButton
=
document
.
querySelector
(
".connectEthereumButton"
)
;
const
switchChainButton
=
document
.
querySelector
(
".switchChainButton"
)
;
window
.
okxwallet
.
on
(
"chainChanged"
,
(
_chainId
)
=>
{
console
.
log
(
`
on chainChanged, current chainId:
${
_chainId
}
`
)
;
}
)
;
switchChainButton
.
addEventListener
(
"click"
,
async
(
)
=>
{
try
{
await
okxwallet
.
request
(
{
method
:
"wallet_switchEthereumChain"
,
params
:
[
{
chainId
:
okxwallet
.
chainId
===
"0x42"
?
"0x38"
:
"0x42"
}
]
}
)
;
}
catch
(
error
)
{
// handle other "switch" errors
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
ethereumButton
.
addEventListener
(
"click"
,
(
)
=>
{
getAccount
(
)
;
}
)
;
async
function
getAccount
(
)
{
await
okxwallet
.
request
(
{
method
:
"eth_requestAccounts"
}
)
;
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="连接账户" id="连接账户">连接账户<a class="index_header-anchor__Xqb+L" href="#连接账户" style="opacity:0">#</a></h2>
<p><code>eth_requestAccounts</code></p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rbbf:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rbbf:">EIP-1102</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">此方法由 <a class="items-center" href="https://eips.ethereum.org/EIPS/eip-1102" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">EIP-1102<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 指定。
在底层逻辑上，它调用 <a href="#wallet-requestpermissions"><code>wallet_requestPermissions</code></a> 以获得 <code>eth_accounts</code> 权限。由于目前来说 <code>eth_accounts</code> 是唯一的权限，所以你现在仅需此方法。</div></div></div></div></div>
<p><strong>描述</strong></p>
<p>此方法请求用户提供一个以太坊地址来识别。返回值为一个解析为单个以太坊地址字符串数组的 Promise。如果用户拒绝该请求，Promise 将被拒绝并返回 <code>4001</code> 错误。</p>
<p>该请求会导致一个欧易的弹窗出现。你应该只在响应用户操作时请求账户，比如一个用户在单击按钮的时候。在请求仍处于待处理状态时，你应该始终禁用导致请求被分派的按钮。</p>
<p>如果你无法检索用户的账户，你应该鼓励用户发起账户请求。</p>
<p><strong>返回值</strong></p>
<p><code>string[]</code> - 单个十六进制以太坊地址字符串的数组。</p>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/WNgrgLP" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Ethereum</span></button></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":Rvbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":Rvbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":Rvbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectEthereumButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Ethereum<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":Rvbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectEthereumButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectEthereumButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectEthereumButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">//Will Start the OKX extension</span>
  okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'eth_requestAccounts'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="添加代币" id="添加代币">添加代币<a class="index_header-anchor__Xqb+L" href="#添加代币" style="opacity:0">#</a></h2>
<p><strong>Note</strong>: 该功能仅在欧易 Web3 钱包插件端支持。</p>
<h3 id="wallet_watchasset"><code>wallet_watchAsset</code><a class="index_header-anchor__Xqb+L" href="#wallet_watchasset" style="opacity:0">#</a></h3>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R17bf:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R17bf:">EIP-747</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">此方法由 <a class="items-center" href="https://eips.ethereum.org/EIPS/eip-747" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">EIP-747<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 指定。</div></div></div></div></div>
<p><strong>描述</strong></p>
<p>此方法请求用户在欧易中关注某代币。返回一个布尔值，这个布尔值代表着代币是否已成功添加。</p>
<p>大多数以太坊钱包都支持关注一组代币，这些代币通常来自集中管理的代币注册表。 <code>wallet_watchAsset</code> 让 Web3 应用程序开发人员能够在运行时询问他们的用户去关注他们钱包中的代币。新添加的代币与通过原始方法（例如集中式注册表）添加的代币没有任何区别。</p>
<p><strong>参数</strong></p>
<ul>
<li><code>WatchAssetParams</code> - 要关注的资产的元数据。</li>
</ul>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">WatchAssetParams</span> <span class="token punctuation">{</span>
  type<span class="token operator">:</span> <span class="token string">'ERC20'</span><span class="token punctuation">;</span> <span class="token comment">// In the future, other standards will be supported</span>
  options<span class="token operator">:</span> <span class="token punctuation">{</span>
    address<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// The address of the token contract</span>
    <span class="token string-property property">'symbol'</span><span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// A ticker symbol or shorthand, up to 11 characters</span>
    decimals<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">;</span> <span class="token comment">// The number of token decimals</span>
    image<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span> <span class="token comment">// A string url of the token logo</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>返回值</strong></p>
<p><code>boolean</code> - 如果添加了代币为 <code>true</code>，否则为 <code>false</code>。</p>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/NWLxegB" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Ethereum</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Add Token</span></button><div class="feedback-wrapper"></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R1vbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R1vbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R1vbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectEthereumButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Ethereum<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>addTokenButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Add Token<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R1vbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> ethereumButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectEthereumButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> addTokenButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.addTokenButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

addTokenButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'wallet_switchEthereumChain'</span><span class="token punctuation">,</span> <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'0x1'</span> <span class="token punctuation">}</span><span class="token punctuation">]</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  okxwallet
    <span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'wallet_watchAsset'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'ERC20'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
          <span class="token literal-property property">address</span><span class="token operator">:</span> <span class="token string">'0xdac17f958d2ee523a2206206994597c13d831ec7'</span><span class="token punctuation">,</span>
          <span class="token literal-property property">symbol</span><span class="token operator">:</span> <span class="token string">'USDT'</span><span class="token punctuation">,</span>
          <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token number">6</span><span class="token punctuation">,</span>
          <span class="token literal-property property">image</span><span class="token operator">:</span> <span class="token string">'https://foo.io/token-image.svg'</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">success</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>success<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'USDT successfully added to wallet!'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Something went wrong.'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span><span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token property-access">error</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

ethereumButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">function</span> <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'eth_requestAccounts'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">error</span><span class="token punctuation">)</span><span class="token arrow operator">=&gt;</span><span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div></div>
<h2 data-content="事件" id="事件">事件<a class="index_header-anchor__Xqb+L" href="#事件" style="opacity:0">#</a></h2>
<p>欧易提供者实现了 <a class="items-center" href="https://nodejs.org/api/events.html" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Node.js <code>EventEmitter</code><i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> API。
本节详细介绍了通过该 API 发出的事件。
网络上有其他各式各样的 <code>EventEmitter</code> 指南可供参考，本指南列出了如下一些事件：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript">okxwallet<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">accounts</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// Handle the new accounts, or lack thereof.</span>
  <span class="token comment">// "accounts" will always be an array, but it can be empty.</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

okxwallet<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'chainChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">chainId</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// Handle the new chain.</span>
  <span class="token comment">// Correctly handling chain changes can be complicated.</span>
  <span class="token comment">// We recommend reloading the page unless you have a very good reason not to.</span>
  <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">location</span><span class="token punctuation">.</span><span class="token method function property-access">reload</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>另外，一旦你使用完监听器，请不要忘记将其删除（例如在 React 中卸载组件时）：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">function</span> <span class="token function">handleAccountsChanged</span><span class="token punctuation">(</span><span class="token parameter">accounts</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// ...</span>
<span class="token punctuation">}</span>

okxwallet<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> handleAccountsChanged<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Later</span>
okxwallet<span class="token punctuation">.</span><span class="token method function property-access">removeListener</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> handleAccountsChanged<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><code>okxwallet.removeListener</code> 的第一个参数是事件名称，第二个参数是对已传递给第一个参数中提到的事件名称的 <code>okxwallet.on</code> 的同一函数的引用。</p>
<p><strong>connect</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">ConnectInfo</span> <span class="token punctuation">{</span>
  chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

okxwallet<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'connect'</span><span class="token punctuation">,</span> <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>connectInfo<span class="token operator">:</span> ConnectInfo<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>欧易提供者会在第一次能够向链提交 RPC 请求时发出此事件。我们建议使用 <code>connect</code> 事件处理程序和 <a href="#okxwallet-isconnected"><code>okxwallet.isConnected()</code></a> 方法来确定欧易提供者的连接状态和连接时间。</p>
<p><strong>disconnect</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxwallet<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'disconnect'</span><span class="token punctuation">,</span> <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>error<span class="token operator">:</span> ProviderRpcError<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>如果欧易提供者无法向任何链提交 RPC 请求，则会发出此事件。通常，这只会发生在网络连接问题或某些其他不可预见的错误状态下。</p>
<p>一旦发出 <code>disconnect</code>，提供者直到重新建立与链的连接之前将不会接受任何新请求，建立新连接需要重新加载页面。你还可以使用 <a href="#okxwallet-isconnected"><code>okxwallet.isConnected()</code></a> 方法来确定提供程序是否已断开连接。</p>
<p><strong>accountsChanged</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxwallet<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>accounts<span class="token operator">:</span> <span class="token builtin">Array</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>每当 <code>eth_accounts</code> RPC 方法的返回值发生变化时，欧易提供程序都会发出此事件。
<code>eth_accounts</code> 会返回一个为空或包含单个账户地址的数组。返回的地址（如果存在）即为允许调用者访问的最近使用的账户地址。由于调用者由其 URL <em>origin</em> 标识，所以具有相同来源(origin)的站点会持有相同的权限。</p>
<p>只要用户公开的账户地址发生变化，就会发出 <code>accountsChanged</code>.</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R33bf:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R33bf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">我们计划在不久的将来允许 <code>eth_accounts</code> 数组能够包含多个地址。</div></div></div></div></div>
<p><strong>chainChanged</strong></p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R37bf:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R37bf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">欧易的默认链及其链 ID 请参见 <a href="#%e9%93%be-ids">Chain IDs section</a>。</div></div></div></div></div>
<p>当前连接的链发生变化时，欧易提供者会发出此事件。</p>
<p>所有的 RPC 请求都提交到当前连接的链上。因此，通过侦听此事件来跟踪当前链 ID 是至关重要的。</p>
<p>我们强烈建议在链更改时重新加载页面，当然你也可以通过需求自行选择。</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript">okxwallet<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'chainChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">_chainId</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">location</span><span class="token punctuation">.</span><span class="token method function property-access">reload</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>message</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">interface</span> <span class="token class-name">ProviderMessage</span> <span class="token punctuation">{</span>
  type<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  data<span class="token operator">:</span> <span class="token builtin">unknown</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

okxwallet<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'message'</span><span class="token punctuation">,</span> <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>message<span class="token operator">:</span> ProviderMessage<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>欧易提供者在有需要通知消费者的消息时发出此事件。消息的种类由 <code>type</code> 字符串标识。</p>
<p>RPC 订阅更新是 <code>message</code> 事件的常见用例。
例如，如果你使用 <code>eth_subscribe</code> 创建订阅，则每个订阅更新都将作为 <code>message</code> 事件发出，其 <code>type</code> 为 <code>eth_subscription</code>。</p>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/jOvqBjR" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<div class="interact-wrapper"><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Ethereum</span></button><button class="okui-btn btn-md btn-outline-primary" style="margin-left:14px" type="button"><span class="btn-content">Switch Chain</span></button><div><div class="feedback-wrapper"><div><strong>Events: </strong><span style="font-family: monospace;">okxwallet is not defined</span></div></div></div></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":R3vbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":R3vbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":R3vbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectEthereumButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect Ethereum<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>switchChainButton btn<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Switch Chain<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":R3vbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> ethereumButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">".connectEthereumButton"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> switchChainButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">".switchChainButton"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">"chainChanged"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">_chainId</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">on chainChanged, current chainId: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>_chainId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

switchChainButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">"click"</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"wallet_switchEthereumChain"</span><span class="token punctuation">,</span>
      <span class="token literal-property property">params</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token literal-property property">chainId</span><span class="token operator">:</span> okxwallet<span class="token punctuation">.</span><span class="token property-access">chainId</span> <span class="token operator">===</span> <span class="token string">"0x42"</span> <span class="token operator">?</span> <span class="token string">"0x38"</span> <span class="token operator">:</span> <span class="token string">"0x42"</span> <span class="token punctuation">}</span><span class="token punctuation">]</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// handle other "switch" errors</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

ethereumButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">"click"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getAccount</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">await</span> okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"eth_requestAccounts"</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
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
    "获取钱包地址",
    "获取 chainId",
    "添加代币",
    "签名交易",
    "智能合约交互"
  ],
  "toc": [
    "什么是 Injected provider API？",
    "连接账户",
    "添加代币",
    "事件"
  ]
}
```

</details>
