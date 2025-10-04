# 获取币种列表 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-tokens#获取币种列表  
**抓取时间:** 2025-05-27 06:05:22  
**字数:** 277

## 导航路径
DEX API > 交易 API > API 参考 > 获取币种列表

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
获取币种列表
获取币种列表
#
获取币种列表。此接口的返回结果是欧易 DEX 认为的主流代币和平台代币。你可以指定该列表之外的代币在欧易 DEX 询价和兑换。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/all-tokens
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
链 ID。即将废弃。
响应参数
#
参数
类型
描述
decimals
String
币种精度 (如:
18
)
tokenContractAddress
String
币种合约地址 (如:
0x382bb369d343125bfb2117af9c149795c6c65c50
)
tokenLogoUrl
String
币种标识 (如:
https://static.okx.com/cdn/wallet/logo/USDT-991ffed9-e495-4d1b-80c2-a4c5f96ce22d.png
)
tokenName
String
币种全称 (如:
Tether
)
tokenSymbol
String
币种简称 (如:
USDT
)
获取支持的链
获取流动性列表
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/all-tokens?chainIndex=1'
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
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/USDT-991ffed9-e495-4d1b-80c2-a4c5f96ce22d.png"
,
"tokenName"
:
"Tether"
,
"tokenSymbol"
:
"USDT"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0xc946daf81b08146b1c7a8da2a851ddf2b3eaaf85"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/explorer/okexchain/exchain_usdc.png"
,
"tokenName"
:
"USD Coin"
,
"tokenSymbol"
:
"USDC"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0xdf54b6c6195ea4d948d03bfd818d365cf175cfc2"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/okb.png"
,
"tokenName"
:
"OKB"
,
"tokenSymbol"
:
"OKB"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/okt.png"
,
"tokenName"
:
"OKTC"
,
"tokenSymbol"
:
"OKT"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0x218c3c3d49d0e7b37aff0d8bb079de36ae61a4c0"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/BNB-20220308.png"
,
"tokenName"
:
"Binance Coin"
,
"tokenSymbol"
:
"BNB"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0x332730a4f6e03d9c55829435f10360e13cfa41ff"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/BUSD-20220308.png"
,
"tokenName"
:
"Binance USD"
,
"tokenSymbol"
:
"BUSD"
}
,
{
"decimals"
:
"18"
,
"tokenContractAddress"
:
"0xdcac52e001f5bd413aa6ea83956438f29098166b"
,
"tokenLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/eth_usdk.png"
,
"tokenName"
:
"USDK"
,
"tokenSymbol"
:
"USDK"
}
]
,
"msg"
:
""
}
获取支持的链
获取流动性列表

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-tokens" style="color:inherit">获取币种列表</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取币种列表">获取币种列表<a class="index_header-anchor__Xqb+L" href="#获取币种列表" style="opacity:0">#</a></h1><p>获取币种列表。此接口的返回结果是欧易 DEX 认为的主流代币和平台代币。你可以指定该列表之外的代币在欧易 DEX 询价和兑换。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/all-tokens</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 <br/>如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>是</td><td>链 ID。即将废弃。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>decimals</td><td>String</td><td>币种精度 (如: <code>18</code>)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址 (如: <code>0x382bb369d343125bfb2117af9c149795c6c65c50</code>)</td></tr><tr><td>tokenLogoUrl</td><td>String</td><td>币种标识 (如: <code>https://static.okx.com/cdn/wallet/logo/USDT-991ffed9-e495-4d1b-80c2-a4c5f96ce22d.png</code>)</td></tr><tr><td>tokenName</td><td>String</td><td>币种全称 (如: <code>Tether</code>)</td></tr><tr><td>tokenSymbol</td><td>String</td><td>币种简称 (如: <code>USDT</code>)</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-aggregator-supported-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-liquidity" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取流动性列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/all-tokens?chainIndex=1'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
  <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/USDT-991ffed9-e495-4d1b-80c2-a4c5f96ce22d.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"Tether"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"USDT"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xc946daf81b08146b1c7a8da2a851ddf2b3eaaf85"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/explorer/okexchain/exchain_usdc.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"USD Coin"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"USDC"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xdf54b6c6195ea4d948d03bfd818d365cf175cfc2"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/okb.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"OKB"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"OKB"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/okt.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"OKTC"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"OKT"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x218c3c3d49d0e7b37aff0d8bb079de36ae61a4c0"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/BNB-20220308.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"Binance Coin"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"BNB"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x332730a4f6e03d9c55829435f10360e13cfa41ff"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/BUSD-20220308.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"Binance USD"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"BUSD"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      <span class="token property">"decimals"</span><span class="token operator">:</span> <span class="token string">"18"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xdcac52e001f5bd413aa6ea83956438f29098166b"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/eth_usdk.png"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenName"</span><span class="token operator">:</span> <span class="token string">"USDK"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenSymbol"</span><span class="token operator">:</span> <span class="token string">"USDK"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-aggregator-supported-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-get-liquidity" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取流动性列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取币种列表"
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
