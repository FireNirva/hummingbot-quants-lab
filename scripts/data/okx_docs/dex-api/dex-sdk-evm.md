# EVM 示例 | DEX SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-sdk-evm#执行授权指令  
**抓取时间:** 2025-05-27 01:44:18  
**字数:** 1081

## 导航路径
DEX API > 资源 > EVM 示例

## 目录
- 执行授权指令
- 创建兑换指令
- 获取报价

---

EVM 示例
#
执行授权指令
#
// approval.ts
import
{
client
}
from
'./DexClient'
;
// Helper function to convert human-readable amounts to base units
export
function
toBaseUnits
(
amount
:
string
,
decimals
:
number
)
:
string
{
// Remove any decimal point and count the decimal places
const
[
integerPart
,
decimalPart
=
''
]
=
amount
.
split
(
'.'
)
;
const
currentDecimals
=
decimalPart
.
length
;
// Combine integer and decimal parts, removing the decimal point
let
result
=
integerPart
+
decimalPart
;
// Add zeros if we need more decimal places
if
(
currentDecimals
<
decimals
)
{
result
=
result
+
'0'
.
repeat
(
decimals
-
currentDecimals
)
;
}
// Remove digits if we have too many decimal places
else
if
(
currentDecimals
>
decimals
)
{
result
=
result
.
slice
(
0
,
result
.
length
-
(
currentDecimals
-
decimals
)
)
;
}
// Remove leading zeros
result
=
result
.
replace
(
/
^
0
+
/
,
''
)
||
'0'
;
return
result
;
}
/**
* Example: Approve a token for swapping
*/
async
function
executeApproval
(
tokenAddress
:
string
,
amount
:
string
)
{
try
{
// Get token information using quote
console
.
log
(
"Getting token information..."
)
;
const
tokenInfo
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
'8453'
,
// Base Chain
fromTokenAddress
:
tokenAddress
,
toTokenAddress
:
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
,
// Native token
amount
:
'1000000'
,
// Use a reasonable amount for quote
slippage
:
'0.5'
}
)
;
const
tokenDecimals
=
parseInt
(
tokenInfo
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
;
const
rawAmount
=
toBaseUnits
(
amount
,
tokenDecimals
)
;
console
.
log
(
`
\nApproval Details:
`
)
;
console
.
log
(
`
--------------------
`
)
;
console
.
log
(
`
Token:
${
tokenInfo
.
data
[
0
]
.
fromToken
.
tokenSymbol
}
`
)
;
console
.
log
(
`
Amount:
${
amount
}
${
tokenInfo
.
data
[
0
]
.
fromToken
.
tokenSymbol
}
`
)
;
console
.
log
(
`
Amount in base units:
${
rawAmount
}
`
)
;
// Execute the approval
console
.
log
(
"\nExecuting approval..."
)
;
const
result
=
await
client
.
dex
.
executeApproval
(
{
chainId
:
'8453'
,
// Base Chain
tokenContractAddress
:
tokenAddress
,
approveAmount
:
rawAmount
}
)
;
if
(
'alreadyApproved'
in
result
)
{
console
.
log
(
"\nToken already approved for the requested amount!"
)
;
return
{
success
:
true
,
alreadyApproved
:
true
}
;
}
else
{
console
.
log
(
"\nApproval completed successfully!"
)
;
console
.
log
(
"Transaction Hash:"
,
result
.
transactionHash
)
;
console
.
log
(
"Explorer URL:"
,
result
.
explorerUrl
)
;
return
result
;
}
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
'Error executing approval:'
,
error
.
message
)
;
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
// Example usage: ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000
const
args
=
process
.
argv
.
slice
(
2
)
;
if
(
args
.
length
!==
2
)
{
console
.
log
(
"Usage: ts-node approval.ts <tokenAddress> <amountToApprove>"
)
;
console
.
log
(
"\nExamples:"
)
;
console
.
log
(
" # Approve 1000 USDC"
)
;
console
.
log
(
`
ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000
`
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
const
[
tokenAddress
,
amount
]
=
args
;
executeApproval
(
tokenAddress
,
amount
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
executeApproval
}
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
/**
* Example: Execute a swap from ETH to USDC on Base chain
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
EVM_PRIVATE_KEY
)
{
throw
new
Error
(
'Missing EVM_PRIVATE_KEY in .env file'
)
;
}
// You can change this to any EVM chain
// For example, for Base, use chainId: '8453'
// For example, for baseSepolia, use chainId: '84532'
// You can also use SUI, use chainId: '784'
// When using another Chain, you need to change the fromTokenAddress and toTokenAddress to the correct addresses for that chain
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
'8453'
,
// Base chain ID
fromTokenAddress
:
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
,
// Native ETH
toTokenAddress
:
'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
,
// USDC on Base
amount
:
String
(
10
*
10
**
14
)
,
// .0001 ETH
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
EVM_WALLET_ADDRESS
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
JSON
.
stringify
(
swapResult
,
null
,
2
)
)
;
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
'8453'
,
// Base Chain
fromTokenAddress
:
'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
,
// USDC
toTokenAddress
:
'0x4200000000000000000000000000000000000006'
,
// WETH
amount
:
'1000000'
,
// 1 USDC (in smallest units)
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
<div class="routes_md__xWlGF"><!--$--><h1 id="evm-示例">EVM 示例<a class="index_header-anchor__Xqb+L" href="#evm-示例" style="opacity:0">#</a></h1>
<h2 data-content="执行授权指令" id="执行授权指令">执行授权指令<a class="index_header-anchor__Xqb+L" href="#执行授权指令" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// approval.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> client <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token comment">// Helper function to convert human-readable amounts to base units</span>
<span class="token keyword module">export</span> <span class="token keyword">function</span> <span class="token function">toBaseUnits</span><span class="token punctuation">(</span><span class="token parameter"><span class="token literal-property property">amount</span><span class="token operator">:</span> string<span class="token punctuation">,</span> <span class="token literal-property property">decimals</span><span class="token operator">:</span> number</span><span class="token punctuation">)</span><span class="token operator">:</span> string <span class="token punctuation">{</span>
    <span class="token comment">// Remove any decimal point and count the decimal places</span>
    <span class="token keyword">const</span> <span class="token punctuation">[</span>integerPart<span class="token punctuation">,</span> decimalPart <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">]</span> <span class="token operator">=</span> amount<span class="token punctuation">.</span><span class="token method function property-access">split</span><span class="token punctuation">(</span><span class="token string">'.'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> currentDecimals <span class="token operator">=</span> decimalPart<span class="token punctuation">.</span><span class="token property-access">length</span><span class="token punctuation">;</span>

    <span class="token comment">// Combine integer and decimal parts, removing the decimal point</span>
    <span class="token keyword">let</span> result <span class="token operator">=</span> integerPart <span class="token operator">+</span> decimalPart<span class="token punctuation">;</span>

    <span class="token comment">// Add zeros if we need more decimal places</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">&lt;</span> decimals<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        result <span class="token operator">=</span> result <span class="token operator">+</span> <span class="token string">'0'</span><span class="token punctuation">.</span><span class="token method function property-access">repeat</span><span class="token punctuation">(</span>decimals <span class="token operator">-</span> currentDecimals<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// Remove digits if we have too many decimal places</span>
    <span class="token keyword control-flow">else</span> <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">&gt;</span> decimals<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        result <span class="token operator">=</span> result<span class="token punctuation">.</span><span class="token method function property-access">slice</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span><span class="token property-access">length</span> <span class="token operator">-</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">-</span> decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token comment">// Remove leading zeros</span>
    result <span class="token operator">=</span> result<span class="token punctuation">.</span><span class="token method function property-access">replace</span><span class="token punctuation">(</span><span class="token regex"><span class="token regex-delimiter">/</span><span class="token regex-source language-regex"><span class="token anchor function">^</span>0<span class="token quantifier number">+</span></span><span class="token regex-delimiter">/</span></span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span> <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">;</span>

    <span class="token keyword control-flow">return</span> result<span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Approve a token for swapping</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeApproval</span><span class="token punctuation">(</span><span class="token parameter"><span class="token literal-property property">tokenAddress</span><span class="token operator">:</span> string<span class="token punctuation">,</span> <span class="token literal-property property">amount</span><span class="token operator">:</span> string</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// Get token information using quote</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
            <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
            <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// Native token</span>
            <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span> <span class="token comment">// Use a reasonable amount for quote</span>
            <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenDecimals <span class="token operator">=</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token function">toBaseUnits</span><span class="token punctuation">(</span>amount<span class="token punctuation">,</span> tokenDecimals<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">\nApproval Details:</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">--------------------</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Token: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount in base units: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>rawAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token comment">// Execute the approval</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting approval..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">executeApproval</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
            <span class="token literal-property property">tokenContractAddress</span><span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
            <span class="token literal-property property">approveAmount</span><span class="token operator">:</span> rawAmount
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token string">'alreadyApproved'</span> <span class="token keyword">in</span> result<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nToken already approved for the requested amount!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span> <span class="token literal-property property">success</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span> <span class="token literal-property property">alreadyApproved</span><span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword control-flow">else</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nApproval completed successfully!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Transaction Hash:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span><span class="token property-access">transactionHash</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span><span class="token property-access">explorerUrl</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword control-flow">return</span> result<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'Error executing approval:'</span><span class="token punctuation">,</span> error<span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword control-flow">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Run if this file is executed directly</span>
<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>require<span class="token punctuation">.</span><span class="token property-access">main</span> <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Example usage: ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000</span>
    <span class="token keyword">const</span> args <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">argv</span><span class="token punctuation">.</span><span class="token method function property-access">slice</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>args<span class="token punctuation">.</span><span class="token property-access">length</span> <span class="token operator">!==</span> <span class="token number">2</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Usage: ts-node approval.ts &lt;tokenAddress&gt; &lt;amountToApprove&gt;"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nExamples:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"  # Approve 1000 USDC"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">  ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> <span class="token punctuation">[</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">]</span> <span class="token operator">=</span> args<span class="token punctuation">;</span>
    <span class="token function">executeApproval</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span>
        <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        <span class="token punctuation">.</span><span class="token keyword control-flow">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">error</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'Error:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
            process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword module">export</span> <span class="token exports"><span class="token punctuation">{</span> executeApproval <span class="token punctuation">}</span></span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="创建兑换指令" id="创建兑换指令">创建兑换指令<a class="index_header-anchor__Xqb+L" href="#创建兑换指令" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// swap.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> client <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Execute a swap from ETH to USDC on Base chain</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">EVM_PRIVATE_KEY</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Missing EVM_PRIVATE_KEY in .env file'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// You can change this to any EVM chain</span>
    <span class="token comment">// For example, for Base, use chainId: '8453'</span>
    <span class="token comment">// For example, for baseSepolia, use chainId: '84532'</span>
    <span class="token comment">// You can also use SUI, use chainId: '784'</span>
    <span class="token comment">// When using another Chain, you need to change the fromTokenAddress and toTokenAddress to the correct addresses for that chain</span>

    <span class="token keyword">const</span> swapResult <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span> <span class="token comment">// Base chain ID</span>
      <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// Native ETH</span>
      <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'</span><span class="token punctuation">,</span> <span class="token comment">// USDC on Base</span>
      <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token known-class-name class-name">String</span><span class="token punctuation">(</span><span class="token number">10</span> <span class="token operator">*</span> <span class="token number">10</span> <span class="token operator">**</span> <span class="token number">14</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token comment">// .0001 ETH</span>
      <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span><span class="token punctuation">,</span> <span class="token comment">// 0.5% slippage</span>
      <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">EVM_WALLET_ADDRESS</span><span class="token operator">!</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">'Swap executed successfully:'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token known-class-name class-name">JSON</span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>swapResult<span class="token punctuation">,</span> <span class="token keyword null nil">null</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

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
    <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
    <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
    <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'0x4200000000000000000000000000000000000006'</span><span class="token punctuation">,</span> <span class="token comment">// WETH</span>
    <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span>  <span class="token comment">// 1 USDC (in smallest units)</span>
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
    "EVM 示例"
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
    "执行授权指令",
    "创建兑换指令",
    "获取报价"
  ]
}
```

</details>
