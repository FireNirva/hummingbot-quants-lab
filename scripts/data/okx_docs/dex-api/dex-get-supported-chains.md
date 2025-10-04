# 获取支持的链 | API 参考 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-get-supported-chains#请求地址  
**抓取时间:** 2025-05-27 04:27:46  
**字数:** 580

## 导航路径
DEX API > 交易 API > API 参考 > 获取支持的链

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
获取支持的链
获取支持的链
#
获取支持跨链兑换的链信息，通过请求返回支持跨入的目标链。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/cross-chain/supported/chain
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
dex 授权合约地址
API 参考
获取币种列表
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/cross-chain/supported/chain'
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
"137"
,
"chainId"
:
"137"
,
"chainName"
:
"Polygon"
,
"dexTokenApproveAddress"
:
"0x3B86917369B83a6892f553609F3c2F439C184e31"
}
,
{
"chainIndex"
:
"195"
,
"chainId"
:
"195"
,
"chainName"
:
"TRON"
,
"dexTokenApproveAddress"
:
"THRAE2VhGNAcvPKtT96AqyXtSQwhiU1XL8"
}
,
{
"chainIndex"
:
"43114"
,
"chainId"
:
"43114"
,
"chainName"
:
"Avalanche C"
,
"dexTokenApproveAddress"
:
"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"
}
,
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
{
"chainIndex"
:
"66"
,
"chainId"
:
"66"
,
"chainName"
:
"OKTC"
,
"dexTokenApproveAddress"
:
"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"
}
,
{
"chainIndex"
:
"56"
,
"chainId"
:
"56"
,
"chainName"
:
"BNB Chain"
,
"dexTokenApproveAddress"
:
"0x2c34A2Fb1d0b4f55de51E1d0bDEfaDDce6b7cDD6"
}
,
{
"chainIndex"
:
"250"
,
"chainId"
:
"250"
,
"chainName"
:
"Fantom"
,
"dexTokenApproveAddress"
:
"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"
}
,
{
"chainIndex"
:
"42161"
,
"chainId"
:
"42161"
,
"chainName"
:
"Arbitrum"
,
"dexTokenApproveAddress"
:
"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"
}
,
{
"chainIndex"
:
"10"
,
"chainId"
:
"10"
,
"chainName"
:
"Optimism"
,
"dexTokenApproveAddress"
:
"0x68D6B739D2020067D1e2F713b999dA97E4d54812"
}
,
{
"chainIndex"
:
"25"
,
"chainId"
:
"25"
,
"chainName"
:
"Cronos"
,
"dexTokenApproveAddress"
:
"0x70cbb871e8f30fc8ce23609e9e0ea87b6b222f58"
}
,
{
"chainIndex"
:
"501"
,
"chainId"
:
"501"
,
"chainName"
:
"Solana"
,
"dexTokenApproveAddress"
:
""
}
,
{
"chainIndex"
:
"324"
,
"chainId"
:
"324"
,
"chainName"
:
"zkSync Era"
,
"dexTokenApproveAddress"
:
"0xc67879F4065d3B9fe1C09EE990B891Aa8E3a4c2f"
}
,
{
"chainIndex"
:
"1030"
,
"chainId"
:
"1030"
,
"chainName"
:
"Conflux eSpace"
,
"dexTokenApproveAddress"
:
"0x68D6B739D2020067D1e2F713b999dA97E4d54812"
}
,
{
"chainIndex"
:
"784"
,
"chainId"
:
"784"
,
"chainName"
:
"SUI"
,
"dexTokenApproveAddress"
:
""
}
,
{
"chainIndex"
:
"1101"
,
"chainId"
:
"1101"
,
"chainName"
:
"Polygon zkEvm"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"59144"
,
"chainId"
:
"59144"
,
"chainName"
:
"Linea"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"5000"
,
"chainId"
:
"5000"
,
"chainName"
:
"Mantle"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"8453"
,
"chainId"
:
"8453"
,
"chainName"
:
"Base"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"534352"
,
"chainId"
:
"534352"
,
"chainName"
:
"Scroll"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"196"
,
"chainId"
:
"196"
,
"chainName"
:
"X Layer"
,
"dexTokenApproveAddress"
:
"0x8b773D83bc66Be128c60e07E17C8901f7a64F000"
}
,
{
"chainIndex"
:
"169"
,
"chainId"
:
"169"
,
"chainName"
:
"Manta Pacific"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"1088"
,
"chainId"
:
"1088"
,
"chainName"
:
"Metis"
,
"dexTokenApproveAddress"
:
"0x57df6092665eb6058DE53939612413ff4B09114E"
}
,
{
"chainIndex"
:
"7000"
,
"chainId"
:
"7000"
,
"chainName"
:
"Zeta"
,
"dexTokenApproveAddress"
:
"0x03B5ACdA01207824cc7Bc21783Ee5aa2B8d1D2fE"
}
,
{
"chainIndex"
:
"4200"
,
"chainId"
:
"4200"
,
"chainName"
:
"Merlin"
,
"dexTokenApproveAddress"
:
"0x8b773D83bc66Be128c60e07E17C8901f7a64F000"
}
,
{
"chainIndex"
:
"81457"
,
"chainId"
:
"81457"
,
"chainName"
:
"Blast"
,
"dexTokenApproveAddress"
:
"0x5fD2Dc91FF1dE7FF4AEB1CACeF8E9911bAAECa68"
}
,
{
"chainIndex"
:
"607"
,
"chainId"
:
"607"
,
"chainName"
:
"TON"
,
"dexTokenApproveAddress"
:
""
}
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
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">跨链 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-get-supported-chains" style="color:inherit">获取支持的链</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取支持的链">获取支持的链<a class="index_header-anchor__Xqb+L" href="#获取支持的链" style="opacity:0">#</a></h1><p>获取支持跨链兑换的链信息，通过请求返回支持跨入的目标链。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/cross-chain/supported/chain</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>否</td><td>链的唯一标识。 <br/>如<code>1</code>: Ethereum，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>否</td><td>链的唯一标识。 即将废弃。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>链的唯一标识。</td></tr><tr><td>chainId</td><td>String</td><td>链的唯一标识。 即将废弃。</td></tr><tr><td>chainName</td><td>String</td><td>链名称 (如<code>Optimism</code>)</td></tr><tr><td>dexTokenApproveAddress</td><td>String</td><td>dex 授权合约地址</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje"> API 参考</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-get-tokens" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取币种列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/cross-chain/supported/chain'</span> <span class="token punctuation">\</span>

