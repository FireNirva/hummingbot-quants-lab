# 智能合约 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-smart-contract#dex-router-合约地址  
**抓取时间:** 2025-05-27 01:49:46  
**字数:** 165

## 导航路径
DEX API > 交易 API > 智能合约

## 目录
- 合约地址
- 二进制合约接口文件 (ABI)

---

智能合约
#
欧易 DEX router 合约地址及 ABI
合约地址
#
DEX router 地址和授权合约地址将会由于合约升级而被替换。为避免影响 API 的正常使用，建议使用
/approve-transaction
API 和
/swap
API 响应参数中的合约地址执行授权或交易操作。
DEX router 合约地址
#
用于签名交易的欧易 DEX router 地址。
链名称
DEX router 合约地址
Ethereum
0x6088d94C5a40CEcd3ae2D4e0710cA687b91c61d0
Solana
6m2CDdhRgxpH4WjvdzxAYbGxwdGUz5MziiL5jek2kBma
SUI
0x8a802657ae00af9271d48199693c91c96ac005b18e63e97d267328fc8600ffa6
extended: 0x3426ae29bab87dd8677f4e0709a772134977c552fa5196d5051c03a400b4faf4
Sonic
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Tron
TQvhNt1uxwjtbgdgYKYxR72Exf4nvA6nQN
Ton
EQBjfOGw4Iq6FYZplhwZ5rRNb7Htac7WJh8g_eQcGTswxVqP
zkSync Era
0x5058C498864795689fe41fB54f29a8B71F0A7201
Optimism
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Polygon
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
BNB Chain
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
OKC
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Avalanche C
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Fantom
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Arbitrum
0x6088d94C5a40CEcd3ae2D4e0710cA687b91c61d0
Linea
0x06f183D52D92c13a5f2B989B8710BA7F00bd6f87
Conflux eSpace
0x8feB9E84b7E9DC86adc6cD6Eb554C5B4355c8405
Base
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Mantle
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Scroll
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Manta
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Metis
0x06f183D52D92c13a5f2B989B8710BA7F00bd6f87
Blast
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Zeta
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
Polygon zkEvm
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Merlin
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
X Layer
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
Mode
0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4
SEI
0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380
币种授权合约地址
#
用于 ERC-20 代币授权的合约地址。Ton，Solana 链不需要授权。
链名称
授权合约地址
Ethereum
0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f
Tron
THRAE2VhGNAcvPKtT96AqyXtSQwhiU1XL8
Sonic
0xd321ab5589d3e8fa5df985ccfef625022e2dd910
zkSync Era
0xc67879F4065d3B9fe1C09EE990B891Aa8E3a4c2f
Optimism
0x68D6B739D2020067D1e2F713b999dA97E4d54812
Polygon
0x3B86917369B83a6892f553609F3c2F439C184e31
BNB Chain
0x2c34A2Fb1d0b4f55de51E1d0bDEfaDDce6b7cDD6
OKC
0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58
Avalanche C
0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f
Fantom
0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58
Arbitrum
0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58
Linea
0x57df6092665eb6058DE53939612413ff4B09114E
Conflux eSpace
0x68D6B739D2020067D1e2F713b999dA97E4d54812
Base
0x57df6092665eb6058DE53939612413ff4B09114E
Mantle
0x57df6092665eb6058DE53939612413ff4B09114E
Scroll
0x57df6092665eb6058DE53939612413ff4B09114E
Manta
0x57df6092665eb6058DE53939612413ff4B09114E
Metis
0x57df6092665eb6058DE53939612413ff4B09114E
Blast
0x5fD2Dc91FF1dE7FF4AEB1CACeF8E9911bAAECa68
Zeta
0x03B5ACdA01207824cc7Bc21783Ee5aa2B8d1D2fE
Polygon zkEvm
0x57df6092665eb6058DE53939612413ff4B09114E
Merlin
0x8b773D83bc66Be128c60e07E17C8901f7a64F000
X Layer
0x8b773D83bc66Be128c60e07E17C8901f7a64F000
Mode
0xbd0EBE49779E154E5042B34D5BcfBc498e4B3249
SEI
0x801D8ED849039007a7170830623180396492c7ED
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
<h2 data-content="合约地址" id="合约地址">合约地址<a class="index_header-anchor__Xqb+L" href="#合约地址" style="opacity:0">#</a></h2>
<p>DEX router 地址和授权合约地址将会由于合约升级而被替换。为避免影响 API 的正常使用，建议使用 <code>/approve-transaction</code> API 和<code>/swap</code> API 响应参数中的合约地址执行授权或交易操作。</p>
<h3 id="dex-router-合约地址">DEX router 合约地址<a class="index_header-anchor__Xqb+L" href="#dex-router-合约地址" style="opacity:0">#</a></h3>
<p>用于签名交易的欧易 DEX router 地址。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>链名称</th><th>DEX router 合约地址</th></tr></thead><tbody><tr><td>Ethereum</td><td>0x6088d94C5a40CEcd3ae2D4e0710cA687b91c61d0</td></tr><tr><td>Solana</td><td>6m2CDdhRgxpH4WjvdzxAYbGxwdGUz5MziiL5jek2kBma</td></tr><tr><td>SUI</td><td>0x8a802657ae00af9271d48199693c91c96ac005b18e63e97d267328fc8600ffa6 <!-- -->extended: 0x3426ae29bab87dd8677f4e0709a772134977c552fa5196d5051c03a400b4faf4</td></tr><tr><td>Sonic</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Tron</td><td>TQvhNt1uxwjtbgdgYKYxR72Exf4nvA6nQN</td></tr><tr><td>Ton</td><td>EQBjfOGw4Iq6FYZplhwZ5rRNb7Htac7WJh8g_eQcGTswxVqP</td></tr><tr><td>zkSync Era</td><td>0x5058C498864795689fe41fB54f29a8B71F0A7201</td></tr><tr><td>Optimism</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Polygon</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>BNB Chain</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>OKC</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Avalanche C</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Fantom</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Arbitrum</td><td>0x6088d94C5a40CEcd3ae2D4e0710cA687b91c61d0</td></tr><tr><td>Linea</td><td>0x06f183D52D92c13a5f2B989B8710BA7F00bd6f87</td></tr><tr><td>Conflux eSpace</td><td>0x8feB9E84b7E9DC86adc6cD6Eb554C5B4355c8405</td></tr><tr><td>Base</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Mantle</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Scroll</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Manta</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Metis</td><td>0x06f183D52D92c13a5f2B989B8710BA7F00bd6f87</td></tr><tr><td>Blast</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Zeta</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>Polygon zkEvm</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Merlin</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>X Layer</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr><tr><td>Mode</td><td>0x9b9efa5Efa731EA9Bbb0369E91fA17Abf249CFD4</td></tr><tr><td>SEI</td><td>0xd30D8CA2E7715eE6804a287eB86FAfC0839b1380</td></tr></tbody></table></div>
<h3 id="币种授权合约地址">币种授权合约地址<a class="index_header-anchor__Xqb+L" href="#币种授权合约地址" style="opacity:0">#</a></h3>
<p>用于 ERC-20 代币授权的合约地址。Ton，Solana 链不需要授权。</p>
<div class="index_table__kvZz5"><table><thead><tr><th>链名称</th><th>授权合约地址</th></tr></thead><tbody><tr><td>Ethereum</td><td>0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f</td></tr><tr><td>Tron</td><td>THRAE2VhGNAcvPKtT96AqyXtSQwhiU1XL8</td></tr><tr><td>Sonic</td><td>0xd321ab5589d3e8fa5df985ccfef625022e2dd910</td></tr><tr><td>zkSync Era</td><td>0xc67879F4065d3B9fe1C09EE990B891Aa8E3a4c2f</td></tr><tr><td>Optimism</td><td>0x68D6B739D2020067D1e2F713b999dA97E4d54812</td></tr><tr><td>Polygon</td><td>0x3B86917369B83a6892f553609F3c2F439C184e31</td></tr><tr><td>BNB Chain</td><td>0x2c34A2Fb1d0b4f55de51E1d0bDEfaDDce6b7cDD6</td></tr><tr><td>OKC</td><td>0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58</td></tr><tr><td>Avalanche C</td><td>0x40aA958dd87FC8305b97f2BA922CDdCa374bcD7f</td></tr><tr><td>Fantom</td><td>0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58</td></tr><tr><td>Arbitrum</td><td>0x70cBb871E8f30Fc8Ce23609E9E0Ea87B6b222F58</td></tr><tr><td>Linea</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Conflux eSpace</td><td>0x68D6B739D2020067D1e2F713b999dA97E4d54812</td></tr><tr><td>Base</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Mantle</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Scroll</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Manta</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Metis</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Blast</td><td>0x5fD2Dc91FF1dE7FF4AEB1CACeF8E9911bAAECa68</td></tr><tr><td>Zeta</td><td>0x03B5ACdA01207824cc7Bc21783Ee5aa2B8d1D2fE</td></tr><tr><td>Polygon zkEvm</td><td>0x57df6092665eb6058DE53939612413ff4B09114E</td></tr><tr><td>Merlin</td><td>0x8b773D83bc66Be128c60e07E17C8901f7a64F000</td></tr><tr><td>X Layer</td><td>0x8b773D83bc66Be128c60e07E17C8901f7a64F000</td></tr><tr><td>Mode</td><td>0xbd0EBE49779E154E5042B34D5BcfBc498e4B3249</td></tr><tr><td>SEI</td><td>0x801D8ED849039007a7170830623180396492c7ED</td></tr></tbody></table></div>
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
    "合约地址",
    "二进制合约接口文件 (ABI)"
  ]
}
```

</details>
