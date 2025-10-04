# 搭建跨链应用 | 搭建跨链应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-crosschain-quick-start#8.3-获取交易状态  
**抓取时间:** 2025-05-27 05:07:25  
**字数:** 1664

## 导航路径
DEX API > 交易 API > 搭建跨链应用 > 搭建跨链应用

## 目录
- 1. 设置你的环境
- 2. 检查授权额度
- 3. 检查授权交易参数并发起授权交易
- 4. 通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链
- 5. 通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种
- 6. 请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID
- 7. 请求跨链兑换接口，发起交易
- 8. 查询交易状态

---

搭建跨链应用
#
在本指南中，我们将通过欧易 DEX 提供的一个示例来展示如何进行跨链兑换，使用 Ethereum 链上的 USDT 兑换 Arbitrum 链上的 USDC。这个过程包括:
设置你的环境
检查授权额度
检查授权交易参数并发起授权交易
通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链
通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种
请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID
请求跨链兑换接口，发起交易
查询交易状态
1. 设置你的环境
#
const
{
Web3
}
=
require
(
'web3'
)
;
const
cryptoJS
=
require
(
'crypto-js'
)
;
// The URL for the Ethereum node you want to connect to
const
web3
=
new
Web3
(
'https://......com'
)
;
const
apiBaseUrl
=
'https://web3.okx.com/api/v5/dex/aggregator'
;
// --------------------- environment variable ---------------------
const
chainId
=
'1'
;
// USDT contract address on Ethereum
const
fromTokenAddress
=
'0xdac17f958d2ee523a2206206994597c13d831ec7'
;
// USDC on Arbitrum will be set later
const
toTokenAddress
=
'0xff970a61a04b1ca14834a43f5de4533ebddb5cc8'
;
// gasPrice or GasLimit ratio
const
ratio
=
BigInt
(
3
)
/
BigInt
(
2
)
;
// your wallet address
const
user
=
'0x6f9fxxxxxxxxxxxxxxxxxxxx61059dcfd9'
const
fromAmount
=
'1000000'
// user wallet private key
const
privateKey
=
'xxxxx'
;
// open api Secret key
const
secretkey
=
'xxxxx'
// Get the current time
const
date
=
new
Date
(
)
;
// --------------------- util function ---------------------
function
getAggregatorRequestUrl
(
methodName
,
queryParams
)
{
return
apiBaseUrl
+
methodName
+
'?'
+
(
new
URLSearchParams
(
queryParams
)
)
.
toString
(
)
;
}
// For cross-chain operations
function
getCrossChainBaseUrl
(
methodName
,
queryParams
)
{
const
baseUrl
=
'https://web3.okx.com/api/v5/dex/cross-chain'
;
return
{
apiRequestUrl
:
baseUrl
+
methodName
+
'?'
+
(
new
URLSearchParams
(
queryParams
)
)
.
toString
(
)
,
path
:
methodName
+
'?'
+
(
new
URLSearchParams
(
queryParams
)
)
.
toString
(
)
}
;
}
const
headersParams
=
{
'Content-Type'
:
'application/json'
,
// The api Key obtained from the previous application
'OK-ACCESS-KEY'
:
'xxxxx'
,
'OK-ACCESS-SIGN'
:
cryptoJS
.
enc
.
Base64
.
stringify
(
// The field order of headersParams should be consistent with the order of quoteParams.
// example : quote ==> cryptoJS.HmacSHA256(timestamp + 'GET' + '/api/v5/dex/aggregator/quote?amount=1000000&chainId=1&toTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&fromTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', secretKey)
cryptoJS
.
HmacSHA256
(
date
.
toISOString
(
)
+
'GET'
+
'/api/v5/dex/aggregator/quote?amount=1000000&chainId=1&toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7'
,
secretkey
)
)
,
// Convert the current time to the desired format
'OK-ACCESS-TIMESTAMP'
:
date
.
toISOString
(
)
,
// The password created when applying for the key
'OK-ACCESS-PASSPHRASE'
:
'xxxxxxx'
,
}
;
2. 检查授权额度
#
以 ETH chain 举例
#
Demo 为 JavaScript 语言
连接到以太坊节点
：您需要确保您已经连接到一个可用的以太坊节点。您可以使用 web3.js 或其他以太坊开发库来连接到节点。在代码中，您需要指定节点的 HTTP 或 WebSocket 端点。
获取代币合约实例
：使用代币的合约地址和 ABI，您需要创建一个代币合约的实例。您可以使用 web3.js 的 web3.eth.Contract 方法来实现这一点，将合约地址和 ABI 作为参数传递给合约实例。
查询授权额度
：通过调用合约实例的 allowance 函数来查询授权额度。该函数需要两个参数：拥有者的地址和被授权者的地址。您可以通过在调用时提供这两个地址来查询授权额度。
spenderAddress 地址可以参考
此处
接口 Response 中的 dexTokenApproveAddress。
const
{
Web3
}
=
require
(
'web3'
)
;
// Connect to an Ethereum node
const
web3
=
new
Web3
(
'https://xxxxx'
)
;
// token address and ABI
const
tokenAddress
=
'0xxxxxxxxx'
;
// user address
const
ownerAddress
=
'0xxxxxxxx'
;
// ETH dex token approval address
const
spenderAddress
=
'0x40aa958dd87fc8305b97f2ba922cddca374bcd7f'
;
const
tokenABI
=
[
{
"constant"
:
true
,
"inputs"
:
[
{
"name"
:
"_owner"
,
"type"
:
"address"
}
,
{
"name"
:
"_spender"
,
"type"
:
"address"
}
]
,
"name"
:
"allowance"
,
"outputs"
:
[
{
"name"
:
""
,
"type"
:
"uint256"
}
]
,
"payable"
:
false
,
"stateMutability"
:
"view"
,
"type"
:
"function"
}
]
;
// Create token contract instance
const
tokenContract
=
new
web3
.
eth
.
Contract
(
tokenABI
,
tokenAddress
)
;
// Query token approve allowance function
async
function
getAllowance
(
ownerAddress
,
spenderAddress
)
{
try
{
const
allowance
=
await
tokenContract
.
methods
.
allowance
(
ownerAddress
,
spenderAddress
)
.
call
(
)
;
console
.
log
(
`
Allowance for
${
ownerAddress
}
to
${
spenderAddress
}
:
${
allowance
}
`
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
'Failed to query allowance:'
,
error
)
;
}
}
getAllowance
(
ownerAddress
,
spenderAddress
)
.
then
(
r
=>
console
.
log
(
r
)
)
;
下文的 allowanceAmount 代表真实的链上授权额度
2.2 获取授权数量
#
提示
获取授权数量。如果 allowanceAmount < fromTokenAmount，请查看步骤 3，如果 allowanceAmount >= fromTokenAmount，你可以选择使用步骤 3 增加授权数量，或者直接进行步骤 4。
const
{
data
:
allowanceData
}
=
await
getAllowanceData
(
)
;
const
allowanceAmount
=
allowanceData
?.
[
0
]
?.
allowanceAmount
;
3. 检查授权交易参数并发起授权交易
#
提示
由于 allowanceAmount < fromTokenAmount，我们需要对该币种进行授权。
3.1 定义授权交易参数
#
接下来，定义你要执行授权交易的参数。
const
getApproveTransactionParams
=
{
chainId
:
fromChainId
,
tokenContractAddress
:
fromTokenAddress
,
userWalletAddress
,
approveAmount
:
fromTokenAmount
,
}
;
3.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
approveTransaction
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getAggregatorRequestUrl
(
'/approve-transaction'
,
getApproveTransactionParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
3.3 获取授权交易 tx 并且发送授权交易
#
if
(
parseFloat
(
allowanceAmount
)
<
parseFloat
(
fromTokenAmount
)
)
{
const
{
data
}
=
await
approveTransaction
(
allowanceAmount
)
;
let
allowanceParams
=
{
...
{
data
:
data
[
0
]
.
data
}
,
// You can modify the data content you want according to the web3 official website
}
;
const
{
rawTransaction
}
=
await
web3
.
eth
.
accounts
.
signTransaction
(
allowanceParams
,
privateKey
)
;
await
web3
.
eth
.
sendSignedTransaction
(
rawTransaction
)
;
}
4. 通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链
#
4.1 定义获取支持的目标链参数
#
接下来，定义参数，并通过 fromChainId 拿到对应的 toChainId 列表。
const
toChainListParams
=
{
chainId
:
fromChainId
,
}
;
4.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
getSupportedChain
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getCrossChainBaseUrl
(
'/supported/chain'
,
toChainListParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
4.3 获取支持的目标链列表并选择 Arbitrum 链，你也可以根据列表选择其他链作为目标链
#
const
{
data
:
supportedChainList
}
=
await
getSupportedChain
(
)
;
const
selectChainItem
=
supportedChainList
.
find
(
(
item
)
=>
{
return
item
.
chainName
===
'Arbitrum'
;
}
)
;
toChainId
=
selectChainItem
?.
chainId
;
5. 通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种
#
5.1 定义获取可交易币种参数
#
接下来，定义参数，并通过 toChainId 拿到可交易的币种列表。
const
toChainTokenListParams
=
{
chainId
:
toChainId
,
}
;
5.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
getToChainTokenList
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getAggregatorRequestUrl
(
'/all-tokens'
'
,
toChainTokenListParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
5.3 获取币种列表并选择 USDC 币种，你也可以根据列表选择其他币种作为目标链币种
#
const
{
data
:
toChainTokenList
}
=
await
getToChainTokenList
(
)
;
const
selectToChainToken
=
toChainTokenList
.
find
(
(
item
)
=>
{
return
item
.
tokenSymbol
===
'USDC'
;
}
)
;
toTokenAddress
=
selectToChainToken
?.
tokenContractAddress
;
6. 请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID
#
6.1 定义询价参数
#
接下来，定义参数，用来拿到询价的基础信息和路径列表信息。
const
quoteParams
=
{
fromChainId
,
toChainId
,
fromTokenAddress
,
toTokenAddress
,
amount
:
fromTokenAmount
,
slippage
,
}
;
6.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
getQuote
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getCrossChainBaseUrl
(
'/quote'
,
quoteParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
6.3 获取询价信息，并选择一条路径作为交易路径
#
const
{
data
:
quoteData
}
=
await
getQuote
(
)
;
bridgeId
=
quoteData
[
0
]
?.
routerList
[
0
]
?.
router
?.
bridgeId
;
7. 请求跨链兑换接口，发起交易
#
7.1 定义跨链兑换参数
#
接下来，定义参数，并获取跨链兑换的 tx 信息。
const
swapParams
=
{
fromChainId
:
fromChainId
,
toChainId
:
toChainId
,
fromTokenAddress
,
toTokenAddress
,
amount
:
fromTokenAmount
,
slippage
,
userWalletAddress
,
bridgeId
,
}
;
7.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
getSwapData
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getCrossChainBaseUrl
(
'/build-tx'
,
swapParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
7.3 请求跨链兑换接口拿到 tx 信息，发起上链交易
#
const
{
data
:
swapData
}
=
await
getSwapData
(
)
;
const
swapDataTxInfo
=
swapData
[
0
]
.
tx
;
const
nonce
=
await
web3
.
eth
.
getTransactionCount
(
userWalletAddress
,
'latest'
)
;
// You can obtain the latest nonce and process the hexadecimal numbers starting with 0x according to your needs
let
signTransactionParams
=
{
data
:
swapDataTxInfo
.
data
,
gasPrice
:
swapDataTxInfo
.
gasPrice
,
to
:
swapDataTxInfo
.
to
,
value
:
swapDataTxInfo
.
value
,
nonce
,
}
;
const
{
rawTransaction
}
=
await
web3
.
eth
.
accounts
.
signTransaction
(
signTransactionParams
,
privateKey
)
;
const
chainTxInfo
=
await
web3
.
eth
.
sendSignedTransaction
(
rawTransaction
)
;
transactionTx
=
chainTxInfo
;
8. 查询交易状态
#
8.1 定义查询参数
#
接下来，定义参数，主要为源链 Hash 地址信息。
const
getCheckStatusParams
=
{
hash
:
transactionTx
,
}
;
8.2 定义辅助函数
#
定义一个辅助函数，用于与 DEX API 进行交互。
const
checkTransactionStatus
=
async
(
)
=>
{
const
{
apiRequestUrl
,
path
}
=
getCrossChainBaseUrl
(
'/status'
,
getCheckStatusParams
)
;
return
fetch
(
apiRequestUrl
,
{
method
:
'get'
,
headers
:
headersParams
,
}
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
json
(
)
)
.
then
(
(
res
)
=>
{
return
res
;
}
)
;
}
;
8.3 获取交易状态
#
提示
你也可以增加轮询的方式获取实时订单状态，这里为单次查询的例子。
const
{
data
:
statusInfo
}
=
await
checkTransactionStatus
(
)
;
console
.
log
(
statusInfo
?.
data
[
0
]
?.
detailStatus
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="搭建跨链应用">搭建跨链应用<a class="index_header-anchor__Xqb+L" href="#搭建跨链应用" style="opacity:0">#</a></h1>
<p>在本指南中，我们将通过欧易 DEX 提供的一个示例来展示如何进行跨链兑换，使用 Ethereum 链上的 USDT 兑换 Arbitrum 链上的 USDC。这个过程包括:</p>
<ul>
<li>设置你的环境</li>
<li>检查授权额度</li>
<li>检查授权交易参数并发起授权交易</li>
<li>通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链</li>
<li>通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种</li>
<li>请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID</li>
<li>请求跨链兑换接口，发起交易</li>
<li>查询交易状态</li>
</ul>
<h2 data-content="1. 设置你的环境" id="1.-设置你的环境">1. 设置你的环境<a class="index_header-anchor__Xqb+L" href="#1.-设置你的环境" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token maybe-class-name">Web3</span> <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'web3'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> cryptoJS <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'crypto-js'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// The URL for the Ethereum node you want to connect to</span>
<span class="token keyword">const</span> web3 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Web3</span><span class="token punctuation">(</span><span class="token string">'https://......com'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> apiBaseUrl <span class="token operator">=</span> <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator'</span><span class="token punctuation">;</span>
<span class="token comment">// --------------------- environment variable ---------------------</span>
<span class="token keyword">const</span> chainId <span class="token operator">=</span> <span class="token string">'1'</span><span class="token punctuation">;</span>
<span class="token comment">// USDT contract address on Ethereum</span>
<span class="token keyword">const</span> fromTokenAddress <span class="token operator">=</span> <span class="token string">'0xdac17f958d2ee523a2206206994597c13d831ec7'</span><span class="token punctuation">;</span>
<span class="token comment">// USDC on Arbitrum will be set later</span>
<span class="token keyword">const</span> toTokenAddress <span class="token operator">=</span> <span class="token string">'0xff970a61a04b1ca14834a43f5de4533ebddb5cc8'</span><span class="token punctuation">;</span>
<span class="token comment">// gasPrice or GasLimit ratio</span>
<span class="token keyword">const</span> ratio <span class="token operator">=</span> <span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token number">3</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// your wallet address</span>
<span class="token keyword">const</span> user <span class="token operator">=</span> <span class="token string">'0x6f9fxxxxxxxxxxxxxxxxxxxx61059dcfd9'</span>
<span class="token keyword">const</span> fromAmount <span class="token operator">=</span> <span class="token string">'1000000'</span>
<span class="token comment">// user wallet private key</span>
<span class="token keyword">const</span> privateKey <span class="token operator">=</span> <span class="token string">'xxxxx'</span><span class="token punctuation">;</span>
<span class="token comment">// open api Secret key</span>
<span class="token keyword">const</span> secretkey <span class="token operator">=</span> <span class="token string">'xxxxx'</span>
<span class="token comment">// Get the current time</span>
<span class="token keyword">const</span> date <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// --------------------- util function ---------------------</span>
<span class="token keyword">function</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span><span class="token parameter">methodName<span class="token punctuation">,</span> queryParams</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">return</span> apiBaseUrl <span class="token operator">+</span> methodName <span class="token operator">+</span> <span class="token string">'?'</span> <span class="token operator">+</span> <span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>queryParams<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// For cross-chain operations</span>
<span class="token keyword">function</span> <span class="token function">getCrossChainBaseUrl</span><span class="token punctuation">(</span><span class="token parameter">methodName<span class="token punctuation">,</span> queryParams</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> baseUrl <span class="token operator">=</span> <span class="token string">'https://web3.okx.com/api/v5/dex/cross-chain'</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">apiRequestUrl</span><span class="token operator">:</span> baseUrl <span class="token operator">+</span> methodName <span class="token operator">+</span> <span class="token string">'?'</span> <span class="token operator">+</span> <span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>queryParams<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token literal-property property">path</span><span class="token operator">:</span> methodName <span class="token operator">+</span> <span class="token string">'?'</span> <span class="token operator">+</span> <span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>queryParams<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> headersParams <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">'Content-Type'</span><span class="token operator">:</span> <span class="token string">'application/json'</span><span class="token punctuation">,</span>
    <span class="token comment">// The api Key obtained from the previous application</span>
    <span class="token string-property property">'OK-ACCESS-KEY'</span><span class="token operator">:</span> <span class="token string">'xxxxx'</span><span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-SIGN'</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>
    <span class="token comment">// The field order of headersParams should be consistent with the order of quoteParams.</span>
    <span class="token comment">// example : quote ==&gt; cryptoJS.HmacSHA256(timestamp + 'GET' + '/api/v5/dex/aggregator/quote?amount=1000000&amp;chainId=1&amp;toTokenAddress=0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE&amp;fromTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', secretKey)</span>
        cryptoJS<span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>date<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token string">'GET'</span> <span class="token operator">+</span> <span class="token string">'/api/v5/dex/aggregator/quote?amount=1000000&amp;chainId=1&amp;toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&amp;fromTokenAddress=0xdac17f958d2ee523a2206206994597c13d831ec7'</span><span class="token punctuation">,</span> secretkey<span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token comment">// Convert the current time to the desired format</span>
    <span class="token string-property property">'OK-ACCESS-TIMESTAMP'</span><span class="token operator">:</span> date<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token comment">// The password created when applying for the key</span>
    <span class="token string-property property">'OK-ACCESS-PASSPHRASE'</span><span class="token operator">:</span> <span class="token string">'xxxxxxx'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="2. 检查授权额度" id="2.-检查授权额度">2. 检查授权额度<a class="index_header-anchor__Xqb+L" href="#2.-检查授权额度" style="opacity:0">#</a></h2>
<h3 id="以-eth-chain-举例">以 ETH chain 举例<a class="index_header-anchor__Xqb+L" href="#以-eth-chain-举例" style="opacity:0">#</a></h3>
<ul>
<li><code>Demo 为 JavaScript 语言</code></li>
</ul>
<ol>
<li><code>连接到以太坊节点</code>：您需要确保您已经连接到一个可用的以太坊节点。您可以使用 web3.js 或其他以太坊开发库来连接到节点。在代码中，您需要指定节点的 HTTP 或 WebSocket 端点。</li>
<li><code>获取代币合约实例</code>：使用代币的合约地址和 ABI，您需要创建一个代币合约的实例。您可以使用 web3.js 的 web3.eth.Contract 方法来实现这一点，将合约地址和 ABI 作为参数传递给合约实例。</li>
<li><code>查询授权额度</code>：通过调用合约实例的 allowance 函数来查询授权额度。该函数需要两个参数：拥有者的地址和被授权者的地址。您可以通过在调用时提供这两个地址来查询授权额度。</li>
<li>spenderAddress 地址可以参考 <a href="/zh-hans/build/dev-docs/dex-api/dex-get-supported-chains">此处</a> 接口 Response 中的 dexTokenApproveAddress。</li>
</ol>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token maybe-class-name">Web3</span> <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'web3'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Connect to an Ethereum node</span>
<span class="token keyword">const</span> web3 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Web3</span><span class="token punctuation">(</span><span class="token string">'https://xxxxx'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// token address and  ABI</span>
<span class="token keyword">const</span> tokenAddress <span class="token operator">=</span> <span class="token string">'0xxxxxxxxx'</span><span class="token punctuation">;</span>
<span class="token comment">// user address</span>
<span class="token keyword">const</span> ownerAddress <span class="token operator">=</span> <span class="token string">'0xxxxxxxx'</span><span class="token punctuation">;</span>
<span class="token comment">// ETH dex token approval address</span>
<span class="token keyword">const</span> spenderAddress <span class="token operator">=</span> <span class="token string">'0x40aa958dd87fc8305b97f2ba922cddca374bcd7f'</span><span class="token punctuation">;</span>


<span class="token keyword">const</span> tokenABI <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
        <span class="token string-property property">"constant"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
        <span class="token string-property property">"inputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_owner"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_spender"</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"allowance"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"outputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"uint256"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string-property property">"payable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token string-property property">"stateMutability"</span><span class="token operator">:</span> <span class="token string">"view"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"function"</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">]</span><span class="token punctuation">;</span>


<span class="token comment">// Create token contract instance</span>
<span class="token keyword">const</span> tokenContract <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span>Contract</span><span class="token punctuation">(</span>tokenABI<span class="token punctuation">,</span> tokenAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Query token approve allowance function</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getAllowance</span><span class="token punctuation">(</span><span class="token parameter">ownerAddress<span class="token punctuation">,</span> spenderAddress</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> allowance <span class="token operator">=</span> <span class="token keyword control-flow">await</span> tokenContract<span class="token punctuation">.</span><span class="token property-access">methods</span><span class="token punctuation">.</span><span class="token method function property-access">allowance</span><span class="token punctuation">(</span>ownerAddress<span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">call</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Allowance for </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>ownerAddress<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> to </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>spenderAddress<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>allowance<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">'Failed to query allowance:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token function">getAllowance</span><span class="token punctuation">(</span>ownerAddress<span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token parameter">r</span> <span class="token arrow operator">=&gt;</span> <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>r<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>下文的 allowanceAmount 代表真实的链上授权额度</li>
</ul>
<h3 id="2.2-获取授权数量">2.2 获取授权数量<a class="index_header-anchor__Xqb+L" href="#2.2-获取授权数量" style="opacity:0">#</a></h3>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rpbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rpbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">获取授权数量。如果 allowanceAmount &lt; fromTokenAmount，请查看步骤 3，如果 allowanceAmount &gt;= fromTokenAmount，你可以选择使用步骤 3 增加授权数量，或者直接进行步骤 4。</div></div></div></div></div>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> allowanceData <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getAllowanceData</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> allowanceAmount <span class="token operator">=</span> allowanceData<span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token operator">?.</span>allowanceAmount<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="3. 检查授权交易参数并发起授权交易" id="3.-检查授权交易参数并发起授权交易">3. 检查授权交易参数并发起授权交易<a class="index_header-anchor__Xqb+L" href="#3.-检查授权交易参数并发起授权交易" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rvbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rvbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">由于 allowanceAmount &lt; fromTokenAmount，我们需要对该币种进行授权。</div></div></div></div></div>
<h3 id="3.1-定义授权交易参数">3.1 定义授权交易参数<a class="index_header-anchor__Xqb+L" href="#3.1-定义授权交易参数" style="opacity:0">#</a></h3>
<p>接下来，定义你要执行授权交易的参数。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> getApproveTransactionParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">chainId</span><span class="token operator">:</span> fromChainId<span class="token punctuation">,</span>
  <span class="token literal-property property">tokenContractAddress</span><span class="token operator">:</span> fromTokenAddress<span class="token punctuation">,</span>
  userWalletAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">approveAmount</span><span class="token operator">:</span> fromTokenAmount<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="3.2-定义辅助函数">3.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#3.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">approveTransaction</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span>
    <span class="token string">'/approve-transaction'</span><span class="token punctuation">,</span>
    getApproveTransactionParams
  <span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="3.3-获取授权交易-tx-并且发送授权交易">3.3 获取授权交易 tx 并且发送授权交易<a class="index_header-anchor__Xqb+L" href="#3.3-获取授权交易-tx-并且发送授权交易" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token function">parseFloat</span><span class="token punctuation">(</span>allowanceAmount<span class="token punctuation">)</span> <span class="token operator">&lt;</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>fromTokenAmount<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> data <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">approveTransaction</span><span class="token punctuation">(</span>allowanceAmount<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">let</span> allowanceParams <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token spread operator">...</span><span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">data</span> <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token comment">// You can modify the data content you want according to the web3 official website</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> rawTransaction <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> web3<span class="token punctuation">.</span><span class="token property-access">eth</span><span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span>
    allowanceParams<span class="token punctuation">,</span>
    privateKey
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">await</span> web3<span class="token punctuation">.</span><span class="token property-access">eth</span><span class="token punctuation">.</span><span class="token method function property-access">sendSignedTransaction</span><span class="token punctuation">(</span>rawTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="4. 通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链" id="4.-通过-fromchainid-拿到可以交易的-tochainid-列表，并选择其中一条链作为目标链">4. 通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链<a class="index_header-anchor__Xqb+L" href="#4.-通过-fromchainid-拿到可以交易的-tochainid-列表，并选择其中一条链作为目标链" style="opacity:0">#</a></h2>
<h3 id="4.1-定义获取支持的目标链参数">4.1 定义获取支持的目标链参数<a class="index_header-anchor__Xqb+L" href="#4.1-定义获取支持的目标链参数" style="opacity:0">#</a></h3>
<p>接下来，定义参数，并通过 fromChainId 拿到对应的 toChainId 列表。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> toChainListParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">chainId</span><span class="token operator">:</span> fromChainId<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="4.2-定义辅助函数">4.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#4.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getSupportedChain</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getCrossChainBaseUrl</span><span class="token punctuation">(</span>
    <span class="token string">'/supported/chain'</span><span class="token punctuation">,</span>
    toChainListParams
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="4.3-获取支持的目标链列表并选择-arbitrum-链，你也可以根据列表选择其他链作为目标链">4.3 获取支持的目标链列表并选择 Arbitrum 链，你也可以根据列表选择其他链作为目标链<a class="index_header-anchor__Xqb+L" href="#4.3-获取支持的目标链列表并选择-arbitrum-链，你也可以根据列表选择其他链作为目标链" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> supportedChainList <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getSupportedChain</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> selectChainItem <span class="token operator">=</span> supportedChainList<span class="token punctuation">.</span><span class="token method function property-access">find</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">item</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">return</span> item<span class="token punctuation">.</span><span class="token property-access">chainName</span> <span class="token operator">===</span> <span class="token string">'Arbitrum'</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
toChainId <span class="token operator">=</span> selectChainItem<span class="token operator">?.</span>chainId<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="5. 通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种" id="5.-通过-tochainid-拿到该链的币种列表，并且选择其中一个代币作为目标链币种">5. 通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种<a class="index_header-anchor__Xqb+L" href="#5.-通过-tochainid-拿到该链的币种列表，并且选择其中一个代币作为目标链币种" style="opacity:0">#</a></h2>
<h3 id="5.1-定义获取可交易币种参数">5.1 定义获取可交易币种参数<a class="index_header-anchor__Xqb+L" href="#5.1-定义获取可交易币种参数" style="opacity:0">#</a></h3>
<p>接下来，定义参数，并通过 toChainId 拿到可交易的币种列表。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> toChainTokenListParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">chainId</span><span class="token operator">:</span> toChainId<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="5.2-定义辅助函数">5.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#5.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getToChainTokenList</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getAggregatorRequestUrl</span><span class="token punctuation">(</span>
    <span class="token string">'/all-tokens'</span>'<span class="token punctuation">,</span>
    toChainTokenListParams
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="5.3-获取币种列表并选择-usdc-币种，你也可以根据列表选择其他币种作为目标链币种">5.3 获取币种列表并选择 USDC 币种，你也可以根据列表选择其他币种作为目标链币种<a class="index_header-anchor__Xqb+L" href="#5.3-获取币种列表并选择-usdc-币种，你也可以根据列表选择其他币种作为目标链币种" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> toChainTokenList <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getToChainTokenList</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> selectToChainToken <span class="token operator">=</span> toChainTokenList<span class="token punctuation">.</span><span class="token method function property-access">find</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">item</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword control-flow">return</span> item<span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span> <span class="token operator">===</span> <span class="token string">'USDC'</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
toTokenAddress <span class="token operator">=</span> selectToChainToken<span class="token operator">?.</span>tokenContractAddress<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="6. 请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID" id="6.-请求询价接口，拿到询价数据，主要目的是为了获取跨链桥-id">6. 请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID<a class="index_header-anchor__Xqb+L" href="#6.-请求询价接口，拿到询价数据，主要目的是为了获取跨链桥-id" style="opacity:0">#</a></h2>
<h3 id="6.1-定义询价参数">6.1 定义询价参数<a class="index_header-anchor__Xqb+L" href="#6.1-定义询价参数" style="opacity:0">#</a></h3>
<p>接下来，定义参数，用来拿到询价的基础信息和路径列表信息。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> quoteParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  fromChainId<span class="token punctuation">,</span>
  toChainId<span class="token punctuation">,</span>
  fromTokenAddress<span class="token punctuation">,</span>
  toTokenAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">amount</span><span class="token operator">:</span> fromTokenAmount<span class="token punctuation">,</span>
  slippage<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="6.2-定义辅助函数">6.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#6.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getQuote</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getCrossChainBaseUrl</span><span class="token punctuation">(</span><span class="token string">'/quote'</span><span class="token punctuation">,</span> quoteParams<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="6.3-获取询价信息，并选择一条路径作为交易路径">6.3 获取询价信息，并选择一条路径作为交易路径<a class="index_header-anchor__Xqb+L" href="#6.3-获取询价信息，并选择一条路径作为交易路径" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> quoteData <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
bridgeId <span class="token operator">=</span> quoteData<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token operator">?.</span>routerList<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token operator">?.</span>router<span class="token operator">?.</span>bridgeId<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="7. 请求跨链兑换接口，发起交易" id="7.-请求跨链兑换接口，发起交易">7. 请求跨链兑换接口，发起交易<a class="index_header-anchor__Xqb+L" href="#7.-请求跨链兑换接口，发起交易" style="opacity:0">#</a></h2>
<h3 id="7.1-定义跨链兑换参数">7.1 定义跨链兑换参数<a class="index_header-anchor__Xqb+L" href="#7.1-定义跨链兑换参数" style="opacity:0">#</a></h3>
<p>接下来，定义参数，并获取跨链兑换的 tx 信息。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> swapParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">fromChainId</span><span class="token operator">:</span> fromChainId<span class="token punctuation">,</span>
  <span class="token literal-property property">toChainId</span><span class="token operator">:</span> toChainId<span class="token punctuation">,</span>
  fromTokenAddress<span class="token punctuation">,</span>
  toTokenAddress<span class="token punctuation">,</span>
  <span class="token literal-property property">amount</span><span class="token operator">:</span> fromTokenAmount<span class="token punctuation">,</span>
  slippage<span class="token punctuation">,</span>
  userWalletAddress<span class="token punctuation">,</span>
  bridgeId<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="7.2-定义辅助函数">7.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#7.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">getSwapData</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getCrossChainBaseUrl</span><span class="token punctuation">(</span><span class="token string">'/build-tx'</span><span class="token punctuation">,</span> swapParams<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="7.3-请求跨链兑换接口拿到-tx-信息，发起上链交易">7.3 请求跨链兑换接口拿到 tx 信息，发起上链交易<a class="index_header-anchor__Xqb+L" href="#7.3-请求跨链兑换接口拿到-tx-信息，发起上链交易" style="opacity:0">#</a></h3>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> swapData <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getSwapData</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> swapDataTxInfo <span class="token operator">=</span> swapData<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token property-access">tx</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token keyword control-flow">await</span> web3<span class="token punctuation">.</span><span class="token property-access">eth</span><span class="token punctuation">.</span><span class="token method function property-access">getTransactionCount</span><span class="token punctuation">(</span>userWalletAddress<span class="token punctuation">,</span> <span class="token string">'latest'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// You can obtain the latest nonce and process the hexadecimal numbers starting with 0x according to your needs</span>
<span class="token keyword">let</span> signTransactionParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">data</span><span class="token operator">:</span> swapDataTxInfo<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">,</span>
  <span class="token literal-property property">gasPrice</span><span class="token operator">:</span> swapDataTxInfo<span class="token punctuation">.</span><span class="token property-access">gasPrice</span><span class="token punctuation">,</span>
  <span class="token literal-property property">to</span><span class="token operator">:</span> swapDataTxInfo<span class="token punctuation">.</span><span class="token property-access">to</span><span class="token punctuation">,</span>
  <span class="token literal-property property">value</span><span class="token operator">:</span> swapDataTxInfo<span class="token punctuation">.</span><span class="token property-access">value</span><span class="token punctuation">,</span>
  nonce<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> rawTransaction <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> web3<span class="token punctuation">.</span><span class="token property-access">eth</span><span class="token punctuation">.</span><span class="token property-access">accounts</span><span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span>
  signTransactionParams<span class="token punctuation">,</span>
  privateKey
<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> chainTxInfo <span class="token operator">=</span> <span class="token keyword control-flow">await</span> web3<span class="token punctuation">.</span><span class="token property-access">eth</span><span class="token punctuation">.</span><span class="token method function property-access">sendSignedTransaction</span><span class="token punctuation">(</span>rawTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
transactionTx <span class="token operator">=</span> chainTxInfo<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="8. 查询交易状态" id="8.-查询交易状态">8. 查询交易状态<a class="index_header-anchor__Xqb+L" href="#8.-查询交易状态" style="opacity:0">#</a></h2>
<h3 id="8.1-定义查询参数">8.1 定义查询参数<a class="index_header-anchor__Xqb+L" href="#8.1-定义查询参数" style="opacity:0">#</a></h3>
<p>接下来，定义参数，主要为源链 Hash 地址信息。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> getCheckStatusParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token literal-property property">hash</span><span class="token operator">:</span> transactionTx<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="8.2-定义辅助函数">8.2 定义辅助函数<a class="index_header-anchor__Xqb+L" href="#8.2-定义辅助函数" style="opacity:0">#</a></h3>
<p>定义一个辅助函数，用于与 DEX API 进行交互。</p>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token function-variable function">checkTransactionStatus</span> <span class="token operator">=</span> <span class="token keyword">async</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> apiRequestUrl<span class="token punctuation">,</span> path <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">getCrossChainBaseUrl</span><span class="token punctuation">(</span>
    <span class="token string">'/status'</span><span class="token punctuation">,</span>
    getCheckStatusParams
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token function">fetch</span><span class="token punctuation">(</span>apiRequestUrl<span class="token punctuation">,</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'get'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headersParams<span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token method function property-access">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token keyword control-flow">return</span> res<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="8.3-获取交易状态">8.3 获取交易状态<a class="index_header-anchor__Xqb+L" href="#8.3-获取交易状态" style="opacity:0">#</a></h3>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R49bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R49bf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">你也可以增加轮询的方式获取实时订单状态，这里为单次查询的例子。</div></div></div></div></div>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword">const</span> <span class="token punctuation">{</span> <span class="token literal-property property">data</span><span class="token operator">:</span> statusInfo <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">checkTransactionStatus</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>statusInfo<span class="token operator">?.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token operator">?.</span>detailStatus<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "搭建跨链应用",
    "搭建跨链应用"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
    "搭建跨链应用",
    "在 Solana 链上发送多签交易",
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
    "1. 设置你的环境",
    "2. 检查授权额度",
    "3. 检查授权交易参数并发起授权交易",
    "4. 通过 fromChainId 拿到可以交易的 toChainId 列表，并选择其中一条链作为目标链",
    "5. 通过 toChainId 拿到该链的币种列表，并且选择其中一个代币作为目标链币种",
    "6. 请求询价接口，拿到询价数据，主要目的是为了获取跨链桥 ID",
    "7. 请求跨链兑换接口，发起交易",
    "8. 查询交易状态"
  ]
}
```

</details>
