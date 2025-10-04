# Websocket 介绍 | Websocket | 行情价格 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-websocket-introduction#websocket-简介  
**抓取时间:** 2025-05-27 06:24:36  
**字数:** 142

## 导航路径
DEX API > 行情 API > Websocket > Websocket 介绍

## 目录
- 连接
- 通知

---

Websocket 简介
#
WebSocket是HTML5一种新的协议（Protocol）。它实现了用户端与服务器全双工通信， 使得数据可以快速地双向传播。通过一次简单的握手就可以建立用户端和服务器连接， 服务器根据业务规则可以主动推送信息给用户端。其优点如下：
用户端和服务器进行数据传输时，请求头信息比较小，大概2个字节。
用户端和服务器皆可以主动地发送数据给对方。
不需要多次创建 TCP 请求和销毁，节约宽带和服务器的资源。
连接
#
连接限制
：3 次/秒 (基于IP)
当订阅私有频道时，使用私有服务的地址
请求限制
每个连接 对于 订阅/取消订阅/登录 请求的总次数限制为 480 次/小时
如果出现网络问题，系统会自动断开连接
如果连接成功后 30s 未订阅或订阅后 30s 内服务器未向用户推送数据，系统会自动断开连接
为了保持连接有效且稳定，建议您进行以下操作：
每次接收到消息后，用户设置一个定时器，定时N秒，N 小于 30。
如果定时器被触发（N 秒内没有收到新消息），发送字符串 'ping'。
期待一个文字字符串 'pong' 作为回应。如果在 N 秒内未收到，请发出错误或重新连接。
连接数限制
API KEY 维度，订阅每个 WebSocket 频道的最大连接数为 30 个。每个 WebSocket 连接都由唯一的 connId 标识。
受此限制的 WebSocket 频道如下：
价格频道
k 线频道
交易频道
若用户通过不同的请求参数在同一个 WebSocket 连接下订阅同一个频道，只算为一次连接。若用户使用相同或不同的 WebSocket 连接订阅上述频道，例如价格频道和交易频道。在该两个频道之间，计数不会累计，因为它们被视作不同的频道。简言之，系统计算每个频道对应的 WebSocket 连接数量。
新链接订阅频道时，平台将对该订阅返回channel-conn-count的消息同步链接数量。
链接数量更新
{
"event"
:
"channel-conn-count"
,
"channel"
:
"prices"
,
"connCount"
:
"2"
,
"connId"
:
"abcd1234"
}
当超出限制时，一般最新订阅的链接会收到拒绝。用户会先收到平时的订阅成功信息然后收到channel-conn-count-error消息，代表平台终止了这个链接的订阅。在异常场景下平台会终止已订阅的现有链接。
链接数量限制报错
{
"event"
:
"channel-conn-count-error"
,
"channel"
:
"prices"
,
"connCount"
:
"20"
,
"connId"
:
"a4d3ae55"
}
通知
#
WebSocket有一种消息类型(event=notice)。
用户会在如下场景收到此类信息：
Websocket服务升级断线
在推送服务升级前30秒会推送信息，告知用户WebSocket服务即将升级。用户可以重新建立新的连接避免由于断线造成的影响。
响应示例
{
"event"
:
"notice"
,
"code"
:
"64008"
,
"msg"
:
"The connection will soon be closed for a service upgrade. Please reconnect."
,
"connId"
:
"a4d3ae55"
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="websocket-简介">Websocket 简介<a class="index_header-anchor__Xqb+L" href="#websocket-简介" style="opacity:0">#</a></h1>
<p>WebSocket是HTML5一种新的协议（Protocol）。它实现了用户端与服务器全双工通信， 使得数据可以快速地双向传播。通过一次简单的握手就可以建立用户端和服务器连接， 服务器根据业务规则可以主动推送信息给用户端。其优点如下：</p>
<ul>
<li>用户端和服务器进行数据传输时，请求头信息比较小，大概2个字节。</li>
<li>用户端和服务器皆可以主动地发送数据给对方。</li>
<li>不需要多次创建 TCP 请求和销毁，节约宽带和服务器的资源。</li>
</ul>
<h2 data-content="连接" id="连接">连接<a class="index_header-anchor__Xqb+L" href="#连接" style="opacity:0">#</a></h2>
<p><strong>连接限制</strong>：3 次/秒 (基于IP)</p>
<p>当订阅私有频道时，使用私有服务的地址</p>
<p><strong>请求限制</strong></p>
<p>每个连接 对于 订阅/取消订阅/登录 请求的总次数限制为 480 次/小时
如果出现网络问题，系统会自动断开连接
如果连接成功后 30s 未订阅或订阅后 30s 内服务器未向用户推送数据，系统会自动断开连接</p>
<p>为了保持连接有效且稳定，建议您进行以下操作：</p>
<ol>
<li>每次接收到消息后，用户设置一个定时器，定时N秒，N 小于 30。</li>
<li>如果定时器被触发（N 秒内没有收到新消息），发送字符串 'ping'。</li>
<li>期待一个文字字符串 'pong' 作为回应。如果在 N 秒内未收到，请发出错误或重新连接。</li>
</ol>
<p><strong>连接数限制</strong></p>
<p>API KEY 维度，订阅每个 WebSocket 频道的最大连接数为 30 个。每个 WebSocket 连接都由唯一的 connId 标识。
受此限制的 WebSocket 频道如下：</p>
<ol>
<li>价格频道</li>
<li>k 线频道</li>
<li>交易频道</li>
</ol>
<p>若用户通过不同的请求参数在同一个 WebSocket 连接下订阅同一个频道，只算为一次连接。若用户使用相同或不同的 WebSocket 连接订阅上述频道，例如价格频道和交易频道。在该两个频道之间，计数不会累计，因为它们被视作不同的频道。简言之，系统计算每个频道对应的 WebSocket 连接数量。
新链接订阅频道时，平台将对该订阅返回channel-conn-count的消息同步链接数量。
链接数量更新</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"event"</span><span class="token operator">:</span><span class="token string">"channel-conn-count"</span><span class="token punctuation">,</span>
    <span class="token property">"channel"</span><span class="token operator">:</span><span class="token string">"prices"</span><span class="token punctuation">,</span>
    <span class="token property">"connCount"</span><span class="token operator">:</span> <span class="token string">"2"</span><span class="token punctuation">,</span>
    <span class="token property">"connId"</span><span class="token operator">:</span><span class="token string">"abcd1234"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<p>当超出限制时，一般最新订阅的链接会收到拒绝。用户会先收到平时的订阅成功信息然后收到channel-conn-count-error消息，代表平台终止了这个链接的订阅。在异常场景下平台会终止已订阅的现有链接。
链接数量限制报错</p>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"channel-conn-count-error"</span><span class="token punctuation">,</span>
    <span class="token property">"channel"</span><span class="token operator">:</span> <span class="token string">"prices"</span><span class="token punctuation">,</span>
    <span class="token property">"connCount"</span><span class="token operator">:</span> <span class="token string">"20"</span><span class="token punctuation">,</span>
    <span class="token property">"connId"</span><span class="token operator">:</span><span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="通知" id="通知">通知<a class="index_header-anchor__Xqb+L" href="#通知" style="opacity:0">#</a></h2>
<p>WebSocket有一种消息类型(event=notice)。
用户会在如下场景收到此类信息：</p>
<ul>
<li>Websocket服务升级断线
在推送服务升级前30秒会推送信息，告知用户WebSocket服务即将升级。用户可以重新建立新的连接避免由于断线造成的影响。
响应示例</li>
</ul>
<div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"event"</span><span class="token operator">:</span> <span class="token string">"notice"</span><span class="token punctuation">,</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"64008"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"The connection will soon be closed for a service upgrade. Please reconnect."</span><span class="token punctuation">,</span>
    <span class="token property">"connId"</span><span class="token operator">:</span> <span class="token string">"a4d3ae55"</span>
<span class="token punctuation">}</span>
</code></pre></div><!--/$--></div>
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
    "Websocket 介绍"
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
    "连接",
    "通知"
  ]
}
```

</details>
