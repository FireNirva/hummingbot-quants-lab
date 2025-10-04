# Provider API (Signet) | Bitcoin | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/bitcoin/provider-signet#signpsbt  
**抓取时间:** 2025-05-27 06:50:04  
**字数:** 531

## 导航路径
DApp 连接钱包 > Bitcoin > Provider API (Signet)

## 目录
- 什么是 Injected provider API (Signet) ？
- connect
- signMessage
- signPsbt
- signPsbts

---

Provider API (Signet)
#
什么是 Injected provider API (Signet) ？
#
OKX Injected Providers API (Signet) 基于 JavaScript 模型，由 OKX 嵌入用户访问网站中。DApp 项目可以通过调用此 API 请求用户账户信息，从用户所连接的区块链中读取数据，并协助用户进行消息和交易的签署。
注：BTC Signet 仅适用于钱包插件端为 2.82.32 或更高版本。
connect
#
okxwallet.bitcoinSignet.connect()
描述
连接钱包
参数
无
返回值
Promise - object
address - string：当前账户的地址
publicKey - string：当前账户的公钥
示例
const
result
=
await
okxwallet
.
bitcoinSignet
.
connect
(
)
// example
{
address
:
'bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq'
,
publicKey
:
'4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497'
}
signMessage
#
okxwallet.bitcoinSignet.signMessage(signStr[, type])
描述
签名消息
参数
signStr - string：需要签名的数据
type - string： (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"
返回值
Promise - string：签名结果
示例
const
signStr
=
'need sign string'
;
const
result
=
await
window
.
okxwallet
.
bitcoinSignet
.
signMessage
(
signStr
,
'ecdsa'
)
// example
INg2ZeG8b6GsiYLiWeQQpvmfFHqCt3zC6ocdlN9ZRQLhSFZdGhgYWF8ipar1wqJtYufxzSYiZm5kdlAcnxgZWQU
=
signPsbt
#
okxwallet.bitcoinSignet.signPsbt(psbtHex[, options])
描述
签名 psbt，该方法将遍历所有与当前地址匹配的输入进行签名
参数
psbtHex - string：要签名的 psbt 的十六进制字符串
注
构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。
示例：可参考下面的 txInput 和 publicKey。
const
txInputs
:
utxoInput
[
]
=
[
]
;
txInputs
.
push
(
{
txId
:
"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"
,
vOut
:
2
,
amount
:
341474
,
address
:
"tb1q8h8....mjxzny"
,
privateKey
:
"0s79......ldjejke"
,
publicKey
:
"tb1q8h8....mjxzny"
,
bip32Derivation
:
[
{
"masterFingerprint"
:
"a22e8e32"
,
"pubkey"
:
"tb1q8h8....mjxzny"
,
"path"
:
"m/49'/0'/0'/0/0"
,
}
,
]
,
}
)
;
options
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名
返回值
Promise - string：已签名 psbt 的十六进制字符串
示例
try
{
let
res
=
await
okxwallet
.
bitcoinSignet
.
signPsbt
(
'70736274ff01007d....'
,
{
autoFinalized
:
false
,
toSignInputs
:
[
{
index
:
0
,
address
:
'tb1q8h8....mjxzny'
,
}
,
{
index
:
1
,
publicKey
:
'tb1q8h8....mjxzny'
,
sighashTypes
:
[
1
]
,
}
,
{
index
:
2
,
publicKey
:
'02062...8779693f'
,
}
,
]
,
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
e
)
{
console
.
log
(
e
)
;
}
okxwallet
.
bitcoinSignet
.
signPsbt
(
'xxxxxxxx'
,
{
toSignInputs
:
[
{
index
:
0
,
publicKey
:
'xxxxxx'
,
disableTweakSigner
:
true
}
]
,
autoFinalized
:
false
,
}
)
;
signPsbts
#
okxwallet.bitcoinSignet.signPsbts(psbtHexs[, options])
描述
签署多个 psbt，该方法将遍历所有与当前地址匹配的输入进行签名
参数
psbtHexs - string[]：要签名的 psbt 的十六进制字符串
注
构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。
示例：可参考下面的 txInput 和 publicKey。
const
txInputs
:
utxoInput
[
]
=
[
]
;
txInputs
.
push
(
{
txId
:
"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"
,
vOut
:
2
,
amount
:
341474
,
address
:
"tb1q8h8....mjxzny"
,
privateKey
:
"0s79......ldjejke"
,
publicKey
:
"tb1q8h8....mjxzny"
,
bip32Derivation
:
[
{
"masterFingerprint"
:
"a22e8e32"
,
"pubkey"
:
"tb1q8h8....mjxzny"
,
"path"
:
"m/49'/0'/0'/0/0"
,
}
,
]
,
}
)
;
options - object[]：签署 psbt 的选项
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
返回值
Promise - string[]：已签名 psbt 的十六进制字符串
示例
try
{
let
res
=
await
okxwallet
.
bitcoinSignet
.
signPsbts
(
[
'70736274ff01007d...'
,
'70736274ff01007d...'
,
]
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
e
)
{
console
.
log
(
e
)
;
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api-(signet)">Provider API (Signet)<a class="index_header-anchor__Xqb+L" href="#provider-api-(signet)" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API (Signet) ？" id="什么是-injected-provider-api-(signet)-？">什么是 Injected provider API (Signet) ？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api-(signet)-？" style="opacity:0">#</a></h2>
<p>OKX Injected Providers API (Signet) 基于 JavaScript 模型，由 OKX 嵌入用户访问网站中。DApp 项目可以通过调用此 API 请求用户账户信息，从用户所连接的区块链中读取数据，并协助用户进行消息和交易的签署。</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R7bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R7bf:">注：BTC Signet 仅适用于钱包插件端为 2.82.32 或更高版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<h2 data-content="connect" id="connect">connect<a class="index_header-anchor__Xqb+L" href="#connect" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoinSignet.connect()</code></p>
<p><strong>描述</strong></p>
<p>连接钱包</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>address - string：当前账户的地址</li>
<li>publicKey - string：当前账户的公钥</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoinSignet<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  address<span class="token operator">:</span> <span class="token string">'bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq'</span><span class="token punctuation">,</span>
  publicKey<span class="token operator">:</span> <span class="token string">'4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="signMessage" id="signmessage">signMessage<a class="index_header-anchor__Xqb+L" href="#signmessage" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoinSignet.signMessage(signStr[, type])</code></p>
<p><strong>描述</strong></p>
<p>签名消息</p>
<p><strong>参数</strong></p>
<ul>
<li>signStr - string：需要签名的数据</li>
<li>type - string： (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：签名结果</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> signStr <span class="token operator">=</span> <span class="token string">'need sign string'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoinSignet<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>signStr<span class="token punctuation">,</span> <span class="token string">'ecdsa'</span><span class="token punctuation">)</span>
<span class="token comment">// example</span>
INg2ZeG8b6GsiYLiWeQQpvmfFHqCt3zC6ocdlN9ZRQLhSFZdGhgYWF8ipar1wqJtYufxzSYiZm5kdlAcnxgZWQU<span class="token operator">=</span>
</code></pre></div>
<h2 data-content="signPsbt" id="signpsbt">signPsbt<a class="index_header-anchor__Xqb+L" href="#signpsbt" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoinSignet.signPsbt(psbtHex[, options])</code></p>
<p><strong>描述</strong></p>
<p>签名 psbt，该方法将遍历所有与当前地址匹配的输入进行签名</p>
<p><strong>参数</strong></p>
<ul>
<li>psbtHex - string：要签名的 psbt 的十六进制字符串</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R1tbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R1tbf:">注</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。</p><p>示例：可参考下面的 txInput 和 publicKey。</p></div></div></div></div></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> txInputs<span class="token operator">:</span> utxoInput<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
txInputs<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">341474</span><span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      privateKey<span class="token operator">:</span> <span class="token string">"0s79......ldjejke"</span><span class="token punctuation">,</span>
      publicKey<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      bip32Derivation<span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
              <span class="token string-property property">"masterFingerprint"</span><span class="token operator">:</span> <span class="token string">"a22e8e32"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"path"</span><span class="token operator">:</span> <span class="token string">"m/49'/0'/0'/0/0"</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>options<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
<li>disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：已签名 psbt 的十六进制字符串</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoinSignet<span class="token punctuation">.</span><span class="token function">signPsbt</span><span class="token punctuation">(</span><span class="token string">'70736274ff01007d....'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
    toSignInputs<span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
        address<span class="token operator">:</span> <span class="token string">'tb1q8h8....mjxzny'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        publicKey<span class="token operator">:</span> <span class="token string">'tb1q8h8....mjxzny'</span><span class="token punctuation">,</span>
        sighashTypes<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
        publicKey<span class="token operator">:</span> <span class="token string">'02062...8779693f'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

okxwallet<span class="token punctuation">.</span>bitcoinSignet<span class="token punctuation">.</span><span class="token function">signPsbt</span><span class="token punctuation">(</span><span class="token string">'xxxxxxxx'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
  toSignInputs<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> index<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span> publicKey<span class="token operator">:</span> <span class="token string">'xxxxxx'</span><span class="token punctuation">,</span> disableTweakSigner<span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="signPsbts" id="signpsbts">signPsbts<a class="index_header-anchor__Xqb+L" href="#signpsbts" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoinSignet.signPsbts(psbtHexs[, options])</code></p>
<p><strong>描述</strong></p>
<p>签署多个 psbt，该方法将遍历所有与当前地址匹配的输入进行签名</p>
<p><strong>参数</strong></p>
<ul>
<li>psbtHexs - string[]：要签名的 psbt 的十六进制字符串</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R2nbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R2nbf:">注</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。</p><p>示例：可参考下面的 txInput 和 publicKey。</p></div></div></div></div></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> txInputs<span class="token operator">:</span> utxoInput<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
txInputs<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">341474</span><span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      privateKey<span class="token operator">:</span> <span class="token string">"0s79......ldjejke"</span><span class="token punctuation">,</span>
      publicKey<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      bip32Derivation<span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
              <span class="token string-property property">"masterFingerprint"</span><span class="token operator">:</span> <span class="token string">"a22e8e32"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"path"</span><span class="token operator">:</span> <span class="token string">"m/49'/0'/0'/0/0"</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>options - object[]：签署 psbt 的选项<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string[]：已签名 psbt 的十六进制字符串</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoinSignet<span class="token punctuation">.</span><span class="token function">signPsbts</span><span class="token punctuation">(</span><span class="token punctuation">[</span>
    <span class="token string">'70736274ff01007d...'</span><span class="token punctuation">,</span>
    <span class="token string">'70736274ff01007d...'</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "Bitcoin",
    "Provider API (Signet)"
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
    "Provider API",
    "Provider API (Fractal Bitcoin)",
    "Provider API (Testnet)",
    "Provider API (Signet)"
  ],
  "toc": [
    "什么是 Injected provider API (Signet) ？",
    "connect",
    "signMessage",
    "signPsbt",
    "signPsbts"
  ]
}
```

</details>
