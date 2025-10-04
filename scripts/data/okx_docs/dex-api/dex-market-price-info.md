# 批量获取价格 | API 参考 | 行情价格 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-market-price-info#响应参数  
**抓取时间:** 2025-05-27 07:24:20  
**字数:** 207

## 导航路径
DEX API > 行情 API > API 参考 > 批量获取价格

## 目录
- API 参考
- 获取支持的链
- 获取价格
- 批量获取价格
- 获取交易
- 获取K线
- 获取历史 K 线
- 错误码
- Websocket
- API 参考
- 错误码
- API 参考
- 错误码
- API 参考
- 错误码

---

DEX API
行情 API
行情价格 API
API 参考
批量获取价格
批量获取价格
#
批量获取代币最新价格。
请求地址
#
POST
https://web3.okx.com/api/v5/dex/market/price-info
请求参数
#
Parameter
Type
Required
Description
chainIndex
String
是
链的唯一标识。 (如
1
代表Ethereum。更多可查看
这里
。)
tokenContractAddress
String
是
币种合约地址 (如：0x382bb369d343125bfb2117af9c149795c6c65c50) 支持批量查询：最多可以输入 100 个地址，以
,
分隔
响应参数
#
Parameter
Type
Description
chainIndex
String
链的唯一标识符（例如：1 表示以太坊；参见更多说明）。
tokenContractAddress
String
代币合约地址（例如：0x382bb369d343125bfb2117af9c149795c6c65c50）
time
String
价格时间戳，使用 Unix 毫秒时间戳格式
price
String
最新代币价格
marketCap
String
代币市值
priceChange5M
String
5 分钟内的价格变动
priceChange1H
String
1 小时内的价格变动
priceChange4H
String
4 小时内的价格变动
priceChange24H
String
24 小时内的价格变动
volume5M
String
5 分钟内的交易量
volume1H
String
1 小时内的交易量
volume4H
String
4 小时内的交易量
volume24H
String
24 小时内的交易量
获取价格
获取交易
请求示例
#
shell
curl
--location
--request
POST
'https://web3.okx.com/api/v5/dex/market/price'
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
'[
{
"chainIndex": "66",
"tokenContractAddress":"0x382bb369d343125bfb2117af9c149795c6c65c50"
}
]'
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
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
,
"time"
:
"1716892020000"
,
"price"
:
"26.458143090226812"
,
"marketCap"
:
"27036475.39446733583542349"
,
"priceChange5M"
:
"-2.12"
,
"priceChange1H"
:
"1"
,
"priceChange4H"
:
"-4.69"
,
"priceChange24H"
:
"61.4"
,
"volume5M"
:
"95979.673920807940184"
,
"volume1H"
:
"1101091.054193115633995724"
,
"volume4H"
:
"3944418.057408155962911033"
,
"volume24H"
:
"16606779.022519656093301767"
}
]
}
获取价格
获取交易

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">行情价格 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-price-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-price-info" style="color:inherit">批量获取价格</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="批量获取价格">批量获取价格<a class="index_header-anchor__Xqb+L" href="#批量获取价格" style="opacity:0">#</a></h1><p>批量获取代币最新价格。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">POST</span> <code>https://web3.okx.com/api/v5/dex/market/price-info</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 (如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>是</td><td>币种合约地址 (如：0x382bb369d343125bfb2117af9c149795c6c65c50) 支持批量查询：最多可以输入 100 个地址，以 <code>,</code>分隔</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>链的唯一标识符（例如：1 表示以太坊；参见更多说明）。</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>代币合约地址（例如：0x382bb369d343125bfb2117af9c149795c6c65c50）</td></tr><tr><td>time</td><td>String</td><td>价格时间戳，使用 Unix 毫秒时间戳格式</td></tr><tr><td>price</td><td>String</td><td>最新代币价格</td></tr><tr><td>marketCap</td><td>String</td><td>代币市值</td></tr><tr><td>priceChange5M</td><td>String</td><td>5 分钟内的价格变动</td></tr><tr><td>priceChange1H</td><td>String</td><td>1 小时内的价格变动</td></tr><tr><td>priceChange4H</td><td>String</td><td>4 小时内的价格变动</td></tr><tr><td>priceChange24H</td><td>String</td><td>24 小时内的价格变动</td></tr><tr><td>volume5M</td><td>String</td><td>5 分钟内的交易量</td></tr><tr><td>volume1H</td><td>String</td><td>1 小时内的交易量</td></tr><tr><td>volume4H</td><td>String</td><td>4 小时内的交易量</td></tr><tr><td>volume24H</td><td>String</td><td>24 小时内的交易量</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-market-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取价格</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-market-trades" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> POST <span class="token string">'https://web3.okx.com/api/v5/dex/market/price'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> <span class="token punctuation">\</span>
--data-raw <span class="token string">'[</span>
<span class="token string">      {</span>
<span class="token string">          "chainIndex": "66",</span>
<span class="token string">          "tokenContractAddress":"0x382bb369d343125bfb2117af9c149795c6c65c50"</span>
<span class="token string">      }</span>
<span class="token string">  ]'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span><span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span><span class="token string">""</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span><span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span><span class="token punctuation">,</span>
    <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1716892020000"</span><span class="token punctuation">,</span>
    <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"26.458143090226812"</span><span class="token punctuation">,</span>
    <span class="token property">"marketCap"</span><span class="token operator">:</span> <span class="token string">"27036475.39446733583542349"</span><span class="token punctuation">,</span>
    <span class="token property">"priceChange5M"</span><span class="token operator">:</span> <span class="token string">"-2.12"</span><span class="token punctuation">,</span>
    <span class="token property">"priceChange1H"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
    <span class="token property">"priceChange4H"</span><span class="token operator">:</span> <span class="token string">"-4.69"</span><span class="token punctuation">,</span>
    <span class="token property">"priceChange24H"</span><span class="token operator">:</span> <span class="token string">"61.4"</span><span class="token punctuation">,</span>
    <span class="token property">"volume5M"</span><span class="token operator">:</span> <span class="token string">"95979.673920807940184"</span><span class="token punctuation">,</span>
    <span class="token property">"volume1H"</span><span class="token operator">:</span> <span class="token string">"1101091.054193115633995724"</span><span class="token punctuation">,</span>
    <span class="token property">"volume4H"</span><span class="token operator">:</span> <span class="token string">"3944418.057408155962911033"</span><span class="token punctuation">,</span>
    <span class="token property">"volume24H"</span><span class="token operator">:</span> <span class="token string">"16606779.022519656093301767"</span>
    <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-market-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取价格</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-market-trades" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "批量获取价格"
  ],
  "sidebar_links": [
    "API 参考",
    "获取支持的链",
    "获取价格",
    "批量获取价格",
    "获取交易",
    "获取K线",
    "获取历史 K 线",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码"
  ],
  "toc": [
    "API 参考",
    "获取支持的链",
    "获取价格",
    "批量获取价格",
    "获取交易",
    "获取K线",
    "获取历史 K 线",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码"
  ]
}
```

</details>
