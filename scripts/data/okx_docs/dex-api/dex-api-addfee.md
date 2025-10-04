# 设置分佣 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-api-addfee#设置分佣  
**抓取时间:** 2025-05-27 00:26:45  
**字数:** 269

## 导航路径
DEX API > 交易 API > 设置分佣

## 目录
- 搭建兑换应用
- 搭建跨链应用
- 介绍
- API 参考
- 设置分佣
- DEX 集成
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 支持的跨链桥
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 错误码

---

设置分佣
#
OKX DEX API 支持为代币兑换，配置分佣费用和费用接收地址。
您可以将分佣相关参数包含在兑换报价中，来设置并收取分佣，对多数支持的链，每笔兑换最多收取 3% 的分佣费用，而针对 Solana 链每笔兑换最多收取 10% 的分佣费用。
OKX DEX API 计划从您向用户收取的分佣费中抽取一定比例。更多详细，请访问
API 费用
页面。
// 使用 quoteParams 来设置分佣
const quoteParams =
{
chainId
:
SOLANA_CHAIN_ID
,
amount
:
rawAmount
,
fromTokenAddress
,
toTokenAddress
,
slippage
:
"0.5"
,
userWalletAddress
:
userAddress
,
// 分佣相关的参数
fromTokenReferrerWalletAddress
:
"Your_REFERRER_WALLET_ADDRESS"
,
// 可选:基于询价币种接收分佣的地址
toTokenReferrerWalletAddress
:
"REFERRER_WALLET"
,
// 可选：基于目标币种接收分佣的地址
feePercent
:
"1.5"
,
// 可选：分佣比例 (0-3%, 最多 2 位小数)
}
as Record<string
,
string>;
分佣参数配置说明：
参数
feePercent
分佣比例，须介于 0 和 3% 之间。
参数
feePercent
最多支持2个小数点，例如传入 1.326%，但最终计算使用 1.32% 作为分佣比例。
对于 Solana，收取分佣的地址必须提前存入一些 SOL 以进行激活。
每笔交易只能从 fromToken 或 toToken 中选择一个作为分佣的来源。
分佣配置详细示例：
// 获取兑换报价
const quoteParams =
{
chainId
:
SOLANA_CHAIN_ID
,
amount
:
rawAmount
,
fromTokenAddress
,
toTokenAddress
,
slippage
:
"0.5"
,
userWalletAddress
:
userAddress
,
// Additional Fee params
fromTokenReferrerWalletAddress
:
"fee-recipient-wallet-address"
,
feePercent
:
"1"
,
// The wallet addresses to receive the commission fee (Each transaction can only choose commission from either the fromToken or the toToken)
// toTokenReferrerWalletAddress: "fee-recipient-wallet-address",
// fromTokenReferrerWalletAddress: "fee-recipient-wallet-address",
}
as Record<string
,
string>;
const timestamp = new Date().toISOString();
 const requestPath =
"/api/v5/dex/aggregator/swap"
;
 const queryString =
"?"
+ new URLSearchParams(quoteParams).toString();
 const headers = getHeaders(timestamp
,
"GET"
,
requestPath
,
queryString);

 const response = await fetch(
 `https
:
//web3.okx.com${requestPath}${queryString}`,
{
method
:
"GET"
,
headers
}
);

 const data = await response.json();
