# 交易频道 | Websocket 参考  | Websocket | 行情价格 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-websocket-trades-channel#响应参数  
**抓取时间:** 2025-05-27 06:42:49  
**字数:** 366

## 导航路径
DEX API > 行情 API > Websocket > Websocket 参考 > 交易频道

## 目录
- API 参考
- 错误码
- Websocket
- Websocket 简介
- Websocket 频道
- 价格频道
- K线频道
- 交易频道
- 错误码
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
Websocket
Websocket 参考
交易频道
交易频道
#
获取最近的成交数据，有成交数据就推送
URL路径
请联系我们
dexapi@okx.com
。
请求参数
#
Parameter
Type
Required
Description
op
String
是
操作,
subscribe
unsubscribe
args
Array
是
请求订阅的频道列表
channel
String
是
频道名,
trades
chainIndex
String
是
链的唯一标识。 (如1代表Ethereum。更多可查看
这里
。)
tokenContractAddress
String
是
币种合约地址
响应参数
#
Parameter
Type
Description
event
String
事件,
subscribe
unsubscribe
error
arg
Object
订阅的频道
channel
String
频道名
chainIndex
String
链的唯一标识
tokenContractAddress
String
币种合约地址
code
String
错误码
msg
String
错误消息
connId
String
WebSocket连接ID
推送数据参数
#
Parameter
Type
Description
arg
Object
订阅成功的频道
> channel
String
频道名
> chainIndex
String
链的唯一标识。
> tokenContractAddress
String
币种合约地址
data
Array
频道的数据
> id
String
成交id
> txHashUrl
String
链上交易的tx哈希
> userAddress
String
交易的发起方
> dexName
String
交易发生的DEX
> poolLogoUrl
String
池子logo链接
> type
String
交易类型。
buy
: 买
sell
: 卖
> amountExchanged
String
交易信息
>> amount
String
成交数量
>> tokenSymbol
String
代币符号
>> tokenContractAddress
String
币种合约地址
> price
String
最新交易价格
> volume
String
交易的美元价值
> time
String
交易的时间，Unix 时间戳格式，用毫秒表示
> isFiltered
String
此交易在k线和币价计算中是否过滤。
0
: 不过滤
1
: 过滤
K线频道
错误码
请求示例
#
shell
{
"op"
:
"subscribe"
,
"args"
:
[
{
"channel"
:
"trades"
,
"chainIndex"
:
"501"
,
"tokenContractAddress"
:
"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
}
]
}
响应示例
#
200
成功响应示例
{
"event"
:
"subscribe"
,
"arg"
:
{
"channel"
:
"trades"
,
"chainIndex"
:
"501"
,
"tokenContractAddress"
:
"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
}
,
"connId"
:
"a4d3ae55"
}
失败响应示例
{
"event"
:
"error"
,
"code"
:
"60012"
,
"msg"
:
"Invalid request: {\"op\": \"subscribe\", \"argss\":[{ \"channel\" : \"trades\", \"chainIndex\" : \"501\", \"tokenContractAddress\" : \"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC\"}]}"
,
"connId"
:
"a4d3ae55"
}
推送数据示例
{
"arg"
:
{
"channel"
:
"trades"
,
"chainIndex"
:
"501"
"tokenContractAddress"
:
"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
}
,
"data"
:
[
{
"id"
:
"1739439633000!@#120!@#14731892839"
,
"chainIndex"
:
"501"
,
"tokenContractAddress"
:
"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
,
"txHashUrl"
:
"https://solscan.io/tx/zgDzoiVG4XuDgQcoEg9vhpRyfyk5thNUQuTeTCeF289Qec5iraeCrUzPLyiE2UCviox2ebbTcsagGvzYF7M5uqs"
,
"userAddress"
:
"2kCm1RHGJjeCKL4SA3ZJCLyXqUD7nEJ7GMtVaP7c6jQ8"
,
"dexName"
:
"Orca Whirlpools"
,
"poolLogoUrl"
:
"https://static.okx.com/cdn/wallet/logo/dex_orcaswap.png"
,
"type"
:
"sell"
,
"changedTokenInfo"
:
[
{
"amount"
:
"100.396595878"
,
"tokenSymbol"
:
"ai16z"
,
"tokenContractAddress"
:
"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"
}
,
{
"amount"
:
"2.482831"
,
"tokenSymbol"
:
"SOL"
,
"tokenContractAddress"
:
"So11111111111111111111111111111111111111112"
}
]
"price"
:
"26.458143090226812"
,
"volume"
:
"519.788163"
,
"time"
:
"1739439633000"
,
"isFiltered"
:
"0"
}
]
}
K线频道
错误码

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">行情价格 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket" style="color:inherit">Websocket</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-channels" style="color:inherit">Websocket 参考 </a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-trades-channel" style="color:inherit">交易频道</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="交易频道">交易频道<a class="index_header-anchor__Xqb+L" href="#交易频道" style="opacity:0">#</a></h1><p>获取最近的成交数据，有成交数据就推送 <br/></p><p><strong>URL路径</strong> <br/>
请联系我们 <a href="mailto:dexapi@okx.com">dexapi@okx.com</a>。</p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>op</td><td>String</td><td>是</td><td>操作, <code>subscribe</code> <code>unsubscribe</code></td></tr><tr><td>args</td><td>Array</td><td>是</td><td>请求订阅的频道列表</td></tr><tr><td>channel</td><td>String</td><td>是</td><td>频道名, <code>trades</code></td></tr><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 (如1代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>是</td><td>币种合约地址</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>event</td><td>String</td><td>事件, <code>subscribe</code> <code>unsubscribe</code> <code>error</code></td></tr><tr><td>arg</td><td>Object</td><td>订阅的频道</td></tr><tr><td>channel</td><td>String</td><td>频道名</td></tr><tr><td>chainIndex</td><td>String</td><td>链的唯一标识</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址</td></tr><tr><td>code</td><td>String</td><td>错误码</td></tr><tr><td>msg</td><td>String</td><td>错误消息</td></tr><tr><td>connId</td><td>String</td><td>WebSocket连接ID</td></tr></tbody></table></div><h2 data-content="推送数据参数" id="推送数据参数">推送数据参数<a class="index_header-anchor__Xqb+L" href="#推送数据参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>arg</td><td>Object</td><td>订阅成功的频道</td></tr><tr><td>&gt; channel</td><td>String</td><td>频道名</td></tr><tr><td>&gt; chainIndex</td><td>String</td><td>链的唯一标识。</td></tr><tr><td>&gt; tokenContractAddress</td><td>String</td><td>币种合约地址</td></tr><tr><td>data</td><td>Array</td><td>频道的数据</td></tr><tr><td>&gt; id</td><td>String</td><td>成交id</td></tr><tr><td>&gt; txHashUrl</td><td>String</td><td>链上交易的tx哈希</td></tr><tr><td>&gt; userAddress</td><td>String</td><td>交易的发起方</td></tr><tr><td>&gt; dexName</td><td>String</td><td>交易发生的DEX</td></tr><tr><td>&gt; poolLogoUrl</td><td>String</td><td>池子logo链接</td></tr><tr><td>&gt; type</td><td>String</td><td>交易类型。<code>buy</code>: 买 <code>sell</code>: 卖</td></tr><tr><td>&gt; amountExchanged</td><td>String</td><td>交易信息</td></tr><tr><td>&gt;&gt; amount</td><td>String</td><td>成交数量</td></tr><tr><td>&gt;&gt; tokenSymbol</td><td>String</td><td>代币符号</td></tr><tr><td>&gt;&gt; tokenContractAddress</td><td>String</td><td>币种合约地址</td></tr><tr><td>&gt; price</td><td>String</td><td>最新交易价格</td></tr><tr><td>&gt; volume</td><td>String</td><td>交易的美元价值</td></tr><tr><td>&gt; time</td><td>String</td><td>交易的时间，Unix 时间戳格式，用毫秒表示</td></tr><tr><td>&gt; isFiltered</td><td>String</td><td>此交易在k线和币价计算中是否过滤。 <br/><code>0</code>: 不过滤 <code>1</code>: 过滤</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-candlesticks-channel" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">K线频道</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"op"</span><span class="token operator">:</span> <span class="token string">"subscribe"</span><span class="token punctuation">,</span>
  <span class="token property">"args"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"trades"</span><span class="token punctuation">,</span>
      <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><p>成功响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"subscribe"</span><span class="token punctuation">,</span>
  <span class="token property">"arg"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"trades"</span><span class="token punctuation">,</span>
      <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>

</code></pre></div><p>失败响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span>
  <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"60012"</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"Invalid request: {\"op\": \"subscribe\", \"argss\":[{ \"channel\" : \"trades\", \"chainIndex\" : \"501\", \"tokenContractAddress\" : \"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC\"}]}"</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>

</code></pre></div><p>推送数据示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"arg"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"trades"</span><span class="token punctuation">,</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"501"</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span><span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
    <span class="token property">"id"</span><span class="token operator">:</span><span class="token string">"1739439633000!@#120!@#14731892839"</span><span class="token punctuation">,</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"501"</span><span class="token punctuation">,</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"</span><span class="token punctuation">,</span>
    <span class="token property">"txHashUrl"</span><span class="token operator">:</span> <span class="token string">"https://solscan.io/tx/zgDzoiVG4XuDgQcoEg9vhpRyfyk5thNUQuTeTCeF289Qec5iraeCrUzPLyiE2UCviox2ebbTcsagGvzYF7M5uqs"</span><span class="token punctuation">,</span>
    <span class="token property">"userAddress"</span><span class="token operator">:</span> <span class="token string">"2kCm1RHGJjeCKL4SA3ZJCLyXqUD7nEJ7GMtVaP7c6jQ8"</span><span class="token punctuation">,</span>
    <span class="token property">"dexName"</span><span class="token operator">:</span> <span class="token string">"Orca Whirlpools"</span><span class="token punctuation">,</span>
    <span class="token property">"poolLogoUrl"</span><span class="token operator">:</span> <span class="token string">"https://static.okx.com/cdn/wallet/logo/dex_orcaswap.png"</span><span class="token punctuation">,</span>
    <span class="token property">"type"</span><span class="token operator">:</span> <span class="token string">"sell"</span><span class="token punctuation">,</span>
    <span class="token property">"changedTokenInfo"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
    <span class="token property">"amount"</span><span class="token operator">:</span><span class="token string">"100.396595878"</span><span class="token punctuation">,</span> 
    <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"ai16z"</span><span class="token punctuation">,</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"HeLp6NuQkmYB4pYWo2zYs22mESHXPQYzXbB8n4V98jwC"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
    <span class="token property">"amount"</span><span class="token operator">:</span><span class="token string">"2.482831"</span><span class="token punctuation">,</span> 
    <span class="token property">"tokenSymbol"</span><span class="token operator">:</span><span class="token string">"SOL"</span><span class="token punctuation">,</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"So11111111111111111111111111111111111111112"</span>
    <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
    <span class="token property">"price"</span><span class="token operator">:</span> <span class="token string">"26.458143090226812"</span><span class="token punctuation">,</span>
    <span class="token property">"volume"</span><span class="token operator">:</span> <span class="token string">"519.788163"</span><span class="token punctuation">,</span>
    <span class="token property">"time"</span><span class="token operator">:</span> <span class="token string">"1739439633000"</span><span class="token punctuation">,</span>
    <span class="token property">"isFiltered"</span><span class="token operator">:</span> <span class="token string">"0"</span>
    <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-candlesticks-channel" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">K线频道</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "行情 API",
    "Websocket",
    "Websocket 参考",
    "交易频道"
  ],
  "sidebar_links": [
    "API 参考",
    "错误码",
    "Websocket",
    "Websocket 简介",
    "Websocket 频道",
    "价格频道",
    "K线频道",
    "交易频道",
    "错误码",
    "API 参考",
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
    "Websocket 简介",
    "Websocket 频道",
    "价格频道",
    "K线频道",
    "交易频道",
    "错误码",
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
