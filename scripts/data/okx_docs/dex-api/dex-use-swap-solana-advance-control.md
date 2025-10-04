# 在 Solana 链上兑换的高级用法 | 搭建兑换应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-swap-solana-advance-control#5.-处理地址查找表  
**抓取时间:** 2025-05-27 02:24:04  
**字数:** 925

## 导航路径
DEX API > 交易 API > 搭建兑换应用 > 在 Solana 链上兑换的高级用法

## 目录
- 1. 设置环境
- 2. 初始化连接和钱包
- 3. 配置兑换参数
- 4. 处理兑换指令
- 5. 处理地址查找表
- 6. 创建并签名交易
- 7. 执行交易
- 最佳实践和注意事项

---

在 Solana 链上兑换的高级用法
#
当你需要对兑换过程进行更多控制和组装定制时，可使用 swap-instruction 接口。
已有的 /swap 兑换接口的作用是，直接返回了构建好的交易数据，可直接签名执行。但 swap-instruction 兑换指令接口允许你：
构建自定义的交易签名流程
按照你的需要处理指令
在已构建的交易添加自己的指令
直接使用查找表来优化交易数据大小
本指南将逐步介绍，如何使用兑换指令接口发起一笔完整的兑换交易。 你将了解如何从 API 接口中获取指令、组装处理它们并将其构建成一个可用的交易。
1. 设置环境
#
导入必要的库并配置 你的环境：
// 与 DEX 交互所需的 Solana 依赖项
import
{
Connection
,
// 处理与 Solana 网络的 RPC 连接
Keypair
,
// 管理用于签名的钱包密钥对
PublicKey
,
// 处理 Solana 公钥的转换和验证
TransactionInstruction
,
// 核心交易指令类型
TransactionMessage
,
// 构建交易消息（v0 格式）
VersionedTransaction
,
// 支持带有查找表的新交易格式
RpcResponseAndContext
,
// RPC 响应包装类型
SimulatedTransactionResponse
,
// 模拟结果类型
AddressLookupTableAccount
,
// 用于交易大小优化
PublicKeyInitData
// 公钥输入类型
}
from
"@solana/web3.js"
;
import
base58
from
"bs58"
;
// 用于私钥解码
import
dotenv
from
"dotenv"
;
// 环境变量管理
dotenv
.
config
(
)
;
2. 初始化连接和钱包
#
设置 你的连接和钱包实例：
// 注意：在生产环境中，请考虑使用具有高速率限制的可靠 RPC 端点
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
// 初始化用于签名的钱包
// 该钱包将作为费用支付者和交易签名者
// 确保它有足够的 SOL 来支付交易费用
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
process
.
env
.
PRIVATE_KEY
?.
toString
(
)
||
""
)
)
)
;
3. 配置兑换参数
#
设置 你的兑换参数：
// 配置交换参数
const
baseUrl
=
"https://beta.okex.org/api/v5/dex/aggregator/swap-instruction"
;
const
params
=
{
chainId
:
"501"
,
// Solana 主网链 ID
feePercent
:
"1"
,
// 你计划收取的分佣费用百分比
amount
:
"1000000"
,
// 最小单位金额（例如，SOL 的 lamports）
fromTokenAddress
:
"11111111111111111111111111111111"
,
// SOL 铸币地址
toTokenAddress
:
"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
,
// USDC 铸币地址
slippage
:
"0.1"
,
// 滑点容忍百分比
userWalletAddress
:
process
.
env
.
WALLET_ADDRESS
||
""
,
// 执行交换的钱包
priceTolerance
:
"0"
,
// 允许的最大价格影响
autoSlippage
:
"false"
,
// 使用固定滑点而非自动滑点
fromTokenReferrerWalletAddress
:
process
.
env
.
WALLET_ADDRESS
||
""
,
// 用于推荐费用
pathNum
:
"3"
// 考虑的最大路由数
}
4. 处理兑换指令
#
获取并处理兑换指令：
// 将 DEX API 指令转换为 Solana 格式的辅助函数
// DEX 返回的指令是自定义格式，需要转换
function
createTransactionInstruction
(
instruction
:
any
)
:
TransactionInstruction
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
// DEX 程序 ID
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
:
any
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
// 如果账户必须签名则为 true
isWritable
:
key
.
isWritable
// 如果指令涉及到修改账户则为 true
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
// 指令参数
}
)
;
}
// 从 DEX 获取最佳交换路由和指令
// 此调用会找到不同 DEX 流动性池中的最佳价格
const
url
=
`
${
baseUrl
}
?
${
new
URLSearchParams
(
params
)
.
toString
(
)
}
`
;
const
{
data
:
{
instructionLists
,
addressLookupTableAccount
}
}
=
await
fetch
(
url
,
{
method
:
'GET'
,
headers
:
{
'Content-Type'
:
'application/json'
}
}
)
.
then
(
res
=>
res
.
json
(
)
)
;
// 将 DEX 指令处理为 Solana 兼容格式
const
instructions
:
TransactionInstruction
[
]
=
[
]
;
// 移除 DEX 返回的重复查找表地址
const
addressLookupTableAccount2
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
"要加载的查找表:"
,
addressLookupTableAccount2
)
;
// 将每个 DEX 指令转换为 Solana 格式
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
5. 处理地址查找表
#
使用地址查找表优化交易数据优化大小
// 使用查找表以优化交易数据大小
// 查找表对于与许多账户交互的复杂兑换至关重要
// 它们显著减少了交易大小和成本
const
addressLookupTableAccounts
:
AddressLookupTableAccount
[
]
=
[
]
;
if
(
addressLookupTableAccount2
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
"加载地址查找表..."
)
;
// 并行获取所有查找表以提高性能
const
lookupTableAccounts
=
await
Promise
.
all
(
addressLookupTableAccount2
.
map
(
async
(
address
:
unknown
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
as
PublicKeyInitData
)
;
// 从 Solana 获取查找表账户数据
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
无法获取查找表账户
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
6. 创建并签名交易
#
创建交易消息并签名:
// 获取最近的 blockhash 以确定交易时间和唯一性
// 交易在此 blockhash 之后的有限时间内有效
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
// 创建版本化交易消息
// V0 消息格式需要支持查找表
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
// 费用支付者地址
recentBlockhash
:
latestBlockhash
.
blockhash
,
// 交易时间
instructions
// 来自 DEX 的兑换指令
}
)
.
compileToV0Message
(
addressLookupTableAccounts
)
;
// 包含查找表
// 创建带有优化的新版本化交易
const
transaction
=
new
VersionedTransaction
(
messageV0
)
;
// 模拟交易以检查错误
// 这有助于在支付费用之前发现问题
const
result
:
RpcResponseAndContext
<
SimulatedTransactionResponse
>
=
await
connection
.
simulateTransaction
(
transaction
)
;
// 使用费用支付者钱包签名交易
const
feePayer
=
Keypair
.
fromSecretKey
(
base58
.
decode
(
process
.
env
.
PRIVATE_KEY
?.
toString
(
)
||
""
)
)
;
transaction
.
sign
(
[
feePayer
]
)
7. 执行交易
#
最后，模拟并发送交易：
// 将交易发送到 Solana
// skipPreflight=false 确保额外的验证
// maxRetries 帮助处理网络问题
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
// 运行预验证
maxRetries
:
5
// 失败时重试
}
)
;
// 记录交易详情
console
.
log
(
"Raw transaction:"
,
transaction
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
"Base58 transaction:"
,
base58
.
encode
(
transaction
.
serialize
(
)
)
)
;
// 记录模拟结果以供调试
console
.
log
(
"=========模拟结果========="
)
;
result
.
value
.
logs
?.
forEach
(
(
log
)
=>
{
console
.
log
(
log
)
;
}
)
;
// 记录交易结果
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
最佳实践和注意事项
#
在实施交换指令时，请记住以下关键点：
错误处理：始终为API响应和事务模拟结果实现正确的错误处理。
防滑保护：根据 你的用例和市场条件选择适当的防滑参数。
Gas优化：在可用时使用地址查找表来减少事务大小和成本。
事务模拟：在发送事务之前始终模拟事务，以便及早发现潜在问题。
重试逻辑：使用适当的退避策略为失败的事务实现适当的重试机制。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="在-solana-链上兑换的高级用法">在 Solana 链上兑换的高级用法<a class="index_header-anchor__Xqb+L" href="#在-solana-链上兑换的高级用法" style="opacity:0">#</a></h1>
<p>当你需要对兑换过程进行更多控制和组装定制时，可使用 swap-instruction 接口。
已有的 /swap 兑换接口的作用是，直接返回了构建好的交易数据，可直接签名执行。但 swap-instruction 兑换指令接口允许你：</p>
<ul>
<li>构建自定义的交易签名流程</li>
<li>按照你的需要处理指令</li>
<li>在已构建的交易添加自己的指令</li>
<li>直接使用查找表来优化交易数据大小</li>
</ul>
<p>本指南将逐步介绍，如何使用兑换指令接口发起一笔完整的兑换交易。 你将了解如何从 API 接口中获取指令、组装处理它们并将其构建成一个可用的交易。</p>
<h2 data-content="1. 设置环境" id="1.-设置环境">1. 设置环境<a class="index_header-anchor__Xqb+L" href="#1.-设置环境" style="opacity:0">#</a></h2>
<p>导入必要的库并配置 你的环境：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 与 DEX 交互所需的 Solana 依赖项</span>
<span class="token keyword">import</span> <span class="token punctuation">{</span>
    Connection<span class="token punctuation">,</span>          <span class="token comment">// 处理与 Solana 网络的 RPC 连接</span>
    Keypair<span class="token punctuation">,</span>            <span class="token comment">// 管理用于签名的钱包密钥对</span>
    PublicKey<span class="token punctuation">,</span>          <span class="token comment">// 处理 Solana 公钥的转换和验证</span>
    TransactionInstruction<span class="token punctuation">,</span>    <span class="token comment">// 核心交易指令类型</span>
    TransactionMessage<span class="token punctuation">,</span>        <span class="token comment">// 构建交易消息（v0 格式）</span>
    VersionedTransaction<span class="token punctuation">,</span>      <span class="token comment">// 支持带有查找表的新交易格式</span>
    RpcResponseAndContext<span class="token punctuation">,</span>     <span class="token comment">// RPC 响应包装类型</span>
    SimulatedTransactionResponse<span class="token punctuation">,</span>  <span class="token comment">// 模拟结果类型</span>
    AddressLookupTableAccount<span class="token punctuation">,</span>     <span class="token comment">// 用于交易大小优化</span>
    PublicKeyInitData              <span class="token comment">// 公钥输入类型</span>
<span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">"@solana/web3.js"</span><span class="token punctuation">;</span>
<span class="token keyword">import</span> base58 <span class="token keyword">from</span> <span class="token string">"bs58"</span><span class="token punctuation">;</span>    <span class="token comment">// 用于私钥解码</span>
<span class="token keyword">import</span> dotenv <span class="token keyword">from</span> <span class="token string">"dotenv"</span><span class="token punctuation">;</span>  <span class="token comment">// 环境变量管理</span>
dotenv<span class="token punctuation">.</span><span class="token function">config</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="2. 初始化连接和钱包" id="2.-初始化连接和钱包">2. 初始化连接和钱包<a class="index_header-anchor__Xqb+L" href="#2.-初始化连接和钱包" style="opacity:0">#</a></h2>
<p>设置 你的连接和钱包实例：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 注意：在生产环境中，请考虑使用具有高速率限制的可靠 RPC 端点</span>
<span class="token keyword">const</span> connection <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Connection</span><span class="token punctuation">(</span>
    process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span> <span class="token operator">||</span> <span class="token string">"https://api.mainnet-beta.solana.com"</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 初始化用于签名的钱包</span>
<span class="token comment">// 该钱包将作为费用支付者和交易签名者</span>
<span class="token comment">// 确保它有足够的 SOL 来支付交易费用</span>
<span class="token keyword">const</span> wallet <span class="token operator">=</span> Keypair<span class="token punctuation">.</span><span class="token function">fromSecretKey</span><span class="token punctuation">(</span>
    Uint8Array<span class="token punctuation">.</span><span class="token function">from</span><span class="token punctuation">(</span>base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">PRIVATE_KEY</span><span class="token operator">?.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">||</span> <span class="token string">""</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="3. 配置兑换参数" id="3.-配置兑换参数">3. 配置兑换参数<a class="index_header-anchor__Xqb+L" href="#3.-配置兑换参数" style="opacity:0">#</a></h2>
<p>设置 你的兑换参数：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 配置交换参数</span>
    <span class="token keyword">const</span> baseUrl <span class="token operator">=</span> <span class="token string">"https://beta.okex.org/api/v5/dex/aggregator/swap-instruction"</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
        chainId<span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>              <span class="token comment">// Solana 主网链 ID</span>
        feePercent<span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>            <span class="token comment">// 你计划收取的分佣费用百分比</span>
        amount<span class="token operator">:</span> <span class="token string">"1000000"</span><span class="token punctuation">,</span>          <span class="token comment">// 最小单位金额（例如，SOL 的 lamports）</span>
        fromTokenAddress<span class="token operator">:</span> <span class="token string">"11111111111111111111111111111111"</span><span class="token punctuation">,</span>  <span class="token comment">// SOL 铸币地址</span>
        toTokenAddress<span class="token operator">:</span> <span class="token string">"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"</span><span class="token punctuation">,</span>  <span class="token comment">// USDC 铸币地址</span>
        slippage<span class="token operator">:</span> <span class="token string">"0.1"</span><span class="token punctuation">,</span>            <span class="token comment">// 滑点容忍百分比</span>
        userWalletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">WALLET_ADDRESS</span> <span class="token operator">||</span> <span class="token string">""</span><span class="token punctuation">,</span>   <span class="token comment">// 执行交换的钱包</span>
        priceTolerance<span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>        <span class="token comment">// 允许的最大价格影响</span>
        autoSlippage<span class="token operator">:</span> <span class="token string">"false"</span><span class="token punctuation">,</span>      <span class="token comment">// 使用固定滑点而非自动滑点</span>
        fromTokenReferrerWalletAddress<span class="token operator">:</span> process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">WALLET_ADDRESS</span> <span class="token operator">||</span> <span class="token string">""</span><span class="token punctuation">,</span>  <span class="token comment">// 用于推荐费用</span>
        pathNum<span class="token operator">:</span> <span class="token string">"3"</span>                 <span class="token comment">// 考虑的最大路由数</span>
    <span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="4. 处理兑换指令" id="4.-处理兑换指令">4. 处理兑换指令<a class="index_header-anchor__Xqb+L" href="#4.-处理兑换指令" style="opacity:0">#</a></h2>
<p>获取并处理兑换指令：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 将 DEX API 指令转换为 Solana 格式的辅助函数</span>
<span class="token comment">// DEX 返回的指令是自定义格式，需要转换</span>
<span class="token keyword">function</span> <span class="token function">createTransactionInstruction</span><span class="token punctuation">(</span>instruction<span class="token operator">:</span> <span class="token builtin">any</span><span class="token punctuation">)</span><span class="token operator">:</span> TransactionInstruction <span class="token punctuation">{</span>
    <span class="token keyword">return</span> <span class="token keyword">new</span> <span class="token class-name">TransactionInstruction</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
        programId<span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>instruction<span class="token punctuation">.</span>programId<span class="token punctuation">)</span><span class="token punctuation">,</span>  <span class="token comment">//  DEX 程序 ID</span>
        keys<span class="token operator">:</span> instruction<span class="token punctuation">.</span>accounts<span class="token punctuation">.</span><span class="token function">map</span><span class="token punctuation">(</span><span class="token punctuation">(</span>key<span class="token operator">:</span> <span class="token builtin">any</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">(</span><span class="token punctuation">{</span>            pubkey<span class="token operator">:</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>key<span class="token punctuation">.</span>pubkey<span class="token punctuation">)</span><span class="token punctuation">,</span>    <span class="token comment">// Account address</span>
            isSigner<span class="token operator">:</span> key<span class="token punctuation">.</span>isSigner<span class="token punctuation">,</span>     <span class="token comment">// 如果账户必须签名则为 true</span>
            isWritable<span class="token operator">:</span> key<span class="token punctuation">.</span>isWritable  <span class="token comment">// 如果指令涉及到修改账户则为 true</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        data<span class="token operator">:</span> Buffer<span class="token punctuation">.</span><span class="token function">from</span><span class="token punctuation">(</span>instruction<span class="token punctuation">.</span>data<span class="token punctuation">,</span> <span class="token string">'base64'</span><span class="token punctuation">)</span>  <span class="token comment">// 指令参数</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// 从 DEX 获取最佳交换路由和指令</span>
<span class="token comment">// 此调用会找到不同 DEX 流动性池中的最佳价格</span>
<span class="token keyword">const</span> url <span class="token operator">=</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>baseUrl<span class="token interpolation-punctuation punctuation">}</span></span><span class="token string">?</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span><span class="token keyword">new</span> <span class="token class-name">URLSearchParams</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">;</span>
<span class="token keyword">const</span> <span class="token punctuation">{</span> data<span class="token operator">:</span> <span class="token punctuation">{</span> instructionLists<span class="token punctuation">,</span> addressLookupTableAccount <span class="token punctuation">}</span> <span class="token punctuation">}</span> <span class="token operator">=</span>
    <span class="token keyword">await</span> <span class="token function">fetch</span><span class="token punctuation">(</span>url<span class="token punctuation">,</span> <span class="token punctuation">{</span>
        method<span class="token operator">:</span> <span class="token string">'GET'</span><span class="token punctuation">,</span>
        headers<span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token string-property property">'Content-Type'</span><span class="token operator">:</span> <span class="token string">'application/json'</span> <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">then</span><span class="token punctuation">(</span>res <span class="token operator">=&gt;</span> res<span class="token punctuation">.</span><span class="token function">json</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 将 DEX 指令处理为 Solana 兼容格式</span>
<span class="token keyword">const</span> instructions<span class="token operator">:</span> TransactionInstruction<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token comment">// 移除 DEX 返回的重复查找表地址</span>
<span class="token keyword">const</span> addressLookupTableAccount2 <span class="token operator">=</span> <span class="token builtin">Array</span><span class="token punctuation">.</span><span class="token function">from</span><span class="token punctuation">(</span><span class="token keyword">new</span> <span class="token class-name">Set</span><span class="token punctuation">(</span>addressLookupTableAccount<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"要加载的查找表:"</span><span class="token punctuation">,</span> addressLookupTableAccount2<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 将每个 DEX 指令转换为 Solana 格式</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span>instructionLists<span class="token operator">?.</span>length<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    instructions<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token operator">...</span>instructionLists<span class="token punctuation">.</span><span class="token function">map</span><span class="token punctuation">(</span>createTransactionInstruction<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="5. 处理地址查找表" id="5.-处理地址查找表">5. 处理地址查找表<a class="index_header-anchor__Xqb+L" href="#5.-处理地址查找表" style="opacity:0">#</a></h2>
<p>使用地址查找表优化交易数据优化大小</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 使用查找表以优化交易数据大小</span>
<span class="token comment">// 查找表对于与许多账户交互的复杂兑换至关重要</span>
<span class="token comment">// 它们显著减少了交易大小和成本</span>
<span class="token keyword">const</span> addressLookupTableAccounts<span class="token operator">:</span> AddressLookupTableAccount<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword">if</span> <span class="token punctuation">(</span>addressLookupTableAccount2<span class="token operator">?.</span>length <span class="token operator">&gt;</span> <span class="token number">0</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"加载地址查找表..."</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
     <span class="token comment">// 并行获取所有查找表以提高性能</span>
    <span class="token keyword">const</span> lookupTableAccounts <span class="token operator">=</span> <span class="token keyword">await</span> <span class="token builtin">Promise</span><span class="token punctuation">.</span><span class="token function">all</span><span class="token punctuation">(</span>
        addressLookupTableAccount2<span class="token punctuation">.</span><span class="token function">map</span><span class="token punctuation">(</span><span class="token keyword">async</span> <span class="token punctuation">(</span>address<span class="token operator">:</span> <span class="token builtin">unknown</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token keyword">const</span> pubkey <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">PublicKey</span><span class="token punctuation">(</span>address <span class="token keyword">as</span> PublicKeyInitData<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token comment">// 从 Solana 获取查找表账户数据</span>
            <span class="token keyword">const</span> account <span class="token operator">=</span> <span class="token keyword">await</span> connection
                <span class="token punctuation">.</span><span class="token function">getAddressLookupTable</span><span class="token punctuation">(</span>pubkey<span class="token punctuation">)</span>
                <span class="token punctuation">.</span><span class="token function">then</span><span class="token punctuation">(</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> res<span class="token punctuation">.</span>value<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>account<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token keyword">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">无法获取查找表账户 </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>address<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
            <span class="token keyword">return</span> account<span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    addressLookupTableAccounts<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token operator">...</span>lookupTableAccounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="6. 创建并签名交易" id="6.-创建并签名交易">6. 创建并签名交易<a class="index_header-anchor__Xqb+L" href="#6.-创建并签名交易" style="opacity:0">#</a></h2>
<p>创建交易消息并签名:</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 获取最近的 blockhash 以确定交易时间和唯一性</span>
<span class="token comment">// 交易在此 blockhash 之后的有限时间内有效</span>
<span class="token keyword">const</span> latestBlockhash <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">getLatestBlockhash</span><span class="token punctuation">(</span><span class="token string">'finalized'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 创建版本化交易消息</span>
<span class="token comment">// V0 消息格式需要支持查找表</span>
<span class="token keyword">const</span> messageV0 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">TransactionMessage</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    payerKey<span class="token operator">:</span> wallet<span class="token punctuation">.</span>publicKey<span class="token punctuation">,</span>     <span class="token comment">// 费用支付者地址</span>
    recentBlockhash<span class="token operator">:</span> latestBlockhash<span class="token punctuation">.</span>blockhash<span class="token punctuation">,</span>  <span class="token comment">// 交易时间</span>
    instructions                     <span class="token comment">// 来自 DEX 的兑换指令</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">compileToV0Message</span><span class="token punctuation">(</span>addressLookupTableAccounts<span class="token punctuation">)</span><span class="token punctuation">;</span>  <span class="token comment">// 包含查找表</span>

<span class="token comment">// 创建带有优化的新版本化交易</span>
<span class="token keyword">const</span> transaction <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">VersionedTransaction</span><span class="token punctuation">(</span>messageV0<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 模拟交易以检查错误</span>
<span class="token comment">// 这有助于在支付费用之前发现问题</span>
<span class="token keyword">const</span> result<span class="token operator">:</span> RpcResponseAndContext<span class="token operator">&lt;</span>SimulatedTransactionResponse<span class="token operator">&gt;</span> <span class="token operator">=</span>
    <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">simulateTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 使用费用支付者钱包签名交易</span>
<span class="token keyword">const</span> feePayer <span class="token operator">=</span> Keypair<span class="token punctuation">.</span><span class="token function">fromSecretKey</span><span class="token punctuation">(</span>
    base58<span class="token punctuation">.</span><span class="token function">decode</span><span class="token punctuation">(</span>process<span class="token punctuation">.</span>env<span class="token punctuation">.</span><span class="token constant">PRIVATE_KEY</span><span class="token operator">?.</span><span class="token function">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">||</span> <span class="token string">""</span><span class="token punctuation">)</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
transaction<span class="token punctuation">.</span><span class="token function">sign</span><span class="token punctuation">(</span><span class="token punctuation">[</span>feePayer<span class="token punctuation">]</span><span class="token punctuation">)</span>
</code></pre></div>
<h2 data-content="7. 执行交易" id="7.-执行交易">7. 执行交易<a class="index_header-anchor__Xqb+L" href="#7.-执行交易" style="opacity:0">#</a></h2>
<p>最后，模拟并发送交易：</p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 将交易发送到 Solana</span>
<span class="token comment">// skipPreflight=false 确保额外的验证</span>
<span class="token comment">// maxRetries 帮助处理网络问题</span>
<span class="token keyword">const</span> txId <span class="token operator">=</span> <span class="token keyword">await</span> connection<span class="token punctuation">.</span><span class="token function">sendRawTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    skipPreflight<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>  <span class="token comment">// 运行预验证</span>
    maxRetries<span class="token operator">:</span> <span class="token number">5</span>         <span class="token comment">// 失败时重试</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 记录交易详情</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Raw transaction:"</span><span class="token punctuation">,</span> transaction<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Base58 transaction:"</span><span class="token punctuation">,</span> base58<span class="token punctuation">.</span><span class="token function">encode</span><span class="token punctuation">(</span>transaction<span class="token punctuation">.</span><span class="token function">serialize</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 记录模拟结果以供调试</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"=========模拟结果========="</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
result<span class="token punctuation">.</span>value<span class="token punctuation">.</span>logs<span class="token operator">?.</span><span class="token function">forEach</span><span class="token punctuation">(</span><span class="token punctuation">(</span>log<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>log<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 记录交易结果</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Transaction ID:"</span><span class="token punctuation">,</span> txId<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">"Explorer URL:"</span><span class="token punctuation">,</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">https://solscan.io/tx/</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>txId<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="最佳实践和注意事项" id="最佳实践和注意事项">最佳实践和注意事项<a class="index_header-anchor__Xqb+L" href="#最佳实践和注意事项" style="opacity:0">#</a></h2>
<p>在实施交换指令时，请记住以下关键点：</p>
<ul>
<li>错误处理：始终为API响应和事务模拟结果实现正确的错误处理。</li>
<li>防滑保护：根据 你的用例和市场条件选择适当的防滑参数。</li>
<li>Gas优化：在可用时使用地址查找表来减少事务大小和成本。</li>
<li>事务模拟：在发送事务之前始终模拟事务，以便及早发现潜在问题。</li>
<li>重试逻辑：使用适当的退避策略为失败的事务实现适当的重试机制。</li>
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
    "搭建兑换应用",
    "在 Solana 链上兑换的高级用法"
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
    "1. 设置环境",
    "2. 初始化连接和钱包",
    "3. 配置兑换参数",
    "4. 处理兑换指令",
    "5. 处理地址查找表",
    "6. 创建并签名交易",
    "7. 执行交易",
    "最佳实践和注意事项"
  ]
}
```

</details>
