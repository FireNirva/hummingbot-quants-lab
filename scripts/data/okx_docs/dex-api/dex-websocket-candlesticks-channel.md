# K线频道 | Websocket 参考  | Websocket | 行情价格 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-websocket-candlesticks-channel  
**抓取时间:** 2025-05-27 07:00:27  
**字数:** 295

## 导航路径
DEX API > 行情 API > Websocket > Websocket 参考 > K线频道

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
K线频道
K线频道
#
获取K线数据，推送频率最快是间隔1秒推送一次数据。
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
操作，
subscribe
unsubscribe
args
Array
是
请求订阅的频道列表
channel
String
是
频道名。
dex-token-candle1s
dex-token-candle1m
dex-token-candle3m
dex-token-candle5m
dex-token-candle15m
dex-token-candle30m
dex-token-candle1H
dex-token-candle2H
dex-token-candle4H
dex-token-candle6H
dex-token-candle12H
dex-token-candle1M
dex-token-candle3M
dex-token-candle1W
dex-token-candle1D
dex-token-candle2D
dex-token-candle3D
dex-token-candle5D
dex-token-candle6Hutc
dex-token-candle12Hutc
dex-token-candle1Dutc
dex-token-candle2Dutc
dex-token-candle3Dutc
dex-token-candle5Dutc
dex-token-candle1Wutc
dex-token-candle1Mutc
dex-token-candle3Mutc
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
链的唯一标识。
tokenContractAddress
String
币种合约地址
code
String
错误码
msg
String
错误消息
｜connId
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
> ts
String
开始时间，Unix时间戳的毫秒数格式，如 1597026383085
> o
String
开盘价格
> h
String
最高价格
> l
String
最低价格
> c
String
收盘价格
> vol
String
交易量，以目标币种为单位
> volUsd
String
交易量，以美元为单位
> confirm
String
K线状态。
0
：K线未完结
1
：K线已完结
价格频道
交易频道
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
"dex-token-candle1s"
,
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
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
"dex-token-candle1s"
,
"chainIndex"
:
"1"
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
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
"Invalid request: {\"op\": \"subscribe\", \"argss\":[{ \"channel\" : \"dex-token-candle1s\", \"chainIndex\" : \"1\", \"tokenContractAddress\" : \"0x382bb369d343125bfb2117af9c149795c6c65c50\"}]}"
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
"dex-token-candle1s"
,
"chainIndex"
:
"1"
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
}
,
"data"
:
[
[
"1597026383085"
,
"8533.02"
,
"8553.74"
,
"8527.17"
,
"8548.26"
,
"529.5858061"
,
"226348.0482"
,
"0"
]
]
}
价格频道
交易频道

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">行情价格 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket" style="color:inherit">Websocket</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-channels" style="color:inherit">Websocket 参考 </a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-candlesticks-channel" style="color:inherit">K线频道</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="k线频道">K线频道<a class="index_header-anchor__Xqb+L" href="#k线频道" style="opacity:0">#</a></h1><p>获取K线数据，推送频率最快是间隔1秒推送一次数据。 <br/></p><p><strong>URL路径</strong> <br/>
请联系我们 <a href="mailto:dexapi@okx.com">dexapi@okx.com</a>。</p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>op</td><td>String</td><td>是</td><td>操作，<code>subscribe</code> <code>unsubscribe</code></td></tr><tr><td>args</td><td>Array</td><td>是</td><td>请求订阅的频道列表</td></tr><tr><td>channel</td><td>String</td><td>是</td><td>频道名。 <code>dex-token-candle1s</code> <code>dex-token-candle1m</code> <code>dex-token-candle3m</code> <code>dex-token-candle5m</code> <code>dex-token-candle15m</code> <code>dex-token-candle30m</code> <code>dex-token-candle1H</code> <code>dex-token-candle2H</code> <code>dex-token-candle4H</code> <code>dex-token-candle6H</code> <code>dex-token-candle12H</code> <code>dex-token-candle1M</code> <code>dex-token-candle3M</code> <code>dex-token-candle1W</code> <code>dex-token-candle1D</code> <code>dex-token-candle2D</code> <code>dex-token-candle3D</code> <code>dex-token-candle5D</code> <code>dex-token-candle6Hutc</code> <code>dex-token-candle12Hutc</code> <code>dex-token-candle1Dutc</code> <code>dex-token-candle2Dutc</code> <code>dex-token-candle3Dutc</code> <code>dex-token-candle5Dutc</code> <code>dex-token-candle1Wutc</code> <code>dex-token-candle1Mutc</code> <code>dex-token-candle3Mutc</code></td></tr><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 (如1代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>是</td><td>币种合约地址</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>event</td><td>String</td><td>事件, <code>subscribe</code> <code>unsubscribe</code> <code>error</code></td></tr><tr><td>arg</td><td>Object</td><td>订阅的频道</td></tr><tr><td>channel</td><td>String</td><td>频道名</td></tr><tr><td>chainIndex</td><td>String</td><td>链的唯一标识。</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>币种合约地址</td></tr><tr><td>code</td><td>String</td><td>错误码</td></tr><tr><td>msg</td><td>String</td><td>错误消息</td></tr><tr><td>｜connId</td><td>String</td><td>WebSocket连接ID</td></tr></tbody></table></div><h2 data-content="推送数据参数" id="推送数据参数">推送数据参数<a class="index_header-anchor__Xqb+L" href="#推送数据参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>arg</td><td>Object</td><td>订阅成功的频道</td></tr><tr><td>&gt; channel</td><td>String</td><td>频道名</td></tr><tr><td>&gt; chainIndex</td><td>String</td><td>链的唯一标识。</td></tr><tr><td>&gt; tokenContractAddress</td><td>String</td><td>币种合约地址</td></tr><tr><td>data</td><td>Array</td><td>频道的数据</td></tr><tr><td>&gt; ts</td><td>String</td><td>开始时间，Unix时间戳的毫秒数格式，如 1597026383085</td></tr><tr><td>&gt; o</td><td>String</td><td>开盘价格</td></tr><tr><td>&gt; h</td><td>String</td><td>最高价格</td></tr><tr><td>&gt; l</td><td>String</td><td>最低价格</td></tr><tr><td>&gt; c</td><td>String</td><td>收盘价格</td></tr><tr><td>&gt; vol</td><td>String</td><td>交易量，以目标币种为单位</td></tr><tr><td>&gt; volUsd</td><td>String</td><td>交易量，以美元为单位</td></tr><tr><td>&gt; confirm</td><td>String</td><td>K线状态。<br/> <code>0</code>：K线未完结  <code>1</code>：K线已完结</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-price-channel" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">价格频道</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-trades-channel" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易频道</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"op"</span><span class="token operator">:</span> <span class="token string">"subscribe"</span><span class="token punctuation">,</span>
  <span class="token property">"args"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"dex-token-candle1s"</span><span class="token punctuation">,</span>
      <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
      <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><p>成功响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"subscribe"</span><span class="token punctuation">,</span>
  <span class="token property">"arg"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"dex-token-candle1s"</span><span class="token punctuation">,</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div><p>失败响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span>
  <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"60012"</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"Invalid request: {\"op\": \"subscribe\", \"argss\":[{ \"channel\" : \"dex-token-candle1s\", \"chainIndex\" : \"1\", \"tokenContractAddress\" : \"0x382bb369d343125bfb2117af9c149795c6c65c50\"}]}"</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div><p>推送数据示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"arg"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"dex-token-candle1s"</span><span class="token punctuation">,</span>
    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span>
    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span><span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">[</span>
      <span class="token string">"1597026383085"</span><span class="token punctuation">,</span>
      <span class="token string">"8533.02"</span><span class="token punctuation">,</span>
      <span class="token string">"8553.74"</span><span class="token punctuation">,</span>
      <span class="token string">"8527.17"</span><span class="token punctuation">,</span>
      <span class="token string">"8548.26"</span><span class="token punctuation">,</span>
      <span class="token string">"529.5858061"</span><span class="token punctuation">,</span>
      <span class="token string">"226348.0482"</span><span class="token punctuation">,</span>
      <span class="token string">"0"</span>
    <span class="token punctuation">]</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-price-channel" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">价格频道</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-trades-channel" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">交易频道</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "K线频道"
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
