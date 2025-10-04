# 智能合约 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-crosschain-smart-contract#智能合约  
**抓取时间:** 2025-05-27 00:43:58  
**字数:** 104

## 导航路径
DEX API > 交易 API > 智能合约

## 目录
- 二进制合约接口文件 (ABI)

---

智能合约
#
欧易 DEX router 合约地址及 ABI
DEX router 地址和授权合约地址将会由于合约升级而被替换。为避免影响 API 的正常使用，建议使用
/approve-transaction
API 和
/build-tx
API 响应参数中的合约地址执行授权或交易操作。
DEX router 合约地址
#
用于签名交易的欧易 DEX router 地址，请查看
这里
获取详情。
币种授权合约地址
#
用于 ERC-20 代币授权的合约地址，请查看
这里
获取详情。
DEX XBridge 合约地址
#
用于签名跨链交易的欧易 DEX XBridge 合约地址
链名称
DEX XBridge合约地址
Ethereum
0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f
BNB Chain
0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f
OKTC
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Polygon
0x89f423567c2648BB828c3997f60c47b54f57Fa6e
Fantom
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Arbitrum
0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f
Optimism
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Cronos
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Avalanche C
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
TRON
TVaV2BBs8tpthbp19QAy7ibmXLoYsomKDD
Solana
okxBd18urPbBi2vsExxUDArzQNcju2DugV9Mt46BxYE
zkSync Era
0x4040bEC373F6e8be2F913324de94A7b9242E5E92
Polygon zkEvm
0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD
Linea
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Mantle
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Base
0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD
Manta
0x91EcECC4F2363770c621a8a061A80d67cfEafEC7
Metis
0xa50FD06d2b099a4B06d54177C7d3AB08D3D3F004
SUI
0x3d097b26cd6a13a0c37e983e81be72cd2965c4dc717a03471e3a7388c21c9263
Scroll
0xf956D9FA19656D8e5219fd6fa8bA6cb198094138
Starknet
0x00e704db07356df9a2ba8cd2a131e0192b9d9d9ddb518eb3bd4e8fb4a1f0901c
Blast
0xf956d9fa19656d8e5219fd6fa8ba6cb198094138
Merlin
0xf956d9fa19656d8e5219fd6fa8ba6cb198094138
X Layer
0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD
二进制合约接口文件 (ABI)
#
请参考：
https://github.com/okx/OKX-DEX-Aggregator-ABI

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="智能合约">智能合约<a class="index_header-anchor__Xqb+L" href="#智能合约" style="opacity:0">#</a></h1>
<p>欧易 DEX router 合约地址及 ABI</p>
<p>DEX router 地址和授权合约地址将会由于合约升级而被替换。为避免影响 API 的正常使用，建议使用 <code>/approve-transaction</code> API 和<code>/build-tx</code> API 响应参数中的合约地址执行授权或交易操作。</p>
<h3 id="dex-router-合约地址">DEX router 合约地址<a class="index_header-anchor__Xqb+L" href="#dex-router-合约地址" style="opacity:0">#</a></h3>
<p>用于签名交易的欧易 DEX router 地址，请查看<a href="/zh-hans/build/dev-docs/dex-api/dex-smart-contract">这里</a>获取详情。</p>
<h3 id="币种授权合约地址">币种授权合约地址<a class="index_header-anchor__Xqb+L" href="#币种授权合约地址" style="opacity:0">#</a></h3>
<p>用于 ERC-20 代币授权的合约地址，请查看<a href="/zh-hans/build/dev-docs/dex-api/dex-smart-contract">这里</a>获取详情。</p>
<h3 id="dex-xbridge-合约地址">DEX XBridge 合约地址<a class="index_header-anchor__Xqb+L" href="#dex-xbridge-合约地址" style="opacity:0">#</a></h3>
<p>用于签名跨链交易的欧易 DEX XBridge 合约地址</p>
<div class="index_table__kvZz5"><table><thead><tr><th>链名称</th><th>DEX XBridge合约地址</th></tr></thead><tbody><tr><td>Ethereum</td><td>0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f</td></tr><tr><td>BNB Chain</td><td>0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f</td></tr><tr><td>OKTC</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Polygon</td><td>0x89f423567c2648BB828c3997f60c47b54f57Fa6e</td></tr><tr><td>Fantom</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Arbitrum</td><td>0xFc99f58A8974A4bc36e60E2d490Bb8D72899ee9f</td></tr><tr><td>Optimism</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Cronos</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Avalanche C</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>TRON</td><td>TVaV2BBs8tpthbp19QAy7ibmXLoYsomKDD</td></tr><tr><td>Solana</td><td>okxBd18urPbBi2vsExxUDArzQNcju2DugV9Mt46BxYE</td></tr><tr><td>zkSync Era</td><td>0x4040bEC373F6e8be2F913324de94A7b9242E5E92</td></tr><tr><td>Polygon zkEvm</td><td>0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD</td></tr><tr><td>Linea</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Mantle</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Base</td><td>0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD</td></tr><tr><td>Manta</td><td>0x91EcECC4F2363770c621a8a061A80d67cfEafEC7</td></tr><tr><td>Metis</td><td>0xa50FD06d2b099a4B06d54177C7d3AB08D3D3F004</td></tr><tr><td>SUI</td><td>0x3d097b26cd6a13a0c37e983e81be72cd2965c4dc717a03471e3a7388c21c9263</td></tr><tr><td>Scroll</td><td>0xf956D9FA19656D8e5219fd6fa8bA6cb198094138</td></tr><tr><td>Starknet</td><td>0x00e704db07356df9a2ba8cd2a131e0192b9d9d9ddb518eb3bd4e8fb4a1f0901c</td></tr><tr><td>Blast</td><td>0xf956d9fa19656d8e5219fd6fa8ba6cb198094138</td></tr><tr><td>Merlin</td><td>0xf956d9fa19656d8e5219fd6fa8ba6cb198094138</td></tr><tr><td>X Layer</td><td>0x5965851f21DAE82eA7C62f87fb7C57172E9F2adD</td></tr></tbody></table></div>
<h2 data-content="二进制合约接口文件 (ABI)" id="二进制合约接口文件-(abi)">二进制合约接口文件 (ABI)<a class="index_header-anchor__Xqb+L" href="#二进制合约接口文件-(abi)" style="opacity:0">#</a></h2>
<p>请参考：<a class="items-center" href="https://github.com/okx/OKX-DEX-Aggregator-ABI" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/OKX-DEX-Aggregator-ABI<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></p><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "智能合约"
  ],
  "sidebar_links": [
    "搭建兑换应用",
    "搭建跨链应用",
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
    "二进制合约接口文件 (ABI)"
  ]
}
```

</details>
