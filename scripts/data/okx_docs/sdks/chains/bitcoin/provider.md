# Provider API | Bitcoin | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/bitcoin/provider#getpublickey  
**抓取时间:** 2025-05-27 07:15:58  
**字数:** 2326

## 导航路径
DApp 连接钱包 > Bitcoin > Provider API

## 目录
- 什么是 Injected provider API？
- connect
- requestAccounts
- getAccounts
- getNetwork
- getPublicKey
- getBalance
- getInscriptions
- sendBitcoin
- send
- sendInscription
- transferNft
- signMessage
- pushTx
- splitUtxo
- inscribe
- mint
- signPsbt
- signPsbts
- pushPsbt
- sendPsbt
- accountChanged
- accountsChanged

---

Provider API
#
什么是 Injected provider API？
#
OKX Injected Providers API 基于 JavaScript 模型，由 OKX 嵌入用户访问网站中。DApp 项目可以通过调用此 API 请求用户账户信息，从用户所连接的区块链中读取数据，并协助用户进行消息和交易的签署。
connect
#
okxwallet.bitcoin.connect()
描述
连接钱包
参数
无
返回值
Promise - object
address - string：当前账户的地址
publicKey - string：当前账户的公钥
示例
const
result
=
await
okxwallet
.
bitcoin
.
connect
(
)
// example
{
address
:
'bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq'
,
publicKey
:
'4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497'
}
requestAccounts
#
此字段仅适用于插件端版本 2.77.1 或更高。
okxwallet.bitcoin.requestAccounts()
描述
请求连接当前账户
参数
无
返回值
Promise - string[]：当前账户的地址
示例
try
{
let
accounts
=
await
okxwallet
.
bitcoin
.
requestAccounts
(
)
;
console
.
log
(
'connect success'
,
accounts
)
;
}
catch
(
e
)
{
console
.
log
(
'connect failed'
)
;
}
// example
[
'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'
]
;
getAccounts
#
此字段仅适用于插件端版本 2.77.1 或更高。
okxwallet.bitcoin.getAccounts()
描述
获取当前账户地址
参数
无
返回值
Promise - string[]：当前账户地址
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
getAccounts
(
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
[
'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'
]
;
getNetwork
#
注意
不支持测试网络。
此字段仅适用于插件端版本 2.77.1 或更高。
okxwallet.bitcoin.getNetwork()
描述
获取网络
参数
无
返回值
Promise - string：网络
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
getNetwork
(
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
livenet
;
getPublicKey
#
此字段仅适用于插件端版本 2.77.1 或更高。
okxwallet.bitcoin.getPublicKey()
描述
获取当前账户的公钥
参数
无
返回值
Promise - string：公钥
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
getPublicKey
(
)
;
console
.
log
(
res
)
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
03cbaedc26f03fd3ba02fc936f338e980c9e2172c5e23128877ed46827e935296f
getBalance
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
okxwallet.bitcoin.getBalance()
描述
获取 BTC 余额
参数
无
返回值
Promise - object：
confirmed - number：已确认的聪数量
unconfirmed - number：未经确认的聪数量
total - number：总聪量
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
getBalance
(
)
;
console
.
log
(
res
)
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
{
"confirmed"
:
0
,
"unconfirmed"
:
100000
,
"total"
:
100000
}
getInscriptions
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
okxwallet.bitcoin.getInscriptions()
描述
获取当前账户的铭文列表
参数
cursor - number： (可选) 偏移量，从 0 开始，默认值是 0
size - number： (可选) 每页的数量，默认值是 20
返回值
Promise - object：
total - number：总数
list - object[]：
inscriptionId - string：铭文 ID
inscriptionNumber - string： 铭文编号
address - string：铭文地址
outputValue - string：铭文的输出值
contentLength - string：铭文的内容长度
contentType - number：铭文的内容类型
timestamp - number：铭文的区块时间
offset - number：铭文的偏移量
output - string：当前铭文所在 UTXO 的标识
genesisTransaction - string：创世交易的交易 ID
location - string：当前位置的 txid 和 vout
目前仅移动端版本不支持以上字段：inscriptionNumber、contentLength、contentType、timestamp、genesisTransaction。
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
getInscriptions
(
0
,
20
)
;
console
.
log
(
res
)
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
{
"total"
:
10
,
"list"
:
[
{
inscriptionId
:
'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531i0'
,
inscriptionNumber
:
55878989
,
address
:
'bc1q8h8s4zd9y0lkrx334aqnj4ykqs220ss735a3gh'
,
outputValue
:
546
,
contentLength
:
53
,
contentType
:
'text/plain'
,
timestamp
:
1705406294
,
location
:
'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531:0:0'
,
output
:
'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531:0'
,
offset
:
0
,
genesisTransaction
:
'02c9eae52923fdb21fe16ee9eb873c7d66fe412a61b75147451d8a47d089def4'
}
]
}
sendBitcoin
#
此字段仅适用于插件端版本 2.77.1 或更高。
okxwallet.bitcoin.sendBitcoin(toAddress, satoshis, options)
描述
发送比特币
参数
toAddress - string：发送地址
satoshis - number：1. 发送的聪数量
options - object： (可选)
feeRate - number：网络资费率
返回值
Promise- string：交易哈希
示例
try
{
let
txid
=
await
okxwallet
.
bitcoin
.
sendBitcoin
(
'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'
,
1000
)
;
console
.
log
(
txid
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
send
#
okxwallet.bitcoin.send({ from, to, value, satBytes })
描述
转移比特币 (支持 memo 字段)
参数
from - string：当前连接的钱包的 BTC 地址
to - string：接受 BTC 的地址
value - string：发送 BTC 的数量
satBytes - string： (可选) 自定义费率
memo - string： (可选) 指定 outputs OP_RETURN 内容
示例
memoPos - number： (可选) 指定 outputs OP_RETURN 输出位置，如果传了 memo 则必须传入 memoPos 指定位置，否则 memo 不生效
返回值
Promise - object
txhash：交易哈希
示例
const
result
=
await
window
.
okxwallet
.
bitcoin
.
send
(
{
from
:
'bc1p4k9ghlrynzuum080a4zk6e2my8kjzfhptr5747afzrn7xmmdtj6sgrhd0m'
,
to
:
'bc1plklsxq4wtv44dv8nm49fj0gh0zm9zxewm6ayzahrxc8yqtennc2s9udmcd'
,
value
:
'0.000012'
,
}
)
;
// example
{
txhash
:
'd153136cd74512b69d24c68b2d2c715c3629e607540c3f6cd3acc1140ca9bf57'
;
}
sendInscription
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。此外，移动端版本的 Atomicals 协议目前暂不支持此字段。
okxwallet.bitcoin.sendInscription(address, inscriptionId, options)
描述
发送铭文
参数
address - string：接收者地址
inscriptionId - string：铭文 ID + 协议，没有传协议则默认是 Ordinals NFT ，目前仅支持 Ordinals 及 Atomicals 协议
协议
描述
Ordinals
Ordinals 协议
Atomicals
Atomicals 协议
options - object： (可选)
feeRate - number：自定义费率
返回值
Promise - string：交易哈希
示例
// 发送 Ordinals NFT
try
{
let
txid
=
await
okxwallet
.
bitcoin
.
sendInscription
(
'tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'
,
'e9b86a063d78cc8a1ed17d291703bcc95bcd521e087ab0c7f1621c9c607def1ai0'
,
{
feeRate
:
15
}
)
;
console
.
log
(
'send Ordinal NFT to tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'
,
{
txid
}
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// 发送 Atomicals NFT
try
{
let
txid
=
await
okxwallet
.
bitcoin
.
sendInscription
(
'tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'
,
'ab12349dca49643fcc55c8e6a685ad0481047139c5b1af5af85387973fc7ceafi0-Atomicals'
,
{
feeRate
:
15
}
)
;
console
.
log
(
'send Atomicals NFT to tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'
,
{
txid
}
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
transferNft
#
此字段当前仅适用于插件端版本，不适用于移动端版本。
okxwallet.bitcoin.transferNft({ from, to, data })
描述
发送铭文
与 sendInscription 方法的不同点
transferNft
方法支持批量转移，
sendInscription
方法只支持单个转移
参数
from - string：当前连接的钱包的 BTC 地址
to - string：接受 NFT 的地址
data - string | string[]：发送的 NFT tokenId + 协议，如果是数组，则是批量转移多个 NFT ， 没有传协议则默认是 Ordinals NFT ，目前仅支持 Ordinals 及 Atomicals 协议
协议
描述
Ordinals
Ordinals 协议
Atomicals
Atomicals 协议
返回值
Promise - object
txhash - string：交易哈希
示例
// 发送 Ordinals NFT
try
{
let
res
=
await
window
.
okxwallet
.
bitcoin
.
transferNft
(
{
from
:
'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'
,
to
:
'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'
,
data
:
[
'2f285ba4c457c98c35dcb008114b96cee7c957f00a6993690efb231f91ccc2d9i0-Ordinals'
,
'2f2532f59d6e46931bc84e496cc6b45f87966b149b85ed3199265cb845550d58i0-Ordinals'
,
]
,
}
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
{
txhash
:
'df409c3ce3c4d7d840b681fab8a3a5b8e32b1600636cc5409d84d2c06365a5fc'
;
}
// 发送 Atomicals NFT
try
{
let
res
=
await
window
.
okxwallet
.
bitcoin
.
transferNft
(
{
from
:
'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'
,
to
:
'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'
,
data
:
[
'ab12349dca49643fcc55c8e6a685ad0481047139c5b1af5af85387973fc7ceafi0-Atomicals'
,
]
,
}
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
{
txhash
:
'df409c3ce3c4d7d840b681fab8a3a5b8e32b1600636cc5409d84d2c06365a5fc'
;
}
signMessage
#
okxwallet.bitcoin.signMessage(signStr[, type])
描述
签名消息
参数
signStr - string：需要签名的数据
type - string： (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"。(请注意：版本低于 6.51.0 的应用仅支持“ecdsa”签名算法，而版本为 6.51.0 或更高的应用可支持所有签名算法类型。)
返回值
Promise - string：签名结果
示例
const
signStr
=
'need sign string'
;
const
result
=
await
window
.
okxwallet
.
bitcoin
.
signMessage
(
signStr
,
'ecdsa'
)
// example
INg2ZeG8b6GsiYLiWeQQpvmfFHqCt3zC6ocdlN9ZRQLhSFZdGhgYWF8ipar1wqJtYufxzSYiZm5kdlAcnxgZWQU
=
pushTx
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
okxwallet.bitcoin.pushTx(rawTx)
描述
推送交易
参数
rawTx - string：上链的原始交易
返回值
Promise - string：交易哈希
示例
try
{
let
txid
=
await
okxwallet
.
bitcoin
.
pushTx
(
'0200000000010135bd7d...'
)
;
console
.
log
(
txid
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
splitUtxo
#
此字段当前仅适用于插件端版本，不适用于移动端版本。
okxwallet.bitcoin.splitUtxo({ from, amount })
描述
拆分 UTXO，初始化钱包
拆分是因为
签名算法
需要
参数
object
from - string：当前连接的钱包的 BTC 地址
amount - number： (可选) 拆分的数量，默认值是 2
返回值
Promise -
{utxos: array}
： UTXO 和签名
示例
try
{
let
{
utxos
}
=
await
window
.
okxwallet
.
bitcoin
.
splitUtxo
(
{
from
:
'bc1pkrym02ck30phct287l0rktjjjnapavkl2qhsy78aeeeuk3qaaulqh90v6s'
,
}
)
;
console
.
log
(
utxos
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
// example
{
utxos
:
[
{
txId
:
'1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306'
,
vOut
:
0
,
amount
:
546
,
rawTransaction
:
'xxxx'
,
}
,
{
txId
:
'1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306'
,
vOut
:
1
,
amount
:
546
,
rawTransaction
:
'xxxx'
,
}
,
]
;
}
inscribe
#
此字段当前仅适用于插件端版本，不适用于移动端版本。
okxwallet.bitcoin.inscribe({ type, from, tick, tid })
描述
铭刻可转移的 BRC-20
参数
type - number：交易类型，详情见下表
类型
描述
51
默认值，BRC-20 的转移铭刻
from - string：当前连接的钱包的 BTC 地址
tick - string：BRC-20 的代币名称 (来自于链上)
返回值
Promise - string：揭示交易的哈希
示例
try
{
let
txid
=
await
okxwallet
.
bitcoin
.
inscribe
(
{
from
:
'bc1pkrym02ck30phct287l0rktjjjnapavkl2qhsy78aeeeuk3qaaulqh90v6s'
,
tick
:
'ordi'
,
}
)
;
console
.
log
(
txid
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
mint
#
此字段当前仅适用于插件端版本，不适用于移动端版本。
okxwallet.bitcoin.mint({ type, from, inscriptions })
描述
支持 Ordinal 协议的通用铭刻，支持批量铭刻
参数
type - number：要发送的铭刻交易类型，详情见下表
类型
描述
60
BRC-20 deploy 铭刻
50
BRC-20 mint 铭刻
51
BRC-20 transfer 铭刻
62
图片铭刻，需要将图片转换为图片字节流的 16 进制字符串表示
61
纯文本
from - string：当前连接钱包的 BTC 地址
inscriptions - object[]：铭刻的数组。单个数组项是对象类型，其拥有的字段及其含义，如下表所示：
字段
类型
默认值
描述
contentType
string
"text/plain;charset=utf-8"
所铭刻内容的类型， MIME 类型的值，Ordinals 协议规定，详情可查看：
https://docs.ordinals.com/inscriptions.html
body
string
无
所铭刻的内容
不同铭刻类型传入的 contentType 和 body 入参：
铭刻类型
contentType
body
图片铭刻
"image/png" 、"image/jpeg" 等
需要将图片转换为图片字节流的 16 进制字符串表示
BRC-20
"text/plain;charset=utf-8"
通过 JSON.stringify 转换为字符串即可
纯文本
"text/plain;charset=utf-8"
直接传入纯文本即可
返回值
Promise - object，其拥有的字段及其含义，如下所示：
commitTx - string：铭刻时，commit 交易的哈希值
revealTxs - string[]：铭刻时，reveal 交易的哈希值。如果是批量铭刻，则分别对应于 reveal 交易的哈希值
commitTxFee - number：commit 交易花费的网络费用
revealTxFees - number[]：reveal 交易花费的网络费用。如果是批量铭刻，则分别对应于 reveal 交易的网路费用
commitAddrs - string[]：commit 交易的 to 地址，即代打地址
feeRate - number：铭刻时，网络费率
size - number：铭刻时，铭文的大小
示例
okxwallet
.
bitcoin
.
mint
(
{
type
:
61
,
from
:
'bc1p4k9ghlrynzuum080a4zk6e2my8kjzfhptr5747afzrn7xmmdtj6sgrhd0m'
,
inscriptions
:
[
{
contentType
:
'text/plain;charset=utf-8'
,
body
:
'hello'
}
,
{
contentType
:
'text/plain;charset=utf-8'
,
body
:
'world'
}
]
}
)
// response
{
"commitAddrs"
:
[
"bc1p9trqtf68gfeq3f3hlktaapp0eapufh02ly8dr6swfwffflvncncqwvtuen"
,
"bc1p5ttl7q2mpvfhjq3wqffka4c05sv5jcfphcl5qeuj0pmsx7evfhcqhm60rk"
]
,
"commitTx"
:
"453e126346bbaaef0aaaa208acd3426cd14a39f825bd76cb8d9892957e2a5bda"
,
"revealTxs"
:
[
"526ff04e4ba34617ee28826412bdc8e22484890635320f880c5ec50f10d6b189"
,
"0f65f79456a59b3e0cd4ef00e279d0d6da57582e114eafbada95b51759a845b2"
]
,
"commitTxFee"
:
1379
,
"revealTxFees"
:
[
973
,
973
]
,
feeRate
:
80
,
size
:
546
,
}
signPsbt
#
okxwallet.bitcoin.signPsbt(psbtHex[, options])
描述
签名 psbt，该方法将遍历所有与当前地址匹配的输入进行签名
参数
psbtHex - string：要签名的 psbt 的十六进制字符串
注
构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。
示例：可参考下面的 txInput 和 publicKey。
const
txInputs
:
utxoInput
[
]
=
[
]
;
txInputs
.
push
(
{
txId
:
"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"
,
vOut
:
2
,
amount
:
341474
,
address
:
"tb1q8h8....mjxzny"
,
privateKey
:
"0s79......ldjejke"
,
publicKey
:
"tb1q8h8....mjxzny"
,
bip32Derivation
:
[
{
"masterFingerprint"
:
"a22e8e32"
,
"pubkey"
:
"tb1q8h8....mjxzny"
,
"path"
:
"m/49'/0'/0'/0/0"
,
}
,
]
,
}
)
;
options
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名
注意
对于移动端版本低于 6.51.0 和插件端版本低于 2.77.1 的情况：不支持options，并且 autoFinalized默认为 false。
对于移动端版本为 6.51.0 或更高以及插件端版本为 2.77.1 或更高的情况：支持 options，并且 autoFinalized 是布尔值, 默认为 true。
返回值
Promise - string：已签名 psbt 的十六进制字符串
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
signPsbt
(
'70736274ff01007d....'
,
{
autoFinalized
:
false
,
toSignInputs
:
[
{
index
:
0
,
address
:
'tb1q8h8....mjxzny'
,
}
,
{
index
:
1
,
publicKey
:
'tb1q8h8....mjxzny'
,
sighashTypes
:
[
1
]
,
}
,
{
index
:
2
,
publicKey
:
'02062...8779693f'
,
}
,
]
,
}
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
okxwallet
.
bitcoin
.
signPsbt
(
'xxxxxxxx'
,
{
toSignInputs
:
[
{
index
:
0
,
publicKey
:
'xxxxxx'
,
disableTweakSigner
:
true
}
]
,
autoFinalized
:
false
,
}
)
;
signPsbts
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
okxwallet.bitcoin.signPsbts(psbtHexs[, options])
描述
签署多个 psbt，该方法将遍历所有与当前地址匹配的输入进行签名
参数
psbtHexs - string[]：要签名的 psbt 的十六进制字符串
注
构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。
示例：可参考下面的 txInput 和 publicKey。
const
txInputs
:
utxoInput
[
]
=
[
]
;
txInputs
.
push
(
{
txId
:
"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"
,
vOut
:
2
,
amount
:
341474
,
address
:
"tb1q8h8....mjxzny"
,
privateKey
:
"0s79......ldjejke"
,
publicKey
:
"tb1q8h8....mjxzny"
,
bip32Derivation
:
[
{
"masterFingerprint"
:
"a22e8e32"
,
"pubkey"
:
"tb1q8h8....mjxzny"
,
"path"
:
"m/49'/0'/0'/0/0"
,
}
,
]
,
}
)
;
options - object[]：签署 psbt 的选项
autoFinalized - boolean：签名后是否完成 psbt，默认为 true
toSignInputs - array：
index - number：要签名的输入
address - string：用于签名的相应私钥所对应的地址
publicKey - string：用于签名的相应私钥所对应的公钥
sighashTypes - number[]： (可选) sighashTypes
返回值
Promise - string[]：已签名 psbt 的十六进制字符串
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
signPsbts
(
[
'70736274ff01007d...'
,
'70736274ff01007d...'
,
]
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
pushPsbt
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
okxwallet.bitcoin.pushPsbt(psbtHex)
描述
广播 psbt 交易
参数
psbtHex - string：要推送的 psbt 的十六进制字符串
返回值
Promise - string：交易哈希
示例
try
{
let
res
=
await
okxwallet
.
bitcoin
.
pushPsbt
(
'70736274ff01007d....'
)
;
console
.
log
(
res
)
;
}
catch
(
e
)
{
console
.
log
(
e
)
;
}
sendPsbt
#
此字段当前仅适用于插件端版本，不适用于移动端版本。
okxwallet.bitcoin.sendPsbt(txs, from)
描述
广播 psbt 交易
与 pushPsbt 方法的不同点
sendPsbt
方法支持批量上链，
pushPsbt
方法只支持单个上链
sendPsbt
支持传入
type
参数，使钱包内的交易历史展示更精确，而通过
pushPsbt
方法上链的交易在交易历史展示的比较简单
参数
txs - array：要发布的 psbt 交易
from - string：当前连接钱包的 BTC 地址
类型
描述
52
发送 BRC-20
20
发送 NFT
返回值
Promise - array：交易哈希
示例
okxwallet
.
bitcoin
.
sendPsbt
(
[
{
itemId
:
"xxxxx0"
,
// 批量唯一标识，多笔交易内不重复即可
signedTx
:
'70736274ff01007d....'
,
// 签名串
type
:
52
,
// 类型 BRC-20 传递 52， NFT 传递 20
extJson
:
{
// 拆UTXO的交易，可不传
// NFTID
inscription
:
"885441055c7bb5d1c54863e33f5c3a06e5a14cc4749cb61a9b3ff1dbe52a5bbbi0"
,
}
}
，
{
itemId
:
"xxxxx1"
,
// 批量唯一标识
signedTx
:
'70736274ff01007d....'
,
// 签名串或者要上链的psbt
dependItemId
:
[
'xxxxx0'
]
,
// 依赖的交易itemId，没有依赖的话，这个字段可以不传
type
:
52
,
// 类型 BRC-20 传递 52， NFT 传递 20
extJson
:
{
// NFTID
inscription
:
"885441055c7bb5d1c54863e33f5c3a06e5a14cc4749cb61a9b3ff1dbe52a5bbbi0"
,
}
}
]
,
from
)
// response
[
{
"xxxxx0"
:
"txId1"
}
，
{
"xxxxx1"
:
"txId2"
}
// 失败txId返回空
]
accountChanged
#
此字段仅适用于移动端版本 6.51.0 或更高。
描述
欧易 Web3 钱包允许用户从单个扩展程序或移动应用程序中无缝管理多个账户。每当用户切换账户时，欧易 Web3 钱包都会发出一个
accountChanged
事件
如果用户在已连接到应用程序时更改账户，并且新账户已经将该应用程序列入白名单，那么用户将保持连接状态并且欧易 Web3 钱包将传递新账户的公钥：
用法
window
.
okxwallet
.
bitcoin
.
on
(
'accountChanged'
,
(
addressInfo
)
=>
{
console
.
log
(
addressInfo
)
;
{
"address"
:
"bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq"
,
"publicKey"
:
"4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497"
,
"compressedPublicKey"
:
"034a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497"
}
}
)
;
accountsChanged
#
此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。
描述
每当用户暴露的账户地址发生变化时，就会发出该消息
用法
window
.
okxwallet
.
bitcoin
.
on
(
'accountsChanged'
,
(
accounts
)
=>
{
console
.
log
(
accounts
)
[
// example
'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'
]
;
}
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="provider-api">Provider API<a class="index_header-anchor__Xqb+L" href="#provider-api" style="opacity:0">#</a></h1>
<h2 data-content="什么是 Injected provider API？" id="什么是-injected-provider-api？">什么是 Injected provider API？<a class="index_header-anchor__Xqb+L" href="#什么是-injected-provider-api？" style="opacity:0">#</a></h2>
<p>OKX Injected Providers API 基于 JavaScript 模型，由 OKX 嵌入用户访问网站中。DApp 项目可以通过调用此 API 请求用户账户信息，从用户所连接的区块链中读取数据，并协助用户进行消息和交易的签署。</p>
<h2 data-content="connect" id="connect">connect<a class="index_header-anchor__Xqb+L" href="#connect" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoin.connect()</code></p>
<p><strong>描述</strong></p>
<p>连接钱包</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>address - string：当前账户的地址</li>
<li>publicKey - string：当前账户的公钥</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">connect</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  address<span class="token operator">:</span> <span class="token string">'bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq'</span><span class="token punctuation">,</span>
  publicKey<span class="token operator">:</span> <span class="token string">'4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497'</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="requestAccounts" id="requestaccounts">requestAccounts<a class="index_header-anchor__Xqb+L" href="#requestaccounts" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rtbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rtbf:">此字段仅适用于插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.requestAccounts()</code></p>
<p><strong>描述</strong></p>
<p>请求连接当前账户</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string[]：当前账户的地址</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> accounts <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">requestAccounts</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'connect success'</span><span class="token punctuation">,</span> accounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span><span class="token string">'connect failed'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">[</span><span class="token string">'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="getAccounts" id="getaccounts">getAccounts<a class="index_header-anchor__Xqb+L" href="#getaccounts" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R1jbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R1jbf:">此字段仅适用于插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.getAccounts()</code></p>
<p><strong>描述</strong></p>
<p>获取当前账户地址</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string[]：当前账户地址</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">getAccounts</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">[</span><span class="token string">'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="getNetwork" id="getnetwork">getNetwork<a class="index_header-anchor__Xqb+L" href="#getnetwork" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R29bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R29bf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><ul>
<li>不支持测试网络。</li>
<li>此字段仅适用于插件端版本 2.77.1 或更高。</li>
</ul></div></div></div></div></div>
<p><code>okxwallet.bitcoin.getNetwork()</code></p>
<p><strong>描述</strong></p>
<p>获取网络</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：网络</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">getNetwork</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
livenet<span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="getPublicKey" id="getpublickey">getPublicKey<a class="index_header-anchor__Xqb+L" href="#getpublickey" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R2vbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R2vbf:">此字段仅适用于插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.getPublicKey()</code></p>
<p><strong>描述</strong></p>
<p>获取当前账户的公钥</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：公钥</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">getPublicKey</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
03cbaedc26f03fd3ba02fc936f338e980c9e2172c5e23128877ed46827e935296f
</code></pre></div>
<h2 data-content="getBalance" id="getbalance">getBalance<a class="index_header-anchor__Xqb+L" href="#getbalance" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R3lbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R3lbf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.getBalance()</code></p>
<p><strong>描述</strong></p>
<p>获取 BTC 余额</p>
<p><strong>参数</strong></p>
<p>无</p>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object：<!-- -->
<ul>
<li>confirmed - number：已确认的聪数量</li>
<li>unconfirmed - number：未经确认的聪数量</li>
<li>total - number：总聪量</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">getBalance</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  <span class="token string-property property">"confirmed"</span><span class="token operator">:</span><span class="token number">0</span><span class="token punctuation">,</span>
  <span class="token string-property property">"unconfirmed"</span><span class="token operator">:</span><span class="token number">100000</span><span class="token punctuation">,</span>
  <span class="token string-property property">"total"</span><span class="token operator">:</span><span class="token number">100000</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="getInscriptions" id="getinscriptions">getInscriptions<a class="index_header-anchor__Xqb+L" href="#getinscriptions" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R4bbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R4bbf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.getInscriptions()</code></p>
<p><strong>描述</strong></p>
<p>获取当前账户的铭文列表</p>
<p><strong>参数</strong></p>
<ul>
<li>cursor - number： (可选) 偏移量，从 0 开始，默认值是 0</li>
<li>size - number： (可选) 每页的数量，默认值是 20</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object：<!-- -->
<ul>
<li>total - number：总数</li>
<li>list - object[]：<!-- -->
<ul>
<li>inscriptionId - string：铭文 ID</li>
<li>inscriptionNumber - string： 铭文编号</li>
<li>address - string：铭文地址</li>
<li>outputValue - string：铭文的输出值</li>
<li>contentLength - string：铭文的内容长度</li>
<li>contentType - number：铭文的内容类型</li>
<li>timestamp - number：铭文的区块时间</li>
<li>offset - number：铭文的偏移量</li>
<li>output - string：当前铭文所在 UTXO 的标识</li>
<li>genesisTransaction - string：创世交易的交易 ID</li>
<li>location - string：当前位置的 txid 和 vout</li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R4rbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R4rbf:">目前仅移动端版本不支持以上字段：inscriptionNumber、contentLength、contentType、timestamp、genesisTransaction。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">getInscriptions</span><span class="token punctuation">(</span><span class="token number">0</span><span class="token punctuation">,</span> <span class="token number">20</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  <span class="token string-property property">"total"</span><span class="token operator">:</span><span class="token number">10</span><span class="token punctuation">,</span>
  <span class="token string-property property">"list"</span><span class="token operator">:</span><span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      inscriptionId<span class="token operator">:</span> <span class="token string">'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531i0'</span><span class="token punctuation">,</span>
      inscriptionNumber<span class="token operator">:</span> <span class="token number">55878989</span><span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token string">'bc1q8h8s4zd9y0lkrx334aqnj4ykqs220ss735a3gh'</span><span class="token punctuation">,</span>
      outputValue<span class="token operator">:</span> <span class="token number">546</span><span class="token punctuation">,</span>
      contentLength<span class="token operator">:</span> <span class="token number">53</span><span class="token punctuation">,</span>
      contentType<span class="token operator">:</span> <span class="token string">'text/plain'</span><span class="token punctuation">,</span>
      timestamp<span class="token operator">:</span> <span class="token number">1705406294</span><span class="token punctuation">,</span>
      location<span class="token operator">:</span> <span class="token string">'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531:0:0'</span><span class="token punctuation">,</span>
      output<span class="token operator">:</span> <span class="token string">'6037b17df2f48cf87f6b6e6ff89af416f6f21dd3d3bc9f1832fb1ff560037531:0'</span><span class="token punctuation">,</span>
      offset<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
      genesisTransaction<span class="token operator">:</span> <span class="token string">'02c9eae52923fdb21fe16ee9eb873c7d66fe412a61b75147451d8a47d089def4'</span>
    <span class="token punctuation">}</span>
  <span class="token punctuation">]</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="sendBitcoin" id="sendbitcoin">sendBitcoin<a class="index_header-anchor__Xqb+L" href="#sendbitcoin" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R53bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R53bf:">此字段仅适用于插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.sendBitcoin(toAddress, satoshis, options)</code></p>
<p><strong>描述</strong></p>
<p>发送比特币</p>
<p><strong>参数</strong></p>
<ul>
<li>toAddress - string：发送地址</li>
<li>satoshis - number：1. 发送的聪数量</li>
<li>options - object： (可选)<!-- -->
<ul>
<li>feeRate - number：网络资费率</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise- string：交易哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> txid <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">sendBitcoin</span><span class="token punctuation">(</span>
    <span class="token string">'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'</span><span class="token punctuation">,</span>
    <span class="token number">1000</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>txid<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="send" id="send">send<a class="index_header-anchor__Xqb+L" href="#send" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoin.send({ from, to, value, satBytes })</code></p>
<p><strong>描述</strong></p>
<p>转移比特币 (支持 memo 字段)</p>
<p><strong>参数</strong></p>
<ul>
<li>from - string：当前连接的钱包的 BTC 地址</li>
<li>to - string：接受 BTC 的地址</li>
<li>value - string：发送 BTC 的数量</li>
<li>satBytes - string： (可选) 自定义费率</li>
<li>memo - string： (可选) 指定 outputs OP_RETURN 内容 <a class="items-center" href="https://mempool.space/zh/tx/0cd710b0e2f6364bd7c0a4edfe27f592cabe48904c92e4913ee95421e1519320" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">示例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
<li>memoPos - number： (可选) 指定 outputs OP_RETURN 输出位置，如果传了 memo 则必须传入 memoPos 指定位置，否则 memo 不生效</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>txhash：交易哈希</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">send</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  from<span class="token operator">:</span> <span class="token string">'bc1p4k9ghlrynzuum080a4zk6e2my8kjzfhptr5747afzrn7xmmdtj6sgrhd0m'</span><span class="token punctuation">,</span>
  to<span class="token operator">:</span> <span class="token string">'bc1plklsxq4wtv44dv8nm49fj0gh0zm9zxewm6ayzahrxc8yqtennc2s9udmcd'</span><span class="token punctuation">,</span>
  value<span class="token operator">:</span> <span class="token string">'0.000012'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  txhash<span class="token operator">:</span> <span class="token string">'d153136cd74512b69d24c68b2d2c715c3629e607540c3f6cd3acc1140ca9bf57'</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="sendInscription" id="sendinscription">sendInscription<a class="index_header-anchor__Xqb+L" href="#sendinscription" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R6dbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R6dbf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。此外，移动端版本的 Atomicals 协议目前暂不支持此字段。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.sendInscription(address, inscriptionId, options)</code></p>
<p><strong>描述</strong></p>
<p>发送铭文</p>
<p><strong>参数</strong></p>
<ul>
<li>
<p>address - string：接收者地址</p>
</li>
<li>
<p>inscriptionId - string：铭文 ID + 协议，没有传协议则默认是 Ordinals NFT ，目前仅支持 Ordinals 及 Atomicals 协议</p>
<div class="index_table__kvZz5"><table><thead><tr><th>协议</th><th>描述</th></tr></thead><tbody><tr><td>Ordinals</td><td>Ordinals 协议</td></tr><tr><td>Atomicals</td><td>Atomicals 协议</td></tr></tbody></table></div>
</li>
<li>
<p>options - object： (可选)</p>
<ul>
<li>feeRate - number：自定义费率</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：交易哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 发送 Ordinals NFT</span>
<span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> txid <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">sendInscription</span><span class="token punctuation">(</span>
    <span class="token string">'tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'</span><span class="token punctuation">,</span>
    <span class="token string">'e9b86a063d78cc8a1ed17d291703bcc95bcd521e087ab0c7f1621c9c607def1ai0'</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span> feeRate<span class="token operator">:</span> <span class="token number">15</span> <span class="token punctuation">}</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>
    <span class="token string">'send Ordinal NFT to tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span> txid <span class="token punctuation">}</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 发送 Atomicals NFT</span>
<span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> txid <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">sendInscription</span><span class="token punctuation">(</span>
    <span class="token string">'tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'</span><span class="token punctuation">,</span>
    <span class="token string">'ab12349dca49643fcc55c8e6a685ad0481047139c5b1af5af85387973fc7ceafi0-Atomicals'</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span> feeRate<span class="token operator">:</span> <span class="token number">15</span> <span class="token punctuation">}</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>
    <span class="token string">'send Atomicals NFT to tb1q8h8s4zd9y0lkrx334aqnj4ykqs220ss7mjxzny'</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span> txid <span class="token punctuation">}</span>
  <span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="transferNft" id="transfernft">transferNft<a class="index_header-anchor__Xqb+L" href="#transfernft" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R75bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R75bf:">此字段当前仅适用于插件端版本，不适用于移动端版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.transferNft({ from, to, data })</code></p>
<p><strong>描述</strong></p>
<p>发送铭文</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R7dbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R7dbf:">与 sendInscription 方法的不同点</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p><code>transferNft</code> 方法支持批量转移，<code>sendInscription</code> 方法只支持单个转移</p></div></div></div></div></div>
<p><strong>参数</strong></p>
<ul>
<li>
<p>from - string：当前连接的钱包的 BTC 地址</p>
</li>
<li>
<p>to - string：接受 NFT 的地址</p>
</li>
<li>
<p>data - string | string[]：发送的 NFT tokenId + 协议，如果是数组，则是批量转移多个 NFT ， 没有传协议则默认是 Ordinals NFT ，目前仅支持 Ordinals 及 Atomicals 协议</p>
<div class="index_table__kvZz5"><table><thead><tr><th>协议</th><th>描述</th></tr></thead><tbody><tr><td>Ordinals</td><td>Ordinals 协议</td></tr><tr><td>Atomicals</td><td>Atomicals 协议</td></tr></tbody></table></div>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object<!-- -->
<ul>
<li>txhash - string：交易哈希</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 发送 Ordinals NFT</span>
<span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">transferNft</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token string">'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> <span class="token string">'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'</span><span class="token punctuation">,</span>
    data<span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token string">'2f285ba4c457c98c35dcb008114b96cee7c957f00a6993690efb231f91ccc2d9i0-Ordinals'</span><span class="token punctuation">,</span>
      <span class="token string">'2f2532f59d6e46931bc84e496cc6b45f87966b149b85ed3199265cb845550d58i0-Ordinals'</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  txhash<span class="token operator">:</span> <span class="token string">'df409c3ce3c4d7d840b681fab8a3a5b8e32b1600636cc5409d84d2c06365a5fc'</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token comment">// 发送 Atomicals NFT</span>
<span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">transferNft</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token string">'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'</span><span class="token punctuation">,</span>
    to<span class="token operator">:</span> <span class="token string">'bc1p8qfrmxdlmynr076uu28vlszxavwujwe7dus0r8y9thrnp5lgfh6qu2ctrr'</span><span class="token punctuation">,</span>
    data<span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token string">'ab12349dca49643fcc55c8e6a685ad0481047139c5b1af5af85387973fc7ceafi0-Atomicals'</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  txhash<span class="token operator">:</span> <span class="token string">'df409c3ce3c4d7d840b681fab8a3a5b8e32b1600636cc5409d84d2c06365a5fc'</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="signMessage" id="signmessage">signMessage<a class="index_header-anchor__Xqb+L" href="#signmessage" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoin.signMessage(signStr[, type])</code></p>
<p><strong>描述</strong></p>
<p>签名消息</p>
<p><strong>参数</strong></p>
<ul>
<li>signStr - string：需要签名的数据</li>
<li>type - string： (可选) "ecdsa" | "bip322-simple"，默认值是 "ecdsa"。(请注意：版本低于 6.51.0 的应用仅支持“ecdsa”签名算法，而版本为 6.51.0 或更高的应用可支持所有签名算法类型。)</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：签名结果</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> signStr <span class="token operator">=</span> <span class="token string">'need sign string'</span><span class="token punctuation">;</span>
<span class="token keyword">const</span> result <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">signMessage</span><span class="token punctuation">(</span>signStr<span class="token punctuation">,</span> <span class="token string">'ecdsa'</span><span class="token punctuation">)</span>
<span class="token comment">// example</span>
INg2ZeG8b6GsiYLiWeQQpvmfFHqCt3zC6ocdlN9ZRQLhSFZdGhgYWF8ipar1wqJtYufxzSYiZm5kdlAcnxgZWQU<span class="token operator">=</span>
</code></pre></div>
<h2 data-content="pushTx" id="pushtx">pushTx<a class="index_header-anchor__Xqb+L" href="#pushtx" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R8jbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R8jbf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.pushTx(rawTx)</code></p>
<p><strong>描述</strong></p>
<p>推送交易</p>
<p><strong>参数</strong></p>
<ul>
<li>rawTx - string：上链的原始交易</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：交易哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> txid <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">pushTx</span><span class="token punctuation">(</span><span class="token string">'0200000000010135bd7d...'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>txid<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="splitUtxo" id="splitutxo">splitUtxo<a class="index_header-anchor__Xqb+L" href="#splitutxo" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R99bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R99bf:">此字段当前仅适用于插件端版本，不适用于移动端版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.splitUtxo({ from, amount })</code></p>
<p><strong>描述</strong></p>
<p>拆分 UTXO，初始化钱包</p>
<p>拆分是因为<a class="items-center" href="https://github.com/magicoss/msigner/blob/main/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">签名算法<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>需要</p>
<img alt="split utxo" src="./2ed310e05c4352d85658.png?x-oss-process=image/format,webp" style="margin-top:20px"/>
<p><strong>参数</strong></p>
<ul>
<li>object<!-- -->
<ul>
<li>from - string：当前连接的钱包的 BTC 地址</li>
<li>amount - number： (可选) 拆分的数量，默认值是 2</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - <code>{utxos: array}</code>： UTXO 和签名</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> <span class="token punctuation">{</span> utxos <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token keyword">await</span> window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">splitUtxo</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token string">'bc1pkrym02ck30phct287l0rktjjjnapavkl2qhsy78aeeeuk3qaaulqh90v6s'</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>utxos<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
<span class="token comment">// example</span>
<span class="token punctuation">{</span>
  utxos<span class="token operator">:</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">'1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306'</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">546</span><span class="token punctuation">,</span>
      rawTransaction<span class="token operator">:</span> <span class="token string">'xxxx'</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">'1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306'</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">546</span><span class="token punctuation">,</span>
      rawTransaction<span class="token operator">:</span> <span class="token string">'xxxx'</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="inscribe" id="inscribe">inscribe<a class="index_header-anchor__Xqb+L" href="#inscribe" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Ra3bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Ra3bf:">此字段当前仅适用于插件端版本，不适用于移动端版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.inscribe({ type, from, tick, tid })</code></p>
<p><strong>描述</strong></p>
<p>铭刻可转移的 BRC-20</p>
<p><strong>参数</strong></p>
<ul>
<li>
<p>type - number：交易类型，详情见下表</p>
<div class="index_table__kvZz5"><table><thead><tr><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>51</td><td>默认值，BRC-20 的转移铭刻</td></tr></tbody></table></div>
</li>
<li>
<p>from - string：当前连接的钱包的 BTC 地址</p>
</li>
<li>
<p>tick - string：BRC-20 的代币名称 (来自于链上)</p>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：揭示交易的哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> txid <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">inscribe</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    from<span class="token operator">:</span> <span class="token string">'bc1pkrym02ck30phct287l0rktjjjnapavkl2qhsy78aeeeuk3qaaulqh90v6s'</span><span class="token punctuation">,</span>
    tick<span class="token operator">:</span> <span class="token string">'ordi'</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>txid<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="mint" id="mint">mint<a class="index_header-anchor__Xqb+L" href="#mint" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rapbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rapbf:">此字段当前仅适用于插件端版本，不适用于移动端版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.mint({ type, from, inscriptions })</code></p>
<p><strong>描述</strong></p>
<p>支持 Ordinal 协议的通用铭刻，支持批量铭刻</p>
<p><strong>参数</strong></p>
<ul>
<li>
<p>type - number：要发送的铭刻交易类型，详情见下表</p>
<div class="index_table__kvZz5"><table><thead><tr><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>60</td><td>BRC-20 deploy 铭刻</td></tr><tr><td>50</td><td>BRC-20 mint 铭刻</td></tr><tr><td>51</td><td>BRC-20 transfer 铭刻</td></tr><tr><td>62</td><td>图片铭刻，需要将图片转换为图片字节流的 16 进制字符串表示</td></tr><tr><td>61</td><td>纯文本</td></tr></tbody></table></div>
</li>
<li>
<p>from - string：当前连接钱包的 BTC 地址</p>
</li>
<li>
<p>inscriptions - object[]：铭刻的数组。单个数组项是对象类型，其拥有的字段及其含义，如下表所示：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>字段</th><th>类型</th><th>默认值</th><th>描述</th></tr></thead><tbody><tr><td>contentType</td><td>string</td><td>"text/plain;charset=utf-8"</td><td>所铭刻内容的类型， MIME 类型的值，Ordinals 协议规定，详情可查看：<a class="items-center" href="https://docs.ordinals.com/inscriptions.html" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://docs.ordinals.com/inscriptions.html<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>body</td><td>string</td><td>无</td><td>所铭刻的内容</td></tr></tbody></table></div>
<p>不同铭刻类型传入的 contentType 和 body 入参：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>铭刻类型</th><th>contentType</th><th>body</th></tr></thead><tbody><tr><td>图片铭刻</td><td>"image/png" 、"image/jpeg" 等</td><td>需要将图片转换为图片字节流的 16 进制字符串表示</td></tr><tr><td>BRC-20</td><td>"text/plain;charset=utf-8"</td><td>通过 JSON.stringify 转换为字符串即可</td></tr><tr><td>纯文本</td><td>"text/plain;charset=utf-8"</td><td>直接传入纯文本即可</td></tr></tbody></table></div>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - object，其拥有的字段及其含义，如下所示：<!-- -->
<ul>
<li>commitTx - string：铭刻时，commit 交易的哈希值</li>
<li>revealTxs - string[]：铭刻时，reveal 交易的哈希值。如果是批量铭刻，则分别对应于 reveal 交易的哈希值</li>
<li>commitTxFee - number：commit 交易花费的网络费用</li>
<li>revealTxFees - number[]：reveal 交易花费的网络费用。如果是批量铭刻，则分别对应于 reveal 交易的网路费用</li>
<li>commitAddrs - string[]：commit 交易的 to 地址，即代打地址</li>
<li>feeRate - number：铭刻时，网络费率</li>
<li>size - number：铭刻时，铭文的大小</li>
</ul>
</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">mint</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    type<span class="token operator">:</span> <span class="token number">61</span><span class="token punctuation">,</span>
    from<span class="token operator">:</span> <span class="token string">'bc1p4k9ghlrynzuum080a4zk6e2my8kjzfhptr5747afzrn7xmmdtj6sgrhd0m'</span><span class="token punctuation">,</span>
    inscriptions<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span>
        contentType<span class="token operator">:</span> <span class="token string">'text/plain;charset=utf-8'</span><span class="token punctuation">,</span>
        body<span class="token operator">:</span> <span class="token string">'hello'</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
        contentType<span class="token operator">:</span> <span class="token string">'text/plain;charset=utf-8'</span><span class="token punctuation">,</span>
        body<span class="token operator">:</span> <span class="token string">'world'</span>
    <span class="token punctuation">}</span><span class="token punctuation">]</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span>

<span class="token comment">// response</span>
<span class="token punctuation">{</span>
    <span class="token string-property property">"commitAddrs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"bc1p9trqtf68gfeq3f3hlktaapp0eapufh02ly8dr6swfwffflvncncqwvtuen"</span><span class="token punctuation">,</span>
        <span class="token string">"bc1p5ttl7q2mpvfhjq3wqffka4c05sv5jcfphcl5qeuj0pmsx7evfhcqhm60rk"</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"commitTx"</span><span class="token operator">:</span> <span class="token string">"453e126346bbaaef0aaaa208acd3426cd14a39f825bd76cb8d9892957e2a5bda"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"revealTxs"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token string">"526ff04e4ba34617ee28826412bdc8e22484890635320f880c5ec50f10d6b189"</span><span class="token punctuation">,</span>
        <span class="token string">"0f65f79456a59b3e0cd4ef00e279d0d6da57582e114eafbada95b51759a845b2"</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token string-property property">"commitTxFee"</span><span class="token operator">:</span> <span class="token number">1379</span><span class="token punctuation">,</span>
    <span class="token string-property property">"revealTxFees"</span><span class="token operator">:</span> <span class="token punctuation">[</span>
        <span class="token number">973</span><span class="token punctuation">,</span>
        <span class="token number">973</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
    feeRate<span class="token operator">:</span> <span class="token number">80</span><span class="token punctuation">,</span>
    size<span class="token operator">:</span> <span class="token number">546</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="signPsbt" id="signpsbt">signPsbt<a class="index_header-anchor__Xqb+L" href="#signpsbt" style="opacity:0">#</a></h2>
<p><code>okxwallet.bitcoin.signPsbt(psbtHex[, options])</code></p>
<p><strong>描述</strong></p>
<p>签名 psbt，该方法将遍历所有与当前地址匹配的输入进行签名</p>
<p><strong>参数</strong></p>
<ul>
<li>psbtHex - string：要签名的 psbt 的十六进制字符串</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rbpbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rbpbf:">注</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。</p><p>示例：可参考下面的 txInput 和 publicKey。</p></div></div></div></div></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> txInputs<span class="token operator">:</span> utxoInput<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
txInputs<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">341474</span><span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      privateKey<span class="token operator">:</span> <span class="token string">"0s79......ldjejke"</span><span class="token punctuation">,</span>
      publicKey<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      bip32Derivation<span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
              <span class="token string-property property">"masterFingerprint"</span><span class="token operator">:</span> <span class="token string">"a22e8e32"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"path"</span><span class="token operator">:</span> <span class="token string">"m/49'/0'/0'/0/0"</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>
<p>options</p>
<ul>
<li>
<p>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</p>
</li>
<li>
<p>toSignInputs - array：</p>
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
<li>disableTweakSigner - boolean： (可选) 签名和解锁 Taproot 地址时， 默认使用 tweakSigner 来生成签名，启用此选项允许使用原始私钥进行签名</li>
</ul>
</li>
</ul>
</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rbvbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rbvbf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><ul>
<li>对于移动端版本低于 6.51.0 和插件端版本低于 2.77.1 的情况：不支持options，并且 autoFinalized默认为 false。</li>
<li>对于移动端版本为 6.51.0 或更高以及插件端版本为 2.77.1 或更高的情况：支持 options，并且 autoFinalized 是布尔值, 默认为 true。</li>
</ul></div></div></div></div></div>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：已签名 psbt 的十六进制字符串</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">signPsbt</span><span class="token punctuation">(</span><span class="token string">'70736274ff01007d....'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
    autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
    toSignInputs<span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span>
        address<span class="token operator">:</span> <span class="token string">'tb1q8h8....mjxzny'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
        publicKey<span class="token operator">:</span> <span class="token string">'tb1q8h8....mjxzny'</span><span class="token punctuation">,</span>
        sighashTypes<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token number">1</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">{</span>
        index<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
        publicKey<span class="token operator">:</span> <span class="token string">'02062...8779693f'</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">signPsbt</span><span class="token punctuation">(</span><span class="token string">'xxxxxxxx'</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
  toSignInputs<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token punctuation">{</span> index<span class="token operator">:</span> <span class="token number">0</span><span class="token punctuation">,</span> publicKey<span class="token operator">:</span> <span class="token string">'xxxxxx'</span><span class="token punctuation">,</span> disableTweakSigner<span class="token operator">:</span> <span class="token boolean">true</span> <span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
  autoFinalized<span class="token operator">:</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="signPsbts" id="signpsbts">signPsbts<a class="index_header-anchor__Xqb+L" href="#signpsbts" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rcbbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rcbbf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.signPsbts(psbtHexs[, options])</code></p>
<p><strong>描述</strong></p>
<p>签署多个 psbt，该方法将遍历所有与当前地址匹配的输入进行签名</p>
<p><strong>参数</strong></p>
<ul>
<li>psbtHexs - string[]：要签名的 psbt 的十六进制字符串</li>
</ul>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rcnbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rcnbf:">注</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><p>构建交易生成 psbt (string 类型)，如果遇到 input 地址是 Taproot 类型，需要提供公钥。</p><p>示例：可参考下面的 txInput 和 publicKey。</p></div></div></div></div></div>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">const</span> txInputs<span class="token operator">:</span> utxoInput<span class="token punctuation">[</span><span class="token punctuation">]</span> <span class="token operator">=</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">;</span>
txInputs<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
      txId<span class="token operator">:</span> <span class="token string">"1e0f92720ef34ab75eefc5d691b551fb2f783eac61503a69cdf63eb7305d2306"</span><span class="token punctuation">,</span>
      vOut<span class="token operator">:</span> <span class="token number">2</span><span class="token punctuation">,</span>
      amount<span class="token operator">:</span> <span class="token number">341474</span><span class="token punctuation">,</span>
      address<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      privateKey<span class="token operator">:</span> <span class="token string">"0s79......ldjejke"</span><span class="token punctuation">,</span>
      publicKey<span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
      bip32Derivation<span class="token operator">:</span> <span class="token punctuation">[</span>
          <span class="token punctuation">{</span>
              <span class="token string-property property">"masterFingerprint"</span><span class="token operator">:</span> <span class="token string">"a22e8e32"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"pubkey"</span><span class="token operator">:</span> <span class="token string">"tb1q8h8....mjxzny"</span><span class="token punctuation">,</span>
              <span class="token string-property property">"path"</span><span class="token operator">:</span> <span class="token string">"m/49'/0'/0'/0/0"</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>options - object[]：签署 psbt 的选项<!-- -->
<ul>
<li>autoFinalized - boolean：签名后是否完成 psbt，默认为 true</li>
<li>toSignInputs - array：<!-- -->
<ul>
<li>index - number：要签名的输入</li>
<li>address - string：用于签名的相应私钥所对应的地址</li>
<li>publicKey - string：用于签名的相应私钥所对应的公钥</li>
<li>sighashTypes - number[]： (可选) sighashTypes</li>
</ul>
</li>
</ul>
</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string[]：已签名 psbt 的十六进制字符串</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">signPsbts</span><span class="token punctuation">(</span><span class="token punctuation">[</span>
    <span class="token string">'70736274ff01007d...'</span><span class="token punctuation">,</span>
    <span class="token string">'70736274ff01007d...'</span><span class="token punctuation">,</span>
  <span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="pushPsbt" id="pushpsbt">pushPsbt<a class="index_header-anchor__Xqb+L" href="#pushpsbt" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rd7bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rd7bf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.pushPsbt(psbtHex)</code></p>
<p><strong>描述</strong></p>
<p>广播 psbt 交易</p>
<p><strong>参数</strong></p>
<ul>
<li>psbtHex - string：要推送的 psbt 的十六进制字符串</li>
</ul>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - string：交易哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript"><span class="token keyword">try</span> <span class="token punctuation">{</span>
  <span class="token keyword">let</span> res <span class="token operator">=</span> <span class="token keyword">await</span> okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">pushPsbt</span><span class="token punctuation">(</span><span class="token string">'70736274ff01007d....'</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>res<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span> <span class="token keyword">catch</span> <span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="sendPsbt" id="sendpsbt">sendPsbt<a class="index_header-anchor__Xqb+L" href="#sendpsbt" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rdtbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rdtbf:">此字段当前仅适用于插件端版本，不适用于移动端版本。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><code>okxwallet.bitcoin.sendPsbt(txs, from)</code></p>
<p><strong>描述</strong></p>
<p>广播 psbt 交易</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Re5bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Re5bf:">与 pushPsbt 方法的不同点</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"><ol>
<li><code>sendPsbt</code> 方法支持批量上链，<code>pushPsbt</code> 方法只支持单个上链</li>
<li><code>sendPsbt</code> 支持传入 <code>type</code> 参数，使钱包内的交易历史展示更精确，而通过 <code>pushPsbt</code> 方法上链的交易在交易历史展示的比较简单</li>
</ol></div></div></div></div></div>
<p><strong>参数</strong></p>
<ul>
<li>txs - array：要发布的 psbt 交易</li>
<li>from - string：当前连接钱包的 BTC 地址</li>
</ul>
<div class="index_table__kvZz5"><table><thead><tr><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>52</td><td>发送 BRC-20</td></tr><tr><td>20</td><td>发送 NFT</td></tr></tbody></table></div>
<p><strong>返回值</strong></p>
<ul>
<li>Promise - array：交易哈希</li>
</ul>
<p><strong>示例</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">sendPsbt</span><span class="token punctuation">(</span><span class="token punctuation">[</span><span class="token punctuation">{</span>
    itemId<span class="token operator">:</span> <span class="token string">"xxxxx0"</span><span class="token punctuation">,</span> <span class="token comment">// 批量唯一标识，多笔交易内不重复即可</span>
    signedTx<span class="token operator">:</span> <span class="token string">'70736274ff01007d....'</span><span class="token punctuation">,</span> <span class="token comment">// 签名串</span>
    type<span class="token operator">:</span> <span class="token number">52</span><span class="token punctuation">,</span> <span class="token comment">// 类型 BRC-20 传递 52， NFT 传递 20</span>
    extJson<span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">// 拆UTXO的交易，可不传</span>
        <span class="token comment">// NFTID</span>
         inscription<span class="token operator">:</span><span class="token string">"885441055c7bb5d1c54863e33f5c3a06e5a14cc4749cb61a9b3ff1dbe52a5bbbi0"</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>，<span class="token punctuation">{</span>
    itemId<span class="token operator">:</span> <span class="token string">"xxxxx1"</span><span class="token punctuation">,</span> <span class="token comment">// 批量唯一标识</span>
    signedTx<span class="token operator">:</span> <span class="token string">'70736274ff01007d....'</span><span class="token punctuation">,</span> <span class="token comment">// 签名串或者要上链的psbt</span>
    dependItemId<span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'xxxxx0'</span><span class="token punctuation">]</span><span class="token punctuation">,</span> <span class="token comment">// 依赖的交易itemId，没有依赖的话，这个字段可以不传</span>
    type<span class="token operator">:</span> <span class="token number">52</span><span class="token punctuation">,</span> <span class="token comment">// 类型 BRC-20 传递 52， NFT 传递 20</span>
    extJson<span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token comment">// NFTID</span>
         inscription<span class="token operator">:</span><span class="token string">"885441055c7bb5d1c54863e33f5c3a06e5a14cc4749cb61a9b3ff1dbe52a5bbbi0"</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">]</span><span class="token punctuation">,</span> from<span class="token punctuation">)</span>

<span class="token comment">// response</span>
<span class="token punctuation">[</span>
    <span class="token punctuation">{</span><span class="token string-property property">"xxxxx0"</span><span class="token operator">:</span><span class="token string">"txId1"</span><span class="token punctuation">}</span>，<span class="token punctuation">{</span><span class="token string-property property">"xxxxx1"</span><span class="token operator">:</span><span class="token string">"txId2"</span><span class="token punctuation">}</span>  <span class="token comment">// 失败txId返回空</span>
<span class="token punctuation">]</span>
</code></pre></div>
<h2 data-content="accountChanged" id="accountchanged">accountChanged<a class="index_header-anchor__Xqb+L" href="#accountchanged" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Renbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Renbf:">此字段仅适用于移动端版本 6.51.0 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><strong>描述</strong></p>
<p>欧易 Web3 钱包允许用户从单个扩展程序或移动应用程序中无缝管理多个账户。每当用户切换账户时，欧易 Web3 钱包都会发出一个 <code>accountChanged</code> 事件</p>
<p>如果用户在已连接到应用程序时更改账户，并且新账户已经将该应用程序列入白名单，那么用户将保持连接状态并且欧易 Web3 钱包将传递新账户的公钥：</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'accountChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>addressInfo<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>addressInfo<span class="token punctuation">)</span><span class="token punctuation">;</span>
  <span class="token punctuation">{</span>
    <span class="token string-property property">"address"</span><span class="token operator">:</span> <span class="token string">"bc1pwqye6x35g2n6xpwalywhpsvsu39k3l6086cvdgqazlw9mz2meansz9knaq"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"publicKey"</span><span class="token operator">:</span> <span class="token string">"4a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497"</span><span class="token punctuation">,</span>
    <span class="token string-property property">"compressedPublicKey"</span><span class="token operator">:</span> <span class="token string">"034a627f388196639041ce226c0229560127ef9a5a39d4885123cd82dc82d8b497"</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="accountsChanged" id="accountschanged">accountsChanged<a class="index_header-anchor__Xqb+L" href="#accountschanged" style="opacity:0">#</a></h2>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rf5bf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rf5bf:">此字段仅适用于移动端版本 6.51.0 或更高以及插件端版本 2.77.1 或更高。</div><div class="okui-alert-desc"><div class="index_desc__5fNBE"></div></div></div></div></div>
<p><strong>描述</strong></p>
<p>每当用户暴露的账户地址发生变化时，就会发出该消息</p>
<p><strong>用法</strong></p>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">window<span class="token punctuation">.</span>okxwallet<span class="token punctuation">.</span>bitcoin<span class="token punctuation">.</span><span class="token function">on</span><span class="token punctuation">(</span><span class="token string">'accountsChanged'</span><span class="token punctuation">,</span> <span class="token punctuation">(</span>accounts<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
  <span class="token builtin">console</span><span class="token punctuation">.</span><span class="token function">log</span><span class="token punctuation">(</span>accounts<span class="token punctuation">)</span><span class="token punctuation">[</span>
    <span class="token comment">// example</span>
    <span class="token string">'tb1qrn7tvhdf6wnh790384ahj56u0xaa0kqgautnnz'</span>
  <span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "Bitcoin",
    "Provider API"
  ],
  "sidebar_links": [
    "什么是连接钱包",
    "支持的网络",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Solana 兼容链",
    "TON",
    "SUI",
    "Aptos/Movement",
    "Cosmos 系/Sei",
    "Tron",
    "Starknet",
    "常见问题",
    "接入前提",
    "EVM 兼容链",
    "Bitcoin 兼容链",
    "Provider API",
    "Provider API (Fractal Bitcoin)",
    "Provider API (Testnet)",
    "Provider API (Signet)"
  ],
  "toc": [
    "什么是 Injected provider API？",
    "connect",
    "requestAccounts",
    "getAccounts",
    "getNetwork",
    "getPublicKey",
    "getBalance",
    "getInscriptions",
    "sendBitcoin",
    "send",
    "sendInscription",
    "transferNft",
    "signMessage",
    "pushTx",
    "splitUtxo",
    "inscribe",
    "mint",
    "signPsbt",
    "signPsbts",
    "pushPsbt",
    "sendPsbt",
    "accountChanged",
    "accountsChanged"
  ]
}
```

</details>
