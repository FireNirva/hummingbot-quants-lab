# 取消订阅 | Websocket 介绍 | Websocket | 行情价格 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-websocket-unsubscribe#请求参数  
**抓取时间:** 2025-05-27 07:19:49  
**字数:** 144

## 导航路径
DEX API > 行情 API > Websocket > Websocket 介绍 > 取消订阅

## 目录
- API 参考
- 错误码
- Websocket
- Websocket 简介
- 登录
- 订阅
- 取消订阅
- Websocket 频道
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
Websocket 介绍
取消订阅
取消订阅
#
取消一个或者多个频道。
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
unsubscribe
args
Array
是
取消订阅的频道列表
> channel
String
是
频道名
> chainIndex
String
是
链的唯一标识。 (如1代表Ethereum。更多可查看
这里
。)
> tokenContractAddress
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
操作，
unsubscribe
或者
error
code
String
错误码
msg
String
错误消息
connId
String
WebSocket连接ID
请求格式说明
{
"op"
:
"unsubscribe"
,
"args"
:
[
"< SubscriptionTopic> "
]
}
订阅
Websocket 频道
请求示例
#
shell
{
"op"
:
"login"
,
"args"
:
[
{
"apiKey"
:
"985d5b66-57ce-40fb-b714-afc0b9787083"
,
"passphrase"
:
"123456"
,
"timestamp"
:
"1538054050"
,
"sign"
:
"7L+zFQ+CEgGu5rzCj4+BdV2/uUHGqddA9pI6ztsRRPs="
}
]
}
响应示例
#
200
{
"event"
:
"unsubscribe"
,
"arg"
:
{
"channel"
:
"price"
,
"chainIndex"
:
"1"
,
"tokenContractAddress"
:
"0x382bb369d343125bfb2117af9c149795c6c65c50"
}
,
"connId"
:
"d0b44253"
}
订阅
Websocket 频道

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">行情价格 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket" style="color:inherit">Websocket</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-introduction" style="color:inherit">Websocket 介绍</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-unsubscribe" style="color:inherit">取消订阅</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="取消订阅">取消订阅<a class="index_header-anchor__Xqb+L" href="#取消订阅" style="opacity:0">#</a></h1><p>取消一个或者多个频道。</p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>op</td><td>String</td><td>是</td><td>操作， <code>unsubscribe</code></td></tr><tr><td>args</td><td>Array</td><td>是</td><td>取消订阅的频道列表</td></tr><tr><td>&gt; channel</td><td>String</td><td>是</td><td>频道名</td></tr><tr><td>&gt; chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 (如1代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>&gt; tokenContractAddress</td><td>String</td><td>是</td><td>币种合约地址</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>event</td><td>String</td><td>操作，<code>unsubscribe</code> 或者 <code>error</code></td></tr><tr><td>code</td><td>String</td><td>错误码</td></tr><tr><td>msg</td><td>String</td><td>错误消息</td></tr><tr><td>connId</td><td>String</td><td>WebSocket连接ID</td></tr></tbody></table></div><p>请求格式说明</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span><span class="token property">"op"</span><span class="token operator">:</span> <span class="token string">"unsubscribe"</span><span class="token punctuation">,</span><span class="token property">"args"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">"&lt; SubscriptionTopic&gt; "</span><span class="token punctuation">]</span><span class="token punctuation">}</span>
</code></pre></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-subscribe" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">订阅</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-channels" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">Websocket 频道</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
	<span class="token property">"op"</span><span class="token operator">:</span> <span class="token string">"login"</span><span class="token punctuation">,</span>
	<span class="token property">"args"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
		<span class="token property">"apiKey"</span><span class="token operator">:</span> <span class="token string">"985d5b66-57ce-40fb-b714-afc0b9787083"</span><span class="token punctuation">,</span>
		<span class="token property">"passphrase"</span><span class="token operator">:</span> <span class="token string">"123456"</span><span class="token punctuation">,</span>
		<span class="token property">"timestamp"</span><span class="token operator">:</span> <span class="token string">"1538054050"</span><span class="token punctuation">,</span>
		<span class="token property">"sign"</span><span class="token operator">:</span> <span class="token string">"7L+zFQ+CEgGu5rzCj4+BdV2/uUHGqddA9pI6ztsRRPs="</span>
	<span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"unsubscribe"</span><span class="token punctuation">,</span>
    <span class="token property">"arg"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"price"</span><span class="token punctuation">,</span>
        <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
        <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0x382bb369d343125bfb2117af9c149795c6c65c50"</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"d0b44253"</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-subscribe" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">订阅</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-channels" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">Websocket 频道</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "Websocket 介绍",
    "取消订阅"
  ],
  "sidebar_links": [
    "API 参考",
    "错误码",
    "Websocket",
    "Websocket 简介",
    "登录",
    "订阅",
    "取消订阅",
    "Websocket 频道",
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
    "登录",
    "订阅",
    "取消订阅",
    "Websocket 频道",
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
