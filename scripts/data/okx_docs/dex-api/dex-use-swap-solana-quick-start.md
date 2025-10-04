# 在 Solana 链上搭建兑换应用 | 搭建兑换应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-swap-solana-quick-start#2.设置环境  
**抓取时间:** 2025-05-27 05:13:23  
**字数:** 6501

## 导航路径
DEX API > 交易 API > 搭建兑换应用 > 在 Solana 链上搭建兑换应用

## 目录
- 方法1：API方法
- 1.设置环境
- 2.获取兑换数据
- 3.准备交易
- 4. 广播交易
- 5.追踪交易
- 6.完整实现
- 7. MEV保护
- 方法2：SDK方法
- 1.安装SDK
- 2.设置环境
- 3.初始化客户端
- 4.调用SDK执行兑换
- 5.附加SDK功能

---

在 Solana 链上搭建兑换应用
#
在 Solana 上使用OKX DEX构建兑换应用程序有两种方法：
API的方法-直接与OKX DEX API交互
SDK方法-使用
@okx-dex/okx-dex-sdk
简化开发人员体验
本指南涵盖了这两种方法，以帮助你选择最适合你需求的方法。
方法1：API方法
#
在本指南中，我们将提供通过OKX DEX进行Solana代币兑换的用例。
1.设置环境
#
导入必要的Node. js库并设置环境变量：
// Required libraries
import
base58
from
"bs58"
;
import
BN
from
"bn.js"
;
import
*
as
solanaWeb3
from
"@solana/web3.js"
;
import
{
Connection
}
from
"@solana/web3.js"
;
import
cryptoJS
from
"crypto-js"
;
import
axios
from
"axios"
;
import
dotenv
from
'dotenv'
;
dotenv
.
config
(
)
;
// Environment variables
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
const
userAddress
=
process
.
env
.
WALLET_ADDRESS
;
const
userPrivateKey
=
process
.
env
.
PRIVATE_KEY
;
const
solanaRpcUrl
=
process
.
env
.
SOLANA_RPC_URL
;
// Constants
const
SOLANA_CHAIN_ID
=
"501"
;
const
COMPUTE_UNITS
=
300000
;
const
MAX_RETRIES
=
3
;
// Initialize Solana connection
const
connection
=
new
Connection
(
`
${
solanaRpcUrl
}
`
,
{
confirmTransactionInitialTimeout
:
5000
}
)
;
// Utility function for OKX API authentication
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
,
body
=
""
)
{
const
stringToSign
=
timestamp
+
method
+
requestPath
+
(
queryString
||
body
)
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
cryptoJS
.
enc
.
Base64
.
stringify
(
cryptoJS
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
2.获取兑换数据
#
Solana的本机令牌地址11111111111111111111111111111111。使用/swap端点检索详细的兑换信息：
async
function
getSwapData
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
=
'0.5'
)
{
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
"/api/v5/dex/aggregator/swap"
;
const
params
=
{
amount
:
amount
,
chainId
:
SOLANA_CHAIN_ID
,
fromTokenAddress
:
fromTokenAddress
,
toTokenAddress
:
toTokenAddress
,
userWalletAddress
:
userAddress
,
slippage
:
slippage
}
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
try
{
const
response
=
await
axios
.
get
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
!==
"0"
||
!
response
.
data
.
data
?.
[
0
]
)
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
"Failed to get swap data"
}
`
)
;
}
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
catch
(
error
)
{
console
.
error
(
"Error fetching swap data:"
,
error
)
;
throw
error
;
}
}
3.准备交易
#
从 /swap 获得callData后，你需要反序列化并签名交易：
async
function
prepareTransaction
(
callData
:
string
)
{
try
{
// Decode the base58 encoded transaction data
const
decodedTransaction
=
base58
.
decode
(
callData
)
;
// Get the latest blockhash
const
recentBlockHash
=
await
connection
.
getLatestBlockhash
(
)
;
console
.
log
(
"Got blockhash:"
,
recentBlockHash
.
blockhash
)
;
let
tx
;
// Try to deserialize as a versioned transaction first
try
{
tx
=
solanaWeb3
.
VersionedTransaction
.
deserialize
(
decodedTransaction
)
;
console
.
log
(
"Successfully created versioned transaction"
)
;
tx
.
message
.
recentBlockhash
=
recentBlockHash
.
blockhash
;
}
catch
(
e
)
{
// Fall back to legacy transaction if versioned fails
console
.
log
(
"Versioned transaction failed, trying legacy:"
,
e
)
;
tx
=
solanaWeb3
.
Transaction
.
from
(
decodedTransaction
)
;
console
.
log
(
"Successfully created legacy transaction"
)
;
tx
.
recentBlockhash
=
recentBlockHash
.
blockhash
;
}
return
{
transaction
:
tx
,
recentBlockHash
}
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
"Error preparing transaction:"
,
error
)
;
throw
error
;
}
}
async
function
signTransaction
(
tx
:
solanaWeb3
.
Transaction
|
solanaWeb3
.
VersionedTransaction
)
{
if
(
!
userPrivateKey
)
{
throw
new
Error
(
"Private key not found"
)
;
}
const
feePayer
=
solanaWeb3
.
Keypair
.
fromSecretKey
(
base58
.
decode
(
userPrivateKey
)
)
;
if
(
tx
instanceof
solanaWeb3
.
VersionedTransaction
)
{
tx
.
sign
(
[
feePayer
]
)
;
}
else
{
tx
.
partialSign
(
feePayer
)
;
}
}
4. 广播交易
#
4.1 使用
RPC
广播交易
const
txId
=
await
connection
.
sendRawTransaction
(
tx
.
serialize
(
)
)
;
console
.
log
(
'Transaction ID:'
,
txId
)
;
// Wait for confirmation
await
connection
.
confirmTransaction
(
txId
)
;
console
.
log
(
`
Transaction confirmed: https://solscan.io/tx/
${
txId
}
`
)
;
4.2 使用
交易上链 API
广播交易
async
function
broadcastTransaction
(
signedTx
:
solanaWeb3
.
Transaction
|
solanaWeb3
.
VersionedTransaction
)
{
try
{
const
serializedTx
=
signedTx
.
serialize
(
)
;
const
encodedTx
=
base58
.
encode
(
serializedTx
)
;
const
path
=
"dex/pre-transaction/broadcast-transaction"
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
encodedTx
,
chainIndex
:
SOLANA_CHAIN_ID
,
address
:
userAddress
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
""
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
Transaction broadcast successfully, Order ID:
${
orderId
}
`
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
'Failed to broadcast transaction:'
,
error
)
;
throw
error
;
}
}
5.追踪交易
#
使用
交易上链 API
// Define transaction status interface
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
 * Tracking transaction confirmation status using the Onchain gateway API
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
Final transaction confirmation status
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
Tracking transaction with Order ID:
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
SOLANA_CHAIN_ID
,
address
:
userAddress
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
Transaction successful: https://solscan.io/tx/
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
instanceof
Error
?
error
.
message
:
"Unknown error"
)
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
'Transaction tracking timed out'
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
// Default error info
let
errorInfo
:
TxErrorInfo
=
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
// More specific error handling based on the failure reason
if
(
failReason
.
includes
(
'insufficient funds'
)
)
{
errorInfo
=
{
error
:
'INSUFFICIENT_FUNDS'
,
message
:
'Your wallet does not have enough funds to complete this transaction'
,
action
:
'Add more SOL to your wallet to cover the transaction'
}
;
}
else
if
(
failReason
.
includes
(
'blockhash'
)
)
{
errorInfo
=
{
error
:
'BLOCKHASH_EXPIRED'
,
message
:
'The transaction blockhash has expired'
,
action
:
'Try again with a fresh transaction'
}
;
}
else
if
(
failReason
.
includes
(
'compute budget'
)
)
{
errorInfo
=
{
error
:
'COMPUTE_BUDGET_EXCEEDED'
,
message
:
'Transaction exceeded compute budget'
,
action
:
'Increase compute units or simplify the transaction'
}
;
}
return
errorInfo
;
}
详细的兑换信息，我们可以使用 Swap API
/**
 * Track transaction using SWAP API
 *
@param
chainId
- Chain ID (e.g., 501 for Solana)
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
trackTransactionWithSwapAPI
(
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
chainId
:
SOLANA_CHAIN_ID
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
[
0
]
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
Explorer URL: https://solscan.io/tx/
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
instanceof
Error
?
error
.
message
:
"Unknown error"
)
)
;
throw
error
;
}
}
交易上链 API 监控使用 /dex/post-transaction/orders 跟踪内部订单处理状态。它有助于监控交易在 OKX 系统中的移动情况，并提供订单 ID 和基本状态（1：待处理，2：成功，3：失败）。
Swap API 交易跟踪使用 /dex/aggregator/history 提供全面的兑换执行详情。它提供特定于代币的信息（代码、金额）、已支付的费用以及详细的区块链数据。如果您需要完整的兑换验证并提供代币级详细信息，请使用此选项。
选择前者用于基本交易状态更新，而选择后者用于获取兑换执行本身的详细信息。
6.完整实现
#
这是一个完整的实现示例：
// solana-swap.ts
import
base58
from
"bs58"
;
import
BN
from
"bn.js"
;
import
*
as
solanaWeb3
from
"@solana/web3.js"
;
import
{
Connection
}
from
"@solana/web3.js"
;
import
cryptoJS
from
"crypto-js"
;
import
axios
from
"axios"
;
import
dotenv
from
'dotenv'
;
dotenv
.
config
(
)
;
// Environment variables
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
const
userAddress
=
process
.
env
.
WALLET_ADDRESS
;
const
userPrivateKey
=
process
.
env
.
PRIVATE_KEY
;
const
solanaRpcUrl
=
process
.
env
.
SOLANA_RPC_URL
;
// Constants
const
SOLANA_CHAIN_ID
=
"501"
;
// Solana Mainnet
const
COMPUTE_UNITS
=
300000
;
const
MAX_RETRIES
=
3
;
const
CONFIRMATION_TIMEOUT
=
60000
;
const
POLLING_INTERVAL
=
5000
;
const
BASE_URL
=
"https://web3.okx.com"
;
const
DEX_PATH
=
"api/v5/dex"
;
// Initialize Solana connection
const
connection
=
new
Connection
(
solanaRpcUrl
||
"https://api.mainnet-beta.solana.com"
,
{
confirmTransactionInitialTimeout
:
30000
}
)
;
// ======== Utility Functions ========
/**
* Generate API authentication headers
*/
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
,
body
=
""
)
{
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
"Missing required environment variables for API authentication"
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
(
queryString
||
body
)
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
cryptoJS
.
enc
.
Base64
.
stringify
(
cryptoJS
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
/**
* Convert human-readable amount to the smallest token units
*/
function
convertAmount
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
try
{
if
(
!
amount
||
isNaN
(
parseFloat
(
amount
)
)
)
{
throw
new
Error
(
"Invalid amount"
)
;
}
const
value
=
parseFloat
(
amount
)
;
if
(
value
<=
0
)
{
throw
new
Error
(
"Amount must be greater than 0"
)
;
}
return
new
BN
(
value
*
Math
.
pow
(
10
,
decimals
)
)
.
toString
(
)
;
}
catch
(
err
)
{
console
.
error
(
"Amount conversion error:"
,
err
)
;
throw
new
Error
(
"Invalid amount format"
)
;
}
}
/**
* Get token information from the API
*/
async
function
getTokenInfo
(
fromTokenAddress
:
string
,
toTokenAddress
:
string
)
{
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
path
=
`
${
DEX_PATH
}
/aggregator/quote
`
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
params
:
Record
<
string
,
string
>
=
{
chainId
:
SOLANA_CHAIN_ID
,
fromTokenAddress
,
toTokenAddress
,
amount
:
"1000000"
,
// Small amount just to get token info
slippage
:
"0.5"
,
}
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
try
{
const
response
=
await
axios
.
get
(
`
${
BASE_URL
}
${
requestPath
}
${
queryString
}
`
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
!==
"0"
||
!
response
.
data
.
data
?.
[
0
]
)
{
throw
new
Error
(
"Failed to get token information"
)
;
}
const
quoteData
=
response
.
data
.
data
[
0
]
;
return
{
fromToken
:
{
symbol
:
quoteData
.
fromToken
.
tokenSymbol
,
decimals
:
parseInt
(
quoteData
.
fromToken
.
decimal
)
,
price
:
quoteData
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
quoteData
.
toToken
.
tokenSymbol
,
decimals
:
parseInt
(
quoteData
.
toToken
.
decimal
)
,
price
:
quoteData
.
toToken
.
tokenUnitPrice
}
}
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
"Error fetching token information:"
,
error
)
;
throw
error
;
}
}
// ======== Pre-Transaction Functionality ========
/**
* Get swap data from the API
*/
async
function
getSwapData
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
=
'0.5'
)
{
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
path
=
`
${
DEX_PATH
}
/aggregator/swap
`
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
// Ensure all parameters are defined before creating URLSearchParams
const
params
:
Record
<
string
,
string
>
=
{
amount
,
chainId
:
SOLANA_CHAIN_ID
,
fromTokenAddress
,
toTokenAddress
,
slippage
}
;
// Only add userWalletAddress if it's defined
if
(
userAddress
)
{
params
.
userWalletAddress
=
userAddress
;
}
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
try
{
const
response
=
await
axios
.
get
(
`
${
BASE_URL
}
${
requestPath
}
${
queryString
}
`
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
!==
"0"
||
!
response
.
data
.
data
?.
[
0
]
)
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
"Failed to get swap data"
}
`
)
;
}
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
catch
(
error
)
{
console
.
error
(
"Error fetching swap data:"
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
* Prepare the transaction with the latest blockhash and compute units
*/
async
function
prepareTransaction
(
callData
:
string
)
{
try
{
// Decode the base58 encoded transaction data
const
decodedTransaction
=
base58
.
decode
(
callData
)
;
// Get the latest blockhash for transaction freshness
const
recentBlockHash
=
await
connection
.
getLatestBlockhash
(
)
;
console
.
log
(
"Got blockhash:"
,
recentBlockHash
.
blockhash
)
;
let
tx
;
// Try to deserialize as a versioned transaction first (Solana v0 transaction format)
try
{
tx
=
solanaWeb3
.
VersionedTransaction
.
deserialize
(
decodedTransaction
)
;
console
.
log
(
"Successfully created versioned transaction"
)
;
tx
.
message
.
recentBlockhash
=
recentBlockHash
.
blockhash
;
}
catch
(
e
)
{
// Fall back to legacy transaction if versioned fails
console
.
log
(
"Versioned transaction failed, trying legacy format"
)
;
tx
=
solanaWeb3
.
Transaction
.
from
(
decodedTransaction
)
;
console
.
log
(
"Successfully created legacy transaction"
)
;
tx
.
recentBlockhash
=
recentBlockHash
.
blockhash
;
// Add compute budget instruction for complex swaps (only for legacy transactions)
// For versioned transactions, this would already be included in the message
const
computeBudgetIx
=
solanaWeb3
.
ComputeBudgetProgram
.
setComputeUnitLimit
(
{
units
:
COMPUTE_UNITS
}
)
;
tx
.
add
(
computeBudgetIx
)
;
}
return
{
transaction
:
tx
,
recentBlockHash
}
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
"Error preparing transaction:"
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
* Sign the transaction with user's private key
*/
async
function
signTransaction
(
tx
:
solanaWeb3
.
Transaction
|
solanaWeb3
.
VersionedTransaction
)
{
if
(
!
userPrivateKey
)
{
throw
new
Error
(
"Private key not found"
)
;
}
const
feePayer
=
solanaWeb3
.
Keypair
.
fromSecretKey
(
base58
.
decode
(
userPrivateKey
)
)
;
if
(
tx
instanceof
solanaWeb3
.
VersionedTransaction
)
{
tx
.
sign
(
[
feePayer
]
)
;
}
else
{
tx
.
partialSign
(
feePayer
)
;
}
return
tx
;
}
/**
* Broadcast transaction using Onchain gateway API
*/
async
function
broadcastTransaction
(
signedTx
:
solanaWeb3
.
Transaction
|
solanaWeb3
.
VersionedTransaction
)
{
try
{
const
serializedTx
=
signedTx
.
serialize
(
)
;
const
encodedTx
=
base58
.
encode
(
serializedTx
)
;
const
path
=
`
${
DEX_PATH
}
/pre-transaction/broadcast-transaction
`
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
// Ensure all parameters are defined
const
broadcastData
:
Record
<
string
,
string
>
=
{
signedTx
:
encodedTx
,
chainIndex
:
SOLANA_CHAIN_ID
}
;
// Only add address if it's defined
if
(
userAddress
)
{
broadcastData
.
address
=
userAddress
;
}
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
""
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
`
${
BASE_URL
}
${
requestPath
}
`
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
Transaction broadcast successfully, Order ID:
${
orderId
}
`
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
'Failed to broadcast transaction:'
,
error
)
;
throw
error
;
}
}
// ======== Post-Transaction Monitoring ========
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
 * Monitor transaction status using Onchain gateway API
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
POLLING_INTERVAL
,
timeoutMs
:
number
=
CONFIRMATION_TIMEOUT
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
`
${
DEX_PATH
}
/post-transaction/orders
`
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
// Ensure all parameters are defined before creating URLSearchParams
const
params
:
Record
<
string
,
string
>
=
{
orderId
:
orderId
,
chainIndex
:
SOLANA_CHAIN_ID
,
limit
:
'1'
}
;
// Only add address if it's defined
if
(
userAddress
)
{
params
.
address
=
userAddress
;
}
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
`
${
BASE_URL
}
${
requestPath
}
${
queryString
}
`
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
Transaction successful: https://solscan.io/tx/
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
instanceof
Error
?
error
.
message
:
"Unknown error"
)
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
 * error handling with failReason
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
// ======== Main Swap Execution Function ========
/**
* Execute a token swap on Solana
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
any
>
{
try
{
// Validate inputs
if
(
!
userPrivateKey
)
{
throw
new
Error
(
"Missing private key"
)
;
}
if
(
!
userAddress
)
{
throw
new
Error
(
"Missing wallet address"
)
;
}
// Step 1: Get swap data from OKX DEX API
console
.
log
(
"Getting swap data..."
)
;
const
swapData
=
await
getSwapData
(
fromTokenAddress
,
toTokenAddress
,
amount
,
slippage
)
;
console
.
log
(
"Swap route obtained"
)
;
// Step 2: Get the transaction data
const
callData
=
swapData
.
tx
.
data
;
if
(
!
callData
)
{
throw
new
Error
(
"Invalid transaction data received from API"
)
;
}
// Step 3: Prepare the transaction with compute units
const
{
transaction
,
recentBlockHash
}
=
await
prepareTransaction
(
callData
)
;
console
.
log
(
"Transaction prepared with compute unit limit:"
,
COMPUTE_UNITS
)
;
// Step 4: Sign the transaction
const
signedTx
=
await
signTransaction
(
transaction
)
;
console
.
log
(
"Transaction signed"
)
;
// Step 5: Broadcast the transaction using Onchain gateway API
const
orderId
=
await
broadcastTransaction
(
signedTx
)
;
console
.
log
(
`
Transaction broadcast successful with order ID:
${
orderId
}
`
)
;
// Step 6: Monitor the transaction status
console
.
log
(
"Monitoring transaction status..."
)
;
const
txStatus
=
await
trackTransaction
(
orderId
)
;
return
{
success
:
true
,
orderId
,
txHash
:
txStatus
.
txHash
,
status
:
txStatus
.
txStatus
===
'2'
?
'SUCCESS'
:
'PENDING'
}
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
"Error during swap:"
,
error
)
;
return
{
success
:
false
,
error
:
error
instanceof
Error
?
error
.
message
:
"Unknown error"
}
;
}
}
// ======== Command Line Interface ========
async
function
main
(
)
{
try
{
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
<
3
)
{
console
.
log
(
"Usage: ts-node solana-swap.ts <amount> <fromTokenAddress> <toTokenAddress> [<slippage>]"
)
;
console
.
log
(
"Example: ts-node solana-swap.ts 0.1 11111111111111111111111111111111 EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 0.5"
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
amountStr
,
fromTokenAddress
,
toTokenAddress
,
slippage
=
'0.5'
]
=
args
;
// Get token information
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
getTokenInfo
(
fromTokenAddress
,
toTokenAddress
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
(
${
tokenInfo
.
fromToken
.
decimals
}
decimals)
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
(
${
tokenInfo
.
toToken
.
decimals
}
decimals)
`
)
;
// Convert amount using fetched decimals
const
rawAmount
=
convertAmount
(
amountStr
,
tokenInfo
.
fromToken
.
decimals
)
;
console
.
log
(
`
Amount in
${
tokenInfo
.
fromToken
.
symbol
}
base units:
`
,
rawAmount
)
;
// Execute swap
console
.
log
(
"\nExecuting swap..."
)
;
const
result
=
await
executeSwap
(
fromTokenAddress
,
toTokenAddress
,
rawAmount
,
slippage
)
;
if
(
result
.
success
)
{
console
.
log
(
"\nSwap completed successfully!"
)
;
console
.
log
(
"Order ID:"
,
result
.
orderId
)
;
if
(
result
.
txHash
)
{
console
.
log
(
"Transaction ID:"
,
result
.
txHash
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
result
.
txHash
}
`
)
;
}
}
else
{
console
.
error
(
"\nSwap failed:"
,
result
.
error
)
;
}
process
.
exit
(
result
.
success
?
0
:
1
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
"Error:"
,
error
instanceof
Error
?
error
.
message
:
"Unknown error"
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
}
// Execute main function if run directly
if
(
require
.
main
===
module
)
{
main
(
)
;
}
// Export functions for modular usage
export
{
executeSwap
,
broadcastTransaction
,
trackTransaction
,
prepareTransaction
}
;
7. MEV保护
#
Solana交易存在MEV（最大可提取价值）风险。虽然MEV保护不直接包含在SDK中，但您可以使用API优先的方法自行实施。
第一道防线使用动态优先级费用-将其视为您在拍卖中对抗MEV机器人的出价。
const
MEV_PROTECTION
=
{
// Trade Protection
MAX_PRICE_IMPACT
:
"0.05"
,
// 5% max price impact
SLIPPAGE
:
"0.05"
,
// 5% slippage tolerance
MIN_ROUTES
:
2
,
// Minimum DEX routes
// Priority Fees
MIN_PRIORITY_FEE
:
10_000
,
MAX_PRIORITY_FEE
:
1_000_000
,
PRIORITY_MULTIPLIER
:
2
,
// TWAP Settings
TWAP_ENABLED
:
true
,
TWAP_INTERVALS
:
4
,
// Split into 4 parts
TWAP_DELAY_MS
:
2000
,
// 2s between trades
// Transaction Settings
COMPUTE_UNITS
:
300_000
,
MAX_RETRIES
:
3
,
CONFIRMATION_TIMEOUT
:
60_000
,
// Block Targeting
TARGET_SPECIFIC_BLOCKS
:
true
,
PREFERRED_SLOT_OFFSET
:
2
,
// Target blocks with slot % 4 == 2
}
as
const
;
static
async
getPriorityFee
(
)
{
const
recentFees
=
await
connection
.
getRecentPrioritizationFees
(
)
;
const
maxFee
=
Math
.
max
(
...
recentFees
.
map
(
fee
=>
fee
.
prioritizationFee
)
)
;
return
Math
.
min
(
maxFee
*
1.5
,
MEV_PROTECTION
.
MAX_PRIORITY_FEE
)
;
}
对于较大的交易，您可以启用TWAP（时间加权平均价格）。您的交易将被分成更小的部分，而不是MEV机器人喜欢瞄准的一个大的飞溅。
// Define the TWAPExecution class outside of the if block
class
TWAPExecution
{
static
async
splitTrade
(
totalAmount
:
string
,
fromTokenAddress
:
string
,
toTokenAddress
:
string
)
:
Promise
<
TradeChunk
[
]
>
{
const
amount
=
new
BN
(
totalAmount
)
;
const
chunkSize
=
amount
.
divn
(
MEV_PROTECTION
.
TWAP_INTERVALS
)
;
return
Array
(
MEV_PROTECTION
.
TWAP_INTERVALS
)
.
fill
(
null
)
.
map
(
(
)
=>
(
{
amount
:
chunkSize
.
toString
(
)
,
fromTokenAddress
,
toTokenAddress
,
minAmountOut
:
"0"
// Will be calculated per chunk
}
)
)
;
}
}
// Then use it in the if block
if
(
MEV_PROTECTION
.
TWAP_ENABLED
)
{
const
chunks
=
await
TWAPExecution
.
splitTrade
(
rawAmount
,
fromTokenAddress
,
toTokenAddress
)
;
}
运行中防护
#
当您使用
此实现
执行交易时，会发生几件事情：
交易前检查：
购买的代币会被检查是否存在貔貅盘特征
检查你的网络费用来设置有竞争力的优先费用
查看你的交易额度来确认是否要拆单
在交易期间：
大额交易将拆分成不同金额的单子，并在随机时间发出
每单将根据市场条件设置优先费用
特定的区块来减少暴露风险
交易的安全性保障：
每笔交易都将进行预执行模拟
对区块确认状态进行内置的追踪
出现问题自动重试逻辑
虽然Solana上的MEV不能完全消除，但这些保护措施使MEV机器人的生活更加困难。
方法2：SDK方法
#
使用OKX DEXSDK提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为您处理许多实现细节，包括重试逻辑、错误处理和事务管理。
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
# Solana Configuration
SOLANA_RPC_URL
=
your_solana_rpc_url
SOLANA_WALLET_ADDRESS
=
your_solana_wallet_address
SOLANA_PRIVATE_KEY
=
your_solana_private_key
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
'SOLANA_WALLET_ADDRESS'
,
'SOLANA_PRIVATE_KEY'
,
'SOLANA_RPC_URL'
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
wsEndpoint
:
process
.
env
.
SOLANA_WS_URL
,
confirmTransactionInitialTimeout
:
5000
}
,
walletAddress
:
process
.
env
.
SOLANA_WALLET_ADDRESS
!
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
computeUnits
:
300000
,
maxRetries
:
3
}
}
)
;
4.调用SDK执行兑换
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
5.附加SDK功能
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

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="在-solana-链上搭建兑换应用">在 Solana 链上搭建兑换应用<a class="index_header-anchor__Xqb+L" href="#在-solana-链上搭建兑换应用" style="opacity:0">#</a></h1>
<p>在 Solana 上使用OKX DEX构建兑换应用程序有两种方法：</p>
<ol>
<li>API的方法-直接与OKX DEX API交互</li>
<li>SDK方法-使用 <code>@okx-dex/okx-dex-sdk</code>简化开发人员体验</li>
</ol>
<p>本指南涵盖了这两种方法，以帮助你选择最适合你需求的方法。</p>
<h2 data-content="方法1：API方法" id="方法1：api方法">方法1：API方法<a class="index_header-anchor__Xqb+L" href="#方法1：api方法" style="opacity:0">#</a></h2>
<p>在本指南中，我们将提供通过OKX DEX进行Solana代币兑换的用例。</p>
<h2 data-content="1.设置环境" id="1.设置环境">1.设置环境<a class="index_header-anchor__Xqb+L" href="#1.设置环境" style="opacity:0">#</a></h2>
<p>导入必要的Node. js库并设置环境变量：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Required libraries</span>
<span class="token keyword">import</span> base58 <span class="token keyword">from</span> <span class="token string">"bs58"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token constant">BN</span> <span class="token keyword">from</span> <span class="token string">"bn.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token operator">*</span> <span class="token keyword">as</span> solanaWeb3 <span class="token keyword">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> Connection <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> cryptoJS <span class="token keyword">from</span> <span class="token string">"crypto-js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> axios <span class="token keyword">from</span> <span class="token string">"axios"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> dotenv <span class="token keyword">from</span> <span class="token string">'dotenv'</span><span class="token punctuation">;</span>

dotenv<span class="token punctuation">.</span><span class="token function">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Environment variables</span>
<span class="token keyword">const</span> apiKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> secretKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> projectId <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userAddress <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userPrivateKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">PRIVATE_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> solanaRpcUrl <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span><span class="token punctuation">;</span>

<span class="token comment">// Constants</span>
<span class="token keyword">const</span> <span class="token constant">SOLANA_CHAIN_ID</span> <span class="token operator">=</span> <span class="token string">"501"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">COMPUTE_UNITS</span> <span class="token operator">=</span> <span class="token number">300000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">MAX_RETRIES</span> <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">;</span>

<span class="token comment">// Initialize Solana connection</span>
<span class="token keyword">const</span> connection <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Connection</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>solanaRpcUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    confirmTransactionInitialTimeout<span class="token operator">:</span> <span class="token number">5000</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Utility function for OKX API authentication</span>
<span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> method<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> requestPath<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">,</span> body <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>

    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> <span class="token punctuation">(</span>queryString <span class="token operator">||</span> body<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span>enc<span class="token punctuation">.</span>Base64<span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>
            cryptoJS<span class="token punctuation">.</span><span class="token function">HmacSHA256</span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="2.获取兑换数据" id="2.获取兑换数据">2.获取兑换数据<a class="index_header-anchor__Xqb+L" href="#2.获取兑换数据" style="opacity:0">#</a></h2>
<p>Solana的本机令牌地址11111111111111111111111111111111。使用/swap端点检索详细的兑换信息：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapData</span><span class="token punctuation">(</span>
    fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> 
    toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> 
    amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> 
    slippage <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token string">"/api/v5/dex/aggregator/swap"</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        amount<span class="token operator">:</span> amount<span class="token punctuation">,</span>
        chainId<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token operator">:</span> fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token operator">:</span> toTokenAddress<span class="token punctuation">,</span>
        userWalletAddress<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
        slippage<span class="token operator">:</span> slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>
            <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>queryString<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span> headers <span class="token punctuation">}</span>
        <span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">!==</span> <span class="token string">"0"</span> <span class="token operator">||</span> <span class="token operator">!</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">"Failed to get swap data"</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error fetching swap data:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="3.准备交易" id="3.准备交易">3.准备交易<a class="index_header-anchor__Xqb+L" href="#3.准备交易" style="opacity:0">#</a></h2>
<p>从 /swap 获得callData后，你需要反序列化并签名交易：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">prepareTransaction</span><span class="token punctuation">(</span>callData<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// Decode the base58 encoded transaction data</span>
        <span class="token keyword">const</span> decodedTransaction <span class="token operator">=</span> base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>callData<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Get the latest blockhash</span>
        <span class="token keyword">const</span> recentBlockHash <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">getLatestBlockhash</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Got blockhash:"</span><span class="token punctuation">,</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">let</span> tx<span class="token punctuation">;</span>
        
        <span class="token comment">// Try to deserialize as a versioned transaction first</span>
        <span class="token keyword">try</span> <span class="token punctuation">{</span>
            tx <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">.</span><span class="token function">deserialize</span><span class="token punctuation">(</span>decodedTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Successfully created versioned transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx<span class="token punctuation">.</span>message<span class="token punctuation">.</span>recentBlockhash <span class="token operator">=</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token comment">// Fall back to legacy transaction if versioned fails</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Versioned transaction failed, trying legacy:"</span><span class="token punctuation">,</span> e<span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>Transaction<span class="token punctuation">.</span><span class="token function">from</span><span class="token punctuation">(</span>decodedTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Successfully created legacy transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx<span class="token punctuation">.</span>recentBlockhash <span class="token operator">=</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            transaction<span class="token operator">:</span> tx<span class="token punctuation">,</span>
            recentBlockHash
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error preparing transaction:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">signTransaction</span><span class="token punctuation">(</span>tx<span class="token operator">:</span> solanaWeb3<span class="token punctuation">.</span>Transaction <span class="token operator">|</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>userPrivateKey<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Private key not found"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    
    <span class="token keyword">const</span> feePayer <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>Keypair<span class="token punctuation">.</span><span class="token function">fromSecretKey</span><span class="token punctuation">(</span>
        base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>userPrivateKey<span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    
    <span class="token keyword">if</span> <span class="token punctuation">(</span>tx <span class="token keyword">instanceof</span> <span class="token class-name">solanaWeb3</span><span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        tx<span class="token punctuation">.</span><span class="token function">sign</span><span class="token punctuation">(</span><span class="token punctuation">[</span>feePayer<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        tx<span class="token punctuation">.</span><span class="token function">partialSign</span><span class="token punctuation">(</span>feePayer<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="4. 广播交易" id="4.-广播交易">4. 广播交易<a class="index_header-anchor__Xqb+L" href="#4.-广播交易" style="opacity:0">#</a></h2>
<p>4.1 使用 <code>RPC</code> 广播交易</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> txId <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">sendRawTransaction</span><span class="token punctuation">(</span>tx<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'Transaction ID:'</span><span class="token punctuation">,</span> txId<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token comment">// Wait for confirmation</span>
    <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">confirmTransaction</span><span class="token punctuation">(</span>txId<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction confirmed: https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>4.2 使用<code>交易上链 API</code>广播交易</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">broadcastTransaction</span><span class="token punctuation">(</span>
    signedTx<span class="token operator">:</span> solanaWeb3<span class="token punctuation">.</span>Transaction <span class="token operator">|</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction
<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> serializedTx <span class="token operator">=</span> signedTx<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> encodedTx <span class="token operator">=</span> base58<span class="token punctuation">.</span><span class="token function">encode</span><span class="token punctuation">(</span>serializedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">"dex/pre-transaction/broadcast-transaction"</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
        
        <span class="token keyword">const</span> broadcastData <span class="token operator">=</span> <span class="token punctuation">{</span>
            signedTx<span class="token operator">:</span> encodedTx<span class="token punctuation">,</span>
            chainIndex<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
            address<span class="token operator">:</span> userAddress
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Prepare authentication with body included in signature</span>
        <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>broadcastData<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> <span class="token string">""</span><span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> broadcastData<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> orderId <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orderId<span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction broadcast successfully, Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> orderId<span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to broadcast transaction:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="5.追踪交易" id="5.追踪交易">5.追踪交易<a class="index_header-anchor__Xqb+L" href="#5.追踪交易" style="opacity:0">#</a></h2>
<p>使用<code>交易上链 API</code></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Define transaction status interface</span>
<span class="token keyword">interface</span> <span class="token class-name">TxErrorInfo</span> <span class="token punctuation">{</span>
    error<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    action<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Tracking transaction confirmation status using the Onchain gateway API
 * <span class="token keyword">@param</span> <span class="token parameter">orderId</span> - Order ID from broadcast response
 * <span class="token keyword">@param</span> <span class="token parameter">intervalMs</span> - Polling interval in milliseconds
 * <span class="token keyword">@param</span> <span class="token parameter">timeoutMs</span> - Maximum time to wait
 * <span class="token keyword">@returns</span> Final transaction confirmation status
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>
    orderId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    intervalMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">5000</span><span class="token punctuation">,</span>
    timeoutMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token number">300000</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Tracking transaction with Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> startTime <span class="token operator">=</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">let</span> lastStatus <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>

    <span class="token keyword">while</span> <span class="token punctuation">(</span>Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span> startTime <span class="token operator">&lt;</span> timeoutMs<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token comment">// Get transaction status</span>
        <span class="token keyword">try</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/post-transaction/orders'</span><span class="token punctuation">;</span>
            <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

            <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
                orderId<span class="token operator">:</span> orderId<span class="token punctuation">,</span>
                chainIndex<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
                address<span class="token operator">:</span> userAddress<span class="token punctuation">,</span>
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
                            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful: https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">warn</span><span class="token punctuation">(</span><span class="token string">'Error checking transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span>message <span class="token operator">:</span> <span class="token string">"Unknown error"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token comment">// Wait before next check</span>
        <span class="token keyword">await</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token builtin">Promise</span></span><span class="token punctuation">(</span>resolve <span class="token operator">=&gt;</span> <span class="token function">setTimeout</span><span class="token punctuation">(</span>resolve<span class="token punctuation">,</span> intervalMs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Transaction tracking timed out'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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

    <span class="token comment">// Default error info</span>
    <span class="token keyword">let</span> errorInfo<span class="token operator">:</span> TxErrorInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
        error<span class="token operator">:</span> <span class="token string">'TRANSACTION_FAILED'</span><span class="token punctuation">,</span>
        message<span class="token operator">:</span> failReason<span class="token punctuation">,</span>
        action<span class="token operator">:</span> <span class="token string">'Try again or contact support'</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>

    <span class="token comment">// More specific error handling based on the failure reason</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>failReason<span class="token punctuation">.</span><span class="token function">includes</span><span class="token punctuation">(</span><span class="token string">'insufficient funds'</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        errorInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
            error<span class="token operator">:</span> <span class="token string">'INSUFFICIENT_FUNDS'</span><span class="token punctuation">,</span>
            message<span class="token operator">:</span> <span class="token string">'Your wallet does not have enough funds to complete this transaction'</span><span class="token punctuation">,</span>
            action<span class="token operator">:</span> <span class="token string">'Add more SOL to your wallet to cover the transaction'</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>failReason<span class="token punctuation">.</span><span class="token function">includes</span><span class="token punctuation">(</span><span class="token string">'blockhash'</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        errorInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
            error<span class="token operator">:</span> <span class="token string">'BLOCKHASH_EXPIRED'</span><span class="token punctuation">,</span>
            message<span class="token operator">:</span> <span class="token string">'The transaction blockhash has expired'</span><span class="token punctuation">,</span>
            action<span class="token operator">:</span> <span class="token string">'Try again with a fresh transaction'</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>failReason<span class="token punctuation">.</span><span class="token function">includes</span><span class="token punctuation">(</span><span class="token string">'compute budget'</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        errorInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
            error<span class="token operator">:</span> <span class="token string">'COMPUTE_BUDGET_EXCEEDED'</span><span class="token punctuation">,</span>
            message<span class="token operator">:</span> <span class="token string">'Transaction exceeded compute budget'</span><span class="token punctuation">,</span>
            action<span class="token operator">:</span> <span class="token string">'Increase compute units or simplify the transaction'</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token keyword">return</span> errorInfo<span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>详细的兑换信息，我们可以使用 Swap API</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token doc-comment comment">/**
 * Track transaction using SWAP API
 * <span class="token keyword">@param</span> <span class="token parameter">chainId</span> - Chain ID (e.g., 501 for Solana)
 * <span class="token keyword">@param</span> <span class="token parameter">txHash</span> - Transaction hash
 * <span class="token keyword">@returns</span> Transaction details
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransactionWithSwapAPI</span><span class="token punctuation">(</span>
    txHash<span class="token operator">:</span> <span class="token builtin">string</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token string">'dex/aggregator/history'</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://web3.okx.com/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>

        <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
            chainId<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
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
            <span class="token keyword">const</span> txData <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
            <span class="token keyword">const</span> status <span class="token operator">=</span> txData<span class="token punctuation">.</span>status<span class="token punctuation">;</span>

            <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'pending'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction is still pending: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">return</span> <span class="token punctuation">{</span> status<span class="token operator">:</span> <span class="token string">'pending'</span><span class="token punctuation">,</span> details<span class="token operator">:</span> txData <span class="token punctuation">}</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token punctuation">(</span>status <span class="token operator">===</span> <span class="token string">'success'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful!</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">From: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>fromTokenDetails<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> - Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>fromTokenDetails<span class="token punctuation">.</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">To: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>toTokenDetails<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> - Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>toTokenDetails<span class="token punctuation">.</span>amount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction Fee: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txFee<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Explorer URL: https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to track transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span>message <span class="token operator">:</span> <span class="token string">"Unknown error"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>交易上链 API 监控使用 /dex/post-transaction/orders 跟踪内部订单处理状态。它有助于监控交易在 OKX 系统中的移动情况，并提供订单 ID 和基本状态（1：待处理，2：成功，3：失败）。</p>
<p>Swap API 交易跟踪使用 /dex/aggregator/history 提供全面的兑换执行详情。它提供特定于代币的信息（代码、金额）、已支付的费用以及详细的区块链数据。如果您需要完整的兑换验证并提供代币级详细信息，请使用此选项。</p>
<p>选择前者用于基本交易状态更新，而选择后者用于获取兑换执行本身的详细信息。</p>
<h2 data-content="6.完整实现" id="6.完整实现">6.完整实现<a class="index_header-anchor__Xqb+L" href="#6.完整实现" style="opacity:0">#</a></h2>
<p>这是一个完整的实现示例：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// solana-swap.ts</span>
<span class="token keyword">import</span> base58 <span class="token keyword">from</span> <span class="token string">"bs58"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token constant">BN</span> <span class="token keyword">from</span> <span class="token string">"bn.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token operator">*</span> <span class="token keyword">as</span> solanaWeb3 <span class="token keyword">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> Connection <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> cryptoJS <span class="token keyword">from</span> <span class="token string">"crypto-js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> axios <span class="token keyword">from</span> <span class="token string">"axios"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> dotenv <span class="token keyword">from</span> <span class="token string">'dotenv'</span><span class="token punctuation">;</span>

dotenv<span class="token punctuation">.</span><span class="token function">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// Environment variables</span>
<span class="token keyword">const</span> apiKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> secretKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> projectId <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userAddress <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userPrivateKey <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">PRIVATE_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> solanaRpcUrl <span class="token operator">=</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span><span class="token punctuation">;</span>

<span class="token comment">// Constants</span>
<span class="token keyword">const</span> <span class="token constant">SOLANA_CHAIN_ID</span> <span class="token operator">=</span> <span class="token string">"501"</span><span class="token punctuation">;</span>  <span class="token comment">// Solana Mainnet</span>
<span class="token keyword">const</span> <span class="token constant">COMPUTE_UNITS</span> <span class="token operator">=</span> <span class="token number">300000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">MAX_RETRIES</span> <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">CONFIRMATION_TIMEOUT</span> <span class="token operator">=</span> <span class="token number">60000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">POLLING_INTERVAL</span> <span class="token operator">=</span> <span class="token number">5000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">BASE_URL</span> <span class="token operator">=</span> <span class="token string">"https://web3.okx.com"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">DEX_PATH</span> <span class="token operator">=</span> <span class="token string">"api/v5/dex"</span><span class="token punctuation">;</span>

<span class="token comment">// Initialize Solana connection</span>
<span class="token keyword">const</span> connection <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Connection</span><span class="token punctuation">(</span>solanaRpcUrl <span class="token operator">||</span> <span class="token string">"https://api.mainnet-beta.solana.com"</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    confirmTransactionInitialTimeout<span class="token operator">:</span> <span class="token number">30000</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// ======== Utility Functions ========</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Generate API authentication headers</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> method<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> requestPath<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">,</span> body <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>apiKey <span class="token operator">||</span> <span class="token operator">!</span>secretKey <span class="token operator">||</span> <span class="token operator">!</span>apiPassphrase <span class="token operator">||</span> <span class="token operator">!</span>projectId<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing required environment variables for API authentication"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    
    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> <span class="token punctuation">(</span>queryString <span class="token operator">||</span> body<span class="token punctuation">)</span><span class="token punctuation">;</span>
    
    <span class="token keyword">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span>enc<span class="token punctuation">.</span>Base64<span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>
            cryptoJS<span class="token punctuation">.</span><span class="token function">HmacSHA256</span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Convert human-readable amount to the smallest token units</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">function</span> <span class="token function">convertAmount</span><span class="token punctuation">(</span>amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> decimals<span class="token operator">:</span> <span class="token builtin">number</span><span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>amount <span class="token operator">||</span> <span class="token function">isNaN</span><span class="token punctuation">(</span><span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">const</span> value <span class="token operator">=</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>value <span class="token operator">&lt;=</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Amount must be greater than 0"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">return</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token constant">BN</span></span><span class="token punctuation">(</span>value <span class="token operator">*</span> Math<span class="token punctuation">.</span><span class="token function">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>err<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Amount conversion error:"</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount format"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Get token information from the API</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getTokenInfo</span><span class="token punctuation">(</span>fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span> toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">DEX_PATH</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">/aggregator/quote</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    
    <span class="token keyword">const</span> params<span class="token operator">:</span> Record<span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token punctuation">,</span> <span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
        chainId<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token punctuation">,</span>
        amount<span class="token operator">:</span> <span class="token string">"1000000"</span><span class="token punctuation">,</span> <span class="token comment">// Small amount just to get token info</span>
        slippage<span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
    
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>
            <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">BASE_URL</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>queryString<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span> headers <span class="token punctuation">}</span>
        <span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">!==</span> <span class="token string">"0"</span> <span class="token operator">||</span> <span class="token operator">!</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Failed to get token information"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">const</span> quoteData <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
        
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            fromToken<span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token builtin">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenSymbol<span class="token punctuation">,</span>
                decimals<span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimal<span class="token punctuation">)</span><span class="token punctuation">,</span>
                price<span class="token operator">:</span> quoteData<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenUnitPrice
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            toToken<span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token builtin">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>tokenSymbol<span class="token punctuation">,</span>
                decimals<span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>decimal<span class="token punctuation">)</span><span class="token punctuation">,</span>
                price<span class="token operator">:</span> quoteData<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>tokenUnitPrice
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error fetching token information:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// ======== Pre-Transaction Functionality ========</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Get swap data from the API</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getSwapData</span><span class="token punctuation">(</span>
    fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    slippage <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">DEX_PATH</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">/aggregator/swap</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
    
    <span class="token comment">// Ensure all parameters are defined before creating URLSearchParams</span>
    <span class="token keyword">const</span> params<span class="token operator">:</span> Record<span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token punctuation">,</span> <span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
        amount<span class="token punctuation">,</span>
        chainId<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token punctuation">,</span>
        slippage
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    
    <span class="token comment">// Only add userWalletAddress if it's defined</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span>userAddress<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        params<span class="token punctuation">.</span>userWalletAddress <span class="token operator">=</span> userAddress<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
    
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>
            <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">BASE_URL</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>queryString<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span> headers <span class="token punctuation">}</span>
        <span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">!==</span> <span class="token string">"0"</span> <span class="token operator">||</span> <span class="token operator">!</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">"Failed to get swap data"</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">return</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error fetching swap data:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Prepare the transaction with the latest blockhash and compute units</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">prepareTransaction</span><span class="token punctuation">(</span>callData<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// Decode the base58 encoded transaction data</span>
        <span class="token keyword">const</span> decodedTransaction <span class="token operator">=</span> base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>callData<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Get the latest blockhash for transaction freshness</span>
        <span class="token keyword">const</span> recentBlockHash <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">getLatestBlockhash</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Got blockhash:"</span><span class="token punctuation">,</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">let</span> tx<span class="token punctuation">;</span>
        
        <span class="token comment">// Try to deserialize as a versioned transaction first (Solana v0 transaction format)</span>
        <span class="token keyword">try</span> <span class="token punctuation">{</span>
            tx <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">.</span><span class="token function">deserialize</span><span class="token punctuation">(</span>decodedTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Successfully created versioned transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx<span class="token punctuation">.</span>message<span class="token punctuation">.</span>recentBlockhash <span class="token operator">=</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token comment">// Fall back to legacy transaction if versioned fails</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Versioned transaction failed, trying legacy format"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>Transaction<span class="token punctuation">.</span><span class="token function">from</span><span class="token punctuation">(</span>decodedTransaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Successfully created legacy transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            tx<span class="token punctuation">.</span>recentBlockhash <span class="token operator">=</span> recentBlockHash<span class="token punctuation">.</span>blockhash<span class="token punctuation">;</span>
            
            <span class="token comment">// Add compute budget instruction for complex swaps (only for legacy transactions)</span>
            <span class="token comment">// For versioned transactions, this would already be included in the message</span>
            <span class="token keyword">const</span> computeBudgetIx <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>ComputeBudgetProgram<span class="token punctuation">.</span><span class="token function">setComputeUnitLimit</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
                units<span class="token operator">:</span> <span class="token constant">COMPUTE_UNITS</span>
            <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            
            tx<span class="token punctuation">.</span><span class="token function">add</span><span class="token punctuation">(</span>computeBudgetIx<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            transaction<span class="token operator">:</span> tx<span class="token punctuation">,</span>
            recentBlockHash
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error preparing transaction:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Sign the transaction with user's private key</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">signTransaction</span><span class="token punctuation">(</span>tx<span class="token operator">:</span> solanaWeb3<span class="token punctuation">.</span>Transaction <span class="token operator">|</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>userPrivateKey<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Private key not found"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    
    <span class="token keyword">const</span> feePayer <span class="token operator">=</span> solanaWeb3<span class="token punctuation">.</span>Keypair<span class="token punctuation">.</span><span class="token function">fromSecretKey</span><span class="token punctuation">(</span>
        base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>userPrivateKey<span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    
    <span class="token keyword">if</span> <span class="token punctuation">(</span>tx <span class="token keyword">instanceof</span> <span class="token class-name">solanaWeb3</span><span class="token punctuation">.</span>VersionedTransaction<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        tx<span class="token punctuation">.</span><span class="token function">sign</span><span class="token punctuation">(</span><span class="token punctuation">[</span>feePayer<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
        tx<span class="token punctuation">.</span><span class="token function">partialSign</span><span class="token punctuation">(</span>feePayer<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    
    <span class="token keyword">return</span> tx<span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Broadcast transaction using Onchain gateway API</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">broadcastTransaction</span><span class="token punctuation">(</span>
    signedTx<span class="token operator">:</span> solanaWeb3<span class="token punctuation">.</span>Transaction <span class="token operator">|</span> solanaWeb3<span class="token punctuation">.</span>VersionedTransaction
<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> serializedTx <span class="token operator">=</span> signedTx<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> encodedTx <span class="token operator">=</span> base58<span class="token punctuation">.</span><span class="token function">encode</span><span class="token punctuation">(</span>serializedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">DEX_PATH</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">/pre-transaction/broadcast-transaction</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
        
        <span class="token comment">// Ensure all parameters are defined</span>
        <span class="token keyword">const</span> broadcastData<span class="token operator">:</span> Record<span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token punctuation">,</span> <span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
            signedTx<span class="token operator">:</span> encodedTx<span class="token punctuation">,</span>
            chainIndex<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Only add address if it's defined</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>userAddress<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            broadcastData<span class="token punctuation">.</span>address <span class="token operator">=</span> userAddress<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token comment">// Prepare authentication with body included in signature</span>
        <span class="token keyword">const</span> bodyString <span class="token operator">=</span> <span class="token constant">JSON</span><span class="token punctuation">.</span><span class="token function">stringify</span><span class="token punctuation">(</span>broadcastData<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'POST'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> <span class="token string">""</span><span class="token punctuation">,</span> bodyString<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">post</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">BASE_URL</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> broadcastData<span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>code <span class="token operator">===</span> <span class="token string">'0'</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> orderId <span class="token operator">=</span> response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>orderId<span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction broadcast successfully, Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> orderId<span class="token punctuation">;</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">API Error: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>response<span class="token punctuation">.</span>data<span class="token punctuation">.</span>msg <span class="token operator">||</span> <span class="token string">'Unknown error'</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">'Failed to broadcast transaction:'</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">throw</span> error<span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// ======== Post-Transaction Monitoring ========</span>

<span class="token comment">// Define error info interface</span>
<span class="token class-name"><span class="token keyword">interface</span></span> TxErrorInfo <span class="token punctuation">{</span>
    error<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    message<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    action<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * Monitor transaction status using Onchain gateway API
 * <span class="token keyword">@param</span> <span class="token parameter">orderId</span> - Order ID from broadcast response
 * <span class="token keyword">@param</span> <span class="token parameter">intervalMs</span> - Polling interval in milliseconds
 * <span class="token keyword">@param</span> <span class="token parameter">timeoutMs</span> - Maximum time to wait
 * <span class="token keyword">@returns</span> Final transaction status
 */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>
    orderId<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    intervalMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token constant">POLLING_INTERVAL</span><span class="token punctuation">,</span>
    timeoutMs<span class="token operator">:</span> <span class="token builtin">number</span> <span class="token operator">=</span> <span class="token constant">CONFIRMATION_TIMEOUT</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Monitoring transaction with Order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> startTime <span class="token operator">=</span> Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">let</span> lastStatus <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>

    <span class="token keyword">while</span> <span class="token punctuation">(</span>Date<span class="token punctuation">.</span><span class="token function">now</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span> startTime <span class="token operator">&lt;</span> timeoutMs<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token comment">// Get transaction status</span>
        <span class="token keyword">try</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> path <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">DEX_PATH</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">/post-transaction/orders</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
            <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">/api/v5/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>path<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
            
            <span class="token comment">// Ensure all parameters are defined before creating URLSearchParams</span>
            <span class="token keyword">const</span> params<span class="token operator">:</span> Record<span class="token operator">&lt;</span><span class="token builtin">string</span><span class="token punctuation">,</span> <span class="token builtin">string</span><span class="token operator">&gt;</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
                orderId<span class="token operator">:</span> orderId<span class="token punctuation">,</span>
                chainIndex<span class="token operator">:</span> <span class="token constant">SOLANA_CHAIN_ID</span><span class="token punctuation">,</span>
                limit<span class="token operator">:</span> <span class="token string">'1'</span>
            <span class="token punctuation">}</span><span class="token punctuation">;</span>
            
            <span class="token comment">// Only add address if it's defined</span>
            <span class="token keyword">if</span> <span class="token punctuation">(</span>userAddress<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                params<span class="token punctuation">.</span>address <span class="token operator">=</span> userAddress<span class="token punctuation">;</span>
            <span class="token punctuation">}</span>

            <span class="token comment">// Prepare authentication</span>
            <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">'GET'</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>

            <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword">await</span> axios<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token constant">BASE_URL</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>requestPath<span class="token interpolation-punctuation punctuation">}</span></span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>queryString<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> <span class="token punctuation">{</span> headers <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            
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
                            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction successful: https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txData<span class="token punctuation">.</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">warn</span><span class="token punctuation">(</span><span class="token string">'Error checking transaction status:'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span>message <span class="token operator">:</span> <span class="token string">"Unknown error"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token comment">// Wait before next check</span>
        <span class="token keyword">await</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token builtin">Promise</span></span><span class="token punctuation">(</span>resolve <span class="token operator">=&gt;</span> <span class="token function">setTimeout</span><span class="token punctuation">(</span>resolve<span class="token punctuation">,</span> intervalMs<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>

    <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Transaction monitoring timed out'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token doc-comment comment">/**
 * error handling with failReason
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

<span class="token comment">// ======== Main Swap Execution Function ========</span>

<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Execute a token swap on Solana</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span>
    fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    amount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
    slippage<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">=</span> <span class="token string">'0.5'</span>
<span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span><span class="token builtin">any</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token comment">// Validate inputs</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>userPrivateKey<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing private key"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>userAddress<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing wallet address"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token comment">// Step 1: Get swap data from OKX DEX API</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Getting swap data..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> swapData <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getSwapData</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">,</span> amount<span class="token punctuation">,</span> slippage<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Swap route obtained"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token comment">// Step 2: Get the transaction data</span>
        <span class="token keyword">const</span> callData <span class="token operator">=</span> swapData<span class="token punctuation">.</span>tx<span class="token punctuation">.</span>data<span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>callData<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid transaction data received from API"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token comment">// Step 3: Prepare the transaction with compute units</span>
        <span class="token keyword">const</span> <span class="token punctuation">{</span> transaction<span class="token punctuation">,</span> recentBlockHash <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">prepareTransaction</span><span class="token punctuation">(</span>callData<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Transaction prepared with compute unit limit:"</span><span class="token punctuation">,</span> <span class="token constant">COMPUTE_UNITS</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token comment">// Step 4: Sign the transaction</span>
        <span class="token keyword">const</span> signedTx <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">signTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Transaction signed"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token comment">// Step 5: Broadcast the transaction using Onchain gateway API</span>
        <span class="token keyword">const</span> orderId <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">broadcastTransaction</span><span class="token punctuation">(</span>signedTx<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Transaction broadcast successful with order ID: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>orderId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token comment">// Step 6: Monitor the transaction status</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Monitoring transaction status..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> txStatus <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">trackTransaction</span><span class="token punctuation">(</span>orderId<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            success<span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
            orderId<span class="token punctuation">,</span>
            txHash<span class="token operator">:</span> txStatus<span class="token punctuation">.</span>txHash<span class="token punctuation">,</span>
            status<span class="token operator">:</span> txStatus<span class="token punctuation">.</span>txStatus <span class="token operator">===</span> <span class="token string">'2'</span> <span class="token operator">?</span> <span class="token string">'SUCCESS'</span> <span class="token operator">:</span> <span class="token string">'PENDING'</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error during swap:"</span><span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">return</span> <span class="token punctuation">{</span>
            success<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
            error<span class="token operator">:</span> error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span>message <span class="token operator">:</span> <span class="token string">"Unknown error"</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// ======== Command Line Interface ========</span>

<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> args <span class="token operator">=</span> process<span class="token punctuation">.</span>argv<span class="token punctuation">.</span><span class="token function">slice</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token punctuation">(</span>args<span class="token punctuation">.</span>length <span class="token operator">&lt;</span> <span class="token number">3</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Usage: ts-node solana-swap.ts &lt;amount&gt; &lt;fromTokenAddress&gt; &lt;toTokenAddress&gt; [&lt;slippage&gt;]"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Example: ts-node solana-swap.ts 0.1 11111111111111111111111111111111 EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 0.5"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        <span class="token keyword">const</span> <span class="token punctuation">[</span>amountStr<span class="token punctuation">,</span> fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">,</span> slippage <span class="token operator">=</span> <span class="token string">'0.5'</span><span class="token punctuation">]</span> <span class="token operator">=</span> args<span class="token punctuation">;</span>
        
        <span class="token comment">// Get token information</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">getTokenInfo</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">From: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> (</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimals<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> decimals)</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">To: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> (</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>decimals<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> decimals)</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Convert amount using fetched decimals</span>
        <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token function">convertAmount</span><span class="token punctuation">(</span>amountStr<span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimals<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount in </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> base units:</span><span class="token template-punctuation string">`</span></span><span class="token punctuation">,</span> rawAmount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token comment">// Execute swap</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting swap..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">,</span> rawAmount<span class="token punctuation">,</span> slippage<span class="token punctuation">)</span><span class="token punctuation">;</span>
        
        <span class="token keyword">if</span> <span class="token punctuation">(</span>result<span class="token punctuation">.</span>success<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap completed successfully!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Order ID:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>orderId<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">if</span> <span class="token punctuation">(</span>result<span class="token punctuation">.</span>txHash<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Transaction ID:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>txHash<span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>result<span class="token punctuation">.</span>txHash<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
            <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"\nSwap failed:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span>error<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        
        process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span>result<span class="token punctuation">.</span>success <span class="token operator">?</span> <span class="token number">0</span> <span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">error</span><span class="token punctuation">(</span><span class="token string">"Error:"</span><span class="token punctuation">,</span> error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span>message <span class="token operator">:</span> <span class="token string">"Unknown error"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        process<span class="token punctuation">.</span><span class="token function">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Execute main function if run directly</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token keyword">require</span><span class="token punctuation">.</span>main <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Export functions for modular usage</span>
<span class="token keyword">export</span> <span class="token punctuation">{</span>
    executeSwap<span class="token punctuation">,</span>
    broadcastTransaction<span class="token punctuation">,</span>
    trackTransaction<span class="token punctuation">,</span>
    prepareTransaction
<span class="token punctuation">}</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="7. MEV保护" id="7.-mev保护">7. MEV保护<a class="index_header-anchor__Xqb+L" href="#7.-mev保护" style="opacity:0">#</a></h2>
<p>Solana交易存在MEV（最大可提取价值）风险。虽然MEV保护不直接包含在SDK中，但您可以使用API优先的方法自行实施。</p>
<p>第一道防线使用动态优先级费用-将其视为您在拍卖中对抗MEV机器人的出价。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> <span class="token constant">MEV_PROTECTION</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token comment">// Trade Protection</span>
    <span class="token constant">MAX_PRICE_IMPACT</span><span class="token operator">:</span> <span class="token string">"0.05"</span><span class="token punctuation">,</span>        <span class="token comment">// 5% max price impact</span>
    <span class="token constant">SLIPPAGE</span><span class="token operator">:</span> <span class="token string">"0.05"</span><span class="token punctuation">,</span>                <span class="token comment">// 5% slippage tolerance</span>
    <span class="token constant">MIN_ROUTES</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>                   <span class="token comment">// Minimum DEX routes</span>

    <span class="token comment">// Priority Fees</span>
    <span class="token constant">MIN_PRIORITY_FEE</span><span class="token operator">:</span> <span class="token number">10_000</span><span class="token punctuation">,</span>
    <span class="token constant">MAX_PRIORITY_FEE</span><span class="token operator">:</span> <span class="token number">1_000_000</span><span class="token punctuation">,</span>
    <span class="token constant">PRIORITY_MULTIPLIER</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>

    <span class="token comment">// TWAP Settings</span>
    <span class="token constant">TWAP_ENABLED</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
    <span class="token constant">TWAP_INTERVALS</span><span class="token operator">:</span> <span class="token number">4</span><span class="token punctuation">,</span>               <span class="token comment">// Split into 4 parts</span>
    <span class="token constant">TWAP_DELAY_MS</span><span class="token operator">:</span> <span class="token number">2000</span><span class="token punctuation">,</span>            <span class="token comment">// 2s between trades</span>

    <span class="token comment">// Transaction Settings</span>
    <span class="token constant">COMPUTE_UNITS</span><span class="token operator">:</span> <span class="token number">300_000</span><span class="token punctuation">,</span>
    <span class="token constant">MAX_RETRIES</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token constant">CONFIRMATION_TIMEOUT</span><span class="token operator">:</span> <span class="token number">60_000</span><span class="token punctuation">,</span>

    <span class="token comment">// Block Targeting</span>
    <span class="token constant">TARGET_SPECIFIC_BLOCKS</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
    <span class="token constant">PREFERRED_SLOT_OFFSET</span><span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>        <span class="token comment">// Target blocks with slot % 4 == 2</span>
<span class="token punctuation">}</span> <span class="token keyword">as</span> <span class="token keyword">const</span><span class="token punctuation">;</span>

<span class="token keyword">static</span> <span class="token keyword">async</span> <span class="token function">getPriorityFee</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> recentFees <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">getRecentPrioritizationFees</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> maxFee <span class="token operator">=</span> Math<span class="token punctuation">.</span><span class="token function">max</span><span class="token punctuation">(</span><span class="token operator">...</span>recentFees<span class="token punctuation">.</span><span class="token function">map</span><span class="token punctuation">(</span>fee <span class="token operator">=&gt;</span> fee<span class="token punctuation">.</span>prioritizationFee<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">return</span> Math<span class="token punctuation">.</span><span class="token function">min</span><span class="token punctuation">(</span>maxFee <span class="token operator">*</span> <span class="token number">1.5</span><span class="token punctuation">,</span> <span class="token constant">MEV_PROTECTION</span><span class="token punctuation">.</span><span class="token constant">MAX_PRIORITY_FEE</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>对于较大的交易，您可以启用TWAP（时间加权平均价格）。您的交易将被分成更小的部分，而不是MEV机器人喜欢瞄准的一个大的飞溅。</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// Define the TWAPExecution class outside of the if block</span>
<span class="token keyword">class</span> <span class="token class-name">TWAPExecution</span> <span class="token punctuation">{</span>
    <span class="token keyword">static</span> <span class="token keyword">async</span> <span class="token function">splitTrade</span><span class="token punctuation">(</span>
        totalAmount<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">,</span>
        toTokenAddress<span class="token operator">:</span> <span class="token builtin">string</span>
    <span class="token punctuation">)</span><span class="token operator">:</span> <span class="token builtin">Promise</span><span class="token operator">&lt;</span>TradeChunk<span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token operator">&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> amount <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name"><span class="token constant">BN</span></span><span class="token punctuation">(</span>totalAmount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> chunkSize <span class="token operator">=</span> amount<span class="token punctuation">.</span><span class="token function">divn</span><span class="token punctuation">(</span><span class="token constant">MEV_PROTECTION</span><span class="token punctuation">.</span><span class="token constant">TWAP_INTERVALS</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">return</span> <span class="token function">Array</span><span class="token punctuation">(</span><span class="token constant">MEV_PROTECTION</span><span class="token punctuation">.</span><span class="token constant">TWAP_INTERVALS</span><span class="token punctuation">)</span>
            <span class="token punctuation">.</span><span class="token function">fill</span><span class="token punctuation">(</span><span class="token keyword">null</span><span class="token punctuation">)</span>
            <span class="token punctuation">.</span><span class="token function">map</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>
                amount<span class="token operator">:</span> chunkSize<span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                fromTokenAddress<span class="token punctuation">,</span>
                toTokenAddress<span class="token punctuation">,</span>
                minAmountOut<span class="token operator">:</span> <span class="token string">"0"</span> <span class="token comment">// Will be calculated per chunk</span>
            <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Then use it in the if block</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token constant">MEV_PROTECTION</span><span class="token punctuation">.</span><span class="token constant">TWAP_ENABLED</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> chunks <span class="token operator">=</span> <span class="token keyword">await</span> TWAPExecution<span class="token punctuation">.</span><span class="token function">splitTrade</span><span class="token punctuation">(</span>
        rawAmount<span class="token punctuation">,</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h3 id="运行中防护">运行中防护<a class="index_header-anchor__Xqb+L" href="#运行中防护" style="opacity:0">#</a></h3>
<p>当您使用<a class="items-center" href="https://github.com/okx/dex-api-library/blob/main/lib/solana/swap/solana-swap-mev.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">此实现<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>执行交易时，会发生几件事情：</p>
<ol>
<li>交易前检查：</li>
</ol>
<ul>
<li>购买的代币会被检查是否存在貔貅盘特征</li>
<li>检查你的网络费用来设置有竞争力的优先费用</li>
<li>查看你的交易额度来确认是否要拆单</li>
</ul>
<ol start="2">
<li>在交易期间：</li>
</ol>
<ul>
<li>大额交易将拆分成不同金额的单子，并在随机时间发出</li>
<li>每单将根据市场条件设置优先费用</li>
<li>特定的区块来减少暴露风险</li>
</ul>
<ol start="3">
<li>交易的安全性保障：</li>
</ol>
<ul>
<li>每笔交易都将进行预执行模拟</li>
<li>对区块确认状态进行内置的追踪</li>
<li>出现问题自动重试逻辑</li>
</ul>
<p>虽然Solana上的MEV不能完全消除，但这些保护措施使MEV机器人的生活更加困难。</p>
<h2 data-content="方法2：SDK方法" id="方法2：sdk方法">方法2：SDK方法<a class="index_header-anchor__Xqb+L" href="#方法2：sdk方法" style="opacity:0">#</a></h2>
<p>使用OKX DEXSDK提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为您处理许多实现细节，包括重试逻辑、错误处理和事务管理。</p>
<h2 data-content="1.安装SDK" id="1.安装sdk">1.安装SDK<a class="index_header-anchor__Xqb+L" href="#1.安装sdk" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">yarn</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">pnpm</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
</code></pre></div>
<h2 data-content="2.设置环境" id="2.设置环境">2.设置环境<a class="index_header-anchor__Xqb+L" href="#2.设置环境" style="opacity:0">#</a></h2>
<p>使用您的API凭据和钱包信息创建一个. env文件：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token comment"># OKX API Credentials</span>
<span class="token assign-left variable">OKX_API_KEY</span><span class="token operator">=</span>your_api_key
<span class="token assign-left variable">OKX_SECRET_KEY</span><span class="token operator">=</span>your_secret_key
<span class="token assign-left variable">OKX_API_PASSPHRASE</span><span class="token operator">=</span>your_passphrase
<span class="token assign-left variable">OKX_PROJECT_ID</span><span class="token operator">=</span>your_project_id
<span class="token comment"># Solana Configuration</span>
<span class="token assign-left variable">SOLANA_RPC_URL</span><span class="token operator">=</span>your_solana_rpc_url
<span class="token assign-left variable">SOLANA_WALLET_ADDRESS</span><span class="token operator">=</span>your_solana_wallet_address
<span class="token assign-left variable">SOLANA_PRIVATE_KEY</span><span class="token operator">=</span>your_solana_private_key
</code></pre></div>
<h2 data-content="3.初始化客户端" id="3.初始化客户端">3.初始化客户端<a class="index_header-anchor__Xqb+L" href="#3.初始化客户端" style="opacity:0">#</a></h2>
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
    <span class="token string">'SOLANA_WALLET_ADDRESS'</span><span class="token punctuation">,</span>
    <span class="token string">'SOLANA_PRIVATE_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'SOLANA_RPC_URL'</span>
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
    solana<span class="token operator">:</span> <span class="token punctuation">{</span>
        connection<span class="token operator">:</span> <span class="token punctuation">{</span>
            rpcUrl<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span><span class="token operator">!</span><span class="token punctuation">,</span>
            wsEndpoint<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_WS_URL</span><span class="token punctuation">,</span>
            confirmTransactionInitialTimeout<span class="token operator">:</span> <span class="token number">5000</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        walletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_WALLET_ADDRESS</span><span class="token operator">!</span><span class="token punctuation">,</span>
        privateKey<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_PRIVATE_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
        computeUnits<span class="token operator">:</span> <span class="token number">300000</span><span class="token punctuation">,</span>
        maxRetries<span class="token operator">:</span> <span class="token number">3</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="4.调用SDK执行兑换" id="4.调用sdk执行兑换">4.调用SDK执行兑换<a class="index_header-anchor__Xqb+L" href="#4.调用sdk执行兑换" style="opacity:0">#</a></h2>
<p>创建兑换执行的文件：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// swap.ts</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span> client <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'./DexClient'</span><span class="token punctuation">;</span>
<span class="token doc-comment comment">/**</span>
<span class="token doc-comment comment"> * Example: Execute a swap from SOL to USDC</span>
<span class="token doc-comment comment"> */</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">try</span> <span class="token punctuation">{</span>
    <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_PRIVATE_KEY</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
      <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">'Missing SOLANA_PRIVATE_KEY in .env file'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token comment">// Get quote to fetch token information</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        chainId<span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
        toTokenAddress<span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
        amount<span class="token operator">:</span> <span class="token string">'1000000'</span><span class="token punctuation">,</span> <span class="token comment">// Small amount for quote</span>
        slippage<span class="token operator">:</span> <span class="token string">'0.5'</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token punctuation">{</span>
        fromToken<span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token builtin">symbol</span><span class="token operator">:</span> quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenSymbol<span class="token punctuation">,</span>
            decimals<span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimal<span class="token punctuation">)</span><span class="token punctuation">,</span>
            price<span class="token operator">:</span> quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>tokenUnitPrice
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        toToken<span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token builtin">symbol</span><span class="token operator">:</span> quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>tokenSymbol<span class="token punctuation">,</span>
            decimals<span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>decimal<span class="token punctuation">)</span><span class="token punctuation">,</span>
            price<span class="token operator">:</span> quote<span class="token punctuation">.</span>data<span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">.</span>toToken<span class="token punctuation">.</span>tokenUnitPrice
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token comment">// Convert amount to base units (for display purposes)</span>
    <span class="token keyword">const</span> humanReadableAmount <span class="token operator">=</span> <span class="token number">0.1</span><span class="token punctuation">;</span> <span class="token comment">// 0.1 SOL</span>
    <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> Math<span class="token punctuation">.</span><span class="token function">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap Details:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"--------------------"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">From: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">To: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>toToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>humanReadableAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string"> </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span><span class="token builtin">symbol</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Amount in base units: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>rawAmount<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Approximate USD value: $</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token punctuation">(</span>humanReadableAmount <span class="token operator">*</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span>fromToken<span class="token punctuation">.</span>price<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toFixed</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Execute the swap</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting swap..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> swapResult <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      chainId<span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span> <span class="token comment">// Solana chain ID</span>
      fromTokenAddress<span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
      toTokenAddress<span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
      amount<span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
      slippage<span class="token operator">:</span> <span class="token string">'0.5'</span><span class="token punctuation">,</span> <span class="token comment">// 0.5% slippage</span>
      userWalletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_WALLET_ADDRESS</span><span class="token operator">!</span>
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
<h2 data-content="5.附加SDK功能" id="5.附加sdk功能">5.附加SDK功能<a class="index_header-anchor__Xqb+L" href="#5.附加sdk功能" style="opacity:0">#</a></h2>
<p>SDK提供了简化开发的附加方法：
获取代币对的报价</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword">await</span> client<span class="token punctuation">.</span>dex<span class="token punctuation">.</span><span class="token function">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    chainId<span class="token operator">:</span> <span class="token string">'501'</span><span class="token punctuation">,</span>  <span class="token comment">// Solana</span>
    fromTokenAddress<span class="token operator">:</span> <span class="token string">'11111111111111111111111111111111'</span><span class="token punctuation">,</span> <span class="token comment">// SOL</span>
    toTokenAddress<span class="token operator">:</span> <span class="token string">'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v'</span><span class="token punctuation">,</span> <span class="token comment">// USDC</span>
    amount<span class="token operator">:</span> <span class="token string">'100000000'</span><span class="token punctuation">,</span>  <span class="token comment">// 0.1 SOL (in lamports)</span>
    slippage<span class="token operator">:</span> <span class="token string">'0.5'</span>     <span class="token comment">// 0.5%</span>
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
    "交易 API",
    "搭建兑换应用",
    "在 Solana 链上搭建兑换应用"
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
    "2.获取兑换数据",
    "3.准备交易",
    "4. 广播交易",
    "5.追踪交易",
    "6.完整实现",
    "7. MEV保护",
    "方法2：SDK方法",
    "1.安装SDK",
    "2.设置环境",
    "3.初始化客户端",
    "4.调用SDK执行兑换",
    "5.附加SDK功能"
  ]
}
```

</details>
