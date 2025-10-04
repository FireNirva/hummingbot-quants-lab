# 智能合约交互 | EVM | 连接浏览器插件钱包 | 接入 Web3 钱包 | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/sdks/chains/evm/web-interact-with-smart-contracts#合约-abi  
**抓取时间:** 2025-05-27 06:31:19  
**字数:** 57

## 导航路径
DApp 连接钱包 > EVM > 智能合约交互

## 目录
- 区块链
- 合约地址
- 合约 ABI
- 合约字节码
- 合约源码

---

智能合约交互
#
要与智能合约交互，DApp 需要对应合约部署的：
区块链
地址
ABI
字节码
源码
区块链
#
如果你的合约没有连接到正确的区块链网络，交易将无法发送。许多 DApp 开发人员首先将他们的合同部署到测试网，以避免在主网开发和测试过程中出现问题带来的超额费用。
无论在哪个区块链上部署 DApp，必须确保用户能够访问。以以太坊为例，你可以使用
wallet_addEthereumChain
和
wallet_switchEthereumChain
这些 RPC 方法提示用户添加与切换对应的链。
合约地址
#
无论是外部密钥对账户还是智能合约，每个账户都有一个地址。只有明确合约的确切地址后，才能确保合约库与合约之间的正常交互。
合约 ABI
#
以以太坊为例，
ABI
定义了智能合约与外部系统之间的交互方式，它是一组方法描述对象，当将其与特定的合约地址一起输入到合约库时，ABI 会指示库提供哪些方法，并且指导如何构造事务以调用对应方法。这种机制使得外部应用能够与智能合约的接口对齐，实现与智能合约的交互。在以太坊中，ABI 的主要作用是将函数调用和参数转换为 EVM（以太坊虚拟机）可以理解的数据格式。
示例库包括：
Ethers
web3.js
Embark
ethjs
Truffle
合约字节码
#
如果 DApp 需要部署一个新的预编译智能合约，它需要包含字节码。你必须先发布合约，在交易完成后才能知道合约的具体地址。
即使你是通过字节码发布的合约，你仍然需要一个
ABI
来与合约进行交互。因为字节码本身并不能描述与合约的交互方式。
合约源码
#
如果 DApp 允许用户编辑并编译智能合约的源码（类似于 Remix ），那需要导入一个完整的编译器。通过这种方式，你可以从源码中生成字节码和 ABI ，并在发布后的交易信息中获取到最终的合约地址。

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="智能合约交互">智能合约交互<a class="index_header-anchor__Xqb+L" href="#智能合约交互" style="opacity:0">#</a></h1>
<p>要与智能合约交互，DApp 需要对应合约部署的：</p>
<ul>
<li><a href="#%e5%8c%ba%e5%9d%97%e9%93%be">区块链</a></li>
<li><a href="#%e5%90%88%e7%ba%a6%e5%9c%b0%e5%9d%80">地址</a></li>
<li><a href="#%e5%90%88%e7%ba%a6-abi">ABI</a></li>
<li><a href="#%e5%90%88%e7%ba%a6%e5%ad%97%e8%8a%82%e7%a0%81">字节码</a></li>
<li><a href="#%e5%90%88%e7%ba%a6%e6%ba%90%e7%a0%81">源码</a></li>
</ul>
<h2 data-content="区块链" id="区块链">区块链<a class="index_header-anchor__Xqb+L" href="#区块链" style="opacity:0">#</a></h2>
<p>如果你的合约没有连接到正确的区块链网络，交易将无法发送。许多 DApp 开发人员首先将他们的合同部署到测试网，以避免在主网开发和测试过程中出现问题带来的超额费用。</p>
<p>无论在哪个区块链上部署 DApp，必须确保用户能够访问。以以太坊为例，你可以使用 <a class="items-center" href="https://ethereum-magicians.org/t/eip-3085-wallet-addethereumchain/5469" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank"><code>wallet_addEthereumChain</code><i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 和 <a href="/zh-hans/build/dev-docs/sdks/chains/evm/web-add-network"><code>wallet_switchEthereumChain</code></a> 这些 RPC 方法提示用户添加与切换对应的链。</p>
<h2 data-content="合约地址" id="合约地址">合约地址<a class="index_header-anchor__Xqb+L" href="#合约地址" style="opacity:0">#</a></h2>
<p>无论是外部密钥对账户还是智能合约，每个账户都有一个地址。只有明确合约的确切地址后，才能确保合约库与合约之间的正常交互。</p>
<h2 data-content="合约 ABI" id="合约-abi">合约 ABI<a class="index_header-anchor__Xqb+L" href="#合约-abi" style="opacity:0">#</a></h2>
<p>以以太坊为例，<a class="items-center" href="https://solidity.readthedocs.io/en/develop/abi-spec.html" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">ABI<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> 定义了智能合约与外部系统之间的交互方式，它是一组方法描述对象，当将其与特定的合约地址一起输入到合约库时，ABI 会指示库提供哪些方法，并且指导如何构造事务以调用对应方法。这种机制使得外部应用能够与智能合约的接口对齐，实现与智能合约的交互。在以太坊中，ABI 的主要作用是将函数调用和参数转换为 EVM（以太坊虚拟机）可以理解的数据格式。</p>
<p>示例库包括：</p>
<ul>
<li><a class="items-center" href="https://www.npmjs.com/package/ethers" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Ethers<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
<li><a class="items-center" href="https://www.npmjs.com/package/web3" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">web3.js<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
<li><a class="items-center" href="https://github.com/embarklabs" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Embark<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
<li><a class="items-center" href="https://www.npmjs.com/package/ethjs" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">ethjs<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
<li><a class="items-center" href="https://trufflesuite.com/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">Truffle<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></li>
</ul>
<h2 data-content="合约字节码" id="合约字节码">合约字节码<a class="index_header-anchor__Xqb+L" href="#合约字节码" style="opacity:0">#</a></h2>
<p>如果 DApp 需要部署一个新的预编译智能合约，它需要包含字节码。你必须先发布合约，在交易完成后才能知道合约的具体地址。</p>
<p>即使你是通过字节码发布的合约，你仍然需要一个  <a href="#%e5%90%88%e7%ba%a6-abi">ABI</a> 来与合约进行交互。因为字节码本身并不能描述与合约的交互方式。</p>
<h2 data-content="合约源码" id="合约源码">合约源码<a class="index_header-anchor__Xqb+L" href="#合约源码" style="opacity:0">#</a></h2>
<p>如果 DApp 允许用户编辑并编译智能合约的源码（类似于 Remix ），那需要导入一个完整的编译器。通过这种方式，你可以从源码中生成字节码和 ABI ，并在发布后的交易信息中获取到最终的合约地址。</p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DApp 连接钱包",
    "EVM",
    "智能合约交互"
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
    "获取钱包地址",
    "获取 chainId",
    "添加代币",
    "签名交易",
    "智能合约交互"
  ],
  "toc": [
    "区块链",
    "合约地址",
    "合约 ABI",
    "合约字节码",
    "合约源码"
  ]
}
```

</details>
