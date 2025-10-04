# 在 Solana 链上发送多签交易 | 搭建跨链应用 | 指南 | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-use-crosschain-solana-quick-start#在-solana-链上发送多签交易  
**抓取时间:** 2025-05-27 04:29:54  
**字数:** 276

## 导航路径
DEX API > 交易 API > 搭建跨链应用 > 在 Solana 链上发送多签交易

## 目录
- 搭建兑换应用
- 搭建跨链应用
- 搭建跨链应用
- 在 Solana 链上发送多签交易
- 介绍
- API 参考
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

在 Solana 链上发送多签交易
#
import
*
as
anchor
from
'@coral-xyz/anchor'
import
{
base64
,
bs58
}
from
'@coral-xyz/anchor/dist/cjs/utils/bytes'
;
async
function
sendtx
(
)
{
const
connection
=
new
anchor
.
web3
.
Connection
(
anchor
.
web3
.
clusterApiUrl
(
"mainnet-beta"
)
// "https://solana-mainnet.g.alchemy.com/v2/EiyeW_PJ3a0Yig7E61nZHpfbMapVbV4m"
)
const
keypair
=
anchor
.
web3
.
Keypair
.
fromSecretKey
(
bs58
.
decode
(
"YOUR_USER_KEYPAIR"
)
)
// user’s wallet private key
const
wallet
=
new
anchor
.
Wallet
(
keypair
)
const
provider
=
new
anchor
.
AnchorProvider
(
connection
,
wallet
)
;
console
.
log
(
wallet
.
publicKey
.
toString
(
)
)
let
json
=
{
"data"
:
"hEFh3sGCFQKmLrMKDhDzr623WrtzawSrzHmtCqquGT2rX63Eh1bxU6UQJRT8WK1DqNJDA2hVvNvm3hpPCbkStRBs9qooQzUP5BSZJMqKGUxFPv5PT1p1kMNCvCc68jL1JQdsPNdhAFHaZa5UcEobMW62DeXorNgf74rCCYcYmH8Jd5TDQjE5Njp94iAqj12fv6WrWUSfHBZvRyrp4HxCUM55UfESi8d1tvFeVBGHXXn1kUdJPaUm4nia2WFxeaKS3RnrTwQeTfHSGK7j1sHvg1k5JStZQxZWaBi58tE7g4RWcEiuYedBKCGT4fjeNxCi8rBfsSk34QNSoRxxQpmayEzCMBFtMgwbpjXR3a1RuQHTBaEtpoUYaRoHtwHbLJ1C6eKBWULEyAxu1gQ8VmCQwh8qZHtuKBeamFGJxH2GK5mQ7rRftHXFhiTpPBfQHcYsFvZP73STDMGA6EMXFb5VKenocr6dG1tcxm4m4VbEiovqTuma6goegYMPA1RJV3fuVRqU4ZyD1AhiGGZyWCHpMpyjsRgFx65k51QBLZzNtmydPfTWnzPCPjYR5EYWsnNy2jGrj1RRTdKNryEE7S1DPB9hh5eHT6qchGyHEpi9WnzV2EntQqzuWz6u9DMVEt1n27ZeK7AcLRjyherRr5v4UvceZZf8ESqPo7Z2CZaMHYqfw463RLBjB5tLsWDR6hMv8RfSnEAy6dMEKkw4zm8h5Gp2JZTHX4ddo7Ag8TNhZkAzkGYk9GAbVKDooNTmVHD8kzQudj4dSCUAebJM7sgapVvbp2ucg7v6TUZvWUUwfvzUiCfxqTxP2z3cxrKmpwkffNZpsE5NnzVxvieGxQLFJqCUfk2eAct3XY6bFr6EkP5n6w8EDo399d3G2J7ohRDt9psCY9YZrgDY2JAYhLp2vGwApkhrfAPwK5voamxXuoghwkQcTmcK3MdU1A8gTH3jhxbFqEom4pmMKbgYaESEnSJpB2wsd1KdDwZjjoHB4HLFMH7fod6FZuH2VMfyjhoHLYEBWuq4DXid9RmWwsazH9qHyNpY4napPvxFcn2hGGtWzav3CMHCFHsz58wtg7ZzmF3yMS6KvGJq2UtqHfBCSd7xMJJPEmKHnftyUtGx23cL4f4J1NyHzwARqo9SFqrZHBVFwaKGAZn3666D9SUt3f6ukGEGDmBnkoK4N9bBpVrdb4zdbRoAPf59wWVCMZ4PHQtGrYYBbZ7omtG5s3BmZy41AxNaAaBEcnhxrzcthK2CqadxZtRooUkUnviWsrhyNH4Cu4xT8TTCJm7VuHsG3rkZSds3pGeMPkna2Ny8RsFtu4vhqQyhyvBzNbNo5ycoeaerFKaS87ny3kAXKzUDSyNFRqfFaoqwcu7fTtxvJgnyv5fLg1a3Ak9avNxKjfrZEc17n1Tq44Vtsbv9YsGjCLqTUEiAQMsvXC1WG6nbQ1DexwsyiUtxy7DcViG4bLQChhMvEM1AYP"
,
"from"
:
"Jk9fBdZBe83dsy5t8FWuk26LZhytWJCa7MXTqkiDEtF"
,
"gasLimit"
:
"622500"
,
"gasPrice"
:
"5000"
,
"key"
:
[
"5B7Q21z2B5o2D1WVpp3LXNFq4NbY2HsVRnWbLTtj3mAdbXnPQe2QvJtrizW8expLE91HbXypzrw8vJsAxm3nHTrW"
]
,
"maxPriorityFeePerGas"
:
""
,
"to"
:
"AqwtzPZxUmM6KoDCm5ceC7kje4DB2bLPRjKVJ8njCjKx"
,
"value"
:
"28000000"
}
const
keypair2
=
anchor
.
web3
.
Keypair
.
fromSecretKey
(
bs58
.
decode
(
json
.
key
[
0
]
)
)
// randomKeyAccount parameters
const
wallet2
=
new
anchor
.
Wallet
(
keypair2
)
let
transaction
=
anchor
.
web3
.
VersionedTransaction
.
deserialize
(
Buffer
.
from
(
bs58
.
decode
(
json
.
data
)
)
)
const
{
blockhash
}
=
await
connection
.
getLatestBlockhash
(
)
;
transaction
.
message
.
recentBlockhash
=
blockhash
 transaction
.
sign
(
[
keypair
,
keypair2
]
)
// Using randomKeyAccount and user’s wallet private key for multi-signature operations
const
txId
=
await
connection
.
sendTransaction
(
transaction
,
{
skipPreflight
:
false
,
maxRetries
:
20
}
)
console
.
log
(
"txId: "
,
txId
)
}
sendtx
(
)

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="在-solana-链上发送多签交易">在 Solana 链上发送多签交易<a class="index_header-anchor__Xqb+L" href="#在-solana-链上发送多签交易" style="opacity:0">#</a></h1>
<div class="remark-highlight"><pre class="language-js"><code class="language-js"><span class="token keyword module">import</span> <span class="token imports"><span class="token operator">*</span> <span class="token keyword module">as</span> anchor</span> <span class="token keyword module">from</span> <span class="token string">'@coral-xyz/anchor'</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> base64<span class="token punctuation">,</span> bs58 <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@coral-xyz/anchor/dist/cjs/utils/bytes'</span><span class="token punctuation">;</span>
<span class="token keyword">async</span> <span class="token keyword">function</span> <span class="token function">sendtx</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> connection <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">anchor<span class="token punctuation">.</span>web3<span class="token punctuation">.</span>Connection</span><span class="token punctuation">(</span>
        anchor<span class="token punctuation">.</span><span class="token property-access">web3</span><span class="token punctuation">.</span><span class="token method function property-access">clusterApiUrl</span><span class="token punctuation">(</span><span class="token string">"mainnet-beta"</span><span class="token punctuation">)</span>
        <span class="token comment">// "https://solana-mainnet.g.alchemy.com/v2/EiyeW_PJ3a0Yig7E61nZHpfbMapVbV4m"</span>
    <span class="token punctuation">)</span>
    <span class="token keyword">const</span> keypair <span class="token operator">=</span> anchor<span class="token punctuation">.</span><span class="token property-access">web3</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Keypair</span></span><span class="token punctuation">.</span><span class="token method function property-access">fromSecretKey</span><span class="token punctuation">(</span>
        bs58<span class="token punctuation">.</span><span class="token method function property-access">decode</span><span class="token punctuation">(</span><span class="token string">"YOUR_USER_KEYPAIR"</span><span class="token punctuation">)</span>
    <span class="token punctuation">)</span>
    <span class="token comment">// user’s wallet private key</span>
    <span class="token keyword">const</span> wallet <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">anchor<span class="token punctuation">.</span>Wallet</span><span class="token punctuation">(</span>keypair<span class="token punctuation">)</span>
    <span class="token keyword">const</span> provider <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">anchor<span class="token punctuation">.</span>AnchorProvider</span><span class="token punctuation">(</span>
        connection<span class="token punctuation">,</span>
        wallet
    <span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span>wallet<span class="token punctuation">.</span><span class="token property-access">publicKey</span><span class="token punctuation">.</span><span class="token method function property-access">toString</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">let</span> json <span class="token operator">=</span>
    <span class="token punctuation">{</span>
        <span class="token string-property property">"data"</span><span class="token operator">:</span> <span class="token string">"hEFh3sGCFQKmLrMKDhDzr623WrtzawSrzHmtCqquGT2rX63Eh1bxU6UQJRT8WK1DqNJDA2hVvNvm3hpPCbkStRBs9qooQzUP5BSZJMqKGUxFPv5PT1p1kMNCvCc68jL1JQdsPNdhAFHaZa5UcEobMW62DeXorNgf74rCCYcYmH8Jd5TDQjE5Njp94iAqj12fv6WrWUSfHBZvRyrp4HxCUM55UfESi8d1tvFeVBGHXXn1kUdJPaUm4nia2WFxeaKS3RnrTwQeTfHSGK7j1sHvg1k5JStZQxZWaBi58tE7g4RWcEiuYedBKCGT4fjeNxCi8rBfsSk34QNSoRxxQpmayEzCMBFtMgwbpjXR3a1RuQHTBaEtpoUYaRoHtwHbLJ1C6eKBWULEyAxu1gQ8VmCQwh8qZHtuKBeamFGJxH2GK5mQ7rRftHXFhiTpPBfQHcYsFvZP73STDMGA6EMXFb5VKenocr6dG1tcxm4m4VbEiovqTuma6goegYMPA1RJV3fuVRqU4ZyD1AhiGGZyWCHpMpyjsRgFx65k51QBLZzNtmydPfTWnzPCPjYR5EYWsnNy2jGrj1RRTdKNryEE7S1DPB9hh5eHT6qchGyHEpi9WnzV2EntQqzuWz6u9DMVEt1n27ZeK7AcLRjyherRr5v4UvceZZf8ESqPo7Z2CZaMHYqfw463RLBjB5tLsWDR6hMv8RfSnEAy6dMEKkw4zm8h5Gp2JZTHX4ddo7Ag8TNhZkAzkGYk9GAbVKDooNTmVHD8kzQudj4dSCUAebJM7sgapVvbp2ucg7v6TUZvWUUwfvzUiCfxqTxP2z3cxrKmpwkffNZpsE5NnzVxvieGxQLFJqCUfk2eAct3XY6bFr6EkP5n6w8EDo399d3G2J7ohRDt9psCY9YZrgDY2JAYhLp2vGwApkhrfAPwK5voamxXuoghwkQcTmcK3MdU1A8gTH3jhxbFqEom4pmMKbgYaESEnSJpB2wsd1KdDwZjjoHB4HLFMH7fod6FZuH2VMfyjhoHLYEBWuq4DXid9RmWwsazH9qHyNpY4napPvxFcn2hGGtWzav3CMHCFHsz58wtg7ZzmF3yMS6KvGJq2UtqHfBCSd7xMJJPEmKHnftyUtGx23cL4f4J1NyHzwARqo9SFqrZHBVFwaKGAZn3666D9SUt3f6ukGEGDmBnkoK4N9bBpVrdb4zdbRoAPf59wWVCMZ4PHQtGrYYBbZ7omtG5s3BmZy41AxNaAaBEcnhxrzcthK2CqadxZtRooUkUnviWsrhyNH4Cu4xT8TTCJm7VuHsG3rkZSds3pGeMPkna2Ny8RsFtu4vhqQyhyvBzNbNo5ycoeaerFKaS87ny3kAXKzUDSyNFRqfFaoqwcu7fTtxvJgnyv5fLg1a3Ak9avNxKjfrZEc17n1Tq44Vtsbv9YsGjCLqTUEiAQMsvXC1WG6nbQ1DexwsyiUtxy7DcViG4bLQChhMvEM1AYP"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"from"</span><span class="token operator">:</span> <span class="token string">"Jk9fBdZBe83dsy5t8FWuk26LZhytWJCa7MXTqkiDEtF"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"gasLimit"</span><span class="token operator">:</span> <span class="token string">"622500"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"gasPrice"</span><span class="token operator">:</span> <span class="token string">"5000"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"key"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token string">"5B7Q21z2B5o2D1WVpp3LXNFq4NbY2HsVRnWbLTtj3mAdbXnPQe2QvJtrizW8expLE91HbXypzrw8vJsAxm3nHTrW"</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token string-property property">"maxPriorityFeePerGas"</span><span class="token operator">:</span> <span class="token string">""</span><span class="token punctuation">,</span>
        <span class="token string-property property">"to"</span><span class="token operator">:</span> <span class="token string">"AqwtzPZxUmM6KoDCm5ceC7kje4DB2bLPRjKVJ8njCjKx"</span><span class="token punctuation">,</span>
        <span class="token string-property property">"value"</span><span class="token operator">:</span> <span class="token string">"28000000"</span>
    <span class="token punctuation">}</span>
    <span class="token keyword">const</span> keypair2 <span class="token operator">=</span> anchor<span class="token punctuation">.</span><span class="token property-access">web3</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">Keypair</span></span><span class="token punctuation">.</span><span class="token method function property-access">fromSecretKey</span><span class="token punctuation">(</span>bs58<span class="token punctuation">.</span><span class="token method function property-access">decode</span><span class="token punctuation">(</span>json<span class="token punctuation">.</span><span class="token property-access">key</span><span class="token punctuation">[</span><span class="token number">0</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token comment">// randomKeyAccount parameters</span>
    <span class="token keyword">const</span> wallet2 <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">anchor<span class="token punctuation">.</span>Wallet</span><span class="token punctuation">(</span>keypair2<span class="token punctuation">)</span>
    <span class="token keyword">let</span> transaction <span class="token operator">=</span> anchor<span class="token punctuation">.</span><span class="token property-access">web3</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">VersionedTransaction</span></span><span class="token punctuation">.</span><span class="token method function property-access">deserialize</span><span class="token punctuation">(</span><span class="token maybe-class-name">Buffer</span><span class="token punctuation">.</span><span class="token keyword module">from</span><span class="token punctuation">(</span>bs58<span class="token punctuation">.</span><span class="token method function property-access">decode</span><span class="token punctuation">(</span>json<span class="token punctuation">.</span><span class="token property-access">data</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token keyword">const</span> <span class="token punctuation">{</span> blockhash <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">getLatestBlockhash</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    transaction<span class="token punctuation">.</span><span class="token property-access">message</span><span class="token punctuation">.</span><span class="token property-access">recentBlockhash</span> <span class="token operator">=</span> blockhash
    transaction<span class="token punctuation">.</span><span class="token method function property-access">sign</span><span class="token punctuation">(</span><span class="token punctuation">[</span>keypair<span class="token punctuation">,</span> keypair2<span class="token punctuation">]</span><span class="token punctuation">)</span>
    <span class="token comment">// Using randomKeyAccount and user’s wallet private key for multi-signature operations</span>
    <span class="token keyword">const</span> txId <span class="token operator">=</span> <span class="token keyword control-flow">await</span> connection<span class="token punctuation">.</span><span class="token method function property-access">sendTransaction</span><span class="token punctuation">(</span>transaction<span class="token punctuation">,</span> <span class="token punctuation">{</span><span class="token literal-property property">skipPreflight</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span> <span class="token literal-property property">maxRetries</span><span class="token operator">:</span> <span class="token number">20</span><span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token console class-name">console</span><span class="token punctuation">.</span><span class="token method function property-access">log</span><span class="token punctuation">(</span><span class="token string">"txId: "</span><span class="token punctuation">,</span> txId<span class="token punctuation">)</span>
<span class="token punctuation">}</span>
<span class="token function">sendtx</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "搭建跨链应用",
    "在 Solana 链上发送多签交易"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
    "搭建跨链应用",
    "在 Solana 链上发送多签交易",
    "介绍",
    "API 参考",
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
  ],
  "toc": [
    "搭建兑换应用",
    "搭建跨链应用",
    "搭建跨链应用",
    "在 Solana 链上发送多签交易",
    "介绍",
    "API 参考",
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
