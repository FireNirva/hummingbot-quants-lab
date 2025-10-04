# 登录 | DEX API | DEX API 文档

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-websocket-login#响应示例  
**抓取时间:** 2025-05-27 07:17:37  
**字数:** 203

## 导航路径
DEX API > 行情 API > Websocket > Websocket 介绍 > 登录

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
登录
登录
#
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
login
args
Array
是
账户列表
> apiKey
String
是
API key
> passphrase
String
是
API key 的密码
> timestamp
String
是
时间戳，Unix Epoch时间，单位是秒
> sign
String
是
签名字符串
响应参数
#
Parameter
Type
Description
event
String
操作，
login
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
apiKey
: 调用 API 的唯一标识。可通过
开发者管理平台
申请
passphrase
:你注册 API Key 时设置的密码，请务必牢记。
timestamp
:Unix Epoch 时间戳，单位为秒，如 1704876947 sign:签名字符串，签名算法如下：
先将timestamp 、 method 、requestPath 进行字符串拼接，再使用HMAC SHA256方法将拼接后的字符串和SecretKey加密，然后进行Base64编码
SecretKey
: 用户申请APIKey时所生成的安全密钥，如：22582BD0CFF14C41EDBF1AB98506286D
其中 timestamp 示例:const timestamp = '' + Date.now() / 1,000
其中 sign 示例: sign=CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(timestamp +'GET'+ '/users/self/verify', secret))
method
总是 'GET'
requestPath
总是 '/users/self/verify'
Tips
请求在时间戳之后30秒会失效，如果您的服务器时间和 API 服务器时间有偏差，推荐使用 REST API查询API服务器的时间，然后设置时间戳
Websocket 简介
订阅
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
全部成功响应示例
{
"event"
:
"login"
,
"code"
:
"0"
,
"msg"
:
""
,
"connId"
:
"a4d3ae55"
}
全部失败响应示例
{
"event"
:
"error"
,
"code"
:
"60009"
,
"msg"
:
"Login failed."
,
"connId"
:
"a4d3ae55"
}
Websocket 简介
订阅

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">行情价格 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket" style="color:inherit">Websocket</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-introduction" style="color:inherit">Websocket 介绍</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-login" style="color:inherit">登录</a></div></div></div></div></div></div>
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="登录">登录<a class="index_header-anchor__Xqb+L" href="#登录" style="opacity: 0;">#</a></h1><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity: 0;">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>op</td><td>String</td><td>是</td><td>操作， <code>login</code></td></tr><tr><td>args</td><td>Array</td><td>是</td><td>账户列表</td></tr><tr><td>&gt; apiKey</td><td>String</td><td>是</td><td>API key</td></tr><tr><td>&gt; passphrase</td><td>String</td><td>是</td><td>API key 的密码</td></tr><tr><td>&gt; timestamp</td><td>String</td><td>是</td><td>时间戳，Unix Epoch时间，单位是秒</td></tr><tr><td>&gt; sign</td><td>String</td><td>是</td><td>签名字符串</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity: 0;">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>event</td><td>String</td><td>操作，<code>login</code> 或者 <code>error</code></td></tr><tr><td>code</td><td>String</td><td>错误码</td></tr><tr><td>msg</td><td>String</td><td>错误消息</td></tr><tr><td>connId</td><td>String</td><td>WebSocket连接ID</td></tr></tbody></table></div><p><p><strong>apiKey</strong>: 调用 API 的唯一标识。可通过<a href="/zh-hans/build/dev-portal">开发者管理平台</a>申请 <br/></p><p><strong>passphrase</strong>:你注册 API Key 时设置的密码，请务必牢记。 <br/></p><p><strong>timestamp</strong>:Unix Epoch 时间戳，单位为秒，如 1704876947 sign:签名字符串，签名算法如下：
先将timestamp 、 method 、requestPath 进行字符串拼接，再使用HMAC SHA256方法将拼接后的字符串和SecretKey加密，然后进行Base64编码 <br/></p><p><strong>SecretKey</strong>: 用户申请APIKey时所生成的安全密钥，如：22582BD0CFF14C41EDBF1AB98506286D
其中 timestamp 示例:const timestamp = '' + Date.now() / 1,000
其中 sign 示例: sign=CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(timestamp +'GET'+ '/users/self/verify', secret))</p><p><strong>method</strong> 总是 'GET' <br/></p><p><strong>requestPath</strong> 总是 '/users/self/verify'</p></p><div class="index_wrapper__x5A2Q"><div aria-labelledby=":r0:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":r0:">Tips</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>请求在时间戳之后30秒会失效，如果您的服务器时间和 API 服务器时间有偏差，推荐使用 REST API查询API服务器的时间，然后设置时间戳</p></div></div></div></div></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":r1:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-introduction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right: 8px;"></i><div><span class="truncate-2 index_f-16__mSYje">Websocket 简介</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-subscribe" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right: 8px;">订阅</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity: 0;">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size: 28px;" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
	<span class="token property">"op"</span><span class="token operator">:</span> <span class="token string">"login"</span><span class="token punctuation">,</span>
	<span class="token property">"args"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
		<span class="token property">"apiKey"</span><span class="token operator">:</span> <span class="token string">"985d5b66-57ce-40fb-b714-afc0b9787083"</span><span class="token punctuation">,</span>
		<span class="token property">"passphrase"</span><span class="token operator">:</span> <span class="token string">"123456"</span><span class="token punctuation">,</span>
		<span class="token property">"timestamp"</span><span class="token operator">:</span> <span class="token string">"1538054050"</span><span class="token punctuation">,</span>
		<span class="token property">"sign"</span><span class="token operator">:</span> <span class="token string">"7L+zFQ+CEgGu5rzCj4+BdV2/uUHGqddA9pI6ztsRRPs="</span>
	<span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity: 0;">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color: rgb(49, 189, 101);"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size: 28px;" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><p>全部成功响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"login"</span><span class="token punctuation">,</span>
  <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div><p>全部失败响应示例</p><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
  <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"error"</span><span class="token punctuation">,</span>
  <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"60009"</span><span class="token punctuation">,</span>
  <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"Login failed."</span><span class="token punctuation">,</span>
  <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":r2:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-introduction" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right: 8px;"></i><div><span class="truncate-2 index_f-16__mSYje">Websocket 简介</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-websocket-subscribe" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right: 8px;">订阅</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div></div>
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
    "登录"
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
