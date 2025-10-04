# 查询交易状态 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-swap-history#请求示例  
**抓取时间:** 2025-05-27 04:37:12  
**字数:** 289

## 导航路径
DEX API > 交易 API > API 参考 > 查询交易状态

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
查询交易状态
查询交易状态
#
根据 txhash 查询单链兑换最终交易状态。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/history
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
txHash
String
是
通过 OKX DEX API 发出的兑换交易 hash
isFromMyProject
Boolean
否
"传 true，判断是否来自当前请求的 API Key 下的订单。不传或传 false，查询任意来自 OKX DEX API 发出的订单"
响应参数
#
参数
类型
描述
chainId
String
链的唯一标识。 (如1: Ethereum，更多可查看
这里
)
txHash
String
交易 Hash
height
String
交易发生的区块高度
txTime
String
交易时间；Unix时间戳的毫秒数格式
status
String
pending
（执行中）
success
（成功）
fail
（失败）
txType
String
交易行为。Approve,Wrap,Unwrap,Swap
fromAddress
String
发送地址
dexrouter
String
交互地址
toAddress
String
接收地址
fromTokenDetails
Array
询价详情
>symbol
String
询价币种简称
>amount
String
询价币种的兑换数量，按最小数量返回，如 ETH 链，wei。
>tokenAddress
String
询价币种合约地址 (如0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE)
toTokenDetails
Array
兑换详情
>symbol
String
目标币种简称
>amount
String
目标币种的兑换数量，按最小数量返回。
>tokenAddress
String
目标币种合约地址 (如0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)
referalAmount
String
分佣金额
errorMsg
String
错误信息
gasLimit
String
gas限额
gasUsed
String
gas消耗。以最小数量返回，例如 ETH 链，wei。
gasPrice
String
gas价格。以最小数量返回，例如 ETH 链，wei。
txFee
String
手续费，返回主链币消耗数量。
兑换
设置分佣
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/history?chainIndex=784&txHash=5GePcvqEakoUtArW8PHULDSQds95vcgeiTznvbnb8hCV'
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
{
"chainId"
:
"784"
,
"dexRouter"
:
"0x51159f25f262ae01e87532b673de3b38df8f0ecc2dc0581f1033df6b84b84955"
,
"errorMsg"
:
""
,
"fromAddress"
:
"0x4b9df646075d8621e2578f14818427e4c708709744ea3b827136056f85f88da7"
,
"fromTokenDetails"
:
{
"amount"
:
"892919000000.000"
,
"symbol"
:
"HIPPO"
,
"tokenAddress"
:
"0x8993129d72e733985f7f1a00396cbd055bad6f817fee36576ce483c8bbb8b87b::sudeng::SUDENG"
}
,
"gasLimit"
:
""
,
"gasPrice"
:
""
,
"gasUsed"
:
""
,
"height"
:
"99502953"
,
"referralAmount"
:
"892919000"
,
"status"
:
"success"
,
"toAddress"
:
"0x4b9df646075d8621e2578f14818427e4c708709744ea3b827136056f85f88da7"
,
"toTokenDetails"
:
{
"amount"
:
"1532443840.00000000"
,
"symbol"
:
"SUI"
,
"tokenAddress"
:
"0x2::sui::SUI"
}
,
"txFee"
:
"7976416"
,
"txHash"
:
"5GePcvqEakoUtArW8PHULDSQds95vcgeiTznvbnb8hCV"
,
"txTime"
:
"1736390263909"
,
"txType"
:
"swap"
}
,
"msg"
:
""
}
兑换
设置分佣

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-swap-history" style="color:inherit">查询交易状态</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="查询交易状态">查询交易状态<a class="index_header-anchor__Xqb+L" href="#查询交易状态" style="opacity:0">#</a></h1><p>根据 txhash 查询单链兑换最终交易状态。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/history</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 <br/>如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>是</td><td>链的唯一标识。 即将废弃。</td></tr><tr><td>txHash</td><td>String</td><td>是</td><td>通过 OKX DEX API 发出的兑换交易 hash</td></tr><tr><td>isFromMyProject</td><td>Boolean</td><td>否</td><td>"传 true，判断是否来自当前请求的 API Key 下的订单。不传或传 false，查询任意来自 OKX DEX API 发出的订单"</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>chainId</td><td>String</td><td>链的唯一标识。 (如1: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>)</td></tr><tr><td>txHash</td><td>String</td><td>交易 Hash</td></tr><tr><td>height</td><td>String</td><td>交易发生的区块高度</td></tr><tr><td>txTime</td><td>String</td><td>交易时间；Unix时间戳的毫秒数格式</td></tr><tr><td>status</td><td>String</td><td><code>pending</code> （执行中）<code>success</code> （成功）<code>fail</code>（失败）</td></tr><tr><td>txType</td><td>String</td><td>交易行为。Approve,Wrap,Unwrap,Swap</td></tr><tr><td>fromAddress</td><td>String</td><td>发送地址</td></tr><tr><td>dexrouter</td><td>String</td><td>交互地址</td></tr><tr><td>toAddress</td><td>String</td><td>接收地址</td></tr><tr><td>fromTokenDetails</td><td>Array</td><td>询价详情</td></tr><tr><td>&gt;symbol</td><td>String</td><td>询价币种简称</td></tr><tr><td>&gt;amount</td><td>String</td><td>询价币种的兑换数量，按最小数量返回，如 ETH 链，wei。</td></tr><tr><td>&gt;tokenAddress</td><td>String</td><td>询价币种合约地址 (如0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE)</td></tr><tr><td>toTokenDetails</td><td>Array</td><td>兑换详情</td></tr><tr><td>&gt;symbol</td><td>String</td><td>目标币种简称</td></tr><tr><td>&gt;amount</td><td>String</td><td>目标币种的兑换数量，按最小数量返回。</td></tr><tr><td>&gt;tokenAddress</td><td>String</td><td>目标币种合约地址 (如0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48)</td></tr><tr><td>referalAmount</td><td>String</td><td>分佣金额</td></tr><tr><td>errorMsg</td><td>String</td><td>错误信息</td></tr><tr><td>gasLimit</td><td>String</td><td>gas限额</td></tr><tr><td>gasUsed</td><td>String</td><td>gas消耗。以最小数量返回，例如 ETH 链，wei。</td></tr><tr><td>gasPrice</td><td>String</td><td>gas价格。以最小数量返回，例如 ETH 链，wei。</td></tr><tr><td>txFee</td><td>String</td><td>手续费，返回主链币消耗数量。</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-swap" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">兑换</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-api-addfee" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">设置分佣</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/history?chainIndex=784&amp;txHash=5GePcvqEakoUtArW8PHULDSQds95vcgeiTznvbnb8hCV'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"784"</span><span class="token punctuation">,</span>
        <span class="token property">"dexRouter"</span><span class="token operator">:</span> <span class="token string">"0x51159f25f262ae01e87532b673de3b38df8f0ecc2dc0581f1033df6b84b84955"</span><span class="token punctuation">,</span>
        <span class="token property">"errorMsg"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"fromAddress"</span><span class="token operator">:</span> <span class="token string">"0x4b9df646075d8621e2578f14818427e4c708709744ea3b827136056f85f88da7"</span><span class="token punctuation">,</span>
        <span class="token property">"fromTokenDetails"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"892919000000.000"</span><span class="token punctuation">,</span>
            <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"HIPPO"</span><span class="token punctuation">,</span>
            <span class="token property">"tokenAddress"</span><span class="token operator">:</span> <span class="token string">"0x8993129d72e733985f7f1a00396cbd055bad6f817fee36576ce483c8bbb8b87b::sudeng::SUDENG"</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"gasLimit"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"gasPrice"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"gasUsed"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token property">"height"</span><span class="token operator">:</span> <span class="token string">"99502953"</span><span class="token punctuation">,</span>
        <span class="token property">"referralAmount"</span><span class="token operator">:</span> <span class="token string">"892919000"</span><span class="token punctuation">,</span>
        <span class="token property">"status"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
        <span class="token property">"toAddress"</span><span class="token operator">:</span> <span class="token string">"0x4b9df646075d8621e2578f14818427e4c708709744ea3b827136056f85f88da7"</span><span class="token punctuation">,</span>
        <span class="token property">"toTokenDetails"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"1532443840.00000000"</span><span class="token punctuation">,</span>
            <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"SUI"</span><span class="token punctuation">,</span>
            <span class="token property">"tokenAddress"</span><span class="token operator">:</span> <span class="token string">"0x2::sui::SUI"</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token property">"txFee"</span><span class="token operator">:</span> <span class="token string">"7976416"</span><span class="token punctuation">,</span>
        <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"5GePcvqEakoUtArW8PHULDSQds95vcgeiTznvbnb8hCV"</span><span class="token punctuation">,</span>
        <span class="token property">"txTime"</span><span class="token operator">:</span> <span class="token string">"1736390263909"</span><span class="token punctuation">,</span>
        <span class="token property">"txType"</span><span class="token operator">:</span> <span class="token string">"swap"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-swap" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">兑换</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-api-addfee" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">设置分佣</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
