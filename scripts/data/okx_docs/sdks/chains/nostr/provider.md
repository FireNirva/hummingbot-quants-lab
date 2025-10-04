# Provider API | nostr | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/nostr/provider#连接钱包的简单示例  
**抓取时间:** 2025-05-27 05:50:35  
**字数:** 372

## 导航路径
DApp 连接钱包 > nostr > Provider API

## 目录
- 什么是 Injected provider API？
- 获取注入的对象
- 连接钱包的简单示例
- 获取公钥
- 签名 Event
- 对消息进行加密
- 对消息进行解密
- 添加/移除事件监听

---

Provider API
#
什么是 Injected provider API？
#
欧易 Injected providers API 是一个 JavaScript API，欧易将其注入用户访问的网站。您的 DApp 可以使用此 API 请求用户帐户，从用户连接的区块链读取数据，帮助用户签署消息和交易。
获取注入的对象
#
Dapp 可以通过如下方式访问注入的对象：
window.okxwallet.nostr
连接钱包的简单示例
#
try
{
const
publicKey
=
await
window
.
okxwallet
.
nostr
.
getPublicKey
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
获取公钥
#
window.okxwallet.nostr.getPublicKey(): Promise<string>
描述
返回当前连接的帐户的公钥。
返回值
publicKey
- string: 当前连接的帐户的公钥。
try
{
const
publicKey
=
await
window
.
okxwallet
.
nostr
.
getPublicKey
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
签名 Event
#
window.okxwallet.nostr.signEvent(event: Event): Promise<SignedEvent>
描述
对 Event 进行签名。
入参
event
- object
created_at
- number: 事件创建时间
kind
- number: 事件类型
tags
- string[][]: 事件标签
content
- string: 事件内容
返回值
event
- SignedEvent：除了包含 event 入参的所有属性外，还包含如下属性
id
- string: 唯一标识
pubkey
- string: 公钥
sig
- string: 签名
const
event
=
{
content
:
"hello"
,
kind
:
4
,
"tags"
:
[
[
"p"
,
"693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8"
]
,
[
"r"
,
"json"
]
,
[
"a"
,
"b4f4e689fca78ebcaeec72162628ba61c51a62e1420b9b8ca8cb63d9a7e26219"
]
]
,
"created_at"
:
1700726837
,
}
const
signedEvent
=
await
window
.
okxwallet
.
nostr
.
signEvent
(
event
)
console
.
log
(
signedEvent
.
id
)
console
.
log
(
signedEvent
.
pubkey
)
console
.
log
(
signedEvent
.
sig
)
对消息进行加密
#
window.okxwallet.nostr.nip04.encrypt(pubkey: string, message: string): Promise<string>
描述
根据
NIP-04
规范对消息进行加密
返回值
encryptMsg
- string: 加密的结果
const
pubkey
=
'693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8'
const
msg
=
'hello world'
const
encryptMsg
=
await
window
.
okxwallet
.
nostr
.
nip04
.
encrypt
(
pubkey
,
msg
)
;
console
.
log
(
encryptMsg
)
对消息进行解密
#
window.okxwallet.nostr.nip04.decrypt(pubkey: string, message: string): Promise<string>
描述
根据
NIP-04
规范对消息进行解密
返回值
decryptMsg
- string: 解密的结果
const
pubkey
=
'693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8'
const
msg
=
'VVPplRPF0w4dNZkuiQ==?iv=Nrb7gcph/9eKuqyuDx0yKQ=='
const
decryptMsg
=
await
window
.
okxwallet
.
nostr
.
nip04
.
decrypt
(
pubkey
,
msg
)
;
console
.
log
(
decryptMsg
)
添加/移除事件监听
#
window.okxwallet.nostr.on(event:string, callback: Function): Promise<void>
window.okxwallet.nostr.off(event:string, callback: Function): Promise<void>
描述
添加事件监听，目前支持的事件有：
accountChanged
：当用户切换账户时会触发该事件
window
.
okxwallet
.
nostr
.
on
(
'accountChanged'
,
async
(
)
=>
{
const
publicKey
=
await
window
.
okxwallet
.
nostr
.
getPublicKey
(
)
;
console
.
log
(
publicKey
)
}
)

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
<li><code>window.okxwallet.nostr</code></li>
</ul>
<h2 data-content="连接钱包的简单示例" id="连接钱包的简单示例">连接钱包的简单示例<a class="index_header-anchor__Xqb+L" href="#连接钱包的简单示例" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> publicKey <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token method function property-access">getPublicKey</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="获取公钥" id="获取公钥">获取公钥<a class="index_header-anchor__Xqb+L" href="#获取公钥" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.nostr.getPublicKey(): Promise&lt;string&gt;</code></p>
<p><strong>描述</strong></p>
<p>返回当前连接的帐户的公钥。</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>publicKey</code> - string: 当前连接的帐户的公钥。</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> publicKey <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token method function property-access">getPublicKey</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="签名 Event" id="签名-event">签名 Event<a class="index_header-anchor__Xqb+L" href="#签名-event" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.nostr.signEvent(event: Event): Promise&lt;SignedEvent&gt;</code></p>
<p><strong>描述</strong></p>
<p>对 Event 进行签名。</p>
<p><strong>入参</strong></p>
<ul>
<li><code>event</code> - object<!-- -->
<ul>
<li><code>created_at</code> - number: 事件创建时间</li>
<li><code>kind</code> - number: 事件类型</li>
<li><code>tags</code> - string[][]: 事件标签</li>
<li><code>content</code> - string: 事件内容</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li><code>event</code> - SignedEvent：除了包含 event 入参的所有属性外，还包含如下属性<!-- -->
<ul>
<li><code>id</code> - string: 唯一标识</li>
<li><code>pubkey</code> - string: 公钥</li>
<li><code>sig</code> - string: 签名</li>
</ul>
</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> event <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">content</span><span class="token operator">:</span> <span class="token string">"hello"</span><span class="token punctuation">,</span>
    <span class="token literal-property property">kind</span><span class="token operator">:</span> <span class="token number">4</span><span class="token punctuation">,</span>
    <span class="token string-property property">"tags"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">[</span>
            <span class="token string">"p"</span><span class="token punctuation">,</span>
            <span class="token string">"693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8"</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">[</span>
            <span class="token string">"r"</span><span class="token punctuation">,</span>
            <span class="token string">"json"</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token punctuation">[</span>
            <span class="token string">"a"</span><span class="token punctuation">,</span>
            <span class="token string">"b4f4e689fca78ebcaeec72162628ba61c51a62e1420b9b8ca8cb63d9a7e26219"</span>
        <span class="token punctuation">]</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"created_at"</span><span class="token operator">:</span> <span class="token number">1700726837</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
<span class="token keyword">const</span> signedEvent <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token method function property-access">signEvent</span><span class="token punctuation">(</span>event<span class="token punctuation">)</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>signedEvent<span class="token punctuation">.</span><span class="token property-access">id</span><span class="token punctuation">)</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>signedEvent<span class="token punctuation">.</span><span class="token property-access">pubkey</span><span class="token punctuation">)</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>signedEvent<span class="token punctuation">.</span><span class="token property-access">sig</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="对消息进行加密" id="对消息进行加密">对消息进行加密<a class="index_header-anchor__Xqb+L" href="#对消息进行加密" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.nostr.nip04.encrypt(pubkey: string, message: string): Promise&lt;string&gt;</code></p>
<p><strong>描述</strong></p>
<p>根据 <a class="items-center" href="https://github.com/nostr-protocol/nips/blob/master/04.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">NIP-04<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 规范对消息进行加密</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>encryptMsg</code> - string: 加密的结果</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> pubkey <span class="token operator">=</span> <span class="token string">'693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8'</span>
<span class="token keyword">const</span> msg <span class="token operator">=</span> <span class="token string">'hello world'</span>
<span class="token keyword">const</span> encryptMsg <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token property-access">nip04</span><span class="token punctuation">.</span><span class="token method function property-access">encrypt</span><span class="token punctuation">(</span>pubkey<span class="token punctuation">,</span> msg<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>encryptMsg<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="对消息进行解密" id="对消息进行解密">对消息进行解密<a class="index_header-anchor__Xqb+L" href="#对消息进行解密" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.nostr.nip04.decrypt(pubkey: string, message: string): Promise&lt;string&gt;</code></p>
<p><strong>描述</strong></p>
<p>根据 <a class="items-center" href="https://github.com/nostr-protocol/nips/blob/master/04.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">NIP-04<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 规范对消息进行解密</p>
<p><strong>返回值</strong></p>
<ul>
<li><code>decryptMsg</code> - string: 解密的结果</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> pubkey <span class="token operator">=</span> <span class="token string">'693d3f45b81c1f3557383fb955f3a8cb2c194c44ffba1e2f4566e678773b44f8'</span>
<span class="token keyword">const</span> msg <span class="token operator">=</span> <span class="token string">'VVPplRPF0w4dNZkuiQ==?iv=Nrb7gcph/9eKuqyuDx0yKQ=='</span>
<span class="token keyword">const</span> decryptMsg <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token property-access">nip04</span><span class="token punctuation">.</span><span class="token method function property-access">decrypt</span><span class="token punctuation">(</span>pubkey<span class="token punctuation">,</span> msg<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>decryptMsg<span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="添加/移除事件监听" id="添加/移除事件监听">添加/移除事件监听<a class="index_header-anchor__Xqb+L" href="#添加/移除事件监听" style="opacity:0">#</a></h2>
<p><code>window.okxwallet.nostr.on(event:string, callback: Function): Promise&lt;void&gt;</code></p>
<p><code>window.okxwallet.nostr.off(event:string, callback: Function): Promise&lt;void&gt;</code></p>
<p><strong>描述</strong></p>
<p>添加事件监听，目前支持的事件有：</p>
<ul>
<li><code>accountChanged</code>：当用户切换账户时会触发该事件</li>
</ul>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'accountChanged'</span><span class="token punctuation">,</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> publicKey <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">nostr</span><span class="token punctuation">.</span><span class="token method function property-access">getPublicKey</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>publicKey<span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "nostr",
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
    "连接钱包的简单示例",
    "获取公钥",
    "签名 Event",
    "对消息进行加密",
    "对消息进行解密",
    "添加/移除事件监听"
  ]
}
```

</details>
