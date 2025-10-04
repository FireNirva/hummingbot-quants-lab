# 运行第一个程序 | 开始 | 首页 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-run-application#运行第一个程序  
**抓取时间:** 2025-05-27 01:09:25  
**字数:** 237

## 导航路径
DEX API > 首页 > 运行第一个程序

## 目录
- 初始化HTTP客户端
- 获取报价示例 (SOL → USDC)

---

运行第一个程序
#
完成环境配置后，你可通过以下代码示例运行首个链上交互应用。
初始化HTTP客户端
#
import
{
OKXDexClient
}
from
'@okx-dex/okx-dex-sdk'
;
import
'dotenv/config'
;
// 初始化DEX客户端
const
client
=
new
OKXDexClient
(
{
apiKey
:
process
.
env
.
OKX_API_KEY
!
,
// 从环境变量获取API密钥
secretKey
:
process
.
env
.
OKX_SECRET_KEY
!
,
// 安全凭证密钥
apiPassphrase
:
process
.
env
.
OKX_API_PASSPHRASE
!
,
// 加密口令
projectId
:
process
.
env
.
OKX_PROJECT_ID
!
,
// 开发者平台创建的项目ID
// 链上交互配置（以Solana为例）
solana
:
{
connection
:
{
rpcUrl
:
process
.
env
.
SOLANA_RPC_URL
!
,
// 节点RPC地址
confirmTransactionInitialTimeout
:
60000
// 交易确认超时设置
}
,
privateKey
:
process
.
env
.
SOLANA_PRIVATE_KEY
!
,
// 钱包私钥（加密存储）
walletAddress
:
process
.
env
.
SOLANA_WALLET_ADDRESS
!
// 钱包地址
}
}
)
;
获取报价示例 (SOL → USDC)
#
async
function
main
(
)
{
try
{
// 获取兑换报价
const
quote
=
await
client
.
dex
.
getQuote
(
{
chainIndex
:
'501'
,
// Solana主网链ID
fromTokenAddress
:
'So11111111111111111111111111111111111111112'
,
// SOL代币地址
toTokenAddress
:
'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
,
// USDC代币地址
amount
:
'1000000000'
,
// 兑换数量（基础单位精度）
slippage
:
'0.1'
// 滑点容忍度（0.1%）
}
)
;
console
.
log
(
'兑换报价详情:'
,
JSON
.
stringify
(
quote
,
null
,
2
)
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
'交易异常:'
,
error
)
;
}
}
// 执行报价查询
main
(
)
;
解释
关键参数说明：
chainIndex：各公链的唯一标识符 (501 = Solana 主网)
slippage：建议根据市场波动性动态调整 (范围 0.1-1%)
amount：需转换为代币最小单位 (如 SOL 的 Lamport 精度)
如需查看更多示例，请访问获取：
交易 API

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="运行第一个程序">运行第一个程序<a class="index_header-anchor__Xqb+L" href="#运行第一个程序" style="opacity:0">#</a></h1>
<p>完成环境配置后，你可通过以下代码示例运行首个链上交互应用。</p>
<h2 data-content="初始化HTTP客户端" id="初始化http客户端">初始化HTTP客户端<a class="index_header-anchor__Xqb+L" href="#初始化http客户端" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">OKXDexClient</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@okx-dex/okx-dex-sdk'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token string">'dotenv/config'</span><span class="token punctuation">;</span>

<span class="token comment">// 初始化DEX客户端</span>
<span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXDexClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  <span class="token literal-property property">apiKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 从环境变量获取API密钥</span>
  <span class="token literal-property property">secretKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 安全凭证密钥</span>
  <span class="token literal-property property">apiPassphrase</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 加密口令</span>
  <span class="token literal-property property">projectId</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 开发者平台创建的项目ID</span>
  <span class="token comment">// 链上交互配置（以Solana为例）</span>
  <span class="token literal-property property">solana</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">connection</span><span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">rpcUrl</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 节点RPC地址</span>
      <span class="token literal-property property">confirmTransactionInitialTimeout</span><span class="token operator">:</span> <span class="token number">60000</span> <span class="token comment">// 交易确认超时设置</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token literal-property property">privateKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_PRIVATE_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span> <span class="token comment">// 钱包私钥（加密存储）</span>
    <span class="token literal-property property">walletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_WALLET_ADDRESS</span><span class="token operator">!</span> <span class="token comment">// 钱包地址</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="获取报价示例 (SOL → USDC)" id="获取报价示例-(sol-→-usdc)">获取报价示例 (SOL → USDC)<a class="index_header-anchor__Xqb+L" href="#获取报价示例-(sol-→-usdc)" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// 获取兑换报价</span>
        <span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">chainIndex</span><span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span> <span class="token comment">// Solana主网链ID</span>
            <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'So11111111111111111111111111111111111111112'</span><span class="token punctuation">,</span> <span class="token comment">// SOL代币地址</span>
            <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC代币地址</span>
            <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'1000000000'</span><span class="token punctuation">,</span> <span class="token comment">// 兑换数量（基础单位精度）</span>
            <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.1'</span> <span class="token comment">// 滑点容忍度（0.1%）</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'兑换报价详情:'</span><span class="token punctuation">,</span> <span class="token known-class-name class-name">JSON</span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>quote<span class="token punctuation">,</span> <span class="token keyword null nil">null</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'交易异常:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// 执行报价查询</span>
<span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rdbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rdbf:">解释</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>关键参数说明：</p><ul>
<li>chainIndex：各公链的唯一标识符 (501 = Solana 主网)</li>
<li>slippage：建议根据市场波动性动态调整 (范围 0.1-1%)</li>
<li>amount：需转换为代币最小单位 (如 SOL 的 Lamport 精度)</li>
</ul></div></div></div></div></div>
<p>如需查看更多示例，请访问获取：</p>
<div><a class="flex index_card__PinRP" href="../dex-api/dex-use-swap-quick-start" target="_self"><picture class="okui-picture shrink-0 index_pic__wsTn5 okui-picture-font"><img alt="交易 API" class="index_img__o7soA" src="https://web3.okx.com/cdn/assets/imgs/253/11D9FE79530B884A.png"/></picture><div class="flex justify-between items-center grow index_right-content__lybMm"><div class="index_text-wrapper__M1izi"><div class="truncate index_text__My7kF">交易 API</div></div><div class="flex justify-center items-center index_icon-border__Hx94n"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-pointer-right-md index_icon__V7Qx8" role="img"></i></div></div></a></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "首页",
    "运行第一个程序"
  ],
  "sidebar_links": [
    "什么是 DEX API",
    "API 访问和用法",
    "API 费用",
    "支持的链",
    "开发者平台",
    "环境设置",
    "运行第一个程序",
    "用户协议"
  ],
  "toc": [
    "初始化HTTP客户端",
    "获取报价示例 (SOL → USDC)"
  ]
}
```

</details>
