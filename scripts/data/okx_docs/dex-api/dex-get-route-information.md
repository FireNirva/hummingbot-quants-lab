# 获取路径信息 | API 参考 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-route-information#请求地址  
**抓取时间:** 2025-05-27 03:46:34  
**字数:** 745

## 导航路径
DEX API > 交易 API > API 参考 > 获取路径信息

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
获取路径信息
获取路径信息
#
通过欧易 DEX 跨链聚合器获取综合最优路径。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/cross-chain/quote
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
toChainIndex
String
是
目标链 ID (如
1
: Ethereum，更多可查看
链 ID 列表
)
fromChainId
String
是
源链 ID，即将废弃
toChainId
String
是
目标链 ID，即将废弃
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
币种询价数量
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
sort
Integer
否
跨链路径选择，默认返回 1
0 代表预计获得数量最多的路径
1 代表综合计算获得数量、网络费用、滑点、跨链桥费后的最优路径
2 代表最快路径，是耗时最少的路径
dexIds
String
否
限定询价的流动性池 dexId , 多个组合按 , 分隔 (如 1,50,180 ，更多可查看流动性列表)
feePercent
String
否
发送到分佣地址的询价币种数量百分比
最小百分比：0
最大百分比：3
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
响应参数
#
参数
类型
描述
fromChainId
String
源链 ID (如1: Ethereum，更多可查看
这里
)
toChainId
String
目标链 ID (如1: Ethereum，更多可查看
这里
)
fromTokenAmount
String
询价币种的兑换数量 (如：500000000000000000000000)
fromToken
Object
询价币种信息
decimals
Integer
币种精度 (如： 18)
tokenContractAddress
String
币种合约地址 (如 ：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
tokenSymbol
String
币种简称 (如 WETH)
toToken
Object
目标链币种基础信息
decimals
Integer
币种精度(如： 6)
tokenContractAddress
String
币种合约地址(如： 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)
tokenSymbol
String
币种简称 (如： USDC)
routerList
Array
询价路径数据集合
router
Object
跨链桥基础信息
bridgeId
Integer
跨链桥 ID (如211)
bridgeName
String
跨链桥名称 (如cBridge)
otherNativeFee
String
部分跨链桥会额外收取一定数量的源链主网币，作为跨链桥手续费，并不是所有跨链桥都会收取该部分费用。目前收取该费用的跨链桥有 Stargate、Wanchain、Arbitrum 官方桥、zkSync Era 官方桥、Linea 官方桥。使用该三方桥需支付otherNativeFee才能完成交易。
otherNativeFeeUsd
String
部分跨链桥额外收取费用的美元计价
crossChainFee
String
跨链桥收取的费用，一般为稳定币或者WETH
crossChainFeeUsd
String
跨链桥收取的费用的美元计价
crossChainFeeTokenAddress
String
跨链桥费币种信息（如：0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE 代表主网代币地址）
estimateGasFee
String
以 wei 为单位的预估消耗的 gas
estimateGasFeeUsd
String
预估消耗 gas 费用的美元计价
estimatedTime
String
预估的跨链交易完成时间，以秒为单位，时间根据历史成功订单交易完成时间动态计算得出
fromDexRouterList
Array
源链兑换路径基础信息, 如果不需要源链兑换路径则返回空
percent
String
一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比
router
String
币种兑换的一条路径
subRouterList
Array
DEX router集合信息
dexProtocol
Array
兑换路径中执行的 DEX 协议
dexName
String
DEX 协议名称
percent
String
一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比 (如：100)
fromToken
Object
询价币种信息
decimals
Integer
币种精度 (如： 18)
tokenContractAddress
String
币种合约地址 (如：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
tokenSymbol
String
币种简称 (如：WETH)
toToken
Object
目标币种信息
decimals
Integer
币种精度 (如： 6)
tokenContractAddress
String
币种合约地址 (如：0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)
tokenSymbol
String
币种符号 (如：USDC)
toDexRouterList
Array
目标链兑换路径基础信息，如果不需要目标链兑换路径则返回为空
percent
String
一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比
router
String
币种兑换的一条路径
subRouterList
Array
DEX Router集合信息
dexName
String
DEX 协议名称
fromToken
Object
询价币种信息
decimals
Integer
币种精度如 (如： 18)
tokenContractAddress
String
币种合约地址(如：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
tokenSymbol
String
币种简称 (如：WETH)
toToken
Object
目标币种信息
decimals
Integer
币种精度 (如： 6)
tokenContractAddress
String
币种合约地址 (如：0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)
tokenSymbol
String
币种符号 (如：USDC)
fromChainNetworkFee
String
询价路径预估消耗的源链网络费用 (以主网币精度显示)
toChainNetworkFee
String
询价路径预估消耗的目标链网络费用 (以主网币精度显示)
minimumReceived
String
目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量)
toTokenAmount
String
目标币种的兑换数量
获取支持的桥信息
交易授权
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/cross-chain/quote?amount=15&fromChainIndex=324&toChainIndex=42161&fromTokenAddress=0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4&toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&slippage=0.07'
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
"fromChainIndex"
:
"56"
,
"fromChainId"
:
"56"
,
"fromToken"
:
{
"decimals"
:
18
,
"tokenContractAddress"
:
"0x55d398326f99059ff775485246999027b3197955"
,
"tokenSymbol"
:
"USDT"
}
,
"fromTokenAmount"
:
"30000000000000000000"
,
"routerList"
:
[
{
"estimateTime"
:
"290"
,
"fromDexRouterList"
:
[
{
"router"
:
"0x55d398326f99059ff775485246999027b3197955--0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c--0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
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
"decimals"
:
18
,
"tokenContractAddress"
:
"0x55d398326f99059ff775485246999027b3197955"
,
"tokenSymbol"
:
"USDT"
}
,
"toToken"
:
{
"decimals"
:
18
,
"tokenContractAddress"
:
"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
,
"tokenSymbol"
:
"WBNB"
}
}
,
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
"decimals"
:
18
,
"tokenContractAddress"
:
"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
,
"tokenSymbol"
:
"WBNB"
}
,
"toToken"
:
{
"decimals"
:
18
,
"tokenContractAddress"
:
"0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"
,
"tokenSymbol"
:
"USDC"
}
}
]
}
]
,
"minimumReceived"
:
"28635611"
,
"needApprove"
:
1
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
"1.090044714717251827012"
,
"otherNativeFee"
:
"0"
,
"crossChainFeeTokenAddress"
:
"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
}
,
"toDexRouterList"
:
[
{
"router"
:
"0x7ceb23fd6bc0add59e62ac25578270cff1b9f619--0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
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
"decimals"
:
18
,
"tokenContractAddress"
:
"0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"
,
"tokenSymbol"
:
"WETH"
}
,
"toToken"
:
{
"decimals"
:
18
,
"tokenContractAddress"
:
"0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"
,
"tokenSymbol"
:
"WMATIC"
}
}
]
}
]
,
"toTokenAmount"
:
"28924860"
}
]
,
"toChainId"
:
"42161"
,
"toChainIndex"
:
"42161"
,
"toToken"
:
{
"decimals"
:
6
,
"tokenContractAddress"
:
"0xff970a61a04b1ca14834a43f5de4533ebddb5cc8"
,
"tokenSymbol"
:
"USDC.e"
}
}
]
,
"msg"
:
""
}
获取支持的桥信息
交易授权

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">跨链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-route-information" style="color:inherit">获取路径信息</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取路径信息">获取路径信息<a class="index_header-anchor__Xqb+L" href="#获取路径信息" style="opacity:0">#</a></h1><p>通过欧易 DEX 跨链聚合器获取综合最优路径。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/cross-chain/quote</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>fromChainIndex</td><td>String</td><td>是</td><td>源链 ID (如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">链 ID 列表</a>)</td></tr><tr><td>toChainIndex</td><td>String</td><td>是</td><td>目标链 ID (如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">链 ID 列表</a>)</td></tr><tr><td>fromChainId</td><td>String</td><td>是</td><td>源链 ID，即将废弃</td></tr><tr><td>toChainId</td><td>String</td><td>是</td><td>目标链 ID，即将废弃</td></tr><tr><td>fromTokenAddress</td><td>String</td><td>是</td><td>询价币种合约地址 (如<code>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</code> )</td></tr><tr><td>toTokenAddress</td><td>String</td><td>是</td><td>目标币种合约地址 (如<code>TEkxiTehnzSmSe2XqrBj4w32RUN966rdz8</code> )</td></tr><tr><td>amount</td><td>String</td><td>是</td><td>币种询价数量 <br/> (数量需包含精度，如授权 <code>1.00</code> USDT 需输入 <code>1000000</code>，授权 <code>1.00</code> DAI 需输入 <code>1000000000000000000</code> ),币种精度可透过<a href="/zh-hans/build/docs/waas/dex-crosschain-get-tokens">币种列表</a>取得</td></tr><tr><td>slippage</td><td>String</td><td>是</td><td>滑点限制，最小值：<code>0.002</code>，最大值：<code>0.5</code>。（如：0.005代表你接受这笔交易最大 0.5%滑点，0.5 就代表你接受这笔交易最大 50%的滑点）</td></tr><tr><td>sort</td><td>Integer</td><td>否</td><td>跨链路径选择，默认返回 1 <br/> <br/> 0 代表预计获得数量最多的路径 <br/> <br/> 1 代表综合计算获得数量、网络费用、滑点、跨链桥费后的最优路径 <br/> <br/> 2 代表最快路径，是耗时最少的路径</td></tr><tr><td>dexIds</td><td>String</td><td>否</td><td>限定询价的流动性池 dexId , 多个组合按 , 分隔 (如 1,50,180 ，更多可查看流动性列表)</td></tr><tr><td>feePercent</td><td>String</td><td>否</td><td>发送到分佣地址的询价币种数量百分比 <code>最小百分比：0</code> <code>最大百分比：3</code></td></tr><tr><td>allowBridge</td><td>Array</td><td>否</td><td>指定该跨链桥是否包含在路径里面 (如<code>[211,235]</code>)</td></tr><tr><td>denyBridge</td><td>Array</td><td>否</td><td>指定该跨链桥是否不包含在路径里面 (如<code>[211,235]</code>)</td></tr><tr><td>priceImpactProtectionPercentage</td><td>String</td><td>否</td><td>(可选，默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。<br/> <br/> 当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。<br/> <br/> 这是一个<strong>可选开启</strong>的功能，默认值为 0.9。当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。<br/><br/> <strong>注意：</strong>当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>fromChainId</td><td>String</td><td>源链 ID (如1: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>)</td></tr><tr><td>toChainId</td><td>String</td><td>目标链 ID (如1: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>)</td></tr><tr><td>fromTokenAmount</td><td>String</td><td>询价币种的兑换数量 (如：500000000000000000000000)</td></tr><tr><td><strong>fromToken</strong></td><td><strong>Object</strong></td><td><strong>询价币种信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度 (如： 18)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如 ：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如 WETH)</td></tr><tr><td><strong>toToken</strong></td><td><strong>Object</strong></td><td><strong>目标链币种基础信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度(如： 6)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址(如： 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如： USDC)</td></tr><tr><td><strong>routerList</strong></td><td><strong>Array</strong></td><td><strong>询价路径数据集合</strong></td></tr><tr><td><strong>router</strong></td><td><strong>Object</strong></td><td><strong>跨链桥基础信息</strong></td></tr><tr><td>bridgeId</td><td>Integer</td><td>跨链桥 ID (如211)</td></tr><tr><td>bridgeName</td><td>String</td><td>跨链桥名称 (如cBridge)</td></tr><tr><td>otherNativeFee</td><td>String</td><td>部分跨链桥会额外收取一定数量的源链主网币，作为跨链桥手续费，并不是所有跨链桥都会收取该部分费用。目前收取该费用的跨链桥有 Stargate、Wanchain、Arbitrum 官方桥、zkSync Era 官方桥、Linea 官方桥。使用该三方桥需支付otherNativeFee才能完成交易。</td></tr><tr><td>otherNativeFeeUsd</td><td>String</td><td>部分跨链桥额外收取费用的美元计价</td></tr><tr><td>crossChainFee</td><td>String</td><td>跨链桥收取的费用，一般为稳定币或者WETH</td></tr><tr><td>crossChainFeeUsd</td><td>String</td><td>跨链桥收取的费用的美元计价</td></tr><tr><td>crossChainFeeTokenAddress</td><td>String</td><td>跨链桥费币种信息（如：0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE 代表主网代币地址）</td></tr><tr><td>estimateGasFee</td><td>String</td><td>以 wei 为单位的预估消耗的 gas</td></tr><tr><td>estimateGasFeeUsd</td><td>String</td><td>预估消耗 gas 费用的美元计价</td></tr><tr><td>estimatedTime</td><td>String</td><td>预估的跨链交易完成时间，以秒为单位，时间根据历史成功订单交易完成时间动态计算得出</td></tr><tr><td><strong>fromDexRouterList</strong></td><td><strong>Array</strong></td><td><strong>源链兑换路径基础信息, 如果不需要源链兑换路径则返回空</strong></td></tr><tr><td><strong>percent</strong></td><td><strong>String</strong></td><td><strong>一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比</strong></td></tr><tr><td>router</td><td>String</td><td>币种兑换的一条路径</td></tr><tr><td><strong>subRouterList</strong></td><td><strong>Array</strong></td><td><strong>DEX router集合信息</strong></td></tr><tr><td><strong>dexProtocol</strong></td><td><strong>Array</strong></td><td><strong>兑换路径中执行的 DEX 协议</strong></td></tr><tr><td>dexName</td><td>String</td><td>DEX 协议名称</td></tr><tr><td>percent</td><td>String</td><td>一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比 (如：100)</td></tr><tr><td><strong>fromToken</strong></td><td><strong>Object</strong></td><td><strong>询价币种信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度 (如： 18)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如：WETH)</td></tr><tr><td><strong>toToken</strong></td><td><strong>Object</strong></td><td><strong>目标币种信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度 (如： 6)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如：0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种符号 (如：USDC)</td></tr><tr><td><strong>toDexRouterList</strong></td><td><strong>Array</strong></td><td><strong>目标链兑换路径基础信息，如果不需要目标链兑换路径则返回为空</strong></td></tr><tr><td>percent</td><td>String</td><td>一条路径中单一 DEX 协议的兑换资产占所有 DEX 协议百分比</td></tr><tr><td>router</td><td>String</td><td>币种兑换的一条路径</td></tr><tr><td><strong>subRouterList</strong></td><td><strong>Array</strong></td><td><strong>DEX Router集合信息</strong></td></tr><tr><td>dexName</td><td>String</td><td>DEX 协议名称</td></tr><tr><td><strong>fromToken</strong></td><td><strong>Object</strong></td><td><strong>询价币种信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度如 (如： 18)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址(如：0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如：WETH)</td></tr><tr><td><strong>toToken</strong></td><td><strong>Object</strong></td><td><strong>目标币种信息</strong></td></tr><tr><td>decimals</td><td>Integer</td><td>币种精度 (如： 6)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如：0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种符号 (如：USDC)</td></tr><tr><td>fromChainNetworkFee</td><td>String</td><td>询价路径预估消耗的源链网络费用 (以主网币精度显示)</td></tr><tr><td>toChainNetworkFee</td><td>String</td><td>询价路径预估消耗的目标链网络费用 (以主网币精度显示)</td></tr><tr><td>minimumReceived</td><td>String</td><td>目标币种的最小兑换数量 (兑换价格达到滑点限制的极限值时，目标币种的兑换数量)</td></tr><tr><td>toTokenAmount</td><td>String</td><td>目标币种的兑换数量</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-supported-bridges" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的桥信息</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-approve-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易授权</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/cross-chain/quote?amount=15&amp;fromChainIndex=324&amp;toChainIndex=42161&amp;fromTokenAddress=0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4&amp;toTokenAddress=0xff970a61a04b1ca14834a43f5de4533ebddb5cc8&amp;slippage=0.07'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"code"</span><span class="token operator">:</span><span class="token string">"0"</span><span class="token punctuation">,</span>
  <span class="token property">"data"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"fromChainIndex"</span><span class="token operator">:</span><span class="token string">"56"</span><span class="token punctuation">,</span>
  <span class="token property">"fromChainId"</span><span class="token operator">:</span><span class="token string">"56"</span><span class="token punctuation">,</span>
  <span class="token property">"fromToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x55d398326f99059ff775485246999027b3197955"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"USDT"</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"fromTokenAmount"</span><span class="token operator">:</span><span class="token string">"30000000000000000000"</span><span class="token punctuation">,</span>
  <span class="token property">"routerList"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"estimateTime"</span><span class="token operator">:</span><span class="token string">"290"</span><span class="token punctuation">,</span>
  <span class="token property">"fromDexRouterList"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"router"</span><span class="token operator">:</span><span class="token string">"0x55d398326f99059ff775485246999027b3197955--0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c--0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"</span><span class="token punctuation">,</span>
  <span class="token property">"routerPercent"</span><span class="token operator">:</span><span class="token string">"100"</span><span class="token punctuation">,</span>
  <span class="token property">"subRouterList"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexProtocol"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexName"</span><span class="token operator">:</span><span class="token string">"Uniswap V3"</span><span class="token punctuation">,</span>
  <span class="token property">"percent"</span><span class="token operator">:</span><span class="token string">"100"</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"fromToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x55d398326f99059ff775485246999027b3197955"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"USDT"</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"toToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"WBNB"</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexProtocol"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexName"</span><span class="token operator">:</span><span class="token string">"Uniswap V3"</span><span class="token punctuation">,</span>
  <span class="token property">"percent"</span><span class="token operator">:</span><span class="token string">"100"</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"fromToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"WBNB"</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"toToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"USDC"</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"minimumReceived"</span><span class="token operator">:</span><span class="token string">"28635611"</span><span class="token punctuation">,</span>
  <span class="token property">"needApprove"</span><span class="token operator">:</span><span class="token number">1</span><span class="token punctuation">,</span>
  <span class="token property">"router"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"bridgeId"</span><span class="token operator">:</span><span class="token number">235</span><span class="token punctuation">,</span>
  <span class="token property">"bridgeName"</span><span class="token operator">:</span><span class="token string">"swft"</span><span class="token punctuation">,</span>
  <span class="token property">"crossChainFee"</span><span class="token operator">:</span><span class="token string">"1.090044714717251827012"</span><span class="token punctuation">,</span>
  <span class="token property">"otherNativeFee"</span><span class="token operator">:</span><span class="token string">"0"</span><span class="token punctuation">,</span>
  <span class="token property">"crossChainFeeTokenAddress"</span><span class="token operator">:</span><span class="token string">"0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"toDexRouterList"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"router"</span><span class="token operator">:</span><span class="token string">"0x7ceb23fd6bc0add59e62ac25578270cff1b9f619--0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"</span><span class="token punctuation">,</span>
  <span class="token property">"routerPercent"</span><span class="token operator">:</span><span class="token string">"100"</span><span class="token punctuation">,</span>
  <span class="token property">"subRouterList"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexProtocol"</span><span class="token operator">:</span><span class="token punctuation">[</span>
<span class="token punctuation">{</span>
  <span class="token property">"dexName"</span><span class="token operator">:</span><span class="token string">"Uniswap V3"</span><span class="token punctuation">,</span>
  <span class="token property">"percent"</span><span class="token operator">:</span><span class="token string">"100"</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"fromToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"WETH"</span>
<span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"toToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">18</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"WMATIC"</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"toTokenAmount"</span><span class="token operator">:</span><span class="token string">"28924860"</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"toChainId"</span><span class="token operator">:</span><span class="token string">"42161"</span><span class="token punctuation">,</span>
  <span class="token property">"toChainIndex"</span><span class="token operator">:</span><span class="token string">"42161"</span><span class="token punctuation">,</span>
  <span class="token property">"toToken"</span><span class="token operator">:</span><span class="token punctuation">{</span>
  <span class="token property">"decimals"</span><span class="token operator">:</span><span class="token number">6</span><span class="token punctuation">,</span>
  <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0xff970a61a04b1ca14834a43f5de4533ebddb5cc8"</span><span class="token punctuation">,</span>
  <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"USDC.e"</span>
<span class="token punctuation">}</span>
<span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span><span class="token string">""</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-supported-bridges" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的桥信息</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-approve-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易授权</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取路径信息"
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