// .. Continue code implementation
分佣配置的命令行：
# Example
:
Swap .
01
SOL to USDC with
1.5
% fee to referrer
npx ts-node swap.ts .
01
11111111111111111111111111111111
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --referrer YOUR_REFERRER_ADDRESS --fee
1.5
计算示例的分佣费用说明：
以 1.5% 的分佣比例，向 100 USDC 的交易收取分佣，设置
toTokenReferrerWalletAddress
作为分佣接收地址参数：
分佣金额：1.5 USDC（100 USDC 的1.5%）
实际用户兑换成功金额：98.5 USDC
分佣（1.5 USDC）将发送到分佣接收地址

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="设置分佣">设置分佣<a class="index_header-anchor__Xqb+L" href="#设置分佣" style="opacity:0">#</a></h1>
<p>OKX DEX API 支持为代币兑换，配置分佣费用和费用接收地址。</p>
<p>您可以将分佣相关参数包含在兑换报价中，来设置并收取分佣，对多数支持的链，每笔兑换最多收取 3% 的分佣费用，而针对 Solana 链每笔兑换最多收取 10% 的分佣费用。</p>
<p>OKX DEX API 计划从您向用户收取的分佣费中抽取一定比例。更多详细，请访问 <a href="/zh-hans/build/dev-docs/dex-api/dex-api-fee">API 费用</a> 页面。</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token comment">// 使用 quoteParams 来设置分佣</span>
const quoteParams = <span class="token punctuation">{</span>
    chainId<span class="token operator">:</span> SOLANA_CHAIN_ID<span class="token punctuation">,</span>
    amount<span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
    fromTokenAddress<span class="token punctuation">,</span>
    toTokenAddress<span class="token punctuation">,</span>
    slippage<span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
    userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
    <span class="token comment">// 分佣相关的参数</span>
    fromTokenReferrerWalletAddress<span class="token operator">:</span> <span class="token string">"Your_REFERRER_WALLET_ADDRESS"</span><span class="token punctuation">,</span> <span class="token comment">// 可选:基于询价币种接收分佣的地址</span>
    toTokenReferrerWalletAddress<span class="token operator">:</span> <span class="token string">"REFERRER_WALLET"</span><span class="token punctuation">,</span> <span class="token comment">// 可选：基于目标币种接收分佣的地址</span>
    feePercent<span class="token operator">:</span> <span class="token string">"1.5"</span><span class="token punctuation">,</span>  <span class="token comment">// 可选：分佣比例 (0-3%, 最多 2 位小数)</span>

<span class="token punctuation">}</span> as Record&lt;string<span class="token punctuation">,</span> string&gt;;
</code></pre></div>
<p>分佣参数配置说明：</p>
<ul>
<li>参数<code>feePercent</code>分佣比例，须介于 0 和 3% 之间。</li>
<li>参数<code>feePercent</code>最多支持2个小数点，例如传入 1.326%，但最终计算使用 1.32% 作为分佣比例。</li>
<li>对于 Solana，收取分佣的地址必须提前存入一些 SOL 以进行激活。</li>
<li>每笔交易只能从 fromToken 或 toToken 中选择一个作为分佣的来源。</li>
</ul>
<p>分佣配置详细示例：</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token comment">// 获取兑换报价</span>
   const quoteParams = <span class="token punctuation">{</span>
       chainId<span class="token operator">:</span> SOLANA_CHAIN_ID<span class="token punctuation">,</span>
       amount<span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
       fromTokenAddress<span class="token punctuation">,</span>
       toTokenAddress<span class="token punctuation">,</span>
       slippage<span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
       userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>

       <span class="token comment">// Additional Fee params</span>
       fromTokenReferrerWalletAddress<span class="token operator">:</span> <span class="token string">"fee-recipient-wallet-address"</span><span class="token punctuation">,</span>
       feePercent<span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>

       <span class="token comment">// The wallet addresses to receive the commission fee (Each transaction can only choose commission from either the fromToken or the toToken)</span>
       <span class="token comment">// toTokenReferrerWalletAddress: "fee-recipient-wallet-address",</span>
       <span class="token comment">// fromTokenReferrerWalletAddress: "fee-recipient-wallet-address",</span>

   <span class="token punctuation">}</span> as Record&lt;string<span class="token punctuation">,</span> string&gt;;
</code></pre></div>
<div class="remark-highlight"><pre class="language-json"><code class="language-json">const timestamp = new Date().toISOString();
    const requestPath = <span class="token string">"/api/v5/dex/aggregator/swap"</span>;
    const queryString = <span class="token string">"?"</span> + new URLSearchParams(quoteParams).toString();
    const headers = getHeaders(timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString);

    const response = await fetch(
        `https<span class="token operator">:</span><span class="token comment">//web3.okx.com${requestPath}${queryString}`,</span>
        <span class="token punctuation">{</span> method<span class="token operator">:</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> headers <span class="token punctuation">}</span>
    );

    const data = await response.json();

    <span class="token comment">// .. Continue code implementation</span>
</code></pre></div>
<p>分佣配置的命令行：</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"># Example<span class="token operator">:</span> Swap .<span class="token number">01</span> SOL to USDC with <span class="token number">1.5</span>% fee to referrer
npx ts-node swap.ts .<span class="token number">01</span> <span class="token number">11111111111111111111111111111111</span> EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --referrer YOUR_REFERRER_ADDRESS --fee <span class="token number">1.5</span>
</code></pre></div>
<p>计算示例的分佣费用说明：</p>
<p>以 1.5% 的分佣比例，向 100 USDC 的交易收取分佣，设置<code>toTokenReferrerWalletAddress</code>作为分佣接收地址参数：</p>
<ul>
<li>分佣金额：1.5 USDC（100 USDC 的1.5%）</li>
<li>实际用户兑换成功金额：98.5 USDC</li>
<li>分佣（1.5 USDC）将发送到分佣接收地址</li>
</ul><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "设置分佣"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "设置分佣",
    "DEX 集成",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "支持的跨链桥",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "错误码"
  ],
  "toc": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "设置分佣",
    "DEX 集成",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "支持的跨链桥",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "错误码"
  ]
}
```

</details>
