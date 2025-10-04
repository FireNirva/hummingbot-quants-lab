# Solana 示例 | DEX SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-sdk-solana#创建并签署交易  
**抓取时间:** 2025-05-27 03:58:26  
**字数:** 1644

## 导航路径
DEX API > 资源 > Solana 示例

## 目录
- 创建兑换指令
- 获取报价
- 执行兑换指令

---

Solana 示例
#
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
* Example: Execute a swap from SOL to USDC
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
SOLANA_PRIVATE_KEY
)
{
throw
new
Error
(
'Missing SOLANA_PRIVATE_KEY in .env file'
)
;
}
// Get quote to fetch token information
console
.
log
(
"Getting token information..."
)
;
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
'501'
,
fromTokenAddress
:
'11111111111111111111111111111111'
,
// SOL
toTokenAddress
:
'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
,
// USDC
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
// Convert amount to base units (for display purposes)
const
humanReadableAmount
=
0.1
;
// 0.1 SOL
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
`
From:
${
tokenInfo
.
fromToken
.
symbol
}
`
)
;
console
.
log
(
`
To:
${
tokenInfo
.
toToken
.
symbol
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
humanReadableAmount
}
${
tokenInfo
.
fromToken
.
symbol
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
console
.
log
(
`
Approximate USD value: $
${
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
`
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
'501'
,
// Solana chain ID
fromTokenAddress
:
'11111111111111111111111111111111'
,
// SOL
toTokenAddress
:
'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
,
// USDC
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
SOLANA_WALLET_ADDRESS
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
'501'
,
// Solana
fromTokenAddress
:
'11111111111111111111111111111111'
,
// SOL
toTokenAddress
:
'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'
,
// USDC
amount
:
'100000000'
,
// 0.1 SOL (in lamports)
slippage
:
'0.5'
// 0.5%
}
)
;
执行兑换指令
#
导入以下代码库
// Required Solana dependencies for DEX interaction
import
{
Connection
,
// Handles RPC connections to Solana network
Keypair
,
// Manages wallet keypairs for signing
PublicKey
,
// Handles Solana public key conversion and validation
TransactionInstruction
,
// Core transaction instruction type
TransactionMessage
,
// Builds transaction messages (v0 format)
VersionedTransaction
,
// Supports newer transaction format with lookup tables
RpcResponseAndContext
,
// RPC response wrapper type
SimulatedTransactionResponse
,
// Simulation result type
AddressLookupTableAccount
,
// For transaction size optimization
PublicKeyInitData
// Public key input type
}
from
"@solana/web3.js"
;
import
base58
from
"bs58"
;
// Required for private key decoding
连线和钱包初始化
// Note: Consider using a reliable RPC endpoint with high rate limits for production
const
connection
=
new
Connection
(
process
.
env
.
SOLANA_RPC_URL
||
"https://api.mainnet-beta.solana.com"
)
;
// Initialize wallet for signing
// This wallet will be the fee payer and transaction signer
const
wallet
=
Keypair
.
fromSecretKey
(
Uint8Array
.
from
(
base58
.
decode
(
userPrivateKey
)
)
)
;
设置兑换参数
#
// Configure swap parameters
const
baseUrl
=
"https://web3.okx.com/api/v5/dex/aggregator/swap-instruction"
;
const
params
=
{
chainId
:
"501"
,
// Solana mainnet chain ID
feePercent
:
"1"
,
// Platform fee percentage
amount
:
"1000000"
,
// Amount in smallest denomination (lamports for SOL)
fromTokenAddress
:
"11111111111111111111111111111111"
,
// SOL mint address
toTokenAddress
:
"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
,
// USDC mint address
slippage
:
"0.1"
,
// Slippage tolerance in percentage
userWalletAddress
:
userAddress
,
// Wallet performing the swap
priceTolerance
:
"0"
,
// Maximum allowed price impact
autoSlippage
:
"false"
,
// Use fixed slippage instead of auto
pathNum
:
"3"
// Maximum routes to consider
}
;
兑换指令
#
// Helper function to convert DEX API instructions to Solana format
function
createTransactionInstruction
(
instruction
)
{
return
new
TransactionInstruction
(
{
programId
:
new
PublicKey
(
instruction
.
programId
)
,
// DEX program ID
keys
:
instruction
.
accounts
.
map
(
(
key
)
=>
(
{
pubkey
:
new
PublicKey
(
key
.
pubkey
)
,
// Account address
isSigner
:
key
.
isSigner
,
// True if account must sign tx
isWritable
:
key
.
isWritable
// True if instruction modifies account
}
)
)
,
data
:
Buffer
.
from
(
instruction
.
data
,
'base64'
)
// Instruction parameters
}
)
;
}
// Fetch optimal swap route and instructions from DEX
const
timestamp
=
new
Date
(
)
.
toISOString
(
)
;
const
requestPath
=
"/api/v5/dex/aggregator/swap-instruction"
;
const
queryString
=
"?"
+
new
URLSearchParams
(
params
)
.
toString
(
)
;
const
headers
=
getHeaders
(
timestamp
,
"GET"
,
requestPath
,
queryString
)
;
const
response
=
await
fetch
(
`
https://web3.okx.com
${
requestPath
}
${
queryString
}
`
,
{
method
:
'GET'
,
headers
}
)
;
const
{
data
}
=
await
response
.
json
(
)
;
const
{
instructionLists
,
addressLookupTableAccount
}
=
data
;
// Process DEX instructions into Solana-compatible format
const
instructions
=
[
]
;
// Remove duplicate lookup table addresses returned by DEX
const
uniqueLookupTables
=
Array
.
from
(
new
Set
(
addressLookupTableAccount
)
)
;
console
.
log
(
"Lookup tables to load:"
,
uniqueLookupTables
)
;
// Convert each DEX instruction to Solana format
if
(
instructionLists
?.
length
)
{
instructions
.
push
(
...
instructionLists
.
map
(
createTransactionInstruction
)
)
;
}
地址查找表
#
// Process lookup tables for transaction optimization
// Lookup tables are crucial for complex swaps that interact with many accounts
// They significantly reduce transaction size and cost
const
addressLookupTableAccounts
=
[
]
;
if
(
uniqueLookupTables
?.
length
>
0
)
{
console
.
log
(
"Loading address lookup tables..."
)
;
// Fetch all lookup tables in parallel for better performance
const
lookupTableAccounts
=
await
Promise
.
all
(
uniqueLookupTables
.
map
(
async
(
address
)
=>
{
const
pubkey
=
new
PublicKey
(
address
)
;
// Get lookup table account data from Solana
const
account
=
await
connection
.
getAddressLookupTable
(
pubkey
)
.
then
(
(
res
)
=>
res
.
value
)
;
if
(
!
account
)
{
throw
new
Error
(
`
Could not fetch lookup table account
${
address
}
`
)
;
}
return
account
;
}
)
)
;
addressLookupTableAccounts
.
push
(
...
lookupTableAccounts
)
;
}
创建并签署交易
#
// Get recent blockhash for transaction timing and uniqueness
const
latestBlockhash
=
await
connection
.
getLatestBlockhash
(
'finalized'
)
;
// Create versioned transaction message (V0 format required for lookup table support)
const
messageV0
=
new
TransactionMessage
(
{
payerKey
:
wallet
.
publicKey
,
// Fee payer address
recentBlockhash
:
latestBlockhash
.
blockhash
,
// Transaction timing
instructions
// Swap instructions from DEX
}
)
.
compileToV0Message
(
addressLookupTableAccounts
)
;
// Include lookup tables
// Create new versioned transaction with optimizations
const
transaction
=
new
VersionedTransaction
(
messageV0
)
;
// Simulate transaction to check for errors
// This helps catch issues before paying fees
const
result
=
await
connection
.
simulateTransaction
(
transaction
)
;
// Sign transaction with fee payer wallet
transaction
.
sign
(
[
wallet
]
)
;
执行交易
#
// Send transaction to Solana
// skipPreflight=false ensures additional validation
// maxRetries helps handle network issues
const
txId
=
await
connection
.
sendRawTransaction
(
transaction
.
serialize
(
)
,
{
skipPreflight
:
false
,
// Run preflight validation
maxRetries
:
5
// Retry on failure
}
)
;
// Log transaction results
console
.
log
(
"Transaction ID:"
,
txId
)
;
console
.
log
(
"Explorer URL:"
,
`
https://solscan.io/tx/
${
txId
}
`
)
;
// Wait for confirmation
await
connection
.
confirmTransaction
(
{
signature
:
txId
,
blockhash
:
latestBlockhash
.
blockhash
,
lastValidBlockHeight
:
latestBlockhash
.
lastValidBlockHeight
}
)
;
console
.
log
(
"Transaction confirmed!"
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="solana-示例">Solana 示例<a class="index_header-anchor__Xqb+L" href="#solana-示例" style="opacity:0">#</a></h1>
<h2 data-content="创建兑换指令" id="创建兑换指令">创建兑换指令<a class="index_header-anchor__Xqb+L" href="#创建兑换指令" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// swap.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> client <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Execute a swap from SOL to USDC</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_PRIVATE_KEY</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Missing SOLANA_PRIVATE_KEY in .env file'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// Get quote to fetch token information</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
        <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
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
    <span class="token comment">// Convert amount to base units (for display purposes)</span>
    <span class="token keyword">const</span> humanReadableAmount <span class="token operator">=</span> <span class="token number">0.1</span><span class="token punctuation">;</span> <span class="token comment">// 0.1 SOL</span>
    <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap Details:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"--------------------"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">From: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">To: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>humanReadableAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount in base units: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>rawAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Approximate USD value: $</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">price</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toFixed</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Execute the swap</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting swap..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> swapResult <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span> <span class="token comment">// Solana chain ID</span>
      <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
      <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
      <span class="token literal-property property">amount</span><span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
      <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span><span class="token punctuation">,</span> <span class="token comment">// 0.5% slippage</span>
      <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_WALLET_ADDRESS</span><span class="token operator">!</span>
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
    <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span>  <span class="token comment">// Solana</span>
    <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
    <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
    <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">'100000000'</span><span class="token punctuation">,</span>  <span class="token comment">// 0.1 SOL (in lamports)</span>
    <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">'0.5'</span>     <span class="token comment">// 0.5%</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="执行兑换指令" id="执行兑换指令">执行兑换指令<a class="index_header-anchor__Xqb+L" href="#执行兑换指令" style="opacity:0">#</a></h2>
<p>导入以下代码库</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Required Solana dependencies for DEX interaction</span>
<span class="token keyword module">import</span> <span class="token punctuation">{</span>
    <span class="token maybe-class-name">Connection</span><span class="token punctuation">,</span>          <span class="token comment">// Handles RPC connections to Solana network</span>
    <span class="token maybe-class-name">Keypair</span><span class="token punctuation">,</span>             <span class="token comment">// Manages wallet keypairs for signing</span>
    <span class="token maybe-class-name">PublicKey</span><span class="token punctuation">,</span>           <span class="token comment">// Handles Solana public key conversion and validation</span>
    <span class="token maybe-class-name">TransactionInstruction</span><span class="token punctuation">,</span>    <span class="token comment">// Core transaction instruction type</span>
    <span class="token maybe-class-name">TransactionMessage</span><span class="token punctuation">,</span>        <span class="token comment">// Builds transaction messages (v0 format)</span>
    <span class="token maybe-class-name">VersionedTransaction</span><span class="token punctuation">,</span>      <span class="token comment">// Supports newer transaction format with lookup tables</span>
    <span class="token maybe-class-name">RpcResponseAndContext</span><span class="token punctuation">,</span>     <span class="token comment">// RPC response wrapper type</span>
    <span class="token maybe-class-name">SimulatedTransactionResponse</span><span class="token punctuation">,</span>  <span class="token comment">// Simulation result type</span>
    <span class="token maybe-class-name">AddressLookupTableAccount</span><span class="token punctuation">,</span>     <span class="token comment">// For transaction size optimization</span>
    <span class="token maybe-class-name">PublicKeyInitData</span>              <span class="token comment">// Public key input type</span>
<span class="token punctuation">}</span> <span class="token keyword module">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports">base58</span> <span class="token keyword module">from</span> <span class="token string">"bs58"</span><span class="token punctuation">;</span>    <span class="token comment">// Required for private key decoding</span>
</code></pre></div>
<p>连线和钱包初始化</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Note: Consider using a reliable RPC endpoint with high rate limits for production</span>
<span class="token keyword">const</span> connection <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Connection</span><span class="token punctuation">(</span>
   process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span> <span class="token operator">||</span> <span class="token string">"https://api.mainnet-beta.solana.com"</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Initialize wallet for signing</span>
<span class="token comment">// This wallet will be the fee payer and transaction signer</span>
<span class="token keyword">const</span> wallet <span class="token operator">=</span> <span class="token maybe-class-name">Keypair</span><span class="token punctuation">.</span><span class="token method function property-access">fromSecretKey</span><span class="token punctuation">(</span>
   <span class="token known-class-name class-name">Uint8Array</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>base58<span class="token punctuation">.</span><span class="token method function property-access">decode</span><span class="token punctuation">(</span>userPrivateKey<span class="token punctuation">)</span><span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="设置兑换参数" id="设置兑换参数">设置兑换参数<a class="index_header-anchor__Xqb+L" href="#设置兑换参数" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Configure swap parameters</span>
<span class="token keyword">const</span> baseUrl <span class="token operator">=</span> <span class="token string">"https://web3.okx.com/api/v5/dex/aggregator/swap-instruction"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>              <span class="token comment">// Solana mainnet chain ID</span>
    <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>             <span class="token comment">// Platform fee percentage</span>
    <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">"1000000"</span><span class="token punctuation">,</span>           <span class="token comment">// Amount in smallest denomination (lamports for SOL)</span>
    <span class="token literal-property property">fromTokenAddress</span><span class="token operator">:</span> <span class="token string">"11111111111111111111111111111111"</span><span class="token punctuation">,</span>  <span class="token comment">// SOL mint address</span>
    <span class="token literal-property property">toTokenAddress</span><span class="token operator">:</span> <span class="token string">"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"</span><span class="token punctuation">,</span>  <span class="token comment">// USDC mint address</span>
    <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">"0.1"</span><span class="token punctuation">,</span>             <span class="token comment">// Slippage tolerance in percentage</span>
    <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> userAddress<span class="token punctuation">,</span>   <span class="token comment">// Wallet performing the swap</span>
    <span class="token literal-property property">priceTolerance</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>         <span class="token comment">// Maximum allowed price impact</span>
    <span class="token literal-property property">autoSlippage</span><span class="token operator">:</span> <span class="token string">"false"</span><span class="token punctuation">,</span>       <span class="token comment">// Use fixed slippage instead of auto</span>
    <span class="token literal-property property">pathNum</span><span class="token operator">:</span> <span class="token string">"3"</span>                 <span class="token comment">// Maximum routes to consider</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="兑换指令" id="兑换指令">兑换指令<a class="index_header-anchor__Xqb+L" href="#兑换指令" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Helper function to convert DEX API instructions to Solana format</span>
<span class="token keyword">function</span> <span class="token function">createTransactionInstruction</span><span class="token punctuation">(</span><span class="token parameter">instruction</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">return</span> <span class="token keyword">new</span> <span class="token class-name">TransactionInstruction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">programId</span><span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>instruction<span class="token punctuation">.</span><span class="token property-access">programId</span><span class="token punctuation">)</span><span class="token punctuation">,</span>  <span class="token comment">// DEX program ID</span>
        <span class="token literal-property property">keys</span><span class="token operator">:</span> instruction<span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">.</span><span class="token method function property-access">map</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">key</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>
            <span class="token literal-property property">pubkey</span><span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>key<span class="token punctuation">.</span><span class="token property-access">pubkey</span><span class="token punctuation">)</span><span class="token punctuation">,</span>    <span class="token comment">// Account address</span>
            <span class="token literal-property property">isSigner</span><span class="token operator">:</span> key<span class="token punctuation">.</span><span class="token property-access">isSigner</span><span class="token punctuation">,</span>     <span class="token comment">// True if account must sign tx</span>
            <span class="token literal-property property">isWritable</span><span class="token operator">:</span> key<span class="token punctuation">.</span><span class="token property-access">isWritable</span>  <span class="token comment">// True if instruction modifies account</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token literal-property property">data</span><span class="token operator">:</span> <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>instruction<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">,</span> <span class="token string">'base64'</span><span class="token punctuation">)</span>  <span class="token comment">// Instruction parameters</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// Fetch optimal swap route and instructions from DEX</span>
<span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token string">"/api/v5/dex/aggregator/swap-instruction"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">fetch</span><span class="token punctuation">(</span>
    <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>queryString<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> headers <span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> data <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> instructionLists<span class="token punctuation">,</span> addressLookupTableAccount <span class="token punctuation">}</span> <span class="token operator">=</span> data<span class="token punctuation">;</span>
<span class="token comment">// Process DEX instructions into Solana-compatible format</span>
<span class="token keyword">const</span> instructions <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token comment">// Remove duplicate lookup table addresses returned by DEX</span>
<span class="token keyword">const</span> uniqueLookupTables <span class="token operator">=</span> <span class="token known-class-name class-name">Array</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">Set</span><span class="token punctuation">(</span>addressLookupTableAccount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Lookup tables to load:"</span><span class="token punctuation">,</span> uniqueLookupTables<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Convert each DEX instruction to Solana format</span>
<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>instructionLists<span class="token operator">?.</span>length<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    instructions<span class="token punctuation">.</span><span class="token method function property-access">push</span><span class="token punctuation">(</span><span class="token spread operator">...</span>instructionLists<span class="token punctuation">.</span><span class="token method function property-access">map</span><span class="token punctuation">(</span>createTransactionInstruction<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="地址查找表" id="地址查找表">地址查找表<a class="index_header-anchor__Xqb+L" href="#地址查找表" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Process lookup tables for transaction optimization</span>
<span class="token comment">// Lookup tables are crucial for complex swaps that interact with many accounts</span>
<span class="token comment">// They significantly reduce transaction size and cost</span>
<span class="token keyword">const</span> addressLookupTableAccounts <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>uniqueLookupTables<span class="token operator">?.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Loading address lookup tables..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Fetch all lookup tables in parallel for better performance</span>
    <span class="token keyword">const</span> lookupTableAccounts <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token known-class-name class-name">Promise</span><span class="token punctuation">.</span><span class="token method function property-access">all</span><span class="token punctuation">(</span>
        uniqueLookupTables<span class="token punctuation">.</span><span class="token method function property-access">map</span><span class="token punctuation">(</span><span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token parameter">address</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> pubkey <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>address<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token comment">// Get lookup table account data from Solana</span>
            <span class="token keyword">const</span> account <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection
                <span class="token punctuation">.</span><span class="token method function property-access">getAddressLookupTable</span><span class="token punctuation">(</span>pubkey<span class="token punctuation">)</span>
                <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token property-access">value</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>account<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Could not fetch lookup table account </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>address<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
            <span class="token keyword control-flow">return</span> account<span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    addressLookupTableAccounts<span class="token punctuation">.</span><span class="token method function property-access">push</span><span class="token punctuation">(</span><span class="token spread operator">...</span>lookupTableAccounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="创建并签署交易" id="创建并签署交易">创建并签署交易<a class="index_header-anchor__Xqb+L" href="#创建并签署交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Get recent blockhash for transaction timing and uniqueness</span>
<span class="token keyword">const</span> latestBlockhash <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">getLatestBlockhash</span><span class="token punctuation">(</span><span class="token string">'finalized'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Create versioned transaction message (V0 format required for lookup table support)</span>
<span class="token keyword">const</span> messageV0 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TransactionMessage</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">payerKey</span><span class="token operator">:</span> wallet<span class="token punctuation">.</span><span class="token property-access">publicKey</span><span class="token punctuation">,</span>     <span class="token comment">// Fee payer address</span>
    <span class="token literal-property property">recentBlockhash</span><span class="token operator">:</span> latestBlockhash<span class="token punctuation">.</span><span class="token property-access">blockhash</span><span class="token punctuation">,</span>  <span class="token comment">// Transaction timing</span>
    instructions                     <span class="token comment">// Swap instructions from DEX</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">compileToV0Message</span><span class="token punctuation">(</span>addressLookupTableAccounts<span class="token punctuation">)</span><span class="token punctuation">;</span>  <span class="token comment">// Include lookup tables</span>
<span class="token comment">// Create new versioned transaction with optimizations</span>
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">VersionedTransaction</span><span class="token punctuation">(</span>messageV0<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Simulate transaction to check for errors</span>
<span class="token comment">// This helps catch issues before paying fees</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">simulateTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Sign transaction with fee payer wallet</span>
transaction<span class="token punctuation">.</span><span class="token method function property-access">sign</span><span class="token punctuation">(</span><span class="token punctuation">[</span>wallet<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="执行交易" id="执行交易">执行交易<a class="index_header-anchor__Xqb+L" href="#执行交易" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Send transaction to Solana</span>
<span class="token comment">// skipPreflight=false ensures additional validation</span>
<span class="token comment">// maxRetries helps handle network issues</span>
<span class="token keyword">const</span> txId <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">sendRawTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">.</span><span class="token method function property-access">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">skipPreflight</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>  <span class="token comment">// Run preflight validation</span>
    <span class="token literal-property property">maxRetries</span><span class="token operator">:</span> <span class="token number">5</span>         <span class="token comment">// Retry on failure</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Log transaction results</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Transaction ID:"</span><span class="token punctuation">,</span> txId<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Wait for confirmation</span>
<span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">confirmTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">signature</span><span class="token operator">:</span> txId<span class="token punctuation">,</span>
    <span class="token literal-property property">blockhash</span><span class="token operator">:</span> latestBlockhash<span class="token punctuation">.</span><span class="token property-access">blockhash</span><span class="token punctuation">,</span>
    <span class="token literal-property property">lastValidBlockHeight</span><span class="token operator">:</span> latestBlockhash<span class="token punctuation">.</span><span class="token property-access">lastValidBlockHeight</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Transaction confirmed!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "Solana 示例"
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
    "创建兑换指令",
    "获取报价",
    "执行兑换指令"
  ]
}
```

</details>
