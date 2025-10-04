# 获取流动性列表 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-liquidity#请求示例  
**抓取时间:** 2025-05-27 05:43:19  
**字数:** 1303

## 导航路径
DEX API > 交易 API > API 参考 > 获取流动性列表

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
获取流动性列表
获取流动性列表
#
获取欧易 DEX 聚合器协议支持兑换的流动性列表。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/get-liquidity
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
1
: Ethereum，更多可查看
这里
。
chainId
String
是
链的唯一标识。 即将废弃。
响应参数
#
参数
类型
描述
id
String
流动性 ID (如:
34
)
name
String
流动性池名称 (如:
Uniswap V2
)
logo
String
流动性协议标志 URL (如:
https://static.okx.com/cdn/wallet/logo/UNI.png
)
获取币种列表
交易授权
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/get-liquidity?chainIndex=1'
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
"id"
:
"34"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/UNI.png"
,
"name"
:
"Uniswap V2"
}
,
{
"id"
:
"29"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/SUSHI.png"
,
"name"
:
"SushiSwap"
}
,
{
"id"
:
"47"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/Dex_DefiSwap.png"
,
"name"
:
"DeFi Swap"
}
,
{
"id"
:
"49"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/convxswap.png"
,
"name"
:
"Convergence"
}
,
{
"id"
:
"48"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/luaswap.png"
,
"name"
:
"LuaSwap"
}
,
{
"id"
:
"40"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/SHIB.png"
,
"name"
:
"ShibaSwap"
}
,
{
"id"
:
"30"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/pancake.png"
,
"name"
:
"PancakeSwap"
}
,
{
"id"
:
"53"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/UNI.png"
,
"name"
:
"Uniswap V3"
}
,
{
"id"
:
"54"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/balancer.png"
,
"name"
:
"Balancer V1"
}
,
{
"id"
:
"51"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/balancer.png"
,
"name"
:
"Balancer V2"
}
,
{
"id"
:
"55"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve V1"
}
,
{
"id"
:
"259"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve"
}
,
{
"id"
:
"58"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve V2"
}
,
{
"id"
:
"52"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/bancor.png"
,
"name"
:
"Bancor"
}
,
{
"id"
:
"59"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Kyber.png"
,
"name"
:
"Kyber"
}
,
{
"id"
:
"81"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Synapse.png"
,
"name"
:
"Synapse"
}
,
{
"id"
:
"83"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Wombat.png"
,
"name"
:
"Wombat"
}
,
{
"id"
:
"80"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/DODO.png"
,
"name"
:
"DODO"
}
,
{
"id"
:
"82"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Shell.png"
,
"name"
:
"Shell"
}
,
{
"id"
:
"88"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/DODO.png"
,
"name"
:
"DODO V2"
}
,
{
"id"
:
"264"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/DODO.png"
,
"name"
:
"DODO V3"
}
,
{
"id"
:
"91"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Smoothy.png"
,
"name"
:
"Smoothy"
}
,
{
"id"
:
"92"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/RadioShack.png"
,
"name"
:
"RadioShack"
}
,
{
"id"
:
"90"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/ORION.png"
,
"name"
:
"Orion"
}
,
{
"id"
:
"89"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/FraxFinance.png"
,
"name"
:
"FraxSwap"
}
,
{
"id"
:
"99"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/okb.png"
,
"name"
:
"OKX DEX"
}
,
{
"id"
:
"28"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Hashflow.png"
,
"name"
:
"HashFlow"
}
,
{
"id"
:
"101"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Swapr.png"
,
"name"
:
"Swapr"
}
,
{
"id"
:
"351"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_DFX.png"
,
"name"
:
"DFX Finance V3"
}
,
{
"id"
:
"104"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_bancor.png"
,
"name"
:
"Bancor V3"
}
,
{
"id"
:
"105"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_PSM.png"
,
"name"
:
"PSM"
}
,
{
"id"
:
"106"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/balancer.png"
,
"name"
:
"Balancer"
}
,
{
"id"
:
"108"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Verse.png"
,
"name"
:
"Verse"
}
,
{
"id"
:
"110"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_1inch_limit_order.png"
,
"name"
:
"1inch Limit Order"
}
,
{
"id"
:
"248"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/okb.png"
,
"name"
:
"OKX Limit Order"
}
,
{
"id"
:
"132"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_defiplaza.png"
,
"name"
:
"DefiPlaza"
}
,
{
"id"
:
"114"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Swerve.png"
,
"name"
:
"Swerve"
}
,
{
"id"
:
"113"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Kyber.png"
,
"name"
:
"Kyber Elastic"
}
,
{
"id"
:
"131"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_defiplaza.png"
,
"name"
:
"StablePlaza"
}
,
{
"id"
:
"130"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_0x_limit_order.png"
,
"name"
:
"0x Limit Order"
}
,
{
"id"
:
"133"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Clipper.png"
,
"name"
:
"Clipper"
}
,
{
"id"
:
"134"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Lido.png"
,
"name"
:
"Lido"
}
,
{
"id"
:
"135"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_NOMISWAP.png"
,
"name"
:
"Nomiswap Stable"
}
,
{
"id"
:
"136"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/solidly.png"
,
"name"
:
"Solidly"
}
,
{
"id"
:
"215"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/traderjoexyz.png"
,
"name"
:
"Trader Joe V2.1"
}
,
{
"id"
:
"153"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Cafe_Swap.png"
,
"name"
:
"Cafe Swap"
}
,
{
"id"
:
"141"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_ELK.png"
,
"name"
:
"ELK"
}
,
{
"id"
:
"102"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Unifi.png"
,
"name"
:
"Unifi"
}
,
{
"id"
:
"159"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_LINKSWAP.png"
,
"name"
:
"LINKSWAP"
}
,
{
"id"
:
"160"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Sake_Swap.png"
,
"name"
:
"Sake Swap"
}
,
{
"id"
:
"27"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve 3CRV"
}
,
{
"id"
:
"202"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"
,
"name"
:
"Aave V2"
}
,
{
"id"
:
"230"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"
,
"name"
:
"Aave V3"
}
,
{
"id"
:
"199"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Compound.png"
,
"name"
:
"Compound"
}
,
{
"id"
:
"266"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Compound.png"
,
"name"
:
"Compound V3"
}
,
{
"id"
:
"184"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_logo_Frax.png"
,
"name"
:
"sfrxETH"
}
,
{
"id"
:
"356"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_logo_Frax.png"
,
"name"
:
"sFRAX"
}
,
{
"id"
:
"186"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Lido.png"
,
"name"
:
"stMatic"
}
,
{
"id"
:
"200"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/pancake.png"
,
"name"
:
"PancakeSwap V3"
}
,
{
"id"
:
"203"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Rocketpool.png"
,
"name"
:
"RocketPool"
}
,
{
"id"
:
"207"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_kronos.png"
,
"name"
:
"Kronos"
}
,
{
"id"
:
"204"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_1inch_limit_order.png"
,
"name"
:
"1inch LP v1.1"
}
,
{
"id"
:
"210"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve TNG"
}
,
{
"id"
:
"330"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"CurveNG"
}
,
{
"id"
:
"214"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Mooniswap.png"
,
"name"
:
"Mooniswap"
}
,
{
"id"
:
"213"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Integral.png"
,
"name"
:
"Integral"
}
,
{
"id"
:
"218"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/dex_Maverick.png"
,
"name"
:
"Maverick V1"
}
,
{
"id"
:
"226"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Curve.png"
,
"name"
:
"Curve LLAMMA"
}
,
{
"id"
:
"234"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/Dex_xSigma.png"
,
"name"
:
"xSigma"
}
,
{
"id"
:
"239"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/Dex_Sushiswap_V3.png"
,
"name"
:
"Sushiswap V3"
}
,
{
"id"
:
"257"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/Synthetix.png"
,
"name"
:
"Wrapped Synthetix"
}
,
{
"id"
:
"262"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/solidly.png"
,
"name"
:
"Solidly V3"
}
,
{
"id"
:
"265"
,
"logo"
:
"https://static.okx.com/cdn/explorer/dex/logo/SmarDex.png"
,
"name"
:
"SmarDex"
}
,
{
"id"
:
"328"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/sDai.png"
,
"name"
:
"sDai"
}
,
{
"id"
:
"365"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/Angle.png"
,
"name"
:
"Angle"
}
,
{
"id"
:
"352"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/Angle.png"
,
"name"
:
"Angle Stake"
}
,
{
"id"
:
"258"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/okb.png"
,
"name"
:
"OKX Pre Limit Order"
}
,
{
"id"
:
"354"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/Origin.png"
,
"name"
:
"Origin Wrapper"
}
,
{
"id"
:
"355"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/Origin.png"
,
"name"
:
"Origin"
}
,
{
"id"
:
"368"
,
"logo"
:
"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"
,
"name"
:
"Bgd Aave Static"
}
,
{
"id"
:
"379"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/Unicly.png"
,
"name"
:
"Unicly"
}
,
{
"id"
:
"394"
,
"logo"
:
"https://static.okx.com/cdn/web3/dex/logo/novabits.png"
,
"name"
:
"Novabits V3"
}
]
,
"msg"
:
""
}
获取币种列表
交易授权

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-liquidity" style="color:inherit">获取流动性列表</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取流动性列表">获取流动性列表<a class="index_header-anchor__Xqb+L" href="#获取流动性列表" style="opacity:0">#</a></h1><p>获取欧易 DEX 聚合器协议支持兑换的流动性列表。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/get-liquidity</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 <br/>如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>是</td><td>链的唯一标识。 即将废弃。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>id</td><td>String</td><td>流动性 ID (如: <code>34</code>)</td></tr><tr><td>name</td><td>String</td><td>流动性池名称 (如: <code>Uniswap V2</code>)</td></tr><tr><td>logo</td><td>String</td><td>流动性协议标志 URL (如:<a class="items-center" href="https://static.okx.com/cdn/wallet/logo/UNI.png" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://static.okx.com/cdn/wallet/logo/UNI.png<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>)</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-tokens" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取币种列表</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-approve-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易授权</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/get-liquidity?chainIndex=1'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"34"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/UNI.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Uniswap V2"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"29"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/SUSHI.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"SushiSwap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"47"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/Dex_DefiSwap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DeFi Swap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"49"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/convxswap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Convergence"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"48"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/luaswap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"LuaSwap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"40"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/SHIB.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"ShibaSwap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"30"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/pancake.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"PancakeSwap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"53"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/UNI.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Uniswap V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"54"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/balancer.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Balancer V1"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"51"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/balancer.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Balancer V2"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"55"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve V1"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"259"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"58"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve V2"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"52"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/bancor.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Bancor"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"59"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Kyber.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Kyber"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"81"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Synapse.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Synapse"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"83"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Wombat.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Wombat"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"80"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/DODO.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DODO"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"82"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Shell.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Shell"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"88"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/DODO.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DODO V2"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"264"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/DODO.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DODO V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"91"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Smoothy.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Smoothy"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"92"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/RadioShack.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"RadioShack"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"90"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/ORION.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Orion"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"89"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/FraxFinance.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"FraxSwap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"99"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/okb.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"OKX DEX"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"28"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Hashflow.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"HashFlow"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"101"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Swapr.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Swapr"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"351"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_DFX.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DFX Finance V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"104"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_bancor.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Bancor V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"105"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_PSM.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"PSM"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"106"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/balancer.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Balancer"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"108"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Verse.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Verse"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"110"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_1inch_limit_order.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"1inch Limit Order"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"248"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/okb.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"OKX Limit Order"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"132"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_defiplaza.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"DefiPlaza"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"114"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Swerve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Swerve"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"113"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Kyber.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Kyber Elastic"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"131"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_defiplaza.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"StablePlaza"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"130"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_0x_limit_order.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"0x Limit Order"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"133"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Clipper.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Clipper"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"134"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Lido.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Lido"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"135"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_NOMISWAP.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Nomiswap Stable"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"136"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/solidly.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Solidly"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"215"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/traderjoexyz.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Trader Joe V2.1"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"153"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Cafe_Swap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Cafe Swap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"141"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_ELK.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"ELK"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"102"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Unifi.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Unifi"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"159"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_LINKSWAP.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"LINKSWAP"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"160"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Sake_Swap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Sake Swap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"27"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve 3CRV"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"202"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Aave V2"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"230"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Aave V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"199"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Compound.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Compound"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"266"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Compound.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Compound V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"184"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_logo_Frax.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"sfrxETH"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"356"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_logo_Frax.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"sFRAX"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"186"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Lido.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"stMatic"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"200"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/pancake.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"PancakeSwap V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"203"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Rocketpool.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"RocketPool"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"207"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_kronos.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Kronos"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"204"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_1inch_limit_order.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"1inch LP v1.1"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"210"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve TNG"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"330"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"CurveNG"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"214"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Mooniswap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Mooniswap"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"213"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Integral.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Integral"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"218"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_Maverick.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Maverick V1"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"226"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Curve.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Curve LLAMMA"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"234"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/Dex_xSigma.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"xSigma"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"239"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/Dex_Sushiswap_V3.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Sushiswap V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"257"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/Synthetix.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Wrapped Synthetix"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"262"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/solidly.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Solidly V3"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"265"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/dex/logo/SmarDex.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"SmarDex"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"328"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/sDai.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"sDai"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"365"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/Angle.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Angle"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"352"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/Angle.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Angle Stake"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"258"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/okb.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"OKX Pre Limit Order"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"354"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/Origin.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Origin Wrapper"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"355"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/Origin.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Origin"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"368"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/Dex_Aave.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Bgd Aave Static"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"379"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/Unicly.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Unicly"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span> <span class="token string">"394"</span><span class="token punctuation">,</span>
    <span class="token property">"logo"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/web3/dex/logo/novabits.png"</span><span class="token punctuation">,</span>
    <span class="token property">"name"</span><span class="token operator">:</span> <span class="token string">"Novabits V3"</span>
  <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
  <span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-tokens" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取币种列表</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-approve-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易授权</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取流动性列表"
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
