# Javascript 签名 SDK | 钱包签名 SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/private-key-wallet-javascript-sdk#coin-solana  
**抓取时间:** 2025-05-27 02:04:37  
**字数:** 1335

## 导航路径
DEX API > 资源 > Javascript 签名 SDK

## 目录
- 概述
- 安装和构建
- 主要功能
- Packages
- 测试用例
- 支持币种

---

Javascript 签名 SDK
#
概述
#
Js-wallet-sdk 是一个基于 TypeScript/JavaScript 语言的钱包解决方案，包括了各条公链不同的密码学算法和常用功能，可以使用它离线进行私钥、地址的创建，组装交易，以及进行签名等等。本文档将详细介绍如何使用此 SDK。目前，它已经支持各种主流的区块链，每种币种类别都有独立的模块实现，我们将在未来持续增加对更多区块链的支持。
支持平台
#
作为一个 Javascript SDK，它支持各种浏览器和 JavaScript 环境，可以轻松地集成到 Web 应用、移动应用或桌面应用中。
安装和构建
#
NPM 构建
#
要使用签名 SDK，首先需要安装它，你可以使用 npm 安装来获取到最新版本。
我们的签名 SDK 支持两种类型的包：公共包和单币种模块。
公共包，针对所有币种：
npm
install
@okxweb3/crypto-lib
npm
install
@okxweb3/coin-base
集成单个币种，以 ETH 和 BTC 为例：
集成 ETH:
npm
install
@okxweb3/coin-ethereum
集成 BTC:
npm
install
@okxweb3/coin-bitcoin
本地构建
#
在本地构建 SDK：
下载项目源码
git
clone https://github.com/okx/js-wallet-sdk.git
运行构建脚本
sh
build.sh
主要功能
#
以下是签名 SDK 中每个模块的具体功能介绍。
crypto-lib: 这个模块提供了常用的安全加密算法和签名算法等。
coin-base: 这个模块提供了币种通用接口。
coin-*: 这个模块实现了各个币种交易构建和签名的方法。每种币种都有一个对应的模块，例如 coin-ethereum、coin-bitcoin 等。这些模块提供了针对特定币种的交易构建和签名方法。
Packages
#
包名
模块
描述
@okxweb3/coin-base
coin-base
我们为这些链或币种提供通用功能，使得访问这些链变得非常简单。
@okxweb3/crypto-lib
crypto-lib
我们提供关于 bip32、bip39、ecdsa、ed25519 等的通用函数。
@okxweb3/coin-aptos
coin-aptos
Aptos SDK 用于与 Aptos 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-bitcoin
coin-bitcoin
Bitcoin SDK 用于与 Bitcoin 主网或测试网交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 Bitcoin，还支持以下链：BTC,BSV,DOGE,LTC,TBTC
@okxweb3/coin-cosmos
coin-cosmos
Cosmos SDK 用于与 Cosmos 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-eos
coin-eos
EOS SDK 用于与 EOS 区块链交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 EOS，还支持 WAX。
@okxweb3/coin-ethereum
coin-ethereum
Ethereum SDK 用于与Ethereum 区块链或 EVM 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-flow
coin-flow
Flow SDK 用于与 Flow 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-near
coin-near
Near SDK 用于与 Near 协议交互，包含与 Near 生态系统交互时需要的主要函数。
@okxweb3/coin-polkadot
coin-polkadot
Polkadot SDK 用于与 Polkadot 区块链交互，包含与 Polkadot 生态系统交互时需要的主要函数。
@okxweb3/coin-solana
coin-solana
Solana SDK 用于与 Solana 链交互，包含与 Solana 生态系统交互时需要的主要函数。
@okxweb3/coin-stacks
coin-stacks
Stacks SDK 用于与 Stacks 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-starknet
coin-starknet
Starknet SDK 用于与 Starknet 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-sui
coin-sui
SUI SDK 用于与 SUI 区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-tron
coin-tron
TRX SDK 用于与TRON区块链交互，包含可用于 web3 钱包的各种函数。
@okxweb3/coin-zkspace
coin-zkspace
ZKSpace SDK 用于与 ZK 合约交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 ZKSpace，还支持 zkSync。
coin-base
#
base 包是所有币种的公共基础模块，提供币种通用的接口方法定义，例如：随机生成私钥、私钥派生、获取派生路径等。目前，单币种的实现包基本实现了通用的接口方法，不同币种支持的功能函数略有不同，具体可以参考各币种实现包的功能函数说明。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-base
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签名交易
getDerivedPath
获取 bip44 路径
validPrivateKey
验证私钥
signMessage
签名消息
verifyMessage
验证签名消息
ecRecover
恢复签名到公钥
getAddressByPublicKey
通过公钥获取地址
getHardWareRawTransaction
获取硬件的原始交易
getHardWareSignedTransaction
获取硬件的签名交易
getHardWareMessageHash
获取硬件的消息哈希
calcTxHash
通过原始交易获取交易哈希
getRawTransaction
生成原始交易数据
validSignedTransaction
检查签名交易
estimateFee
估计燃气费
关于 coin-base 包支持的功能函数和使用案例，更详细的内容可以查看 github 文档：
coin-base功能函数
。
crypto-lib
#
这是一个包含了 bip32, bip39, ecdsa, ed25519 等常用的安全加密和签名算法的实现，例如：
bip32 常用函数：这些函数主要用于处理和操作比特币改进型支付协议（BIP32）相关的任务。
bip39 生成助记词、公私钥、签名消息函数：这些函数主要用于处理和操作比特币改进型支付协议（BIP39）相关的任务，如生成助记词，公私钥，以及签名消息。
常用的哈希和编解码函数：这些函数主要用于处理常见的哈希和编解码任务，如 SHA256 哈希，Base64 编解码等。
ed5519 常用签名函数：这些函数主要用于处理和操作 ed5519 签名算法相关的任务。
ecds 常用签名函数：这些函数主要用于处理和操作椭圆曲线数字签名算法（ECDSA）相关的任务。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/crypto-lib
关于 crypto-lib 包支持的功能函数和使用案例，更详细的内容可以查看 github 文档：
crypto-lib功能函数
。
coin-aptos
#
Aptos SDK 主要用集成 Aptos 区块链，包含有私钥生成、私钥派生、生成地址、交易转帐等功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-aptos
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成一个随机的私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新的地址
validAddress
验证地址的有效性
signTransaction
对交易进行签名
getDerivedPath
获取 bip44 路径
signMessage
对消息进行签名
verifyMessage
验证签名消息的有效性
calcTxHash
通过原始交易获取交易哈希
validSignedTransaction
检查已签名的交易的有效性
Aptos 交易支持类型有：
"transfer"、"tokenTransfer"、"tokenMint"、"tokenBurn"、"tokenRegister"、"dapp"、"simulate"、"offerNft"、"claimNft"、"offerNft_simulate"、"claimNft_simulate"
关于 coin-aptos 包支持的功能函数和使用案例，可以查看 github 文档以获取更详细的内容：
coin-aptos功能函数
。
coin-bitcoin
#
coin-bitcoin 是一个用于集成 Bitcoin 区块链的 SDK，它支持 Bitcoin 的主网和测试网，并提供了一系列的功能函数，使开发者能够更方便地与 Bitcoin 区块链进行交互。除了 BTC，它还支持 BSV、DOGE、LTC 和 TBTC 等币种。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-bitcoin
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成一个随机的私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新的地址
validAddress
验证地址的有效性
signTransaction
对交易进行签名
getDerivedPath
获取 bip44 路径
signMessage
对消息进行签名
verifyMessage
验证签名消息的有效性
calcTxHash
通过原始交易获取交易哈希
validSignedTransaction
检查已签名的交易的有效性
getAddressByPublicKey
通过公钥获取地址
关于 coin-bitcoin 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-bitcoin功能函数
。
coin-cosmos
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
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-cosmos
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
signMessage
签署消息
verifyMessage
验证签署的消息
calcTxHash
通过原始交易获取交易哈希
validSignedTransaction
检查已签署的交易
getAddressByPublicKey
通过公钥获取地址
关于 coin-cosmos 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-cosmos功能函数
。
coin-eos
#
EOS SDK 是一个用于集成 EOS 区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易序列化等。除了 EOS 外，它还支持 Wax 币种。
这些功能函数使开发者能够更方便地与 EOS 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-eos
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
calcTxHash
通过原始交易获取交易哈希
关于 coin-eos 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-eos功能函数
。
coin-ethereum
#
Ethereum SDK 是一个用于集成 Ethereum 区块链和其他 支持EVM (以太坊虚拟机) 的区块链的工具包。它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。
这些功能函数使开发者能够更方便地与 Ethereum 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-ethereum
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
validPrivateKey
验证私钥
signMessage
签署消息
verifyMessage
验证签署的消息
ecRecover
恢复签名到公钥
getAddressByPublicKey
通过公钥获取地址
getHardWareRawTransaction
获取硬件的原始交易
关于 coin-ethereum 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-ethereum功能函数
。
coin-flow
#
Flow 区块链是一个新一代的、面向未来的区块链平台，它专为高性能应用和游戏而设计。
Flow SDK 是一个用于集成 Flow 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-flow
支持函数：
函数名称
功能
备注
validateAddress
验证地址
signTransaction
签署交易
Flow 交易支持类型有：Account 和 Transfer
关于 coin-flow 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-flow 功能函数
。
coin-near
#
Near 协议是一个可扩展的区块链平台，它通过使用新颖的共识机制和分片技术，实现了高吞吐量和低延迟的交易处理。Near SDK 使开发者能够更方便地开发和部署在 Near 区块链上的应用。
Near SDK 是一个用于集成 Near 协议的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-near
支持函数：
函数名称
功能
备注
getAddress
通过种子获取地址
validateAddress
验证地址
signTransaction
签署交易
transfer
转账
fullAccessKey
获取完全访问密钥
publicKeyFromSeed
从种子获取公钥
关于 coin-near 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-near功能函数
。
coin-polkadot
#
Polkadot 是一个多链异构的区块链平台，它允许各种区块链网络以共享的安全模型并行运行，同时还能实现链与链之间的信息和价值的无缝转移。
Polkadot SDK 是一个用于集成 Polkadot 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-polkadot
支持函数：
函数名称
功能
备注
getAddress
通过种子获取地址
validateAddress
验证地址
SignTx
签署交易
关于 coin-polkadot 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-polkadot 功能函数
。
coin-solana
#
Solana 是一个高性能的区块链平台，它通过创新的共识算法和区块产生机制，实现了高吞吐量和低延迟的交易处理。
Solana SDK 是一个用于集成 Solana 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-solana
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
signMessage
签署消息
calcTxHash
通过原始交易获取交易哈希
validSignedTransaction
检查已签署的交易
getHardWareRawTransaction
获取硬件的原始交易
getHardWareSignedTransaction
获取硬件的已签署交易
getHardWareMessageHash
获取硬件的消息哈希
关于 coin-solana 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-solana功能函数
。
coin-stacks
#
Stacks 是一个开源的区块链平台，它允许开发者在 Stacks 区块链上构建智能合约和去中心化应用。
Stacks SDK 主要用集成 Stacks 区块链，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-stacks
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
signMessage
签署消息
verifyMessage
验证签名消息
calcTxHash
通过原始交易获取交易哈希
getRawTransaction
获取原始交易
关于 coin-stacks 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-stacks 功能函数
。
coin-starknet
#
StarkNet 是一个去中心化的、可扩展的区块链网络，它使用了零知识证明技术来提高交易处理的效率和安全性。
StarkNet SDK 是一个用于集成 StarkNet 区块链的工具包，它提供了一系列的功能函数，使开发者能够更方便地与 StarkNet 区块链进行交互。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-starknet
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
signMessage
签署消息
verifyMessage
验证签名消息
关于 coin-starknet 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-starknet 功能函数
。
coin-sui
#
SUI SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-sui
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
signMessage
签署消息
calcTxHash
通过原始交易获取交易哈希
提示
注意：与 secp256k1 不同的是，ed25519 的私钥派生只支持 hard 模式的派生，详情参见：
https://github.com/satoshilabs/slips/blob/master/slip-0010.md
关于 coin-sui 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-sui 功能函数
。
coin-tron
#
TRON SDK 是一个用于集成 TRON 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-tron
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
validPrivateKey
验证私钥
signMessage
签署消息
verifyMessage
验证签名消息
ecRecover
恢复签名到公钥
getAddressByPublicKey
通过公钥获取地址
getHardWareRawTransaction
获取硬件的原始交易
getHardWareSignedTransaction
获取硬件的签名交易
getHardWareMessageHash
获取硬件的消息哈希
calcTxHash
通过原始交易获取交易哈希
getRawTransaction
生成原始交易数据
validSignedTransaction
检查签名交易
关于 coin-tron 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-tron 功能函数
。
coin-zkspace
#
ZKSpace SDK 主要用集成 ZK 合约，包含多种用于集成 web3 钱包的功能函数，除了 ZKSpace 外，还支持 zkSync。
通过 npm 获取最新版本的包：
npm
install
@okxweb3/coin-zkspace
支持函数：
函数名称
功能
备注
getRandomPrivateKey
生成随机私钥
getDerivedPrivateKey
从 DerivePriKeyParams 生成私钥
getNewAddress
通过私钥获取新地址
validAddress
验证地址
signTransaction
签署交易
getDerivedPath
获取 bip44 路径
validPrivateKey
验证私钥
signMessage
签署消息
verifyMessage
验证签名消息
ecRecover
恢复签名到公钥
getAddressByPublicKey
通过公钥获取地址
getHardWareRawTransaction
获取硬件的原始交易
getHardWareSignedTransaction
获取硬件的签名交易
getHardWareMessageHash
获取硬件的消息哈希
calcTxHash
通过原始交易获取交易哈希
getRawTransaction
生成原始交易数据
交易签名支持 data 类型有：transfer 和 changePubkey
关于 coin-zkspace 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：
coin-zkspace 功能函数
。
测试用例
#
在 github 上，每个模块对应的 package 下有一个
tests
目录，放有各个币种模块的测试用例，可以通过测试用例了解到更多关于 SDK 中函数的用法。
币种
测试用例
备注
BTC
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/tests/btc.test.ts
ETH
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-ethereum/tests/eth.test.ts
Cosmos
https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-cosmos/tests
Aptos
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-aptos/tests/aptos.test.ts
EOS
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-eos/tests/eos.test.ts
Solana
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-solana/tests/sol.test.ts
Stacks
https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-stacks/tests
Starknet
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-starknet/tests/crypto.test.ts
SUI
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-sui/tests/crypto.test.ts
TRON
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-tron/tests/trx.test.ts
ZKSpace
https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-zkspace/tests
Flow
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-flow/tests/flow.test.ts
Near
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-near/tests/near.test.ts
Polkadot
https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-polkadot/tests/dot.test.ts
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
<div class="routes_md__xWlGF"><!--$--><h1 id="javascript-签名-sdk">Javascript 签名 SDK<a class="index_header-anchor__Xqb+L" href="#javascript-签名-sdk" style="opacity:0">#</a></h1>
<h2 data-content="概述" id="概述">概述<a class="index_header-anchor__Xqb+L" href="#概述" style="opacity:0">#</a></h2>
<p>Js-wallet-sdk 是一个基于 TypeScript/JavaScript 语言的钱包解决方案，包括了各条公链不同的密码学算法和常用功能，可以使用它离线进行私钥、地址的创建，组装交易，以及进行签名等等。本文档将详细介绍如何使用此 SDK。目前，它已经支持各种主流的区块链，每种币种类别都有独立的模块实现，我们将在未来持续增加对更多区块链的支持。</p>
<h3 id="支持平台">支持平台<a class="index_header-anchor__Xqb+L" href="#支持平台" style="opacity:0">#</a></h3>
<p>作为一个 Javascript SDK，它支持各种浏览器和 JavaScript 环境，可以轻松地集成到 Web 应用、移动应用或桌面应用中。</p>
<h2 data-content="安装和构建" id="安装和构建">安装和构建<a class="index_header-anchor__Xqb+L" href="#安装和构建" style="opacity:0">#</a></h2>
<h3 id="npm-构建">NPM 构建<a class="index_header-anchor__Xqb+L" href="#npm-构建" style="opacity:0">#</a></h3>
<p>要使用签名 SDK，首先需要安装它，你可以使用 npm 安装来获取到最新版本。</p>
<p>我们的签名 SDK 支持两种类型的包：公共包和单币种模块。</p>
<p>公共包，针对所有币种：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/crypto-lib
<span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-base
</code></pre></div>
<p>集成单个币种，以 ETH 和 BTC 为例：</p>
<p>集成 ETH:</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-ethereum
</code></pre></div>
<p>集成 BTC:</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-bitcoin
</code></pre></div>
<h3 id="本地构建">本地构建<a class="index_header-anchor__Xqb+L" href="#本地构建" style="opacity:0">#</a></h3>
<p>在本地构建 SDK：</p>
<ol>
<li>下载项目源码</li>
</ol>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">git</span> clone https://github.com/okx/js-wallet-sdk.git
</code></pre></div>
<ol start="2">
<li>运行构建脚本</li>
</ol>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">sh</span> build.sh
</code></pre></div>
<h2 data-content="主要功能" id="主要功能">主要功能<a class="index_header-anchor__Xqb+L" href="#主要功能" style="opacity:0">#</a></h2>
<p>以下是签名 SDK 中每个模块的具体功能介绍。</p>
<ul>
<li>crypto-lib: 这个模块提供了常用的安全加密算法和签名算法等。</li>
<li>coin-base: 这个模块提供了币种通用接口。</li>
<li>coin-*: 这个模块实现了各个币种交易构建和签名的方法。每种币种都有一个对应的模块，例如 coin-ethereum、coin-bitcoin 等。这些模块提供了针对特定币种的交易构建和签名方法。</li>
</ul>
<h2 data-content="Packages" id="packages">Packages<a class="index_header-anchor__Xqb+L" href="#packages" style="opacity:0">#</a></h2>
<div class="index_table__kvZz5"><table><thead><tr><th>包名</th><th>模块</th><th>描述</th></tr></thead><tbody><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-base/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-base<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-base</td><td>我们为这些链或币种提供通用功能，使得访问这些链变得非常简单。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/crypto-lib/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/crypto-lib<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>crypto-lib</td><td>我们提供关于 bip32、bip39、ecdsa、ed25519 等的通用函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-aptos/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-aptos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-aptos</td><td>Aptos SDK 用于与 Aptos 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-bitcoin<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-bitcoin</td><td>Bitcoin SDK 用于与 Bitcoin 主网或测试网交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 Bitcoin，还支持以下链：BTC,BSV,DOGE,LTC,TBTC</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-cosmos/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-cosmos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-cosmos</td><td>Cosmos SDK 用于与 Cosmos 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-eos/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-eos<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-eos</td><td>EOS SDK 用于与 EOS 区块链交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 EOS，还支持 WAX。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-ethereum/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-ethereum<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-ethereum</td><td>Ethereum SDK 用于与Ethereum 区块链或 EVM 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-flow/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-flow<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-flow</td><td>Flow SDK 用于与 Flow 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-near/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-near<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-near</td><td>Near SDK 用于与 Near 协议交互，包含与 Near 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-polkadot/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-polkadot<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-polkadot</td><td>Polkadot SDK 用于与 Polkadot 区块链交互，包含与 Polkadot 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-solana/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-solana<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-solana</td><td>Solana SDK 用于与 Solana 链交互，包含与 Solana 生态系统交互时需要的主要函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-stacks/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-stacks<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-stacks</td><td>Stacks SDK 用于与 Stacks 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-starknet/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-starknet<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-starknet</td><td>Starknet SDK 用于与 Starknet 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-sui/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-sui<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-sui</td><td>SUI SDK 用于与 SUI 区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-tron/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-tron<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-tron</td><td>TRX SDK 用于与TRON区块链交互，包含可用于 web3 钱包的各种函数。</td></tr><tr><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-zkspace/README.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">@okxweb3/coin-zkspace<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td>coin-zkspace</td><td>ZKSpace SDK 用于与 ZK 合约交互，包含可用于 web3 钱包的各种函数。SDK 不仅支持 ZKSpace，还支持 zkSync。</td></tr></tbody></table></div>
<h3 id="coin-base">coin-base<a class="index_header-anchor__Xqb+L" href="#coin-base" style="opacity:0">#</a></h3>
<p>base 包是所有币种的公共基础模块，提供币种通用的接口方法定义，例如：随机生成私钥、私钥派生、获取派生路径等。目前，单币种的实现包基本实现了通用的接口方法，不同币种支持的功能函数略有不同，具体可以参考各币种实现包的功能函数说明。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-base
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签名交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>validPrivateKey</td><td>验证私钥</td><td></td></tr><tr><td>signMessage</td><td>签名消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息</td><td></td></tr><tr><td>ecRecover</td><td>恢复签名到公钥</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr><tr><td>getHardWareRawTransaction</td><td>获取硬件的原始交易</td><td></td></tr><tr><td>getHardWareSignedTransaction</td><td>获取硬件的签名交易</td><td></td></tr><tr><td>getHardWareMessageHash</td><td>获取硬件的消息哈希</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>getRawTransaction</td><td>生成原始交易数据</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查签名交易</td><td></td></tr><tr><td>estimateFee</td><td>估计燃气费</td><td></td></tr></tbody></table></div>
<p>关于 coin-base 包支持的功能函数和使用案例，更详细的内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-base/README.md#supporting-functions" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-base功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="crypto-lib">crypto-lib<a class="index_header-anchor__Xqb+L" href="#crypto-lib" style="opacity:0">#</a></h3>
<p>这是一个包含了 bip32, bip39, ecdsa, ed25519 等常用的安全加密和签名算法的实现，例如：</p>
<ul>
<li>bip32 常用函数：这些函数主要用于处理和操作比特币改进型支付协议（BIP32）相关的任务。</li>
<li>bip39 生成助记词、公私钥、签名消息函数：这些函数主要用于处理和操作比特币改进型支付协议（BIP39）相关的任务，如生成助记词，公私钥，以及签名消息。</li>
<li>常用的哈希和编解码函数：这些函数主要用于处理常见的哈希和编解码任务，如 SHA256 哈希，Base64 编解码等。</li>
<li>ed5519 常用签名函数：这些函数主要用于处理和操作 ed5519 签名算法相关的任务。</li>
<li>ecds 常用签名函数：这些函数主要用于处理和操作椭圆曲线数字签名算法（ECDSA）相关的任务。</li>
</ul>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/crypto-lib
</code></pre></div>
<p>关于 crypto-lib 包支持的功能函数和使用案例，更详细的内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/crypto-lib/README.md#provides" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">crypto-lib功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-aptos">coin-aptos<a class="index_header-anchor__Xqb+L" href="#coin-aptos" style="opacity:0">#</a></h3>
<p>Aptos SDK 主要用集成 Aptos 区块链，包含有私钥生成、私钥派生、生成地址、交易转帐等功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-aptos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成一个随机的私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新的地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址的有效性</td><td></td></tr><tr><td>signTransaction</td><td>对交易进行签名</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>对消息进行签名</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息的有效性</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查已签名的交易的有效性</td><td></td></tr></tbody></table></div>
<p>Aptos 交易支持类型有：</p>
<p>"transfer"、"tokenTransfer"、"tokenMint"、"tokenBurn"、"tokenRegister"、"dapp"、"simulate"、"offerNft"、"claimNft"、"offerNft_simulate"、"claimNft_simulate"</p>
<p>关于 coin-aptos 包支持的功能函数和使用案例，可以查看 github 文档以获取更详细的内容：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-aptos/README.md#usage" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-aptos功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-bitcoin">coin-bitcoin<a class="index_header-anchor__Xqb+L" href="#coin-bitcoin" style="opacity:0">#</a></h3>
<p>coin-bitcoin 是一个用于集成 Bitcoin 区块链的 SDK，它支持 Bitcoin 的主网和测试网，并提供了一系列的功能函数，使开发者能够更方便地与 Bitcoin 区块链进行交互。除了 BTC，它还支持 BSV、DOGE、LTC 和 TBTC 等币种。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-bitcoin
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成一个随机的私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新的地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址的有效性</td><td></td></tr><tr><td>signTransaction</td><td>对交易进行签名</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>对消息进行签名</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息的有效性</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查已签名的交易的有效性</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr></tbody></table></div>
<p>关于 coin-bitcoin 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/README.md#using-bitcoin-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-bitcoin功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-cosmos">coin-cosmos<a class="index_header-anchor__Xqb+L" href="#coin-cosmos" style="opacity:0">#</a></h3>
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
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-cosmos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签署的消息</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查已签署的交易</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr></tbody></table></div>
<p>关于 coin-cosmos 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-cosmos/README.md#using-cosmos-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-cosmos功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-eos">coin-eos<a class="index_header-anchor__Xqb+L" href="#coin-eos" style="opacity:0">#</a></h3>
<p>EOS SDK 是一个用于集成 EOS 区块链的工具包，它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易序列化等。除了 EOS 外，它还支持 Wax 币种。</p>
<p>这些功能函数使开发者能够更方便地与 EOS 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-eos
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr></tbody></table></div>
<p>关于 coin-eos 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-eos/README.md#using-eos-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-eos功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-ethereum">coin-ethereum<a class="index_header-anchor__Xqb+L" href="#coin-ethereum" style="opacity:0">#</a></h3>
<p>Ethereum SDK 是一个用于集成 Ethereum 区块链和其他 支持EVM (以太坊虚拟机) 的区块链的工具包。它提供了一系列的功能函数，包括生成私钥、派生私钥、生成地址和交易转账等。</p>
<p>这些功能函数使开发者能够更方便地与 Ethereum 区块链进行交互，包括创建和管理钱包，发送和接收交易，以及查询区块链信息等。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-ethereum
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>validPrivateKey</td><td>验证私钥</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签署的消息</td><td></td></tr><tr><td>ecRecover</td><td>恢复签名到公钥</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr><tr><td>getHardWareRawTransaction</td><td>获取硬件的原始交易</td><td></td></tr></tbody></table></div>
<p>关于 coin-ethereum 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-ethereum/README.md#using-ethereum-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-ethereum功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-flow">coin-flow<a class="index_header-anchor__Xqb+L" href="#coin-flow" style="opacity:0">#</a></h3>
<p>Flow 区块链是一个新一代的、面向未来的区块链平台，它专为高性能应用和游戏而设计。</p>
<p>Flow SDK 是一个用于集成 Flow 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-flow
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>validateAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr></tbody></table></div>
<p>Flow 交易支持类型有：Account 和 Transfer</p>
<p>关于 coin-flow 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-flow/README.md#using-flow-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-flow 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-near">coin-near<a class="index_header-anchor__Xqb+L" href="#coin-near" style="opacity:0">#</a></h3>
<p>Near 协议是一个可扩展的区块链平台，它通过使用新颖的共识机制和分片技术，实现了高吞吐量和低延迟的交易处理。Near SDK 使开发者能够更方便地开发和部署在 Near 区块链上的应用。</p>
<p>Near SDK 是一个用于集成 Near 协议的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-near
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getAddress</td><td>通过种子获取地址</td><td></td></tr><tr><td>validateAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>transfer</td><td>转账</td><td></td></tr><tr><td>fullAccessKey</td><td>获取完全访问密钥</td><td></td></tr><tr><td>publicKeyFromSeed</td><td>从种子获取公钥</td><td></td></tr></tbody></table></div>
<p>关于 coin-near 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-near/README.md#using-near-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-near功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-polkadot">coin-polkadot<a class="index_header-anchor__Xqb+L" href="#coin-polkadot" style="opacity:0">#</a></h3>
<p>Polkadot 是一个多链异构的区块链平台，它允许各种区块链网络以共享的安全模型并行运行，同时还能实现链与链之间的信息和价值的无缝转移。</p>
<p>Polkadot SDK 是一个用于集成 Polkadot 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-polkadot
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getAddress</td><td>通过种子获取地址</td><td></td></tr><tr><td>validateAddress</td><td>验证地址</td><td></td></tr><tr><td>SignTx</td><td>签署交易</td><td></td></tr></tbody></table></div>
<p>关于 coin-polkadot 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-polkadot/README.md#using-polkadot-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-polkadot 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-solana">coin-solana<a class="index_header-anchor__Xqb+L" href="#coin-solana" style="opacity:0">#</a></h3>
<p>Solana 是一个高性能的区块链平台，它通过创新的共识算法和区块产生机制，实现了高吞吐量和低延迟的交易处理。</p>
<p>Solana SDK 是一个用于集成 Solana 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-solana
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查已签署的交易</td><td></td></tr><tr><td>getHardWareRawTransaction</td><td>获取硬件的原始交易</td><td></td></tr><tr><td>getHardWareSignedTransaction</td><td>获取硬件的已签署交易</td><td></td></tr><tr><td>getHardWareMessageHash</td><td>获取硬件的消息哈希</td><td></td></tr></tbody></table></div>
<p>关于 coin-solana 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-solana/README.md#using-solana-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-solana功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-stacks">coin-stacks<a class="index_header-anchor__Xqb+L" href="#coin-stacks" style="opacity:0">#</a></h3>
<p>Stacks 是一个开源的区块链平台，它允许开发者在 Stacks 区块链上构建智能合约和去中心化应用。</p>
<p>Stacks SDK 主要用集成 Stacks 区块链，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-stacks
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>getRawTransaction</td><td>获取原始交易</td><td></td></tr></tbody></table></div>
<p>关于 coin-stacks 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-stacks/README.md#using-stacks-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-stacks 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-starknet">coin-starknet<a class="index_header-anchor__Xqb+L" href="#coin-starknet" style="opacity:0">#</a></h3>
<p>StarkNet 是一个去中心化的、可扩展的区块链网络，它使用了零知识证明技术来提高交易处理的效率和安全性。</p>
<p>StarkNet SDK 是一个用于集成 StarkNet 区块链的工具包，它提供了一系列的功能函数，使开发者能够更方便地与 StarkNet 区块链进行交互。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-starknet
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息</td><td></td></tr></tbody></table></div>
<p>关于 coin-starknet 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-starknet/README.md#using-starknet-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-starknet 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-sui">coin-sui<a class="index_header-anchor__Xqb+L" href="#coin-sui" style="opacity:0">#</a></h3>
<p>SUI SDK 是一个用于集成 SUI 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-sui
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr></tbody></table></div>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":R8fbf:" class="okui-alert info-alert"><i aria-hidden="true" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":R8fbf:">提示</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">注意：与 secp256k1 不同的是，ed25519 的私钥派生只支持 hard 模式的派生，详情参见：<a class="items-center" href="https://github.com/satoshilabs/slips/blob/master/slip-0010.md" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/satoshilabs/slips/blob/master/slip-0010.md<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></div></div></div></div></div>
<p>关于 coin-sui 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-sui/README.md#usage" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-sui 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-tron">coin-tron<a class="index_header-anchor__Xqb+L" href="#coin-tron" style="opacity:0">#</a></h3>
<p>TRON SDK 是一个用于集成 TRON 区块链的工具包，包含多种用于集成 web3 钱包的功能函数。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-tron
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>validPrivateKey</td><td>验证私钥</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息</td><td></td></tr><tr><td>ecRecover</td><td>恢复签名到公钥</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr><tr><td>getHardWareRawTransaction</td><td>获取硬件的原始交易</td><td></td></tr><tr><td>getHardWareSignedTransaction</td><td>获取硬件的签名交易</td><td></td></tr><tr><td>getHardWareMessageHash</td><td>获取硬件的消息哈希</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>getRawTransaction</td><td>生成原始交易数据</td><td></td></tr><tr><td>validSignedTransaction</td><td>检查签名交易</td><td></td></tr></tbody></table></div>
<p>关于 coin-tron 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-tron/README.md#using-trx-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-tron 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h3 id="coin-zkspace">coin-zkspace<a class="index_header-anchor__Xqb+L" href="#coin-zkspace" style="opacity:0">#</a></h3>
<p>ZKSpace SDK 主要用集成 ZK 合约，包含多种用于集成 web3 钱包的功能函数，除了 ZKSpace 外，还支持 zkSync。</p>
<p>通过 npm 获取最新版本的包：</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okxweb3/coin-zkspace
</code></pre></div>
<p>支持函数：</p>
<div class="index_table__kvZz5"><table><thead><tr><th>函数名称</th><th>功能</th><th>备注</th></tr></thead><tbody><tr><td>getRandomPrivateKey</td><td>生成随机私钥</td><td></td></tr><tr><td>getDerivedPrivateKey</td><td>从 DerivePriKeyParams 生成私钥</td><td></td></tr><tr><td>getNewAddress</td><td>通过私钥获取新地址</td><td></td></tr><tr><td>validAddress</td><td>验证地址</td><td></td></tr><tr><td>signTransaction</td><td>签署交易</td><td></td></tr><tr><td>getDerivedPath</td><td>获取 bip44 路径</td><td></td></tr><tr><td>validPrivateKey</td><td>验证私钥</td><td></td></tr><tr><td>signMessage</td><td>签署消息</td><td></td></tr><tr><td>verifyMessage</td><td>验证签名消息</td><td></td></tr><tr><td>ecRecover</td><td>恢复签名到公钥</td><td></td></tr><tr><td>getAddressByPublicKey</td><td>通过公钥获取地址</td><td></td></tr><tr><td>getHardWareRawTransaction</td><td>获取硬件的原始交易</td><td></td></tr><tr><td>getHardWareSignedTransaction</td><td>获取硬件的签名交易</td><td></td></tr><tr><td>getHardWareMessageHash</td><td>获取硬件的消息哈希</td><td></td></tr><tr><td>calcTxHash</td><td>通过原始交易获取交易哈希</td><td></td></tr><tr><td>getRawTransaction</td><td>生成原始交易数据</td><td></td></tr></tbody></table></div>
<p>交易签名支持 data 类型有：transfer 和 changePubkey</p>
<p>关于 coin-zkspace 包支持的功能函数和使用案例，更加详细内容可以查看 github 文档：<a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-zkspace/README.md#using-zkspace-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">coin-zkspace 功能函数<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<h2 data-content="测试用例" id="测试用例">测试用例<a class="index_header-anchor__Xqb+L" href="#测试用例" style="opacity:0">#</a></h2>
<p>在 github 上，每个模块对应的 package 下有一个 <code>tests</code> 目录，放有各个币种模块的测试用例，可以通过测试用例了解到更多关于 SDK 中函数的用法。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>币种</th><th>测试用例</th><th>备注</th></tr></thead><tbody><tr><td>BTC</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/tests/btc.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-bitcoin/tests/btc.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>ETH</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-ethereum/tests/eth.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-ethereum/tests/eth.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Cosmos</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-cosmos/tests" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-cosmos/tests<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Aptos</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-aptos/tests/aptos.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-aptos/tests/aptos.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>EOS</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-eos/tests/eos.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-eos/tests/eos.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Solana</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-solana/tests/sol.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-solana/tests/sol.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Stacks</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-stacks/tests" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-stacks/tests<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Starknet</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-starknet/tests/crypto.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-starknet/tests/crypto.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>SUI</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-sui/tests/crypto.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-sui/tests/crypto.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>TRON</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-tron/tests/trx.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-tron/tests/trx.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>ZKSpace</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-zkspace/tests" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/tree/main/packages/coin-zkspace/tests<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Flow</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-flow/tests/flow.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-flow/tests/flow.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Near</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-near/tests/near.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-near/tests/near.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr><tr><td>Polkadot</td><td><a class="items-center" href="https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-polkadot/tests/dot.test.ts" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/js-wallet-sdk/blob/main/packages/coin-polkadot/tests/dot.test.ts<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></td><td></td></tr></tbody></table></div>
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
    "Javascript 签名 SDK"
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
