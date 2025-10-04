# 获取历史综合币价 | API 参考 | 综合币价 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-historical-index-price#获取历史综合币价  
**抓取时间:** 2025-05-27 07:30:26  
**字数:** 203

## 导航路径
DEX API > 行情 API > API 参考 > 获取历史综合币价

## 目录
- API 参考
- 错误码
- Websocket
- API 参考
- 获取支持的链
- 获取综合币价
- 获取历史综合币价
- 错误码
- API 参考
- 错误码
- API 参考
- 错误码

---

DEX API
行情 API
综合币价 API
API 参考
获取历史综合币价
获取历史综合币价
#
查询某个代币的历史综合价格。
请求路径
#
GET
https://web3.okx.com/api/v5/dex/index/historical-price
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
tokenContractAddress
String
否
代币地址。
1
：传""代表查询对应链的主链币。
2
：传具体的代币合约地址，代表查询对应的代币。
limit
String
否
每次查询多少条，默认值为 50，最大 200。
cursor
String
否
游标位置，默认为第一个。
begin
String
否
开始时间，查询晚于该时间的历史币价。Unix时间戳，用毫秒表示。
end ract
String
否
结束时间，查询早于该时间的历史币价。若 begin 和 end 都不传，查询当前时间以前的历史币价。Unix 时间戳，用毫秒表示。
period
String
否
时间间隔单位:
1m
: 1分钟
5m
: 5分钟
30m
: 30分钟
1h
: 1小时
1d
: 1天（默认）。
响应参数
#
Parameter
Type
Description
prices
Array
历史价格的列表
>time
String
分钟时间戳（整分钟）
>price
String
币种价格，单位为美元，18 位精度
cursor
String
游标位置
获取综合币价
错误码
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/index/historical-price?chainIndex=1&limit=5&begin=1700040600000&period=5m'
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
"success"
,
"data"
:
[
{
"cursor"
:
"31"
,
"prices"
:
[
{
"time"
:
"1700040600000"
,
"price"
:
"1994.430000000000000000"
}
,
{
"time"
:
"1700040300000"
,
"price"
:
"1994.190000000000000000"
}
,
{
"time"
:
"1700040000000"
,
"price"
:
"1992.090000000000000000"
}
,
{
"time"
:
"1700039700000"
,
"price"
:
"1992.190000000000000000"
}
,
{
"time"
:
"1700039400000"
,
"price"
:
"1990.190000000000000000"
}
]
}
]
}
获取综合币价
错误码

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">综合币价 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-index-price-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-historical-index-price" style="color:inherit">获取历史综合币价</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取历史综合币价">获取历史综合币价<a class="index_header-anchor__Xqb+L" href="#获取历史综合币价" style="opacity:0">#</a></h1><p>查询某个代币的历史综合价格。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/index/historical-price</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>否</td><td>代币地址。<br/> <code>1</code>：传""代表查询对应链的主链币。<br/><code>2</code>：传具体的代币合约地址，代表查询对应的代币。</td></tr><tr><td>limit</td><td>String</td><td>否</td><td>每次查询多少条，默认值为 50，最大 200。</td></tr><tr><td>cursor</td><td>String</td><td>否</td><td>游标位置，默认为第一个。</td></tr><tr><td>begin</td><td>String</td><td>否</td><td>开始时间，查询晚于该时间的历史币价。Unix时间戳，用毫秒表示。</td></tr><tr><td>end      ract</td><td>String</td><td>否</td><td>结束时间，查询早于该时间的历史币价。若 begin 和 end 都不传，查询当前时间以前的历史币价。Unix 时间戳，用毫秒表示。</td></tr><tr><td>period</td><td>String</td><td>否</td><td>时间间隔单位: <br/> <code>1m</code>: 1分钟 <br/> <code>5m</code>: 5分钟 <br/> <code>30m</code>: 30分钟 <br/> <code>1h</code>: 1小时 <br/> <code>1d</code>: 1天（默认）。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>prices</td><td>Array</td><td>历史价格的列表</td></tr><tr><td>&gt;time</td><td>String</td><td>分钟时间戳（整分钟）</td></tr><tr><td>&gt;price</td><td>String</td><td>币种价格，单位为美元，18 位精度</td></tr><tr><td>cursor</td><td>String</td><td>游标位置</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-index-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取综合币价</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-index-price-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/index/historical-price?chainIndex=1&amp;limit=5&amp;begin=1700040600000&amp;period=5m'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> 
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
        <span class="token property">"cursor"</span><span class="token operator">:</span><span class="token string">"31"</span><span class="token punctuation">,</span>
        <span class="token property">"prices"</span><span class="token operator">:</span><span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1700040600000"</span><span class="token punctuation">,</span>
                <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"1994.430000000000000000"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1700040300000"</span><span class="token punctuation">,</span>
                <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"1994.190000000000000000"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1700040000000"</span><span class="token punctuation">,</span>
                <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"1992.090000000000000000"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1700039700000"</span><span class="token punctuation">,</span>
                <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"1992.190000000000000000"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1700039400000"</span><span class="token punctuation">,</span>
                <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"1990.190000000000000000"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span>
      <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-index-price" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取综合币价</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-index-price-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取历史综合币价"
  ],
  "sidebar_links": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "获取支持的链",
    "获取综合币价",
    "获取历史综合币价",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码"
  ],
  "toc": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "获取支持的链",
    "获取综合币价",
    "获取历史综合币价",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码"
  ]
}
```

</details>
