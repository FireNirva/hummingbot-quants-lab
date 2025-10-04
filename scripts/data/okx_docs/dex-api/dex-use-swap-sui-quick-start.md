# 在 Sui 链上搭建兑换应用 | 搭建兑换应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-swap-sui-quick-start#方法1：api方法  
**抓取时间:** 2025-05-27 03:58:46  
**字数:** 3533

## 导航路径
DEX API > 交易 API > 搭建兑换应用 > 在 Sui 链上搭建兑换应用

## 目录
- 方法1：API方法
- 1. 设置环境
- 2. 获取代币信息和兑换报价
- 3. 处理和签署交易
- 4. 执行交易
- 5. 完整实现
- 方法2：SDK方法
- 1. 安装SDK
- 2. 设置环境
- 3. 初始化客户端
- 4. 创建代币助手（可选）
- 5. 调用SDK执行兑换

---

在 Sui 链上搭建兑换应用
#
在Sui上使用OKX DEX构建兑换应用程序有两种方法：
API 方法 - 直接调用 OKX DEX API
SDK方法 - 使用
@okx-dex/okx-dex-sdk
，简化了开发人员的体验
本指南涵盖了这两种方法，以帮助你选择最适合你需求的方法。
方法1：API方法
#
在本指南中，我们将提供通过OKX DEX进行Sui代币兑换的用例。
1. 设置环境
#
导入必要的Node. js库并设置环境变量：
// Required libraries
import
{
SuiWallet
}
from
"@okxweb3/coin-sui"
;
import
{
getFullnodeUrl
,
SuiClient
}
from
'@mysten/sui/client'
;
import
{
Transaction
}
from
'@mysten/sui/transactions'
;
import
cryptoJS
from
"crypto-js"
;
// Install dependencies
// npm i @okxweb3/coin-sui
// npm i @mysten/sui
// npm i crypto-js
// Set up environment variables
const
apiKey
=
'your_api_key'
;
const
secretKey
=
'your_secret_key'
;
const
apiPassphrase
=
'your_passphrase'
;
const
projectId
=
'your_project_id'
;
const
userAddress
=
'your_sui_wallet_address'
;
const
userPrivateKey
=
'your_sui_wallet_private_key'
;
// Constants
const
SUI_CHAIN_ID
=
"784"
;
const
DEFAULT_GAS_BUDGET
=
50000000
;
const
MAX_RETRIES
=
3
;
// Initialize Sui client
const
wallet
=
new
SuiWallet
(
)
;
const
client
=
new
SuiClient
(
{
url
:
getFullnodeUrl
(
'mainnet'
)
}
)
;
// For Sui, you need to use the hexWithoutFlag format of your private key
// You can convert your key using sui keytool:
// sui keytool convert <your_sui_private_key>
2. 获取代币信息和兑换报价
#
首先，创建一个实用函数来处理API身份验证标头：
function
getHeaders
(
timestamp
,
method
,
requestPath
,
queryString
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
然后，创建一个函数来获取令牌信息：
async
function
getTokenInfo
(
fromTokenAddress
,
toTokenAddress
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
"/api/v5/dex/aggregator/quote"
;
const
params
=
{
chainId
:
SUI_CHAIN_ID
,
fromTokenAddress
,
toTokenAddress
,
amount
:
"1000000"
,
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
const
response
=
await
fetch
(
https
:
/
/
web3
.
okx
.
com$
{
requestPath
}
$
{
queryString
}
,
{
method
:
"GET"
,
headers
}
)
;
if
(
!
response
.
ok
)
{
throw
new
Error
(
Failed
to
get
quote
:
$
{
await
response
.
text
(
)
}
)
;
}
const
data
=
await
response
.
json
(
)
;
if
(
data
.
code
!==
"0"
||
!
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
创建一个函数将人类可读的数量转换为基本单位：
function
convertAmount
(
amount
,
decimals
)
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
(
BigInt
(
Math
.
floor
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
3. 处理和签署交易
#
从/swap获得数据后，你需要处理并签署事务：
async
function
executeSwap
(
txData
,
privateKey
)
{
// Create transaction block
const
txBlock
=
Transaction
.
from
(
txData
)
;
txBlock
.
setSender
(
normalizedWalletAddress
)
;
// Set gas parameters
const
referenceGasPrice
=
await
client
.
getReferenceGasPrice
(
)
;
txBlock
.
setGasPrice
(
BigInt
(
referenceGasPrice
)
)
;
txBlock
.
setGasBudget
(
BigInt
(
DEFAULT_GAS_BUDGET
)
)
;
// Build and sign transaction
const
builtTx
=
await
txBlock
.
build
(
{
client
}
)
;
const
txBytes
=
Buffer
.
from
(
builtTx
)
.
toString
(
'base64'
)
;
const
signedTx
=
await
wallet
.
signTransaction
(
{
privateKey
,
data
:
{
type
:
'raw'
,
data
:
txBytes
}
}
)
;
if
(
!
signedTx
?.
signature
)
{
throw
new
Error
(
"Failed to sign transaction"
)
;
}
return
{
builtTx
,
signature
:
signedTx
.
signature
}
;
}
4. 执行交易
#
最后，执行签名交易：
async
function
sendTransaction
(
builtTx
,
signature
)
{
// Execute transaction
const
result
=
await
client
.
executeTransactionBlock
(
{
transactionBlock
:
builtTx
,
signature
:
[
signature
]
,
options
:
{
showEffects
:
true
,
showEvents
:
true
,
}
}
)
;
// Wait for confirmation
const
confirmation
=
await
client
.
waitForTransaction
(
{
digest
:
result
.
digest
,
options
:
{
showEffects
:
true
,
showEvents
:
true
,
}
}
)
;
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
"Transaction ID:"
,
result
.
digest
)
;
console
.
log
(
"Explorer URL:"
,
https
:
/
/
suiscan
.
xyz
/
mainnet
/
tx
/
$
{
result
.
digest
}
)
;
return
result
.
digest
;
}
5. 完整实现
#
这是一个完整的实现，将所有内容整合在一起：
// swap.ts
import
{
SuiWallet
}
from
"@okxweb3/coin-sui"
;
import
{
getFullnodeUrl
,
SuiClient
}
from
'@mysten/sui/client'
;
import
{
Transaction
}
from
'@mysten/sui/transactions'
;
import
cryptoJS
from
"crypto-js"
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
// Constants
const
SUI_CHAIN_ID
=
"784"
;
const
DEFAULT_GAS_BUDGET
=
50000000
;
const
MAX_RETRIES
=
3
;
// Initialize clients
const
wallet
=
new
SuiWallet
(
)
;
const
client
=
new
SuiClient
(
{
url
:
getFullnodeUrl
(
'mainnet'
)
}
)
;
// Normalize wallet address
const
normalizedWalletAddress
=
userAddress
;
function
getHeaders
(
timestamp
,
method
,
requestPath
,
queryString
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
async
function
getTokenInfo
(
fromTokenAddress
,
toTokenAddress
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
"/api/v5/dex/aggregator/quote"
;
const
params
=
{
chainId
:
SUI_CHAIN_ID
,
fromTokenAddress
,
toTokenAddress
,
amount
:
"1000000"
,
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
const
response
=
await
fetch
(
https
:
/
/
web3
.
okx
.
com$
{
requestPath
}
$
{
queryString
}
,
{
method
:
"GET"
,
headers
}
)
;
if
(
!
response
.
ok
)
{
throw
new
Error
(
Failed
to
get
quote
:
$
{
await
response
.
text
(
)
}
)
;
}
const
data
=
await
response
.
json
(
)
;
if
(
data
.
code
!==
"0"
||
!
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
function
convertAmount
(
amount
,
decimals
)
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
(
BigInt
(
Math
.
floor
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
"Usage: ts-node swap.ts <amount> <fromTokenAddress> <toTokenAddress>"
)
;
console
.
log
(
"Example: ts-node swap.ts 1.5 0x2::sui::SUI 0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"
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
amount
,
fromTokenAddress
,
toTokenAddress
]
=
args
;
if
(
!
userPrivateKey
||
!
userAddress
)
{
throw
new
Error
(
"Private key or user address not found"
)
;
}
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
(
$
{
tokenInfo
.
fromToken
.
decimals
}
decimals
)
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
(
$
{
tokenInfo
.
toToken
.
decimals
}
decimals
)
)
;
// Convert amount using fetched decimals
const
rawAmount
=
convertAmount
(
amount
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
Amount
in
$
{
tokenInfo
.
fromToken
.
symbol
}
base units
:
,
rawAmount
)
;
// Get swap quote
const
quoteParams
=
{
chainId
:
SUI_CHAIN_ID
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
normalizedWalletAddress
,
}
;
// Get swap data
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
queryString
=
"?"
+
new
URLSearchParams
(
quoteParams
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
console
.
log
(
"Requesting swap quote..."
)
;
const
response
=
await
fetch
(
https
:
/
/
web3
.
okx
.
com$
{
requestPath
}
$
{
queryString
}
,
{
method
:
"GET"
,
headers
}
)
;
const
data
=
await
response
.
json
(
)
;
if
(
data
.
code
!==
"0"
)
{
throw
new
Error
(
API
Error
:
$
{
data
.
msg
}
)
;
}
const
swapData
=
data
.
data
[
0
]
;
// Show estimated output and price impact
const
outputAmount
=
parseFloat
(
swapData
.
routerResult
.
toTokenAmount
)
/
Math
.
pow
(
10
,
tokenInfo
.
toToken
.
decimals
)
;
console
.
log
(
"\nSwap Quote:"
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
amount
}
$
{
tokenInfo
.
fromToken
.
symbol
}
(
$$
{
(
parseFloat
(
amount
)
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
outputAmount
.
toFixed
(
tokenInfo
.
toToken
.
decimals
)
}
$
{
tokenInfo
.
toToken
.
symbol
}
(
$$
{
(
outputAmount
*
parseFloat
(
tokenInfo
.
toToken
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
)
;
if
(
swapData
.
priceImpactPercentage
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
swapData
.
priceImpactPercentage
}
%
)
;
}
console
.
log
(
"\nExecuting swap transaction..."
)
;
let
retryCount
=
0
;
while
(
retryCount
<
MAX_RETRIES
)
{
try
{
// Create transaction block
const
txBlock
=
Transaction
.
from
(
swapData
.
tx
.
data
)
;
txBlock
.
setSender
(
normalizedWalletAddress
)
;
// Set gas parameters
const
referenceGasPrice
=
await
client
.
getReferenceGasPrice
(
)
;
txBlock
.
setGasPrice
(
BigInt
(
referenceGasPrice
)
)
;
txBlock
.
setGasBudget
(
BigInt
(
DEFAULT_GAS_BUDGET
)
)
;
// Build and sign transaction
const
builtTx
=
await
txBlock
.
build
(
{
client
}
)
;
const
txBytes
=
Buffer
.
from
(
builtTx
)
.
toString
(
'base64'
)
;
const
signedTx
=
await
wallet
.
signTransaction
(
{
privateKey
:
userPrivateKey
,
data
:
{
type
:
'raw'
,
data
:
txBytes
}
}
)
;
if
(
!
signedTx
?.
signature
)
{
throw
new
Error
(
"Failed to sign transaction"
)
;
}
// Execute transaction
const
result
=
await
client
.
executeTransactionBlock
(
{
transactionBlock
:
builtTx
,
signature
:
[
signedTx
.
signature
]
,
options
:
{
showEffects
:
true
,
showEvents
:
true
,
}
}
)
;
// Wait for confirmation
const
confirmation
=
await
client
.
waitForTransaction
(
{
digest
:
result
.
digest
,
options
:
{
showEffects
:
true
,
showEvents
:
true
,
}
}
)
;
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
"Transaction ID:"
,
result
.
digest
)
;
console
.
log
(
"Explorer URL:"
,
https
:
/
/
suiscan
.
xyz
/
mainnet
/
tx
/
$
{
result
.
digest
}
)
;
process
.
exit
(
0
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
Attempt
$
{
retryCount
+
1
}
failed
:
,
error
)
;
retryCount
++
;
if
(
retryCount
===
MAX_RETRIES
)
{
throw
error
;
}
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
2000
*
retryCount
)
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
方法2：SDK方法
#
OKX DEX SDK 提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为你处理许多实现细节，包括重试逻辑、错误处理和交易管理。
1. 安装SDK
#
npm
install
@okx-dex/okx-dex-sdk
or
yarn
add
@okx-dex/okx-dex-sdk
or
pnpm
add
@okx-dex/okx-dex-sdk
2. 设置环境
#
使用你的API凭据和钱包信息创建一个. env文件：
OKX API Credentials
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
Sui Configuration
SUI_WALLET_ADDRESS
=
your_sui_wallet_address
SUI_PRIVATE_KEY
=
your_sui_private_key
请记住，你需要使用SUI私钥的hexWithouse tFlag格式，你可以使用SUICLI获得：
sui keytool convert
<
your_sui_private_key
>
3. 初始化客户端
#
为你的DEX客户端创建一个文件（例如，DexClient. ts）：
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
'SUI_WALLET_ADDRESS'
,
'SUI_PRIVATE_KEY'
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
Missing
required environment variable
:
$
{
envVar
}
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
sui
:
{
privateKey
:
process
.
env
.
SUI_PRIVATE_KEY
!
,
walletAddress
:
process
.
env
.
SUI_WALLET_ADDRESS
!
,
connection
:
{
rpcUrl
:
'https://sui-mainnet.blockvision.org'
}
}
}
)
;
4. 创建代币助手（可选）
#
你可以创建一个代币列表助手以便于参考：
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
5. 调用SDK执行兑换
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
## 附加
SDK
功能
SDK
提供了简化开发的附加方法：
获取代币对的报价
`
`
`javascript
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
<div class="routes_md__xWlGF"><!--$--><h1 id="在-sui-链上搭建兑换应用">在 Sui 链上搭建兑换应用<a class="index_header-anchor__Xqb+L" href="#在-sui-链上搭建兑换应用" style="opacity:0">#</a></h1>
<p>在Sui上使用OKX DEX构建兑换应用程序有两种方法：</p>
<ul>
<li>API 方法 - 直接调用 OKX DEX API</li>
<li>SDK方法 - 使用 <code>@okx-dex/okx-dex-sdk</code>，简化了开发人员的体验</li>
</ul>
<p>本指南涵盖了这两种方法，以帮助你选择最适合你需求的方法。</p>
<h2 data-content="方法1：API方法" id="方法1：api方法">方法1：API方法<a class="index_header-anchor__Xqb+L" href="#方法1：api方法" style="opacity:0">#</a></h2>
<p>在本指南中，我们将提供通过OKX DEX进行Sui代币兑换的用例。</p>
<h2 data-content="1. 设置环境" id="1.-设置环境">1. 设置环境<a class="index_header-anchor__Xqb+L" href="#1.-设置环境" style="opacity:0">#</a></h2>
<p>导入必要的Node. js库并设置环境变量：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Required libraries</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">SuiWallet</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">"@okxweb3/coin-sui"</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> getFullnodeUrl<span class="token punctuation">,</span> <span class="token maybe-class-name">SuiClient</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@mysten/sui/client'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">Transaction</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@mysten/sui/transactions'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports">cryptoJS</span> <span class="token keyword module">from</span> <span class="token string">"crypto-js"</span><span class="token punctuation">;</span>
<span class="token comment">// Install dependencies</span>
<span class="token comment">// npm i @okxweb3/coin-sui</span>
<span class="token comment">// npm i @mysten/sui</span>
<span class="token comment">// npm i crypto-js</span>
<span class="token comment">// Set up environment variables</span>
<span class="token keyword">const</span> apiKey <span class="token operator">=</span> <span class="token string">'your_api_key'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> secretKey <span class="token operator">=</span> <span class="token string">'your_secret_key'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> <span class="token string">'your_passphrase'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> projectId <span class="token operator">=</span> <span class="token string">'your_project_id'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userAddress <span class="token operator">=</span> <span class="token string">'your_sui_wallet_address'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userPrivateKey <span class="token operator">=</span> <span class="token string">'your_sui_wallet_private_key'</span><span class="token punctuation">;</span>
<span class="token comment">// Constants</span>
<span class="token keyword">const</span> <span class="token constant">SUI_CHAIN_ID</span> <span class="token operator">=</span> <span class="token string">"784"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">DEFAULT_GAS_BUDGET</span> <span class="token operator">=</span> <span class="token number">50000000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">MAX_RETRIES</span> <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">;</span>
<span class="token comment">// Initialize Sui client</span>
<span class="token keyword">const</span> wallet <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">SuiWallet</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">SuiClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">url</span><span class="token operator">:</span> <span class="token function">getFullnodeUrl</span><span class="token punctuation">(</span><span class="token string">'mainnet'</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// For Sui, you need to use the hexWithoutFlag format of your private key</span>
<span class="token comment">// You can convert your key using sui keytool:</span>
<span class="token comment">// sui keytool convert &lt;your_sui_private_key&gt;</span>
</code></pre></div>
<h2 data-content="2. 获取代币信息和兑换报价" id="2.-获取代币信息和兑换报价">2. 获取代币信息和兑换报价<a class="index_header-anchor__Xqb+L" href="#2.-获取代币信息和兑换报价" style="opacity:0">#</a></h2>
<p>首先，创建一个实用函数来处理API身份验证标头：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> method<span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>apiKey <span class="token operator">||</span> <span class="token operator">!</span>secretKey <span class="token operator">||</span> <span class="token operator">!</span>apiPassphrase <span class="token operator">||</span> <span class="token operator">!</span>projectId<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing required environment variables"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> queryString<span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>
            cryptoJS<span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
然后，创建一个函数来获取令牌信息：
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getTokenInfo</span><span class="token punctuation">(</span><span class="token parameter">fromTokenAddress<span class="token punctuation">,</span> toTokenAddress</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token string">"/api/v5/dex/aggregator/quote"</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token constant">SUI_CHAIN_ID</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token punctuation">,</span>
        <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">"1000000"</span><span class="token punctuation">,</span>
        <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">fetch</span><span class="token punctuation">(</span>
        
<span class="token literal-property property">https</span><span class="token operator">:</span><span class="token operator">/</span><span class="token operator">/</span>web3<span class="token punctuation">.</span><span class="token property-access">okx</span><span class="token punctuation">.</span><span class="token property-access">com$</span><span class="token punctuation">{</span>requestPath<span class="token punctuation">}</span>$<span class="token punctuation">{</span>queryString<span class="token punctuation">}</span>
<span class="token punctuation">,</span>
        <span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> headers <span class="token punctuation">}</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>response<span class="token punctuation">.</span><span class="token property-access">ok</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Failed</span> to <span class="token keyword">get</span> <span class="token literal-property property">quote</span><span class="token operator">:</span> $<span class="token punctuation">{</span><span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">text</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>data<span class="token punctuation">.</span><span class="token property-access">code</span> <span class="token operator">!==</span> <span class="token string">"0"</span> <span class="token operator">||</span> <span class="token operator">!</span>data<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Failed to get token information"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> quoteData <span class="token operator">=</span> data<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">fromToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">toToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
创建一个函数将人类可读的数量转换为基本单位：
<span class="token keyword">function</span> <span class="token function">convertAmount</span><span class="token punctuation">(</span><span class="token parameter">amount<span class="token punctuation">,</span> decimals</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>amount <span class="token operator">||</span> <span class="token function">isNaN</span><span class="token punctuation">(</span><span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">const</span> value <span class="token operator">=</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>value <span class="token operator">&lt;=</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Amount must be greater than 0"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword control-flow">return</span> <span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">floor</span><span class="token punctuation">(</span>value <span class="token operator">*</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>err<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">"Amount conversion error:"</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount format"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="3. 处理和签署交易" id="3.-处理和签署交易">3. 处理和签署交易<a class="index_header-anchor__Xqb+L" href="#3.-处理和签署交易" style="opacity:0">#</a></h2>
<p>从/swap获得数据后，你需要处理并签署事务：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">executeSwap</span><span class="token punctuation">(</span><span class="token parameter">txData<span class="token punctuation">,</span> privateKey</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Create transaction block</span>
    <span class="token keyword">const</span> txBlock <span class="token operator">=</span> <span class="token maybe-class-name">Transaction</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>txData<span class="token punctuation">)</span><span class="token punctuation">;</span>
    txBlock<span class="token punctuation">.</span><span class="token method function property-access">setSender</span><span class="token punctuation">(</span>normalizedWalletAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Set gas parameters</span>
    <span class="token keyword">const</span> referenceGasPrice <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">getReferenceGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    txBlock<span class="token punctuation">.</span><span class="token method function property-access">setGasPrice</span><span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span>referenceGasPrice<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    txBlock<span class="token punctuation">.</span><span class="token method function property-access">setGasBudget</span><span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token constant">DEFAULT_GAS_BUDGET</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Build and sign transaction</span>
    <span class="token keyword">const</span> builtTx <span class="token operator">=</span> <span class="token keyword control-flow">await</span> txBlock<span class="token punctuation">.</span><span class="token method function property-access">build</span><span class="token punctuation">(</span><span class="token punctuation">{</span> client <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> txBytes <span class="token operator">=</span> <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>builtTx<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token string">'base64'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> signedTx <span class="token operator">=</span> <span class="token keyword control-flow">await</span> wallet<span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        privateKey<span class="token punctuation">,</span>
        <span class="token literal-property property">data</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'raw'</span><span class="token punctuation">,</span>
            <span class="token literal-property property">data</span><span class="token operator">:</span> txBytes
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>signedTx<span class="token operator">?.</span>signature<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Failed to sign transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span> builtTx<span class="token punctuation">,</span> <span class="token literal-property property">signature</span><span class="token operator">:</span> signedTx<span class="token punctuation">.</span><span class="token property-access">signature</span> <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="4. 执行交易" id="4.-执行交易">4. 执行交易<a class="index_header-anchor__Xqb+L" href="#4.-执行交易" style="opacity:0">#</a></h2>
<p>最后，执行签名交易：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">sendTransaction</span><span class="token punctuation">(</span><span class="token parameter">builtTx<span class="token punctuation">,</span> signature</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token comment">// Execute transaction</span>
    <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">executeTransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">transactionBlock</span><span class="token operator">:</span> builtTx<span class="token punctuation">,</span>
        <span class="token literal-property property">signature</span><span class="token operator">:</span> <span class="token punctuation">[</span>signature<span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">showEffects</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
            <span class="token literal-property property">showEvents</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token comment">// Wait for confirmation</span>
    <span class="token keyword">const</span> confirmation <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">waitForTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        <span class="token literal-property property">digest</span><span class="token operator">:</span> result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">,</span>
        <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">showEffects</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
            <span class="token literal-property property">showEvents</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap completed successfully!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Transaction ID:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> 
<span class="token literal-property property">https</span><span class="token operator">:</span><span class="token operator">/</span><span class="token operator">/</span>suiscan<span class="token punctuation">.</span><span class="token property-access">xyz</span><span class="token operator">/</span>mainnet<span class="token operator">/</span>tx<span class="token operator">/</span>$<span class="token punctuation">{</span>result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="5. 完整实现" id="5.-完整实现">5. 完整实现<a class="index_header-anchor__Xqb+L" href="#5.-完整实现" style="opacity:0">#</a></h2>
<p>这是一个完整的实现，将所有内容整合在一起：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// swap.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">SuiWallet</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">"@okxweb3/coin-sui"</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> getFullnodeUrl<span class="token punctuation">,</span> <span class="token maybe-class-name">SuiClient</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@mysten/sui/client'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">Transaction</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@mysten/sui/transactions'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports">cryptoJS</span> <span class="token keyword module">from</span> <span class="token string">"crypto-js"</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports">dotenv</span> <span class="token keyword module">from</span> <span class="token string">'dotenv'</span><span class="token punctuation">;</span>
dotenv<span class="token punctuation">.</span><span class="token method function property-access">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Environment variables</span>
<span class="token keyword">const</span> apiKey <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> secretKey <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> apiPassphrase <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> projectId <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userAddress <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">WALLET_ADDRESS</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> userPrivateKey <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">PRIVATE_KEY</span><span class="token punctuation">;</span>
<span class="token comment">// Constants</span>
<span class="token keyword">const</span> <span class="token constant">SUI_CHAIN_ID</span> <span class="token operator">=</span> <span class="token string">"784"</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">DEFAULT_GAS_BUDGET</span> <span class="token operator">=</span> <span class="token number">50000000</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token constant">MAX_RETRIES</span> <span class="token operator">=</span> <span class="token number">3</span><span class="token punctuation">;</span>
<span class="token comment">// Initialize clients</span>
<span class="token keyword">const</span> wallet <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">SuiWallet</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">SuiClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">url</span><span class="token operator">:</span> <span class="token function">getFullnodeUrl</span><span class="token punctuation">(</span><span class="token string">'mainnet'</span><span class="token punctuation">)</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// Normalize wallet address</span>
<span class="token keyword">const</span> normalizedWalletAddress <span class="token operator">=</span> userAddress<span class="token punctuation">;</span>
<span class="token keyword">function</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> method<span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString <span class="token operator">=</span> <span class="token string">""</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>apiKey <span class="token operator">||</span> <span class="token operator">!</span>secretKey <span class="token operator">||</span> <span class="token operator">!</span>apiPassphrase <span class="token operator">||</span> <span class="token operator">!</span>projectId<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Missing required environment variables"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> stringToSign <span class="token operator">=</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> requestPath <span class="token operator">+</span> queryString<span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span>
        <span class="token string-property property">"Content-Type"</span><span class="token operator">:</span> <span class="token string">"application/json"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-KEY"</span><span class="token operator">:</span> apiKey<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-SIGN"</span><span class="token operator">:</span> cryptoJS<span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>
            cryptoJS<span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>stringToSign<span class="token punctuation">,</span> secretKey<span class="token punctuation">)</span>
        <span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-TIMESTAMP"</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PASSPHRASE"</span><span class="token operator">:</span> apiPassphrase<span class="token punctuation">,</span>
        <span class="token string-property property">"OK-ACCESS-PROJECT"</span><span class="token operator">:</span> projectId<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">getTokenInfo</span><span class="token punctuation">(</span><span class="token parameter">fromTokenAddress<span class="token punctuation">,</span> toTokenAddress</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token string">"/api/v5/dex/aggregator/quote"</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token constant">SUI_CHAIN_ID</span><span class="token punctuation">,</span>
        fromTokenAddress<span class="token punctuation">,</span>
        toTokenAddress<span class="token punctuation">,</span>
        <span class="token literal-property property">amount</span><span class="token operator">:</span> <span class="token string">"1000000"</span><span class="token punctuation">,</span>
        <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">fetch</span><span class="token punctuation">(</span>
        
<span class="token literal-property property">https</span><span class="token operator">:</span><span class="token operator">/</span><span class="token operator">/</span>web3<span class="token punctuation">.</span><span class="token property-access">okx</span><span class="token punctuation">.</span><span class="token property-access">com$</span><span class="token punctuation">{</span>requestPath<span class="token punctuation">}</span>$<span class="token punctuation">{</span>queryString<span class="token punctuation">}</span>
<span class="token punctuation">,</span>
        <span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> headers <span class="token punctuation">}</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>response<span class="token punctuation">.</span><span class="token property-access">ok</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Failed</span> to <span class="token keyword">get</span> <span class="token literal-property property">quote</span><span class="token operator">:</span> $<span class="token punctuation">{</span><span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">text</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>data<span class="token punctuation">.</span><span class="token property-access">code</span> <span class="token operator">!==</span> <span class="token string">"0"</span> <span class="token operator">||</span> <span class="token operator">!</span>data<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token operator">?.</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Failed to get token information"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> quoteData <span class="token operator">=</span> data<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">fromToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">toToken</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">symbol</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenSymbol</span><span class="token punctuation">,</span>
            <span class="token literal-property property">decimals</span><span class="token operator">:</span> <span class="token function">parseInt</span><span class="token punctuation">(</span>quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimal</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token literal-property property">price</span><span class="token operator">:</span> quoteData<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">tokenUnitPrice</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token keyword">function</span> <span class="token function">convertAmount</span><span class="token punctuation">(</span><span class="token parameter">amount<span class="token punctuation">,</span> decimals</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>amount <span class="token operator">||</span> <span class="token function">isNaN</span><span class="token punctuation">(</span><span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">const</span> value <span class="token operator">=</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>value <span class="token operator">&lt;=</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Amount must be greater than 0"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword control-flow">return</span> <span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">floor</span><span class="token punctuation">(</span>value <span class="token operator">*</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> decimals<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>err<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">"Amount conversion error:"</span><span class="token punctuation">,</span> err<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Invalid amount format"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
        <span class="token keyword">const</span> args <span class="token operator">=</span> process<span class="token punctuation">.</span><span class="token property-access">argv</span><span class="token punctuation">.</span><span class="token method function property-access">slice</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>args<span class="token punctuation">.</span><span class="token property-access">length</span> <span class="token operator">&lt;</span> <span class="token number">3</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Usage: ts-node swap.ts &lt;amount&gt; &lt;fromTokenAddress&gt; &lt;toTokenAddress&gt;"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Example: ts-node swap.ts 1.5 0x2::sui::SUI 0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">const</span> <span class="token punctuation">[</span>amount<span class="token punctuation">,</span> fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">]</span> <span class="token operator">=</span> args<span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>userPrivateKey <span class="token operator">||</span> <span class="token operator">!</span>userAddress<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Private key or user address not found"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token comment">// Get token information</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Getting token information..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> tokenInfo <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">getTokenInfo</span><span class="token punctuation">(</span>fromTokenAddress<span class="token punctuation">,</span> toTokenAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">From</span><span class="token operator">:</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span> <span class="token punctuation">(</span>$<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">}</span> decimals<span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">To</span><span class="token operator">:</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span> <span class="token punctuation">(</span>$<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">}</span> decimals<span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token comment">// Convert amount using fetched decimals</span>
        <span class="token keyword">const</span> rawAmount <span class="token operator">=</span> <span class="token function">convertAmount</span><span class="token punctuation">(</span>amount<span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Amount</span> <span class="token keyword">in</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span> base units<span class="token operator">:</span>
<span class="token punctuation">,</span> rawAmount<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token comment">// Get swap quote</span>
        <span class="token keyword">const</span> quoteParams <span class="token operator">=</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">chainId</span><span class="token operator">:</span> <span class="token constant">SUI_CHAIN_ID</span><span class="token punctuation">,</span>
            <span class="token literal-property property">amount</span><span class="token operator">:</span> rawAmount<span class="token punctuation">,</span>
            fromTokenAddress<span class="token punctuation">,</span>
            toTokenAddress<span class="token punctuation">,</span>
            <span class="token literal-property property">slippage</span><span class="token operator">:</span> <span class="token string">"0.5"</span><span class="token punctuation">,</span>
            <span class="token literal-property property">userWalletAddress</span><span class="token operator">:</span> normalizedWalletAddress<span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
        <span class="token comment">// Get swap data</span>
        <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> requestPath <span class="token operator">=</span> <span class="token string">"/api/v5/dex/aggregator/swap"</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> queryString <span class="token operator">=</span> <span class="token string">"?"</span> <span class="token operator">+</span> <span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>quoteParams<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token function">getHeaders</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> requestPath<span class="token punctuation">,</span> queryString<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Requesting swap quote..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> response <span class="token operator">=</span> <span class="token keyword control-flow">await</span> <span class="token function">fetch</span><span class="token punctuation">(</span>
            
<span class="token literal-property property">https</span><span class="token operator">:</span><span class="token operator">/</span><span class="token operator">/</span>web3<span class="token punctuation">.</span><span class="token property-access">okx</span><span class="token punctuation">.</span><span class="token property-access">com$</span><span class="token punctuation">{</span>requestPath<span class="token punctuation">}</span>$<span class="token punctuation">{</span>queryString<span class="token punctuation">}</span>
<span class="token punctuation">,</span>
            <span class="token punctuation">{</span> <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">"GET"</span><span class="token punctuation">,</span> headers <span class="token punctuation">}</span>
        <span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">const</span> data <span class="token operator">=</span> <span class="token keyword control-flow">await</span> response<span class="token punctuation">.</span><span class="token method function property-access">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>data<span class="token punctuation">.</span><span class="token property-access">code</span> <span class="token operator">!==</span> <span class="token string">"0"</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>
<span class="token constant">API</span> <span class="token known-class-name class-name">Error</span><span class="token operator">:</span> $<span class="token punctuation">{</span>data<span class="token punctuation">.</span><span class="token property-access">msg</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">const</span> swapData <span class="token operator">=</span> data<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
        <span class="token comment">// Show estimated output and price impact</span>
        <span class="token keyword">const</span> outputAmount <span class="token operator">=</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>swapData<span class="token punctuation">.</span><span class="token property-access">routerResult</span><span class="token punctuation">.</span><span class="token property-access">toTokenAmount</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token known-class-name class-name">Math</span><span class="token punctuation">.</span><span class="token method function property-access">pow</span><span class="token punctuation">(</span><span class="token number">10</span><span class="token punctuation">,</span> tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap Quote:"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">Input</span><span class="token operator">:</span> $<span class="token punctuation">{</span>amount<span class="token punctuation">}</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span> <span class="token punctuation">(</span>$$<span class="token punctuation">{</span><span class="token punctuation">(</span><span class="token function">parseFloat</span><span class="token punctuation">(</span>amount<span class="token punctuation">)</span> <span class="token operator">*</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">fromToken</span><span class="token punctuation">.</span><span class="token property-access">price</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toFixed</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token literal-property property">Output</span><span class="token operator">:</span> $<span class="token punctuation">{</span>outputAmount<span class="token punctuation">.</span><span class="token method function property-access">toFixed</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">decimals</span><span class="token punctuation">)</span><span class="token punctuation">}</span> $<span class="token punctuation">{</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">symbol</span><span class="token punctuation">}</span> <span class="token punctuation">(</span>$$<span class="token punctuation">{</span><span class="token punctuation">(</span>outputAmount <span class="token operator">*</span> <span class="token function">parseFloat</span><span class="token punctuation">(</span>tokenInfo<span class="token punctuation">.</span><span class="token property-access">toToken</span><span class="token punctuation">.</span><span class="token property-access">price</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toFixed</span><span class="token punctuation">(</span><span class="token number">2</span><span class="token punctuation">)</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>swapData<span class="token punctuation">.</span><span class="token property-access">priceImpactPercentage</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Price</span> <span class="token maybe-class-name">Impact</span><span class="token operator">:</span> $<span class="token punctuation">{</span>swapData<span class="token punctuation">.</span><span class="token property-access">priceImpactPercentage</span><span class="token punctuation">}</span><span class="token operator">%</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nExecuting swap transaction..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> retryCount <span class="token operator">=</span> <span class="token number">0</span><span class="token punctuation">;</span>
        <span class="token keyword control-flow">while</span> <span class="token punctuation">(</span>retryCount <span class="token operator">&lt;</span> <span class="token constant">MAX_RETRIES</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword control-flow">try</span> <span class="token punctuation">{</span>
                <span class="token comment">// Create transaction block</span>
                <span class="token keyword">const</span> txBlock <span class="token operator">=</span> <span class="token maybe-class-name">Transaction</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>swapData<span class="token punctuation">.</span><span class="token property-access">tx</span><span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                txBlock<span class="token punctuation">.</span><span class="token method function property-access">setSender</span><span class="token punctuation">(</span>normalizedWalletAddress<span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token comment">// Set gas parameters</span>
                <span class="token keyword">const</span> referenceGasPrice <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">getReferenceGasPrice</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                txBlock<span class="token punctuation">.</span><span class="token method function property-access">setGasPrice</span><span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span>referenceGasPrice<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                txBlock<span class="token punctuation">.</span><span class="token method function property-access">setGasBudget</span><span class="token punctuation">(</span><span class="token known-class-name class-name">BigInt</span><span class="token punctuation">(</span><span class="token constant">DEFAULT_GAS_BUDGET</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token comment">// Build and sign transaction</span>
                <span class="token keyword">const</span> builtTx <span class="token operator">=</span> <span class="token keyword control-flow">await</span> txBlock<span class="token punctuation">.</span><span class="token method function property-access">build</span><span class="token punctuation">(</span><span class="token punctuation">{</span> client <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">const</span> txBytes <span class="token operator">=</span> <span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>builtTx<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token string">'base64'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">const</span> signedTx <span class="token operator">=</span> <span class="token keyword control-flow">await</span> wallet<span class="token punctuation">.</span><span class="token method function property-access">signTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
                    <span class="token literal-property property">privateKey</span><span class="token operator">:</span> userPrivateKey<span class="token punctuation">,</span>
                    <span class="token literal-property property">data</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                        <span class="token literal-property property">type</span><span class="token operator">:</span> <span class="token string">'raw'</span><span class="token punctuation">,</span>
                        <span class="token literal-property property">data</span><span class="token operator">:</span> txBytes
                    <span class="token punctuation">}</span>
                <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>signedTx<span class="token operator">?.</span>signature<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token string">"Failed to sign transaction"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token punctuation">}</span>
                <span class="token comment">// Execute transaction</span>
                <span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">executeTransactionBlock</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
                    <span class="token literal-property property">transactionBlock</span><span class="token operator">:</span> builtTx<span class="token punctuation">,</span>
                    <span class="token literal-property property">signature</span><span class="token operator">:</span> <span class="token punctuation">[</span>signedTx<span class="token punctuation">.</span><span class="token property-access">signature</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                    <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                        <span class="token literal-property property">showEffects</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token literal-property property">showEvents</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token comment">// Wait for confirmation</span>
                <span class="token keyword">const</span> confirmation <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token method function property-access">waitForTransaction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
                    <span class="token literal-property property">digest</span><span class="token operator">:</span> result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">,</span>
                    <span class="token literal-property property">options</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                        <span class="token literal-property property">showEffects</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token literal-property property">showEvents</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"\nSwap completed successfully!"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Transaction ID:"</span><span class="token punctuation">,</span> result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> 
<span class="token literal-property property">https</span><span class="token operator">:</span><span class="token operator">/</span><span class="token operator">/</span>suiscan<span class="token punctuation">.</span><span class="token property-access">xyz</span><span class="token operator">/</span>mainnet<span class="token operator">/</span>tx<span class="token operator">/</span>$<span class="token punctuation">{</span>result<span class="token punctuation">.</span><span class="token property-access">digest</span><span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
                process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Attempt</span> $<span class="token punctuation">{</span>retryCount <span class="token operator">+</span> <span class="token number">1</span><span class="token punctuation">}</span> failed<span class="token operator">:</span>
<span class="token punctuation">,</span> error<span class="token punctuation">)</span><span class="token punctuation">;</span>
                retryCount<span class="token operator">++</span><span class="token punctuation">;</span>
                <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>retryCount <span class="token operator">===</span> <span class="token constant">MAX_RETRIES</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword control-flow">throw</span> error<span class="token punctuation">;</span>
                <span class="token punctuation">}</span>
                <span class="token keyword control-flow">await</span> <span class="token keyword">new</span> <span class="token class-name">Promise</span><span class="token punctuation">(</span><span class="token parameter">resolve</span> <span class="token arrow operator">=&gt;</span> <span class="token function">setTimeout</span><span class="token punctuation">(</span>resolve<span class="token punctuation">,</span> <span class="token number">2000</span> <span class="token operator">*</span> retryCount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span> <span class="token keyword control-flow">catch</span> <span class="token punctuation">(</span>error<span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">error</span><span class="token punctuation">(</span><span class="token string">"Error:"</span><span class="token punctuation">,</span> error <span class="token keyword">instanceof</span> <span class="token class-name">Error</span> <span class="token operator">?</span> error<span class="token punctuation">.</span><span class="token property-access">message</span> <span class="token operator">:</span> <span class="token string">"Unknown error"</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        process<span class="token punctuation">.</span><span class="token method function property-access">exit</span><span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>require<span class="token punctuation">.</span><span class="token property-access">main</span> <span class="token operator">===</span> module<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token function">main</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="方法2：SDK方法" id="方法2：sdk方法">方法2：SDK方法<a class="index_header-anchor__Xqb+L" href="#方法2：sdk方法" style="opacity:0">#</a></h2>
<p>OKX DEX SDK 提供了更简单的开发人员体验，同时保留了API方法的所有功能。SDK为你处理许多实现细节，包括重试逻辑、错误处理和交易管理。</p>
<h2 data-content="1. 安装SDK" id="1.-安装sdk">1. 安装SDK<a class="index_header-anchor__Xqb+L" href="#1.-安装sdk" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okx-dex/okx-dex-sdk
or
<span class="token function">yarn</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
or
<span class="token function">pnpm</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
</code></pre></div>
<h2 data-content="2. 设置环境" id="2.-设置环境">2. 设置环境<a class="index_header-anchor__Xqb+L" href="#2.-设置环境" style="opacity:0">#</a></h2>
<p>使用你的API凭据和钱包信息创建一个. env文件：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">OKX API Credentials
<span class="token assign-left variable">OKX_API_KEY</span><span class="token operator">=</span>your_api_key
<span class="token assign-left variable">OKX_SECRET_KEY</span><span class="token operator">=</span>your_secret_key
<span class="token assign-left variable">OKX_API_PASSPHRASE</span><span class="token operator">=</span>your_passphrase
<span class="token assign-left variable">OKX_PROJECT_ID</span><span class="token operator">=</span>your_project_id
Sui Configuration
<span class="token assign-left variable">SUI_WALLET_ADDRESS</span><span class="token operator">=</span>your_sui_wallet_address
<span class="token assign-left variable">SUI_PRIVATE_KEY</span><span class="token operator">=</span>your_sui_private_key
请记住，你需要使用SUI私钥的hexWithouse tFlag格式，你可以使用SUICLI获得：
sui keytool convert <span class="token operator">&lt;</span>your_sui_private_key<span class="token operator">&gt;</span>
</code></pre></div>
<h2 data-content="3. 初始化客户端" id="3.-初始化客户端">3. 初始化客户端<a class="index_header-anchor__Xqb+L" href="#3.-初始化客户端" style="opacity:0">#</a></h2>
<p>为你的DEX客户端创建一个文件（例如，DexClient. ts）：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// DexClient.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">OKXDexClient</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@okx-dex/okx-dex-sdk'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token string">'dotenv/config'</span><span class="token punctuation">;</span>
<span class="token comment">// Validate environment variables</span>
<span class="token keyword">const</span> requiredEnvVars <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token string">'OKX_API_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_SECRET_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_API_PASSPHRASE'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_PROJECT_ID'</span><span class="token punctuation">,</span>
    <span class="token string">'SUI_WALLET_ADDRESS'</span><span class="token punctuation">,</span>
    <span class="token string">'SUI_PRIVATE_KEY'</span>
<span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword control-flow">for</span> <span class="token punctuation">(</span><span class="token keyword">const</span> envVar <span class="token keyword">of</span> requiredEnvVars<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">[</span>envVar<span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span>
<span class="token maybe-class-name">Missing</span> required environment variable<span class="token operator">:</span> $<span class="token punctuation">{</span>envVar<span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Initialize the client</span>
<span class="token keyword module">export</span> <span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXDexClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">apiKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">secretKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">apiPassphrase</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">projectId</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">sui</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">privateKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SUI_PRIVATE_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
        <span class="token literal-property property">walletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SUI_WALLET_ADDRESS</span><span class="token operator">!</span><span class="token punctuation">,</span>
        <span class="token literal-property property">connection</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">rpcUrl</span><span class="token operator">:</span> <span class="token string">'https://sui-mainnet.blockvision.org'</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="4. 创建代币助手（可选）" id="4.-创建代币助手（可选）">4. 创建代币助手（可选）<a class="index_header-anchor__Xqb+L" href="#4.-创建代币助手（可选）" style="opacity:0">#</a></h2>
<p>你可以创建一个代币列表助手以便于参考：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token comment">// Common tokens on Sui mainnet</span>
<span class="token keyword module">export</span> <span class="token keyword">const</span> <span class="token constant">TOKENS</span> <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token constant">SUI</span><span class="token operator">:</span> <span class="token string">"0x2::sui::SUI"</span><span class="token punctuation">,</span>
    <span class="token constant">USDC</span><span class="token operator">:</span> <span class="token string">"0xdba34672e30cb065b1f93e3ab55318768fd6fef66c15942c9f7cb846e2f900e7::usdc::USDC"</span>
<span class="token punctuation">}</span> <span class="token keyword module">as</span> <span class="token keyword">const</span><span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="5. 调用SDK执行兑换" id="5.-调用sdk执行兑换">5. 调用SDK执行兑换<a class="index_header-anchor__Xqb+L" href="#5.-调用sdk执行兑换" style="opacity:0">#</a></h2>
<p>创建兑换执行的文件：</p>
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

## 附加<span class="token constant">SDK</span>功能
<span class="token constant">SDK</span>提供了简化开发的附加方法：
获取代币对的报价

<span class="token template-string"><span class="token template-punctuation string">`</span><span class="token template-punctuation string">`</span></span>`javascript
<span class="token keyword">const</span> quote <span class="token operator">=</span> <span class="token keyword control-flow">await</span> client<span class="token punctuation">.</span><span class="token property-access">dex</span><span class="token punctuation">.</span><span class="token method function property-access">getQuote</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
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
    "交易 API",
    "搭建兑换应用",
    "在 Sui 链上搭建兑换应用"
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
    "1. 设置环境",
    "2. 获取代币信息和兑换报价",
    "3. 处理和签署交易",
    "4. 执行交易",
    "5. 完整实现",
    "方法2：SDK方法",
    "1. 安装SDK",
    "2. 设置环境",
    "3. 初始化客户端",
    "4. 创建代币助手（可选）",
    "5. 调用SDK执行兑换"
  ]
}
```

</details>