<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"137"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"137"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Polygon"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x3B86917369B83a6892f553609F3c2F439C184e31"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"195"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"195"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"TRON"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"THRAE2VhGNAcvPKtT96AqyXtSQwhiU1XL8"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"43114"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"43114"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Avalanche C"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Ethereum"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"66"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"66"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"OKTC"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"56"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"56"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"BNB Chain"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x2c34A2Fb1d0b4f55de51E1d0bDEfaDDce6b7cDD6"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"250"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"250"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Fantom"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"42161"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"42161"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Arbitrum"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"10"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"10"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Optimism"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x68D6B739D2020067D1e2F713b999dA97E4d54812"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"25"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"25"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Cronos"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x70cbb871e8f30fc8ce23609e9e0ea87b6b222f58"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Solana"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">""</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"324"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"324"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"zkSync Era"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0xc67879F4065d3B9fe1C09EE990B891Aa8E3a4c2f"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1030"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"1030"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Conflux eSpace"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x68D6B739D2020067D1e2F713b999dA97E4d54812"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"784"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"784"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"SUI"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">""</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1101"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"1101"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Polygon zkEvm"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"59144"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"59144"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Linea"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"5000"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"5000"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Mantle"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"8453"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"8453"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Base"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"534352"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"534352"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Scroll"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"196"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"196"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"X Layer"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x8b773D83bc66Be128c60e07E17C8901f7a64F000"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"169"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"169"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Manta Pacific"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1088"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"1088"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Metis"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x57df6092665eb6058DE53939612413ff4B09114E"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"7000"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"7000"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Zeta"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x03B5ACdA01207824cc7Bc21783Ee5aa2B8d1D2fE"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"4200"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"4200"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Merlin"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x8b773D83bc66Be128c60e07E17C8901f7a64F000"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"81457"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"81457"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"Blast"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">"0x5fD2Dc91FF1dE7FF4AEB1CACeF8E9911bAAECa68"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"607"</span><span class="token punctuation">,</span>
    <span class="token property">"chainId"</span><span class="token operator">:</span> <span class="token string">"607"</span><span class="token punctuation">,</span>
    <span class="token property">"chainName"</span><span class="token operator">:</span> <span class="token string">"TON"</span><span class="token punctuation">,</span>
    <span class="token property">"dexTokenApproveAddress"</span><span class="token operator">:</span> <span class="token string">""</span>
  <span class="token punctuation">}</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
  <span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-api" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje"> API 参考</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-crosschain-get-tokens" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取币种列表</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
