# 获取钱包地址 | Tron | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/tron/connect  
**抓取时间:** 2025-05-27 06:29:38  
**字数:** 137

## 导航路径
DApp 连接钱包 > Tron > 获取钱包地址

## 目录
- 创建连接
- 监听账户地址变化

---

获取钱包地址
#
钱包账户地址被用于多种场景，包括作为标识符和用于签名交易。
创建连接
#
此处建议提供一个按钮，允许用户将欧易 Web3 钱包 Tron 连接到 DApp。
在下方的示例项目代码中，JavaScript 代码在用户点击连接按钮时访问用户的帐户地址，HTML 代码显示按钮和当前帐户地址：
Connect Tron
HTML
JavaScript
<
button
class
=
"
connectTronButton
"
>
Connect to Tron
</
button
>
const
connectTronButton
=
document
.
querySelector
(
'.connectTronButton'
)
;
connectTronButton
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
window
.
okxwallet
.
tronLink
.
request
(
{
method
:
'tron_requestAccounts'
}
)
}
)
;
监听账户地址变化
#
您可以使用事件来监听变化:
window
.
addEventListener
(
'message'
,
function
(
e
)
{
if
(
e
.
data
.
message
&&
e
.
data
.
message
.
action
===
"accountsChanged"
)
{
// handler logic
console
.
log
(
'got accountsChanged event'
,
e
.
data
,
e
.
data
.
message
.
address
)
}
}
)
每当
tron_requestAccounts
RPC 方法的返回值发生变化时，欧易都会发出对应事件提醒。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="获取钱包地址">获取钱包地址<a class="index_header-anchor__Xqb+L" href="#获取钱包地址" style="opacity:0">#</a></h1>
<p>钱包账户地址被用于多种场景，包括作为标识符和用于签名交易。</p>
<h2 data-content="创建连接" id="创建连接">创建连接<a class="index_header-anchor__Xqb+L" href="#创建连接" style="opacity:0">#</a></h2>
<p>此处建议提供一个按钮，允许用户将欧易 Web3 钱包 Tron 连接到 DApp。</p>
<p>在下方的示例项目代码中，JavaScript 代码在用户点击连接按钮时访问用户的帐户地址，HTML 代码显示按钮和当前帐户地址：</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Tron</span></button></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":Rdbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":Rdbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":Rdbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectTronButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect to Tron<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":Rdbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectTronButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectTronButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectTronButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">//Will Start the OKX extension</span>
  <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">okxwallet</span><span class="token punctuation">.</span><span class="token property-access">tronLink</span><span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'tron_requestAccounts'</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="监听账户地址变化" id="监听账户地址变化">监听账户地址变化<a class="index_header-anchor__Xqb+L" href="#监听账户地址变化" style="opacity:0">#</a></h2>
<p>您可以使用事件来监听变化:</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">window<span class="token punctuation">.</span><span class="token function">addEventListener</span><span class="token punctuation">(</span><span class="token string">'message'</span><span class="token punctuation">,</span> <span class="token keyword">function</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">if</span> <span class="token punctuation">(</span>e<span class="token punctuation">.</span>data<span class="token punctuation">.</span>message <span class="token operator">&amp;&amp;</span> e<span class="token punctuation">.</span>data<span class="token punctuation">.</span>message<span class="token punctuation">.</span>action <span class="token operator">===</span> <span class="token string">"accountsChanged"</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// handler logic</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'got accountsChanged event'</span><span class="token punctuation">,</span> e<span class="token punctuation">.</span>data<span class="token punctuation">,</span> e<span class="token punctuation">.</span>data<span class="token punctuation">.</span>message<span class="token punctuation">.</span>address<span class="token punctuation">)</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div>
<p>每当 <code>tron_requestAccounts</code> RPC 方法的返回值发生变化时，欧易都会发出对应事件提醒。</p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "Tron",
    "获取钱包地址"
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
    "获取钱包地址",
    "Provider API",
    "Solana 兼容链"
  ],
  "toc": [
    "创建连接",
    "监听账户地址变化"
  ]
}
```

</details>
