# 获取钱包地址 | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/web-access-user-accounts#更多链的账户地址获取  
**抓取时间:** 2025-05-27 06:32:33  
**字数:** 118

## 导航路径
DApp 连接钱包 > EVM > 获取钱包地址

## 目录
- 创建连接
- 监听账户地址变化
- 更多链的账户地址获取

---

获取钱包地址
#
钱包地址被用于多种场景，包括作为标识符和用于签名交易。
以以太坊为例，以太坊地址是账户的唯一公开标识符，每个账户都有一个对应的地址，地址用于在网络上进行交互和识别，而账户则包含了与该地址相关的所有状态信息和功能。
如果想请求用户的签名或让用户批准一笔交易，DApp 必须使用 eth_requestAccounts RPC 方法来访问用户的账户。
创建连接
#
此处建议提供一个按钮，允许用户将欧易 Web3 钱包连接到 DApp。选择此按钮可调用
eth_requestAccounts
方法来访问用户帐户地址。
在下方的示例项目代码中，JavaScript 代码在用户点击连接按钮时访问用户的帐户地址，HTML 代码显示按钮和当前帐户地址：
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
Connect to Ethereum
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
监听账户地址变化
#
您可以使用事件来监听变化:
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
RPC 方法的返回值发生变化时，欧易都会发出对应事件提醒。
eth_accounts
会返回一个为空或包含单个账户地址的数组，返回的账户地址如果存在，即为允许调用者访问的最近使用的账户地址。
由于调用者由其 URL
origin
标识，所以具有相同来源（origin）的站点会持有相同的权限。只要用户公开的账户地址发生变化，就会发出
accountsChanged
。
更多链的账户地址获取
#
更多链的账户获取方法见
Injected providers
。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="获取钱包地址">获取钱包地址<a class="index_header-anchor__Xqb+L" href="#获取钱包地址" style="opacity:0">#</a></h1>
<p>钱包地址被用于多种场景，包括作为标识符和用于签名交易。</p>
<p>以以太坊为例，以太坊地址是账户的唯一公开标识符，每个账户都有一个对应的地址，地址用于在网络上进行交互和识别，而账户则包含了与该地址相关的所有状态信息和功能。</p>
<p>如果想请求用户的签名或让用户批准一笔交易，DApp 必须使用 eth_requestAccounts RPC 方法来访问用户的账户。</p>
<h2 data-content="创建连接" id="创建连接">创建连接<a class="index_header-anchor__Xqb+L" href="#创建连接" style="opacity:0">#</a></h2>
<p>此处建议提供一个按钮，允许用户将欧易 Web3 钱包连接到 DApp。选择此按钮可调用 <code>eth_requestAccounts</code> 方法来访问用户帐户地址。</p>
<p>在下方的示例项目代码中，JavaScript 代码在用户点击连接按钮时访问用户的帐户地址，HTML 代码显示按钮和当前帐户地址：</p>
<div><button class="okui-btn btn-md btn-fill-highlight" type="button"><span class="btn-content">Connect Ethereum</span></button></div>
<div class="okui-tabs" style="height:auto;margin-top:14px"><div class="okui-tabs-pane-list okui-tabs-pane-list-md okui-tabs-pane-list-blue okui-tabs-pane-list-underline"><div class="okui-tabs-pane-list-wrapper underline-special-style"><div class="okui-tabs-pane-list-container" role="tablist"><div class="okui-tabs-pane-list-flex-shrink"><div aria-selected="true" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline okui-tabs-pane-underline-active" data-pane-id="HTML" id=":Rhbf:-HTML" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="0">HTML</div><div aria-selected="false" class="okui-tabs-pane okui-tabs-pane-spacing okui-tabs-pane-md okui-tabs-pane-blue okui-tabs-pane-underline" data-pane-id="JavaScript" id=":Rhbf:-JavaScript" role="tab" style="--okd-inner-tabs-spacing:8px" tabindex="-1">JavaScript</div></div></div></div></div><div class="okui-tabs-panel-list"><div aria-hidden="false" aria-labelledby=":Rhbf:-HTML" class="okui-tabs-panel okui-tabs-panel-show" role="tabpanel" tabindex="0"><div class="remark-highlight"><pre class="language-html"><code class="language-html"><span class="token tag"><span class="token tag"><span class="token punctuation">&lt;</span>button</span> <span class="token attr-name">class</span><span class="token attr-value"><span class="token punctuation attr-equals">=</span><span class="token punctuation">"</span>connectEthereumButton<span class="token punctuation">"</span></span><span class="token punctuation">&gt;</span></span>Connect to Ethereum<span class="token tag"><span class="token tag"><span class="token punctuation">&lt;/</span>button</span><span class="token punctuation">&gt;</span></span>
</code></pre></div></div><div aria-hidden="true" aria-labelledby=":Rhbf:-JavaScript" class="okui-tabs-panel" role="tabpanel" tabindex="-1"><div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> connectEthereumButton <span class="token operator">=</span> <span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">querySelector</span><span class="token punctuation">(</span><span class="token string">'.connectEthereumButton'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

connectEthereumButton<span class="token punctuation">.</span><span class="token method function property-access">addEventListener</span><span class="token punctuation">(</span><span class="token string">'click'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">//Will Start the OKX extension</span>
  okxwallet<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span><span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'eth_requestAccounts'</span> <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div></div></div>
<h2 data-content="监听账户地址变化" id="监听账户地址变化">监听账户地址变化<a class="index_header-anchor__Xqb+L" href="#监听账户地址变化" style="opacity:0">#</a></h2>
<p>您可以使用事件来监听变化:</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxwallet<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>accounts<span class="token operator">:</span> <span class="token builtin">Array</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">void</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>每当 <code>eth_accounts</code> RPC 方法的返回值发生变化时，欧易都会发出对应事件提醒。
<code>eth_accounts</code> 会返回一个为空或包含单个账户地址的数组，返回的账户地址如果存在，即为允许调用者访问的最近使用的账户地址。</p>
<p>由于调用者由其 URL <em>origin</em> 标识，所以具有相同来源（origin）的站点会持有相同的权限。只要用户公开的账户地址发生变化，就会发出 <code>accountsChanged</code>。</p>
<h2 data-content="更多链的账户地址获取" id="更多链的账户地址获取">更多链的账户地址获取<a class="index_header-anchor__Xqb+L" href="#更多链的账户地址获取" style="opacity:0">#</a></h2>
<p>更多链的账户获取方法见 <a href="/zh-hans/build/dev-docs/sdks/chains/evm/provider">Injected providers</a>。</p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
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
    "获取钱包地址",
    "获取 chainId",
    "添加代币",
    "签名交易",
    "智能合约交互"
  ],
  "toc": [
    "创建连接",
    "监听账户地址变化",
    "更多链的账户地址获取"
  ]
}
```

</details>
