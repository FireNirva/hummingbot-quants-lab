# 日志更新 | 首页 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-change-log#2024-年-1-月-2-日  
**抓取时间:** 2025-05-27 07:34:08  
**字数:** 852

## 导航路径
DEX API > 首页 > 日志更新

## 目录
- 什么是 DEX API
- API 访问和用法
- API 费用
- 支持的链
- 开发者平台
- 环境设置
- 运行第一个程序
- 用户协议

---

日志更新
#
2025 年 5 月 22 日
#
API/DEX API
更新
行情 API 现在支持查询返回最多 100 个币种的 5 分钟、1 小时、4 小时和 24 小时的交易量，以及对应时间范围内的价格变动，你可以在 /price-info 接口中查看。
2025 年 5 月 16 日
#
API/DEX API
更新
交易 API 现已支持
Solana 四档优先费
。
2025 年 5 月 13 日
#
API/DEX API
更新
交易 API 现已支持为 Solana 链设置
正滑点收益
。
2025 年 5 月 5 日
#
API/DEX API
更新
交易 API 现已支持为 Solana 链设置
最高 10% 的分佣费用
。
2025 年 5 月 2 日
#
API/DEX API
更新
交易 API 现已支持为
Ton 链
设置分佣费用。
交易 API 现已支持为 **EVM wrap token **设置分佣费用。
2025 年 5 月 1 日
#
API/DEX API
更新
交易 API 现已支持交易上链 API 功能，支持获取 Gas price、Gas limit 交易所需信息，并直接广播交易。
2025 年 3 月 27 日
#
API/DEX API
更新
OKX DEX API 现已支持
Market API
。
2025 年 3 月 12 日
#
API/DEX API
Update
单链兑换已支持 Sonic 链
2025 年 2 月 11 日
#
API/DEX API
Update
单链兑换接口已支持 Solana 链的/swap-instruction 接口，你可自定义组装交易指令
2025 年 1 月 23 日
#
API/DEX API
Update
单链兑换接口已支持指定单个流动性池进行兑换的功能，你可通过设置
directRouter
参数来实现，当前仅支持 Solana 链
单链兑换接口已支持查询兑换交易历史功能
2024 年 12 月 26 日
#
API/DEX API
Update
单链兑换接口已支持自动滑点功能
2024 年 11 月 25 日
#
API/DEX API
Update
单链兑换接口 swapReceiverAddress 参数已支持 Solana 链，现在可以在 Solana 链，为一笔兑换交易指定其他接收地址
2024 年 11 月 12 日
#
API/DEX API
Update
单链兑换接口增加 Solana 新分佣地址入参参数，Sol 及 SPL token 均支持直接使用钱包地址分佣
获取单链流动性列表及获取跨链桥列表接口，支持返回协议 logo 内容
单链询价、兑换接口，支持识别并返回貔貅盘，买卖税 100% 的风险代币
2024 年 10 月 29 日
#
API/DEX API
Update
单链兑换支持 Sui 链
2024 年 7 月 2 日
#
API/DEX API
Update
ETH dexRouter 合约 0xf3de3c0d654fda23dad170f0f320a92172509127 在 2024 年 8 月 1 日后将无法正常使用，请使用最新版本。
2024 年 6 月 19 日
#
API/DEX API
Update
兑换 API DEX Router eth 合约地址更新
2024 年 5 月 7 日
#
API/DEX API
Update
Solana 主网支持分佣功能
2024 年 4 月 19 日
#
API/DEX API
Update
跨链支持 SUI 链
2024 年 4 月 19 日
#
API/DEX API
Update
跨链支持 X Layer 链
2024 年 4 月 12 日
#
API/DeFi API
Update
跨链滑点限制请求参数范围调整为 0.002-0.5
跨链支持 Merlin 链
2024 年 4 月 12 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增返回参数（quoteCompareList）
2024 年 4 月 8 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增请求参数（toTokenReferrerAddress）
2024 年 4 月 2 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增支持链（Merlin）
2024 年 3 月 22 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增请求参数（callDataMemo）
2024 年 3 月 22 日
#
API/DeFi API
Update
向 DEX 跨链获取路径信息接口和跨链兑换接口增加了新的请求参数 （sort)
DEX XBridge 合约地址更新
2024 年 3 月 13 日
#
API/DeFi API
Update
向 DEX 跨链查询交易状态接口增加了新的响应参数 （sourceChainGasfee, destinationChainGasfee, crossChainFee)
向 DEX 跨链兑换接口增加了新的请求参数（onlyBridge）以及新的响应参数（minmumReceive, maxPriorityFeePerGas）
跨链兑换 API 智能合约部分新增跨链合约地址 （DEX XBridge 合约地址）
跨链兑换 API 新增获取仅通过跨链桥交易的币种列表接口
2024 年 3 月 7 日
#
API/DeFi API
Update
更新 单链跨链兑换接口, 新增请求参数（priceImpactProtectionPercentage）
2024 年 2 月 29 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增返回参数（decimal）
2024 年 2 月 22 日
#
API/DeFi API
Update
更新 单链兑换接口, 新增返回参数（maxPriorityFeePerGas）
2024 年 2 月 1 日
#
API/DeFi API
Update
更新 单链兑换接口 支持 solana, 新增请求参数（solTokenAccountAddress）
新增 单链兑换 支持 solana 快速开始引导
2024 年 1 月 17 日
#
API/DeFi API
Update
向 DEX 跨链兑换接口增加了新的请求参数（feePercent, referrerAddress)
2024 年 1 月 11 日
#
API/DeFi API
Update
跨链滑点范围调整为 0.005-0.5
2024 年 1 月 2 日
#
API/DeFi API
Update
向 DEX 跨链兑换接口增加了新的请求参数（receiveAddress)
向 DEX 跨链查询交易状态接口增加了新的请求参数（chainld)
2023 年 12 月 28 日
#
API/DeFi API
Update
上线欧易 Web3 DeFi 首版 API 文档
新增接入 DeFi API 的申购、赎回以及领取奖励金流程
新增查询信息、计算预估信息、调用交易数据、查询用户信息的方法
2023 年 12 月 20 日
#
API/DEX API
Update
向 DEX 跨链兑换获取路径信息接口和跨链兑换接口增加了新的响应参数（crossChainFeeTokenAddress）
向 DEX 跨链兑换查询交易状态接口增加了新的响应参数（status）
2023 年 12 月 14 日
#
API/DEX API
Update
新增 Dex Iframe
2023 年 12 月 14 日
#
API/DEX API
Update
向 DEX 交易接口增加了新的可选参数（swapReceiverAddress）
2023 年 12 月 08 日
#
API/DEX API
Update
新增 DEX 限价单列表查询接口
新增 DEX 限价单获取取消 calldata
2023 年 12 月 06 日
#
API/DEX API
Update
向 DEX 跨链兑换获取路径信息接口增加了新的响应参数（toDexRouterList）
向 DEX 跨链兑换查询交易状态接口增加了新的响应参数（toAmount, errorMsg）
向 DEX 跨链兑换 FAQ 增加了跨链退款问题
2023 年 11 月 24 日
#
API/DEX API
Update
Order API 新增挂单模块，支持挂单到 OpenSea 和 OKX
Order model 模型增加更多字段的解释
2023 年 11 月 23 日
#
API/DEX API
Update
增加了 DEX 跨链聚合器 API 快速开始教程
2023 年 11 月 21 日
#
API/DEX API
Update
增加了 DEX 跨链聚合器 API 快速开始教程
2023 年 11 月 15 日
#
API/DEX API
Update
向 DEX 跨链聚合器获取路径信息接口 cross-chain/quote 添加了新的响应参数 （crossChainFee)
向 DEX 跨链聚合器跨链兑换接口 cross-chain/build-tx 添加新的响应参数（crossChainFee）
2023 年 11 月 10 日
#
API/DEX API
Update
增加了 DEX API 快速开始教程
2023 年 11 月 7 日
#
API/DEX API
Update
增加了 DEX 跨链聚合器 API
2023 年 10 月 31 日
#
API/DEX API
Update
添加了 DEX 限价单 API
2023 年 10 月 23 日
#
API/DEX API
Update
添加了智能合约模块，包含合约地址信息及合约 ABI
2023 年 9 月 27 日
#
DApp 接入钱包文档升级
Update
更新了 DApp 接入欧易 Web3 钱包移动端的内容
添加了 DApp 接入欧易 Web3 钱包移动端的引导和内容
2023 年 8 月 17 日
#
API/Marketplace API
Update
添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key
根据最新版本更新了所有 URI
更新了错误码
API/DEX API
Update
添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key
更新了错误码
API/比特币生态
Update
添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key
根据最新版本更新了所有 URI
2023 年 5 月 29 日
#
API/比特币生态
Update
添加了新的 BRC-20 接口：
brc20/token-list
向 BRC-20 接口
brc20/transaction-list
添加了新的响应参数（ index, location ）
在 BRC-20 接口
brc20/inscriptions-list
添加了新的响应参数（ location ）

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="日志更新">日志更新<a class="index_header-anchor__Xqb+L" href="#日志更新" style="opacity:0">#</a></h1>
<h3 id="2025-年-5-月-22-日">2025 年 5 月 22 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-22-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>行情 API 现在支持查询返回最多 100 个币种的 5 分钟、1 小时、4 小时和 24 小时的交易量，以及对应时间范围内的价格变动，你可以在 /price-info 接口中查看。</li>
</ul>
<h3 id="2025-年-5-月-16-日">2025 年 5 月 16 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-16-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>交易 API 现已支持 <strong>Solana 四档优先费</strong>。</li>
</ul>
<h3 id="2025-年-5-月-13-日">2025 年 5 月 13 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-13-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>交易 API 现已支持为 Solana 链设置<strong>正滑点收益</strong>。</li>
</ul>
<h3 id="2025-年-5-月-5-日">2025 年 5 月 5 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-5-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>交易 API 现已支持为 Solana 链设置<strong>最高 10% 的分佣费用</strong>。</li>
</ul>
<h3 id="2025-年-5-月-2-日">2025 年 5 月 2 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-2-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>交易 API 现已支持为 <strong>Ton 链</strong>设置分佣费用。</li>
<li>交易 API 现已支持为 **EVM wrap token **设置分佣费用。</li>
</ul>
<h3 id="2025-年-5-月-1-日">2025 年 5 月 1 日<a class="index_header-anchor__Xqb+L" href="#2025-年-5-月-1-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>交易 API 现已支持交易上链 API 功能，支持获取 Gas price、Gas limit 交易所需信息，并直接广播交易。</li>
</ul>
<h3 id="2025-年-3-月-27-日">2025 年 3 月 27 日<a class="index_header-anchor__Xqb+L" href="#2025-年-3-月-27-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">更新</span></p>
<ul>
<li>OKX DEX API 现已支持 <strong>Market API</strong>。</li>
</ul>
<h3 id="2025-年-3-月-12-日">2025 年 3 月 12 日<a class="index_header-anchor__Xqb+L" href="#2025-年-3-月-12-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换已支持 Sonic 链</li>
</ul>
<h3 id="2025-年-2-月-11-日">2025 年 2 月 11 日<a class="index_header-anchor__Xqb+L" href="#2025-年-2-月-11-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换接口已支持 Solana 链的/swap-instruction 接口，你可自定义组装交易指令</li>
</ul>
<h3 id="2025-年-1-月-23-日">2025 年 1 月 23 日<a class="index_header-anchor__Xqb+L" href="#2025-年-1-月-23-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换接口已支持指定单个流动性池进行兑换的功能，你可通过设置<code>directRouter</code>参数来实现，当前仅支持 Solana 链</li>
<li>单链兑换接口已支持查询兑换交易历史功能</li>
</ul>
<h3 id="2024-年-12-月-26-日">2024 年 12 月 26 日<a class="index_header-anchor__Xqb+L" href="#2024-年-12-月-26-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换接口已支持自动滑点功能</li>
</ul>
<h3 id="2024-年-11-月-25-日">2024 年 11 月 25 日<a class="index_header-anchor__Xqb+L" href="#2024-年-11-月-25-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换接口 swapReceiverAddress 参数已支持 Solana 链，现在可以在 Solana 链，为一笔兑换交易指定其他接收地址</li>
</ul>
<h3 id="2024-年-11-月-12-日">2024 年 11 月 12 日<a class="index_header-anchor__Xqb+L" href="#2024-年-11-月-12-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换接口增加 Solana 新分佣地址入参参数，Sol 及 SPL token 均支持直接使用钱包地址分佣</li>
<li>获取单链流动性列表及获取跨链桥列表接口，支持返回协议 logo 内容</li>
<li>单链询价、兑换接口，支持识别并返回貔貅盘，买卖税 100% 的风险代币</li>
</ul>
<h3 id="2024-年-10-月-29-日">2024 年 10 月 29 日<a class="index_header-anchor__Xqb+L" href="#2024-年-10-月-29-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>单链兑换支持 Sui 链</li>
</ul>
<h3 id="2024-年-7-月-2-日">2024 年 7 月 2 日<a class="index_header-anchor__Xqb+L" href="#2024-年-7-月-2-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>ETH dexRouter 合约 0xf3de3c0d654fda23dad170f0f320a92172509127 在 2024 年 8 月 1 日后将无法正常使用，请使用最新版本。</li>
</ul>
<h3 id="2024-年-6-月-19-日">2024 年 6 月 19 日<a class="index_header-anchor__Xqb+L" href="#2024-年-6-月-19-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>兑换 API DEX Router eth 合约地址更新</li>
</ul>
<h3 id="2024-年-5-月-7-日">2024 年 5 月 7 日<a class="index_header-anchor__Xqb+L" href="#2024-年-5-月-7-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>Solana 主网支持分佣功能</li>
</ul>
<h3 id="2024-年-4-月-19-日">2024 年 4 月 19 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-19-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>跨链支持 SUI 链</li>
</ul>
<h3 id="2024-年-4-月-19-日">2024 年 4 月 19 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-19-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>跨链支持 X Layer 链</li>
</ul>
<h3 id="2024-年-4-月-12-日">2024 年 4 月 12 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-12-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>跨链滑点限制请求参数范围调整为 0.002-0.5</li>
<li>跨链支持 Merlin 链</li>
</ul>
<h3 id="2024-年-4-月-12-日">2024 年 4 月 12 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-12-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增返回参数（quoteCompareList）</li>
</ul>
<h3 id="2024-年-4-月-8-日">2024 年 4 月 8 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-8-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增请求参数（toTokenReferrerAddress）</li>
</ul>
<h3 id="2024-年-4-月-2-日">2024 年 4 月 2 日<a class="index_header-anchor__Xqb+L" href="#2024-年-4-月-2-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增支持链（Merlin）</li>
</ul>
<h3 id="2024-年-3-月-22-日">2024 年 3 月 22 日<a class="index_header-anchor__Xqb+L" href="#2024-年-3-月-22-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增请求参数（callDataMemo）</li>
</ul>
<h3 id="2024-年-3-月-22-日">2024 年 3 月 22 日<a class="index_header-anchor__Xqb+L" href="#2024-年-3-月-22-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链获取路径信息接口和跨链兑换接口增加了新的请求参数 （sort)</li>
<li>DEX XBridge 合约地址更新</li>
</ul>
<h3 id="2024-年-3-月-13-日">2024 年 3 月 13 日<a class="index_header-anchor__Xqb+L" href="#2024-年-3-月-13-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链查询交易状态接口增加了新的响应参数 （sourceChainGasfee, destinationChainGasfee, crossChainFee)</li>
<li>向 DEX 跨链兑换接口增加了新的请求参数（onlyBridge）以及新的响应参数（minmumReceive, maxPriorityFeePerGas）</li>
<li>跨链兑换 API 智能合约部分新增跨链合约地址 （DEX XBridge 合约地址）</li>
<li>跨链兑换 API 新增获取仅通过跨链桥交易的币种列表接口</li>
</ul>
<h3 id="2024-年-3-月-7-日">2024 年 3 月 7 日<a class="index_header-anchor__Xqb+L" href="#2024-年-3-月-7-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链跨链兑换接口, 新增请求参数（priceImpactProtectionPercentage）</li>
</ul>
<h3 id="2024-年-2-月-29-日">2024 年 2 月 29 日<a class="index_header-anchor__Xqb+L" href="#2024-年-2-月-29-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增返回参数（decimal）</li>
</ul>
<h3 id="2024-年-2-月-22-日">2024 年 2 月 22 日<a class="index_header-anchor__Xqb+L" href="#2024-年-2-月-22-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口, 新增返回参数（maxPriorityFeePerGas）</li>
</ul>
<h3 id="2024-年-2-月-1-日">2024 年 2 月 1 日<a class="index_header-anchor__Xqb+L" href="#2024-年-2-月-1-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新 单链兑换接口 支持 solana, 新增请求参数（solTokenAccountAddress）</li>
<li>新增 单链兑换 支持 solana 快速开始引导</li>
</ul>
<h3 id="2024-年-1-月-17-日">2024 年 1 月 17 日<a class="index_header-anchor__Xqb+L" href="#2024-年-1-月-17-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链兑换接口增加了新的请求参数（feePercent, referrerAddress)</li>
</ul>
<h3 id="2024-年-1-月-11-日">2024 年 1 月 11 日<a class="index_header-anchor__Xqb+L" href="#2024-年-1-月-11-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>跨链滑点范围调整为 0.005-0.5</li>
</ul>
<h3 id="2024-年-1-月-2-日">2024 年 1 月 2 日<a class="index_header-anchor__Xqb+L" href="#2024-年-1-月-2-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链兑换接口增加了新的请求参数（receiveAddress)</li>
<li>向 DEX 跨链查询交易状态接口增加了新的请求参数（chainld)</li>
</ul>
<h3 id="2023-年-12-月-28-日">2023 年 12 月 28 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-28-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DeFi API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>上线欧易 Web3 DeFi 首版 API 文档</li>
<li>新增接入 DeFi API 的申购、赎回以及领取奖励金流程</li>
<li>新增查询信息、计算预估信息、调用交易数据、查询用户信息的方法</li>
</ul>
<h3 id="2023-年-12-月-20-日">2023 年 12 月 20 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-20-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链兑换获取路径信息接口和跨链兑换接口增加了新的响应参数（crossChainFeeTokenAddress）</li>
<li>向 DEX 跨链兑换查询交易状态接口增加了新的响应参数（status）</li>
</ul>
<h3 id="2023-年-12-月-14-日">2023 年 12 月 14 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-14-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>新增 Dex Iframe</li>
</ul>
<h3 id="2023-年-12-月-14-日">2023 年 12 月 14 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-14-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 交易接口增加了新的可选参数（swapReceiverAddress）</li>
</ul>
<h3 id="2023-年-12-月-08-日">2023 年 12 月 08 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-08-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>新增 DEX 限价单列表查询接口</li>
<li>新增 DEX 限价单获取取消 calldata</li>
</ul>
<h3 id="2023-年-12-月-06-日">2023 年 12 月 06 日<a class="index_header-anchor__Xqb+L" href="#2023-年-12-月-06-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链兑换获取路径信息接口增加了新的响应参数（toDexRouterList）</li>
<li>向 DEX 跨链兑换查询交易状态接口增加了新的响应参数（toAmount, errorMsg）</li>
<li>向 DEX 跨链兑换 FAQ 增加了跨链退款问题</li>
</ul>
<h3 id="2023-年-11-月-24-日">2023 年 11 月 24 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-24-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>Order API 新增挂单模块，支持挂单到 OpenSea 和 OKX</li>
<li>Order model 模型增加更多字段的解释</li>
</ul>
<h3 id="2023-年-11-月-23-日">2023 年 11 月 23 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-23-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>增加了 DEX 跨链聚合器 API 快速开始教程</li>
</ul>
<h3 id="2023-年-11-月-21-日">2023 年 11 月 21 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-21-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>增加了 DEX 跨链聚合器 API 快速开始教程</li>
</ul>
<h3 id="2023-年-11-月-15-日">2023 年 11 月 15 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-15-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>向 DEX 跨链聚合器获取路径信息接口 cross-chain/quote 添加了新的响应参数 （crossChainFee)</li>
<li>向 DEX 跨链聚合器跨链兑换接口 cross-chain/build-tx 添加新的响应参数（crossChainFee）</li>
</ul>
<h3 id="2023-年-11-月-10-日">2023 年 11 月 10 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-10-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>增加了 DEX API 快速开始教程</li>
</ul>
<h3 id="2023-年-11-月-7-日">2023 年 11 月 7 日<a class="index_header-anchor__Xqb+L" href="#2023-年-11-月-7-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>增加了 DEX 跨链聚合器 API</li>
</ul>
<h3 id="2023-年-10-月-31-日">2023 年 10 月 31 日<a class="index_header-anchor__Xqb+L" href="#2023-年-10-月-31-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了 DEX 限价单 API</li>
</ul>
<h3 id="2023-年-10-月-23-日">2023 年 10 月 23 日<a class="index_header-anchor__Xqb+L" href="#2023-年-10-月-23-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了智能合约模块，包含合约地址信息及合约 ABI</li>
</ul>
<h3 id="2023-年-9-月-27-日">2023 年 9 月 27 日<a class="index_header-anchor__Xqb+L" href="#2023-年-9-月-27-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>DApp 接入钱包文档升级</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>更新了 DApp 接入欧易 Web3 钱包移动端的内容</li>
<li>添加了 DApp 接入欧易 Web3 钱包移动端的引导和内容</li>
</ul>
<hr/>
<h3 id="2023-年-8-月-17-日">2023 年 8 月 17 日<a class="index_header-anchor__Xqb+L" href="#2023-年-8-月-17-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/Marketplace API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key</li>
<li>根据最新版本更新了所有 URI</li>
<li>更新了错误码</li>
</ul>
<p class="flex items-center"><strong>API/DEX API</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key</li>
<li>更新了错误码</li>
</ul>
<p class="flex items-center"><strong>API/比特币生态</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了 API key 的身份验证。此后的所有接口都需要从 Web3 开发者管理平台生成 API key</li>
<li>根据最新版本更新了所有 URI</li>
</ul>
<hr/>
<h3 id="2023-年-5-月-29-日">2023 年 5 月 29 日<a class="index_header-anchor__Xqb+L" href="#2023-年-5-月-29-日" style="opacity:0">#</a></h3>
<p class="flex items-center"><strong>API/比特币生态</strong><span class="index_update__bQGFe index_text__nVoPA">Update</span></p>
<ul>
<li>添加了新的 BRC-20 接口：<code>brc20/token-list</code></li>
<li>向 BRC-20 接口 <code>brc20/transaction-list</code> 添加了新的响应参数（ index, location ）</li>
<li>在 BRC-20 接口 <code>brc20/inscriptions-list</code> 添加了新的响应参数（ location ）</li>
</ul>
<hr/><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "首页",
    "日志更新"
  ],
  "sidebar_links": [
    "什么是 DEX API",
    "API 访问和用法",
    "API 费用",
    "支持的链",
    "开发者平台",
    "环境设置",
    "运行第一个程序",
    "用户协议"
  ],
  "toc": [
    "什么是 DEX API",
    "API 访问和用法",
    "API 费用",
    "支持的链",
    "开发者平台",
    "环境设置",
    "运行第一个程序",
    "用户协议"
  ]
}
```

</details>
