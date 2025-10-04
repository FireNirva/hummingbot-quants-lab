# Sui 示例 | DEX SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-sdk-sui#创建币种助手-(可忽略)  
**抓取时间:** 2025-05-27 03:53:19  
**字数:** 816

## 导航路径
DEX API > 资源 > Sui 示例

## 目录
- 创建币种助手 (可忽略)
- 创建兑换指令
- 获取报价

---

Sui 示例
#
创建币种助手 (可忽略)
#
// Common tokens on Sui mainnet
export
const
TOKENS
=
{
SUI
:
"0x2::sui::SUI"
,
USDC
:
"0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"
}
as
const
;
创建兑换指令
#
// swap.ts
import
{
client
}
from
'./DexClient'
;
import
{
TOKENS
}
from
'./Tokens'
;
// Optional, if you created the token helper
/**
Example: Execute a swap from SUI to USDC
*/
async
function
executeSwap
(
)
{
try
{
if
(
!
process
.
env
.
SUI_PRIVATE_KEY
)
{
throw
new
Error
(
'Missing SUI_PRIVATE_KEY in .env file'
)
;
}
// First, get token information using a quote
console
.
log
(
"Getting token information..."
)
;
const
fromTokenAddress
=
TOKENS
.
SUI
;
// Or use directly: "0x2::sui::SUI"
const
toTokenAddress
=
TOKENS
.
USDC
;
// Or use directly: "0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"
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
chainId
:
'784'
,
// Sui chain ID
fromTokenAddress
,
toTokenAddress
,
amount
:
'1000000'
,
// Small amount for quote
slippage
:
'0.5'
}
)
;
const
tokenInfo
=
{
fromToken
:
{
symbol
:
quote
.
data
[
0
]
.
fromToken
.
tokenSymbol
,
decimals
:
parseInt
(
quote
.
data
[
0
]
.
fromToken
.
decimal
)
,
price
:
quote
.
data
[
0
]
.
fromToken
.
tokenUnitPrice
}
,
toToken
:
{
symbol
:
quote
.
data
[
0
]
.
toToken
.
tokenSymbol
,
decimals
:
parseInt
(
quote
.
data
[
0
]
.
toToken
.
decimal
)
,
price
:
quote
.
data
[
0
]
.
toToken
.
tokenUnitPrice
}
}
;
// Convert amount to base units
const
humanReadableAmount
=
1.5
;
// 1.5 SUI
const
rawAmount
=
(
humanReadableAmount
*
Math
.
pow
(
10
,
tokenInfo
.
fromToken
.
decimals
)
)
.
toString
(
)
;
console
.
log
(
"\nSwap Details:"
)
;
console
.
log
(
"--------------------"
)
;
console
.
log
(
From
:
$
{
tokenInfo
.
fromToken
.
symbol
}
)
;
console
.
log
(
To
:
$
{
tokenInfo
.
toToken
.
symbol
}
)
;
console
.
log
(
Amount
:
$
{
humanReadableAmount
}
$
{
tokenInfo
.
fromToken
.
symbol
}
)
;
console
.
log
(
Amount
in
base units
:
$
{
rawAmount
}
)
;
console
.
log
(
Approximate
USD
value
:
$$
{
(
humanReadableAmount
*
parseFloat
(
tokenInfo
.
fromToken
.
price
)
)
.
toFixed
(
2
)
}
)
;
// Execute the swap
console
.
log
(
"\nExecuting swap..."
)
;
const
swapResult
=
await
client
.
dex
.
executeSwap
(
{
chainId
:
'784'
,
// Sui chain ID
fromTokenAddress
,
toTokenAddress
,
amount
:
rawAmount
,
slippage
:
'0.5'
,
// 0.5% slippage
userWalletAddress
:
process
.
env
.
SUI_WALLET_ADDRESS
!
}
)
;
console
.
log
(
'Swap executed successfully:'
)
;
console
.
log
(
"\nTransaction ID:"
,
swapResult
.
transactionId
)
;
console
.
log
(
"Explorer URL:"
,
swapResult
.
explorerUrl
)
;
if
(
swapResult
.
details
)
{
console
.
log
(
"\nDetails:"
)
;
console
.
log
(
Input
:
$
{
swapResult
.
details
.
fromToken
.
amount
}
$
{
swapResult
.
details
.
fromToken
.
symbol
}
)
;
console
.
log
(
Output
:
$
{
swapResult
.
details
.
toToken
.
amount
}
$
{
swapResult
.
details
.
toToken
.
symbol
}
)
;
if
(
swapResult
.
details
.
priceImpact
)
{
console
.
log
(
Price
Impact
:
$
{
swapResult
.
details
.
priceImpact
}
%
)
;
}
}
return
swapResult
;
}
catch
(
error
)
{
if
(
error
instanceof
Error
)
{
console
.
error
(
'Error executing swap:'
,
error
.
message
)
;
// API errors include details in the message
if
(
error
.
message
.
includes
(
'API Error:'
)
)
{
const
match
=
error
.
message
.
match
(
/
API Error:
(
.
*
)
/
)
;
if
(
match
)
console
.
error
(
'API Error Details:'
,
match
[
1
]
)
;
}
}
throw
error
;
}
}
// Run if this file is executed directly
if
(
require
.
main
===
module
)
{
executeSwap
(
)
.
then
(
(
)
=>
process
.
exit
(
0
)
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
error
(
'Error:'
,
error
)
;
process
.
exit
(
1
)
;
}
)
;
}
export
{
executeSwap
}
;
获取报价
#
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
chainId
:
'784'
,
// Sui
fromTokenAddress
:
'0x2::sui::SUI'
,
// SUI
toTokenAddress
:
'0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC'
,
// USDC
amount
:
'100000000'
,
// In base units
slippage
:
'0.5'
// 0.5%
}
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="sui-示例">Sui 示例<a class="index_header-anchor__Xqb+L" href="#sui-示例" style="opacity:0">#</a></h1>
<h2 data-content="创建币种助手 (可忽略)" id="创建币种助手-(可忽略)">创建币种助手 (可忽略)<a class="index_header-anchor__Xqb+L" href="#创建币种助手-(可忽略)" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Common tokens on Sui mainnet</span>
<span class="token keyword module">export</span> <span class="token keyword">const</span> <span class="token constant">TOKENS</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token constant">SUI</span><span class="token operator">:</span> <span class="token string">"0x2::sui::SUI"</span><span class="token punctuation">,</span>
    <span class="token constant">USDC</span><span class="token operator">:</span> <span class="token string">"0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"</span>
