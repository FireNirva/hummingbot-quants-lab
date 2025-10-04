# 获取特定交易 | API 参考 | 交易历史 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-tx-history-specific-transaction-detail-by-txhash#响应示例  
**抓取时间:** 2025-05-27 04:37:51  
**字数:** 460

## 导航路径
DEX API > 行情 API > API 参考 > 获取特定交易

## 目录
- API 参考
- 错误码
- Websocket
- API 参考
- 错误码
- API 参考
- 错误码
- API 参考
- 获取支持的链
- 获取交易历史
- 获取特定交易
- 错误码

---

DEX API
行情 API
交易历史 API
API 参考
获取特定交易
获取特定交易
#
根据 txHash 查询某个交易的详情。
注意
将一笔交易和其中的内部交易都分解成子交易，并根据变动的资产类型给出了不同的子交易类型：
0
: 外层主链币转移
1
: 合约内层主链币转移
2
: token转移
请求路径
#
GET
https://web3.okx.com/api/v5/dex/post-transaction/transaction-detail-by-txhash
请求参数
#
Parameter
Type
Required
Description
chainIndex
String
是
链唯一标识。(如
1
代表Ethereum。更多可查看
这里
。)
txHash
String
是
交易哈希
itype
String
否
交易的层级类型
0
:外层主链币转移
1
:合约内层主链币转移
2
:token转移
响应参数
#
Parameter
Type
Description
chainIndex
String
链的唯一标识
height
String
交易发生的区块高度
txTime
String
交易时间；Unix时间戳的毫秒数格式
txhash
String
交易哈希
txStatus
String
交易状态
1
:pending 确认中
2
:success：成功
3
:fail：失败
gasLimit
String
gas限额
gasUsed
String
gas消耗
gasPrice
String
gas价格
txFee
String
交易手续费
否nce
String
否nce
amount
String
交易数量
symbol
String
交易数量对应的币种简称
methodId
String
合约调用函数
fromDetails
Array
交易输入详情
>address
String
发送/输入地址
>vinIndex
String
位于当前交易输入的序号
>preVoutIndex
String
位于上一笔输出里的序号
>txhash
String
交易哈希，和 prevoutIndex 一起唯一确认输入的 UTXO
> isContract
Boolean
发送地址是否是合约地址 true:是 ；false：否
> amount
String
交易数量
toDetails
Array
交易输出详情
>address
String
接收/输出地址
>voutIndex
String
输出的序号
> isContract
Boolean
接收地址是否是合约地址 true:是 ；false：否
> amount
String
交易数量
internalTransactionDetails
Array
内部交易详情
> from
String
交易发送方的地址
> to
String
交易接受方的地址
> isFromContract
Boolean
from地址是否是合约地址
> isToContract
Boolean
to地址是否是合约地址
> amount
String
交易数量
>txStatus
String
交易状态
tokenTransferDetails
Array
代币交易详情
> from
String
交易发送方的地址
> to
String
交易接受方的地址
> isFromContract
Boolean
from地址是否是合约地址
> isToContract
Boolean
to地址是否是合约地址
> tokenContractAddress
String
代币合约地址
> symbol
String
交易代币的简称
> amount
String
交易数量
l1OriginHash
String
L1执行的交易哈希
获取交易历史
错误码
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/post-transaction/transaction-detail-by-txhash?txHash=0x9ab8ccccc9f778ea91ce4c0f15517672c4bd06d166e830da41ba552e744d29a5&chainIndex=42161'
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
"chainIndex"
:
"42161"
,
"height"
:
"245222398"
,
"txTime"
:
"1724253417000"
,
"txhash"
:
"0x9ab8ccccc9f778ea91ce4c0f15517672c4bd06d166e830da41ba552e744d29a5"
,
"gasLimit"
:
"2000000"
,
"gasUsed"
:
"2000000"
,
"gasPrice"
:
"10000000"
,
"txFee"
:
""
,
"nonce"
:
"0"
,
"symbol"
:
"ETH"
,
"amount"
:
"0"
,
"txStatus"
:
"success"
,
"methodId"
:
"0xc9f95d32"
,
"l1OriginHash"
:
"0xa6a87ba2f18cc32bbae8f3b2253a29a9617ed1eb0940d80443f6e3bf9873dbad"
,
"fromDetails"
:
[
{
"address"
:
"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"
,
"vinIndex"
:
""
,
"preVoutIndex"
:
""
,
"txHash"
:
""
,
"isContract"
:
false
,
"amount"
:
""
}
]
,
"toDetails"
:
[
{
"address"
:
"0x000000000000000000000000000000000000006e"
,
"voutIndex"
:
""
,
"isContract"
:
false
,
"amount"
:
""
}
]
,
"internalTransactionDetails"
:
[
{
"from"
:
"0x0000000000000000000000000000000000000000"
,
"to"
:
"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"
,
"isFromContract"
:
false
,
"isToContract"
:
false
,
"amount"
:
"0.02"
,
"state"
:
"success"
}
,
{
"from"
:
"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"
,
"to"
:
"0x428ab2ba90eba0a4be7af34c9ac451ab061ac010"
,
"isFromContract"
:
false
,
"isToContract"
:
false
,
"amount"
:
"0.00998"
,
"state"
:
"success"
}
,
{
"from"
:
"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"
,
"to"
:
"0x428ab2ba90eba0a4be7af34c9ac451ab061ac010"
,
"isFromContract"
:
false
,
"isToContract"
:
false
,
"amount"
:
"0.009977946366846017"
,
"state"
:
"success"
}
]
,
"tokenTransferDetails"
:
[
]
}
]
}
获取交易历史
错误码

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">交易历史 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-specific-transaction-detail-by-txhash" style="color:inherit">获取特定交易</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取特定交易">获取特定交易<a class="index_header-anchor__Xqb+L" href="#获取特定交易" style="opacity:0">#</a></h1><p>根据 txHash 查询某个交易的详情。</p><div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rddf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rddf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"> 将一笔交易和其中的内部交易都分解成子交易，并根据变动的资产类型给出了不同的子交易类型：<br/> <code>0</code>: 外层主链币转移 <br/> <code>1</code>: 合约内层主链币转移 <br/> <code>2</code>: token转移</div></div></div></div></div><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/post-transaction/transaction-detail-by-txhash</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链唯一标识。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>txHash</td><td>String</td><td>是</td><td>交易哈希</td></tr><tr><td>itype</td><td>String</td><td>否</td><td>交易的层级类型 <br/> <code>0</code>:外层主链币转移 <br/> <code>1</code>:合约内层主链币转移 <br/> <code>2</code>:token转移</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>链的唯一标识</td></tr><tr><td>height</td><td>String</td><td>交易发生的区块高度</td></tr><tr><td>txTime</td><td>String</td><td>交易时间；Unix时间戳的毫秒数格式</td></tr><tr><td>txhash</td><td>String</td><td>交易哈希</td></tr><tr><td>txStatus</td><td>String</td><td>交易状态 <br/> <code>1</code>:pending 确认中 <br/> <code>2</code>:success：成功 <br/> <code>3</code>:fail：失败</td></tr><tr><td>gasLimit</td><td>String</td><td>gas限额</td></tr><tr><td>gasUsed</td><td>String</td><td>gas消耗</td></tr><tr><td>gasPrice</td><td>String</td><td>gas价格</td></tr><tr><td>txFee</td><td>String</td><td>交易手续费</td></tr><tr><td>否nce</td><td>String</td><td>否nce</td></tr><tr><td>amount</td><td>String</td><td>交易数量</td></tr><tr><td>symbol</td><td>String</td><td>交易数量对应的币种简称</td></tr><tr><td>methodId</td><td>String</td><td>合约调用函数</td></tr><tr><td>fromDetails</td><td>Array</td><td>交易输入详情</td></tr><tr><td>&gt;address</td><td>String</td><td>发送/输入地址</td></tr><tr><td>&gt;vinIndex</td><td>String</td><td>位于当前交易输入的序号</td></tr><tr><td>&gt;preVoutIndex</td><td>String</td><td>位于上一笔输出里的序号</td></tr><tr><td>&gt;txhash</td><td>String</td><td>交易哈希，和 prevoutIndex 一起唯一确认输入的 UTXO</td></tr><tr><td>&gt; isContract</td><td>Boolean</td><td>发送地址是否是合约地址 true:是 ；false：否</td></tr><tr><td>&gt; amount</td><td>String</td><td>交易数量</td></tr><tr><td>toDetails</td><td>Array</td><td>交易输出详情</td></tr><tr><td>&gt;address</td><td>String</td><td>接收/输出地址</td></tr><tr><td>&gt;voutIndex</td><td>String</td><td>输出的序号</td></tr><tr><td>&gt; isContract</td><td>Boolean</td><td>接收地址是否是合约地址 true:是 ；false：否</td></tr><tr><td>&gt; amount</td><td>String</td><td>交易数量</td></tr><tr><td>internalTransactionDetails</td><td>Array</td><td>内部交易详情</td></tr><tr><td>&gt; from</td><td>String</td><td>交易发送方的地址</td></tr><tr><td>&gt; to</td><td>String</td><td>交易接受方的地址</td></tr><tr><td>&gt; isFromContract</td><td>Boolean</td><td>from地址是否是合约地址</td></tr><tr><td>&gt; isToContract</td><td>Boolean</td><td>to地址是否是合约地址</td></tr><tr><td>&gt; amount</td><td>String</td><td>交易数量</td></tr><tr><td>&gt;txStatus</td><td>String</td><td>交易状态</td></tr><tr><td>tokenTransferDetails</td><td>Array</td><td>代币交易详情</td></tr><tr><td>&gt; from</td><td>String</td><td>交易发送方的地址</td></tr><tr><td>&gt; to</td><td>String</td><td>交易接受方的地址</td></tr><tr><td>&gt; isFromContract</td><td>Boolean</td><td>from地址是否是合约地址</td></tr><tr><td>&gt; isToContract</td><td>Boolean</td><td>to地址是否是合约地址</td></tr><tr><td>&gt; tokenContractAddress</td><td>String</td><td>代币合约地址</td></tr><tr><td>&gt; symbol</td><td>String</td><td>交易代币的简称</td></tr><tr><td>&gt; amount</td><td>String</td><td>交易数量</td></tr><tr><td>l1OriginHash</td><td>String</td><td>L1执行的交易哈希</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-transactions-by-address" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取交易历史</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/post-transaction/transaction-detail-by-txhash?txHash=0x9ab8ccccc9f778ea91ce4c0f15517672c4bd06d166e830da41ba552e744d29a5&amp;chainIndex=42161'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"42161"</span><span class="token punctuation">,</span>
            <span class="token property">"height"</span><span class="token operator">:</span> <span class="token string">"245222398"</span><span class="token punctuation">,</span>
            <span class="token property">"txTime"</span><span class="token operator">:</span> <span class="token string">"1724253417000"</span><span class="token punctuation">,</span>
            <span class="token property">"txhash"</span><span class="token operator">:</span> <span class="token string">"0x9ab8ccccc9f778ea91ce4c0f15517672c4bd06d166e830da41ba552e744d29a5"</span><span class="token punctuation">,</span>
            <span class="token property">"gasLimit"</span><span class="token operator">:</span> <span class="token string">"2000000"</span><span class="token punctuation">,</span>
            <span class="token property">"gasUsed"</span><span class="token operator">:</span> <span class="token string">"2000000"</span><span class="token punctuation">,</span>
            <span class="token property">"gasPrice"</span><span class="token operator">:</span> <span class="token string">"10000000"</span><span class="token punctuation">,</span>
            <span class="token property">"txFee"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
            <span class="token property">"nonce"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
            <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"ETH"</span><span class="token punctuation">,</span>
            <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
            <span class="token property">"txStatus"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
            <span class="token property">"methodId"</span><span class="token operator">:</span> <span class="token string">"0xc9f95d32"</span><span class="token punctuation">,</span>
            <span class="token property">"l1OriginHash"</span><span class="token operator">:</span> <span class="token string">"0xa6a87ba2f18cc32bbae8f3b2253a29a9617ed1eb0940d80443f6e3bf9873dbad"</span><span class="token punctuation">,</span>
            <span class="token property">"fromDetails"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"</span><span class="token punctuation">,</span>
                    <span class="token property">"vinIndex"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"preVoutIndex"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"isContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">""</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token property">"toDetails"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"address"</span><span class="token operator">:</span> <span class="token string">"0x000000000000000000000000000000000000006e"</span><span class="token punctuation">,</span>
                    <span class="token property">"voutIndex"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"isContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">""</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token property">"internalTransactionDetails"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"from"</span><span class="token operator">:</span> <span class="token string">"0x0000000000000000000000000000000000000000"</span><span class="token punctuation">,</span>
                    <span class="token property">"to"</span><span class="token operator">:</span> <span class="token string">"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"</span><span class="token punctuation">,</span>
                    <span class="token property">"isFromContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"isToContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"0.02"</span><span class="token punctuation">,</span>
                    <span class="token property">"state"</span><span class="token operator">:</span> <span class="token string">"success"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"from"</span><span class="token operator">:</span> <span class="token string">"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"</span><span class="token punctuation">,</span>
                    <span class="token property">"to"</span><span class="token operator">:</span> <span class="token string">"0x428ab2ba90eba0a4be7af34c9ac451ab061ac010"</span><span class="token punctuation">,</span>
                    <span class="token property">"isFromContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"isToContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"0.00998"</span><span class="token punctuation">,</span>
                    <span class="token property">"state"</span><span class="token operator">:</span> <span class="token string">"success"</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"from"</span><span class="token operator">:</span> <span class="token string">"0xd297fa914353c44b2e33ebe05f21846f1048cfeb"</span><span class="token punctuation">,</span>
                    <span class="token property">"to"</span><span class="token operator">:</span> <span class="token string">"0x428ab2ba90eba0a4be7af34c9ac451ab061ac010"</span><span class="token punctuation">,</span>
                    <span class="token property">"isFromContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"isToContract"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"0.009977946366846017"</span><span class="token punctuation">,</span>
                    <span class="token property">"state"</span><span class="token operator">:</span> <span class="token string">"success"</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token property">"tokenTransferDetails"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>

</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-transactions-by-address" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取交易历史</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-error-code" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">错误码</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取特定交易"
  ],
  "sidebar_links": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "获取支持的链",
    "获取交易历史",
    "获取特定交易",
    "错误码"
  ],
  "toc": [
    "API 参考",
    "错误码",
    "Websocket",
    "API 参考",
    "错误码",
    "API 参考",
    "错误码",
    "API 参考",
    "获取支持的链",
    "获取交易历史",
    "获取特定交易",
    "错误码"
  ]
}
```

</details>
