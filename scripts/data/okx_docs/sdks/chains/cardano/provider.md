# Provider API | cardano | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/cardano/provider#签名消息  
**抓取时间:** 2025-05-27 07:25:49  
**字数:** 504

## 导航路径
DApp 连接钱包 > cardano > Provider API

## 目录
- 什么是 Injected provider API？
- 获取注入的对象
- 注入对象的属性和方法
- 连接钱包的简单示例
- 获取网络 Id
- 获取 UTXO
- 获取资产
- 获取已使用的钱包地址
- 获取未使用的钱包地址
- 获取找零地址
- 签名交易
- 签名消息
- 广播交易

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
获取注入的对象
#
Dapp 可以通过两种方式访问注入的对象，分别是：
window.okxwallet.cardano
window.cardano.okxwallet
这两个属性都指向同一个对象，提供两个方式是为了方便 Dapp 使用。
注入对象的属性和方法
#
name
- string: 钱包的名称，值为 'OKX Wallet'
icon
- string: 钱包的图标
apiVersion
- string: 版本号
isEnabled
- () => Promise<bool>: 返回当前钱包是否已经链接上 Dapp 。如果 Dapp 已经链接到用户的钱包，则返回 true ，否则返回 false 。如果此函数返回 true ，则后续调用 wallet.enable() 时都会成功并且返回 API 对象。
enable
- () => Promise<API>: 该用法用于链接钱包，如果用户同意了链接钱包，则会将 API 对象返回给 Dapp 。
连接钱包的简单示例
#
try
{
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
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
获取网络 Id
#
api.getNetworkId(): Promise<number>
描述
返回当前连接的帐户的网络 Id 。
返回值
networkId
- string: 当前连接的帐户的网络 Id 。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
networkId
=
await
okxwalletCardanoApi
.
getNetworkId
(
)
;
获取 UTXO
#
api.getUtxos(amount: cbor<value> = undefined): Promise<TransactionUnspentOutput[] | undefined>
描述
如果 amount 没有定义，则返回由钱包控制的所有 UTXO (未花费的交易输出)列表。 如果 amount 定义了，则返回达到 amount 中指定的 ADA /多资产价值目标所需的 UTXO ，如果无法达到，则返回 null 。
返回值
utxos
- string[]: UTXO 列表。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
utxos
=
await
okxwalletCardanoApi
.
getUtxos
(
)
;
获取资产
#
api.getBalance(): Promise<cbor<value>>
描述
返回钱包可用的总余额。这与 api.getUtxos() 返回的结果相加是一样的。
返回值
balance
- string: 钱包可用的总余额
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
utxos
=
await
okxwalletCardanoApi
.
getBalance
(
)
;
获取已使用的钱包地址
#
api.getUsedAddresses(): Promise<cbor<address>[]>
描述
返回所有由钱包控制的已使用地址(包括在某些链上交易中)的列表。
返回值
addresses
- string[]: 已使用的地址列表。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
utxos
=
await
okxwalletCardanoApi
.
getUsedAddresses
(
)
;
获取未使用的钱包地址
#
api.getUnusedAddresses(): Promise<cbor<address>[]>
描述
返回由钱包控制的未使用地址列表。
返回值
addresses
- string[]: 未使用的地址列表。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
utxos
=
await
okxwalletCardanoApi
.
getUnusedAddresses
(
)
;
获取找零地址
#
api.getChangeAddress(): Promise<cbor<address>>
描述
返回钱包组装交易时，需要使用到的找零地址。
返回值
changeAddress
- string: 找零地址.
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
utxos
=
await
okxwalletCardanoApi
.
getChangeAddress
(
)
;
签名交易
#
api.signTx(tx: cbor<transaction>): Promise<cbor<transaction_witness_set>>
描述
请求用户对交易进行签名，如果用户同意，则尝试对交易进行签名，并返回签名的交易。
返回值
signedTx
- string: 签名的交易。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
rawTransaction
=
''
;
const
result
=
await
okxwalletCardanoApi
.
signTx
(
rawTransaction
)
;
签名消息
#
api.signData: (addr: Cbor<address>, payload: HexString) => Promise<DataSignature>
描述
签名消息。
阅读更多关于 CIP-0030 的消息签名规范。(
https://github.com/cardano-foundation/CIPs/tree/master/CIP-0030
).
返回值
dataSignature
- object
signature - string
key - string
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
addresses
=
await
okxwalletCardanoApi
.
getUsedAddresses
(
)
;
const
payload
=
''
;
const
result
=
await
okxwalletCardanoApi
.
signData
(
addresses
[
0
]
,
payload
)
;
广播交易
#
api.submitTx(tx: cbor<transaction>): Promise<hash32>
描述
广播交易，并返回给 Dapp 交易哈希以便 Dapp 追踪这笔交易。
返回值
txHash
- string: 交易哈希。
const
okxwalletCardanoApi
=
await
window
.
okxwallet
.
cardano
.
enable
(
)
;
const
transaction
=
''
;
const
result
=
await
okxwalletCardanoApi
.
submitTx
(
transaction
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
<p>Dapp 可以通过两种方式访问注入的对象，分别是：</p>
<ul>
<li><code>window.okxwallet.cardano</code></li>
<li><code>window.cardano.okxwallet</code></li>
</ul>
<p>这两个属性都指向同一个对象，提供两个方式是为了方便 Dapp 使用。</p>
<h2 data-content="注入对象的属性和方法" id="注入对象的属性和方法">注入对象的属性和方法<a class="index_header-anchor__Xqb+L" href="#注入对象的属性和方法" style="opacity:0">#</a></h2>
<ol>
<li><code>name</code> - string: 钱包的名称，值为 'OKX Wallet'</li>
<li><code>icon</code> - string: 钱包的图标</li>
<li><code>apiVersion</code> - string: 版本号</li>
<li><code>isEnabled</code> - () =&gt; Promise&lt;bool&gt;: 返回当前钱包是否已经链接上 Dapp 。如果 Dapp 已经链接到用户的钱包，则返回 true ，否则返回 false 。如果此函数返回 true ，则后续调用 wallet.enable() 时都会成功并且返回 API 对象。</li>
<li><code>enable</code> - () =&gt; Promise&lt;API&gt;: 该用法用于链接钱包，如果用户同意了链接钱包，则会将 API 对象返回给 Dapp 。</li>
</ol>
<h2 data-content="连接钱包的简单示例" id="连接钱包的简单示例">连接钱包的简单示例<a class="index_header-anchor__Xqb+L" href="#连接钱包的简单示例" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="获取网络 Id" id="获取网络-id">获取网络 Id<a class="index_header-anchor__Xqb+L" href="#获取网络-id" style="opacity:0">#</a></h2>
<p><code>api.getNetworkId(): Promise&lt;number&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回当前连接的帐户的网络 Id 。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>networkId</code> - string: 当前连接的帐户的网络 Id 。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> networkId <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getNetworkId</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取 UTXO" id="获取-utxo">获取 UTXO<a class="index_header-anchor__Xqb+L" href="#获取-utxo" style="opacity:0">#</a></h2>
<p><code>api.getUtxos(amount: cbor&lt;value&gt; = undefined): Promise&lt;TransactionUnspentOutput[] | undefined&gt;</code></p>
<p><strong>描述</strong></p>
<p>如果 amount 没有定义，则返回由钱包控制的所有 UTXO (未花费的交易输出)列表。 如果 amount 定义了，则返回达到 amount 中指定的 ADA /多资产价值目标所需的 UTXO ，如果无法达到，则返回 null 。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>utxos</code> - string[]: UTXO 列表。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> utxos <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getUtxos</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取资产" id="获取资产">获取资产<a class="index_header-anchor__Xqb+L" href="#获取资产" style="opacity:0">#</a></h2>
<p><code>api.getBalance(): Promise&lt;cbor&lt;value&gt;&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回钱包可用的总余额。这与 api.getUtxos() 返回的结果相加是一样的。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>balance</code> - string: 钱包可用的总余额</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> utxos <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getBalance</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取已使用的钱包地址" id="获取已使用的钱包地址">获取已使用的钱包地址<a class="index_header-anchor__Xqb+L" href="#获取已使用的钱包地址" style="opacity:0">#</a></h2>
<p><code>api.getUsedAddresses(): Promise&lt;cbor&lt;address&gt;[]&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回所有由钱包控制的已使用地址(包括在某些链上交易中)的列表。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>addresses</code> - string[]: 已使用的地址列表。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> utxos <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getUsedAddresses</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取未使用的钱包地址" id="获取未使用的钱包地址">获取未使用的钱包地址<a class="index_header-anchor__Xqb+L" href="#获取未使用的钱包地址" style="opacity:0">#</a></h2>
<p><code>api.getUnusedAddresses(): Promise&lt;cbor&lt;address&gt;[]&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回由钱包控制的未使用地址列表。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>addresses</code> - string[]: 未使用的地址列表。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> utxos <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getUnusedAddresses</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取找零地址" id="获取找零地址">获取找零地址<a class="index_header-anchor__Xqb+L" href="#获取找零地址" style="opacity:0">#</a></h2>
<p><code>api.getChangeAddress(): Promise&lt;cbor&lt;address&gt;&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回钱包组装交易时，需要使用到的找零地址。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>changeAddress</code> - string: 找零地址.</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> utxos <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getChangeAddress</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="签名交易" id="签名交易">签名交易<a class="index_header-anchor__Xqb+L" href="#签名交易" style="opacity:0">#</a></h2>
<p><code>api.signTx(tx: cbor&lt;transaction&gt;): Promise&lt;cbor&lt;transaction_witness_set&gt;&gt;</code></p>
<p><strong>描述</strong></p>
<p>请求用户对交易进行签名，如果用户同意，则尝试对交易进行签名，并返回签名的交易。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>signedTx</code> - string: 签名的交易。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> rawTransaction <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">signTx</span><span class="token punctuation">(</span>rawTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="签名消息" id="签名消息">签名消息<a class="index_header-anchor__Xqb+L" href="#签名消息" style="opacity:0">#</a></h2>
<p><code>api.signData: (addr: Cbor&lt;address&gt;, payload: HexString) =&gt; Promise&lt;DataSignature&gt;</code></p>
<p><strong>描述</strong></p>
<p>签名消息。
阅读更多关于 CIP-0030 的消息签名规范。(<a class="items-center" href="https://github.com/cardano-foundation/CIPs/tree/master/CIP-0030" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/cardano-foundation/CIPs/tree/master/CIP-0030<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>).</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>dataSignature</code> - object<!-- -->
<ul>
<li>signature - string</li>
<li>key - string</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> addresses <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">getUsedAddresses</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> payload <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">signData</span><span class="token punctuation">(</span>addresses<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">,</span> payload<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="广播交易" id="广播交易">广播交易<a class="index_header-anchor__Xqb+L" href="#广播交易" style="opacity:0">#</a></h2>
<p><code>api.submitTx(tx: cbor&lt;transaction&gt;): Promise&lt;hash32&gt;</code></p>
<p><strong>描述</strong></p>
<p>广播交易，并返回给 Dapp 交易哈希以便 Dapp 追踪这笔交易。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>txHash</code> - string: 交易哈希。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> okxwalletCardanoApi <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">cardano</span><span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> okxwalletCardanoApi<span class="token punctuation">.</span><span class="token method function property-access">submitTx</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "cardano",
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
    "注入对象的属性和方法",
    "连接钱包的简单示例",
    "获取网络 Id",
    "获取 UTXO",
    "获取资产",
    "获取已使用的钱包地址",
    "获取未使用的钱包地址",
    "获取找零地址",
    "签名交易",
    "签名消息",
    "广播交易"
  ]
}
```

</details>
