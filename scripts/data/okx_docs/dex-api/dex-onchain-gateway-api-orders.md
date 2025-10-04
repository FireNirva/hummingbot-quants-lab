# 获取广播订单列表 | API 参考 | 交易上链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-orders#请求参数  
**抓取时间:** 2025-05-27 06:00:20  
**字数:** 211

## 导航路径
DEX API > 交易 API > API 参考 > 获取广播订单列表

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
获取广播订单列表
获取广播订单列表
#
查询从广播接口发出的订单列表，按时间倒序排列。
请求路径
#
GET
https://web3.okx.com/api/v5/dex/post-transaction/orders
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
chainIndex
String
是
链唯一标识。(如
1
代表Ethereum。更多可查看
这里
。)
txStatus
String
否
交易状态:
1
: 排队中
2
: 成功
3
:失败
orderId
String
否
交易订单唯一标识
cursor
String
否
游标
limit
String
否
返回条数，默认返回最近的 20 条，最多 100 条
响应参数
#
Parameter
Type
Description
cursor
String
游标
orders
Array
订单列表
>chainIndex
String
链唯一标识
>address
String
地址
>orderId
String
订单 Id
>txStatus
String
交易状态:
1
: 排队中
2
: 成功
3
:失败
>failReason
String
交易失败的原因
>txHash
String
交易哈希
广播交易
错误码
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/post-transaction/orders?address=0x238193be9e80e68eace3588b45d8cf4a7eae0fa3&chainIndex=1'
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
"1"
,
"orders"
:
[
{
"chainIndex"
:
"1"
,
"orderId"
:
"016cf21d020be6c2f071dad9bbd8ec5cb9342fa8"
,
"address"
:
"0x238193be9e80e68eace3588b45d8cf4a7eae0fa3"
,
"txHash"
:
"0xb240e65dd9156b4a450be72f6c9fe41be6f72397025bb465b21a96ee9871a589"
,
"failReason"
:
""
,
"txstatus"
:
"2"
}
,
{
"chainIndex"
:
"1"
,
"orderId"
:
"592051a92a744627022955be929ecb5c9e777705"
,
"address"
:
"0x238193be9e80e68eace3588b45d8cf4a7eae0fa3"
,
"txHash"
:
"0xc401ffcd2a2b4b1db42ce68dfde8e63c0a1e9653484efb2873dbf5d0cbeb227a"
,
"txstatus"
:
"1"
,
"failReason"
:
""
,
}
]
}
]
}
广播交易
错误码

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">交易上链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-orders" style="color:inherit">获取广播订单列表</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取广播订单列表">获取广播订单列表<a class="index_header-anchor__Xqb+L" href="#获取广播订单列表" style="opacity:0">#</a></h1><p>查询从广播接口发出的订单列表，按时间倒序排列。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/post-transaction/orders</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>address</td><td>String</td><td>是</td><td>地址</td></tr><tr><td>chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>txStatus</td><td>String</td><td>否</td><td>交易状态: <br/> <code>1</code>: 排队中 <br/> <code>2</code>: 成功 <br/> <code>3</code>:失败</td></tr><tr><td>orderId</td><td>String</td><td>否</td><td>交易订单唯一标识</td></tr><tr><td>cursor</td><td>String</td><td>否</td><td>游标</td></tr><tr><td>limit</td><td>String</td><td>否</td><td>返回条数，默认返回最近的 20 条，最多 100 条</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>cursor</td><td>String</td><td>游标</td></tr><tr><td>orders</td><td>Array</td><td>订单列表</td></tr><tr><td>&gt;chainIndex</td><td>String</td><td>链唯一标识</td></tr><tr><td>&gt;address</td><td>String</td><td>地址</td></tr><tr><td>&gt;orderId</td><td>String</td><td>订单 Id</td></tr><tr><td>&gt;txStatus</td><td>String</td><td>交易状态: <br/> <code>1</code>: 排队中 <br/> <code>2</code>: 成功 <br/> <code>3</code>:失败</td></tr><tr><td>&gt;failReason</td><td>String</td><td>交易失败的原因</td></tr><tr><td>&gt;txHash</td><td>String</td><td>交易哈希</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-broadcast-transaction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">广播交易</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/post-transaction/orders?address=0x238193be9e80e68eace3588b45d8cf4a7eae0fa3&amp;chainIndex=1'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>

            <span class="token property">"cursor"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
            <span class="token property">"orders"</span><span class="token operator">:</span><span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"orderId"</span><span class="token operator">:</span> <span class="token string">"016cf21d020be6c2f071dad9bbd8ec5cb9342fa8"</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0x238193be9e80e68eace3588b45d8cf4a7eae0fa3"</span><span class="token punctuation">,</span>
                    <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"0xb240e65dd9156b4a450be72f6c9fe41be6f72397025bb465b21a96ee9871a589"</span><span class="token punctuation">,</span>
                    <span class="token property">"failReason"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"txstatus"</span><span class="token operator">:</span> <span class="token string">"2"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"orderId"</span><span class="token operator">:</span> <span class="token string">"592051a92a744627022955be929ecb5c9e777705"</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0x238193be9e80e68eace3588b45d8cf4a7eae0fa3"</span><span class="token punctuation">,</span>
                    <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"0xc401ffcd2a2b4b1db42ce68dfde8e63c0a1e9653484efb2873dbf5d0cbeb227a"</span><span class="token punctuation">,</span>
                    <span class="token property">"txstatus"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"failReason"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span> 
<span class="token punctuation">}</span>

</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-broadcast-transaction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">广播交易</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取广播订单列表"
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
