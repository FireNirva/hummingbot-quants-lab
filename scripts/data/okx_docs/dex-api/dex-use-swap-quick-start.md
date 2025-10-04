# 在 EVM 链上搭建兑换应用 | 搭建兑换应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-swap-quick-start#3.检查授权交易参数并发起授权  
**抓取时间:** 2025-05-27 01:26:35  
**字数:** 8574

## 导航路径
DEX API > 交易 API > 搭建兑换应用 > 在 EVM 链上搭建兑换应用

## 目录
- 方法1：API方法
- 1.设置环境
- 2.检查授权额度
- 3.检查授权交易参数并发起授权
- 4.请求询价接口，拿到询价数据
- 5.请求兑换接口，发起交易
- 6. 广播交易
- 7. 追踪交易
- 8. 完整实现
- 方法2：SDK方法
- 1.安装SDK
- 2.设置环境
- 3.初始化客户端
- 4.调用SDK执行代币授权
- 5.调用SDK执行兑换
- 6.附加的SDK功能

---

在 EVM 链上搭建兑换应用
#
在EVM网络上使用OKX DEX构建兑换应用程序有两种方法：
API 方法-直接调用 OKX DEX API
SDK 方法-使用
@okx-dex/okx-dex-sdk
简化开发人员体验
本指南涵盖了这两种方法，以帮助您选择最适合您需求的方法。
方法1：API方法
#
在这种方法中，我们将直接使用OKX DEX API演示代币兑换。我们将在以太坊网络上将USDC兑换为ETH。
1.设置环境
#
// --------------------- npm package ---------------------
import
{
Web3
}
from
'web3'
;
import
axios
from
'axios'
;
import
*
as
dotenv
from
'dotenv'
;
import
CryptoJS
from
'crypto-js'
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
// --------------------- environment variable ---------------------
// Load hidden environment variables
dotenv
.
config
(
)
;
// Your wallet information - REPLACE WITH YOUR OWN VALUES
const
WALLET_ADDRESS
:
string
=
process
.
env
.
EVM_WALLET_ADDRESS
||
'0xYourWalletAddress'
;
const
PRIVATE_KEY
:
string
=
process
.
env
.
EVM_PRIVATE_KEY
||
'YourPrivateKey'
;
// Token addresses for swap on Ethereum Mainnet
const
ETH_ADDRESS
:
string
=
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
;
// Native ETH
const
USDC_ADDRESS
:
string
=
'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
;
// USDC
// Chain ID for Ethereum Mainnet
const
chainId
:
string
=
'1'
;
// API URL
const
baseUrl
:
string
=
'https://web3.okx.com/api/v5/'
;
// Amount to swap in smallest unit (approx $1 of ETH)
// 1 ETH = 10^18 wei, so 0.0005 ETH
const
SWAP_AMOUNT
:
string
=
'500000000000000'
;
// 0.0005 ETH (approx $1)
const
SLIPPAGE
:
string
=
'0.5'
;
// 0.5% slippage tolerance
// --------------------- util function ---------------------
export
function
getHeaders
(
timestamp
:
string
,
method
:
string
,
requestPath
:
string
,
queryString
=
""
)
{
// Check https://web3.okx.com/zh-hans/web3/build/docs/waas/rest-authentication for api-key
const
apiKey
=
process
.
env
.
OKX_API_KEY
;
const
secretKey
=
process
.
env
.
OKX_SECRET_KEY
;
const
apiPassphrase
=
process
.
env
.
OKX_API_PASSPHRASE
;
const
projectId
=
process
.
env
.
OKX_PROJECT_ID
;
if
(
!
apiKey
||
!
secretKey
||
!
apiPassphrase
||
!
projectId
)
{
throw
new
Error
(
"Missing required environment variables"
)
;
}
const
stringToSign
=
timestamp
+
method
+
requestPath
+
queryString
;
return
{
"Content-Type"
:
"application/json"
,
"OK-ACCESS-KEY"
:
apiKey
,
"OK-ACCESS-SIGN"
:
CryptoJS
.
enc
.
Base64
.
stringify
(
CryptoJS
.
HmacSHA256
(
stringToSign
,
secretKey
)
)
,
"OK-ACCESS-TIMESTAMP"
:
timestamp
,
"OK-ACCESS-PASSPHRASE"
:
apiPassphrase
,
"OK-ACCESS-PROJECT"
:
projectId
,
}
;
}
;
2.检查授权额度
#
您需要检查代币是否已批准DEX进行支出。此步骤仅适用于ERC20代币，而不是像ETH这样的本地代币。
/**
 * Check token allowance for DEX
 *
@param
tokenAddress
- Token contract address
 *
@param
ownerAddress
- Your wallet address
 *
@param
spenderAddress
- DEX spender address
 *
@returns
Allowance amount
 */
