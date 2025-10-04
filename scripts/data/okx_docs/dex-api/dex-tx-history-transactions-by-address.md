# 获取交易历史 | API 参考 | 交易历史 API | 行情 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-tx-history-transactions-by-address#获取交易历史  
**抓取时间:** 2025-05-27 06:17:23  
**字数:** 295

## 导航路径
DEX API > 行情 API > API 参考 > 获取交易历史

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
获取交易历史
获取交易历史
#
查询地址维度下的交易历史，按时间倒序排序。
请求路径
#
GET
https://web3.okx.com/api/v5/dex/post-transaction/transactions-by-address
请求参数
#
Parameter
Type
Required
Description
address
String
是
具体某条链的账户地址。
chains
String
是
筛选需要获取交易历史的链，多条链以","分隔。最多支持 50 个。(如
1
代表Ethereum。更多可查看
这里
。)
tokenContractAddress
String
否
代币地址。
1
：传""代表查询对应链的主链币。
2
：传具体的代币合约地址，代表查询对应的代币。
3
：不传，代表查询主链币和所有代币。
begin
String
否
开始时间，查询晚于该时间的交易历史。Unix 时间戳，用毫秒表示。
end
String
否
结束时间，查询早于该时间的交易历史。若 begin 和 end 都不传，查询当前时间以前的交易历史。Unix 时间戳，用毫秒表示。
cursor
String
否
游标。
limit
String
否
返回条数，默认返回最近的 20 条。多链查询最多支持 20 条，单链查询最多 100 条。
响应参数
#
Parameter
Type
Description
transactions
Array
交易列表
>chainIndex
String
链 ID
>txHash
String
交易 hash
>itype
String
交易的层级类型
0
:外层主链币转移
1
:合约内层主链币转移
2
:token转移
>methodId
String
合约调用函数
>nonce
String
发起者地址发起的第几笔交易
>txTime
String
交易时间；Unix时间戳的毫秒数格式，如 1597026383085
>from
Array
交易输入
>>address
String
发送/输入地址，多签交易时，逗号分隔
>>amount
String
输入数量
>to
Array
交易输出
>>address
String
接收。输出地址，多签交易时，逗号分隔
>>amount
String
输出数量
>tokenContractAddress
String
代币的合约地址
>amount
String
交易数量
>symbol
String
交易数量对应的币种
>txFee
String
手续费
>txStatus
String
交易状态、success 成功、fail 失败、pending 等待确认
>hitBlacklist
Boolean
false：不是黑名单 true：是黑名单
cursor
String
游标
获取支持的链
获取特定交易
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api//v5/dex/post-transaction/transactions-by-address?address=0x50c476a139aab23fdaf9bca12614cdd54a4244e4&chains=1'
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
\
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
"cursor"
:
"1706197403"
,
"transactionList"
:
[
{
"chainIndex"
:
"1"
,
"txHash"
:
"0x963767695543cfb7804039c470b110b87adf9ab69ebc002b571523b714b828ca"
,
"methodId"
:
""
,
"nonce"
:
""
,
"txTime"
:
"1724213411000"
,
"from"
:
[
{
"address"
:
"0xae7ab96520de3a18e5e111b5eaab095312d7fe84"
"amount"
:
""
}
]
,
"to"
:
[
{
"address"
:
"0x50c476a139aab23fdaf9bca12614cdd54a4244e4"
"amount"
:
""
}
]
,
"tokenContractAddress"
:
"0xe13c851c331874028cd8f681052ad3367000fb13"
,
"amount"
:
"1"
,
"symbol"
:
"claim rewards on stethdao.net"
,
"txFee"
:
""
,
"txStatus"
:
"success"
,
"hitBlacklist"
:
true
,
"tag"
:
"Risk Airdrop"
,
"itype"
:
"2"
}
]
}
]
}
获取支持的链
获取特定交易

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-market-api-introduction" style="color:inherit">行情 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">交易历史 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-transactions-by-address" style="color:inherit">获取交易历史</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取交易历史">获取交易历史<a class="index_header-anchor__Xqb+L" href="#获取交易历史" style="opacity:0">#</a></h1><p>查询地址维度下的交易历史，按时间倒序排序。</p><h3 id="请求路径">请求路径<a class="index_header-anchor__Xqb+L" href="#请求路径" style="opacity:0">#</a></h3><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/post-transaction/transactions-by-address</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Required</th><th>Description</th></tr></thead><tbody><tr><td>address</td><td>String</td><td>是</td><td>具体某条链的账户地址。</td></tr><tr><td>chains</td><td>String</td><td>是</td><td>筛选需要获取交易历史的链，多条链以","分隔。最多支持 50 个。(如<code>1</code>代表Ethereum。更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。)</td></tr><tr><td>tokenContractAddress</td><td>String</td><td>否</td><td>代币地址。<br/> <code>1</code>：传""代表查询对应链的主链币。<br/><code>2</code>：传具体的代币合约地址，代表查询对应的代币。<br/><code>3</code>：不传，代表查询主链币和所有代币。</td></tr><tr><td>begin</td><td>String</td><td>否</td><td>开始时间，查询晚于该时间的交易历史。Unix 时间戳，用毫秒表示。</td></tr><tr><td>end</td><td>String</td><td>否</td><td>结束时间，查询早于该时间的交易历史。若 begin 和 end 都不传，查询当前时间以前的交易历史。Unix 时间戳，用毫秒表示。</td></tr><tr><td>cursor</td><td>String</td><td>否</td><td>游标。</td></tr><tr><td>limit</td><td>String</td><td>否</td><td>返回条数，默认返回最近的 20 条。多链查询最多支持 20 条，单链查询最多 100 条。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>Parameter</th><th>Type</th><th>Description</th></tr></thead><tbody><tr><td>transactions</td><td>Array</td><td>交易列表</td></tr><tr><td>&gt;chainIndex</td><td>String</td><td>链 ID</td></tr><tr><td>&gt;txHash</td><td>String</td><td>交易 hash</td></tr><tr><td>&gt;itype</td><td>String</td><td>交易的层级类型 <br/> <code>0</code>:外层主链币转移 <br/> <code>1</code>:合约内层主链币转移 <br/> <code>2</code>:token转移</td></tr><tr><td>&gt;methodId</td><td>String</td><td>合约调用函数</td></tr><tr><td>&gt;nonce</td><td>String</td><td>发起者地址发起的第几笔交易</td></tr><tr><td>&gt;txTime</td><td>String</td><td>交易时间；Unix时间戳的毫秒数格式，如 1597026383085</td></tr><tr><td>&gt;from</td><td>Array</td><td>交易输入</td></tr><tr><td>&gt;&gt;address</td><td>String</td><td>发送/输入地址，多签交易时，逗号分隔</td></tr><tr><td>&gt;&gt;amount</td><td>String</td><td>输入数量</td></tr><tr><td>&gt;to</td><td>Array</td><td>交易输出</td></tr><tr><td>&gt;&gt;address</td><td>String</td><td>接收。输出地址，多签交易时，逗号分隔</td></tr><tr><td>&gt;&gt;amount</td><td>String</td><td>输出数量</td></tr><tr><td>&gt;tokenContractAddress</td><td>String</td><td>代币的合约地址</td></tr><tr><td>&gt;amount</td><td>String</td><td>交易数量</td></tr><tr><td>&gt;symbol</td><td>String</td><td>交易数量对应的币种</td></tr><tr><td>&gt;txFee</td><td>String</td><td>手续费</td></tr><tr><td>&gt;txStatus</td><td>String</td><td>交易状态、success 成功、fail 失败、pending 等待确认</td></tr><tr><td>&gt;hitBlacklist</td><td>Boolean</td><td>false：不是黑名单 true：是黑名单</td></tr><tr><td>cursor</td><td>String</td><td>游标</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-specific-transaction-detail-by-txhash" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取特定交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api//v5/dex/post-transaction/transactions-by-address?address=0x50c476a139aab23fdaf9bca12614cdd54a4244e4&amp;chains=1'</span><span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'Content-Type: application/json'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-SIGN: leaV********3uw='</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-PASSPHRASE: 1****6'</span> <span class="token punctuation">\</span>
<span class="token parameter variable">--header</span> <span class="token string">'OK-ACCESS-TIMESTAMP: 2023-10-18T12:21:41.274Z'</span> <span class="token punctuation">\</span>
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token punctuation">{</span>
            <span class="token property">"cursor"</span><span class="token operator">:</span> <span class="token string">"1706197403"</span><span class="token punctuation">,</span>
            <span class="token property">"transactionList"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                <span class="token punctuation">{</span>
                    <span class="token property">"chainIndex"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"txHash"</span><span class="token operator">:</span> <span class="token string">"0x963767695543cfb7804039c470b110b87adf9ab69ebc002b571523b714b828ca"</span><span class="token punctuation">,</span>
                    <span class="token property">"methodId"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"nonce"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"txTime"</span><span class="token operator">:</span> <span class="token string">"1724213411000"</span><span class="token punctuation">,</span>
                    <span class="token property">"from"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                        <span class="token punctuation">{</span>
                            <span class="token property">"address"</span><span class="token operator">:</span> 
                                <span class="token string">"0xae7ab96520de3a18e5e111b5eaab095312d7fe84"</span>
                                <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">""</span>
                        <span class="token punctuation">}</span>
                    <span class="token punctuation">]</span><span class="token punctuation">,</span>
                    <span class="token property">"to"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                        <span class="token punctuation">{</span>
                            <span class="token property">"address"</span><span class="token operator">:</span> 
                                <span class="token string">"0x50c476a139aab23fdaf9bca12614cdd54a4244e4"</span>
                                <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">""</span>
                        <span class="token punctuation">}</span>
                    <span class="token punctuation">]</span><span class="token punctuation">,</span>
                    <span class="token property">"tokenContractAddress"</span><span class="token operator">:</span> <span class="token string">"0xe13c851c331874028cd8f681052ad3367000fb13"</span><span class="token punctuation">,</span>
                    <span class="token property">"amount"</span><span class="token operator">:</span> <span class="token string">"1"</span><span class="token punctuation">,</span>
                    <span class="token property">"symbol"</span><span class="token operator">:</span> <span class="token string">"claim rewards on stethdao.net"</span><span class="token punctuation">,</span>
                    <span class="token property">"txFee"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
                    <span class="token property">"txStatus"</span><span class="token operator">:</span> <span class="token string">"success"</span><span class="token punctuation">,</span>
                    <span class="token property">"hitBlacklist"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                    <span class="token property">"tag"</span><span class="token operator">:</span> <span class="token string">"Risk Airdrop"</span><span class="token punctuation">,</span>
                    <span class="token property">"itype"</span><span class="token operator">:</span> <span class="token string">"2"</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">]</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-chains" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取支持的链</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-tx-history-specific-transaction-detail-by-txhash" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">获取特定交易</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取交易历史"
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
