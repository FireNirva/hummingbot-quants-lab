# 跨链兑换 | API 参考 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-crosschain-swap#请求地址  
**抓取时间:** 2025-05-27 04:20:23  
**字数:** 493

## 导航路径
DEX API > 交易 API > API 参考 > 跨链兑换

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
- 获取支持的链
- 获取币种列表
- 获取仅跨链桥交易的币种列表
- 获取仅通过跨链桥交易的币对列表
- 获取支持的桥信息
- 获取路径信息
- 交易授权
- 跨链兑换
- 查询交易状态
- 支持的跨链桥
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 错误码

---

DEX API
交易 API
跨链 API
API 参考
跨链兑换
跨链兑换
#
获取跨链兑换所需的交易数据。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/cross-chain/build-tx
请求参数
#
参数
类型
必传
描述
fromChainIndex
String
是
源链 ID (如
1
: Ethereum，更多可查看
链 ID 列表
)
fromChainId
String
是
源链 ID。即将废弃
toChainIndex
String
是
目标链 ID (如
1
: Ethereum，更多可查看
链 ID 列表
)
toChainId
String
是
目标链 ID 。即将废弃
fromTokenAddress
String
是
询价币种合约地址 (如
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
)
toTokenAddress
String
是
目标币种合约地址 (如
TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8
)
amount
String
是
币种询价数量 币种询价数量
(数量需包含精度，如授权
1.00
USDT 需输入
1000000
，授权
1.00
DAI 需输入
1000000000000000000
),币种精度可透过
币种列表
取得
slippage
String
是
滑点限制，最小值：
0.002
，最大值：
0.5
。（如：0.005代表你接受这笔交易最大 0.5%滑点，0.5 就代表你接受这笔交易最大 50%的滑点）
1. 如果只通过跨链桥把同一个token X 从A链跨到b链，推荐滑点设定0.002
2. 如果除了通过跨链桥把token X 从A链跨到b链，还涉及到其他币别转换，推荐滑点设定0.01-0.025，实际滑点设置需同时考量币别交易量
sort
String
否
跨链路径选择,默认返回 1
0 代表预计获得数量最多的路径
1 代表综合计算获得数量、网络费用、滑点、跨链桥费后的最优路径
2 代表最快路径，是耗时最少的路径
dexIds
String
否
限定询价的流动性池 dexId , 多个组合按 , 分隔 (如 1,50,180 ，更多可查看流动性列表)
userWalletAddress
String
是
用户钱包地址，AA钱包地址暂不支持跨链交易 (如
0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9
)
allowBridge
Array
否
指定该跨链桥是否包含在路径里面 (如
[211,235]
)
denyBridge
Array
否
指定该跨链桥是否不包含在路径里面 (如
[211,235]
)
receiveAddress
String
否
用于自定义设置目标币种的接收地址，如果未设置则返回用户发送交易的钱包地址。TRON, SUI 以及其他非 EVM 链，需要设置自定义接收地址。 (如：
0x3f6a3f57569358a512ccc0e513f171516b0fd42a
)
feePercent
String
否
发送到分佣地址的询价币种数量百分比
最小百分比：0
最大百分比：3
注意
跨链分佣目前仅支持从
fromtoken
询价币种分佣 。
referrerAddress
String
否
分佣地址 (如：0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9)
收取分佣费用的地址。使用 API 时，可结合 feePercent 设置佣金比例。
注意：
1. 对于
EVM
：此处不支持涉及打包币对的交易，例如 ETH 和 WETH 的交易
2. 对于
Solana
：分佣地址需提前存入一些 SOL 进行激活。
priceImpactProtectionPercentage
String
否
(可选，默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。
当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。
这是一个
可选开启
的功能，默认值为 0.9。当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。
注意：
当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。
onlyBridge
boolean
否
仅通过跨链桥完成跨链交易，不涉及源链兑换以及目标链兑换。
memo
String
否
你可以自定义 /build-tx 中携带的参数，数据编码为长度固定为 64 字节、128 个字符长度的 16 进制字符串，并可通过 /status API 查询。
响应参数
#
参数
类型
描述
fromTokenAmount
String
询价币种的兑换数量
(数量需包含精度，如
1.00
USDT 则为
1000000
)
toTokenAmount
String
目标币种的兑换数量
(数量需包含精度，如
1.00
USDT 则为
1000000
)
minmumReceive
String
目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量)
router
Object
跨链桥基础信息
bridgeId
Integer
跨链桥 ID (如：
211
)
bridgeName
String
跨链桥名称 (如：
cBridge
)
otherNativeFee
String
部分跨链桥会额外收取一定数量的源链主网币，作为跨链桥手续费，并不是所有跨链桥都会收取该部分费用。目前收取该费用的跨链桥有 Stargate、Wanchain、Arbitrum 官方桥、zkSync Era 官方桥、Linea 官方桥。 使用该三方桥需支付
otherNativeFee
才能完成交易。
crossChainFee
String
跨链桥收取的费用，一般为稳定币或者WETH
crossChainFeeTokenAddress
String
跨链桥费币种信息（如：
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
代表主网代币地址）
tx
Object
交易上链所需的数据信息
data
String
上链 inputData 数据
from
String
用户钱包地址 (如：
0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9
)
to
String
欧易 DEX router 合约地址 (如：
0x6dc1fb08decf9f95a01222baa359aa0e02e07716
)
value
String
与合约交互的主链币数量 (wei) (如：
0
)
gasLimit
String
gas费用限额 (交易的gas (单位：wei)。如果该值太低，无法实现报价，则会返回错误信息) (如：
50000
)
gasPrice
String
以 wei 位单位的 Gas price (如：
110000000
)
maxPriorityFeePerGas
String
EIP-1559:每单位 gas 优先费用的推荐值 (如：
500000000
)
randomKeyAccount
Array
随机私钥账户参数并不是每次交易都需要。仅在某些特殊交易（例如使用CCTP桥进行代币跨链）时，才会生成和返回这个随机私钥账户。提供此参数时，您必须使用它与用户的钱包私钥一起进行多签操作，以确保交易的安全和顺利完成。点击此处查看
多签示例
signatureData
Array
如果返回此参数，则代表该交易需要额外的签名数据。开发者应将此参数作为交易签名的输入之一，并确保其在签名过程中正确应用。
交易授权
查询交易状态
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/cross-chain/build-tx?amount=15&fromChainIndex=324&toChainIndex=42161&fromTokenAddress=0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4&toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&slippage=0.07&userWalletAddress=0x22497668Fb12BA21E6A132de7168D0Ecc69cDF7d&feePercent=1&referrerAddress=0x3f6a3f57569358a512ccc0e513f171516b0fd42a'
\
--header
'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'
\
--header
'OK-ACCESS-SIGN: leaV********3uw='
\
--header
'OK-ACCESS-PASSPHRASE: 1****6'
\
--header
'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'
响应示例
#
200
{
"code"
:
0
,
"msg"
:
""
,
"data"
:
[
{
"fromTokenAmount"
:
"1000000000000"
,
"router"
:
{
"bridgeId"
:
235
,
"bridgeName"
:
"swft"
,
"crossChainFee"
:
"4.67131461"
,
"otherNativeFee"
:
"1.50000000"
,
"crossChainFeeTokenAddress"
:
"0x6b175474e89094c44da98b954eedeac495271d0f"
}
,
"toTokenAmount"
:
"1000000000000"
,
"minmumReceive"
:
"1000000000000"
,
"tx"
:
{
"data"
:
"0xc748673057861a797275cd8a068abb95a902e8de"
,
"from"
:
"0x6dc1fb08decf9f95a01222baa359aa0e02e07716"
,
"to"
:
"0x6dc1fb08decf9f95a01222baa359aa0e02e07716"
,
"value"
:
0
,
"gasLimit"
:
"442621"
,
"gasPrice"
:
"3192374970"
,
"maxPriorityFeePerGas"
:
"3599"
"randomKeyAccount"
:
[
"xxxxxxx0x6dc1fb08decf9f95a01222baa359aa0e02e079999"
]
}
}
]
}
交易授权
查询交易状态

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">跨链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-swap" style="color:inherit">跨链兑换</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="跨链兑换">跨链兑换<a class="index_header-anchor__Xqb+L" href="#跨链兑换" style="opacity:0">#</a></h1><p>获取跨链兑换所需的交易数据。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/cross-chain/build-tx</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>fromChainIndex</td><td>String</td><td>是</td><td>源链 ID (如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">链 ID 列表</a>)</td></tr><tr><td>fromChainId</td><td>String</td><td>是</td><td>源链 ID。即将废弃</td></tr><tr><td>toChainIndex</td><td>String</td><td>是</td><td>目标链 ID (如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">链 ID 列表</a>)</td></tr><tr><td>toChainId</td><td>String</td><td>是</td><td>目标链 ID 。即将废弃</td></tr><tr><td>fromTokenAddress</td><td>String</td><td>是</td><td>询价币种合约地址 (如<code>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</code>)</td></tr><tr><td>toTokenAddress</td><td>String</td><td>是</td><td>目标币种合约地址 (如<code>TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8</code>)</td></tr><tr><td>amount</td><td>String</td><td>是</td><td>币种询价数量  币种询价数量 <br/> (数量需包含精度，如授权 <code>1.00</code> USDT 需输入 <code>1000000</code>，授权 <code>1.00</code> DAI 需输入 <code>1000000000000000000</code>),币种精度可透过<a href="/zh-hans/build/dev-docs/dex-crosschain-get-tokens">币种列表</a>取得</td></tr><tr><td>slippage</td><td>String</td><td>是</td><td>滑点限制，最小值：<code>0.002</code>，最大值：<code>0.5</code>。（如：0.005代表你接受这笔交易最大 0.5%滑点，0.5 就代表你接受这笔交易最大 50%的滑点）<br/> 1. 如果只通过跨链桥把同一个token X 从A链跨到b链，推荐滑点设定0.002 <br/> 2. 如果除了通过跨链桥把token X 从A链跨到b链，还涉及到其他币别转换，推荐滑点设定0.01-0.025，实际滑点设置需同时考量币别交易量</td></tr><tr><td>sort</td><td>String</td><td>否</td><td>跨链路径选择,默认返回 1 <br/> <br/> 0 代表预计获得数量最多的路径 <br/> <br/> 1 代表综合计算获得数量、网络费用、滑点、跨链桥费后的最优路径 <br/> <br/> 2 代表最快路径，是耗时最少的路径</td></tr><tr><td>dexIds</td><td>String</td><td>否</td><td>限定询价的流动性池 dexId , 多个组合按 , 分隔 (如 1,50,180 ，更多可查看流动性列表)</td></tr><tr><td>userWalletAddress</td><td>String</td><td>是</td><td>用户钱包地址，AA钱包地址暂不支持跨链交易 (如<code>0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9</code>)</td></tr><tr><td>allowBridge</td><td>Array</td><td>否</td><td>指定该跨链桥是否包含在路径里面 (如<code>[211,235]</code>)</td></tr><tr><td>denyBridge</td><td>Array</td><td>否</td><td>指定该跨链桥是否不包含在路径里面 (如<code>[211,235]</code>)</td></tr><tr><td>receiveAddress</td><td>String</td><td>否</td><td>用于自定义设置目标币种的接收地址，如果未设置则返回用户发送交易的钱包地址。TRON, SUI 以及其他非 EVM 链，需要设置自定义接收地址。 (如：<code>0x3f6a3f57569358a512ccc0e513f171516b0fd42a</code>)</td></tr><tr><td>feePercent</td><td>String</td><td>否</td><td>发送到分佣地址的询价币种数量百分比 <code>最小百分比：0</code> <code>最大百分比：3</code> <br/> <br/> <div class="index_wrapper__x5A2Q"><div aria-labelledby=":R2kfkddf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R2kfkddf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"> 跨链分佣目前仅支持从<code>fromtoken</code>询价币种分佣 。</div></div></div></div></div></td></tr><tr><td>referrerAddress</td><td>String</td><td>否</td><td>分佣地址 (如：0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9) <br/> 收取分佣费用的地址。使用 API 时，可结合 feePercent 设置佣金比例。 <br/> <br/> 注意： <br/>1. 对于<strong>EVM</strong>：此处不支持涉及打包币对的交易，例如 ETH 和 WETH 的交易  <br/>2. 对于<strong>Solana</strong>：分佣地址需提前存入一些 SOL 进行激活。</td></tr><tr><td>priceImpactProtectionPercentage</td><td>String</td><td>否</td><td>(可选，默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。<br/> <br/> 当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。<br/> <br/> 这是一个<strong>可选开启</strong>的功能，默认值为 0.9。当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。<br/><br/> <strong>注意：</strong>当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。</td></tr><tr><td>onlyBridge</td><td>boolean</td><td>否</td><td>仅通过跨链桥完成跨链交易，不涉及源链兑换以及目标链兑换。</td></tr><tr><td>memo</td><td>String</td><td>否</td><td>你可以自定义 /build-tx 中携带的参数，数据编码为长度固定为 64 字节、128 个字符长度的 16 进制字符串，并可通过 /status API 查询。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>fromTokenAmount</td><td>String</td><td>询价币种的兑换数量 <br/> (数量需包含精度，如 <code>1.00</code> USDT 则为 <code>1000000</code>)</td></tr><tr><td>toTokenAmount</td><td>String</td><td>目标币种的兑换数量 <br/> (数量需包含精度，如 <code>1.00</code> USDT 则为 <code>1000000</code>)</td></tr><tr><td>minmumReceive</td><td>String</td><td>目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量)</td></tr><tr><td><em><strong>router</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>跨链桥基础信息</strong></em></td></tr><tr><td>bridgeId</td><td>Integer</td><td>跨链桥 ID (如：<code>211</code>)</td></tr><tr><td>bridgeName</td><td>String</td><td>跨链桥名称 (如： <code>cBridge</code>)</td></tr><tr><td>otherNativeFee</td><td>String</td><td>部分跨链桥会额外收取一定数量的源链主网币，作为跨链桥手续费，并不是所有跨链桥都会收取该部分费用。目前收取该费用的跨链桥有 Stargate、Wanchain、Arbitrum 官方桥、zkSync Era 官方桥、Linea 官方桥。 使用该三方桥需支付<code>otherNativeFee</code>才能完成交易。</td></tr><tr><td>crossChainFee</td><td>String</td><td>跨链桥收取的费用，一般为稳定币或者WETH</td></tr><tr><td>crossChainFeeTokenAddress</td><td>String</td><td>跨链桥费币种信息（如：<code>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</code> 代表主网代币地址）</td></tr><tr><td><em><strong>tx</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>交易上链所需的数据信息</strong></em></td></tr><tr><td>data</td><td>String</td><td>上链 inputData 数据</td></tr><tr><td>from</td><td>String</td><td>用户钱包地址 (如：<code>0x6f9ffea7370310cd0f890dfde5e0e061059dcfd9</code>)</td></tr><tr><td>to</td><td>String</td><td>欧易 DEX router 合约地址 (如：<code>0x6dc1fb08decf9f95a01222baa359aa0e02e07716</code>)</td></tr><tr><td>value</td><td>String</td><td>与合约交互的主链币数量 (wei) (如：<code>0</code>)</td></tr><tr><td>gasLimit</td><td>String</td><td>gas费用限额 (交易的gas (单位：wei)。如果该值太低，无法实现报价，则会返回错误信息) (如：<code>50000</code>)</td></tr><tr><td>gasPrice</td><td>String</td><td>以 wei 位单位的 Gas price (如：<code>110000000</code>)</td></tr><tr><td>maxPriorityFeePerGas</td><td>String</td><td>EIP-1559:每单位 gas 优先费用的推荐值 (如：<code>500000000</code>)</td></tr><tr><td>randomKeyAccount</td><td>Array</td><td>随机私钥账户参数并不是每次交易都需要。仅在某些特殊交易（例如使用CCTP桥进行代币跨链）时，才会生成和返回这个随机私钥账户。提供此参数时，您必须使用它与用户的钱包私钥一起进行多签操作，以确保交易的安全和顺利完成。点击此处查看<a href="/zh-hans/build/docs/waas/dex-use-crosschain-solana-quick-start">多签示例</a></td></tr><tr><td>signatureData</td><td>Array</td><td>如果返回此参数，则代表该交易需要额外的签名数据。开发者应将此参数作为交易签名的输入之一，并确保其在签名过程中正确应用。</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-approve-transaction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">交易授权</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-transaction-status" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">查询交易状态</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/cross-chain/build-tx?amount=15&amp;fromChainIndex=324&amp;toChainIndex=42161&amp;fromTokenAddress=0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4&amp;toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&amp;slippage=0.07&amp;userWalletAddress=0x22497668Fb12BA21E6A132de7168D0Ecc69cDF7d&amp;feePercent=1&amp;referrerAddress=0x3f6a3f57569358a512ccc0e513f171516b0fd42a'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"code"</span><span class="token operator">:</span><span class="token number">0</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span><span class="token string">""</span><span class="token punctuation">,</span>
  <span class="token property">"data"</span><span class="token operator">:</span>
  <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"fromTokenAmount"</span><span class="token operator">:</span> <span class="token string">"1000000000000"</span><span class="token punctuation">,</span>
      <span class="token property">"router"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
          <span class="token property">"bridgeId"</span><span class="token operator">:</span> <span class="token number">235</span><span class="token punctuation">,</span>
          <span class="token property">"bridgeName"</span><span class="token operator">:</span> <span class="token string">"swft"</span><span class="token punctuation">,</span>
          <span class="token property">"crossChainFee"</span><span class="token operator">:</span> <span class="token string">"4.67131461"</span><span class="token punctuation">,</span>
          <span class="token property">"otherNativeFee"</span><span class="token operator">:</span> <span class="token string">"1.50000000"</span><span class="token punctuation">,</span>
          <span class="token property">"crossChainFeeTokenAddress"</span><span class="token operator">:</span> <span class="token string">"0x6b175474e89094c44da98b954eedeac495271d0f"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token property">"toTokenAmount"</span><span class="token operator">:</span> <span class="token string">"1000000000000"</span><span class="token punctuation">,</span>
      <span class="token property">"minmumReceive"</span><span class="token operator">:</span> <span class="token string">"1000000000000"</span><span class="token punctuation">,</span>
      <span class="token property">"tx"</span><span class="token operator">:</span><span class="token punctuation">{</span>
          <span class="token property">"data"</span><span class="token operator">:</span><span class="token string">"0xc748673057861a797275cd8a068abb95a902e8de"</span><span class="token punctuation">,</span>
          <span class="token property">"from"</span><span class="token operator">:</span><span class="token string">"0x6dc1fb08decf9f95a01222baa359aa0e02e07716"</span><span class="token punctuation">,</span>
          <span class="token property">"to"</span><span class="token operator">:</span><span class="token string">"0x6dc1fb08decf9f95a01222baa359aa0e02e07716"</span><span class="token punctuation">,</span>
          <span class="token property">"value"</span><span class="token operator">:</span><span class="token number">0</span><span class="token punctuation">,</span>
          <span class="token property">"gasLimit"</span><span class="token operator">:</span><span class="token string">"442621"</span><span class="token punctuation">,</span>
          <span class="token property">"gasPrice"</span><span class="token operator">:</span><span class="token string">"3192374970"</span><span class="token punctuation">,</span>
          <span class="token property">"maxPriorityFeePerGas"</span><span class="token operator">:</span><span class="token string">"3599"</span>
          <span class="token property">"randomKeyAccount"</span><span class="token operator">:</span><span class="token punctuation">[</span><span class="token string">"xxxxxxx0x6dc1fb08decf9f95a01222baa359aa0e02e079999"</span><span class="token punctuation">]</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-approve-transaction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">交易授权</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-transaction-status" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">查询交易状态</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "API 参考",
    "跨链兑换"
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
    "获取支持的链",
    "获取币种列表",
    "获取仅跨链桥交易的币种列表",
    "获取仅通过跨链桥交易的币对列表",
    "获取支持的桥信息",
    "获取路径信息",
    "交易授权",
    "跨链兑换",
    "查询交易状态"
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
    "获取支持的链",
    "获取币种列表",
    "获取仅跨链桥交易的币种列表",
    "获取仅通过跨链桥交易的币对列表",
    "获取支持的桥信息",
    "获取路径信息",
    "交易授权",
    "跨链兑换",
    "查询交易状态",
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
