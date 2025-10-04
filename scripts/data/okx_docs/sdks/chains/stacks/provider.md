# Provider API | stacks | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/stacks/provider#provider-api  
**抓取时间:** 2025-05-27 07:35:26  
**字数:** 476

## 导航路径
DApp 连接钱包 > stacks > Provider API

## 目录
- 什么是 Injected provider API？
- 连接账户
- 合约调用
- 转账交易
- 签名消息

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
连接账户
#
window.okxwallet.stacks.connect()
描述
通过调用
window.okxwallet.stacks.connect()
连接欧易 Web3 钱包。
当成功调用
window.okxwallet.stacks.connect()
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
stacks
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
合约调用
#
window.okxwallet.stacks.signTransaction(transaction)
参数
transaction - object
stxAddress - string: 当前连接的钱包的 stx 地址
txType - string: 交易类型，必须传入
contract_call
contractName - string: 合约名称
contractAddress - string: 合约地址
functionName - string: 函数名称
functionArgs - array<string>: 16进制序列化的合约调用数据
postConditionMode - number: (非必需)是否允许后置条件
1: 允许
2: 拒绝
postConditions - array<string>: (非必需)后置条件的参数
anchorMode - number: (非必需)交易上链的方式
1: 交易必须被 anchored block 接收
2: 交易必须被 microblock 接收
3: 可以任意选择一种接收方式
返回值
result - object
txHash - string: 交易哈希
signature - string: 签名字符串
try
{
const
transaction
=
{
"stxAddress"
:
""
,
"txType"
:
"contract_call"
,
"contractName"
:
"amm-swap-pool-v1-1"
,
"contractAddress"
:
"SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9"
,
"functionName"
:
"swap-helper"
,
"functionArgs"
:
[
"0616e685b016b3b6cd9ebf35f38e5ae29392e2acd51d0a746f6b656e2d77737478"
,
"0616e685b016b3b6cd9ebf35f38e5ae29392e2acd51d176167653030302d676f7665726e616e63652d746f6b656e"
,
"0100000000000000000000000005f5e100"
,
"01000000000000000000000000000f4240"
,
"0a010000000000000000000000000078b854"
]
,
"postConditionMode"
:
2
,
"postConditions"
:
[
"000216c03b5520cf3a0bd270d8e41e5e19a464aef6294c010000000000002710"
,
"010316e685b016b3b6cd9ebf35f38e5ae29392e2acd51d0f616c65782d7661756c742d76312d3116e685b016b3b6cd9ebf35f38e5ae29392e2acd51d176167653030302d676f7665726e616e63652d746f6b656e04616c657803000000000078b854"
]
,
"anchorMode"
:
3
,
}
;
const
{
txHash
,
signature
}
=
await
window
.
okxwallet
.
stacks
.
signTransaction
(
transaction
)
;
console
.
location
(
{
txHash
,
signature
}
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
转账交易
#
window.okxwallet.stacks.signTransaction(transaction)
参数
transaction - object
stxAddress - string: 当前连接的钱包的 stx 地址
txType - string: 交易类型，必须传入
token_transfer
recipient - string: 接收地址
amount - stirng: 发送的数量
memo - stirng: (非必需)备注信息
anchorMode - number: (非必需)交易上链的方式
1: 交易必须被 anchored block 接收
2: 交易必须被 microblock 接收
3: 可以任意选择一种接收方式
返回值
result - object
txHash - string: 交易哈希
signature - string: 签名字符串
try
{
const
transaction
=
{
stxAddress
:
''
,
txType
:
'token_transfer'
,
recipient
:
''
,
amount
:
'10000'
,
memo
:
'test'
}
;
const
{
txHash
,
signature
}
=
await
window
.
okxwallet
.
stacks
.
signTransaction
(
transaction
)
;
console
.
location
(
{
txHash
,
signature
}
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
签名消息
#
window.okxwallet.stacks.signMessage(data)
参数
data - object
message - string: 需要签名的数据
返回值
result - object
publicKey - string: 验签的公钥
signature - string: 签名字符串
try
{
const
data
=
{
message
:
'1234'
}
;
const
{
publicKey
,
signature
}
=
await
window
.
okxwallet
.
stacks
.
signMessage
(
data
)
;
console
.
location
(
{
publicKey
,
signature
}
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

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。</p>
<h2 data-content="连接账户" id="连接账户">连接账户<a class="index_header-anchor__Xqb+L" href="#连接账户" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.stacks.connect()</code></p>
<p><strong>描述</strong></p>
<p>通过调用 <code>window.okxwallet.stacks.connect()</code> 连接欧易 Web3 钱包。</p>
<p>当成功调用 <code>window.okxwallet.stacks.connect()</code>，将会唤起欧易 Web3 钱包连接钱包页面，用户可以决定是否连接当前 DApp，如果用户同意将会返回地址 (<code>address</code>) 和公钥 (<code>public key</code>)。</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">stacks</span><span class="token punctuation">.</span><span class="token method function property-access">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>response<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { address: string, publicKey: string }</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// { code: 4001, message: "User rejected the request."}</span>
  <span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="合约调用" id="合约调用">合约调用<a class="index_header-anchor__Xqb+L" href="#合约调用" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.stacks.signTransaction(transaction)</code></p>
<p><strong>参数</strong></p>
<ul>
<li>transaction - object<!-- -->
<ul>
<li>stxAddress - string: 当前连接的钱包的 stx 地址</li>
<li>txType - string: 交易类型，必须传入 <code>contract_call</code></li>
<li>contractName - string: 合约名称</li>
<li>contractAddress - string: 合约地址</li>
<li>functionName - string: 函数名称</li>
<li>functionArgs - array&lt;string&gt;: 16进制序列化的合约调用数据</li>
<li>postConditionMode - number: (非必需)是否允许后置条件<!-- -->
<ul>
<li>1: 允许</li>
<li>2: 拒绝</li>
</ul>
</li>
<li>postConditions - array&lt;string&gt;: (非必需)后置条件的参数</li>
<li>anchorMode - number: (非必需)交易上链的方式<!-- -->
<ul>
<li>1: 交易必须被 anchored block 接收</li>
<li>2: 交易必须被 microblock 接收</li>
<li>3: 可以任意选择一种接收方式</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>result - object<!-- -->
<ul>
<li>txHash - string: 交易哈希</li>
<li>signature - string: 签名字符串</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token string-property property">"stxAddress"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
      <span class="token string-property property">"txType"</span><span class="token operator">:</span> <span class="token string">"contract_call"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"contractName"</span><span class="token operator">:</span> <span class="token string">"amm-swap-pool-v1-1"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"contractAddress"</span><span class="token operator">:</span> <span class="token string">"SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"functionName"</span><span class="token operator">:</span> <span class="token string">"swap-helper"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"functionArgs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token string">"0616e685b016b3b6cd9ebf35f38e5ae29392e2acd51d0a746f6b656e2d77737478"</span><span class="token punctuation">,</span>
          <span class="token string">"0616e685b016b3b6cd9ebf35f38e5ae29392e2acd51d176167653030302d676f7665726e616e63652d746f6b656e"</span><span class="token punctuation">,</span>
          <span class="token string">"0100000000000000000000000005f5e100"</span><span class="token punctuation">,</span>
          <span class="token string">"01000000000000000000000000000f4240"</span><span class="token punctuation">,</span>
          <span class="token string">"0a010000000000000000000000000078b854"</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"postConditionMode"</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      <span class="token string-property property">"postConditions"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token string">"000216c03b5520cf3a0bd270d8e41e5e19a464aef6294c010000000000002710"</span><span class="token punctuation">,</span>
          <span class="token string">"010316e685b016b3b6cd9ebf35f38e5ae29392e2acd51d0f616c65782d7661756c742d76312d3116e685b016b3b6cd9ebf35f38e5ae29392e2acd51d176167653030302d676f7665726e616e63652d746f6b656e04616c657803000000000078b854"</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"anchorMode"</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> <span class="token punctuation">{</span>txHash<span class="token punctuation">,</span> signature<span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">stacks</span><span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">location</span><span class="token punctuation">(</span><span class="token punctuation">{</span>txHash<span class="token punctuation">,</span> signature<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="转账交易" id="转账交易">转账交易<a class="index_header-anchor__Xqb+L" href="#转账交易" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.stacks.signTransaction(transaction)</code></p>
<p><strong>参数</strong></p>
<ul>
<li>transaction - object<!-- -->
<ul>
<li>stxAddress - string: 当前连接的钱包的 stx 地址</li>
<li>txType - string: 交易类型，必须传入 <code>token_transfer</code></li>
<li>recipient - string: 接收地址</li>
<li>amount - stirng: 发送的数量</li>
<li>memo - stirng: (非必需)备注信息</li>
<li>anchorMode - number: (非必需)交易上链的方式<!-- -->
<ul>
<li>1: 交易必须被 anchored block 接收</li>
<li>2: 交易必须被 microblock 接收</li>
<li>3: 可以任意选择一种接收方式</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>result - object<!-- -->
<ul>
<li>txHash - string: 交易哈希</li>
<li>signature - string: 签名字符串</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">stxAddress</span><span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">,</span>
      <span class="token literal-property property">txType</span><span class="token operator">:</span> <span class="token string">'token_transfer'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">recipient</span><span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">,</span>
      <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'10000'</span><span class="token punctuation">,</span>
      <span class="token literal-property property">memo</span><span class="token operator">:</span> <span class="token string">'test'</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> <span class="token punctuation">{</span>txHash<span class="token punctuation">,</span> signature<span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">stacks</span><span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">location</span><span class="token punctuation">(</span><span class="token punctuation">{</span>txHash<span class="token punctuation">,</span> signature<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签名消息" id="签名消息">签名消息<a class="index_header-anchor__Xqb+L" href="#签名消息" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.stacks.signMessage(data)</code></p>
<p><strong>参数</strong></p>
<ul>
<li>data - object<!-- -->
<ul>
<li>message - string: 需要签名的数据</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>result - object<!-- -->
<ul>
<li>publicKey - string: 验签的公钥</li>
<li>signature - string: 签名字符串</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">message</span><span class="token operator">:</span> <span class="token string">'1234'</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> <span class="token punctuation">{</span>publicKey<span class="token punctuation">,</span> signature<span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">stacks</span><span class="token punctuation">.</span><span class="token method function property-access">signMessage</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">location</span><span class="token punctuation">(</span><span class="token punctuation">{</span>publicKey<span class="token punctuation">,</span> signature<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "stacks",
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
    "合约调用",
    "转账交易",
    "签名消息"
  ]
}
```

</details>
