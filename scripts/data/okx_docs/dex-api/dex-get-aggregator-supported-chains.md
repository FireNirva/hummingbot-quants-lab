# 获取支持的链 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-aggregator-supported-chains#请求参数  
**抓取时间:** 2025-05-27 06:37:27  
**字数:** 124

## 导航路径
DEX API > 交易 API > API 参考 > 获取支持的链

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
获取支持的链
获取支持的链
#
获取支持单链兑换的链信息，通过请求返回支持跨入的目标链。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/supported/chain
请求参数
#
参数
类型
必传
描述
chainIndex
String
否
链的唯一标识。
如
1
: Ethereum，更多可查看
这里
。
chainId
String
否
链的唯一标识。 即将废弃。
响应参数
#
参数
类型
描述
chainIndex
String
链的唯一标识。
chainId
String
链的唯一标识。 即将废弃。
chainName
String
链名称 (如
Optimism
)
dexTokenApproveAddress
String
dex 授权合约地址，如果未产生授权，返回为空。
API 参考
获取币种列表
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/supported/chain?chainIndex=1'
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
"chainIndex"
:
"1"
,
"chainId"
:
"1"
,
"chainName"
:
"Ethereum"
,
"dexTokenApproveAddress"
:
"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"
}
,
]
,
"msg"
:
""
}
API 参考
获取币种列表

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-aggregator-supported-chains" style="color:inherit">获取支持的链</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取支持的链">获取支持的链<a class="index_header-anchor__Xqb+L" href="#获取支持的链" style="opacity:0">#</a></h1><p>获取支持单链兑换的链信息，通过请求返回支持跨入的目标链。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/supported/chain</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>否</td><td>链的唯一标识。 <br/>如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>否</td><td>链的唯一标识。 即将废弃。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>链的唯一标识。</td></tr><tr><td>chainId</td><td>String</td><td>链的唯一标识。 即将废弃。</td></tr><tr><td>chainName</td><td>String</td><td>链名称 (如<code>Optimism</code>)</td></tr><tr><td>dexTokenApproveAddress</td><td>String</td><td>dex 授权合约地址，如果未产生授权，返回为空。</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">API 参考</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-tokens" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取币种列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/supported/chain?chainIndex=1'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span><span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span><span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
            <span class="token property">"chainIndex"</span><span class="token operator">:</span><span class="token string">"1"</span><span class="token punctuation">,</span>
            <span class="token property">"chainId"</span><span class="token operator">:</span><span class="token string">"1"</span><span class="token punctuation">,</span>
            <span class="token property">"chainName"</span><span class="token operator">:</span><span class="token string">"Ethereum"</span><span class="token punctuation">,</span>
            <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span><span class="token string">""</span>
  <span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">API 参考</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-tokens" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取币种列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取支持的链"
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
