# Go 签名 SDK | 钱包签名 SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/private-key-wallet-go-sdk#ethereum-sdk  
**抓取时间:** 2025-05-27 03:17:09  
**字数:** 998

## 导航路径
DEX API > 资源 > Go 签名 SDK

## 目录
- 概述
- 安装和构建
- 主要功能
- Packages
- 测试用例
- 支持币种

---

Go 签名 SDK
#
概述
#
Go-wallet-sdk 是一个基于 Go 语言的钱包解决方案，包括了各条公链不同的密码学算法和常用功能，可以使用它离线进行私钥、地址的创建，组装交易，以及进行签名等等。本文档将详细介绍如何使用此 SDK。目前，它已经支持各种主流的区块链，每种币种类别都有独立的模块实现，我们将在未来持续增加对更多区块链的支持。
支持平台
#
作为一个 Go SDK，可以轻松地集成到 Web 应用、移动应用或桌面应用中。
安装和构建
#
Go GET
#
要使用签名 SDK，首先需要安装它，你可以使用
go get
安装来获取到最新版本。
我们的签名 SDK 支持两种类型的包：公共包和单币种模块。
公共包，针对所有币种：
go get
-u
github.com/okx/go-wallet-sdk/crypto
集成单个币种，以 ETH 和 BTC 为例：
集成 ETH:
go get
-u
github.com/okx/go-wallet-sdk/coins/ethereum
集成 BTC:
go get
-u
github.com/okx/go-wallet-sdk/coins/bitcoin
主要功能
#
以下是签名 SDK 中每个模块的具体功能介绍。
crypto: 这个模块提供了常用的安全加密算法和签名算法等。
coins: 这个模块实现了各个币种交易构建和签名的方法。每种币种都有一个对应的模块，例如 ethereum、bitcoin 等。这些模块提供了针对特定币种的交易构建和签名方法。
Packages
#
包名
模块
描述
github.com/okx/go-wallet-sdk/crypto
crypto
我们提供关于 bip32、bip39、ecdsa、ed25519 等的通用函数。
github.com/okx/go-wallet-sdk/coins/aptos
aptos
Aptos SDK 用于与 Aptos 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/bitcoin
bitcoin
Bitcoin SDK 用于与 Bitcoin 主网或测试网交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 Bitcoin，还支持以下链：BTC, BSV, DOGE, LTC, TBTC。
github.com/okx/go-wallet-sdk/coins/cosmos
cosmos
Cosmos SDK 用于与 Cosmos 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/eos
eos
EOS SDK 用于与 EOS 区块链交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 EOS，还支持 WAX。
github.com/okx/go-wallet-sdk/coins/ethereum
ethereum
Ethereum SDK 用于与 Ethereum 区块链或 EVM 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/flow
flow
Flow SDK 用于与 Flow 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/near
near
Near SDK 用于与 Near 协议交互，包含与 Near 生态系统交互时需要的主要函数。
github.com/okx/go-wallet-sdk/coins/polkadot
polkadot
Polkadot SDK 用于与 Polkadot 区块链交互，包含与 Polkadot 生态系统交互时需要的主要函数。
github.com/okx/go-wallet-sdk/coins/solana
solana
Solana SDK 用于与 Solana 链交互，包含与 Solana 生态系统交互时需要的主要函数。
github.com/okx/go-wallet-sdk/coins/stacks
stacks
Stacks SDK 用于与 Stacks 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/starknet
starknet
Starknet SDK 用于与 Starknet 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/sui
sui
SUI SDK 用于与 SUI 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/tron
tron
TRX SDK 用于与 TRON 区块链交互，包含可用于 web3 钱包的各种函数。
github.com/okx/go-wallet-sdk/coins/zkspace
zkspace
ZKSpace SDK 用于与 ZK 合约交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 ZKSpace，还支持 zkSync。
crypto
#
这是一个包含了 BIP32, BIP39, ECDSA, ED25519 等常用的安全加密和签名算法的实现，例如：
BIP32 常用函数：这些函数主要用于处理和操作比特币改进型支付协议 (BIP32) 相关的任务。
BIP39 生成助记词、公私钥、签名消息函数：这些函数主要用于处理和操作比特币改进型支付协议 (BIP39) 相关的任务，如生成助记词，公私钥，以及签名消息。
常用的哈希和编解码函数：这些函数主要用于处理常见的哈希和编解码任务，如 SHA256 哈希，Base64 编解码等。
ED25519 常用签名函数：这些函数主要用于处理和操作 ED25519 签名算法相关的任务。
ECDSA 常用签名函数：这些函数主要用于处理和操作椭圆曲线数字签名算法 (ECDSA) 相关的任务。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/crypto
aptos-sdk
#
Aptos SDK 主要用集成 Aptos 区块链，包含有私钥生成、私钥派生、生成地址、交易转帐等功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/aptos
支持函数：
函数名称
功能
NewAddress
通过私钥获取新的地址
ValidateAddress
验证地址的有效性
SignRawTransaction
对交易进行签名
Aptos 交易支持类型有：
"transfer"、"tokenTransfer"、"tokenMint"、"tokenBurn"、"tokenRegister"、"dapp"、"simulate"、"offerNft"、"claimNft"、"offerNft_simulate"、"claimNft_simulate"
关于 aptos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
bitcoin-sdk
#
bitcoin-sdk 是一个用于集成 Bitcoin 区块链的 SDK，它支持 Bitcoin 的主网和测试网，并提供了一系列的功能函数，使开发者能够更方便地与 Bitcoin 区块链进行交互。除了 BTC，它还支持 BSV、DOGE、LTC 和 TBTC 等币种。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/bitcoin
支持函数：
函数名称
功能
NewAddress
通过私钥获取新的地址
SignTx
对交易进行签名
GenerateUnsignedPSBTHex
PSBT生成交易
关于 bitcoin-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
cosmos-sdk
#
Cosmos SDK 是一个用于集成 Cosmos 架构的区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。它支持的币种包括：
Atom
Axelar
Cronos
Evmos
Iris
Juno
Kava
Kujira
Osmos
Secret
Sei
Stargaze
Terra
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/cosmos
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
Transfer
签署交易
SignMessage
签署消息
关于 cosmos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
eos-sdk
#
EOS SDK 是一个用于集成 EOS 区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易序列化等。除了 EOS 外，它还支持 WAX 币种。
这些功能函数使开发者能够更方便地与 EOS 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/eos
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
SignTransaction
签署交易
关于 eos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
ethereum-sdk
#
Ethereum SDK 是一个用于集成 Ethereum 区块链和其他支持 EVM（以太坊虚拟机）的区块链的工具包。它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。
这些功能函数使开发者能够更方便地与 Ethereum 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/ethereum
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
SignTransaction
签署交易
SignMessage
签署消息
关于 ethereum-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
flow-sdk
#
Flow 区块链是一个新一代的、面向未来的区块链平台，它专为高性能应用和游戏而设计。
Flow SDK 是一个用于集成 Flow 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/flow
支持函数：
函数名称
功能
CreateNewAccountTx
创建地址
SignTx
签署交易
Flow 交易支持类型有：Account 和 Transfer
关于 flow-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
near-sdk
#
Near 协议是一个可扩展的区块链平台，它通过使用新颖的共识机制和分片技术，实现了高吞吐量和低延迟的交易处理。Near SDK 使开发者能够更方便地开发和部署在 Near 区块链上的应用。
Near SDK 是一个用于集成 Near 协议的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/near
支持函数：
函数名称
功能
NewAccount
通过种子获取地址
SignTransaction
签署交易
关于 near-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
polkadot-sdk
#
Polkadot 是一个多链异构的区块链平台，它允许各种区块链网络以共享的安全模型并行运行，同时还能实现链与链之间的信息和价值的无缝转移。
Polkadot SDK 是一个用于集成 Polkadot 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/polkadot
支持函数：
函数名称
功能
NewAddress
通过种子获取地址
SignTx
签署交易
关于 polkadot-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
solana-sdk
#
Solana 是一个高性能的区块链平台，它通过创新的共识算法和区块产生机制，实现了高吞吐量和低延迟的交易处理。
Solana SDK 是一个用于集成 Solana 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/solana
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
SignTransaction
签署交易
关于 solana-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
stacks-sdk
#
Stacks 是一个开源的区块链平台，它允许开发者在 Bitcoin 区块链上构建智能合约和去中心化应用。
Stacks SDK 主要用集成 Stacks 区块链，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/stacks
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
Transfer
签署交易
关于 stacks-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
starknet-sdk
#
StarkNet 是一个去中心化的、可扩展的区块链网络，它使用了零知识证明技术来提高交易处理的效率和安全性。
StarkNet SDK 是一个用于集成 StarkNet 区块链的工具包，它提供了一系列的功能函数，使开发者能够更方便地与 StarkNet 区块链进行交互。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/starknet
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
CreateSignedContractTx
签署交易
关于 starknet-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
sui-sdk
#
SUI SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/sui
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
SignTransaction
签署交易
SignMessage
签署消息
注意：与 secp256k1 不同的是，ed25519 的私钥派生只支持 hard 模式的派生，详情参见：
https://github.com/satoshilabs/slips/blob/master/slip-0010.md
关于 sui-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
tron-sdk
#
TRON SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/tron
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
SignTransaction
签署交易
关于 tron-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
zkspace-sdk
#
ZKSpace SDK 主要用集成 ZK 合约，包含多种用于集成 web3 钱包的功能函数，除了 ZKSpace 外，还支持 ZKSync。
通过
go get
获取最新版本的包：
go get
-u
github.com/okx/go-wallet-sdk/coins/zkspace
支持函数：
函数名称
功能
NewAddress
通过私钥获取新地址
CreateSignTransferTx
签署交易
交易签名支持 data 类型有：transfer 和 changePubkey
关于 zkspace-sdk 包支持的功能函数和使用案例，更加详细内容可以查看
github
文档。
测试用例
#
在 github 上，每个模块对应的 package 下有一个
tests
目录，放有各个币种模块的测试用例，可以通过测试用例了解到更多关于 SDK 中函数的用法。
币种
测试用例
BTC
测试用例
ETH
测试用例
Cosmos
测试用例
Aptos
测试用例
EOS
测试用例
Solana
测试用例
Stacks
测试用例
Starknet
测试用例
Sui
测试用例
Tron
测试用例
Zkspace
测试用例
Flow
测试用例
Near
测试用例
Polkadot
测试用例
支持币种
#
币族
币种
派生路径
BTC
BTC
常规地址：
m/44'/0'/0/0'/0
隔离见证：
m/49'/0'/0/0'/0
m/84'/0'/0/0'/0
m/86'/0'/0/0'/0
BTC
BCH
m/44'/145'/0'/0/0
BTC
BSV
m/44'/236'/0'/0/0
BTC
LTC
m/44'/2'/0'/0/0
BTC
Doge
m/44'/3'/0'/0/0
BTC
TBTC
m/44'/0'/0/0'/0
BTC
Omni usdt
m/44'/0'/0/0'/0
ETH
ETH
m/44'/60'/0'/0/0
ETH
Arbitrum One
m/44'/60'/0'/0/0
ETH
Arbitrum Nova
m/44'/60'/0'/0/0
ETH
Avalanche C
m/44'/60'/0'/0/0
ETH
Boba
m/44'/60'/0'/0/0
ETH
BNB Chain
m/44'/60'/0'/0/0
ETH
Base
m/44'/60'/0'/0/0
ETH
Core
m/44'/60'/0'/0/0
ETH
Cronos(EVM)
m/44'/60'/0'/0/0
ETH
Celo
m/44'/60'/0'/0/0
ETH
Conflux(EVM)
m/44'/60'/0'/0/0
ETH
Endurance
m/44'/60'/0'/0/0
ETH
EthereumPoW
m/44'/60'/0'/0/0
ETH
EthereumFair
m/44'/60'/0'/0/0
ETH
Filecoin EVM
m/44'/60'/0'/0/0
ETH
Fantom
m/44'/60'/0'/0/0
ETH
Flare
m/44'/60'/0'/0/0
ETH
Gnosis
m/44'/60'/0'/0/0
ETH
Goerli
m/44'/60'/0'/0/0
ETH
HAQQ Network
m/44'/60'/0'/0/0
ETH
Klaytn
m/44'/60'/0'/0/0
ETH
KCC
m/44'/60'/0'/0/0
ETH
Kava EVM
m/44'/60'/0'/0/0
ETH
Linea
m/44'/60'/0'/0/0
ETH
Metis
m/44'/60'/0'/0/0
ETH
Moonebeam
m/44'/60'/0'/0/0
ETH
Moonriver
m/44'/60'/0'/0/0
ETH
Mantle
m/44'/60'/0'/0/0
ETH
Omega Network
m/44'/60'/0'/0/0
ETH
OKTC
m/44'/60'/0'/0/0
ETH
Optimism
m/44'/60'/0'/0/0
ETH
opBNB
m/44'/60'/0'/0/0
ETH
Polygon
m/44'/60'/0'/0/0
ETH
Polygon zkEVM
m/44'/60'/0'/0/0
ETH
PulseChain
m/44'/60'/0'/0/0
ETH
Sepolia
m/44'/60'/0'/0/0
ETH
zkSync Era
m/44'/60'/0'/0/0
ETH
ZetaChian
m/44'/60'/0'/0/0
Cosmos
Atom
m/44'/118'/0'/0/0
Cosmos
Axelar
m/44'/118'/0'/0/0
Cosmos
Cronos
m/44'/394'/0'/0/0
Cosmos
Osmos
m/44'/118'/0'/0/0
Cosmos
Evmos
m/44'/60'/0'/0/0
Cosmos
Iris
m/44'/118'/0'/0/0
Cosmos
Juno
m/44'/118'/0'/0/0
Cosmos
Kava
m/44'/459'/0'/0/0
Cosmos
Kujira
m/44'/118'/0'/0/0
Cosmos
Secret
m/44'/529'/0'/0/0
Cosmos
Sei
m/44'/118'/0'/0/0
Cosmos
Stargaze
m/44'/118'/0'/0/0
Cosmos
Terra
m/44'/330'/0'/0/0
Aptos
Aptos
m/44'/637'/0'/0/0
EOS
EOS
m/44'/194'/0'/0/0
Solana
Solana
m/44'/501'/0'/0/0
Stacks
Stacks
m/44'/5757'/0'/0/0
ETH layer 2
Starknet
m/44'/9004'/0'/0/0
SUI
SUI
m/44'/784'/0'/0/0
TRX
TRON
m/44'/195'/0'/0/0
ETH layer 2
ZKSpace
m/44'/60'/0'/0/0
ETH layer 2
zkSync
m/44'/60'/0'/0/0

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="go-签名-sdk">Go 签名 SDK<a class="index_header-anchor__Xqb+L" href="#go-签名-sdk" style="opacity:0">#</a></h1>
<h2 data-content="概述" id="概述">概述<a class="index_header-anchor__Xqb+L" href="#概述" style="opacity:0">#</a></h2>
<p>Go-wallet-sdk 是一个基于 Go 语言的钱包解决方案，包括了各条公链不同的密码学算法和常用功能，可以使用它离线进行私钥、地址的创建，组装交易，以及进行签名等等。本文档将详细介绍如何使用此 SDK。目前，它已经支持各种主流的区块链，每种币种类别都有独立的模块实现，我们将在未来持续增加对更多区块链的支持。</p>
<h3 id="支持平台">支持平台<a class="index_header-anchor__Xqb+L" href="#支持平台" style="opacity:0">#</a></h3>
<p>作为一个 Go SDK，可以轻松地集成到 Web 应用、移动应用或桌面应用中。</p>
<h2 data-content="安装和构建" id="安装和构建">安装和构建<a class="index_header-anchor__Xqb+L" href="#安装和构建" style="opacity:0">#</a></h2>
<h3 id="go-get">Go GET<a class="index_header-anchor__Xqb+L" href="#go-get" style="opacity:0">#</a></h3>
<p>要使用签名 SDK，首先需要安装它，你可以使用 <code>go get</code> 安装来获取到最新版本。</p>
<p>我们的签名 SDK 支持两种类型的包：公共包和单币种模块。</p>
<p>公共包，针对所有币种：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/crypto
</code></pre></div>
<p>集成单个币种，以 ETH 和 BTC 为例：</p>
<p>集成 ETH:</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/ethereum
</code></pre></div>
<p>集成 BTC:</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/bitcoin
</code></pre></div>
<h2 data-content="主要功能" id="主要功能">主要功能<a class="index_header-anchor__Xqb+L" href="#主要功能" style="opacity:0">#</a></h2>
<p>以下是签名 SDK 中每个模块的具体功能介绍。</p>
<ul>
<li>crypto: 这个模块提供了常用的安全加密算法和签名算法等。</li>
<li>coins: 这个模块实现了各个币种交易构建和签名的方法。每种币种都有一个对应的模块，例如 ethereum、bitcoin 等。这些模块提供了针对特定币种的交易构建和签名方法。</li>
</ul>
<h2 data-content="Packages" id="packages">Packages<a class="index_header-anchor__Xqb+L" href="#packages" style="opacity:0">#</a></h2>
<div class="index_table__kvZz5"><table><thead><tr><th>包名</th><th>模块</th><th>描述</th></tr></thead><tbody><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/crypto" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/crypto<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>crypto</td><td>我们提供关于 bip32、bip39、ecdsa、ed25519 等的通用函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/aptos" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/aptos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>aptos</td><td>Aptos SDK 用于与 Aptos 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/bitcoin" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/bitcoin<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>bitcoin</td><td>Bitcoin SDK 用于与 Bitcoin 主网或测试网交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 Bitcoin，还支持以下链：BTC, BSV, DOGE, LTC, TBTC。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/cosmos" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/cosmos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>cosmos</td><td>Cosmos SDK 用于与 Cosmos 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/eos" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/eos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>eos</td><td>EOS SDK 用于与 EOS 区块链交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 EOS，还支持 WAX。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/ethereum" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/ethereum<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>ethereum</td><td>Ethereum SDK 用于与 Ethereum 区块链或 EVM 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/flow" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/flow<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>flow</td><td>Flow SDK 用于与 Flow 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/near" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/near<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>near</td><td>Near SDK 用于与 Near 协议交互，包含与 Near 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/polkadot" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/polkadot<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>polkadot</td><td>Polkadot SDK 用于与 Polkadot 区块链交互，包含与 Polkadot 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/solana" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/solana<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>solana</td><td>Solana SDK 用于与 Solana 链交互，包含与 Solana 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/stacks" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/stacks<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>stacks</td><td>Stacks SDK 用于与 Stacks 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/starknet" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/starknet<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>starknet</td><td>Starknet SDK 用于与 Starknet 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/sui" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/sui<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>sui</td><td>SUI SDK 用于与 SUI 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/tron" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/tron<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>tron</td><td>TRX SDK 用于与 TRON 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/zkspace" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github.com/okx/go-wallet-sdk/coins/zkspace<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>zkspace</td><td>ZKSpace SDK 用于与 ZK 合约交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 ZKSpace，还支持 zkSync。</td></tr></tbody></table></div>
<h3 id="crypto">crypto<a class="index_header-anchor__Xqb+L" href="#crypto" style="opacity:0">#</a></h3>
<p>这是一个包含了 BIP32, BIP39, ECDSA, ED25519 等常用的安全加密和签名算法的实现，例如：</p>
<ul>
<li>BIP32 常用函数：这些函数主要用于处理和操作比特币改进型支付协议 (BIP32) 相关的任务。</li>
<li>BIP39 生成助记词、公私钥、签名消息函数：这些函数主要用于处理和操作比特币改进型支付协议 (BIP39) 相关的任务，如生成助记词，公私钥，以及签名消息。</li>
<li>常用的哈希和编解码函数：这些函数主要用于处理常见的哈希和编解码任务，如 SHA256 哈希，Base64 编解码等。</li>
<li>ED25519 常用签名函数：这些函数主要用于处理和操作 ED25519 签名算法相关的任务。</li>
<li>ECDSA 常用签名函数：这些函数主要用于处理和操作椭圆曲线数字签名算法 (ECDSA) 相关的任务。</li>
</ul>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/crypto
</code></pre></div>
<h3 id="aptos-sdk">aptos-sdk<a class="index_header-anchor__Xqb+L" href="#aptos-sdk" style="opacity:0">#</a></h3>
<p>Aptos SDK 主要用集成 Aptos 区块链，包含有私钥生成、私钥派生、生成地址、交易转帐等功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/aptos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新的地址</td></tr><tr><td>ValidateAddress</td><td>验证地址的有效性</td></tr><tr><td>SignRawTransaction</td><td>对交易进行签名</td></tr></tbody></table></div>
<p>Aptos 交易支持类型有：</p>
<p>"transfer"、"tokenTransfer"、"tokenMint"、"tokenBurn"、"tokenRegister"、"dapp"、"simulate"、"offerNft"、"claimNft"、"offerNft_simulate"、"claimNft_simulate"</p>
<p>关于 aptos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/aptos/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="bitcoin-sdk">bitcoin-sdk<a class="index_header-anchor__Xqb+L" href="#bitcoin-sdk" style="opacity:0">#</a></h3>
<p>bitcoin-sdk 是一个用于集成 Bitcoin 区块链的 SDK，它支持 Bitcoin 的主网和测试网，并提供了一系列的功能函数，使开发者能够更方便地与 Bitcoin 区块链进行交互。除了 BTC，它还支持 BSV、DOGE、LTC 和 TBTC 等币种。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/bitcoin
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新的地址</td></tr><tr><td>SignTx</td><td>对交易进行签名</td></tr><tr><td>GenerateUnsignedPSBTHex</td><td>PSBT生成交易</td></tr></tbody></table></div>
<p>关于 bitcoin-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/bitcoin" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="cosmos-sdk">cosmos-sdk<a class="index_header-anchor__Xqb+L" href="#cosmos-sdk" style="opacity:0">#</a></h3>
<p>Cosmos SDK 是一个用于集成 Cosmos 架构的区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。它支持的币种包括：</p>
<ul>
<li>Atom</li>
<li>Axelar</li>
<li>Cronos</li>
<li>Evmos</li>
<li>Iris</li>
<li>Juno</li>
<li>Kava</li>
<li>Kujira</li>
<li>Osmos</li>
<li>Secret</li>
<li>Sei</li>
<li>Stargaze</li>
<li>Terra</li>
</ul>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/cosmos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>Transfer</td><td>签署交易</td></tr><tr><td>SignMessage</td><td>签署消息</td></tr></tbody></table></div>
<p>关于 cosmos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/cosmos" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="eos-sdk">eos-sdk<a class="index_header-anchor__Xqb+L" href="#eos-sdk" style="opacity:0">#</a></h3>
<p>EOS SDK 是一个用于集成 EOS 区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易序列化等。除了 EOS 外，它还支持 WAX 币种。
这些功能函数使开发者能够更方便地与 EOS 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/eos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 eos-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/eos" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="ethereum-sdk">ethereum-sdk<a class="index_header-anchor__Xqb+L" href="#ethereum-sdk" style="opacity:0">#</a></h3>
<p>Ethereum SDK 是一个用于集成 Ethereum 区块链和其他支持 EVM（以太坊虚拟机）的区块链的工具包。它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。
这些功能函数使开发者能够更方便地与 Ethereum 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/ethereum
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr><tr><td>SignMessage</td><td>签署消息</td></tr></tbody></table></div>
<p>关于 ethereum-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/ethereum" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="flow-sdk">flow-sdk<a class="index_header-anchor__Xqb+L" href="#flow-sdk" style="opacity:0">#</a></h3>
<p>Flow 区块链是一个新一代的、面向未来的区块链平台，它专为高性能应用和游戏而设计。
Flow SDK 是一个用于集成 Flow 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/flow
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>CreateNewAccountTx</td><td>创建地址</td></tr><tr><td>SignTx</td><td>签署交易</td></tr></tbody></table></div>
<p>Flow 交易支持类型有：Account 和 Transfer</p>
<p>关于 flow-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/flow" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="near-sdk">near-sdk<a class="index_header-anchor__Xqb+L" href="#near-sdk" style="opacity:0">#</a></h3>
<p>Near 协议是一个可扩展的区块链平台，它通过使用新颖的共识机制和分片技术，实现了高吞吐量和低延迟的交易处理。Near SDK 使开发者能够更方便地开发和部署在 Near 区块链上的应用。
Near SDK 是一个用于集成 Near 协议的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/near
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAccount</td><td>通过种子获取地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 near-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/near" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="polkadot-sdk">polkadot-sdk<a class="index_header-anchor__Xqb+L" href="#polkadot-sdk" style="opacity:0">#</a></h3>
<p>Polkadot 是一个多链异构的区块链平台，它允许各种区块链网络以共享的安全模型并行运行，同时还能实现链与链之间的信息和价值的无缝转移。
Polkadot SDK 是一个用于集成 Polkadot 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/polkadot
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过种子获取地址</td></tr><tr><td>SignTx</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 polkadot-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/polkadot" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="solana-sdk">solana-sdk<a class="index_header-anchor__Xqb+L" href="#solana-sdk" style="opacity:0">#</a></h3>
<p>Solana 是一个高性能的区块链平台，它通过创新的共识算法和区块产生机制，实现了高吞吐量和低延迟的交易处理。
Solana SDK 是一个用于集成 Solana 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/solana
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 solana-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/solana" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="stacks-sdk">stacks-sdk<a class="index_header-anchor__Xqb+L" href="#stacks-sdk" style="opacity:0">#</a></h3>
<p>Stacks 是一个开源的区块链平台，它允许开发者在 Bitcoin 区块链上构建智能合约和去中心化应用。
Stacks SDK 主要用集成 Stacks 区块链，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/stacks
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>Transfer</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 stacks-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/stacks" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="starknet-sdk">starknet-sdk<a class="index_header-anchor__Xqb+L" href="#starknet-sdk" style="opacity:0">#</a></h3>
<p>StarkNet 是一个去中心化的、可扩展的区块链网络，它使用了零知识证明技术来提高交易处理的效率和安全性。
StarkNet SDK 是一个用于集成 StarkNet 区块链的工具包，它提供了一系列的功能函数，使开发者能够更方便地与 StarkNet 区块链进行交互。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/starknet
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>CreateSignedContractTx</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 starknet-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/starknet" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="sui-sdk">sui-sdk<a class="index_header-anchor__Xqb+L" href="#sui-sdk" style="opacity:0">#</a></h3>
<p>SUI SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/sui
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr><tr><td>SignMessage</td><td>签署消息</td></tr></tbody></table></div>
<p>注意：与 secp256k1 不同的是，ed25519 的私钥派生只支持 hard 模式的派生，详情参见：<a class="items-center" href="https://github.com/satoshilabs/slips/blob/master/slip-0010.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/satoshilabs/slips/blob/master/slip-0010.md<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></p>
<p>关于 sui-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/sui" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="tron-sdk">tron-sdk<a class="index_header-anchor__Xqb+L" href="#tron-sdk" style="opacity:0">#</a></h3>
<p>TRON SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/tron
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>SignTransaction</td><td>签署交易</td></tr></tbody></table></div>
<p>关于 tron-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/tron" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h3 id="zkspace-sdk">zkspace-sdk<a class="index_header-anchor__Xqb+L" href="#zkspace-sdk" style="opacity:0">#</a></h3>
<p>ZKSpace SDK 主要用集成 ZK 合约，包含多种用于集成 web3 钱包的功能函数，除了 ZKSpace 外，还支持 ZKSync。</p>
<p>通过 <code>go get</code> 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash">go get <span class="token parameter variable">-u</span> github.com/okx/go-wallet-sdk/coins/zkspace
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th></tr></thead><tbody><tr><td>NewAddress</td><td>通过私钥获取新地址</td></tr><tr><td>CreateSignTransferTx</td><td>签署交易</td></tr></tbody></table></div>
<p>交易签名支持 data 类型有：transfer 和 changePubkey</p>
<p>关于 zkspace-sdk 包支持的功能函数和使用案例，更加详细内容可以查看 <a class="items-center" href="https://github.com/okx/go-wallet-sdk/tree/main/coins/zkspace" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">github<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 文档。</p>
<h2 data-content="测试用例" id="测试用例">测试用例<a class="index_header-anchor__Xqb+L" href="#测试用例" style="opacity:0">#</a></h2>
<p>在 github 上，每个模块对应的 package 下有一个 <code>tests</code> 目录，放有各个币种模块的测试用例，可以通过测试用例了解到更多关于 SDK 中函数的用法。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>币种</th><th>测试用例</th></tr></thead><tbody><tr><td>BTC</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/bitcoin/psbt_tx_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>ETH</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/ethereum/eth_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Cosmos</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/cosmos/atom/atom_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Aptos</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/aptos/aptos_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>EOS</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/eos/tx_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Solana</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/solana/sol_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Stacks</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/stacks/stack_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Starknet</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/starknet/account_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Sui</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/sui/sui_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Tron</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/tron/tron_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Zkspace</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/zkspace/account_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Flow</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/flow/account_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Near</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/near/transaction_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr><tr><td>Polkadot</td><td><a class="items-center" href="https://github.com/okx/go-wallet-sdk/blob/main/coins/polkadot/polkadot_test.go" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">测试用例<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td></tr></tbody></table></div>
<h2 data-content="支持币种" id="支持币种">支持币种<a class="index_header-anchor__Xqb+L" href="#支持币种" style="opacity:0">#</a></h2>
<div class="index_table__kvZz5"><table><thead><tr><th>币族</th><th>币种</th><th>派生路径</th></tr></thead><tbody><tr><td>BTC</td><td>BTC</td><td>常规地址： <br/> m/44'/0'/0/0'/0  <br/> 隔离见证： <br/>  m/49'/0'/0/0'/0 <br/>  m/84'/0'/0/0'/0 <br/>  m/86'/0'/0/0'/0</td></tr><tr><td>BTC</td><td>BCH</td><td>m/44'/145'/0'/0/0</td></tr><tr><td>BTC</td><td>BSV</td><td>m/44'/236'/0'/0/0</td></tr><tr><td>BTC</td><td>LTC</td><td>m/44'/2'/0'/0/0</td></tr><tr><td>BTC</td><td>Doge</td><td>m/44'/3'/0'/0/0</td></tr><tr><td>BTC</td><td>TBTC</td><td>m/44'/0'/0/0'/0</td></tr><tr><td>BTC</td><td>Omni usdt</td><td>m/44'/0'/0/0'/0</td></tr><tr><td>ETH</td><td>ETH</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Arbitrum One</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Arbitrum Nova</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Avalanche C</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Boba</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>BNB Chain</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Base</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Core</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Cronos(EVM)</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Celo</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Conflux(EVM)</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Endurance</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>EthereumPoW</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>EthereumFair</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Filecoin EVM</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Fantom</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Flare</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Gnosis</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Goerli</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>HAQQ Network</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Klaytn</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>KCC</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Kava EVM</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Linea</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Metis</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Moonebeam</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Moonriver</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Mantle</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Omega Network</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>OKTC</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Optimism</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>opBNB</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Polygon</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Polygon zkEVM</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>PulseChain</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>Sepolia</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>zkSync Era</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH</td><td>ZetaChian</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Atom</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Axelar</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Cronos</td><td>m/44'/394'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Osmos</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Evmos</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Iris</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Juno</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Kava</td><td>m/44'/459'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Kujira</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Secret</td><td>m/44'/529'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Sei</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Stargaze</td><td>m/44'/118'/0'/0/0</td></tr><tr><td>Cosmos</td><td>Terra</td><td>m/44'/330'/0'/0/0</td></tr><tr><td>Aptos</td><td>Aptos</td><td>m/44'/637'/0'/0/0</td></tr><tr><td>EOS</td><td>EOS</td><td>m/44'/194'/0'/0/0</td></tr><tr><td>Solana</td><td>Solana</td><td>m/44'/501'/0'/0/0</td></tr><tr><td>Stacks</td><td>Stacks</td><td>m/44'/5757'/0'/0/0</td></tr><tr><td>ETH layer 2</td><td>Starknet</td><td>m/44'/9004'/0'/0/0</td></tr><tr><td>SUI</td><td>SUI</td><td>m/44'/784'/0'/0/0</td></tr><tr><td>TRX</td><td>TRON</td><td>m/44'/195'/0'/0/0</td></tr><tr><td>ETH layer 2</td><td>ZKSpace</td><td>m/44'/60'/0'/0/0</td></tr><tr><td>ETH layer 2</td><td>zkSync</td><td>m/44'/60'/0'/0/0</td></tr></tbody></table></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "资源",
    "Go 签名 SDK"
  ],
  "sidebar_links": [
    "介绍",
    "EVM 示例",
    "Solana 示例",
    "Sui 示例",
    "Javascript 签名 SDK",
    "Go 签名 SDK"
  ],
  "toc": [
    "概述",
    "安装和构建",
    "主要功能",
    "Packages",
    "测试用例",
    "支持币种"
  ]
}
```

</details>
