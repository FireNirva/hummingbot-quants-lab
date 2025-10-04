# 获取 Gas Price | API 参考 | 交易上链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-price#请求示例  
**抓取时间:** 2025-05-27 07:13:41  
**字数:** 234

## 导航路径
DEX API > 交易 API > API 参考 > 获取 Gas Price

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
获取 Gas Price
获取 Gas Price
#
动态获取各个链的预估 gas gasPrice。
请求路径
#
GET
https://web3.okx.com/api/v5/dex/pre-transaction/gas-price
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
响应参数
#
EVM & Tron
#
Parameter
Type
Description
normal
String
中档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN
min
String
低档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN
max
String
高档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN
supporteip1559
Boolean
是否支持 1559
eip1559Protocol
Object
1559 协议
eip1559 Protocol
#
Parameter
Type
Description
eip1559Protocol
Object
1559 协议结构
>baseFee
String
基础费用，单位为 wei
>proposePriorityFee
String
中档小费，单位为 wei
>safePriorityFee
String
低档小费，单位为 wei
>fastPriorityFee
String
高档小费，单位为 wei
Solana
#
Parameter
Type
Description
priorityFee
String
优先费。只适用于
Solana
>proposePriorityFee
String
中档优先费，单位是 microlamports。60 分位
>safePriorityFee
String
低档优先费，单位是 microlamports。80 分位
>fastPriorityFee
String
低档优先费，单位是 microlamports。95 分位
>extremePriorityFee
String
低档优先费，单位是 microlamports。99 分位
获取支持的链
获取 Gas Limit
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/pre-transaction/gas-price?chainIndex=1'
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
"data"
:
[
{
"normal"
:
"21289500000"
,
//中档gasPrice
"min"
:
"15670000000"
,
//低档gasPrice
"max"
:
"29149000000"
,
//高档gasPrice
"supportEip1559"
:
true
,
//是否支持1559
"erc1599Protocol"
:
{
"suggestBaseFee"
:
"15170000000"
,
//建议基础费用
"baseFee"
:
"15170000000"
,
//基础费用
"proposePriorityFee"
:
"810000000"
,
//中档小费
"safePriorityFee"
:
"500000000"
,
//低档小费
"fastPriorityFee"
:
"3360000000"
//高档小费
}
,
"priorityFee"
:
{
}
}
]
,
"msg"
:
""
}
获取支持的链
获取 Gas Limit

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">交易上链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-price" style="color:inherit">获取 Gas Price</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取-gas-price">获取 Gas Price<a class="index_header-anchor__Xqb+L" href="#获取-gas-price" style="opacity:0">#</a></h1><p>动态获取各个链的预估 gas gasPrice。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/pre-transaction/gas-price</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><h3 id="evm-&amp;-tron">EVM &amp; Tron<a class="index_header-anchor__Xqb+L" href="#evm-&amp;-tron" style="opacity:0">#</a></h3><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>normal</td><td>String</td><td>中档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN</td></tr><tr><td>min</td><td>String</td><td>低档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN</td></tr><tr><td>max</td><td>String</td><td>高档 gasPrice。对于EVM，单位为 wei。对于Tron，单位是 SUN</td></tr><tr><td>supporteip1559</td><td>Boolean</td><td>是否支持 1559</td></tr><tr><td>eip1559Protocol</td><td>Object</td><td>1559 协议</td></tr></tbody></table></div><h3 id="eip1559-protocol">eip1559 Protocol<a class="index_header-anchor__Xqb+L" href="#eip1559-protocol" style="opacity:0">#</a></h3><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>eip1559Protocol</td><td>Object</td><td>1559 协议结构</td></tr><tr><td>&gt;baseFee</td><td>String</td><td>基础费用，单位为 wei</td></tr><tr><td>&gt;proposePriorityFee</td><td>String</td><td>中档小费，单位为 wei</td></tr><tr><td>&gt;safePriorityFee</td><td>String</td><td>低档小费，单位为 wei</td></tr><tr><td>&gt;fastPriorityFee</td><td>String</td><td>高档小费，单位为 wei</td></tr></tbody></table></div><h3 id="solana">Solana<a class="index_header-anchor__Xqb+L" href="#solana" style="opacity:0">#</a></h3><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>priorityFee</td><td>String</td><td>优先费。只适用于 <code>Solana</code></td></tr><tr><td>&gt;proposePriorityFee</td><td>String</td><td>中档优先费，单位是 microlamports。60 分位</td></tr><tr><td>&gt;safePriorityFee</td><td>String</td><td>低档优先费，单位是 microlamports。80 分位</td></tr><tr><td>&gt;fastPriorityFee</td><td>String</td><td>低档优先费，单位是 microlamports。95 分位</td></tr><tr><td>&gt;extremePriorityFee</td><td>String</td><td>低档优先费，单位是 microlamports。99 分位</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-limit" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取 Gas Limit</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/pre-transaction/gas-price?chainIndex=1'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"normal"</span> <span class="token operator">:</span> <span class="token string">"21289500000"</span><span class="token punctuation">,</span> <span class="token comment">//中档gasPrice</span>
            <span class="token property">"min"</span> <span class="token operator">:</span> <span class="token string">"15670000000"</span><span class="token punctuation">,</span><span class="token comment">//低档gasPrice</span>
            <span class="token property">"max"</span> <span class="token operator">:</span> <span class="token string">"29149000000"</span><span class="token punctuation">,</span> <span class="token comment">//高档gasPrice            </span>
            <span class="token property">"supportEip1559"</span> <span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span><span class="token comment">//是否支持1559</span>
            <span class="token property">"erc1599Protocol"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                <span class="token property">"suggestBaseFee"</span> <span class="token operator">:</span> <span class="token string">"15170000000"</span><span class="token punctuation">,</span><span class="token comment">//建议基础费用</span>
                <span class="token property">"baseFee"</span> <span class="token operator">:</span> <span class="token string">"15170000000"</span><span class="token punctuation">,</span><span class="token comment">//基础费用</span>
                <span class="token property">"proposePriorityFee"</span> <span class="token operator">:</span> <span class="token string">"810000000"</span><span class="token punctuation">,</span><span class="token comment">//中档小费</span>
                <span class="token property">"safePriorityFee"</span> <span class="token operator">:</span> <span class="token string">"500000000"</span><span class="token punctuation">,</span><span class="token comment">//低档小费</span>
                <span class="token property">"fastPriorityFee"</span> <span class="token operator">:</span> <span class="token string">"3360000000"</span><span class="token comment">//高档小费</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token property">"priorityFee"</span><span class="token operator">:</span><span class="token punctuation">{</span><span class="token punctuation">}</span>
       <span class="token punctuation">}</span>     
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
<span class="token punctuation">}</span>

</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-onchain-gateway-api-gas-limit" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取 Gas Limit</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取 Gas Price"
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
