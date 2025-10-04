# 查询交易状态 | API 参考 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-transaction-status#响应示例  
**抓取时间:** 2025-05-27 02:56:53  
**字数:** 268

## 导航路径
DEX API > 交易 API > API 参考 > 查询交易状态

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
查询交易状态
查询交易状态
#
根据 txhash 查询跨链兑换最终交易状态。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/cross-chain/status
请求参数
#
参数
类型
必传
描述
hash
String
是
源链 Hash 地址
chainIndex
String
否
源链 ID。
如
1
: Ethereum，更多可查看
这里
。
chainId
String
否
源链 ID。即将废弃。
响应参数
#
参数
类型
描述
fromChainId
String
源链 ID
toChainId
String
目标链 ID
fromTxHash
String
源链交易 Hash
toTxHash
String
目标链交易 Hash
fromAmount
String
询价币种的兑换数量 (数量包含精度，如 1.00 USDT 则为 1000000)
fromTokenAddress
String
询价币种合约地址 (如0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE)
toAmount
String
目标币种的兑换数量 (数量包含精度，如 1.00 USDT 则为 1000000)
toTokenAddress
String
目标币种合约地址 (如0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)｜
errorMsg
String
错误信息
bridgeHash
String
目标链跨链桥交易 Hash
refundChainId
String
退款链 ID
refundTokenAddress
String
退款币种的合约地址
refundTxHash
String
退款交易 Hash
sourceChainGasfee
String
源链兑换实际消耗的gas fee
crossChainFee
Object
跨链桥实际收取的费用
symbol
String
跨链桥币种symbol
address
String
跨链桥币种地址
amount
String
跨链桥收取的数量
crossChainInfo
Object
跨链桥的信息
memo
String
/build-tx 中携带的自定义参数
destinationChainGasfee
String
目标链兑换实际消耗的gas fee
detailStatus
String
WAITING (订单处理中) FROM_SUCCESS (源链订单成功) FROM_FAILURE (源链订单失败) BRIDGE_PENDING (跨链桥订单执行中) BRIDGE_SUCCESS (跨链桥订单成功) SUCCESS (跨链兑换订单成功) REFUND (跨链失败，订单退款)
status
String
PENDING （跨链执行中） SUCCESS （跨链成功） FAILURE （跨链失败）
跨链兑换
支持的跨链桥
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/cross-chain/status?hash=0x0922d94d3bb459d05f16c64ba4b71ec1138940ed552a701837dba2536893e7fc'
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
"msg"
:
""
,
"data"
:
[
{
"bridgeHash"
:
"0x94ec8deac0dxxxb1c4ef09e0f29689xxxxfd9e66de822e2059bxxxx78c1ae1e8"
,
"fromChainId"
:
"109"
,
"toChainId"
:
"110"
,
"toAmount"
:
25300000000000
,
"errorMsg"
:
""
,
"toTxHash"
:
"0x94ec8deac0d114b1c4ef09e0f29689dc53fd9e66de822e2059b9ad078c1ae1e8"
,
"fromTxHash"
:
"0xa917f8c0ff8dd4b7bdf2eac4d54be40f7a7d4a06a517c6c590ea9a9bd99f40ba"
,
"refundTokenAddress"
:
""
,
"sourceChainGasfee"
:
"0.2"
"destinationChainGasfee"
:
"0.1"
"crossChainFee"
:
{
"symbol"
:
"usdt"
,
"address"
:
"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"
,
"amount"
:
"2.3"
,
}
"detailStatus"
:
"SUCCESS"
,
"status"
:
"SUCCESS"
}
]
}
跨链兑换
支持的跨链桥

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">跨链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-transaction-status" style="color:inherit">查询交易状态</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="查询交易状态">查询交易状态<a class="index_header-anchor__Xqb+L" href="#查询交易状态" style="opacity:0">#</a></h1><p>根据 txhash 查询跨链兑换最终交易状态。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/cross-chain/status</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>hash</td><td>String</td><td>是</td><td>源链 Hash 地址</td></tr><tr><td>chainIndex</td><td>String</td><td>否</td><td>源链 ID。 <br/> 如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>否</td><td>源链 ID。即将废弃。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>fromChainId</td><td>String</td><td>源链 ID</td></tr><tr><td>toChainId</td><td>String</td><td>目标链 ID</td></tr><tr><td>fromTxHash</td><td>String</td><td>源链交易 Hash</td></tr><tr><td>toTxHash</td><td>String</td><td>目标链交易 Hash</td></tr><tr><td>fromAmount</td><td>String</td><td>询价币种的兑换数量 (数量包含精度，如 1.00 USDT 则为 1000000)</td></tr><tr><td>fromTokenAddress</td><td>String</td><td>询价币种合约地址 (如0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE)</td></tr><tr><td>toAmount</td><td>String</td><td>目标币种的兑换数量 (数量包含精度，如 1.00 USDT 则为 1000000)</td></tr><tr><td>toTokenAddress</td><td>String</td><td>目标币种合约地址 (如0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)｜</td></tr><tr><td>errorMsg</td><td>String</td><td>错误信息</td></tr><tr><td>bridgeHash</td><td>String</td><td>目标链跨链桥交易 Hash</td></tr><tr><td>refundChainId</td><td>String</td><td>退款链 ID</td></tr><tr><td>refundTokenAddress</td><td>String</td><td>退款币种的合约地址</td></tr><tr><td>refundTxHash</td><td>String</td><td>退款交易 Hash</td></tr><tr><td>sourceChainGasfee</td><td>String</td><td>源链兑换实际消耗的gas fee</td></tr><tr><td>crossChainFee</td><td>Object</td><td>跨链桥实际收取的费用</td></tr><tr><td>symbol</td><td>String</td><td>跨链桥币种symbol</td></tr><tr><td>address</td><td>String</td><td>跨链桥币种地址</td></tr><tr><td>amount</td><td>String</td><td>跨链桥收取的数量</td></tr><tr><td>crossChainInfo</td><td>Object</td><td>跨链桥的信息</td></tr><tr><td>memo</td><td>String</td><td>/build-tx 中携带的自定义参数</td></tr><tr><td>destinationChainGasfee</td><td>String</td><td>目标链兑换实际消耗的gas fee</td></tr><tr><td>detailStatus</td><td>String</td><td>WAITING (订单处理中) FROM_SUCCESS (源链订单成功) FROM_FAILURE (源链订单失败) BRIDGE_PENDING (跨链桥订单执行中) BRIDGE_SUCCESS (跨链桥订单成功) SUCCESS (跨链兑换订单成功) REFUND (跨链失败，订单退款)</td></tr><tr><td>status</td><td>String</td><td>PENDING （跨链执行中） SUCCESS （跨链成功） FAILURE （跨链失败）</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-swap" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">跨链兑换</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-supported-bridges" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">支持的跨链桥</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/cross-chain/status?hash=0x0922d94d3bb459d05f16c64ba4b71ec1138940ed552a701837dba2536893e7fc'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"code"</span><span class="token operator">:</span><span class="token string">"0"</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span><span class="token string">""</span><span class="token punctuation">,</span>
  <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token property">"bridgeHash"</span><span class="token operator">:</span> <span class="token string">"0x94ec8deac0dxxxb1c4ef09e0f29689xxxxfd9e66de822e2059bxxxx78c1ae1e8"</span><span class="token punctuation">,</span>
        <span class="token property">"fromChainId"</span><span class="token operator">:</span> <span class="token string">"109"</span><span class="token punctuation">,</span>
        <span class="token property">"toChainId"</span><span class="token operator">:</span> <span class="token string">"110"</span><span class="token punctuation">,</span>
        <span class="token property">"toAmount"</span><span class="token operator">:</span> <span class="token number">25300000000000</span><span class="token punctuation">,</span>
        <span class="token property">"errorMsg"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"toTxHash"</span><span class="token operator">:</span> <span class="token string">"0x94ec8deac0d114b1c4ef09e0f29689dc53fd9e66de822e2059b9ad078c1ae1e8"</span><span class="token punctuation">,</span>
        <span class="token property">"fromTxHash"</span><span class="token operator">:</span> <span class="token string">"0xa917f8c0ff8dd4b7bdf2eac4d54be40f7a7d4a06a517c6c590ea9a9bd99f40ba"</span><span class="token punctuation">,</span>
        <span class="token property">"refundTokenAddress"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"sourceChainGasfee"</span><span class="token operator">:</span><span class="token string">"0.2"</span>
        <span class="token property">"destinationChainGasfee"</span><span class="token operator">:</span><span class="token string">"0.1"</span>
        <span class="token property">"crossChainFee"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
             <span class="token property">"symbol"</span><span class="token operator">:</span><span class="token string">"usdt"</span><span class="token punctuation">,</span>
             <span class="token property">"address"</span><span class="token operator">:</span><span class="token string">"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"</span><span class="token punctuation">,</span>
             <span class="token property">"amount"</span><span class="token operator">:</span><span class="token string">"2.3"</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
        <span class="token property">"detailStatus"</span><span class="token operator">:</span> <span class="token string">"SUCCESS"</span><span class="token punctuation">,</span>
        <span class="token property">"status"</span><span class="token operator">:</span> <span class="token string">"SUCCESS"</span>

    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-swap" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">跨链兑换</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-supported-bridges" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">支持的跨链桥</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "查询交易状态"
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
