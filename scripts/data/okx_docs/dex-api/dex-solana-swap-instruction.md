# 获取 Solana 兑换交易指令 | API 参考 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-solana-swap-instruction#响应参数  
**抓取时间:** 2025-05-27 05:07:08  
**字数:** 1296

## 导航路径
DEX API > 交易 API > API 参考 > 获取 Solana 兑换交易指令

## 目录
- 搭建兑换应用
- 搭建跨链应用
- 介绍
- API 参考
- 获取支持的链
- 获取币种列表
- 获取流动性列表
- 交易授权
- 获取兑换价格
- 获取 Solana 兑换交易指令
- 兑换
- 查询交易状态
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

DEX API
交易 API
兑换 API
API 参考
获取 Solana 兑换交易指令
获取 Solana 兑换交易指令
#
获取在 Solana 兑换或者询价自定义组装使用的交易指令数据。
请求地址
#
GET
https://web3.okx.com/api/v5/dex/aggregator/swap-instruction
请求参数
#
参数
类型
必传
描述
chainIndex
String
是
链的唯一标识。
如
501
: Solana，更多可查看
这里
。
chainId
String
是
链的唯一标识。即将废弃
amount
String
是
币种询价数量
(数量需包含精度，如兑换 1.00 USDT 需输入 1000000，兑换 1.00 DAI 需输入 1000000000000000000)，币种精度可通过
币种列表
取得。
fromTokenAddress
String
是
询价币种合约地址 (如：
0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
)
toTokenAddress
String
是
目标币种合约地址 (如：
0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
)
slippage
String
是
滑点限制。
注意：
在 Solana 网络上，滑点最小值为
0
，最大值需
小于 1
。
（如：
0.005
代表这笔交易的最大滑点为
0.5%
，
1
代表这笔交易的最大滑点为
100%
）
userWalletAddress
String
是
用户钱包地址 (如：
0x3f6a3f57569358a512ccc0e513f171516b0fd42a
)
swapReceiverAddress
String
否
购买的资产的收件人地址 如果未设置，则用户钱包地址收到购买的资产 (如：
0x3f6a3f57569358a512ccc0e513f171516b0fd42a
)
feePercent
String
否
发送到分佣地址的询价或者目标币种数量百分比，
最小百分比：0
，
最大百分比：10
。最多支持小数点后 2 位，系统将自动忽略超出的部分。(例如：实际传入 1.326%，但分拥计算时仅会取 1.32% 的分拥比例)
fromTokenReferrerWalletAddress
String
否
收取 fromToken 分佣费用的钱包地址。
使用 API 时，
需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣
。
注意:
对于
Solana
:分佣地址需提前存入一些 SOL 进行激活。
toTokenReferrerWalletAddress
String
否
收取 toToken 分佣费用的钱包地址。
使用 API 时，
需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣
。
注意:
对于
Solana
:分佣地址需提前存入一些 SOL 进行激活。
dexIds
String
否
限定询价的流动性池 dexId , 多个组合按
,
分隔 (如
1,50,180
，更多可查看流动性列表)
priceImpactProtectionPercentage
String
否
(可选，默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。
当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。
这是一个
可选开启
的功能，默认值为 0.9。当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。
注意：
当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。
computeUnitPrice
String
否
用于 Solana 网络上的交易，类似于 Ethereum 上的 gasPrice，这个价格决定了交易的优先级，价格越高意味着交易越有可能更快地被网络处理。
computeUnitLimit
String
否
用于 Solana 网络上的交易，可类比为 Ethereum 上的的 gasLimit，这个限制可以确保交易不会占用过多的计算资源。
响应参数
#
参数
类型
描述
addressLookupTableAccount
Array
地址查找表账户。是 Solana 区块链中的一种数据结构，用于优化交易中地址的管理和引用。它允许开发者将一组相关的地址存储在一个表中，并通过索引值（而非完整的 32 字节地址）在交易中引用这些地址，从而显著提升交易的效率和可扩展性。
instructionLists
Array
交易指令详细信息
data
String
指令数据
accounts
Array
指令账户信息
isSigner
Boolean
账户是否是签名者
isWritable
Boolean
账户是否可写
pubkey
Boolean
账户公钥地址
programId
String
指令执行程序id
获取兑换价格
兑换
请求示例
#
shell
curl
--location
--request
GET
'https://web3.okx.com/api/v5/dex/aggregator/swap-instruction?chainIndex=501&amount=350000000&fromTokenAddress=11111111111111111111111111111111&toTokenAddress=Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB&slippage=0.4&userWalletAddress=FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk \
--header '
OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418
' \
--header '
OK-ACCESS-SIGN: leaV********3uw
=
' \
--header '
OK-ACCESS-PASSPHRASE:
1
****6
' \
--header '
OK-ACCESS-TIMESTAMP:
2023
-10-18T12:21:41.274Z'
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
{
"addressLookupTableAddresses"
:
[
"EDDSpjZHrsFKYTMJDcBqXAjkLcu9EKdvrQR4XnqsXErH"
,
"9YcB7FUV4cLxTtDWEf399ooy3idpfepeEhMqGihKDDwX"
,
"4tbRdGdVvuSzWjFeJJYVMv2vvTpEhCdWbFmNZAnuxmtk"
]
,
"instructionLists"
:
[
{
"data"
:
"ApC+BgA="
,
"accounts"
:
[
]
,
"programId"
:
"ComputeBudget111111111111111111111111111111"
}
,
{
"data"
:
"A08vKAAAAAAA"
,
"accounts"
:
[
]
,
"programId"
:
"ComputeBudget111111111111111111111111111111"
}
,
{
"data"
:
"AwAAAN22LW+lIkpOjB6e81eI68Mgzu7zEfkmh9QEBkCPOLG3DQAAAAAAAAAxNzM5MjU1OTc3NzU58B0fAAAAAAClAAAAAAAAAAbd9uHXZaGT2cvhRs7reawctIXtX1s3kTqM9YV+/wCp"
,
"accounts"
:
[
{
"isSigner"
:
true
,
"isWritable"
:
false
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
]
,
"programId"
:
"11111111111111111111111111111111"
}
,
{
"data"
:
"AQ=="
,
"accounts"
:
[
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"So11111111111111111111111111111111111111112"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"SysvarRent111111111111111111111111111111111"
}
]
,
"programId"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
,
{
"data"
:
"AgAAAICT3BQAAAAA"
,
"accounts"
:
[
{
"isSigner"
:
true
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
]
,
"programId"
:
"11111111111111111111111111111111"
}
,
{
"data"
:
"EQ=="
,
"accounts"
:
[
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
]
,
"programId"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
,
{
"data"
:
"AQ=="
,
"accounts"
:
[
{
"isSigner"
:
true
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"11111111111111111111111111111111"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
]
,
"programId"
:
"ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
}
,
{
"data"
:
"QUs/TOtbW4iAk9wUAAAAAIXrRQQAAAAAHVqQAgAAAAABAAAAgJPcFAAAAAABAAAAAgAAAAEAAAANAQAAAGQBAAAABQEAAABkTpgBAAAAAAA="
,
"accounts"
:
[
{
"isSigner"
:
true
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"So11111111111111111111111111111111111111112"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"
}
,
{
"isSigner"
:
true
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HjkGLCPnsMr4yP2Tmi1Uj7gV7Y2xDj2Npn9kYfVBYr2s"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"8gJ7UWboMeQ6z6AQwFP3cAZwSYG8udVS2UesyCbH79r7"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"chM5ZB1uPZxvJJAK4D1Z4KHAYjWKvwuQTy6fFAeWQ1T"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"FGFaiYjXTVuLsKvzn6ueckraNTeqUGHeYqrQPQCpd7kH"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"So11111111111111111111111111111111111111112"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"DoBNfRox1ZjEsZq6QPY4jpN8hN4Fu9JVkAxJQro164VR"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"D1ZN9Wj1fRSUQfCjhvnu1hqDMT7hzjzBBpi12nVniYD6"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"6TWKYuLYtuJVtvfqnPEs1ZxFMRDGTKkQJgTa4Dv7CzQS"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"EMfT8Jw2M5fs691J6ycgTuggXRJ4uLfbCrqZYJXMXpdL"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"7VVeicGxT7XmwG4Sg25QVFRcAZDaBtGxT9d1CpByzGYN"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"5quBtoiQqxF9Jv6KYKctB59NT3gtJD2Y65kdnB1Uev3h"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HV1KXxWFaSeriyFvXyx48FqG9BoFbfinB8njCJonqP7K"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HjkGLCPnsMr4yP2Tmi1Uj7gV7Y2xDj2Npn9kYfVBYr2s"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"2EXiumdi14E9b8Fy62QcA5Uh6WdHS2b38wtSxp72Mibj"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"3uaZBfHPfmpAHW7dsimC1SnyR61X4bJqQZKWmRSCXJxv"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"4zbGjjRx8bmZjynJg2KnkJ54VAk1crcrYsGMy79EXK1P"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"5XkWQL9FJL4qEvL8c3zCzzWnMGzerM3jbGuuyRprsEgG"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"jfrmNrBtxnX1FH36ATeiaXnpA4ppQcKtv7EfrgMsgLJ"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"CDSr3ssLcRB6XYPJwAfFt18MZvEZp4LjHcvzBVZ45duo"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"77quYg4MGneUdjgXCunt9GgM1usmrxKY31twEy3WHwcS"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"37m9QdvxmKRdjm3KKV2AjTiGcXMfWHQpVFnmhtb289yo"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"AQKXXC29ybqL8DLeAVNt3ebpwMv8Sb4csberrP6Hz6o5"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9MgPMkdEHFX7DZaitSh6Crya3kCCr1As6JC75bm3mjuC"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"H61Y7xVnbWVXrQQx3EojTEqf3ogKVY5GfGjEn5ewyX7B"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9FLih4qwFMjdqRAGmHeCxa64CgjP1GtcgKJgHHgz44ar"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
false
,
"pubkey"
:
"FGBvMAu88q9d1Csz7ZECB5a2gbWwp6qicNxN2Mo7QhWG"
}
]
,
"programId"
:
"6m2CDdhRgxpH4WjvdzxAYbGxwdGUz5MziiL5jek2kBma"
}
,
{
"data"
:
"CQ=="
,
"accounts"
:
[
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"
}
,
{
"isSigner"
:
false
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
,
{
"isSigner"
:
true
,
"isWritable"
:
true
,
"pubkey"
:
"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"
}
]
,
"programId"
:
"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
]
}
,
"msg"
:
""
}
获取兑换价格
兑换

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="doc-content routes_web3-content__PbRs0 routes_web3-content-with-sec-nav__6HMH4"><div class="index_wrapper__5T0Vu"><div aria-label="页面路径" class="okui-breadcrumbs okui-breadcrumbs-secondary okui-breadcrumbs-lg" role="navigation"><div class="okui-overflow_scroll"><div class="okui-overflow_scroll-nav"><div class="okui-overflow_scroll-nav-icon icon-left icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm icon-left-inner" role="img"></i></div><div class="okui-overflow_scroll-nav-icon icon-right icon-hide"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-sm" role="img"></i></div></div><div class="okui-overflow_scroll-scroll"><div class="okui-overflow_scroll-scroll-children"><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-what-is-dex-api" style="color:inherit">DEX API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-trade-api-introduction" style="color:inherit">交易 API</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><span class="cursor-auto index_text__5k+e+">兑换 API</span></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div class="okui-breadcrumbs-crumb"><div class="okui-hyperlink okui-hyperlink-secondary okui-hyperlink-no-hover-underline okui-hyperlink-lg okui-hyperlink-medium okui-breadcrumbs-crumb-link"><span class="okui-hyperlink-text"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-api-reference" style="color:inherit">API 参考</a></span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md crumb-icon" role="img"></i></div><div aria-current="location" class="okui-breadcrumbs-crumb okui-breadcrumbs-crumb-active"><a class="index_text__5k+e+" href="/zh-hans/build/dev-docs/dex-api/dex-solana-swap-instruction" style="color:inherit">获取 Solana 兑换交易指令</a></div></div></div></div></div></div><!--$-->
<div class="index_container__BsMBZ"><div class="index_params-wrapper__P58Fw"><h1 id="获取-solana-兑换交易指令">获取 Solana 兑换交易指令<a class="index_header-anchor__Xqb+L" href="#获取-solana-兑换交易指令" style="opacity:0">#</a></h1><p>获取在 Solana 兑换或者询价自定义组装使用的交易指令数据。</p><h2 data-content="请求地址" id="请求地址">请求地址<a class="index_header-anchor__Xqb+L" href="#请求地址" style="opacity:0">#</a></h2><p><span class="index_tag__Pwjko">GET</span> <code>https://web3.okx.com/api/v5/dex/aggregator/swap-instruction</code></p><h2 data-content="请求参数" id="请求参数">请求参数<a class="index_header-anchor__Xqb+L" href="#请求参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>必传</th><th>描述</th></tr></thead><tbody><tr><td>chainIndex</td><td>String</td><td>是</td><td>链的唯一标识。 <br/>如<code>501</code>: Solana，更多可查看<a href="/zh-hans/build/dev-docs/dex-api/dex-supported-chain">这里</a>。</td></tr><tr><td>chainId</td><td>String</td><td>是</td><td>链的唯一标识。即将废弃</td></tr><tr><td>amount</td><td>String</td><td>是</td><td>币种询价数量  <br/> (数量需包含精度，如兑换 1.00 USDT 需输入 1000000，兑换 1.00 DAI 需输入 1000000000000000000)，币种精度可通过<a href="/zh-hans/build/dev-docs/dex-get-tokens">币种列表</a>取得。</td></tr><tr><td>fromTokenAddress</td><td>String</td><td>是</td><td>询价币种合约地址 (如：<code>0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee</code>)</td></tr><tr><td>toTokenAddress</td><td>String</td><td>是</td><td>目标币种合约地址 (如：<code>0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48</code>)</td></tr><tr><td>slippage</td><td>String</td><td>是</td><td>滑点限制。<br/> <br/> 注意：<br/> 在 Solana 网络上，滑点最小值为 <code>0</code>，最大值需<code>小于 1</code>。<br/> （如：<code>0.005</code>代表这笔交易的最大滑点为<code>0.5%</code>，<code>1</code>代表这笔交易的最大滑点为 <code>100%</code>）</td></tr><tr><td>userWalletAddress</td><td>String</td><td>是</td><td>用户钱包地址 (如：<code>0x3f6a3f57569358a512ccc0e513f171516b0fd42a</code>)</td></tr><tr><td>swapReceiverAddress</td><td>String</td><td>否</td><td>购买的资产的收件人地址 如果未设置，则用户钱包地址收到购买的资产 (如：<code>0x3f6a3f57569358a512ccc0e513f171516b0fd42a</code>)</td></tr><tr><td>feePercent</td><td>String</td><td>否</td><td>发送到分佣地址的询价或者目标币种数量百分比，<code>最小百分比：0</code>，<code>最大百分比：10</code>。最多支持小数点后 2 位，系统将自动忽略超出的部分。(例如：实际传入 1.326%，但分拥计算时仅会取 1.32% 的分拥比例)</td></tr><tr><td>fromTokenReferrerWalletAddress</td><td>String</td><td>否</td><td>收取 fromToken 分佣费用的钱包地址。<br/>使用 API 时，<strong>需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣</strong>。<br/><br/>注意:<br/> 对于 <strong>Solana</strong>:分佣地址需提前存入一些 SOL 进行激活。</td></tr><tr><td>toTokenReferrerWalletAddress</td><td>String</td><td>否</td><td>收取 toToken 分佣费用的钱包地址。<br/>使用 API 时，<strong>需要结合 feePercent 设置佣金比例，且单笔交易只能选择 fromToken 分佣或 toToken 分佣</strong>。<br/><br/>注意:<br/> 对于 <strong>Solana</strong>:分佣地址需提前存入一些 SOL 进行激活。</td></tr><tr><td>dexIds</td><td>String</td><td>否</td><td>限定询价的流动性池 dexId , 多个组合按 <code>,</code> 分隔 (如 <code>1,50,180</code> ，更多可查看流动性列表)</td></tr><tr><td>priceImpactProtectionPercentage</td><td>String</td><td>否</td><td>(可选，默认值为 90%) 允许的价格影响百分比 (介于 0 和 1.0 之间)。<br/> <br/> 当用户设置了 priceImpactProtectionPercentage 后，如果估算的价格影响超过了指定的百分比，将会返回一个错误。例如，如果 PriceImpactProtectionPercentage = .25 (25%)，任何价格影响高于 25% 的报价都将返回错误。<br/> <br/> 这是一个<strong>可选开启</strong>的功能，默认值为 0.9。当百分比被设置为 1.0 (100%) 时，此功能将被禁用，也就是说，每一笔交易都会被允许通过。<br/><br/> <strong>注意：</strong>当我们无法计算价格影响时，我们会返回 null，并且价格影响保护也会被禁用。</td></tr><tr><td>computeUnitPrice</td><td>String</td><td>否</td><td>用于 Solana 网络上的交易，类似于 Ethereum 上的 gasPrice，这个价格决定了交易的优先级，价格越高意味着交易越有可能更快地被网络处理。</td></tr><tr><td>computeUnitLimit</td><td>String</td><td>否</td><td>用于 Solana 网络上的交易，可类比为 Ethereum 上的的 gasLimit，这个限制可以确保交易不会占用过多的计算资源。</td></tr></tbody></table></div><h2 data-content="响应参数" id="响应参数">响应参数<a class="index_header-anchor__Xqb+L" href="#响应参数" style="opacity:0">#</a></h2><div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>addressLookupTableAccount</td><td>Array</td><td>地址查找表账户。是 Solana 区块链中的一种数据结构，用于优化交易中地址的管理和引用。它允许开发者将一组相关的地址存储在一个表中，并通过索引值（而非完整的 32 字节地址）在交易中引用这些地址，从而显著提升交易的效率和可扩展性。</td></tr><tr><td>instructionLists</td><td>Array</td><td>交易指令详细信息</td></tr><tr><td>data</td><td>String</td><td>指令数据</td></tr><tr><td>accounts</td><td>Array</td><td>指令账户信息</td></tr><tr><td>isSigner</td><td>Boolean</td><td>账户是否是签名者</td></tr><tr><td>isWritable</td><td>Boolean</td><td>账户是否可写</td></tr><tr><td>pubkey</td><td>Boolean</td><td>账户公钥地址</td></tr><tr><td>programId</td><td>String</td><td>指令执行程序id</td></tr></tbody></table></div><div class="index_pc-footer__bI-X6"><div data-ssr-id=":R2df:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-quote" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取兑换价格</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-swap" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">兑换</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div><div class="index_code-example-wrapper__xJmbi"><h2 data-content="请求示例" id="请求示例">请求示例<a class="index_header-anchor__Xqb+L" href="#请求示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW">shell</div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-shell"><code class="language-shell"><span class="token function">curl</span> <span class="token parameter variable">--location</span> <span class="token parameter variable">--request</span> GET <span class="token string">'https://web3.okx.com/api/v5/dex/aggregator/swap-instruction?chainIndex=501&amp;amount=350000000&amp;fromTokenAddress=11111111111111111111111111111111&amp;toTokenAddress=Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB&amp;slippage=0.4&amp;userWalletAddress=FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk \</span>
<span class="token string"></span>
<span class="token string">--header '</span>OK-ACCESS-KEY: 37c541a1-****-****-****-10fe7a038418<span class="token string">' \</span>
<span class="token string">--header '</span>OK-ACCESS-SIGN: leaV********3uw<span class="token operator">=</span><span class="token string">' \</span>
<span class="token string">--header '</span>OK-ACCESS-PASSPHRASE: <span class="token number">1</span>****6<span class="token string">' \</span>
<span class="token string">--header '</span>OK-ACCESS-TIMESTAMP: <span class="token number">2023</span>-10-18T12:21:41.274Z'
</code></pre></div></div></div><h2 data-content="响应示例" id="响应示例">响应示例<a class="index_header-anchor__Xqb+L" href="#响应示例" style="opacity:0">#</a></h2><div class="index_code-example__GIWWb"><div class="index_header__fvB9O"><div class="index_option__w7tNW"><div class="flex items-center"><div class="index_circle__Y78Kg" style="background-color:#31BD65"></div>200</div></div><div class="okui-popup okui-tooltip okui-tooltip-neutral" data-testid="okd-popup"><i class="icon iconfont doc-ssr-okds-copy cursor-pointer okui-a11y-button" role="button" style="font-size:28px" tabindex="0"></i></div></div><div class="index_code-example-body__PrHtZ"><div class="remark-highlight"><pre class="language-json"><code class="language-json"><span class="token punctuation">{</span>
    <span class="token property">"code"</span><span class="token operator">:</span> <span class="token string">"0"</span><span class="token punctuation">,</span>
    <span class="token property">"data"</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token property">"addressLookupTableAddresses"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token string">"EDDSpjZHrsFKYTMJDcBqXAjkLcu9EKdvrQR4XnqsXErH"</span><span class="token punctuation">,</span>
            <span class="token string">"9YcB7FUV4cLxTtDWEf399ooy3idpfepeEhMqGihKDDwX"</span><span class="token punctuation">,</span>
            <span class="token string">"4tbRdGdVvuSzWjFeJJYVMv2vvTpEhCdWbFmNZAnuxmtk"</span>
        <span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token property">"instructionLists"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"ApC+BgA="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"ComputeBudget111111111111111111111111111111"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"A08vKAAAAAAA"</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"ComputeBudget111111111111111111111111111111"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"AwAAAN22LW+lIkpOjB6e81eI68Mgzu7zEfkmh9QEBkCPOLG3DQAAAAAAAAAxNzM5MjU1OTc3NzU58B0fAAAAAAClAAAAAAAAAAbd9uHXZaGT2cvhRs7reawctIXtX1s3kTqM9YV+/wCp"</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"11111111111111111111111111111111"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"AQ=="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"So11111111111111111111111111111111111111112"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"SysvarRent111111111111111111111111111111111"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"AgAAAICT3BQAAAAA"</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"11111111111111111111111111111111"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"EQ=="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"AQ=="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"11111111111111111111111111111111"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"QUs/TOtbW4iAk9wUAAAAAIXrRQQAAAAAHVqQAgAAAAABAAAAgJPcFAAAAAABAAAAAgAAAAEAAAANAQAAAGQBAAAABQEAAABkTpgBAAAAAAA="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"So11111111111111111111111111111111111111112"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HjkGLCPnsMr4yP2Tmi1Uj7gV7Y2xDj2Npn9kYfVBYr2s"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"8gJ7UWboMeQ6z6AQwFP3cAZwSYG8udVS2UesyCbH79r7"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"chM5ZB1uPZxvJJAK4D1Z4KHAYjWKvwuQTy6fFAeWQ1T"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FGFaiYjXTVuLsKvzn6ueckraNTeqUGHeYqrQPQCpd7kH"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"So11111111111111111111111111111111111111112"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"DoBNfRox1ZjEsZq6QPY4jpN8hN4Fu9JVkAxJQro164VR"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"D1ZN9Wj1fRSUQfCjhvnu1hqDMT7hzjzBBpi12nVniYD6"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"6TWKYuLYtuJVtvfqnPEs1ZxFMRDGTKkQJgTa4Dv7CzQS"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"EMfT8Jw2M5fs691J6ycgTuggXRJ4uLfbCrqZYJXMXpdL"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"7VVeicGxT7XmwG4Sg25QVFRcAZDaBtGxT9d1CpByzGYN"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"5quBtoiQqxF9Jv6KYKctB59NT3gtJD2Y65kdnB1Uev3h"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HV1KXxWFaSeriyFvXyx48FqG9BoFbfinB8njCJonqP7K"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HjkGLCPnsMr4yP2Tmi1Uj7gV7Y2xDj2Npn9kYfVBYr2s"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"HwEh3U3E7aPRwXUhzes6wxX1kbSmKm85ugK6DXP5vgzf"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"2EXiumdi14E9b8Fy62QcA5Uh6WdHS2b38wtSxp72Mibj"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"3uaZBfHPfmpAHW7dsimC1SnyR61X4bJqQZKWmRSCXJxv"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"4zbGjjRx8bmZjynJg2KnkJ54VAk1crcrYsGMy79EXK1P"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"5XkWQL9FJL4qEvL8c3zCzzWnMGzerM3jbGuuyRprsEgG"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"jfrmNrBtxnX1FH36ATeiaXnpA4ppQcKtv7EfrgMsgLJ"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"CDSr3ssLcRB6XYPJwAfFt18MZvEZp4LjHcvzBVZ45duo"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"77quYg4MGneUdjgXCunt9GgM1usmrxKY31twEy3WHwcS"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"37m9QdvxmKRdjm3KKV2AjTiGcXMfWHQpVFnmhtb289yo"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"AQKXXC29ybqL8DLeAVNt3ebpwMv8Sb4csberrP6Hz6o5"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9MgPMkdEHFX7DZaitSh6Crya3kCCr1As6JC75bm3mjuC"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"H61Y7xVnbWVXrQQx3EojTEqf3ogKVY5GfGjEn5ewyX7B"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9FLih4qwFMjdqRAGmHeCxa64CgjP1GtcgKJgHHgz44ar"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FGBvMAu88q9d1Csz7ZECB5a2gbWwp6qicNxN2Mo7QhWG"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"6m2CDdhRgxpH4WjvdzxAYbGxwdGUz5MziiL5jek2kBma"</span>
            <span class="token punctuation">}</span><span class="token punctuation">,</span>
            <span class="token punctuation">{</span>
                <span class="token property">"data"</span><span class="token operator">:</span> <span class="token string">"CQ=="</span><span class="token punctuation">,</span>
                <span class="token property">"accounts"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"9haFKThJYWEVA66mtxv7nTBWMHieQdnZpmLjvXAiS2zm"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span><span class="token punctuation">,</span>
                    <span class="token punctuation">{</span>
                        <span class="token property">"isSigner"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"isWritable"</span><span class="token operator">:</span> <span class="token boolean">true</span><span class="token punctuation">,</span>
                        <span class="token property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"FvUDkjR1STZ3c6g3DjXwLsiQ477t2HGH4LQ81xMKWJZk"</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">]</span><span class="token punctuation">,</span>
                <span class="token property">"programId"</span><span class="token operator">:</span> <span class="token string">"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">]</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token property">"msg"</span><span class="token operator">:</span> <span class="token string">""</span>
<span class="token punctuation">}</span>
</code></pre></div></div></div><div class="index_sm-footer__Mk-6b"><div data-ssr-id=":R2lf:"><div class="md:flex md:justify-between index_web3-pagination-footer__9BwqX"><a class="flex items-center justify-start grow index_last__rkE9+" href="/zh-hans/build/dev-docs/dex-api/dex-get-quote" target="_self"><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-left-centered-md index_icon__B+vCh" role="img" style="margin-right:8px"></i><div><span class="truncate-2 index_f-16__mSYje">获取兑换价格</span></div></a><a class="flex items-center justify-end grow index_next__Bv5Lh" href="/zh-hans/build/dev-docs/dex-api/dex-swap" target="_self"><div><span class="truncate-2 index_f-16__mSYje" style="padding-right:8px">兑换</span></div><i aria-hidden="true" class="icon iconfont doc-ssr-okds-arrow-chevron-right-centered-md index_icon__B+vCh" role="img"></i></a></div></div></div></div></div><!--/$--></div>
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
    "获取 Solana 兑换交易指令"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取币种列表",
    "获取流动性列表",
    "交易授权",
    "获取兑换价格",
    "获取 Solana 兑换交易指令",
    "兑换",
    "查询交易状态",
    "设置分佣",
    "DEX 集成",
    "智能合约",
    "错误码",
    "FAQ",
    "介绍",
    "API 参考",
    "支持的跨链桥"
  ],
  "toc": [
    "搭建兑换应用",
    "搭建跨链应用",
    "介绍",
    "API 参考",
    "获取支持的链",
    "获取币种列表",
    "获取流动性列表",
    "交易授权",
    "获取兑换价格",
    "获取 Solana 兑换交易指令",
    "兑换",
    "查询交易状态",
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