async
function
checkAllowance
(
tokenAddress
:
string
,
ownerAddress
:
string
,
spenderAddress
:
string
)
:
Promise
<
bigint
>
{
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
return
BigInt
(
String
(
allowance
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
'Failed to query allowance:'
,
error
)
;
throw
error
;
}
}
3.检查授权交易参数并发起授权
#
由于 allowanceAmount 小于 fromTokenAmount，你需要对该币种进行授权。
3.1 定义授权交易参数
const
getApproveTransactionParams
=
{
chainId
:
chainId
,
tokenContractAddress
:
tokenAddress
,
approveAmount
:
amount
}
;
3.2 定义辅助函数
async
function
getApproveTransaction
(
tokenAddress
:
string
,
amount
:
string
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/approve-transaction'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
tokenContractAddress
:
tokenAddress
,
approveAmount
:
amount
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get approval transaction data:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
3.3 计算 gasLimit
/**
 * Get transaction gas limit from Onchain gateway API
 *
@param
fromAddress
- Sender address
 *
@param
toAddress
- Target contract address
 *
@param
txAmount
- Transaction amount (0 for approvals)
 *
@param
inputData
- Transaction calldata
 *
@returns
Estimated gas limit
 */
async
function
getGasLimit
(
fromAddress
:
string
,
toAddress
:
string
,
txAmount
:
string
=
'0'
,
inputData
:
string
=
''
)
:
Promise
<
string
>
{
try
{
const
path
=
'dex/pre-transaction/gas-limit'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
body
=
{
chainIndex
:
chainId
,
fromAddress
:
fromAddress
,
toAddress
:
toAddress
,
txAmount
:
txAmount
,
extJson
:
{
inputData
:
inputData
}
}
;
// Prepare authentication with body included in signature
const
bodyString
=
JSON
.
stringify
(
body
)
;
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
`
/api/v5/
${
path
}
`
;
const
headers
=
getHeaders
(
timestamp
,
'POST'
,
requestPath
,
bodyString
)
;
const
response
=
await
axios
.
post
(
url
,
body
,
{
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
.
gasLimit
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get gas limit:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
3.4 获取授权交易 tx 并且发送授权请求
/**
 * Sign and send approve transaction
 *
@param
tokenAddress
- Token to approve
 *
@param
amount
- Amount to approve
 *
@returns
Order ID of the approval transaction
 */
async
function
approveToken
(
tokenAddress
:
string
,
amount
:
string
)
:
Promise
<
string
|
null
>
{
const
spenderAddress
=
'0x3b3ae790Df4F312e745D270119c6052904FB6790'
;
// Ethereum Mainnet DEX spender
// See Router addresses at: https://web3.okx.com/build/docs/waas/dex-smart-contract
const
currentAllowance
=
await
checkAllowance
(
tokenAddress
,
WALLET_ADDRESS
,
spenderAddress
)
;
if
(
currentAllowance
>=
BigInt
(
amount
)
)
{
console
.
log
(
'Sufficient allowance already exists'
)
;
return
null
;
}
console
.
log
(
'Insufficient allowance, approving tokens...'
)
;
// Get approve transaction data from OKX DEX API
const
approveData
=
await
getApproveTransaction
(
tokenAddress
,
amount
)
;
// Get accurate gas limit using Onchain gateway API
const
gasLimit
=
await
getGasLimit
(
WALLET_ADDRESS
,
tokenAddress
,
'0'
,
approveData
.
data
)
;
// Get current gas price (can also use Onchain gateway API)
const
gasPrice
=
await
web3
.
eth
.
getGasPrice
(
)
;
const
adjustedGasPrice
=
BigInt
(
gasPrice
)
*
BigInt
(
15
)
/
BigInt
(
10
)
;
// 1.5x for faster confirmation
// Get current nonce
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
WALLET_ADDRESS
,
'latest'
)
;
// Create transaction object
const
txObject
=
{
from
:
WALLET_ADDRESS
,
to
:
tokenAddress
,
data
:
approveData
.
data
,
value
:
'0'
,
gas
:
gasLimit
,
gasPrice
:
adjustedGasPrice
.
toString
(
)
,
nonce
:
nonce
}
;
// Sign transaction
const
{
signedTx
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
txObject
,
PRIVATE_KEY
)
;
await
web3
.
eth
.
sendSignedTransaction
(
signedTx
)
;
}
4.请求询价接口，拿到询价数据
#
4.1定义报价参数
const
quoteParams
=
{
amount
:
fromAmount
,
chainId
:
chainId
,
toTokenAddress
:
toTokenAddress
,
fromTokenAddress
:
fromTokenAddress
,
}
;
4.2 定义辅助函数
/**
 * Get swap quote from DEX API
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
slippage
- Maximum slippage (e.g., "0.5" for 0.5%)
 *
@returns
Swap quote
 */
async
function
getSwapQuote
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/quote'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
fromTokenAddress
,
toTokenAddress
,
amount
,
slippage
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get swap quote:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
5.请求兑换接口，发起交易
#
5.1 定义兑换参数
const
swapParams
=
{
chainId
:
chainId
,
fromTokenAddress
,
toTokenAddress
,
amount
,
userWalletAddress
:
userAddress
,
slippage
}
;
5.2 定义辅助函数
/**
 * Get swap quote from DEX API
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
userAddress
- User wallet address
 *
@param
slippage
- Maximum slippage (e.g., "0.5" for 0.5%)
 *
@returns
Swap quote
 */
async
function
getSwapQuote
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
userAddress
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/swap'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
fromTokenAddress
,
toTokenAddress
,
amount
,
userWalletAddress
:
userAddress
,
slippage
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get swap quote:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
5.3 请求兑换接口拿到 tx 信息
/**
 * Execute token swap
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
slippage
- Maximum slippage
 */
async
function
executeSwap
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
string
>
{
// 1. Check allowance and approve if necessary (skip for native token)
if
(
fromTokenAddress
!==
ETH_ADDRESS
)
{
await
approveToken
(
fromTokenAddress
,
amount
)
;
}
// 2. Get swap transaction data
const
swapData
=
await
getSwapTransaction
(
fromTokenAddress
,
toTokenAddress
,
amount
,
WALLET_ADDRESS
,
slippage
)
;
const
txData
=
swapData
.
tx
;
console
.
log
(
"Swap TX data received"
)
;
// 3. Get accurate gas limit using Onchain gateway API
const
gasLimit
=
await
getGasLimit
(
WALLET_ADDRESS
,
txData
.
to
,
txData
.
value
||
'0'
,
txData
.
data
)
;
console
.
log
(
"Gas limit received"
)
;
// 4. Get current nonce
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
WALLET_ADDRESS
,
'latest'
)
;
console
.
log
(
"Nonce received"
)
;
// 5. Get current gas price and adjust for faster confirmation
const
gasPrice
=
await
web3
.
eth
.
getGasPrice
(
)
;
const
adjustedGasPrice
=
BigInt
(
gasPrice
)
*
BigInt
(
15
)
/
BigInt
(
10
)
;
// 1.5x for faster confirmation
console
.
log
(
"Gas price received"
)
;
// 6. Create transaction object
const
txObject
=
{
from
:
WALLET_ADDRESS
,
to
:
txData
.
to
,
data
:
txData
.
data
,
value
:
txData
.
value
||
'0'
,
gas
:
gasLimit
,
gasPrice
:
adjustedGasPrice
.
toString
(
)
,
nonce
:
nonce
}
;
console
.
log
(
"TX build complete"
)
;
// 7. Sign transaction
const
{
signedTx
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
txObject
,
PRIVATE_KEY
)
;
console
.
log
(
"TX signed"
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
signedTx
)
;
console
.
log
(
'chainTxInfo:'
,
chainTxInfo
)
;
}
6. 广播交易
#
6.1 用
RPC
广播交易
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
signedTx
)
;
console
.
log
(
'chainTxInfo:'
,
chainTxInfo
)
;
6.2 用
交易上链 API
广播交易
try
{
const
path
=
'dex/pre-transaction/broadcast-transaction'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
broadcastData
=
{
signedTx
:
signedTx
.
rawTransaction
,
chainIndex
:
chainId
,
address
:
WALLET_ADDRESS
}
;
// Prepare authentication with body included in signature
const
bodyString
=
JSON
.
stringify
(
broadcastData
)
;
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
`
/api/v5/
${
path
}
`
;
const
headers
=
getHeaders
(
timestamp
,
'POST'
,
requestPath
,
bodyString
)
;
const
response
=
await
axios
.
post
(
url
,
broadcastData
,
{
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
const
orderId
=
response
.
data
.
data
[
0
]
.
orderId
;
console
.
log
(
`
Swap transaction broadcast successfully, Order ID:
${
orderId
}
`
)
;
// 9. Monitor transaction status
await
trackTransaction
(
orderId
)
;
return
orderId
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to broadcast swap transaction:'
,
error
)
;
throw
error
;
}
7. 追踪交易
#
使用
交易上链 API
// Define error info interface
interface
TxErrorInfo
{
error
:
string
;
message
:
string
;
action
:
string
;
}
/**
 * Monitor transaction status
 *
@param
orderId
- Order ID from broadcast response
 *
@param
intervalMs
- Polling interval in milliseconds
 *
@param
timeoutMs
- Maximum time to wait
 *
@returns
Final transaction status
 */
async
function
trackTransaction
(
orderId
:
string
,
intervalMs
:
number
=
5000
,
timeoutMs
:
number
=
300000
)
:
Promise
<
any
>
{
console
.
log
(
`
Monitoring transaction with Order ID:
${
orderId
}
`
)
;
const
startTime
=
Date
.
now
(
)
;
let
lastStatus
=
''
;
while
(
Date
.
now
(
)
-
startTime
<
timeoutMs
)
{
// Get transaction status
try
{
const
path
=
'dex/post-transaction/orders'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
params
=
{
orderId
:
orderId
,
chainIndex
:
chainId
,
address
:
WALLET_ADDRESS
,
limit
:
'1'
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
&&
response
.
data
.
data
&&
response
.
data
.
data
.
length
>
0
)
{
if
(
response
.
data
.
data
[
0
]
.
orders
&&
response
.
data
.
data
[
0
]
.
orders
.
length
>
0
)
{
const
txData
=
response
.
data
.
data
[
0
]
.
orders
[
0
]
;
// Use txStatus to match the API response
const
status
=
txData
.
txStatus
;
// Only log when status changes
if
(
status
!==
lastStatus
)
{
lastStatus
=
status
;
if
(
status
===
'1'
)
{
console
.
log
(
`
Transaction pending:
${
txData
.
txHash
||
'Hash not available yet'
}
`
)
;
}
else
if
(
status
===
'2'
)
{
console
.
log
(
`
Transaction successful: https://web3.okx.com/explorer/base/tx/
${
txData
.
txHash
}
`
)
;
return
txData
;
}
else
if
(
status
===
'3'
)
{
const
failReason
=
txData
.
failReason
||
'Unknown reason'
;
const
errorMessage
=
`
Transaction failed:
${
failReason
}
`
;
console
.
error
(
errorMessage
)
;
const
errorInfo
=
handleTransactionError
(
txData
)
;
console
.
log
(
`
Error type:
${
errorInfo
.
error
}
`
)
;
console
.
log
(
`
Suggested action:
${
errorInfo
.
action
}
`
)
;
throw
new
Error
(
errorMessage
)
;
}
}
}
else
{
console
.
log
(
`
No orders found for Order ID:
${
orderId
}
`
)
;
}
}
}
catch
(
error
)
{
console
.
warn
(
'Error checking transaction status:'
,
(
error
as
Error
)
.
message
)
;
}
// Wait before next check
await
new
Promise
(
resolve
=>
setTimeout
(
resolve
,
intervalMs
)
)
;
}
throw
new
Error
(
'Transaction monitoring timed out'
)
;
}
/**
 * Comprehensive error handling with failReason
 *
@param
txData
- Transaction data from post-transaction/orders
 *
@returns
Structured error information
 */
function
handleTransactionError
(
txData
:
any
)
:
TxErrorInfo
{
const
failReason
=
txData
.
failReason
||
'Unknown reason'
;
// Log the detailed error
console
.
error
(
`
Transaction failed with reason:
${
failReason
}
`
)
;
// Default error handling
return
{
error
:
'TRANSACTION_FAILED'
,
message
:
failReason
,
action
:
'Try again or contact support'
}
;
}
使用
查询 Dex 交易状态 API
/**
 * Track transaction status using DEX API
 *
@param
chainId
- Chain ID (e.g., 1 for Ethereum Mainnet)
 *
@param
txHash
- Transaction hash
 *
@returns
Transaction details
 */
async
function
trackTransactionStatus
(
chainId
:
string
,
txHash
:
string
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/history'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
txHash
:
txHash
,
isFromMyProject
:
'true'
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
const
txData
=
response
.
data
.
data
;
const
status
=
txData
.
status
;
if
(
status
===
'pending'
)
{
console
.
log
(
`
Transaction is still pending:
${
txHash
}
`
)
;
return
{
status
:
'pending'
,
details
:
txData
}
;
}
else
if
(
status
===
'success'
)
{
console
.
log
(
`
Transaction successful!
`
)
;
console
.
log
(
`
From:
${
txData
.
fromTokenDetails
.
symbol
}
- Amount:
${
txData
.
fromTokenDetails
.
amount
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
txData
.
toTokenDetails
.
symbol
}
- Amount:
${
txData
.
toTokenDetails
.
amount
}
`
)
;
console
.
log
(
`
Transaction Fee:
${
txData
.
txFee
}
`
)
;
console
.
log
(
`
Explorer URL: https://web3.okx.com/explorer/base/tx/
${
txHash
}
`
)
;
return
{
status
:
'success'
,
details
:
txData
}
;
}
else
if
(
status
===
'failure'
)
{
console
.
error
(
`
Transaction failed:
${
txData
.
errorMsg
||
'Unknown reason'
}
`
)
;
return
{
status
:
'failure'
,
details
:
txData
}
;
}
return
txData
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to track transaction status:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
交易上链 API 监控使用 /dex/post-transaction/orders 跟踪内部订单处理状态。它有助于监控交易在 OKX 系统中的移动情况，并提供订单 ID 和 基本状态（1：待处理，2：成功，3：失败）。
Swap API 交易跟踪使用 /dex/aggregator/history 提供全面的兑换执行详情。它提供特定于代币的信息（代码、金额）、已支付的费用以及详细的区块链数据。如果您需要完整的兑换验证并提供代币级详细信息，请使用此选项。
选择前者用于基本交易状态更新，而选择后者用于获取兑换执行本身的详细信息。
8. 完整实现
#
这是一个完整的实现示例：
// Token Swap using OKX Onchain gateway API on Base
// Required packages
import
{
Web3
}
from
'web3'
;
import
axios
from
'axios'
;
import
*
as
dotenv
from
'dotenv'
;
import
CryptoJS
from
'crypto-js'
;
// Load environment variables
dotenv
.
config
(
)
;
// Connect to Base network
const
web3
=
new
Web3
(
'https://mainnet.base.org'
)
;
// Your wallet information - REPLACE WITH YOUR OWN VALUES
const
WALLET_ADDRESS
:
string
=
process
.
env
.
EVM_WALLET_ADDRESS
||
'0xYourWalletAddress'
;
const
PRIVATE_KEY
:
string
=
process
.
env
.
EVM_PRIVATE_KEY
||
'YourPrivateKey'
;
// Without 0x prefix
// Token addresses for swap on Base
const
ETH_ADDRESS
:
string
=
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
;
// Native ETH
const
USDC_ADDRESS
:
string
=
'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
;
// Base USDC
// Chain ID for Base
const
chainId
:
string
=
'8453'
;
// API URL
// const baseUrl: string = 'https://web3.okx.com/api/v5/';
const
baseUrl
:
string
=
'https://beta.okex.org/api/v5/'
// Amount to swap in smallest unit (approx $1 of ETH)
// 1 ETH = 10^18 wei, so 0.0005 ETH = 5 * 10^14 wei at ~$2000/ETH
const
SWAP_AMOUNT
:
string
=
'500000000000000'
;
// 0.0005 ETH (approx $1)
const
SLIPPAGE
:
string
=
'0.5'
;
// 0.5% slippage tolerance
// Define type for error handling
interface
TxErrorInfo
{
error
:
string
;
message
:
string
;
action
:
string
;
}
// ===== Get Header Function =====
export
function
getHeaders
(
timestamp
:
string
,
method
:
string
,
requestPath
:
string
,
queryString
=
""
)
{
const
apiKey
=
process
.
env
.
OKX_API_KEY
;
const
secretKey
=
process
.
env
.
OKX_SECRET_KEY
;
const
apiPassphrase
=
process
.
env
.
OKX_API_PASSPHRASE
;
const
projectId
=
process
.
env
.
OKX_PROJECT_ID
;
if
(
!
apiKey
||
!
secretKey
||
!
apiPassphrase
||
!
projectId
)
{
throw
new
Error
(
"Missing required environment variables"
)
;
}
const
stringToSign
=
timestamp
+
method
+
requestPath
+
queryString
;
return
{
"Content-Type"
:
"application/json"
,
"OK-ACCESS-KEY"
:
apiKey
,
"OK-ACCESS-SIGN"
:
CryptoJS
.
enc
.
Base64
.
stringify
(
CryptoJS
.
HmacSHA256
(
stringToSign
,
secretKey
)
)
,
"OK-ACCESS-TIMESTAMP"
:
timestamp
,
"OK-ACCESS-PASSPHRASE"
:
apiPassphrase
,
"OK-ACCESS-PROJECT"
:
projectId
,
}
;
}
// ===== Token Approval Functions =====
/**
 * Check token allowance for DEX
 *
@param
tokenAddress
- Token contract address
 *
@param
ownerAddress
- Your wallet address
 *
@param
spenderAddress
- DEX spender address
 *
@returns
Allowance amount
 */
async
function
checkAllowance
(
tokenAddress
:
string
,
ownerAddress
:
string
,
spenderAddress
:
string
)
:
Promise
<
bigint
>
{
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
return
BigInt
(
String
(
allowance
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
'Failed to query allowance:'
,
error
)
;
throw
error
;
}
}
/**
 * Get approve transaction data from OKX DEX API
 *
@param
tokenAddress
- Token contract address
 *
@param
amount
- Amount to approve
 *
@returns
Approval transaction data
 */
async
function
getApproveTransaction
(
tokenAddress
:
string
,
amount
:
string
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/approve-transaction'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
tokenContractAddress
:
tokenAddress
,
approveAmount
:
amount
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get approval transaction data:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
/**
 * Get transaction gas limit from Onchain gateway API
 *
@param
fromAddress
- Sender address
 *
@param
toAddress
- Target contract address
 *
@param
txAmount
- Transaction amount (0 for approvals)
 *
@param
inputData
- Transaction calldata
 *
@returns
Estimated gas limit
 */
async
function
getGasLimit
(
fromAddress
:
string
,
toAddress
:
string
,
txAmount
:
string
=
'0'
,
inputData
:
string
=
''
)
:
Promise
<
string
>
{
try
{
const
path
=
'dex/pre-transaction/gas-limit'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
console
.
log
(
{
path
:
path
,
url
:
url
}
)
const
body
=
{
chainIndex
:
chainId
,
fromAddress
:
fromAddress
,
toAddress
:
toAddress
,
txAmount
:
txAmount
,
extJson
:
{
inputData
:
inputData
}
}
;
// Prepare authentication with body included in signature
const
bodyString
=
JSON
.
stringify
(
body
)
;
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
`
/api/v5/
${
path
}
`
;
const
headers
=
getHeaders
(
timestamp
,
'POST'
,
requestPath
,
bodyString
)
;
const
response
=
await
axios
.
post
(
url
,
body
,
{
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
.
gasLimit
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get gas limit:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
/**
 * Sign and send approve transaction
 *
@param
tokenAddress
- Token to approve
 *
@param
amount
- Amount to approve
 *
@returns
Order ID of the approval transaction
 */
async
function
approveToken
(
tokenAddress
:
string
,
amount
:
string
)
:
Promise
<
string
|
null
>
{
const
spenderAddress
=
'0x6b2C0c7be2048Daa9b5527982C29f48062B34D58'
;
// Base DEX spender
const
currentAllowance
=
await
checkAllowance
(
tokenAddress
,
WALLET_ADDRESS
,
spenderAddress
)
;
if
(
currentAllowance
>=
BigInt
(
amount
)
)
{
console
.
log
(
'Sufficient allowance already exists'
)
;
return
null
;
}
console
.
log
(
'Insufficient allowance, approving tokens...'
)
;
// Get approve transaction data from OKX DEX API
const
approveData
=
await
getApproveTransaction
(
tokenAddress
,
amount
)
;
// Get accurate gas limit using Onchain gateway API
const
gasLimit
=
await
getGasLimit
(
WALLET_ADDRESS
,
tokenAddress
,
'0'
,
approveData
.
data
)
;
// Get current gas price (can also use Onchain gateway API)
const
gasPrice
=
await
web3
.
eth
.
getGasPrice
(
)
;
const
adjustedGasPrice
=
BigInt
(
gasPrice
)
*
BigInt
(
15
)
/
BigInt
(
10
)
;
// 1.5x for faster confirmation
// Get current nonce
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
WALLET_ADDRESS
,
'latest'
)
;
// Create transaction object
const
txObject
=
{
from
:
WALLET_ADDRESS
,
to
:
tokenAddress
,
data
:
approveData
.
data
,
value
:
'0'
,
gas
:
gasLimit
,
gasPrice
:
adjustedGasPrice
.
toString
(
)
,
nonce
:
nonce
}
;
// Sign transaction
const
signedTx
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
txObject
,
PRIVATE_KEY
)
;
// Broadcast transaction using Onchain gateway API
try
{
const
path
=
'dex/pre-transaction/broadcast-transaction'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
broadcastData
=
{
signedTx
:
signedTx
.
rawTransaction
,
chainIndex
:
chainId
,
address
:
WALLET_ADDRESS
}
;
// Prepare authentication with body included in signature
const
bodyString
=
JSON
.
stringify
(
broadcastData
)
;
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
`
/api/v5/
${
path
}
`
;
const
headers
=
getHeaders
(
timestamp
,
'POST'
,
requestPath
,
bodyString
)
;
const
response
=
await
axios
.
post
(
url
,
broadcastData
,
{
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
const
orderId
=
response
.
data
.
data
[
0
]
.
orderId
;
console
.
log
(
`
Approval transaction broadcast successfully, Order ID:
${
orderId
}
`
)
;
// Monitor transaction status
await
trackTransaction
(
orderId
)
;
return
orderId
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to broadcast approval transaction:'
,
error
)
;
throw
error
;
}
}
// ===== Swap Functions =====
/**
 * Get swap quote from DEX API
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
userAddress
- User wallet address
 *
@param
slippage
- Maximum slippage (e.g., "0.5" for 0.5%)
 *
@returns
Swap quote
 */
async
function
getSwapQuote
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
userAddress
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/swap'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
fromTokenAddress
,
toTokenAddress
,
amount
,
userWalletAddress
:
userAddress
,
slippage
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get swap quote:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
/**
 * Get swap transaction data from DEX API
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
userAddress
- User wallet address
 *
@param
slippage
- Maximum slippage
 *
@returns
Swap transaction data
 */
async
function
getSwapTransaction
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
userAddress
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
any
>
{
try
{
const
path
=
'dex/aggregator/swap'
;
const
url
=
`
${
baseUrl
}
${
path
}
`
;
const
params
=
{
chainId
:
chainId
,
fromTokenAddress
,
toTokenAddress
,
amount
,
userWalletAddress
:
userAddress
,
slippage
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
return
response
.
data
.
data
[
0
]
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to get swap transaction data:'
,
(
error
as
Error
)
.
message
)
;
throw
error
;
}
}
/**
 * Execute token swap
 *
@param
fromTokenAddress
- Source token address
 *
@param
toTokenAddress
- Destination token address
 *
@param
amount
- Amount to swap
 *
@param
slippage
- Maximum slippage
 *
@returns
Order ID of the swap transaction
 */
async
function
executeSwap
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
,
amount
:
string
,
slippage
:
string
=
'0.5'
)
:
Promise
<
string
>
{
// 1. Check allowance and approve if necessary (skip for native token)
if
(
fromTokenAddress
!==
ETH_ADDRESS
)
{
await
approveToken
(
fromTokenAddress
,
amount
)
;
}
// 2. Get swap transaction data
const
swapData
=
await
getSwapTransaction
(
fromTokenAddress
,
toTokenAddress
,
amount
,
WALLET_ADDRESS
,
slippage
)
;
const
txData
=
swapData
.
tx
;
console
.
log
(
"Swap TX data received"
)
;
// 3. Get accurate gas limit using Onchain gateway API
const
gasLimit
=
await
getGasLimit
(
WALLET_ADDRESS
,
txData
.
to
,
txData
.
value
||
'0'
,
txData
.
data
)
;
console
.
log
(
"Gas limit received"
)
;
// 4. Get current nonce
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
WALLET_ADDRESS
,
'latest'
)
;
console
.
log
(
"Nonce received"
)
;
// 5. Get current gas price and adjust for faster confirmation
const
gasPrice
=
await
web3
.
eth
.
getGasPrice
(
)
;
const
adjustedGasPrice
=
BigInt
(
gasPrice
)
*
BigInt
(
15
)
/
BigInt
(
10
)
;
// 1.5x for faster confirmation
console
.
log
(
"Gas price received"
)
;
// 6. Create transaction object
const
txObject
=
{
from
:
WALLET_ADDRESS
,
to
:
txData
.
to
,
data
:
txData
.
data
,
value
:
txData
.
value
||
'0'
,
gas
:
gasLimit
,
gasPrice
:
adjustedGasPrice
.
toString
(
)
,
nonce
:
nonce
}
;
console
.
log
(
"TX build complete"
)
;
// 7. Sign transaction
const
signedTx
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
txObject
,
PRIVATE_KEY
)
;
console
.
log
(
"TX signed"
)
;
// 8. Broadcast transaction using Onchain gateway API
try
{
const
path
=
'dex/pre-transaction/broadcast-transaction'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
broadcastData
=
{
signedTx
:
signedTx
.
rawTransaction
,
chainIndex
:
chainId
,
address
:
WALLET_ADDRESS
}
;
// Prepare authentication with body included in signature
const
bodyString
=
JSON
.
stringify
(
broadcastData
)
;
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
`
/api/v5/
${
path
}
`
;
const
headers
=
getHeaders
(
timestamp
,
'POST'
,
requestPath
,
bodyString
)
;
const
response
=
await
axios
.
post
(
url
,
broadcastData
,
{
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
)
{
const
orderId
=
response
.
data
.
data
[
0
]
.
orderId
;
console
.
log
(
`
Swap transaction broadcast successfully, Order ID:
${
orderId
}
`
)
;
// 9. Monitor transaction status
await
trackTransaction
(
orderId
)
;
return
orderId
;
}
else
{
throw
new
Error
(
`
API Error:
${
response
.
data
.
msg
||
'Unknown error'
}
`
)
;
}
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
'Failed to broadcast swap transaction:'
,
error
)
;
throw
error
;
}
}
// ===== Transaction Monitoring =====
/**
 * Monitor transaction status
 *
@param
orderId
- Order ID from broadcast response
 *
@param
intervalMs
- Polling interval in milliseconds
 *
@param
timeoutMs
- Maximum time to wait
 *
@returns
Final transaction status
 */
async
function
trackTransaction
(
orderId
:
string
,
intervalMs
:
number
=
5000
,
timeoutMs
:
number
=
300000
)
:
Promise
<
any
>
{
console
.
log
(
`
Monitoring transaction with Order ID:
${
orderId
}
`
)
;
const
startTime
=
Date
.
now
(
)
;
let
lastStatus
=
''
;
while
(
Date
.
now
(
)
-
startTime
<
timeoutMs
)
{
// Get transaction status
try
{
const
path
=
'dex/post-transaction/orders'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
params
=
{
orderId
:
orderId
,
chainIndex
:
chainId
,
address
:
WALLET_ADDRESS
,
limit
:
'1'
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
&&
response
.
data
.
data
&&
response
.
data
.
data
.
length
>
0
)
{
if
(
response
.
data
.
data
[
0
]
.
orders
&&
response
.
data
.
data
[
0
]
.
orders
.
length
>
0
)
{
const
txData
=
response
.
data
.
data
[
0
]
.
orders
[
0
]
;
// Use txStatus to match the API response
const
status
=
txData
.
txStatus
;
// Only log when status changes
if
(
status
!==
lastStatus
)
{
lastStatus
=
status
;
if
(
status
===
'1'
)
{
console
.
log
(
`
Transaction pending:
${
txData
.
txHash
||
'Hash not available yet'
}
`
)
;
}
else
if
(
status
===
'2'
)
{
console
.
log
(
`
Transaction successful: https://web3.okx.com/explorer/base/tx/
${
txData
.
txHash
}
`
)
;
return
txData
;
}
else
if
(
status
===
'3'
)
{
const
failReason
=
txData
.
failReason
||
'Unknown reason'
;
const
errorMessage
=
`
Transaction failed:
${
failReason
}
`
;
console
.
error
(
errorMessage
)
;
const
errorInfo
=
handleTransactionError
(
txData
)
;
console
.
log
(
`
Error type:
${
errorInfo
.
error
}
`
)
;
console
.
log
(
`
Suggested action:
${
errorInfo
.
action
}
`
)
;
throw
new
Error
(
errorMessage
)
;
}
}
}
else
{
console
.
log
(
`
No orders found for Order ID:
${
orderId
}
`
)
;
}
}
}
catch
(
error
)
{
console
.
warn
(
'Error checking transaction status:'
,
(
error
as
Error
)
.
message
)
;
}
// Wait before next check
await
new
Promise
(
resolve
=>
setTimeout
(
resolve
,
intervalMs
)
)
;
}
throw
new
Error
(
'Transaction monitoring timed out'
)
;
}
/**
 * Comprehensive error handling with failReason
 *
@param
txData
- Transaction data from post-transaction/orders
 *
@returns
Structured error information
 */
function
handleTransactionError
(
txData
:
any
)
:
TxErrorInfo
{
const
failReason
=
txData
.
failReason
||
'Unknown reason'
;
// Log the detailed error
console
.
error
(
`
Transaction failed with reason:
${
failReason
}
`
)
;
// Default error handling
return
{
error
:
'TRANSACTION_FAILED'
,
message
:
failReason
,
action
:
'Try again or contact support'
}
;
}
// ===== Main Function =====
/**
* Main function to execute ETH to USDC swap on Base
*/
async
function
main
(
)
:
Promise
<
void
>
{
try
{
console
.
log
(
'Starting ETH to USDC swap on Base using Onchain gateway API'
)
;
// Execute swap from ETH to USDC on Base
const
orderId
=
await
executeSwap
(
ETH_ADDRESS
,
// From ETH on Base
USDC_ADDRESS
,
// To USDC on Base
SWAP_AMOUNT
,
// Amount in ETH's smallest unit (0.0005 ETH ≈ $1)
SLIPPAGE
// 0.5% slippage
)
;
// Get final transaction details
try
{
const
path
=
'dex/post-transaction/orders'
;
const
url
=
`
https://web3.okx.com/api/v5/
${
path
}
`
;
const
params
=
{
orderId
:
orderId
,
chainIndex
:
chainId
}
;
// Prepare authentication
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
`
/api/v5/
${
path
}
`
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
'GET'
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
axios
.
get
(
url
,
{
params
,
headers
}
)
;
if
(
response
.
data
.
code
===
'0'
&&
response
.
data
.
data
&&
response
.
data
.
data
.
length
>
0
)
{
console
.
log
(
'Transaction Hash:'
,
response
.
data
.
data
[
0
]
.
txHash
)
;
}
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
'Failed to get final transaction details:'
,
(
error
as
Error
)
.
message
)
;
}
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
'Swap failed:'
,
(
error
as
Error
)
.
message
)
;
}
}
// Execute the main function
main
(
)
;
方法2：SDK方法
#
使用OKX DEX SDK提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为您处理许多实现细节，包括重试逻辑、错误处理和交易管理。
1.安装SDK
#
npm
install
@okx-dex/okx-dex-sdk
# or
yarn
add
@okx-dex/okx-dex-sdk
# or
pnpm
add
@okx-dex/okx-dex-sdk
2.设置环境
#
使用您的API凭据和钱包信息创建一个. env文件：
# OKX API Credentials
OKX_API_KEY
=
your_api_key
OKX_SECRET_KEY
=
your_secret_key
OKX_API_PASSPHRASE
=
your_passphrase
OKX_PROJECT_ID
=
your_project_id
# EVM Configuration
EVM_RPC_URL
=
your_evm_rpc_url
EVM_WALLET_ADDRESS
=
your_evm_wallet_address
EVM_PRIVATE_KEY
=
your_evm_private_key
3.初始化客户端
#
为您的DEX客户端创建一个文件（例如，DexClient. ts）：
// DexClient.ts
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
// Validate environment variables
const
requiredEnvVars
=
[
'OKX_API_KEY'
,
'OKX_SECRET_KEY'
,
'OKX_API_PASSPHRASE'
,
'OKX_PROJECT_ID'
,
'EVM_WALLET_ADDRESS'
,
'EVM_PRIVATE_KEY'
,
'EVM_RPC_URL'
]
;
for
(
const
envVar
of
requiredEnvVars
)
{
if
(
!
process
.
env
[
envVar
]
)
{
throw
new
Error
(
`
Missing required environment variable:
${
envVar
}
`
)
;
}
}
// Initialize the client
export
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
secretKey
:
process
.
env
.
OKX_SECRET_KEY
!
,
apiPassphrase
:
process
.
env
.
OKX_API_PASSPHRASE
!
,
projectId
:
process
.
env
.
OKX_PROJECT_ID
!
,
evm
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
EVM_RPC_URL
!
,
}
,
walletAddress
:
process
.
env
.
EVM_WALLET_ADDRESS
!
,
privateKey
:
process
.
env
.
EVM_PRIVATE_KEY
!
,
}
}
)
;
4.调用SDK执行代币授权
#
创建代币授权工具的功能：
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
5.调用SDK执行兑换
#
创建兑换执行的文件：
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
6.附加的SDK功能
#
SDK提供了简化开发的附加方法：
获取代币对的报价
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
<div class="routes_md__xWlGF"><h1 id="在-evm-链上搭建兑换应用">在 EVM 链上搭建兑换应用<a class="index_header-anchor__Xqb+L" href="#在-evm-链上搭建兑换应用" style="opacity: 0;">#</a></h1>
<p>在EVM网络上使用OKX DEX构建兑换应用程序有两种方法：</p>
<ol>
<li>API 方法-直接调用 OKX DEX API</li>
<li>SDK 方法-使用 <code>@okx-dex/okx-dex-sdk</code> 简化开发人员体验</li>
</ol>
<p>本指南涵盖了这两种方法，以帮助您选择最适合您需求的方法。</p>
<h2 data-content="方法1：API方法" id="方法1：api方法">方法1：API方法<a class="index_header-anchor__Xqb+L" href="#方法1：api方法" style="opacity: 0;">#</a></h2>
<p>在这种方法中，我们将直接使用OKX DEX API演示代币兑换。我们将在以太坊网络上将USDC兑换为ETH。</p>
<h2 data-content="1.设置环境" id="1.设置环境">1.设置环境<a class="index_header-anchor__Xqb+L" href="#1.设置环境" style="opacity: 0;">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// --------------------- npm package ---------------------</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> Web3 <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'web3'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> axios <span class="token keyword">from</span> <span class="token string">'axios'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token operator">*</span> <span class="token keyword">as</span> dotenv <span class="token keyword">from</span> <span class="token string">'dotenv'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> CryptoJS <span class="token keyword">from</span> <span class="token string">'crypto-js'</span><span class="token punctuation">;</span>
<span class="token comment">// The URL for the Ethereum node you want to connect to</span>
<span class="token keyword">const</span> web3 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Web3</span><span class="token punctuation">(</span><span class="token string">'https://......com'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// --------------------- environment variable ---------------------</span>

<span class="token comment">// Load hidden environment variables</span>
dotenv<span class="token punctuation">.</span><span class="token function">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Your wallet information - REPLACE WITH YOUR OWN VALUES</span>
<span class="token keyword">const</span> <span class="token constant">WALLET_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_WALLET_ADDRESS</span> <span class="token operator">||</span> <span class="token string">'0xYourWalletAddress'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">PRIVATE_KEY</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_PRIVATE_KEY</span> <span class="token operator">||</span> <span class="token string">'YourPrivateKey'</span><span class="token punctuation">;</span> 

<span class="token comment">// Token addresses for swap on Ethereum Mainnet</span>
<span class="token keyword">const</span> <span class="token constant">ETH_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">;</span> <span class="token comment">// Native ETH</span>
<span class="token keyword">const</span> <span class="token constant">USDC_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'</span><span class="token punctuation">;</span> <span class="token comment">// USDC</span>

<span class="token comment">// Chain ID for Ethereum Mainnet</span>
<span class="token keyword">const</span> chainId<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'1'</span><span class="token punctuation">;</span>

<span class="token comment">// API URL</span>
<span class="token keyword">const</span> baseUrl<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'https://web3.okx.com/api/v5/'</span><span class="token punctuation">;</span>

<span class="token comment">// Amount to swap in smallest unit (approx $1 of ETH)</span>
<span class="token comment">// 1 ETH = 10^18 wei, so 0.0005 ETH</span>
<span class="token keyword">const</span> <span class="token constant">SWAP_AMOUNT</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'500000000000000'</span><span class="token punctuation">;</span> <span class="token comment">// 0.0005 ETH (approx $1)</span>
<span class="token keyword">const</span> <span class="token constant">SLIPPAGE</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span><span class="token punctuation">;</span> <span class="token comment">// 0.5% slippage tolerance</span>

<span class="token comment">// --------------------- util function ---------------------</span>
<span class="token keyword">export</span> <span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> method<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> requestPath<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
<span class="token comment">// Check https://web3.okx.com/zh-hans/web3/build/docs/waas/rest-authentication for api-key</span>
    <span class="token keyword">const</span> apiKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> secretKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> projectId <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>apiKey <span class="token operator">||</span> <span class="token operator">!</span>secretKey <span class="token operator">||</span> <span class="token operator">!</span>apiPassphrase <span class="token operator">||</span> <span class="token operator">!</span>projectId<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing required environment variables"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> queryString<span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> CryptoJS<span class="token punctuation">.</span>enc<span class="token punctuation">.</span>Base64<span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>
            CryptoJS<span class="token punctuation">.</span><span class="token function">HmacSHA256</span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="2.检查授权额度" id="2.检查授权额度">2.检查授权额度<a class="index_header-anchor__Xqb+L" href="#2.检查授权额度" style="opacity: 0;">#</a></h2>
<p>您需要检查代币是否已批准DEX进行支出。此步骤仅适用于ERC20代币，而不是像ETH这样的本地代币。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Check token allowance for DEX
 * <span class="token keyword">@param</span> <span class="token parameter">tokenAddress</span> - Token contract address
 * <span class="token keyword">@param</span> <span class="token parameter">ownerAddress</span> - Your wallet address
 * <span class="token keyword">@param</span> <span class="token parameter">spenderAddress</span> - DEX spender address
 * <span class="token keyword">@returns</span> Allowance amount
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">checkAllowance</span><span class="token punctuation">(</span>
  tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  ownerAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  spenderAddress<span class="token operator">:</span> <span class="token builtin">string</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>bigint<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> tokenABI <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token string-property property">"constant"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
      <span class="token string-property property">"inputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_owner"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span> <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_spender"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span> <span class="token punctuation">}</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"allowance"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"outputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"uint256"</span> <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"payable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
      <span class="token string-property property">"stateMutability"</span><span class="token operator">:</span> <span class="token string">"view"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"function"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> tokenContract <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">web3</span><span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">Contract</span><span class="token punctuation">(</span>tokenABI<span class="token punctuation">,</span> tokenAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> allowance <span class="token operator">=</span> <span class="token keyword">await</span> tokenContract<span class="token punctuation">.</span>methods<span class="token punctuation">.</span><span class="token function">allowance</span><span class="token punctuation">(</span>ownerAddress<span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">call</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token function">String</span><span class="token punctuation">(</span>allowance<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to query allowance:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="3.检查授权交易参数并发起授权" id="3.检查授权交易参数并发起授权">3.检查授权交易参数并发起授权<a class="index_header-anchor__Xqb+L" href="#3.检查授权交易参数并发起授权" style="opacity: 0;">#</a></h2>
<p>由于 allowanceAmount 小于 fromTokenAmount，你需要对该币种进行授权。</p>
<p>3.1 定义授权交易参数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> getApproveTransactionParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
  tokenContractAddress<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
  approveAmount<span class="token operator">:</span> amount
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<p>3.2 定义辅助函数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getApproveTransaction</span><span class="token punctuation">(</span>
  tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/approve-transaction'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      tokenContractAddress<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
      approveAmount<span class="token operator">:</span> amount
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get approval transaction data:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>3.3 计算 gasLimit</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Get transaction gas limit from Onchain gateway API
 * <span class="token keyword">@param</span> <span class="token parameter">fromAddress</span> - Sender address
 * <span class="token keyword">@param</span> <span class="token parameter">toAddress</span> - Target contract address
 * <span class="token keyword">@param</span> <span class="token parameter">txAmount</span> - Transaction amount (0 for approvals)
 * <span class="token keyword">@param</span> <span class="token parameter">inputData</span> - Transaction calldata
 * <span class="token keyword">@returns</span> Estimated gas limit
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span>
  fromAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  txAmount<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
  inputData<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">''</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/pre-transaction/gas-limit'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> body <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromAddress<span class="token operator">:</span> fromAddress<span class="token punctuation">,</span>
      toAddress<span class="token operator">:</span> toAddress<span class="token punctuation">,</span>
      txAmount<span class="token operator">:</span> txAmount<span class="token punctuation">,</span>
      extJson<span class="token operator">:</span> <span class="token punctuation">{</span>
        inputData<span class="token operator">:</span> inputData
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication with body included in signature</span>
    <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>body<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> body<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>gasLimit<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get gas limit:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>3.4 获取授权交易 tx 并且发送授权请求</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Sign and send approve transaction
 * <span class="token keyword">@param</span> <span class="token parameter">tokenAddress</span> - Token to approve
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to approve
 * <span class="token keyword">@returns</span> Order ID of the approval transaction
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">approveToken</span><span class="token punctuation">(</span>tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span> <span class="token operator">|</span> <span class="token keyword">null</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> spenderAddress <span class="token operator">=</span> <span class="token string">'0x3b3ae790Df4F312e745D270119c6052904FB6790'</span><span class="token punctuation">;</span> <span class="token comment">// Ethereum Mainnet DEX spender</span>
  <span class="token comment">// See Router addresses at:  https://web3.okx.com/build/docs/waas/dex-smart-contract</span>
  <span class="token keyword">const</span> currentAllowance <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">checkAllowance</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">if</span> <span class="token punctuation">(</span>currentAllowance <span class="token operator">&gt;=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Sufficient allowance already exists'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token keyword">null</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Insufficient allowance, approving tokens...'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get approve transaction data from OKX DEX API</span>
  <span class="token keyword">const</span> approveData <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getApproveTransaction</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get accurate gas limit using Onchain gateway API</span>
  <span class="token keyword">const</span> gasLimit <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> tokenAddress<span class="token punctuation">,</span> <span class="token string">'0'</span><span class="token punctuation">,</span> approveData<span class="token punctuation">.</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get current gas price (can also use Onchain gateway API)</span>
  <span class="token keyword">const</span> gasPrice <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> adjustedGasPrice <span class="token operator">=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>gasPrice<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 1.5x for faster confirmation</span>

  <span class="token comment">// Get current nonce</span>
  <span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getTransactionCount</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> <span class="token string">'latest'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Create transaction object</span>
  <span class="token keyword">const</span> txObject <span class="token operator">=</span> <span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
    data<span class="token operator">:</span> approveData<span class="token punctuation">.</span>data<span class="token punctuation">,</span>
    value<span class="token operator">:</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    gas<span class="token operator">:</span> gasLimit<span class="token punctuation">,</span>
    gasPrice<span class="token operator">:</span> adjustedGasPrice<span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    nonce<span class="token operator">:</span> nonce
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token comment">// Sign transaction</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span>signedTx<span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span>accounts<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>txObject<span class="token punctuation">,</span> <span class="token constant">PRIVATE_KEY</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">sendSignedTransaction</span><span class="token punctuation">(</span>signedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="4.请求询价接口，拿到询价数据" id="4.请求询价接口，拿到询价数据">4.请求询价接口，拿到询价数据<a class="index_header-anchor__Xqb+L" href="#4.请求询价接口，拿到询价数据" style="opacity: 0;">#</a></h2>
<p>4.1定义报价参数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> quoteParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  amount<span class="token operator">:</span> fromAmount<span class="token punctuation">,</span>
  chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> toTokenAddress<span class="token punctuation">,</span>
  fromTokenAddress<span class="token operator">:</span> fromTokenAddress<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<p>4.2 定义辅助函数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Get swap quote from DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage (e.g., "0.5" for 0.5%)
 * <span class="token keyword">@returns</span> Swap quote
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapQuote</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/quote'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      amount<span class="token punctuation">,</span>
      slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get swap quote:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="5.请求兑换接口，发起交易" id="5.请求兑换接口，发起交易">5.请求兑换接口，发起交易<a class="index_header-anchor__Xqb+L" href="#5.请求兑换接口，发起交易" style="opacity: 0;">#</a></h2>
<p>5.1 定义兑换参数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> swapParams <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      amount<span class="token punctuation">,</span>
      userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
      slippage
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<p>5.2 定义辅助函数</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Get swap quote from DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">userAddress</span> - User wallet address
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage (e.g., "0.5" for 0.5%)
 * <span class="token keyword">@returns</span> Swap quote
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapQuote</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  userAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/swap'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      amount<span class="token punctuation">,</span>
      userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
      slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get swap quote:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>5.3 请求兑换接口拿到 tx 信息</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Execute token swap
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// 1. Check allowance and approve if necessary (skip for native token)</span>
  <span class="token keyword">if</span> <span class="token punctuation">(</span>fromTokenAddress <span class="token operator">!==</span> <span class="token constant">ETH_ADDRESS</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">await</span> <span class="token function">approveToken</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token comment">// 2. Get swap transaction data</span>
  <span class="token keyword">const</span> swapData <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getSwapTransaction</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">,</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> slippage<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> txData <span class="token operator">=</span> swapData<span class="token punctuation">.</span>tx<span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Swap TX data received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 3. Get accurate gas limit using Onchain gateway API</span>
  <span class="token keyword">const</span> gasLimit <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span>
    <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>to<span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>value <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>data
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Gas limit received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 4. Get current nonce</span>
  <span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getTransactionCount</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> <span class="token string">'latest'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Nonce received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 5. Get current gas price and adjust for faster confirmation</span>
  <span class="token keyword">const</span> gasPrice <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> adjustedGasPrice <span class="token operator">=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>gasPrice<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 1.5x for faster confirmation</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Gas price received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 6. Create transaction object</span>
  <span class="token keyword">const</span> txObject <span class="token operator">=</span> <span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> txData<span class="token punctuation">.</span>to<span class="token punctuation">,</span>
    data<span class="token operator">:</span> txData<span class="token punctuation">.</span>data<span class="token punctuation">,</span>
    value<span class="token operator">:</span> txData<span class="token punctuation">.</span>value <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    gas<span class="token operator">:</span> gasLimit<span class="token punctuation">,</span>
    gasPrice<span class="token operator">:</span> adjustedGasPrice<span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    nonce<span class="token operator">:</span> nonce
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"TX build complete"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 7. Sign transaction</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span>signedTx<span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span>accounts<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>txObject<span class="token punctuation">,</span> <span class="token constant">PRIVATE_KEY</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"TX signed"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> chainTxInfo <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">sendSignedTransaction</span><span class="token punctuation">(</span>signedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'chainTxInfo:'</span><span class="token punctuation">,</span> chainTxInfo<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="6. 广播交易" id="6.-广播交易">6. 广播交易<a class="index_header-anchor__Xqb+L" href="#6.-广播交易" style="opacity: 0;">#</a></h2>
<p>6.1 用 <code>RPC</code> 广播交易</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> chainTxInfo <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">sendSignedTransaction</span><span class="token punctuation">(</span>signedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'chainTxInfo:'</span><span class="token punctuation">,</span> chainTxInfo<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>6.2 用<code>交易上链 API</code>广播交易</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/pre-transaction/broadcast-transaction'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> broadcastData <span class="token operator">=</span> <span class="token punctuation">{</span>
      signedTx<span class="token operator">:</span> signedTx<span class="token punctuation">.</span>rawTransaction<span class="token punctuation">,</span>
      chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication with body included in signature</span>
    <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>broadcastData<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> broadcastData<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> orderId <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orderId<span class="token punctuation">;</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Swap transaction broadcast successfully, Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token comment">// 9. Monitor transaction status</span>
      <span class="token keyword">await</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>orderId<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">return</span> orderId<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to broadcast swap transaction:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="7. 追踪交易" id="7.-追踪交易">7. 追踪交易<a class="index_header-anchor__Xqb+L" href="#7.-追踪交易" style="opacity: 0;">#</a></h2>
<p>使用<code>交易上链 API</code></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Define error info interface</span>
<span class="token keyword">interface</span> <span class="token class-name">TxErrorInfo</span> <span class="token punctuation">{</span>
  error<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  action<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Monitor transaction status
 * <span class="token keyword">@param</span> <span class="token parameter">orderId</span> - Order ID from broadcast response
 * <span class="token keyword">@param</span> <span class="token parameter">intervalMs</span> - Polling interval in milliseconds
 * <span class="token keyword">@param</span> <span class="token parameter">timeoutMs</span> - Maximum time to wait
 * <span class="token keyword">@returns</span> Final transaction status
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>
  orderId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  intervalMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">5000</span><span class="token punctuation">,</span>
  timeoutMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">300000</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Monitoring transaction with Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> startTime <span class="token operator">=</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">let</span> lastStatus <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>

  <span class="token keyword">while</span> <span class="token punctuation">(</span>Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span> startTime <span class="token operator">&lt;</span> timeoutMs<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Get transaction status</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/post-transaction/orders'</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        orderId<span class="token operator">:</span> orderId<span class="token punctuation">,</span>
        chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
        address<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
        limit<span class="token operator">:</span> <span class="token string">'1'</span>
      <span class="token punctuation">}</span><span class="token punctuation">;</span>

      <span class="token comment">// Prepare authentication</span>
      <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      
      <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span> <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders<span class="token punctuation">.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
          <span class="token keyword">const</span> txData <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
          
          <span class="token comment">// Use txStatus to match the API response</span>
          <span class="token keyword">const</span> status <span class="token operator">=</span> txData<span class="token punctuation">.</span>txStatus<span class="token punctuation">;</span>

          <span class="token comment">// Only log when status changes</span>
          <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">!==</span> lastStatus<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            lastStatus <span class="token operator">=</span> status<span class="token punctuation">;</span>

            <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'1'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction pending: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash <span class="token operator">||</span> <span class="token string">'Hash not available yet'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'2'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful: https://web3.okx.com/explorer/base/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token keyword">return</span> txData<span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'3'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token keyword">const</span> failReason <span class="token operator">=</span> txData<span class="token punctuation">.</span>failReason <span class="token operator">||</span> <span class="token string">'Unknown reason'</span><span class="token punctuation">;</span>
              <span class="token keyword">const</span> errorMessage <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction failed: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>failReason<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span>errorMessage<span class="token punctuation">)</span><span class="token punctuation">;</span>

              <span class="token keyword">const</span> errorInfo <span class="token operator">=</span> <span class="token function">handleTransactionError</span><span class="token punctuation">(</span>txData<span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Error type: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>errorInfo<span class="token punctuation">.</span>error<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Suggested action: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>errorInfo<span class="token punctuation">.</span>action<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

              <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>errorMessage<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
          <span class="token punctuation">}</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
          <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">No orders found for Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">warn</span><span class="token punctuation">(</span><span class="token string">'Error checking transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token comment">// Wait before next check</span>
    <span class="token keyword">await</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token builtin">Promise</span></span><span class="token punctuation">(</span>resolve <span class="token operator">=&gt;</span> <span class="token function">setTimeout</span><span class="token punctuation">(</span>resolve<span class="token punctuation">,</span> intervalMs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Transaction monitoring timed out'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Comprehensive error handling with failReason
 * <span class="token keyword">@param</span> <span class="token parameter">txData</span> - Transaction data from post-transaction/orders
 * <span class="token keyword">@returns</span> Structured error information
 */</span>
<span class="token keyword">function</span> <span class="token function">handleTransactionError</span><span class="token punctuation">(</span>txData<span class="token operator">:</span> <span class="token builtin">any</span><span class="token punctuation">)</span><span class="token operator">:</span> TxErrorInfo <span class="token punctuation">{</span>
  <span class="token keyword">const</span> failReason <span class="token operator">=</span> txData<span class="token punctuation">.</span>failReason <span class="token operator">||</span> <span class="token string">'Unknown reason'</span><span class="token punctuation">;</span>

  <span class="token comment">// Log the detailed error</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction failed with reason: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>failReason<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Default error handling</span>
  <span class="token keyword">return</span> <span class="token punctuation">{</span>
    error<span class="token operator">:</span> <span class="token string">'TRANSACTION_FAILED'</span><span class="token punctuation">,</span>
    message<span class="token operator">:</span> failReason<span class="token punctuation">,</span>
    action<span class="token operator">:</span> <span class="token string">'Try again or contact support'</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>使用 <code>查询 Dex 交易状态 API</code></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Track transaction status using DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">chainId</span> - Chain ID (e.g., 1 for Ethereum Mainnet)
 * <span class="token keyword">@param</span> <span class="token parameter">txHash</span> - Transaction hash
 * <span class="token keyword">@returns</span> Transaction details
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransactionStatus</span><span class="token punctuation">(</span>chainId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> txHash<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/history'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      txHash<span class="token operator">:</span> txHash<span class="token punctuation">,</span>
      isFromMyProject<span class="token operator">:</span> <span class="token string">'true'</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> txData <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">;</span>
      <span class="token keyword">const</span> status <span class="token operator">=</span> txData<span class="token punctuation">.</span>status<span class="token punctuation">;</span>

      <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'pending'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction is still pending: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">return</span> <span class="token punctuation">{</span> status<span class="token operator">:</span> <span class="token string">'pending'</span><span class="token punctuation">,</span> details<span class="token operator">:</span> txData <span class="token punctuation">}</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'success'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful!</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">From: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>fromTokenDetails<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> - Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>fromTokenDetails<span class="token punctuation">.</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">To: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>toTokenDetails<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> - Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>toTokenDetails<span class="token punctuation">.</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction Fee: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txFee<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Explorer URL: https://web3.okx.com/explorer/base/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">return</span> <span class="token punctuation">{</span> status<span class="token operator">:</span> <span class="token string">'success'</span><span class="token punctuation">,</span> details<span class="token operator">:</span> txData <span class="token punctuation">}</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'failure'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction failed: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>errorMsg <span class="token operator">||</span> <span class="token string">'Unknown reason'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">return</span> <span class="token punctuation">{</span> status<span class="token operator">:</span> <span class="token string">'failure'</span><span class="token punctuation">,</span> details<span class="token operator">:</span> txData <span class="token punctuation">}</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span>
      
      <span class="token keyword">return</span> txData<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to track transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p><p>交易上链 API 监控使用 /dex/post-transaction/orders 跟踪内部订单处理状态。它有助于监控交易在 OKX 系统中的移动情况，并提供订单 ID 和 基本状态（1：待处理，2：成功，3：失败）。<br/>
Swap API 交易跟踪使用 /dex/aggregator/history  提供全面的兑换执行详情。它提供特定于代币的信息（代码、金额）、已支付的费用以及详细的区块链数据。如果您需要完整的兑换验证并提供代币级详细信息，请使用此选项。
选择前者用于基本交易状态更新，而选择后者用于获取兑换执行本身的详细信息。</p></p>
<h2 data-content="8. 完整实现" id="8.-完整实现">8. 完整实现<a class="index_header-anchor__Xqb+L" href="#8.-完整实现" style="opacity: 0;">#</a></h2>
<p>这是一个完整的实现示例：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Token Swap using OKX Onchain gateway API on Base</span>
<span class="token comment">// Required packages</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> Web3 <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'web3'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> axios <span class="token keyword">from</span> <span class="token string">'axios'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token operator">*</span> <span class="token keyword">as</span> dotenv <span class="token keyword">from</span> <span class="token string">'dotenv'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> CryptoJS <span class="token keyword">from</span> <span class="token string">'crypto-js'</span><span class="token punctuation">;</span>

<span class="token comment">// Load environment variables</span>
dotenv<span class="token punctuation">.</span><span class="token function">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Connect to Base network</span>
<span class="token keyword">const</span> web3 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Web3</span><span class="token punctuation">(</span><span class="token string">'https://mainnet.base.org'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Your wallet information - REPLACE WITH YOUR OWN VALUES</span>
<span class="token keyword">const</span> <span class="token constant">WALLET_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_WALLET_ADDRESS</span> <span class="token operator">||</span> <span class="token string">'0xYourWalletAddress'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">PRIVATE_KEY</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_PRIVATE_KEY</span> <span class="token operator">||</span> <span class="token string">'YourPrivateKey'</span><span class="token punctuation">;</span> <span class="token comment">// Without 0x prefix</span>

<span class="token comment">// Token addresses for swap on Base</span>
<span class="token keyword">const</span> <span class="token constant">ETH_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">;</span> <span class="token comment">// Native ETH</span>
<span class="token keyword">const</span> <span class="token constant">USDC_ADDRESS</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'</span><span class="token punctuation">;</span> <span class="token comment">// Base USDC</span>

<span class="token comment">// Chain ID for Base</span>
<span class="token keyword">const</span> chainId<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'8453'</span><span class="token punctuation">;</span>

<span class="token comment">// API URL</span>
<span class="token comment">// const baseUrl: string = 'https://web3.okx.com/api/v5/';</span>
<span class="token keyword">const</span> baseUrl<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'https://beta.okex.org/api/v5/'</span>

<span class="token comment">// Amount to swap in smallest unit (approx $1 of ETH)</span>
<span class="token comment">// 1 ETH = 10^18 wei, so 0.0005 ETH = 5 * 10^14 wei at ~$2000/ETH</span>
<span class="token keyword">const</span> <span class="token constant">SWAP_AMOUNT</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'500000000000000'</span><span class="token punctuation">;</span> <span class="token comment">// 0.0005 ETH (approx $1)</span>
<span class="token keyword">const</span> <span class="token constant">SLIPPAGE</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span><span class="token punctuation">;</span> <span class="token comment">// 0.5% slippage tolerance</span>

<span class="token comment">// Define type for error handling</span>
<span class="token keyword">interface</span> <span class="token class-name">TxErrorInfo</span> <span class="token punctuation">{</span>
  error<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
  action<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// ===== Get Header Function =====</span>

<span class="token keyword">export</span> <span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> method<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> requestPath<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> apiKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> secretKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> projectId <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>apiKey <span class="token operator">||</span> <span class="token operator">!</span>secretKey <span class="token operator">||</span> <span class="token operator">!</span>apiPassphrase <span class="token operator">||</span> <span class="token operator">!</span>projectId<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing required environment variables"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> queryString<span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> CryptoJS<span class="token punctuation">.</span>enc<span class="token punctuation">.</span>Base64<span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>
            CryptoJS<span class="token punctuation">.</span><span class="token function">HmacSHA256</span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// ===== Token Approval Functions =====</span>

<span class="token doc-comment comment">/**
 * Check token allowance for DEX
 * <span class="token keyword">@param</span> <span class="token parameter">tokenAddress</span> - Token contract address
 * <span class="token keyword">@param</span> <span class="token parameter">ownerAddress</span> - Your wallet address
 * <span class="token keyword">@param</span> <span class="token parameter">spenderAddress</span> - DEX spender address
 * <span class="token keyword">@returns</span> Allowance amount
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">checkAllowance</span><span class="token punctuation">(</span>
  tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  ownerAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  spenderAddress<span class="token operator">:</span> <span class="token builtin">string</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>bigint<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> tokenABI <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token string-property property">"constant"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
      <span class="token string-property property">"inputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_owner"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span> <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"_spender"</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"address"</span> <span class="token punctuation">}</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">"allowance"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"outputs"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> <span class="token string-property property">"name"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span> <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"uint256"</span> <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token string-property property">"payable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
      <span class="token string-property property">"stateMutability"</span><span class="token operator">:</span> <span class="token string">"view"</span><span class="token punctuation">,</span>
      <span class="token string-property property">"type"</span><span class="token operator">:</span> <span class="token string">"function"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> tokenContract <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">web3</span><span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">Contract</span><span class="token punctuation">(</span>tokenABI<span class="token punctuation">,</span> tokenAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> allowance <span class="token operator">=</span> <span class="token keyword">await</span> tokenContract<span class="token punctuation">.</span>methods<span class="token punctuation">.</span><span class="token function">allowance</span><span class="token punctuation">(</span>ownerAddress<span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">call</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token function">String</span><span class="token punctuation">(</span>allowance<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to query allowance:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Get approve transaction data from OKX DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">tokenAddress</span> - Token contract address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to approve
 * <span class="token keyword">@returns</span> Approval transaction data
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getApproveTransaction</span><span class="token punctuation">(</span>
  tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/approve-transaction'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      tokenContractAddress<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
      approveAmount<span class="token operator">:</span> amount
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get approval transaction data:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Get transaction gas limit from Onchain gateway API
 * <span class="token keyword">@param</span> <span class="token parameter">fromAddress</span> - Sender address
 * <span class="token keyword">@param</span> <span class="token parameter">toAddress</span> - Target contract address
 * <span class="token keyword">@param</span> <span class="token parameter">txAmount</span> - Transaction amount (0 for approvals)
 * <span class="token keyword">@param</span> <span class="token parameter">inputData</span> - Transaction calldata
 * <span class="token keyword">@returns</span> Estimated gas limit
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span>
  fromAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  txAmount<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
  inputData<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">''</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/pre-transaction/gas-limit'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token punctuation">{</span>path<span class="token operator">:</span> path<span class="token punctuation">,</span> url<span class="token operator">:</span>url<span class="token punctuation">}</span><span class="token punctuation">)</span>

    <span class="token keyword">const</span> body <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromAddress<span class="token operator">:</span> fromAddress<span class="token punctuation">,</span>
      toAddress<span class="token operator">:</span> toAddress<span class="token punctuation">,</span>
      txAmount<span class="token operator">:</span> txAmount<span class="token punctuation">,</span>
      extJson<span class="token operator">:</span> <span class="token punctuation">{</span>
        inputData<span class="token operator">:</span> inputData
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication with body included in signature</span>
    <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>body<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> body<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>gasLimit<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get gas limit:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Sign and send approve transaction
 * <span class="token keyword">@param</span> <span class="token parameter">tokenAddress</span> - Token to approve
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to approve
 * <span class="token keyword">@returns</span> Order ID of the approval transaction
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">approveToken</span><span class="token punctuation">(</span>tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span> <span class="token operator">|</span> <span class="token keyword">null</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> spenderAddress <span class="token operator">=</span> <span class="token string">'0x6b2C0c7be2048Daa9b5527982C29f48062B34D58'</span><span class="token punctuation">;</span> <span class="token comment">// Base DEX spender</span>
  <span class="token keyword">const</span> currentAllowance <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">checkAllowance</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> spenderAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">if</span> <span class="token punctuation">(</span>currentAllowance <span class="token operator">&gt;=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Sufficient allowance already exists'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token keyword">null</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Insufficient allowance, approving tokens...'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get approve transaction data from OKX DEX API</span>
  <span class="token keyword">const</span> approveData <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getApproveTransaction</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get accurate gas limit using Onchain gateway API</span>
  <span class="token keyword">const</span> gasLimit <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> tokenAddress<span class="token punctuation">,</span> <span class="token string">'0'</span><span class="token punctuation">,</span> approveData<span class="token punctuation">.</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Get current gas price (can also use Onchain gateway API)</span>
  <span class="token keyword">const</span> gasPrice <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> adjustedGasPrice <span class="token operator">=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>gasPrice<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 1.5x for faster confirmation</span>

  <span class="token comment">// Get current nonce</span>
  <span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getTransactionCount</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> <span class="token string">'latest'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Create transaction object</span>
  <span class="token keyword">const</span> txObject <span class="token operator">=</span> <span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
    data<span class="token operator">:</span> approveData<span class="token punctuation">.</span>data<span class="token punctuation">,</span>
    value<span class="token operator">:</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    gas<span class="token operator">:</span> gasLimit<span class="token punctuation">,</span>
    gasPrice<span class="token operator">:</span> adjustedGasPrice<span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    nonce<span class="token operator">:</span> nonce
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token comment">// Sign transaction</span>
  <span class="token keyword">const</span> signedTx <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span>accounts<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>txObject<span class="token punctuation">,</span> <span class="token constant">PRIVATE_KEY</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Broadcast transaction using Onchain gateway API</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/pre-transaction/broadcast-transaction'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> broadcastData <span class="token operator">=</span> <span class="token punctuation">{</span>
      signedTx<span class="token operator">:</span> signedTx<span class="token punctuation">.</span>rawTransaction<span class="token punctuation">,</span>
      chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication with body included in signature</span>
    <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>broadcastData<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> broadcastData<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> orderId <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orderId<span class="token punctuation">;</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Approval transaction broadcast successfully, Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token comment">// Monitor transaction status</span>
      <span class="token keyword">await</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>orderId<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">return</span> orderId<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to broadcast approval transaction:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// ===== Swap Functions =====</span>

<span class="token doc-comment comment">/**
 * Get swap quote from DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">userAddress</span> - User wallet address
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage (e.g., "0.5" for 0.5%)
 * <span class="token keyword">@returns</span> Swap quote
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapQuote</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  userAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/swap'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      amount<span class="token punctuation">,</span>
      userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
      slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get swap quote:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Get swap transaction data from DEX API
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">userAddress</span> - User wallet address
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage
 * <span class="token keyword">@returns</span> Swap transaction data
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapTransaction</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  userAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/swap'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      fromTokenAddress<span class="token punctuation">,</span>
      toTokenAddress<span class="token punctuation">,</span>
      amount<span class="token punctuation">,</span>
      userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
      slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get swap transaction data:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Execute token swap
 * <span class="token keyword">@param</span> <span class="token parameter">fromTokenAddress</span> - Source token address
 * <span class="token keyword">@param</span> <span class="token parameter">toTokenAddress</span> - Destination token address
 * <span class="token keyword">@param</span> <span class="token parameter">amount</span> - Amount to swap
 * <span class="token keyword">@param</span> <span class="token parameter">slippage</span> - Maximum slippage
 * <span class="token keyword">@returns</span> Order ID of the swap transaction
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span>
  fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token comment">// 1. Check allowance and approve if necessary (skip for native token)</span>
  <span class="token keyword">if</span> <span class="token punctuation">(</span>fromTokenAddress <span class="token operator">!==</span> <span class="token constant">ETH_ADDRESS</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">await</span> <span class="token function">approveToken</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token comment">// 2. Get swap transaction data</span>
  <span class="token keyword">const</span> swapData <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getSwapTransaction</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">,</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> slippage<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> txData <span class="token operator">=</span> swapData<span class="token punctuation">.</span>tx<span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Swap TX data received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 3. Get accurate gas limit using Onchain gateway API</span>
  <span class="token keyword">const</span> gasLimit <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getGasLimit</span><span class="token punctuation">(</span>
    <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>to<span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>value <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    txData<span class="token punctuation">.</span>data
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Gas limit received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 4. Get current nonce</span>
  <span class="token keyword">const</span> nonce <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getTransactionCount</span><span class="token punctuation">(</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span> <span class="token string">'latest'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Nonce received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 5. Get current gas price and adjust for faster confirmation</span>
  <span class="token keyword">const</span> gasPrice <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span><span class="token function">getGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> adjustedGasPrice <span class="token operator">=</span> <span class="token function">BigInt</span><span class="token punctuation">(</span>gasPrice<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">15</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token function">BigInt</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">)</span><span class="token punctuation">;</span> <span class="token comment">// 1.5x for faster confirmation</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Gas price received"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 6. Create transaction object</span>
  <span class="token keyword">const</span> txObject <span class="token operator">=</span> <span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> txData<span class="token punctuation">.</span>to<span class="token punctuation">,</span>
    data<span class="token operator">:</span> txData<span class="token punctuation">.</span>data<span class="token punctuation">,</span>
    value<span class="token operator">:</span> txData<span class="token punctuation">.</span>value <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">,</span>
    gas<span class="token operator">:</span> gasLimit<span class="token punctuation">,</span>
    gasPrice<span class="token operator">:</span> adjustedGasPrice<span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    nonce<span class="token operator">:</span> nonce
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"TX build complete"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 7. Sign transaction</span>
  <span class="token keyword">const</span> signedTx <span class="token operator">=</span> <span class="token keyword">await</span> web3<span class="token punctuation">.</span>eth<span class="token punctuation">.</span>accounts<span class="token punctuation">.</span><span class="token function">signTransaction</span><span class="token punctuation">(</span>txObject<span class="token punctuation">,</span> <span class="token constant">PRIVATE_KEY</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"TX signed"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 8. Broadcast transaction using Onchain gateway API</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/pre-transaction/broadcast-transaction'</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> broadcastData <span class="token operator">=</span> <span class="token punctuation">{</span>
      signedTx<span class="token operator">:</span> signedTx<span class="token punctuation">.</span>rawTransaction<span class="token punctuation">,</span>
      chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// Prepare authentication with body included in signature</span>
    <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>broadcastData<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> broadcastData<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> orderId <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orderId<span class="token punctuation">;</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Swap transaction broadcast successfully, Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token comment">// 9. Monitor transaction status</span>
      <span class="token keyword">await</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>orderId<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">return</span> orderId<span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to broadcast swap transaction:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// ===== Transaction Monitoring =====</span>

<span class="token doc-comment comment">/**
 * Monitor transaction status
 * <span class="token keyword">@param</span> <span class="token parameter">orderId</span> - Order ID from broadcast response
 * <span class="token keyword">@param</span> <span class="token parameter">intervalMs</span> - Polling interval in milliseconds
 * <span class="token keyword">@param</span> <span class="token parameter">timeoutMs</span> - Maximum time to wait
 * <span class="token keyword">@returns</span> Final transaction status
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>
  orderId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
  intervalMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">5000</span><span class="token punctuation">,</span>
  timeoutMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">300000</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Monitoring transaction with Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> startTime <span class="token operator">=</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">let</span> lastStatus <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>

  <span class="token keyword">while</span> <span class="token punctuation">(</span>Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span> startTime <span class="token operator">&lt;</span> timeoutMs<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Get transaction status</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/post-transaction/orders'</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        orderId<span class="token operator">:</span> orderId<span class="token punctuation">,</span>
        chainIndex<span class="token operator">:</span> chainId<span class="token punctuation">,</span>
        address<span class="token operator">:</span> <span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">,</span>
        limit<span class="token operator">:</span> <span class="token string">'1'</span>
      <span class="token punctuation">}</span><span class="token punctuation">;</span>

      <span class="token comment">// Prepare authentication</span>
      <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      
      <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span> <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders<span class="token punctuation">.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
          <span class="token keyword">const</span> txData <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orders<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
          
          <span class="token comment">// Use txStatus to match the API response</span>
          <span class="token keyword">const</span> status <span class="token operator">=</span> txData<span class="token punctuation">.</span>txStatus<span class="token punctuation">;</span>

          <span class="token comment">// Only log when status changes</span>
          <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">!==</span> lastStatus<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            lastStatus <span class="token operator">=</span> status<span class="token punctuation">;</span>

            <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'1'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction pending: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash <span class="token operator">||</span> <span class="token string">'Hash not available yet'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'2'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful: https://web3.okx.com/explorer/base/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token keyword">return</span> txData<span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'3'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
              <span class="token keyword">const</span> failReason <span class="token operator">=</span> txData<span class="token punctuation">.</span>failReason <span class="token operator">||</span> <span class="token string">'Unknown reason'</span><span class="token punctuation">;</span>
              <span class="token keyword">const</span> errorMessage <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction failed: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>failReason<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span>errorMessage<span class="token punctuation">)</span><span class="token punctuation">;</span>

              <span class="token keyword">const</span> errorInfo <span class="token operator">=</span> <span class="token function">handleTransactionError</span><span class="token punctuation">(</span>txData<span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Error type: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>errorInfo<span class="token punctuation">.</span>error<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
              <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Suggested action: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>errorInfo<span class="token punctuation">.</span>action<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

              <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>errorMessage<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
          <span class="token punctuation">}</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
          <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">No orders found for Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">warn</span><span class="token punctuation">(</span><span class="token string">'Error checking transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token comment">// Wait before next check</span>
    <span class="token keyword">await</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token builtin">Promise</span></span><span class="token punctuation">(</span>resolve <span class="token operator">=&gt;</span> <span class="token function">setTimeout</span><span class="token punctuation">(</span>resolve<span class="token punctuation">,</span> intervalMs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Transaction monitoring timed out'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Comprehensive error handling with failReason
 * <span class="token keyword">@param</span> <span class="token parameter">txData</span> - Transaction data from post-transaction/orders
 * <span class="token keyword">@returns</span> Structured error information
 */</span>
<span class="token keyword">function</span> <span class="token function">handleTransactionError</span><span class="token punctuation">(</span>txData<span class="token operator">:</span> <span class="token builtin">any</span><span class="token punctuation">)</span><span class="token operator">:</span> TxErrorInfo <span class="token punctuation">{</span>
  <span class="token keyword">const</span> failReason <span class="token operator">=</span> txData<span class="token punctuation">.</span>failReason <span class="token operator">||</span> <span class="token string">'Unknown reason'</span><span class="token punctuation">;</span>

  <span class="token comment">// Log the detailed error</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction failed with reason: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>failReason<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// Default error handling</span>
  <span class="token keyword">return</span> <span class="token punctuation">{</span>
    error<span class="token operator">:</span> <span class="token string">'TRANSACTION_FAILED'</span><span class="token punctuation">,</span>
    message<span class="token operator">:</span> failReason<span class="token punctuation">,</span>
    action<span class="token operator">:</span> <span class="token string">'Try again or contact support'</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// ===== Main Function =====</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Main function to execute ETH to USDC swap on Base</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token keyword">void</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Starting ETH to USDC swap on Base using Onchain gateway API'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token comment">// Execute swap from ETH to USDC on Base</span>
    <span class="token keyword">const</span> orderId <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span>
      <span class="token constant">ETH_ADDRESS</span><span class="token punctuation">,</span>    <span class="token comment">// From ETH on Base</span>
      <span class="token constant">USDC_ADDRESS</span><span class="token punctuation">,</span>   <span class="token comment">// To USDC on Base</span>
      <span class="token constant">SWAP_AMOUNT</span><span class="token punctuation">,</span>    <span class="token comment">// Amount in ETH's smallest unit (0.0005 ETH ≈ $1)</span>
      <span class="token constant">SLIPPAGE</span>        <span class="token comment">// 0.5% slippage</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token comment">// Get final transaction details</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
      <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/post-transaction/orders'</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        orderId<span class="token operator">:</span> orderId<span class="token punctuation">,</span>
        chainIndex<span class="token operator">:</span> chainId
      <span class="token punctuation">}</span><span class="token punctuation">;</span>

      <span class="token comment">// Prepare authentication</span>
      <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

      <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span> <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data <span class="token operator">&amp;&amp;</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Transaction Hash:'</span><span class="token punctuation">,</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>txHash<span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to get final transaction details:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Swap failed:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">as</span> Error<span class="token punctuation">)</span><span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Execute the main function</span>
<span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="方法2：SDK方法" id="方法2：sdk方法">方法2：SDK方法<a class="index_header-anchor__Xqb+L" href="#方法2：sdk方法" style="opacity: 0;">#</a></h2>
<p>使用OKX DEX SDK提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为您处理许多实现细节，包括重试逻辑、错误处理和交易管理。</p>
<h2 data-content="1.安装SDK" id="1.安装sdk">1.安装SDK<a class="index_header-anchor__Xqb+L" href="#1.安装sdk" style="opacity: 0;">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">yarn</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">pnpm</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
</code></pre></div>
<h2 data-content="2.设置环境" id="2.设置环境">2.设置环境<a class="index_header-anchor__Xqb+L" href="#2.设置环境" style="opacity: 0;">#</a></h2>
<p>使用您的API凭据和钱包信息创建一个. env文件：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token comment"># OKX API Credentials</span>
<span class="token assign-left variable">OKX_API_KEY</span><span class="token operator">=</span>your_api_key
<span class="token assign-left variable">OKX_SECRET_KEY</span><span class="token operator">=</span>your_secret_key
<span class="token assign-left variable">OKX_API_PASSPHRASE</span><span class="token operator">=</span>your_passphrase
<span class="token assign-left variable">OKX_PROJECT_ID</span><span class="token operator">=</span>your_project_id
<span class="token comment"># EVM Configuration</span>
<span class="token assign-left variable">EVM_RPC_URL</span><span class="token operator">=</span>your_evm_rpc_url
<span class="token assign-left variable">EVM_WALLET_ADDRESS</span><span class="token operator">=</span>your_evm_wallet_address
<span class="token assign-left variable">EVM_PRIVATE_KEY</span><span class="token operator">=</span>your_evm_private_key
</code></pre></div>
<h2 data-content="3.初始化客户端" id="3.初始化客户端">3.初始化客户端<a class="index_header-anchor__Xqb+L" href="#3.初始化客户端" style="opacity: 0;">#</a></h2>
<p>为您的DEX客户端创建一个文件（例如，DexClient. ts）：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// DexClient.ts</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> OKXDexClient <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@okx-dex/okx-dex-sdk'</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token string">'dotenv/config'</span><span class="token punctuation">;</span>
<span class="token comment">// Validate environment variables</span>
<span class="token keyword">const</span> requiredEnvVars <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token string">'OKX_API_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_SECRET_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_API_PASSPHRASE'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_PROJECT_ID'</span><span class="token punctuation">,</span>
    <span class="token string">'EVM_WALLET_ADDRESS'</span><span class="token punctuation">,</span>
    <span class="token string">'EVM_PRIVATE_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'EVM_RPC_URL'</span>
<span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword">for</span> <span class="token punctuation">(</span><span class="token keyword">const</span> envVar <span class="token keyword">of</span> requiredEnvVars<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span>env<span class="token punctuation">[</span>envVar<span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Missing required environment variable: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>envVar<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Initialize the client</span>
<span class="token keyword">export</span> <span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXDexClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    apiKey<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    secretKey<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    apiPassphrase<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token operator">!</span><span class="token punctuation">,</span>
    projectId<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token operator">!</span><span class="token punctuation">,</span>
    evm<span class="token operator">:</span> <span class="token punctuation">{</span>
        connection<span class="token operator">:</span> <span class="token punctuation">{</span>
            rpcUrl<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_RPC_URL</span><span class="token operator">!</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        walletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_WALLET_ADDRESS</span><span class="token operator">!</span><span class="token punctuation">,</span>
        privateKey<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_PRIVATE_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="4.调用SDK执行代币授权" id="4.调用sdk执行代币授权">4.调用SDK执行代币授权<a class="index_header-anchor__Xqb+L" href="#4.调用sdk执行代币授权" style="opacity: 0;">#</a></h2>
<p>创建代币授权工具的功能：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// approval.ts</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> client <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token comment">// Helper function to convert human-readable amounts to base units</span>
<span class="token keyword">export</span> <span class="token keyword">function</span> <span class="token function">toBaseUnits</span><span class="token punctuation">(</span>amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> decimals<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token punctuation">{</span>
    <span class="token comment">// Remove any decimal point and count the decimal places</span>
    <span class="token keyword">const</span> <span class="token punctuation">[</span>integerPart<span class="token punctuation">,</span> decimalPart <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">]</span> <span class="token operator">=</span> amount<span class="token punctuation">.</span><span class="token function">split</span><span class="token punctuation">(</span><span class="token string">'.'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> currentDecimals <span class="token operator">=</span> decimalPart<span class="token punctuation">.</span>length<span class="token punctuation">;</span>

    <span class="token comment">// Combine integer and decimal parts, removing the decimal point</span>
    <span class="token keyword">let</span> result <span class="token operator">=</span> integerPart <span class="token operator">+</span> decimalPart<span class="token punctuation">;</span>

    <span class="token comment">// Add zeros if we need more decimal places</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">&lt;</span> decimals<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        result <span class="token operator">=</span> result <span class="token operator">+</span> <span class="token string">'0'</span><span class="token punctuation">.</span><span class="token function">repeat</span><span class="token punctuation">(</span>decimals <span class="token operator">-</span> currentDecimals<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// Remove digits if we have too many decimal places</span>
    <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">&gt;</span> decimals<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        result <span class="token operator">=</span> result<span class="token punctuation">.</span><span class="token function">slice</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>length <span class="token operator">-</span> <span class="token punctuation">(</span>currentDecimals <span class="token operator">-</span> decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token comment">// Remove leading zeros</span>
    result <span class="token operator">=</span> result<span class="token punctuation">.</span><span class="token function">replace</span><span class="token punctuation">(</span><span class="token regex"><span class="token regex-delimiter">/</span><span class="token regex-source language-regex"><span class="token anchor function">^</span>0<span class="token quantifier number">+</span></span><span class="token regex-delimiter">/</span></span><span class="token punctuation">,</span> <span class="token string">''</span><span class="token punctuation">)</span> <span class="token operator">||</span> <span class="token string">'0'</span><span class="token punctuation">;</span>

    <span class="token keyword">return</span> result<span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Approve a token for swapping</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeApproval</span><span class="token punctuation">(</span>tokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// Get token information using quote</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            chainId<span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
            fromTokenAddress<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
            toTokenAddress<span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// Native token</span>
            amount<span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span> <span class="token comment">// Use a reasonable amount for quote</span>
            slippage<span class="token operator">:</span> <span class="token string">'0.5'</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenDecimals <span class="token operator">=</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimal<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token function">toBaseUnits</span><span class="token punctuation">(</span>amount<span class="token punctuation">,</span> tokenDecimals<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">\nApproval Details:</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">--------------------</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Token: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenSymbol<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenSymbol<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount in base units: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>rawAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token comment">// Execute the approval</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting approval..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">executeApproval</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
            chainId<span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
            tokenContractAddress<span class="token operator">:</span> tokenAddress<span class="token punctuation">,</span>
            approveAmount<span class="token operator">:</span> rawAmount
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token string">'alreadyApproved'</span> <span class="token keyword">in</span> result<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nToken already approved for the requested amount!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> <span class="token punctuation">{</span> success<span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span> alreadyApproved<span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nApproval completed successfully!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Transaction Hash:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>transactionHash<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>explorerUrl<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> result<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Error executing approval:'</span><span class="token punctuation">,</span> error<span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Run if this file is executed directly</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token keyword">require</span><span class="token punctuation">.</span>main <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Example usage: ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000</span>
    <span class="token keyword">const</span> args <span class="token operator">=</span> process<span class="token punctuation">.</span>argv<span class="token punctuation">.</span><span class="token function">slice</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>args<span class="token punctuation">.</span>length <span class="token operator">!==</span> <span class="token number">2</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Usage: ts-node approval.ts &lt;tokenAddress&gt; &lt;amountToApprove&gt;"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nExamples:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"  # Approve 1000 USDC"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">  ts-node approval.ts 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 1000</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> <span class="token punctuation">[</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">]</span> <span class="token operator">=</span> args<span class="token punctuation">;</span>
    <span class="token function">executeApproval</span><span class="token punctuation">(</span>tokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">)</span>
        <span class="token punctuation">.</span><span class="token function">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
        <span class="token punctuation">.</span><span class="token function">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Error:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
            process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword">export</span> <span class="token punctuation">{</span> executeApproval <span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="5.调用SDK执行兑换" id="5.调用sdk执行兑换">5.调用SDK执行兑换<a class="index_header-anchor__Xqb+L" href="#5.调用sdk执行兑换" style="opacity: 0;">#</a></h2>
<p>创建兑换执行的文件：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// swap.ts</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> client <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Execute a swap from ETH to USDC on Base chain</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_PRIVATE_KEY</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Missing EVM_PRIVATE_KEY in .env file'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// You can change this to any EVM chain</span>
    <span class="token comment">// For example, for Base, use chainId: '8453'</span>
    <span class="token comment">// For example, for baseSepolia, use chainId: '84532'</span>
    <span class="token comment">// You can also use SUI, use chainId: '784'</span>
    <span class="token comment">// When using another Chain, you need to change the fromTokenAddress and toTokenAddress to the correct addresses for that chain</span>

    <span class="token keyword">const</span> swapResult <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span> <span class="token comment">// Base chain ID</span>
      fromTokenAddress<span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// Native ETH</span>
      toTokenAddress<span class="token operator">:</span> <span class="token string">'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'</span><span class="token punctuation">,</span> <span class="token comment">// USDC on Base</span>
      amount<span class="token operator">:</span> <span class="token function">String</span><span class="token punctuation">(</span><span class="token number">10</span> <span class="token operator">*</span> <span class="token number">10</span> <span class="token operator">**</span> <span class="token number">14</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token comment">// .0001 ETH</span>
      slippage<span class="token operator">:</span> <span class="token string">'0.5'</span><span class="token punctuation">,</span> <span class="token comment">// 0.5% slippage</span>
      userWalletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">EVM_WALLET_ADDRESS</span><span class="token operator">!</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Swap executed successfully:'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>swapResult<span class="token punctuation">,</span> <span class="token keyword">null</span><span class="token punctuation">,</span> <span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">return</span> swapResult<span class="token punctuation">;</span>
  <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Error executing swap:'</span><span class="token punctuation">,</span> error<span class="token punctuation">.</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token comment">// API errors include details in the message</span>
      <span class="token keyword">if</span> <span class="token punctuation">(</span>error<span class="token punctuation">.</span>message<span class="token punctuation">.</span><span class="token function">includes</span><span class="token punctuation">(</span><span class="token string">'API Error:'</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> match <span class="token operator">=</span> error<span class="token punctuation">.</span>message<span class="token punctuation">.</span><span class="token function">match</span><span class="token punctuation">(</span><span class="token regex"><span class="token regex-delimiter">/</span><span class="token regex-source language-regex">API Error: <span class="token group punctuation">(</span><span class="token char-set class-name">.</span><span class="token quantifier number">*</span><span class="token group punctuation">)</span></span><span class="token regex-delimiter">/</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>match<span class="token punctuation">)</span> <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'API Error Details:'</span><span class="token punctuation">,</span> match<span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Run if this file is executed directly</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token keyword">require</span><span class="token punctuation">.</span>main <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token function">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">.</span><span class="token function">catch</span><span class="token punctuation">(</span><span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Error:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
      process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword">export</span> <span class="token punctuation">{</span> executeSwap <span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="6.附加的SDK功能" id="6.附加的sdk功能">6.附加的SDK功能<a class="index_header-anchor__Xqb+L" href="#6.附加的sdk功能" style="opacity: 0;">#</a></h2>
<p>SDK提供了简化开发的附加方法：
获取代币对的报价</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    chainId<span class="token operator">:</span> <span class="token string">'8453'</span><span class="token punctuation">,</span>  <span class="token comment">// Base Chain</span>
    fromTokenAddress<span class="token operator">:</span> <span class="token string">'0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
    toTokenAddress<span class="token operator">:</span> <span class="token string">'0x4200000000000000000000000000000000000006'</span><span class="token punctuation">,</span> <span class="token comment">// WETH</span>
    amount<span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span>  <span class="token comment">// 1 USDC (in smallest units)</span>
    slippage<span class="token operator">:</span> <span class="token string">'0.5'</span>     <span class="token comment">// 0.5%</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "搭建兑换应用",
    "在 EVM 链上搭建兑换应用"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "在 Solana 链上搭建兑换应用",
    "在 Solana 链上兑换的高级用法",
    "在 EVM 链上搭建兑换应用",
    "在 Sui 链上搭建兑换应用",
    "在 Ton 链上搭建兑换应用",
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
    "FAQ"
  ],
  "toc": [
    "方法1：API方法",
    "1.设置环境",
    "2.检查授权额度",
    "3.检查授权交易参数并发起授权",
    "4.请求询价接口，拿到询价数据",
    "5.请求兑换接口，发起交易",
    "6. 广播交易",
    "7. 追踪交易",
    "8. 完整实现",
    "方法2：SDK方法",
    "1.安装SDK",
    "2.设置环境",
    "3.初始化客户端",
    "4.调用SDK执行代币授权",
    "5.调用SDK执行兑换",
    "6.附加的SDK功能"
  ]
}
```

</details>
