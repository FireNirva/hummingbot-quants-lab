# 兑换 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-swap#请求示例  
**抓取时间:** 2025-05-27 06:38:06  
**字数:** 998

## 导航路径
DEX API > 交易 API > API 参考 > 兑换

## 目录
- 搭建兑换应用
- 搭建跨链应用
- 介绍
- API 参考
- 获取支持的链
- 获取币种列表
- 获取流动性列表
- 交易授权
- 获取兑换价格
- 获取 Solana 兑换交易指令
- 兑换
- 查询交易状态
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

DEX API
交易 API
兑换 API
API 参考
兑换
兑换
#
通过 DEX 聚合器 router 获取兑换所需的交易数据。
注意
Uni v3 池子兑换存在以下场景：
如果池子内，想要兑换的币对流动性被抽空，池子将仅消耗部分支付币种，产生剩余。OKX DEX Router 作为完全去中心化的智能合约将自动退回您的剩余。
您集成过程中，注意兼容该情况，为您的合约设置支持币种退回，保障您用户的使用。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/swap
请求参数
#
参数
类型
必传
描述
chainIndex
String
是
链的唯一标识。
如
501
: Solana，更多可查看
这里
。
chainId
String
是
链的唯一标识。 即将废弃。
amount
String
是
币种询价数量
(数量需包含精度，如兑换 1.00 USDT 需输入 1000000，兑换 1.00 DAI 需输入 1000000000000000000)，币种精度可通过
币种列表
取得。
fromTokenAddress
String
是
询价币种合约地址 (如：
0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
)
toTokenAddress
String
是
目标币种合约地址 (如：
0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
)
slippage
String
是
滑点限制。
注意：
1. 在 EVM 网络上，滑点最小值为
0
，最大值为
1
。
2. 在 Solana 网络上，滑点最小值为
0
，最大值需
小于 1
。
（如：
0.005
代表这笔交易的最大滑点为
0.5%
，
1
代表这笔交易的最大滑点为
100%
）
userWalletAddress
String
是
用户钱包地址 (如：
0x3f6a3f57569358a512ccc0e513f171516b0fd42a
)
swapReceiverAddress
String
否
购买的资产的收件人地址 如果未设置，则用户钱包地址收到购买的资产 (如：
0x3f6a3f57569358a512ccc0e513f171516b0fd42a
)
feePercent
String
否
发送到分佣地址的询价或者目标币种数量百分比，
最小百分比 > 0
，
Solana 链
最大百分比：10
。
其他链
最大百分比：3
，最多支持小数点后 2 位，系统将自动忽略超出的部分。(例如：实际传入 1.326%，但分拥计算时仅会取 1.32% 的分拥比例)
fromTokenReferrerWalletAddress
String
否
收取 fromToken 分佣费用的钱包地址。
使用 API 时，
需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣
。
注意:
1.对于
Solana
:分佣地址需提前存入一些 SOL 进行激活。
2.对于
TON
:支持经过 Stonfi V2 和 Dedust 流动性池交易的分佣，不支持经过 Stonfi V1 流动性池交易的分佣
toTokenReferrerWalletAddress
String
否
收取 toToken 分佣费用的钱包地址。
使用 API 时，
需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣
。
注意:
1.对于
Solana
:分佣地址需提前存入一些 SOL 进行激活。
2.对于
TON
:仅支持经过 Stonfi V2 流动性池交易的分佣
positiveSlippagePercent
String
否
收取的正滑点比例。设置此参数后，可将用户在交易中获得超过报价金额的额外部分按比例作为收入收取。目前该参数仅支持
Solana 链
，其他链的正滑点将全部返还给用户。
正滑点收取比例默认设置为 0。
最小百分比
：0，
最大百分比
：10 最多支持小数点后 1 位。
positiveSlippageFeeAddress
string
否
收取正滑点分佣费用的钱包地址。 使用时需要结合 positiveSlippagePercent 设置比例。若填入，所有正滑点收益将转至該地址，若未填入则使用收取分佣费用的钱包地址。
gaslimit
String
否
Gas (以最小单位表示：wei) 费用限额 (如果该值太低，无法实现报价，则会返回错误信息)。
仅适用于EVM。
gasLevel
String
否
Gas价格等级 (默认为
average
,交易消耗gas价格水平，可设置为
average
、
fast
或
slow
)
dexIds
String
否
限定询价的流动性池 dexId , 多个组合按
,
分隔 (如
1,50,180
，更多可查看流动性列表)
directRoute
Boolean
否
默认设置为 false。启用后，将限制路由仅使用单一流动性池。当前，该功能仅适用于 Solana 兑换。
callDataMemo
String
否
你可以自定义 callData 中上链携带的参数，将想要带到链上的数据编码成长度固定为 64 bytes、128 个字符长度的 16 进制字符串。例如，“0x...111”，字符串中需要保留“0x”开头。
computeUnitPrice
String
否
用于 Solana 网络上的交易，类似于 Ethereum 上的 gasPrice，这个价格决定了交易的优先级，价格越高意味着交易越有可能更快地被网络处理。
computeUnitLimit
String
否
用于 Solana 网络上的交易，可类比为 Ethereum 上的的 gasLimit，这个限制可以确保交易不会占用过多的计算资源。
dexIds
String
否
限定询价的流动性池 dexId , 多个组合按
,
分隔 (如
1,50,180
，更多可查看流动性列表)
directRoute
Boolean
否
默认设置为 false。启用后，将限制路由仅使用单一流动性池。当前，该功能仅适用于 Solana 兑换。
priceImpactProtectionPercentage
String
否
(默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。
当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。
当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。
注意：
当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。
callDataMemo
String
否
你可以自定义 callData 中上链携带的参数，将想要带到链上的数据编码成长度固定为 64 bytes、128 个字符长度的 16 进制字符串。例如，“0x...111”，字符串中需要保留“0x”开头。
autoSlippage
Boolean
否
默认为 false。当设置为 true 时，原 slippage 参数（如果有传入）将会被 autoSlippage 覆盖，将基于当前市场数据计算并设定自動滑点。
maxAutoSlippage
String
否
当 autoSlippage 设置为 true 时，此值为 API 所返回的 autoSlippage 的最大上限，建议采用此值以控制风险。
响应参数
#
参数
类型
描述
routerResult
Object
询价路径数据对象
chainIndex
String
否
chainId
String
否
fromTokenAmount
String
询价币种的兑换数量 (如：
500000000000000000000000
)
toTokenAmount
String
目标币种的兑换数量 (如：
168611907733361
)
tradeFee
String
询价路径预估消耗的网络费用 (USD 计价)
estimateGasFee
String
预估消耗的 gas，各个链的最小单位返回，例如 wei
dexRouterList
Array
询价路径数据集合
router
String
币种兑换的一条路径
routerPercent
String
当前兑换路径处理的资产占所有资产的百分比 (如：
5
)
subRouterList
Array
询价路径数据子集合
dexProtocol
Array
兑换路径中执行的 DEX 协议
dexName
String
DEX 协议名称 (如：
Verse
)
percent
String
一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比 (如：
100
)
fromToken
Object
询价币种信息
tokenContractAddress
String
币种合约地址 (如：
0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
)
tokenSymbol
String
币种简称 (如：
USDC
)
tokenUnitPrice
String
该接口返回的币种单价是基于链上的实时美元价格。注：此价格仅为推荐价格，在一些特殊情况中，币种单价可能为 null
decimal
String
币种精度定义了单个的该币种可以被分成多少份的最小单位。例如，如果一个币种的精度是 8，则表示单个的这种代币可以被分成 100,000,000 份的最小单位。
注意：该参数仅供参考，币种精度会随着合约拥有者的设置改变等原因发生变化。
isHoneyPot
Boolean
代币是否为貔貅币。
是：true
否：false
taxRate
String
代币卖出税率，适用于可设定税费机制的代币（如SafeMoon、SPL2022代币）。普通代币无税费时返回
0
。取值为
最小：0
最大：1
，0.01表示1%。
toToken
Object
目标币种信息
tokenContractAddress
String
币种合约地址 (如：
0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
)
tokenSymbol
String
币种简称 (如：
USDC
)
tokenUnitPrice
String
该接口返回的币种单价是一个结合了链上、交易所以及其他第三方来源数据的综合美元价格。注：此价格仅为推荐价格，在一些特殊情况中，币种单价可能为 null
decimal
String
币种精度定义了单个的该币种可以被分成多少份的最小单位。例如，如果一个币种的精度是 8，则表示单个的这种代币可以被分成 100,000,000 份的最小单位。
注意：该参数仅供参考，币种精度会随着合约拥有者的设置改变等原因发生变化。
isHoneyPot
Boolean
代币是否为貔貅币。
是：true
否：false
taxRate
String
代币买入税率，适用于可设定税费机制的代币（如SafeMoon、SPL2022代币）。普通代币无税费时返回
0
。取值为
最小：0
最大：1
，0.01表示1%。
quoteCompareList
Array
询价路径对比列表
dexName
String
询价路径 DEX 名称
dexLogo
String
DEX 协议名称
tradeFee
String
询价路径预估消耗的网络费用 (USD 计价)
amountOut
String
询价路径的接收数量
priceImpactPercentage
String
Percentage = (接收价值 – 支付价值) / 支付价值。因为当前兑换数量影响了流动性池深度，导致产生了价值差额。若接收价值大于支付价值，Percentage 有可能是正数。
tx
Object
发交易信息
signatureData
Array
如果返回此参数，则代表该交易需要额外的签名数据。开发者应将此参数作为交易签名的输入之一，并确保其在签名过程中正确应用。
from
String
用户钱包地址 (如：0x3f6a3f57569358a512ccc0e513f171516b0fd42a)
gas
String
gas 费限值的估计值，在 gasprice 基础上增加 50%，以 10 进制标准格式返回。 (如：
1173250
)
gasPrice
String
以 wei 为单位的 gas price ，以 10 进制标准格式返回。(如：
58270000000
)
maxPriorityFeePerGas
String
EIP-1559:每单位 gas 优先费用的推荐值 (如：
500000000
)
to
String
欧易 DEX router 合约地址 (如：
0x3b3ae790Df4F312e745D270119c6052904FB6790
)
value
String
与合约交互的主链币数量，以 10 进制标准格式最小单位返回 (wei) (如：
0
)
minReceiveAmount
String
目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量，如：
900645839798
)
data
String
Call data
slippage
String
当前交易的滑点值
获取 Solana 兑换交易指令
查询交易状态
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/swap?chainIndex=1&amount=10000000000000&toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&slippage=0.05&userWalletAddress=0x6f9ffea7370310cd0f890dfde5e0e061059dcfb8'
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
"0"
,
"data"
:
[
{
"routerResult"
:
{
"chainId"
:
"1"
,
"dexRouterList"
:
[
{
"router"
:
"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee--0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
,
"routerPercent"
:
"100"
,
"subRouterList"
:
[
{
"dexProtocol"
:
[
{
"dexName"
:
"Uniswap V3"
,
"percent"
:
"100"
}
]
,
"fromToken"
:
{
"decimal"
:
"18"
,
"isHoneyPot"
:
false
,
"taxRate"
:
"0"
,
"tokenContractAddress"
:
"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
,
"tokenSymbol"
:
"WETH"
,
"tokenUnitPrice"
:
"3342.87"
}
,
"toToken"
:
{
"decimal"
:
"6"
,
"isHoneyPot"
:
false
,
"taxRate"
:
"0"
,
"tokenContractAddress"
:
"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
,
"tokenSymbol"
:
"USDC"
,
"tokenUnitPrice"
:
"0.9995"
}
}
]
}
]
,
"estimateGasFee"
:
"135000"
,
"fromToken"
:
{
"decimal"
:
"18"
,
"isHoneyPot"
:
false
,
"taxRate"
:
"0"
,
"tokenContractAddress"
:
"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
,
"tokenSymbol"
:
"ETH"
,
"tokenUnitPrice"
:
"3342.87"
}
,
"fromTokenAmount"
:
"10000000000000"
,
"priceImpactPercentage"
:
"0.001"
,
"quoteCompareList"
:
[
{
"amountOut"
:
"32990"
,
"dexLogo"
:
"https://static.okx.com/cdn/wallet/logo/balancer.png"
,
"dexName"
:
"Balancer V1"
,
"tradeFee"
:
"44.32919149271585462"
}
,
{
"amountOut"
:
"334"
,
"dexLogo"
:
"https://static.okx.com/cdn/wallet/logo/DODO.png"
,
"dexName"
:
"DODO"
,
"tradeFee"
:
"36.96825563599181972"
}
,
{
"amountOut"
:
"33023"
,
"dexLogo"
:
"https://static.okx.com/cdn/wallet/logo/balancer.png"
,
"dexName"
:
"Balancer V2"
,
"tradeFee"
:
"19.79273863696907162"
}
,
{
"amountOut"
:
"32980"
,
"dexLogo"
:
"https://static.okx.com/cdn/explorer/dex/logo/Dex_Sushiswap_V3.png"
,
"dexName"
:
"Sushiswap V3"
,
"tradeFee"
:
"15.70332982767794112"
}
,
{
"amountOut"
:
"32964"
,
"dexLogo"
:
"https://static.okx.com/cdn/wallet/logo/SHIB.png"
,
"dexName"
:
"ShibaSwap"
,
"tradeFee"
:
"15.70332982767794112"
}
]
,
"toToken"
:
{
"decimal"
:
"6"
,
"isHoneyPot"
:
false
,
"taxRate"
:
"0"
,
"tokenContractAddress"
:
"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
,
"tokenSymbol"
:
"USDC"
,
"tokenUnitPrice"
:
"0.9995"
}
,
"toTokenAmount"
:
"33474"
,
"tradeFee"
:
"4.3491690602723664"
}
,
"tx"
:
{
"data"
:
"0x0d5f0e3b00000000000000000001881f6f9ffea7370310cd0f890dfde5e0e061059dcfb8000000000000000000000000000000000000000000000000000009184e72a0000000000000000000000000000000000000000000000000000000000000007c3800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000001800000000000000000000000e0554a476a092703abdb3ef35c80e0d76d32939f"
,
"from"
:
"0x6f9ffea7370310cd0f890dfde5e0e061059dcfb8"
,
"gas"
:
"202500"
,
"gasPrice"
:
"32657616776"
,
"maxPriorityFeePerGas"
:
"2086453233"
,
"minReceiveAmount"
:
"31800"
,
"signatureData"
:
[
""
]
,
"to"
:
"0x7D0CcAa3Fac1e5A943c5168b6CEd828691b46B36"
,
"value"
:
"10000000000000"
}
}
]
,
"msg"
:
""
}
获取 Solana 兑换交易指令
查询交易状态

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-swap" style="color:inherit">兑换</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="兑换">兑换<a class="index_header-anchor__Xqb+L" href="#兑换" style="opacity:0">#</a></h1><p>通过 DEX 聚合器 router 获取兑换所需的交易数据。</p><div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rddf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rddf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">Uni v3 池子兑换存在以下场景：<br/> 如果池子内，想要兑换的币对流动性被抽空，池子将仅消耗部分支付币种，产生剩余。OKX DEX Router 作为完全去中心化的智能合约将自动退回您的剩余。<br/> 您集成过程中，注意兼容该情况，为您的合约设置支持币种退回，保障您用户的使用。</div></div></div></div></div><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/swap</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 <br/>如<code>501</code>: Solana，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>是</td><td>链的唯一标识。 即将废弃。</td></tr><tr><td>amount</td><td>String</td><td>是</td><td>币种询价数量  <br/> (数量需包含精度，如兑换 1.00 USDT 需输入 1000000，兑换 1.00 DAI 需输入 1000000000000000000)，币种精度可通过<a href="/zh-hans/build/dev-docs/dex-get-tokens">币种列表</a>取得。</td></tr><tr><td>fromTokenAddress</td><td>String</td><td>是</td><td>询价币种合约地址 (如：<code>0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee</code>)</td></tr><tr><td>toTokenAddress</td><td>String</td><td>是</td><td>目标币种合约地址 (如：<code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code>)</td></tr><tr><td>slippage</td><td>String</td><td>是</td><td>滑点限制。<br/> <br/> 注意：<br/> 1. 在 EVM 网络上，滑点最小值为 <code>0</code>，最大值为 <code>1</code>。<br/>  2. 在 Solana 网络上，滑点最小值为 <code>0</code>，最大值需<code>小于 1</code>。<br/> （如：<code>0.005</code>代表这笔交易的最大滑点为<code>0.5%</code>，<code>1</code>代表这笔交易的最大滑点为 <code>100%</code>）</td></tr><tr><td>userWalletAddress</td><td>String</td><td>是</td><td>用户钱包地址 (如：<code>0x3f6a3f57569358a512ccc0e513f171516b0fd42a</code>)</td></tr><tr><td>swapReceiverAddress</td><td>String</td><td>否</td><td>购买的资产的收件人地址 如果未设置，则用户钱包地址收到购买的资产 (如：<code>0x3f6a3f57569358a512ccc0e513f171516b0fd42a</code>)</td></tr><tr><td>feePercent</td><td>String</td><td>否</td><td>发送到分佣地址的询价或者目标币种数量百分比，<code>最小百分比 &gt; 0</code>， <br/> Solana 链<code>最大百分比：10</code>。 <br/> 其他链<code>最大百分比：3</code>，最多支持小数点后 2 位，系统将自动忽略超出的部分。(例如：实际传入 1.326%，但分拥计算时仅会取 1.32% 的分拥比例)</td></tr><tr><td>fromTokenReferrerWalletAddress</td><td>String</td><td>否</td><td>收取 fromToken 分佣费用的钱包地址。<br/>使用 API 时，<strong>需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣</strong>。<br/><br/>注意:<br/> 1.对于 <strong>Solana</strong>:分佣地址需提前存入一些 SOL 进行激活。<br/> 2.对于 <strong>TON</strong>:支持经过 Stonfi V2 和 Dedust 流动性池交易的分佣，不支持经过 Stonfi V1 流动性池交易的分佣</td></tr><tr><td>toTokenReferrerWalletAddress</td><td>String</td><td>否</td><td>收取 toToken 分佣费用的钱包地址。<br/>使用 API 时，<strong>需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣</strong>。<br/><br/>注意:<br/>1.对于 <strong>Solana</strong>:分佣地址需提前存入一些 SOL 进行激活。<br/> 2.对于 <strong>TON</strong>:仅支持经过 Stonfi V2 流动性池交易的分佣</td></tr><tr><td>positiveSlippagePercent</td><td>String</td><td>否</td><td>收取的正滑点比例。设置此参数后，可将用户在交易中获得超过报价金额的额外部分按比例作为收入收取。目前该参数仅支持 <strong>Solana 链</strong>，其他链的正滑点将全部返还给用户。<br/>正滑点收取比例默认设置为 0。<code>最小百分比</code>：0，<code>最大百分比</code>：10 最多支持小数点后 1 位。</td></tr><tr><td>positiveSlippageFeeAddress</td><td>string</td><td>否</td><td>收取正滑点分佣费用的钱包地址。 使用时需要结合 positiveSlippagePercent 设置比例。若填入，所有正滑点收益将转至該地址，若未填入则使用收取分佣费用的钱包地址。</td></tr><tr><td>gaslimit</td><td>String</td><td>否</td><td>Gas (以最小单位表示：wei) 费用限额 (如果该值太低，无法实现报价，则会返回错误信息)。<br/> 仅适用于EVM。</td></tr><tr><td>gasLevel</td><td>String</td><td>否</td><td>Gas价格等级 (默认为 <code>average</code>,交易消耗gas价格水平，可设置为 <code>average</code>、<code>fast</code> 或 <code>slow</code>)</td></tr><tr><td>dexIds</td><td>String</td><td>否</td><td>限定询价的流动性池 dexId , 多个组合按 <code>,</code> 分隔 (如 <code>1,50,180</code> ，更多可查看流动性列表)</td></tr><tr><td>directRoute</td><td>Boolean</td><td>否</td><td>默认设置为 false。启用后，将限制路由仅使用单一流动性池。当前，该功能仅适用于 Solana 兑换。</td></tr><tr><td>callDataMemo</td><td>String</td><td>否</td><td>你可以自定义 callData 中上链携带的参数，将想要带到链上的数据编码成长度固定为 64 bytes、128 个字符长度的 16 进制字符串。例如，“0x...111”，字符串中需要保留“0x”开头。</td></tr><tr><td>computeUnitPrice</td><td>String</td><td>否</td><td>用于 Solana 网络上的交易，类似于 Ethereum 上的 gasPrice，这个价格决定了交易的优先级，价格越高意味着交易越有可能更快地被网络处理。</td></tr><tr><td>computeUnitLimit</td><td>String</td><td>否</td><td>用于 Solana 网络上的交易，可类比为 Ethereum 上的的 gasLimit，这个限制可以确保交易不会占用过多的计算资源。</td></tr><tr><td>dexIds</td><td>String</td><td>否</td><td>限定询价的流动性池 dexId , 多个组合按 <code>,</code> 分隔 (如 <code>1,50,180</code> ，更多可查看流动性列表)</td></tr><tr><td>directRoute</td><td>Boolean</td><td>否</td><td>默认设置为 false。启用后，将限制路由仅使用单一流动性池。当前，该功能仅适用于 Solana 兑换。</td></tr><tr><td>priceImpactProtectionPercentage</td><td>String</td><td>否</td><td>(默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。<br/> <br/> 当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。<br/> 当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。<br/><br/> <strong>注意：</strong>当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。</td></tr><tr><td>callDataMemo</td><td>String</td><td>否</td><td>你可以自定义 callData 中上链携带的参数，将想要带到链上的数据编码成长度固定为 64 bytes、128 个字符长度的 16 进制字符串。例如，“0x...111”，字符串中需要保留“0x”开头。</td></tr><tr><td>autoSlippage</td><td>Boolean</td><td>否</td><td>默认为 false。当设置为 true 时，原 slippage 参数（如果有传入）将会被 autoSlippage 覆盖，将基于当前市场数据计算并设定自動滑点。</td></tr><tr><td>maxAutoSlippage</td><td>String</td><td>否</td><td>当 autoSlippage 设置为 true 时，此值为 API 所返回的 autoSlippage 的最大上限，建议采用此值以控制风险。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td><em><strong>routerResult</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>询价路径数据对象</strong></em></td></tr><tr><td>chainIndex</td><td>String</td><td>否</td></tr><tr><td>chainId</td><td>String</td><td>否</td></tr><tr><td>fromTokenAmount</td><td>String</td><td>询价币种的兑换数量  (如：<code>500000000000000000000000</code>)</td></tr><tr><td>toTokenAmount</td><td>String</td><td>目标币种的兑换数量  (如：<code>168611907733361</code>)</td></tr><tr><td>tradeFee</td><td>String</td><td>询价路径预估消耗的网络费用 (USD 计价)</td></tr><tr><td>estimateGasFee</td><td>String</td><td>预估消耗的 gas，各个链的最小单位返回，例如 wei</td></tr><tr><td><em><strong>dexRouterList</strong></em></td><td><em><strong>Array</strong></em></td><td><em><strong>询价路径数据集合</strong></em></td></tr><tr><td>router</td><td>String</td><td>币种兑换的一条路径</td></tr><tr><td>routerPercent</td><td>String</td><td>当前兑换路径处理的资产占所有资产的百分比 (如：<code>5</code>)</td></tr><tr><td><em><strong>subRouterList</strong></em></td><td><em><strong>Array</strong></em></td><td><em><strong>询价路径数据子集合</strong></em></td></tr><tr><td><em><strong>dexProtocol</strong></em></td><td><em><strong>Array</strong></em></td><td><em><strong>兑换路径中执行的 DEX 协议</strong></em></td></tr><tr><td>dexName</td><td>String</td><td>DEX 协议名称 (如：<code>Verse</code>)</td></tr><tr><td>percent</td><td>String</td><td>一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比 (如：<code>100</code>)</td></tr><tr><td><em><strong>fromToken</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>询价币种信息</strong></em></td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如：<code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code>)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如：<code>USDC</code>)</td></tr><tr><td>tokenUnitPrice</td><td>String</td><td>该接口返回的币种单价是基于链上的实时美元价格。注：此价格仅为推荐价格，在一些特殊情况中，币种单价可能为 null</td></tr><tr><td>decimal</td><td>String</td><td>币种精度定义了单个的该币种可以被分成多少份的最小单位。例如，如果一个币种的精度是 8，则表示单个的这种代币可以被分成 100,000,000 份的最小单位。<em><strong>注意：该参数仅供参考，币种精度会随着合约拥有者的设置改变等原因发生变化。</strong></em></td></tr><tr><td>isHoneyPot</td><td>Boolean</td><td>代币是否为貔貅币。 <code>是：true</code> <code>否：false </code></td></tr><tr><td>taxRate</td><td>String</td><td>代币卖出税率，适用于可设定税费机制的代币（如SafeMoon、SPL2022代币）。普通代币无税费时返回 <code>0</code>。取值为 <code>最小：0</code> <code>最大：1</code>，0.01表示1%。</td></tr><tr><td><em><strong>toToken</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>目标币种信息</strong></em></td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如：<code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code>)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如：<code>USDC</code>)</td></tr><tr><td>tokenUnitPrice</td><td>String</td><td>该接口返回的币种单价是一个结合了链上、交易所以及其他第三方来源数据的综合美元价格。注：此价格仅为推荐价格，在一些特殊情况中，币种单价可能为 null</td></tr><tr><td>decimal</td><td>String</td><td>币种精度定义了单个的该币种可以被分成多少份的最小单位。例如，如果一个币种的精度是 8，则表示单个的这种代币可以被分成 100,000,000 份的最小单位。<em><strong>注意：该参数仅供参考，币种精度会随着合约拥有者的设置改变等原因发生变化。</strong></em></td></tr><tr><td>isHoneyPot</td><td>Boolean</td><td>代币是否为貔貅币。 <code>是：true</code> <code>否：false </code></td></tr><tr><td>taxRate</td><td>String</td><td>代币买入税率，适用于可设定税费机制的代币（如SafeMoon、SPL2022代币）。普通代币无税费时返回 <code>0</code>。取值为 <code>最小：0</code> <code>最大：1</code>，0.01表示1%。</td></tr><tr><td><em><strong>quoteCompareList</strong></em></td><td><em><strong>Array</strong></em></td><td><em><strong>询价路径对比列表</strong></em></td></tr><tr><td>dexName</td><td>String</td><td>询价路径 DEX 名称</td></tr><tr><td>dexLogo</td><td>String</td><td>DEX 协议名称</td></tr><tr><td>tradeFee</td><td>String</td><td>询价路径预估消耗的网络费用 (USD 计价)</td></tr><tr><td>amountOut</td><td>String</td><td>询价路径的接收数量</td></tr><tr><td>priceImpactPercentage</td><td>String</td><td>Percentage = (接收价值 – 支付价值) / 支付价值。因为当前兑换数量影响了流动性池深度，导致产生了价值差额。若接收价值大于支付价值，Percentage 有可能是正数。</td></tr><tr><td><em><strong>tx</strong></em></td><td><em><strong>Object</strong></em></td><td><em><strong>发交易信息</strong></em></td></tr><tr><td>signatureData</td><td><em><strong>Array</strong></em></td><td>如果返回此参数，则代表该交易需要额外的签名数据。开发者应将此参数作为交易签名的输入之一，并确保其在签名过程中正确应用。</td></tr><tr><td>from</td><td>String</td><td>用户钱包地址 (如：0x3f6a3f57569358a512ccc0e513f171516b0fd42a)</td></tr><tr><td>gas</td><td>String</td><td>gas 费限值的估计值，在 gasprice 基础上增加 50%，以 10 进制标准格式返回。 (如：<code>1173250</code>)</td></tr><tr><td>gasPrice</td><td>String</td><td>以 wei 为单位的 gas price ，以 10 进制标准格式返回。(如：<code>58270000000</code>)</td></tr><tr><td>maxPriorityFeePerGas</td><td>String</td><td>EIP-1559:每单位 gas 优先费用的推荐值   (如：<code>500000000</code>)</td></tr><tr><td>to</td><td>String</td><td>欧易 DEX router 合约地址 (如：<code>0x3b3ae790Df4F312e745D270119c6052904FB6790</code>)</td></tr><tr><td>value</td><td>String</td><td>与合约交互的主链币数量，以 10 进制标准格式最小单位返回 (wei) (如：<code>0</code>)</td></tr><tr><td>minReceiveAmount</td><td>String</td><td>目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量，如：<code>900645839798</code>)</td></tr><tr><td>data</td><td>String</td><td>Call data</td></tr><tr><td>slippage</td><td>String</td><td>当前交易的滑点值</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-solana-swap-instruction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取 Solana 兑换交易指令</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-swap-history" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">查询交易状态</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/swap?chainIndex=1&amp;amount=10000000000000&amp;toTokenAddress=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48&amp;fromTokenAddress=0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee&amp;slippage=0.05&amp;userWalletAddress=0x6f9ffea7370310cd0f890dfde5e0e061059dcfb8'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
        <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"routerResult"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token property">"dexRouterList"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"router"</span><span class="token operator">:</span> <span class="token string">"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee--0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"</span><span class="token punctuation">,</span>
        <span class="token property">"routerPercent"</span><span class="token operator">:</span> <span class="token string">"100"</span><span class="token punctuation">,</span>
        <span class="token property">"subRouterList"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"dexProtocol"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"Uniswap V3"</span><span class="token punctuation">,</span>
        <span class="token property">"percent"</span><span class="token operator">:</span> <span class="token string">"100"</span>
      <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"fromToken"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"decimal"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
        <span class="token property">"isHoneyPot"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token property">"taxRate"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"WETH"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenUnitPrice"</span><span class="token operator">:</span> <span class="token string">"3342.87"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"toToken"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"decimal"</span><span class="token operator">:</span> <span class="token string">"6"</span><span class="token punctuation">,</span>
        <span class="token property">"isHoneyPot"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token property">"taxRate"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"USDC"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenUnitPrice"</span><span class="token operator">:</span> <span class="token string">"0.9995"</span>
      <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
        <span class="token punctuation">]</span>
      <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"estimateGasFee"</span><span class="token operator">:</span> <span class="token string">"135000"</span><span class="token punctuation">,</span>
        <span class="token property">"fromToken"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"decimal"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
        <span class="token property">"isHoneyPot"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token property">"taxRate"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"ETH"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenUnitPrice"</span><span class="token operator">:</span> <span class="token string">"3342.87"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"fromTokenAmount"</span><span class="token operator">:</span> <span class="token string">"10000000000000"</span><span class="token punctuation">,</span>
        <span class="token property">"priceImpactPercentage"</span><span class="token operator">:</span> <span class="token string">"0.001"</span><span class="token punctuation">,</span>
        <span class="token property">"quoteCompareList"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"amountOut"</span><span class="token operator">:</span> <span class="token string">"32990"</span><span class="token punctuation">,</span>
        <span class="token property">"dexLogo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/balancer.png"</span><span class="token punctuation">,</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"Balancer V1"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"44.32919149271585462"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token property">"amountOut"</span><span class="token operator">:</span> <span class="token string">"334"</span><span class="token punctuation">,</span>
        <span class="token property">"dexLogo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/DODO.png"</span><span class="token punctuation">,</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"DODO"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"36.96825563599181972"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token property">"amountOut"</span><span class="token operator">:</span> <span class="token string">"33023"</span><span class="token punctuation">,</span>
        <span class="token property">"dexLogo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/balancer.png"</span><span class="token punctuation">,</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"Balancer V2"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"19.79273863696907162"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token property">"amountOut"</span><span class="token operator">:</span> <span class="token string">"32980"</span><span class="token punctuation">,</span>
        <span class="token property">"dexLogo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/Dex_Sushiswap_V3.png"</span><span class="token punctuation">,</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"Sushiswap V3"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"15.70332982767794112"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        <span class="token property">"amountOut"</span><span class="token operator">:</span> <span class="token string">"32964"</span><span class="token punctuation">,</span>
        <span class="token property">"dexLogo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/SHIB.png"</span><span class="token punctuation">,</span>
        <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"ShibaSwap"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"15.70332982767794112"</span>
      <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"toToken"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"decimal"</span><span class="token operator">:</span> <span class="token string">"6"</span><span class="token punctuation">,</span>
        <span class="token property">"isHoneyPot"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token property">"taxRate"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"USDC"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenUnitPrice"</span><span class="token operator">:</span> <span class="token string">"0.9995"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"toTokenAmount"</span><span class="token operator">:</span> <span class="token string">"33474"</span><span class="token punctuation">,</span>
        <span class="token property">"tradeFee"</span><span class="token operator">:</span> <span class="token string">"4.3491690602723664"</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"tx"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"0x0d5f0e3b00000000000000000001881f6f9ffea7370310cd0f890dfde5e0e061059dcfb8000000000000000000000000000000000000000000000000000009184e72a0000000000000000000000000000000000000000000000000000000000000007c3800000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000001800000000000000000000000e0554a476a092703abdb3ef35c80e0d76d32939f"</span><span class="token punctuation">,</span>
        <span class="token property">"from"</span><span class="token operator">:</span> <span class="token string">"0x6f9ffea7370310cd0f890dfde5e0e061059dcfb8"</span><span class="token punctuation">,</span>
        <span class="token property">"gas"</span><span class="token operator">:</span> <span class="token string">"202500"</span><span class="token punctuation">,</span>
        <span class="token property">"gasPrice"</span><span class="token operator">:</span> <span class="token string">"32657616776"</span><span class="token punctuation">,</span>
        <span class="token property">"maxPriorityFeePerGas"</span><span class="token operator">:</span> <span class="token string">"2086453233"</span><span class="token punctuation">,</span>
        <span class="token property">"minReceiveAmount"</span><span class="token operator">:</span> <span class="token string">"31800"</span><span class="token punctuation">,</span>
        <span class="token property">"signatureData"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">""</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"to"</span><span class="token operator">:</span> <span class="token string">"0x7D0CcAa3Fac1e5A943c5168b6CEd828691b46B36"</span><span class="token punctuation">,</span>
        <span class="token property">"value"</span><span class="token operator">:</span> <span class="token string">"10000000000000"</span>
      <span class="token punctuation">}</span>
      <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
      <span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-solana-swap-instruction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取 Solana 兑换交易指令</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-swap-history" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">查询交易状态</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "兑换"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取币种列表",
    "获取流动性列表",
    "交易授权",
    "获取兑换价格",
    "获取 Solana 兑换交易指令",
    "兑换",
    "查询交易状态",
    "设置分佣",
    "DEX 集成",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "支持的跨链桥"
  ],
  "toc": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取币种列表",
    "获取流动性列表",
    "交易授权",
    "获取兑换价格",
    "获取 Solana 兑换交易指令",
    "兑换",
    "查询交易状态",
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
