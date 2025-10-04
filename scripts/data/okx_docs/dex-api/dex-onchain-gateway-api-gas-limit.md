# 获取 Gas Limit | API 参考 | 交易上链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-limit#请求参数  
**抓取时间:** 2025-05-27 05:56:07  
**字数:** 163

## 导航路径
DEX API > 交易 API > API 参考 > 获取 Gas Limit

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
- 支持的跨链桥
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 获取支持的链
- 获取 Gas Price
- 获取 Gas Limit
- 广播交易
- 获取广播订单列表
- 错误码

---

DEX API
交易 API
交易上链 API
API 参考
获取 Gas Limit
获取 Gas Limit
#
通过交易信息的预执行，获取预估消耗的 Gaslimit 。
请求路径
#
POST
https://web3.okx.com/api/v5/dex/pre-transaction/gas-limit
请求参数
#
Parameter
Type
Required
Description
chainIndex
String
是
链唯一标识。(如
1
代表Ethereum。更多可查看
这里
。)
fromAddress
String
是
From 地址。
toAddress
String
是
To 地址。
txAmount
String
否
交易金额。默认值：
0
。
1.对于主链币交易（当fromToken为主链币时，例如 ETH ），txAmount可设置为主链币的数量，或通过
/swap
API获取（例如：
txAmount = swapResponse.tx.value
）。
2.对于代币交易，需将 txAmount 设为0。
金额必须使用主链币的基础单位（如ETH对应wei）。
extJson
Object
否
扩展参数，用于添加 calldata 等信息
extJson
Parameter
Type
Required
Description
inputData
String
否
calldata
响应参数
#
Parameter
Type
Description
gasLimit
String
预估gas limit数额
获取 Gas Price
广播交易
请求示例
#
shell
curl
--location
--request
POST
'https://web3.okx.com/api/v5/dex/pre-transaction/gas-limit'
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
--data-raw
'{
"fromAddr": "0x383c8208b4711256753b70729ba0cf0cda55efad",
"toAddr": "0x4ad041bbc6fa102394773c6d8f6d634320773af4",
"txAmount": "31600000000000000",
"chainIndex": "1",
"extJson": {
"inputData":"041bbc6fa102394773c6d8f6d634320773af4"
}
}'
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
"gasLimit"
:
"652683"
}
]
,
"msg"
:
""
}
获取 Gas Price
广播交易

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">交易上链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-limit" style="color:inherit">获取 Gas Limit</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取-gas-limit">获取 Gas Limit<a class="index_header-anchor__Xqb+L" href="#获取-gas-limit" style="opacity:0">#</a></h1><p>通过交易信息的预执行，获取预估消耗的 Gaslimit 。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">POST</span> <code>https://web3.okx.com/api/v5/dex/pre-transaction/gas-limit</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>fromAddress</td><td>String</td><td>是</td><td>From 地址。</td></tr><tr><td>toAddress</td><td>String</td><td>是</td><td>To 地址。</td></tr><tr><td>txAmount</td><td>String</td><td>否</td><td>交易金额。默认值：<code>0</code>。<br/>1.对于主链币交易（当fromToken为主链币时，例如 ETH ），txAmount可设置为主链币的数量，或通过 <a href="/zh-hans/build/dev-docs/dex-api/dex-swap">/swap</a> API获取（例如：<code>txAmount = swapResponse.tx.value</code>）。<br/>2.对于代币交易，需将 txAmount 设为0。<br/>金额必须使用主链币的基础单位（如ETH对应wei）。</td></tr><tr><td>extJson</td><td>Object</td><td>否</td><td>扩展参数，用于添加 calldata 等信息</td></tr></tbody></table></div><p>extJson</p><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>inputData</td><td>String</td><td>否</td><td>calldata</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>gasLimit</td><td>String</td><td>预估gas limit数额</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取 Gas Price</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-broadcast-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">广播交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> POST <span class="token string">'https://web3.okx.com/api/v5/dex/pre-transaction/gas-limit'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> <span class="token punctuation">\</span>
--data-raw <span class="token string">'{</span>
<span class="token string">    "fromAddr": "0x383c8208b4711256753b70729ba0cf0cda55efad",</span>
<span class="token string">    "toAddr": "0x4ad041bbc6fa102394773c6d8f6d634320773af4",</span>
<span class="token string">    "txAmount": "31600000000000000",</span>
<span class="token string">    "chainIndex": "1",</span>
<span class="token string">    "extJson": {</span>
<span class="token string">        "inputData":"041bbc6fa102394773c6d8f6d634320773af4"</span>
<span class="token string">    }</span>
<span class="token string">}'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
        <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
        <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
              <span class="token property">"gasLimit"</span><span class="token operator">:</span> <span class="token string">"652683"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取 Gas Price</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-broadcast-transaction" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">广播交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取 Gas Limit"
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
    "支持的跨链桥",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取 Gas Price",
    "获取 Gas Limit"
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
    "支持的跨链桥",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取 Gas Price",
    "获取 Gas Limit",
    "广播交易",
    "获取广播订单列表",
    "错误码"
  ]
}
```

</details>
