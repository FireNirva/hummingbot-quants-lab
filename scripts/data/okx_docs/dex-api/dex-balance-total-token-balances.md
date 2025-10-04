# 获取资产明细 | API 参考 | 余额 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-balance-total-token-balances#请求参数  
**抓取时间:** 2025-05-27 07:26:29  
**字数:** 1200

## 导航路径
DEX API > 行情 API > API 参考 > 获取资产明细

## 目录
- API 参考
- 错误码
- Websocket
- API 参考
- 错误码
- API 参考
- 获取支持的链
- 获取总估值
- 获取资产明细
- 获取特定代币余额
- 错误码
- API 参考
- 错误码

---

DEX API
行情 API
余额 API
API 参考
获取资产明细
获取资产明细
#
查询地址持有的多个链或指定链的代币 余额列表。
请求路径
#
GET
https://web3.okx.com/api/v5/dex/balance/all-token-balances-by-address
请求参数
#
Parameter
Type
Required
Description
address
String
是
地址
chains
String
是
筛选需要获取资产明细的链，多条链以","分隔。最多支持 50 个。(如
1
代表Ethereum。更多可查看
这里
。)
excludeRiskToken
String
否
是否过滤风险空投代币和貔貅盘代币。默认过滤。
0
: 过滤
1
: 不过滤
对于貔貅盘代币，目前只支持
ETH
、
BSC
、
SOL
、
BASE
四条链，更多的链即将被支持。
响应参数
#
Parameter
Type
Description
tokenAssets
Array
代币余额
>chainIndex
String
链唯一标识
>tokenContractAddress
String
合约地址
>address
String
地址
>symbol
String
代币简称
>balance
String
代币数量
>rawBalance
String
代币的原始数量。更多的链即将被支持。对于不支持的链，该字段为空。
>tokenPrice
String
币种单位价值，以美元计价
>isRiskToken
Boolean
true
：命中风险空投代币和貔貅盘代币
false
：未命中风险空投代币和貔貅盘代币
获取总估值
获取特定代币余额
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/balance/asset/all-token-balances-by-address?address=0xEd0C6079229E2d407672a117c22b62064f4a4312&chains=1'
\
--header
'Content-Type: application/json'
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
\
响应示例
#
200
{
"code"
:
"0"
,
"msg"
:
"success"
,
"data"
:
[
{
"tokenAssets"
:
[
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x386ae941d4262b0ee96354499df2ab8442734ec0"
,
"symbol"
:
"PT-sUSDE-27FEB2025"
,
"balance"
:
"47042180.520700015"
,
"tokenPrice"
:
"0.968391562089677097"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"
,
"symbol"
:
"wstETH"
,
"balance"
:
"7565.892480395067"
,
"tokenPrice"
:
"4321.611627695311"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
,
"symbol"
:
"WBTC"
,
"balance"
:
"329.10055205"
,
"tokenPrice"
:
"98847.8"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x23878914efe38d27c4d67ab83ed1b93a74d4086a"
,
"symbol"
:
"aEthUSDT"
,
"balance"
:
"30057379.938443"
,
"tokenPrice"
:
"0.99978"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x657e8c867d8b37dcc18fa4caead9c45eb088c642"
,
"symbol"
:
"eBTC"
,
"balance"
:
"271.94970471"
,
"tokenPrice"
:
"99094.345321371"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x4d5f47fa6a74757f35c14fd3a6ef8e3c9bc514e8"
,
"symbol"
:
"aEthWETH"
,
"balance"
:
"6080.001975381972"
,
"tokenPrice"
:
"3634.32"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xe00bd3df25fb187d6abbb620b3dfd19839947b81"
,
"symbol"
:
"PT-sUSDE-27MAR2025"
,
"balance"
:
"19016580.895408865"
,
"tokenPrice"
:
"0.952031186961110727"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xa17581a9e3356d9a858b789d68b4d866e593ae94"
,
"symbol"
:
"cWETHv3"
,
"balance"
:
"3000.000734740809"
,
"tokenPrice"
:
"3663.74"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x9d39a5de30e57443bff2a8307a4256c8797a3497"
,
"symbol"
:
"sUSDe"
,
"balance"
:
"4863500.628333919"
,
"tokenPrice"
:
"1.144688569528375454"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xec5a52c685cc3ad79a6a347abace330d69e0b1ed"
,
"symbol"
:
"PT-LBTC-27MAR2025"
,
"balance"
:
"46.02912324"
,
"tokenPrice"
:
"97165.169717785655331396"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x8236a87084f8b84306f72007f36f2618a5634494"
,
"symbol"
:
"LBTC"
,
"balance"
:
"38.09998"
,
"tokenPrice"
:
"99187.19184268864"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xbeef047a543e45807105e51a8bbefcc5950fcfba"
,
"symbol"
:
"steakUSDT"
,
"balance"
:
"482651.8612595832"
,
"tokenPrice"
:
"1.063"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x4c9edd5852cd905f086c759e8383e09bff1e68b3"
,
"symbol"
:
"USDe"
,
"balance"
:
"69564"
,
"tokenPrice"
:
"0.99977"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9"
,
"symbol"
:
"sENA"
,
"balance"
:
"42294.989425"
,
"tokenPrice"
:
"1.19"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
""
,
"symbol"
:
"ETH"
,
"balance"
:
"8.135546539084933"
,
"tokenPrice"
:
"3638.63"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xbf5495efe5db9ce00f80364c8b423567e58d2110"
,
"symbol"
:
"ezETH"
,
"balance"
:
"5.270854886240325"
,
"tokenPrice"
:
"3763.152404188635320082"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x6b175474e89094c44da98b954eedeac495271d0f"
,
"symbol"
:
"DAI"
,
"balance"
:
"1196.2693184870445"
,
"tokenPrice"
:
"1.0002"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xc00e94cb662c3520282e6f5717214004a7f26888"
,
"symbol"
:
"COMP"
,
"balance"
:
"0.007643"
,
"tokenPrice"
:
"84.43345772756197"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x9abfc0f085c82ec1be31d30843965fcc63053ffe"
,
"symbol"
:
"Q*"
,
"balance"
:
"900"
,
"tokenPrice"
:
"0.000419255747329174"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xa1290d69c65a6fe4df752f95823fae25cb99e5a7"
,
"symbol"
:
"rsETH"
,
"balance"
:
"0.00007090104120006"
,
"tokenPrice"
:
"3765.640772858747921444"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x56015bbe3c01fe05bc30a8a9a9fd9a88917e7db3"
,
"symbol"
:
"CAT"
,
"balance"
:
"0.42"
,
"tokenPrice"
:
"0.06242994543936436"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xec53bf9167f50cdeb3ae105f56099aaab9061f83"
,
"symbol"
:
"EIGEN"
,
"balance"
:
"0.002496149915967488"
,
"tokenPrice"
:
"4.018538365202288"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x58d97b57bb95320f9a05dc918aef65434969c2b2"
,
"symbol"
:
"MORPHO"
,
"balance"
:
"0.001409373661132556"
,
"tokenPrice"
:
"3.3568669630371337"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6"
,
"symbol"
:
"STG"
,
"balance"
:
"0.000009547670354338"
,
"tokenPrice"
:
"0.49707759500034454"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xba3335588d9403515223f109edc4eb7269a9ab5d"
,
"symbol"
:
"GEAR"
,
"balance"
:
"0.000009005734110189"
,
"tokenPrice"
:
"0.012329598382413718"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x35fa164735182de50811e8e2e824cfb9b6118ac2"
,
"symbol"
:
"eETH"
,
"balance"
:
"0.000000000000000001"
,
"tokenPrice"
:
"3637.93"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xae7ab96520de3a18e5e111b5eaab095312d7fe84"
,
"symbol"
:
"stETH"
,
"balance"
:
"0.000000000000000001"
,
"tokenPrice"
:
"3637.93"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xa3931d71877c0e7a3148cb7eb4463524fec27fbd"
,
"symbol"
:
"sUSDS"
,
"balance"
:
"67435907.43236613"
,
"tokenPrice"
:
"0"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xa8705a14c79fa1cded70875510211fec822b3c30"
,
"symbol"
:
"BEEX"
,
"balance"
:
"5000000"
,
"tokenPrice"
:
"0"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0xabc0abace9fb9625fcefbedc423e8f94225bd251"
,
"symbol"
:
"TANUKI"
,
"balance"
:
"3548102.746002181"
,
"tokenPrice"
:
"0"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
,
{
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x356b8d89c1e1239cbbb9de4815c39a1474d5ba7d"
,
"symbol"
:
"syrupUSDT"
,
"balance"
:
"1750000"
,
"tokenPrice"
:
"0"
,
"isRiskToken"
:
false
,
"rawBalance"
:
""
,
"address"
:
"0xed0c6079229e2d407672a117c22b62064f4a4312"
}
]
}
]
}
获取总估值
获取特定代币余额

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">余额 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-total-token-balances" style="color:inherit">获取资产明细</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取资产明细">获取资产明细<a class="index_header-anchor__Xqb+L" href="#获取资产明细" style="opacity:0">#</a></h1><p>查询地址持有的多个链或指定链的代币 余额列表。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/balance/all-token-balances-by-address </code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>address</td><td>String</td><td>是</td><td>地址</td></tr><tr><td>chains</td><td>String</td><td>是</td><td>筛选需要获取资产明细的链，多条链以","分隔。最多支持 50 个。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>excludeRiskToken</td><td>String</td><td>否</td><td>是否过滤风险空投代币和貔貅盘代币。默认过滤。<br/><code>0</code>: 过滤 <br/> <code>1</code>: 不过滤 <br/>对于貔貅盘代币，目前只支持<code>ETH</code>、<code>BSC</code>、<code>SOL</code>、<code>BASE</code> 四条链，更多的链即将被支持。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>tokenAssets</td><td>Array</td><td>代币余额</td></tr><tr><td>&gt;chainIndex</td><td>String</td><td>链唯一标识</td></tr><tr><td>&gt;tokenContractAddress</td><td>String</td><td>合约地址</td></tr><tr><td>&gt;address</td><td>String</td><td>地址</td></tr><tr><td>&gt;symbol</td><td>String</td><td>代币简称</td></tr><tr><td>&gt;balance</td><td>String</td><td>代币数量</td></tr><tr><td>&gt;rawBalance</td><td>String</td><td>代币的原始数量。更多的链即将被支持。对于不支持的链，该字段为空。</td></tr><tr><td>&gt;tokenPrice</td><td>String</td><td>币种单位价值，以美元计价</td></tr><tr><td>&gt;isRiskToken</td><td>Boolean</td><td><code>true</code>：命中风险空投代币和貔貅盘代币 <br/> <code>false</code>：未命中风险空投代币和貔貅盘代币</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-total-value" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取总估值</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-balance-specific-token-balance" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取特定代币余额</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/balance/asset/all-token-balances-by-address?address=0xEd0C6079229E2d407672a117c22b62064f4a4312&amp;chains=1'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> <span class="token punctuation">\</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"tokenAssets"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x386ae941d4262b0ee96354499df2ab8442734ec0"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"PT-sUSDE-27FEB2025"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"47042180.520700015"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.968391562089677097"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x7f39c581f595b53c5cb19bd0b3f8da6c935e2ca0"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"wstETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"7565.892480395067"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"4321.611627695311"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"WBTC"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"329.10055205"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"98847.8"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x23878914efe38d27c4d67ab83ed1b93a74d4086a"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"aEthUSDT"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"30057379.938443"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.99978"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x657e8c867d8b37dcc18fa4caead9c45eb088c642"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"eBTC"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"271.94970471"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"99094.345321371"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x4d5f47fa6a74757f35c14fd3a6ef8e3c9bc514e8"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"aEthWETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"6080.001975381972"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3634.32"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xe00bd3df25fb187d6abbb620b3dfd19839947b81"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"PT-sUSDE-27MAR2025"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"19016580.895408865"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.952031186961110727"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa17581a9e3356d9a858b789d68b4d866e593ae94"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"cWETHv3"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"3000.000734740809"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3663.74"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>

                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x9d39a5de30e57443bff2a8307a4256c8797a3497"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"sUSDe"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"4863500.628333919"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"1.144688569528375454"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xec5a52c685cc3ad79a6a347abace330d69e0b1ed"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"PT-LBTC-27MAR2025"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"46.02912324"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"97165.169717785655331396"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x8236a87084f8b84306f72007f36f2618a5634494"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"LBTC"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"38.09998"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"99187.19184268864"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xbeef047a543e45807105e51a8bbefcc5950fcfba"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"steakUSDT"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"482651.8612595832"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"1.063"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x4c9edd5852cd905f086c759e8383e09bff1e68b3"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"USDe"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"69564"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.99977"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x8be3460a480c80728a8c4d7a5d5303c85ba7b3b9"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"sENA"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"42294.989425"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"1.19"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"ETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"8.135546539084933"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3638.63"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xbf5495efe5db9ce00f80364c8b423567e58d2110"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"ezETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"5.270854886240325"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3763.152404188635320082"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x6b175474e89094c44da98b954eedeac495271d0f"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"DAI"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"1196.2693184870445"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"1.0002"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xc00e94cb662c3520282e6f5717214004a7f26888"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"COMP"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.007643"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"84.43345772756197"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x9abfc0f085c82ec1be31d30843965fcc63053ffe"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"Q*"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"900"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.000419255747329174"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa1290d69c65a6fe4df752f95823fae25cb99e5a7"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"rsETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.00007090104120006"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3765.640772858747921444"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x56015bbe3c01fe05bc30a8a9a9fd9a88917e7db3"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"CAT"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.42"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.06242994543936436"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xec53bf9167f50cdeb3ae105f56099aaab9061f83"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"EIGEN"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.002496149915967488"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"4.018538365202288"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x58d97b57bb95320f9a05dc918aef65434969c2b2"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"MORPHO"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.001409373661132556"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3.3568669630371337"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xaf5191b0de278c7286d6c7cc6ab6bb8a73ba2cd6"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"STG"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.000009547670354338"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.49707759500034454"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xba3335588d9403515223f109edc4eb7269a9ab5d"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"GEAR"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.000009005734110189"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0.012329598382413718"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x35fa164735182de50811e8e2e824cfb9b6118ac2"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"eETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.000000000000000001"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3637.93"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xae7ab96520de3a18e5e111b5eaab095312d7fe84"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"stETH"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0.000000000000000001"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3637.93"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa3931d71877c0e7a3148cb7eb4463524fec27fbd"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"sUSDS"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"67435907.43236613"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xa8705a14c79fa1cded70875510211fec822b3c30"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"BEEX"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"5000000"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xabc0abace9fb9625fcefbedc423e8f94225bd251"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"TANUKI"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"3548102.746002181"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x356b8d89c1e1239cbbb9de4815c39a1474d5ba7d"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"syrupUSDT"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"1750000"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xed0c6079229e2d407672a117c22b62064f4a4312"</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-total-value" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取总估值</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-balance-specific-token-balance" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取特定代币余额</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "行情 API",
    "API 参考",
    "获取资产明细"
  ],
  "sidebar_links": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "获取支持的链",
    "获取总估值",
    "获取资产明细",
    "获取特定代币余额",
    "错误码",
    "API 参考",
    "错误码"
  ],
  "toc": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "获取支持的链",
    "获取总估值",
    "获取资产明细",
    "获取特定代币余额",
    "错误码",
    "API 参考",
    "错误码"
  ]
}
```

</details>
