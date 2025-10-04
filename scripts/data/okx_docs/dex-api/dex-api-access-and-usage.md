# API 访问和用法 | 概览 | 首页 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-api-access-and-usage#设置标题  
**抓取时间:** 2025-05-27 01:30:03  
**字数:** 1034

## 导航路径
DEX API > 首页 > API 访问和用法

## 目录
- 鉴权
- Postman 示例
- Javascript 示例
- 遗留 API

---

API 访问和用法
#
在开始使用 DEX API 之前，你需要先在开发者管理平台创建项目并生成 API key。详细的步骤和相关资源请参考
这里
。
鉴权
#
所有对 API 发起访问的请求都需要包括下面信息来进行身份认证。
OK-ACCESS-KEY ： API key
OK-ACCESS-TIMESTAMP ：发起请求的时间 (UTC) 。ISO 格式，如：2020-12-08T09:08:57.715Z
OK-ACCESS-PASSPHRASE ：创建 API key 时指定的 passphrase
OK-ACCESS-SIGN ：签名
签名步骤：
第一步：将 timestamp 、 method 、requestPath 、 body 拼接成一个字符串
第二步：以 HMAC SHA256 算法 和 secret key (在创建 API key 时生成) 对预哈希字符串 (第一步产生的结果) 进行签名
第三步：以 Base64 算法对签名进行编码
解释
例如，sign=CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(timestamp + 'GET' + '/api/v5/dex/aggregator/swap', SecretKey))
其中，timestamp 与 OK-ACCESS-TIMESTAMP 必须相同
其中，GET 是 method （HTTP请求方法，字母全部大写）
其中，/api/v5/dex/aggregator/swap 是requestPath （请求接口路径）
其中 body 为空。如果请求没有请求体（通常为 GET 请求），那 body 可省略
注意
时间戳与服务端时差不得超过 30 秒
POST 请求需包含原始请求体参与签名计算
Secret key 仅创建时可见，请通过安全渠道存储
Postman 示例
#
Postman 是一款流行的 API 开发和测试工具，允许开发人员设计、测试和记录 API。它提供了对用户友好的图形界面，用于向 API 发送 HTTP 请求。
如果你还没有安装 Postman，你可以免费从 Postman 网站下载它：
https://www.postman.com/
提示
这个示例需要你具备对 Postman 的基础理解。
添加参数
#
这通常适用于 GET 请求。
如果你的请求需要查询参数，你可以在
Params
选项卡下添加它们。在这里，你可以添加查询参数的 key-value pair。
设置标题
#
在
Headers
选项卡下，添加以下键-值对：
OK-ACCESS-KEY
OK-ACCESS-PASSPHRASE
添加正文
#
这通常适用于 POST 请求。
如果你的请求需要一个请求主体，你可以在
Body
选项卡下添加它们。
在下拉菜单中选择
raw
和
JSON
。
使用 JSON 格式输入你的请求主体。
设置预请求脚本
#
用于生成所需的签名 (
OK-ACCESS-SIGN
) 和时间戳 (
OK-ACCESS-TIMESTAMP
)。
在
Pre-request Script
选项卡下，插入与请求类型相对应的脚本。
在生成预哈希字符串时，GET 请求会排除请求主体。
根据需要编辑密钥。
GET 请求：
var
method
=
pm
.
request
.
method
;
var
now
=
new
Date
(
)
;
var
isoString
=
now
.
toISOString
(
)
;
var
path
=
pm
.
request
.
url
.
getPathWithQuery
(
)
;
var
sign
=
CryptoJS
.
enc
.
Base64
.
stringify
(
CryptoJS
.
HmacSHA256
(
isoString
+
method
+
path
,
pm
.
variables
.
replaceIn
(
'{{secret_key}}'
)
)
)
;
pm
.
request
.
headers
.
add
(
{
key
:
'OK-ACCESS-SIGN'
,
value
:
sign
}
)
;
pm
.
request
.
headers
.
add
(
{
key
:
'OK-ACCESS-TIMESTAMP'
,
value
:
isoString
}
)
;
POST 请求:
var
method
=
pm
.
request
.
method
;
var
now
=
new
Date
(
)
;
var
isoString
=
now
.
toISOString
(
)
;
var
path
=
pm
.
request
.
url
.
getPathWithQuery
(
)
;
var
bodyStr
=
pm
.
request
.
body
.
raw
;
var
sign
=
CryptoJS
.
enc
.
Base64
.
stringify
(
CryptoJS
.
HmacSHA256
(
isoString
+
method
+
path
+
bodyStr
,
pm
.
variables
.
replaceIn
(
'{{secret_key}}'
)
)
)
pm
.
request
.
headers
.
add
(
{
key
:
'OK-ACCESS-SIGN'
,
value
:
sign
}
)
;
pm
.
request
.
headers
.
add
(
{
key
:
'OK-ACCESS-TIMESTAMP'
,
value
:
isoString
}
)
;
Javascript 示例
#
若要通过 Javascript 脚本调用 API，请参考以下代码示例：
const
https
=
require
(
'https'
)
;
const
crypto
=
require
(
'crypto'
)
;
const
querystring
=
require
(
'querystring'
)
;
// 定义 API 凭证
const
api_config
=
{
"api_key"
:
''
,
"secret_key"
:
''
,
"passphrase"
:
''
,
}
;
function
preHash
(
timestamp
,
method
,
request_path
,
params
)
{
// 根据字符串和参数创建预签名
let
query_string
=
''
;
if
(
method
===
'GET'
&&
params
)
{
query_string
=
'?'
+
querystring
.
stringify
(
params
)
;
}
if
(
method
===
'POST'
&&
params
)
{
query_string
=
JSON
.
stringify
(
params
)
;
}
return
timestamp
+
method
+
request_path
+
query_string
;
}
function
sign
(
message
,
secret_key
)
{
// 使用 HMAC-SHA256 对预签名字符串进行签名
const
hmac
=
crypto
.
createHmac
(
'sha256'
,
secret_key
)
;
hmac
.
update
(
message
)
;
return
hmac
.
digest
(
'base64'
)
;
}
function
createSignature
(
method
,
request_path
,
params
)
{
// 获取 ISO 8601 格式时间戳
const
timestamp
=
new
Date
(
)
.
toISOString
(
)
.
slice
(
0
,
-
5
)
+
'Z'
;
// 生成签名
const
message
=
preHash
(
timestamp
,
method
,
request_path
,
params
)
;
const
signature
=
sign
(
message
,
api_config
[
'secret_key'
]
)
;
return
{
signature
,
timestamp
}
;
}
function
sendGetRequest
(
request_path
,
params
)
{
// 生成签名
const
{
signature
,
timestamp
}
=
createSignature
(
"GET"
,
request_path
,
params
)
;
// 生成请求头
const
headers
=
{
'OK-ACCESS-KEY'
:
api_config
[
'api_key'
]
,
'OK-ACCESS-SIGN'
:
signature
,
'OK-ACCESS-TIMESTAMP'
:
timestamp
,
'OK-ACCESS-PASSPHRASE'
:
api_config
[
'passphrase'
]
,
}
;
const
options
=
{
hostname
:
'web3.okx.com'
,
path
:
request_path
+
(
params
?
`
?
${
querystring
.
stringify
(
params
)
}
`
:
''
)
,
method
:
'GET'
,
headers
:
headers
}
;
const
req
=
https
.
request
(
options
,
(
res
)
=>
{
let
data
=
''
;
res
.
on
(
'data'
,
(
chunk
)
=>
{
data
+=
chunk
;
}
)
;
res
.
on
(
'end'
,
(
)
=>
{
console
.
log
(
data
)
;
}
)
;
}
)
;
req
.
end
(
)
;
}
function
sendPostRequest
(
request_path
,
params
)
{
// 生成签名
const
{
signature
,
timestamp
}
=
createSignature
(
"POST"
,
request_path
,
params
)
;
// 生成请求头
const
headers
=
{
'OK-ACCESS-KEY'
:
api_config
[
'api_key'
]
,
'OK-ACCESS-SIGN'
:
signature
,
'OK-ACCESS-TIMESTAMP'
:
timestamp
,
'OK-ACCESS-PASSPHRASE'
:
api_config
[
'passphrase'
]
,
'Content-Type'
:
'application/json'
}
;
const
options
=
{
hostname
:
'web3.okx.com'
,
path
:
request_path
,
method
:
'POST'
,
headers
:
headers
}
;
const
req
=
https
.
request
(
options
,
(
res
)
=>
{
let
data
=
''
;
res
.
on
(
'data'
,
(
chunk
)
=>
{
data
+=
chunk
;
}
)
;
res
.
on
(
'end'
,
(
)
=>
{
console
.
log
(
data
)
;
}
)
;
}
)
;
if
(
params
)
{
req
.
write
(
JSON
.
stringify
(
params
)
)
;
}
req
.
end
(
)
;
}
// GET 请求示例
const
getRequestPath
=
'/api/v5/dex/aggregator/quote'
;
const
getParams
=
{
'chainId'
:
42161
,
'amount'
:
1000000000000
,
'toTokenAddress'
:
'0xff970a61a04b1ca14834a43f5de4533ebddb5cc8'
,
'fromTokenAddress'
:
'0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'
}
;
sendGetRequest
(
getRequestPath
,
getParams
)
;
// POST 请求示例
const
postRequestPath
=
'/api/v5/mktplace/nft/ordinals/listings'
;
const
postParams
=
{
'slug'
:
'sats'
}
;
sendPostRequest
(
postRequestPath
,
postParams
)
;
遗留 API
#
钱包 API、市场 API 和 DeFi API 已经被归档，我们将不再提供更新。如果你正在使用相关服务并需要查看有关的文档内容 ，请前往
这里
。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="api-访问和用法">API 访问和用法<a class="index_header-anchor__Xqb+L" href="#api-访问和用法" style="opacity:0">#</a></h1>
<p>在开始使用 DEX API 之前，你需要先在开发者管理平台创建项目并生成 API key。详细的步骤和相关资源请参考<a href="/zh-hans/build/dev-docs/dex-api/dex-developer-portal">这里</a>。</p>
<h2 data-content="鉴权" id="鉴权">鉴权<a class="index_header-anchor__Xqb+L" href="#鉴权" style="opacity:0">#</a></h2>
<p>所有对 API 发起访问的请求都需要包括下面信息来进行身份认证。</p>
<ul>
<li>OK-ACCESS-KEY ： API key</li>
<li>OK-ACCESS-TIMESTAMP ：发起请求的时间 (UTC) 。ISO 格式，如：2020-12-08T09:08:57.715Z</li>
<li>OK-ACCESS-PASSPHRASE ：创建 API key 时指定的 passphrase</li>
<li>OK-ACCESS-SIGN ：签名</li>
</ul>
<p>签名步骤：</p>
<ul>
<li>第一步：将 timestamp 、 method 、requestPath 、 body 拼接成一个字符串</li>
<li>第二步：以 HMAC SHA256 算法 和 secret key (在创建 API key 时生成) 对预哈希字符串 (第一步产生的结果) 进行签名</li>
<li>第三步：以 Base64 算法对签名进行编码</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rfbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rfbf:">解释</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><ul>
<li>例如，sign=CryptoJS.enc.Base64.stringify(CryptoJS.HmacSHA256(timestamp + 'GET' + '/api/v5/dex/aggregator/swap', SecretKey))</li>
<li>其中，timestamp 与 OK-ACCESS-TIMESTAMP 必须相同</li>
<li>其中，GET 是 method （HTTP请求方法，字母全部大写）</li>
<li>其中，/api/v5/dex/aggregator/swap 是requestPath （请求接口路径）</li>
<li>其中 body 为空。如果请求没有请求体（通常为 GET 请求），那 body 可省略</li>
</ul></div></div></div></div></div>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rhbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rhbf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><ul>
<li>时间戳与服务端时差不得超过 30 秒</li>
<li>POST 请求需包含原始请求体参与签名计算</li>
<li>Secret key 仅创建时可见，请通过安全渠道存储</li>
</ul></div></div></div></div></div>
<h2 data-content="Postman 示例" id="postman-示例">Postman 示例<a class="index_header-anchor__Xqb+L" href="#postman-示例" style="opacity:0">#</a></h2>
<p>Postman 是一款流行的 API 开发和测试工具，允许开发人员设计、测试和记录 API。它提供了对用户友好的图形界面，用于向 API 发送 HTTP 请求。</p>
<p>如果你还没有安装 Postman，你可以免费从 Postman 网站下载它：<a class="items-center" href="https://www.postman.com/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://www.postman.com/<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rpbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rpbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">这个示例需要你具备对 Postman 的基础理解。</div></div></div></div></div>
<h3 id="添加参数">添加参数<a class="index_header-anchor__Xqb+L" href="#添加参数" style="opacity:0">#</a></h3>
<ul>
<li>这通常适用于 GET 请求。</li>
<li>如果你的请求需要查询参数，你可以在 <strong>Params</strong> 选项卡下添加它们。在这里，你可以添加查询参数的 key-value pair。</li>
</ul>
<p><picture class="okui-picture index_pic__VGZfY okui-picture-font" style="width:100%;aspect-ratio:3.1341463414634148"><img alt="图片" class="index_img__AfAvr" src="https://web3.okx.com/cdn/assets/okexchain/okc-docs/dex-docs/../9200ae895b949b939dad.png?x-oss-process=image/format,webp"/></picture></p>
<h3 id="设置标题">设置标题<a class="index_header-anchor__Xqb+L" href="#设置标题" style="opacity:0">#</a></h3>
<p>在 <strong>Headers</strong> 选项卡下，添加以下键-值对：</p>
<ul>
<li><code>OK-ACCESS-KEY</code></li>
<li><code>OK-ACCESS-PASSPHRASE</code></li>
</ul>
<p><picture class="okui-picture index_pic__VGZfY okui-picture-font" style="width:100%;aspect-ratio:3.1341463414634148"><img alt="图片" class="index_img__AfAvr" src="https://web3.okx.com/cdn/assets/okexchain/okc-docs/dex-docs/../f8aa803831e35d7c9d68.png?x-oss-process=image/format,webp"/></picture></p>
<h3 id="添加正文">添加正文<a class="index_header-anchor__Xqb+L" href="#添加正文" style="opacity:0">#</a></h3>
<ul>
<li>这通常适用于 POST 请求。</li>
<li>如果你的请求需要一个请求主体，你可以在 <strong>Body</strong> 选项卡下添加它们。</li>
<li>在下拉菜单中选择 <strong>raw</strong> 和 <strong>JSON</strong>。</li>
<li>使用 JSON 格式输入你的请求主体。</li>
</ul>
<p><picture class="okui-picture index_pic__VGZfY okui-picture-font" style="width:100%;aspect-ratio:3.1341463414634148"><img alt="图片" class="index_img__AfAvr" src="https://web3.okx.com/cdn/assets/okexchain/okc-docs/dex-docs/../e456946243de17a068c9.png?x-oss-process=image/format,webp"/></picture></p>
<h3 id="设置预请求脚本">设置预请求脚本<a class="index_header-anchor__Xqb+L" href="#设置预请求脚本" style="opacity:0">#</a></h3>
<ul>
<li>用于生成所需的签名 (<code>OK-ACCESS-SIGN</code>) 和时间戳 (<code>OK-ACCESS-TIMESTAMP</code>)。</li>
<li>在 <strong>Pre-request Script</strong> 选项卡下，插入与请求类型相对应的脚本。</li>
<li>在生成预哈希字符串时，GET 请求会排除请求主体。</li>
<li>根据需要编辑密钥。</li>
</ul>
<p>GET 请求：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">var</span> method <span class="token operator">=</span> pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">method</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> now <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> isoString <span class="token operator">=</span> now<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> path <span class="token operator">=</span> pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">url</span><span class="token punctuation">.</span><span class="token method function property-access">getPathWithQuery</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> sign<span class="token operator">=</span><span class="token maybe-class-name">CryptoJS</span><span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span><span class="token maybe-class-name">CryptoJS</span><span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>isoString <span class="token operator">+</span> method <span class="token operator">+</span> path<span class="token punctuation">,</span> pm<span class="token punctuation">.</span><span class="token property-access">variables</span><span class="token punctuation">.</span><span class="token method function property-access">replaceIn</span><span class="token punctuation">(</span><span class="token string">'{{secret_key}}'</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">headers</span><span class="token punctuation">.</span><span class="token method function property-access">add</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">key</span><span class="token operator">:</span> <span class="token string">'OK-ACCESS-SIGN'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">value</span><span class="token operator">:</span> sign
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">headers</span><span class="token punctuation">.</span><span class="token method function property-access">add</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">key</span><span class="token operator">:</span> <span class="token string">'OK-ACCESS-TIMESTAMP'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">value</span><span class="token operator">:</span> isoString
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<p>POST 请求:</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">var</span> method <span class="token operator">=</span> pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">method</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> now <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> isoString <span class="token operator">=</span> now<span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> path <span class="token operator">=</span> pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">url</span><span class="token punctuation">.</span><span class="token method function property-access">getPathWithQuery</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> bodyStr <span class="token operator">=</span> pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">body</span><span class="token punctuation">.</span><span class="token property-access">raw</span><span class="token punctuation">;</span>
<span class="token keyword">var</span> sign<span class="token operator">=</span><span class="token maybe-class-name">CryptoJS</span><span class="token punctuation">.</span><span class="token property-access">enc</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Base64</span></span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span><span class="token maybe-class-name">CryptoJS</span><span class="token punctuation">.</span><span class="token method function property-access"><span class="token maybe-class-name">HmacSHA256</span></span><span class="token punctuation">(</span>isoString <span class="token operator">+</span> method <span class="token operator">+</span> path <span class="token operator">+</span> bodyStr<span class="token punctuation">,</span> pm<span class="token punctuation">.</span><span class="token property-access">variables</span><span class="token punctuation">.</span><span class="token method function property-access">replaceIn</span><span class="token punctuation">(</span><span class="token string">'{{secret_key}}'</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>

pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">headers</span><span class="token punctuation">.</span><span class="token method function property-access">add</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">key</span><span class="token operator">:</span> <span class="token string">'OK-ACCESS-SIGN'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">value</span><span class="token operator">:</span> sign
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

pm<span class="token punctuation">.</span><span class="token property-access">request</span><span class="token punctuation">.</span><span class="token property-access">headers</span><span class="token punctuation">.</span><span class="token method function property-access">add</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">key</span><span class="token operator">:</span> <span class="token string">'OK-ACCESS-TIMESTAMP'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">value</span><span class="token operator">:</span> isoString
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="Javascript 示例" id="javascript-示例">Javascript 示例<a class="index_header-anchor__Xqb+L" href="#javascript-示例" style="opacity:0">#</a></h2>
<p>若要通过 Javascript 脚本调用 API，请参考以下代码示例：</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> https <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'https'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> crypto <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'crypto'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> querystring <span class="token operator">=</span> <span class="token function">require</span><span class="token punctuation">(</span><span class="token string">'querystring'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 定义 API 凭证</span>
<span class="token keyword">const</span> api_config <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token string-property property">"api_key"</span><span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">,</span>
  <span class="token string-property property">"secret_key"</span><span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">,</span>
  <span class="token string-property property">"passphrase"</span><span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token keyword">function</span> <span class="token function">preHash</span><span class="token punctuation">(</span><span class="token parameter">timestamp<span class="token punctuation">,</span> method<span class="token punctuation">,</span> request_path<span class="token punctuation">,</span> params</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// 根据字符串和参数创建预签名</span>
  <span class="token keyword">let</span> query_string <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>method <span class="token operator">===</span> <span class="token string">'GET'</span> <span class="token operator">&amp;&amp;</span> params<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    query_string <span class="token operator">=</span> <span class="token string">'?'</span> <span class="token operator">+</span> querystring<span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
  <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>method <span class="token operator">===</span> <span class="token string">'POST'</span> <span class="token operator">&amp;&amp;</span> params<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    query_string <span class="token operator">=</span> <span class="token known-class-name class-name">JSON</span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>
  <span class="token keyword control-flow">return</span> timestamp <span class="token operator">+</span> method <span class="token operator">+</span> request_path <span class="token operator">+</span> query_string<span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">function</span> <span class="token function">sign</span><span class="token punctuation">(</span><span class="token parameter">message<span class="token punctuation">,</span> secret_key</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// 使用 HMAC-SHA256 对预签名字符串进行签名</span>
  <span class="token keyword">const</span> hmac <span class="token operator">=</span> crypto<span class="token punctuation">.</span><span class="token method function property-access">createHmac</span><span class="token punctuation">(</span><span class="token string">'sha256'</span><span class="token punctuation">,</span> secret_key<span class="token punctuation">)</span><span class="token punctuation">;</span>
  hmac<span class="token punctuation">.</span><span class="token method function property-access">update</span><span class="token punctuation">(</span>message<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> hmac<span class="token punctuation">.</span><span class="token method function property-access">digest</span><span class="token punctuation">(</span><span class="token string">'base64'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">function</span> <span class="token function">createSignature</span><span class="token punctuation">(</span><span class="token parameter">method<span class="token punctuation">,</span> request_path<span class="token punctuation">,</span> params</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// 获取 ISO 8601 格式时间戳</span>
  <span class="token keyword">const</span> timestamp <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">Date</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">toISOString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token method function property-access">slice</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token operator">-</span><span class="token number">5</span><span class="token punctuation">)</span> <span class="token operator">+</span> <span class="token string">'Z'</span><span class="token punctuation">;</span>
  <span class="token comment">// 生成签名</span>
  <span class="token keyword">const</span> message <span class="token operator">=</span> <span class="token function">preHash</span><span class="token punctuation">(</span>timestamp<span class="token punctuation">,</span> method<span class="token punctuation">,</span> request_path<span class="token punctuation">,</span> params<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> signature <span class="token operator">=</span> <span class="token function">sign</span><span class="token punctuation">(</span>message<span class="token punctuation">,</span> api_config<span class="token punctuation">[</span><span class="token string">'secret_key'</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token keyword control-flow">return</span> <span class="token punctuation">{</span> signature<span class="token punctuation">,</span> timestamp <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">function</span> <span class="token function">sendGetRequest</span><span class="token punctuation">(</span><span class="token parameter">request_path<span class="token punctuation">,</span> params</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// 生成签名</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> signature<span class="token punctuation">,</span> timestamp <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">createSignature</span><span class="token punctuation">(</span><span class="token string">"GET"</span><span class="token punctuation">,</span> request_path<span class="token punctuation">,</span> params<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 生成请求头</span>
  <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">'OK-ACCESS-KEY'</span><span class="token operator">:</span> api_config<span class="token punctuation">[</span><span class="token string">'api_key'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-SIGN'</span><span class="token operator">:</span> signature<span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-TIMESTAMP'</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-PASSPHRASE'</span><span class="token operator">:</span> api_config<span class="token punctuation">[</span><span class="token string">'passphrase'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> options <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">hostname</span><span class="token operator">:</span> <span class="token string">'web3.okx.com'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">path</span><span class="token operator">:</span> request_path <span class="token operator">+</span> <span class="token punctuation">(</span>params <span class="token operator">?</span> <span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">?</span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>querystring<span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span> <span class="token operator">:</span> <span class="token string">''</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'GET'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headers
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> req <span class="token operator">=</span> https<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span>options<span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">let</span> data <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
    res<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'data'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">chunk</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      data <span class="token operator">+=</span> chunk<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    res<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'end'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  req<span class="token punctuation">.</span><span class="token method function property-access">end</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">function</span> <span class="token function">sendPostRequest</span><span class="token punctuation">(</span><span class="token parameter">request_path<span class="token punctuation">,</span> params</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token comment">// 生成签名</span>
  <span class="token keyword">const</span> <span class="token punctuation">{</span> signature<span class="token punctuation">,</span> timestamp <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">createSignature</span><span class="token punctuation">(</span><span class="token string">"POST"</span><span class="token punctuation">,</span> request_path<span class="token punctuation">,</span> params<span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token comment">// 生成请求头</span>
  <span class="token keyword">const</span> headers <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token string-property property">'OK-ACCESS-KEY'</span><span class="token operator">:</span> api_config<span class="token punctuation">[</span><span class="token string">'api_key'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-SIGN'</span><span class="token operator">:</span> signature<span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-TIMESTAMP'</span><span class="token operator">:</span> timestamp<span class="token punctuation">,</span>
    <span class="token string-property property">'OK-ACCESS-PASSPHRASE'</span><span class="token operator">:</span> api_config<span class="token punctuation">[</span><span class="token string">'passphrase'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">'Content-Type'</span><span class="token operator">:</span> <span class="token string">'application/json'</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> options <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">hostname</span><span class="token operator">:</span> <span class="token string">'web3.okx.com'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">path</span><span class="token operator">:</span> request_path<span class="token punctuation">,</span>
    <span class="token literal-property property">method</span><span class="token operator">:</span> <span class="token string">'POST'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">headers</span><span class="token operator">:</span> headers
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> req <span class="token operator">=</span> https<span class="token punctuation">.</span><span class="token method function property-access">request</span><span class="token punctuation">(</span>options<span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">res</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">let</span> data <span class="token operator">=</span> <span class="token string">''</span><span class="token punctuation">;</span>
    res<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'data'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token parameter">chunk</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      data <span class="token operator">+=</span> chunk<span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    res<span class="token punctuation">.</span><span class="token method function property-access">on</span><span class="token punctuation">(</span><span class="token string">'end'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span>params<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    req<span class="token punctuation">.</span><span class="token method function property-access">write</span><span class="token punctuation">(</span><span class="token known-class-name class-name">JSON</span><span class="token punctuation">.</span><span class="token method function property-access">stringify</span><span class="token punctuation">(</span>params<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span>

  req<span class="token punctuation">.</span><span class="token method function property-access">end</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// GET 请求示例</span>
<span class="token keyword">const</span> getRequestPath <span class="token operator">=</span> <span class="token string">'/api/v5/dex/aggregator/quote'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> getParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token string-property property">'chainId'</span><span class="token operator">:</span> <span class="token number">42161</span><span class="token punctuation">,</span>
  <span class="token string-property property">'amount'</span><span class="token operator">:</span> <span class="token number">1000000000000</span><span class="token punctuation">,</span>
  <span class="token string-property property">'toTokenAddress'</span><span class="token operator">:</span> <span class="token string">'0xff970a61a04b1ca14834a43f5de4533ebddb5cc8'</span><span class="token punctuation">,</span>
  <span class="token string-property property">'fromTokenAddress'</span><span class="token operator">:</span> <span class="token string">'0x82aF49447D8a07e3bd95BD0d56f35241523fBab1'</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token function">sendGetRequest</span><span class="token punctuation">(</span>getRequestPath<span class="token punctuation">,</span> getParams<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// POST 请求示例</span>
<span class="token keyword">const</span> postRequestPath <span class="token operator">=</span> <span class="token string">'/api/v5/mktplace/nft/ordinals/listings'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> postParams <span class="token operator">=</span> <span class="token punctuation">{</span>
  <span class="token string-property property">'slug'</span><span class="token operator">:</span> <span class="token string">'sats'</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token function">sendPostRequest</span><span class="token punctuation">(</span>postRequestPath<span class="token punctuation">,</span> postParams<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="遗留 API" id="遗留-api">遗留 API<a class="index_header-anchor__Xqb+L" href="#遗留-api" style="opacity:0">#</a></h2>
<p>钱包 API、市场 API 和 DeFi API 已经被归档，我们将不再提供更新。如果你正在使用相关服务并需要查看有关的文档内容 ，请前往<a href="/zh-hans/build/docs/waas/okx-waas-what-is-waas">这里</a> 。</p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "首页",
    "API 访问和用法"
  ],
  "sidebar_links": [
    "什么是 DEX API",
    "API 访问和用法",
    "API 费用",
    "支持的链",
    "开发者平台",
    "环境设置",
    "运行第一个程序",
    "用户协议"
  ],
  "toc": [
    "鉴权",
    "Postman 示例",
    "Javascript 示例",
    "遗留 API"
  ]
}
```

</details>
