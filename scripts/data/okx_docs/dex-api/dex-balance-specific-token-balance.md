# 获取特定代币余额 | API 参考 | 余额 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-balance-specific-token-balance#请求路径  
**抓取时间:** 2025-05-27 07:11:03  
**字数:** 205

## 导航路径
DEX API > 行情 API > API 参考 > 获取特定代币余额

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
获取特定代币余额
获取特定代币余额
#
查询地址下指定代币的余额。
请求路径
#
POST
https://web3.okx.com/api/v5/dex/balance/token-balances-by-address
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
tokenContractAddresses
Array
是
代币合约地址列表，查询指定代币余额。上限是 20
>chainIndex
String
是
链唯一标识。(如
1
代表Ethereum。更多可查看
这里
。)
>tokenContractAddress
String
是
代币地址。
1
：传""代表查询对应链的主链币。
2
：传具体的代币合约地址，代表查询对应的代币。
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
代币余额列表
>chainIndex
String
链唯一标识
>tokenContractAddress
String
代币地址。为空 "" 代表返回结果是相关链，主链币的数据
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
代币的原始数量。对于不支持的链，该字段为空。更多的链即将被支持。
>tokenPrice
String
币种单价价值，以美元计价
>isRiskToken
Boolean
true
：命中风险空投代币和貔貅盘代币
false
：未命中风险空投代币和貔貅盘代币
获取资产明细
错误码
请求示例
#
shell
curl
--location
--request
POST
'https://web3.okx.com/api/v5/dex/balance/token-balances-by-address'
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
"address":"0x50c476a139aab23fdaf9bca12614cdd54a4244e3",
"tokenContractAddresses": [
{
"chainIndex": "1",
"tokenContractAddress": ""
}
]
}'
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
""
,
"symbol"
:
"eth"
,
"balance"
:
"0"
,
"tokenPrice"
:
"3640.43"
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
""
}
]
}
]
}
获取资产明细
错误码

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">余额 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-specific-token-balance" style="color:inherit">获取特定代币余额</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取特定代币余额">获取特定代币余额<a class="index_header-anchor__Xqb+L" href="#获取特定代币余额" style="opacity:0">#</a></h1><p>查询地址下指定代币的余额。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">POST</span> <code>https://web3.okx.com/api/v5/dex/balance/token-balances-by-address</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>address</td><td>String</td><td>是</td><td>地址</td></tr><tr><td>tokenContractAddresses</td><td>Array</td><td>是</td><td>代币合约地址列表，查询指定代币余额。上限是 20</td></tr><tr><td>&gt;chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>&gt;tokenContractAddress</td><td>String</td><td>是</td><td>代币地址。<br/> <code>1</code>：传""代表查询对应链的主链币。<br/><code>2</code>：传具体的代币合约地址，代表查询对应的代币。</td></tr><tr><td>excludeRiskToken</td><td>String</td><td>否</td><td>是否过滤风险空投代币和貔貅盘代币。默认过滤。<br/><code>0</code>: 过滤 <br/> <code>1</code>: 不过滤 <br/> 对于貔貅盘代币，目前只支持 <code>ETH</code>、<code>BSC</code>、<code>SOL</code>、<code>BASE</code> 四条链，更多的链即将被支持。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>tokenAssets</td><td>Array</td><td>代币余额列表</td></tr><tr><td>&gt;chainIndex</td><td>String</td><td>链唯一标识</td></tr><tr><td>&gt;tokenContractAddress</td><td>String</td><td>代币地址。为空 "" 代表返回结果是相关链，主链币的数据</td></tr><tr><td>&gt;address</td><td>String</td><td>地址</td></tr><tr><td>&gt;symbol</td><td>String</td><td>代币简称</td></tr><tr><td>&gt;balance</td><td>String</td><td>代币数量</td></tr><tr><td>&gt;rawBalance</td><td>String</td><td>代币的原始数量。对于不支持的链，该字段为空。更多的链即将被支持。</td></tr><tr><td>&gt;tokenPrice</td><td>String</td><td>币种单价价值，以美元计价</td></tr><tr><td>&gt;isRiskToken</td><td>Boolean</td><td><code>true</code>：命中风险空投代币和貔貅盘代币 <br/> <code>false</code>：未命中风险空投代币和貔貅盘代币</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-total-token-balances" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取资产明细</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-balance-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> POST <span class="token string">'https://web3.okx.com/api/v5/dex/balance/token-balances-by-address'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> <span class="token punctuation">\</span>
--data-raw <span class="token string">'{</span>
<span class="token string">    "address":"0x50c476a139aab23fdaf9bca12614cdd54a4244e3",</span>
<span class="token string">    "tokenContractAddresses": [</span>
<span class="token string">        {</span>
<span class="token string">            "chainIndex": "1",</span>
<span class="token string">            "tokenContractAddress": ""</span>
<span class="token string">        }</span>
<span class="token string">    ]</span>
<span class="token string">}'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"tokenAssets"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"eth"</span><span class="token punctuation">,</span>
                    <span class="token property">"balance"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenPrice"</span><span class="token operator">:</span> <span class="token string">"3640.43"</span><span class="token punctuation">,</span>
                    <span class="token property">"isRiskToken"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"rawBalance"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">""</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-balance-total-token-balances" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取资产明细</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-balance-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取特定代币余额"
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