<span class="token punctuation">}</span> <span class="token keyword module">as</span> <span class="token keyword">const</span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="创建兑换指令" id="创建兑换指令">创建兑换指令<a class="index_header-anchor__Xqb+L" href="#创建兑换指令" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// swap.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> client <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token punctuation">{</span> <span class="token constant">TOKENS</span> <span class="token punctuation">}</span> <span class="token keyword module">from</span> <span class="token string">'./Tokens'</span><span class="token punctuation">;</span> <span class="token comment">// Optional, if you created the token helper</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment">Example: Execute a swap from SUI to USDC</span>
<span class="token doc-comment comment">*/</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SUI_PRIVATE_KEY</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Missing SUI_PRIVATE_KEY in .env file'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// First, get token information using a quote</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> fromTokenAddress <span class="token operator">=</span> <span class="token constant">TOKENS</span><span class="token punctuation">.</span><span class="token constant">SUI</span><span class="token punctuation">;</span> <span class="token comment">// Or use directly: "0x2::sui::SUI"</span>
    <span class="token keyword">const</span> toTokenAddress <span class="token operator">=</span> <span class="token constant">TOKENS</span><span class="token punctuation">.</span><span class="token constant">USDC</span><span class="token punctuation">;</span> <span class="token comment">// Or use directly: "0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"</span>

    <span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'784'</span><span class="token punctuation">,</span> <span class="token comment">// Sui chain ID</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token punctuation">,</span>
        <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span> <span class="token comment">// Small amount for quote</span>
        <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">fromToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">toToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quote<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token comment">// Convert amount to base units</span>
    <span class="token keyword">const</span> humanReadableAmount <span class="token operator">=</span> <span class="token number">1.5</span><span class="token punctuation">;</span> <span class="token comment">// 1.5 SUI</span>
    <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap Details:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"--------------------"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">From</span><span class="token operator">:</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">To</span><span class="token operator">:</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">Amount</span><span class="token operator">:</span> $<span class="token punctuation">{</span>humanReadableAmount<span class="token punctuation">}</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Amount</span> <span class="token keyword">in</span> base units<span class="token operator">:</span> $<span class="token punctuation">{</span>rawAmount<span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Approximate</span> <span class="token constant">USD</span> <span class="token literal-property property">value</span><span class="token operator">:</span> $$<span class="token punctuation">{</span><span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">price</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toFixed</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Execute the swap</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting swap..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> swapResult <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'784'</span><span class="token punctuation">,</span> <span class="token comment">// Sui chain ID</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      <span class="token literal-property property">amount</span><span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
      <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span><span class="token punctuation">,</span> <span class="token comment">// 0.5% slippage</span>
      <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SUI_WALLET_ADDRESS</span><span class="token operator">!</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'Swap executed successfully:'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nTransaction ID:"</span><span class="token punctuation">,</span> swapResult<span class="token punctuation">.</span><span class="token property-access">transactionId</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> swapResult<span class="token punctuation">.</span><span class="token property-access">explorerUrl</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nDetails:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">Input</span><span class="token operator">:</span> $<span class="token punctuation">{</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">amount</span><span class="token punctuation">}</span> $<span class="token punctuation">{</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">Output</span><span class="token operator">:</span> $<span class="token punctuation">{</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">amount</span><span class="token punctuation">}</span> $<span class="token punctuation">{</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">priceImpact</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Price</span> <span class="token maybe-class-name">Impact</span><span class="token operator">:</span> $<span class="token punctuation">{</span>swapResult<span class="token punctuation">.</span><span class="token property-access">details</span><span class="token punctuation">.</span><span class="token property-access">priceImpact</span><span class="token punctuation">}</span><span class="token operator">%</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>

    <span class="token keyword control-flow">return</span> swapResult<span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'Error executing swap:'</span><span class="token punctuation">,</span> error<span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token comment">// API errors include details in the message</span>
      <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">.</span><span class="token method function property-access">includes</span><span class="token punctuation">(</span><span class="token string">'API Error:'</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> match <span class="token operator">=</span> error<span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">.</span><span class="token method function property-access">match</span><span class="token punctuation">(</span><span class="token regex"><span class="token regex-delimiter">/</span><span class="token regex-source language-regex">API Error: <span class="token group punctuation">(</span><span class="token char-set class-name">.</span><span class="token quantifier number">*</span><span class="token group punctuation">)</span></span><span class="token regex-delimiter">/</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>match<span class="token punctuation">)</span> <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'API Error Details:'</span><span class="token punctuation">,</span> match<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
    <span class="token keyword control-flow">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Run if this file is executed directly</span>
<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>require<span class="token punctuation">.</span><span class="token property-access">main</span> <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">error</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'Error:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
      process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword module">export</span> <span class="token exports"><span class="token punctuation">{</span> executeSwap <span class="token punctuation">}</span></span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="获取报价" id="获取报价">获取报价<a class="index_header-anchor__Xqb+L" href="#获取报价" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'784'</span><span class="token punctuation">,</span>  <span class="token comment">// Sui</span>
    <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'0x2::sui::SUI'</span><span class="token punctuation">,</span> <span class="token comment">// SUI</span>
    <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
    <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'100000000'</span><span class="token punctuation">,</span>  <span class="token comment">// In base units</span>
    <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span>     <span class="token comment">// 0.5%</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "资源",
    "Sui 示例"
  ],
  "sidebar_links": [
    "介绍",
    "EVM 示例",
    "Solana 示例",
    "Sui 示例",
    "Javascript 签名 SDK",
    "Go 签名 SDK"
  ],
  "toc": [
    "创建币种助手 (可忽略)",
    "创建兑换指令",
    "获取报价"
  ]
}
```

</details>
