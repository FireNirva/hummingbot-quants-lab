# Provider API | sui | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/sui/provider#什么是-injected-provider-api？  
**抓取时间:** 2025-05-27 06:49:03  
**字数:** 840

## 导航路径
DApp 连接钱包 > sui > Provider API

## 目录
- 什么是 Injected provider API？
- 获取 wallet 对象
- 获取账户
- 第一笔交易
- 签名信息
- 连接账户
- 事件

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
获取 wallet 对象
#
Sui 钱包使用的是 wallet standard，相比其他异构链有些不同，可以通过事件通知的方式获取 wallet 对象：
const
GlobalWallet
=
{
register
:
(
wallet
)
=>
{
GlobalWallet
[
wallet
.
chainName
]
=
wallet
}
}
const
event
=
new
CustomEvent
(
'wallet-standard:app-ready'
,
{
detail
:
GlobalWallet
}
)
;
window
.
dispatchEvent
(
event
)
;
const
suiWallet
=
GlobalWallet
.
suiMainnet
获取账户
#
通过以上获取到的 suiWallet 对象，可以获取到账户：
const
suiAccounts
=
suiWallet
.
connectedAccounts
// suiAccounts 结构:
[
{
"address"
:
"0x7995ca23961fe06d8cea7da58ca751567ce820d7cba77b4a373249034eecca4a"
,
"publicKey"
:
"tUvCYrG22rHKR0c306MxgnhXOSf16Ot6H3GMO7btwDI="
,
"chains"
:
[
"sui:mainnet"
]
,
"features"
:
[
"sui:signAndExecuteTransactionBlock"
,
"sui:signTransactionBlock"
,
"sui:signMessage"
]
}
]
第一笔交易
#
suiWallet.features['sui:signAndExecuteTransactionBlock'].signAndExecuteTransactionBlock
签名并发送交易
Sui 钱包使用的是 wallet standard，相比其他异构链有些不同，所有方法都挂在 features[] 里
创建交易后，Web 应用程序可能会要求用户的欧易 Web3 钱包签署并发送交易。如果接受，欧易 Web3 钱包将使用用户的私钥签署交易并通过
SUI JSON RPC
连接提交。在
suiWallet
上调用
signAndExecuteTransactionBlock
方法会为已签名的交易返回
promise
。
const
handleTransaction
=
async
(
)
=>
{
const
tx
=
new
TransactionBlock
(
)
tx
.
moveCall
(
{
target
:
`
${
packageId
}
::
${
moduleName
}
::
${
functionName
}
`
,
arguments
:
[
tx
.
pure
(
params1
)
,
tx
.
pure
(
params2
)
,
]
,
typeArguments
:
[
]
,
}
)
const
result
=
await
suiWallet
.
features
[
'sui:signAndExecuteTransactionBlock'
]
.
signAndExecuteTransactionBlock
(
{
transactionBlock
:
tx
,
options
:
{
showEffects
:
true
}
,
}
)
console
.
log
(
'result'
,
result
)
// 通过result?.effects?.status?.status获取交易状态，成功为 'success'，失败为'failure'
}
拆币
在发交易时，付 gas 费的 objectId，如果这个 object 本身就要被发送，还要用来付 gas 费，这时候就需要用到拆币(split coin)
const
handleTransaction
=
async
(
)
=>
{
const
tx
=
new
TransactionBlock
(
)
const
value
=
'300000000'
// 这里是想要拆出的目标值
const
[
coins
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
tx
.
pure
(
BigInt
(
value
)
)
,
]
)
tx
.
moveCall
(
{
target
:
`
${
packageId
}
::
${
moduleName
}
::
${
functionName
}
`
,
arguments
:
[
tx
.
pure
(
参数
1
)
,
tx
.
pure
(
参数
2
)
,
tx
.
makeMoveVec
(
{
objects
:
[
coins
]
}
)
,
]
,
typeArguments
:
[
]
,
}
)
const
result
=
await
suiWallet
.
features
[
'sui:signAndExecuteTransactionBlock'
]
.
signAndExecuteTransactionBlock
(
{
transactionBlock
:
tx
,
options
:
{
showEffects
:
true
}
,
}
)
console
.
log
(
'result'
,
result
)
// 通过result?.effects?.status?.status获取交易状态，成功为 'success'，失败为'failure'
}
对交易块进行签名
通过
provider
上的
signTransactionBlock
方法可以签署一个交易块(多个交易的集合)。
const
tx
=
new
TransactionBlock
(
)
;
tx
.
moveCall
(
{
target
:
'xxx'
,
arguments
:
[
tx
.
pure
(
'okx'
)
,
tx
.
pure
(
'wallet'
)
,
]
,
}
)
;
const
input
=
{
transactionBlockSerialized
:
tx
.
serialize
(
)
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
l
const
transaction
=
await
suiWallet
.
features
[
'sui:signTransactionBlock'
]
.
signTransactionBlock
(
{
transactionBlock
:
tx
}
)
签名信息
#
对单个交易签名（不发送）
创建交易后，Web 应用程序可能会要求用户的欧易 Web3 钱包签署交易，而无需将其提交到网络。调用
signMessage
方法会为已签名的交易返回
Promise
。
import
{
ethers
}
from
'ethers'
;
// 这里借用 ethers 库来帮我们处理 message，将其转为 Uint8Array 类型
const
message
=
ethers
.
utils
.
toUtf8Bytes
(
'okx'
)
const
{
signature
,
messageBytes
}
=
await
suiWallet
.
features
[
'sui:signMessage'
]
.
signMessage
(
{
message
}
)
错误码
#
错误码
标题
描述
4900
断开连接
OKX Wallet could not connect to the network.
4100
未授权
The requested method and/or account has not been authorized by the user.
4001
用户拒绝请求
The user rejected the request through OKX wallet.
-32000
无效输入
Missing or invalid parameters.
-32002
请求资源不可用
This error occurs when a dapp attempts to submit a new transaction while OKX wallet's approval dialog is already open for a previous transaction. Only one approve window can be open at a time. Users should approve or reject their transaction before initiating a new transaction.
-32003
拒绝交易
OKX Wallet does not recognize a valid transaction.
-32601
未找到方法
OKX Wallet does not recognize the method.
-32603
内部错误
Something went wrong within OKX wallet.
连接账户
#
suiWallet.features['standard:connect'].connect()
描述
连接到欧易 Web3 钱包可以通过调用
suiWallet.features['standard:connect'].connect()
。
connect
调用将返回一个
Promise
对象，该
Promise
对象在用户接受连接请求时
resolve
，并在用户拒绝请求或关闭弹出窗口时
reject
。有关欧易 Web3 钱包可能发生错误的详细信息，请参考
错误码
。
当用户接受连接请求时，
suiWallet.features['standard:events']
也会触发连接事件。
suiWallet
.
features
[
'standard:events'
]
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
一旦 Web 应用程序连接到欧易 Web3 钱包，它将能够读取连接账户的公钥并提示用户进行其他交易。
例子
在
codeopen
中打开。
事件
#
成功连接
连接到欧易 Web3 钱包可以通过调用
suiWallet.features['standard:events'].on
。 当用户接受连接请求时，会触发连接事件。
用法
suiWallet
.
features
[
'standard:events'
]
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
断开连接
断开连接与连接过程相同。但是，钱包也有可能发起断开连接，而不是应用程序本身。
用法
suiWallet
.
features
[
'standard:events'
]
.
on
(
"disconnect"
,
(
)
=>
{
console
.
log
(
"disconnected!"
)
}
)
;
账户变更
欧易 Web3 钱包允许用户从单个扩展程序或移动应用程序中无缝管理多个账户。每当用户切换账户时，欧易 Web3 钱包都会发出一个
accountChanged
事件。
如果用户在已连接到应用程序时更改账户，并且新账户已经将该应用程序列入白名单，那么用户将保持连接状态并且欧易 Web3 钱包将传递新账户的公钥：
用法
suiWallet
.
features
[
'standard:events'
]
.
on
(
'accountChanged'
,
(
publicKey
)
=>
{
if
(
publicKey
)
{
console
.
log
(
`
Switched to account
${
publicKey
.
toBase58
(
)
}
`
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
<h2 data-content="获取 wallet 对象" id="获取-wallet-对象">获取 wallet 对象<a class="index_header-anchor__Xqb+L" href="#获取-wallet-对象" style="opacity:0">#</a></h2>
<p>Sui 钱包使用的是 wallet standard，相比其他异构链有些不同，可以通过事件通知的方式获取 wallet 对象：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> GlobalWallet <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token function-variable function">register</span><span class="token operator">:</span> <span class="token punctuation">(</span>wallet<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
          GlobalWallet<span class="token punctuation">[</span>wallet<span class="token punctuation">.</span>chainName<span class="token punctuation">]</span> <span class="token operator">=</span> wallet
      <span class="token punctuation">}</span>
  <span class="token punctuation">}</span>
  <span class="token keyword">const</span> event <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">CustomEvent</span><span class="token punctuation">(</span><span class="token string">'wallet-standard:app-ready'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span> detail<span class="token operator">:</span> GlobalWallet <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  window<span class="token punctuation">.</span><span class="token function">dispatchEvent</span><span class="token punctuation">(</span>event<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> suiWallet <span class="token operator">=</span> GlobalWallet<span class="token punctuation">.</span>suiMainnet
</code></pre></div>
<h2 data-content="获取账户" id="获取账户">获取账户<a class="index_header-anchor__Xqb+L" href="#获取账户" style="opacity:0">#</a></h2>
<p>通过以上获取到的 suiWallet 对象，可以获取到账户：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> suiAccounts <span class="token operator">=</span> suiWallet<span class="token punctuation">.</span>connectedAccounts

<span class="token comment">// suiAccounts 结构:</span>
<span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
      <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"0x7995ca23961fe06d8cea7da58ca751567ce820d7cba77b4a373249034eecca4a"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"tUvCYrG22rHKR0c306MxgnhXOSf16Ot6H3GMO7btwDI="</span><span class="token punctuation">,</span>
      <span class="token string-property property">"chains"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token string">"sui:mainnet"</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"features"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token string">"sui:signAndExecuteTransactionBlock"</span><span class="token punctuation">,</span>
          <span class="token string">"sui:signTransactionBlock"</span><span class="token punctuation">,</span>
          <span class="token string">"sui:signMessage"</span>
      <span class="token punctuation">]</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">]</span>
</code></pre></div>
<h2 data-content="第一笔交易" id="第一笔交易">第一笔交易<a class="index_header-anchor__Xqb+L" href="#第一笔交易" style="opacity:0">#</a></h2>
<p><code>suiWallet.features['sui:signAndExecuteTransactionBlock'].signAndExecuteTransactionBlock</code></p>
<p><strong>签名并发送交易</strong></p>
<p>Sui 钱包使用的是 wallet standard，相比其他异构链有些不同，所有方法都挂在 features[] 里
创建交易后，Web 应用程序可能会要求用户的欧易 Web3 钱包签署并发送交易。如果接受，欧易 Web3 钱包将使用用户的私钥签署交易并通过 <code>SUI JSON RPC</code> 连接提交。在 <code>suiWallet</code> 上调用 <code>signAndExecuteTransactionBlock</code> 方法会为已签名的交易返回 <code>promise</code>。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> <span class="token function-variable function">handleTransaction</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> tx <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    tx<span class="token punctuation">.</span><span class="token function">moveCall</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      target<span class="token operator">:</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>packageId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">::</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>moduleName<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">::</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>functionName<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
      arguments<span class="token operator">:</span> <span class="token punctuation">[</span>
        tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span>params1<span class="token punctuation">)</span><span class="token punctuation">,</span>
        tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span>params2<span class="token punctuation">)</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      typeArguments<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'sui:signAndExecuteTransactionBlock'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">signAndExecuteTransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      transactionBlock<span class="token operator">:</span> tx<span class="token punctuation">,</span>
      options<span class="token operator">:</span> <span class="token punctuation">{</span> showEffects<span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'result'</span><span class="token punctuation">,</span> result<span class="token punctuation">)</span>
    <span class="token comment">// 通过result?.effects?.status?.status获取交易状态，成功为 'success'，失败为'failure'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>拆币</strong></p>
<p>在发交易时，付 gas 费的 objectId，如果这个 object 本身就要被发送，还要用来付 gas 费，这时候就需要用到拆币(split coin)</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> <span class="token function-variable function">handleTransaction</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> tx <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">)</span>

    <span class="token keyword">const</span> value <span class="token operator">=</span> <span class="token string">'300000000'</span>  <span class="token comment">// 这里是想要拆出的目标值</span>
    <span class="token keyword">const</span> <span class="token punctuation">[</span>coins<span class="token punctuation">]</span> <span class="token operator">=</span> tx<span class="token punctuation">.</span><span class="token function">splitCoins</span><span class="token punctuation">(</span>tx<span class="token punctuation">.</span>gas<span class="token punctuation">,</span> <span class="token punctuation">[</span>
      tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span><span class="token function">BigInt</span><span class="token punctuation">(</span>value<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">)</span>
    tx<span class="token punctuation">.</span><span class="token function">moveCall</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      target<span class="token operator">:</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>packageId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">::</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>moduleName<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">::</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>functionName<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
      arguments<span class="token operator">:</span> <span class="token punctuation">[</span>
        tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span>参数<span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span>参数<span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        tx<span class="token punctuation">.</span><span class="token function">makeMoveVec</span><span class="token punctuation">(</span><span class="token punctuation">{</span> objects<span class="token operator">:</span> <span class="token punctuation">[</span>coins<span class="token punctuation">]</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      typeArguments<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'sui:signAndExecuteTransactionBlock'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">signAndExecuteTransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      transactionBlock<span class="token operator">:</span> tx<span class="token punctuation">,</span>
      options<span class="token operator">:</span> <span class="token punctuation">{</span> showEffects<span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'result'</span><span class="token punctuation">,</span> result<span class="token punctuation">)</span>
    <span class="token comment">// 通过result?.effects?.status?.status获取交易状态，成功为 'success'，失败为'failure'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><strong>对交易块进行签名</strong></p>
<p>通过 <code>provider</code> 上的 <code>signTransactionBlock</code> 方法可以签署一个交易块(多个交易的集合)。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> tx <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
tx<span class="token punctuation">.</span><span class="token function">moveCall</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  target<span class="token operator">:</span> <span class="token string">'xxx'</span><span class="token punctuation">,</span>
  arguments<span class="token operator">:</span> <span class="token punctuation">[</span>
    tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span><span class="token string">'okx'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    tx<span class="token punctuation">.</span><span class="token function">pure</span><span class="token punctuation">(</span><span class="token string">'wallet'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> input <span class="token operator">=</span> <span class="token punctuation">{</span>
  transactionBlockSerialized<span class="token operator">:</span> tx<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
  options<span class="token operator">:</span> <span class="token punctuation">{</span>
    showEffects<span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>l
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">await</span> suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'sui:signTransactionBlock'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">signTransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">{</span> transactionBlock<span class="token operator">:</span> tx <span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="签名信息" id="签名信息">签名信息<a class="index_header-anchor__Xqb+L" href="#签名信息" style="opacity:0">#</a></h2>
<p><strong>对单个交易签名（不发送）</strong></p>
<p>创建交易后，Web 应用程序可能会要求用户的欧易 Web3 钱包签署交易，而无需将其提交到网络。调用 <code>signMessage</code> 方法会为已签名的交易返回 <code>Promise</code>。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">import</span> <span class="token punctuation">{</span> ethers <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'ethers'</span><span class="token punctuation">;</span>
<span class="token comment">// 这里借用 ethers 库来帮我们处理 message，将其转为 Uint8Array 类型</span>

<span class="token keyword">const</span> message <span class="token operator">=</span> ethers<span class="token punctuation">.</span>utils<span class="token punctuation">.</span><span class="token function">toUtf8Bytes</span><span class="token punctuation">(</span><span class="token string">'okx'</span><span class="token punctuation">)</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> signature<span class="token punctuation">,</span> messageBytes <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword">await</span> suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'sui:signMessage'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span><span class="token punctuation">{</span> message <span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<h3 id="错误码">错误码<a class="index_header-anchor__Xqb+L" href="#错误码" style="opacity:0">#</a></h3>
<div class="index_table__kvZz5"><table><thead><tr><th align="left"><div style="width:100px">错误码</div></th><th align="left"><div style="width:120px">标题</div></th><th align="left">描述</th></tr></thead><tbody><tr><td align="left">4900</td><td align="left">断开连接</td><td align="left">OKX Wallet could not connect to the network.</td></tr><tr><td align="left">4100</td><td align="left">未授权</td><td align="left">The requested method and/or account has not been authorized by the user.</td></tr><tr><td align="left">4001</td><td align="left">用户拒绝请求</td><td align="left">The user rejected the request through OKX wallet.</td></tr><tr><td align="left">-32000</td><td align="left">无效输入</td><td align="left">Missing or invalid parameters.</td></tr><tr><td align="left">-32002</td><td align="left">请求资源不可用</td><td align="left">This error occurs when a dapp attempts to submit a new transaction while OKX wallet's approval dialog is already open for a previous transaction. Only one approve window can be open at a time. Users should  approve or reject their transaction before initiating a new transaction.</td></tr><tr><td align="left">-32003</td><td align="left">拒绝交易</td><td align="left">OKX Wallet does not recognize a valid transaction.</td></tr><tr><td align="left">-32601</td><td align="left">未找到方法</td><td align="left">OKX Wallet does not recognize the method.</td></tr><tr><td align="left">-32603</td><td align="left">内部错误</td><td align="left">Something went wrong within OKX wallet.</td></tr></tbody></table></div>
<h2 data-content="连接账户" id="连接账户">连接账户<a class="index_header-anchor__Xqb+L" href="#连接账户" style="opacity:0">#</a></h2>
<p><code>suiWallet.features['standard:connect'].connect()</code></p>
<p><strong>描述</strong></p>
<p>连接到欧易 Web3 钱包可以通过调用  <code>suiWallet.features['standard:connect'].connect()</code>。</p>
<p><code>connect</code> 调用将返回一个 <code>Promise</code> 对象，该 <code>Promise</code> 对象在用户接受连接请求时 <code>resolve</code>，并在用户拒绝请求或关闭弹出窗口时 <code>reject</code>。有关欧易 Web3 钱包可能发生错误的详细信息，请参考 <a href="#%e9%94%99%e8%af%af%e7%a0%81">错误码</a>。
当用户接受连接请求时，<code>suiWallet.features['standard:events']</code> 也会触发连接事件。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'standard:events'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"connected!"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>一旦 Web 应用程序连接到欧易 Web3 钱包，它将能够读取连接账户的公钥并提示用户进行其他交易。</p>
<p><strong>例子</strong></p>
<p>在 <a class="items-center" href="https://codepen.io/okxwallet/pen/RweEpKL" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">codeopen<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>中打开。</p>
<h2 data-content="事件" id="事件">事件<a class="index_header-anchor__Xqb+L" href="#事件" style="opacity:0">#</a></h2>
<p><strong>成功连接</strong></p>
<p>连接到欧易 Web3 钱包可以通过调用 <code>suiWallet.features['standard:events'].on</code>。 当用户接受连接请求时，会触发连接事件。</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'standard:events'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"connect"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"connected!"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>断开连接</strong></p>
<p>断开连接与连接过程相同。但是，钱包也有可能发起断开连接，而不是应用程序本身。</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'standard:events'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">"disconnect"</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"disconnected!"</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p><strong>账户变更</strong></p>
<p>欧易 Web3 钱包允许用户从单个扩展程序或移动应用程序中无缝管理多个账户。每当用户切换账户时，欧易 Web3 钱包都会发出一个 <code>accountChanged</code> 事件。</p>
<p>如果用户在已连接到应用程序时更改账户，并且新账户已经将该应用程序列入白名单，那么用户将保持连接状态并且欧易 Web3 钱包将传递新账户的公钥：</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">suiWallet<span class="token punctuation">.</span>features<span class="token punctuation">[</span><span class="token string">'standard:events'</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'accountChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>publicKey<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">if</span> <span class="token punctuation">(</span>publicKey<span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Switched to account </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>publicKey<span class="token punctuation">.</span><span class="token function">toBase58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
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
    "sui",
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
    "获取 wallet 对象",
    "获取账户",
    "第一笔交易",
    "签名信息",
    "连接账户",
    "事件"
  ]
}
```

</details>
