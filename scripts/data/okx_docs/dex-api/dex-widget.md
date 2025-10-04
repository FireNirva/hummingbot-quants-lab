# DEX Widget | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-widget#updateparams  
**抓取时间:** 2025-05-27 04:53:42  
**字数:** 1487

## 导航路径
DEX API > 资源 > DEX Widget

## 目录
- 安装
- 快速开始
- 钱包提供方
- 参数
- 类型描述
- 多语言配置
- ChainId 配置
- 默认币对配置
- 自定义费率
- feePercent
- referrerAddress
- Widget 更新
- 事件监听

---

使用 Widget
#
本文将告诉你如何将功能强大的欧易 Widget 与你的产品进行整合，让你只需 30 分钟即可搭建一个高效交易界面！
安装
#
yarn
add
@okxweb3/dex-widget
// or
npm
install
@okxweb3/dex-widget
// or
pnpm
add
@okxweb3/dex-widget
快速开始
#
下方的例子将向你演示如何在一个 React 项目中使用
@okxweb3/dex-widget
。你还可以通过此
链接
查看更多例子。
实际 Demo：
https://okx.github.io/dex-widget/
import
React
,
{
useRef
,
useEffect
}
from
'react'
;
import
ReactDOM
from
'react-dom/client'
;
import
{
createOkxSwapWidget
}
from
'@okxweb3/dex-widget'
;
function
App
(
)
{
const
widgetRef
=
useRef
(
)
;
useEffect
(
(
)
=>
{
const
params
=
{
width
:
375
,
providerType
:
'EVM'
,
}
;
const
provider
=
window
.
ethereum
;
const
listeners
=
[
{
event
:
'ON_CONNECT_WALLET'
,
handler
:
(
)
=>
{
provider
.
enable
(
)
;
}
,
}
,
]
;
const
instance
=
createOkxSwapWidget
(
widgetRef
.
current
,
{
params
,
provider
,
listeners
,
}
)
;
return
(
)
=>
{
instance
.
destroy
(
)
;
}
;
}
,
[
]
)
;
return
<
div ref
=
{
widgetRef
}
/
>
;
}
const
root
=
ReactDOM
.
createRoot
(
document
.
getElementById
(
'root'
)
)
;
root
.
render
(
<
React
.
StrictMode
>
<
App
/
>
<
/
React
.
StrictMode
>
)
;
钱包提供方
#
如果需要连接钱包，你可以从你的应用中传递钱包提供方信息。同时添加 ON_CONNECT_WALLET 事件，即可无缝连接并使用 Widget。
如果提供方是在 Ethereum 或其他 EVM 网络上，它必须要符合 EIP-1193 才能创建交易界面。
如果提供方是在 Solana 网络上，它必须从你的应用中传递钱包提供方的信息。
import
{
createOkxSwapWidget
,
ProviderType
}
from
'@okxweb3/dex-widget'
;
const
widgetEthInstance
=
createOkxSwapWidget
(
document
.
getElementById
(
'widget'
)
,
{
params
:
{
providerType
:
ProviderType
.
EVM
,
}
,
provider
:
window
.
ethereum
,
// e.g. window.okexchain
}
)
;
const
widgetSolanaInstance
=
createOkxSwapWidget
(
document
.
getElementById
(
'widget'
)
,
{
params
:
{
providerType
:
ProviderType
.
SOLANA
,
}
,
provider
:
window
.
solana
,
// window.okexchain.solana
}
)
;
Rainbow 连接钱包组件的示例可参考这个
链接
。
参数
#
下方表格内是对 Params 的描述。
参数
类型
默认值
描述
width
number
450
用 css 值 (px) 表示的 Widget 宽度。如果未设置宽度，则宽度的展示样式为：>767px 显示为 450 px， <768 px 显示为 100%， < 375 px 则显示为 375 px。
theme
THEME
light
兑换 Widget 提供默认的日间、夜间主题选项。你可以按下方示例来切换 Widget 的主题。
lang
string
en_us
你可以调整 Widget 所使用的语言，请在多语言配置部分了解更多细节信息。
tradeType
TradeType
auto
交易的类型，可以是“swap”、“bridge”，或“auto”。注意：“自动”包含“swap”和“bridge”。
chainIds
Array<string>
[]
承载单链兑换的区块链的 ID，请在 ChainId 配置部分查看你可选的所有网络。
feeConfig
IFeeConfig
{}
你可以选择在 Widget 中为所有交易类型设置一个费率，请在自定义费率部分了解详情。
tokenPair
ITokenPair
{}
你所设定使用的兑换默认代币对，请在默认币对配置部分了解详情。
bridgeTokenPair
ITokenPair
{}
你所设定使用的跨链默认代币对，请在默认币对配置部分了解详情。
providerType
ProviderType
' '
ProviderType 是和提供方一致的类型参数，例如，如果提供方是 Solana，那么 providerType 就会是 SOLANA。
类型描述
#
interface
IFeeConfig
{
[
key
:
string
]
:
{
feePercent
?
:
string
|
number
;
referrerAddress
?
:
{
[
key
:
string
]
:
{
feePercent
:
string
|
number
;
}
;
}
;
}
;
}
interface
ITokenPair
{
fromChain
:
string
|
number
;
toChain
:
string
|
number
;
fromToken
?
:
string
;
toToken
?
:
string
;
}
enum
ProviderType
{
EVM
=
'EVM'
,
SOLANA
=
'SOLANA'
,
WALLET_CONNECT
=
'WALLET_CONNECT'
,
}
enum
TradeType
{
SWAP
=
'swap'
,
BRIDGE
=
'bridge'
,
AUTO
=
'auto'
,
}
enum
THEME
{
LIGHT
=
'light'
,
DARK
=
'dark'
,
}
多语言配置
#
lang
描述
en_us
English，默认
zh_cn
简体中文
zh_tw
繁體中文
fr_fr
Français (Afrique)
id_id
Bahasa Indonesia
ru_ru
Русский
tr_tr
Türkçe
vi_vn
Tiếng Việt
de_de
Deutsch
it_it
Italiano
pl_pl
Polski
pt_pt
Português (Portugal)
es_es
Español (España)
pt_br
Português (Brasil)
es_419
Español (Latinoamérica)
cs_cz
Čeština
ro_ro
Română
uk_ua
Українська
ar_eh
العربية
nl_nl
Nederlands
ChainId 配置
#
网络
ChainId
主网币合约地址
Ethereum
1
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Solana
501
11111111111111111111111111111111
Arbitrum
42161
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Base
8453
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Sonic
146
0x4Efa4b8545a3a77D80Da3ECC8F81EdB1a4bda783
Optimism
10
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
zkSync Era
324
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
BNB Chain
56
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Linea
59144
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Polygon
137
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Avalanche C
43114
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Mantle
5000
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Scroll
534352
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
X layer
196
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
Blast
81457
0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE
默认币对配置
#
tokenPair
: 如果没有配置，则单链兑换将默认设置在 Ethereum 网络，且
fromToken
为 ETH，
toToken
为 USDC。
bridgeTokenPair
: 如果没有配置，则跨链兑换将默认设置为从 Ethereum 跨链至 BNB Chain，且
fromToken
为 ETH，
toToken
为 BNB。
import
React
,
{
useEffect
,
useRef
}
from
'react'
;
import
{
OkxSwapWidgetParams
,
ProviderType
,
TradeType
,
}
from
'@okxweb3/dex-widget'
;
const
provider
=
window
.
ethereum
;
export
function
EvmWidget
(
)
{
const
widgetRef
=
useRef
(
)
;
const
params
=
{
chainIds
:
[
'1'
,
'10'
]
,
lang
:
'zh_cn'
,
providerType
:
ProviderType
.
EVM
,
theme
:
'dark'
,
tradeType
:
TradeType
.
AUTO
,
tokenPair
:
{
fromChain
:
1
,
//ETH
toChain
:
1
,
// ETH
fromToken
:
'0xdac17f958d2ee523a2206206994597c13d831ec7'
,
// USDT
toToken
:
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
,
// ETH
}
,
bridgeTokenPair
:
{
fromChain
:
1
,
//ETH
toChain
:
56
,
// BNB
fromToken
:
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
,
// ETH
toToken
:
'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
,
// BNB
}
,
}
;
const
initialConfig
=
{
params
,
provider
,
listeners
:
[
{
event
:
'ON_CONNECT_WALLET'
,
handler
:
(
token
,
preToken
)
=>
{
provider
.
enable
(
)
;
}
,
}
,
]
,
}
;
useEffect
(
(
)
=>
{
const
widgetHandler
=
createOkxSwapWidget
(
widgetRef
.
current
,
initialConfig
)
;
return
(
)
=>
{
widgetHandler
?.
destroy
(
)
;
}
;
}
,
[
]
)
;
return
<
div ref
=
{
widgetRef
}
/
>
;
}
参数
类型
描述
fromChain
String
fromToken 所属的源链 ID (例如，1：Ethereum，可在 ChainId 配置部分查看所有已支持的网络和对应的链 ID)。
fromToken
String
试图卖出的代币的合约地址，例如 ETH：0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE。如果 fromToken 是某一区块链的主网币，请查看链 ID 以获取合约地址。
toChain
String
toToken 所属的目标链 ID (例如，1：Ethereum，可在 ChainId 配置部分查看所有已支持的网络和对应的链 ID)。
toToken
String
试图卖出的代币的合约地址，例如 USDC：0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48。如果 toToken 是某一区块链的主网币，请查看链 ID 以获取合约地址。
自定义费率
#
添加下列参数后，你即可启用 feeConfig 在你的用户在各个网络上执行交易时，通过 Widget 收取手续费：
你需要声明 chainId、feePercent 和 referrerAddress。
在 Ethereum 和其他 EVM 网络，设置 feePercent 和 referrerAddress 即可收取手续费。
在 Solana 网络，SOL 和 SPL 代币的分佣有些不同。SOL 分佣使用的是钱包地址，而 SPL 代币分佣使用的是代币账号。
你可以添加 feePercent 以调整 referrerAddress 所收到的分佣的费率。
// EVM feeConfig example
feeConfig
:
{
[
chainId
]
:
{
referrerAddress
:
'xxx'
,
feePercent
:
[
0
-
3
]
,
}
}
// Solana feeConfig example
feeConfig
:
{
[
chainId
]
:
{
feePercent
:
[
0
-
3
]
,
referrerAddress
:
{
[
tokenContractA
]
:
{
referrerAccount
:
'account/abc'
,
feePercent
:
'1'
,
}
,
[
tokenContractB
]
:
{
referrerAccount
:
'account/abc'
,
feePercent
:
'2'
,
}
}
}
}
// Full Example
feeConfig
:
{
1
:
{
// Ethereum chainId
feePercent
:
3
,
// The percentage of Fee
referrerAddress
:
'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'
,
// eth address that receives the fee
}
,
56
:
{
// Bnb Chain chainId
feePercent
:
3
,
//
referrerAddress
:
'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'
,
// bnb address that receives the fee
}
,
501
:
{
// solana chainId
referrerAddress
:
{
'11111111111111111111111111111111'
:
{
//solana SOL contract address
account
:
'6rocMMKG1DNg93RDfVL2xVdrA5nbAT8cFMbdvVTHUF4m'
,
feePercent
:
1
,
}
,
EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
:
{
//solana USDC contract address
account
:
'C6XW7mFvCuVxYFTi9zTQrUcwkvhfGYAvuosXz6pLDZsa'
,
//solana USDC token account that receives the fee
feePercent
:
1
,
}
,
JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN
:
{
//solana JUP contract address
account
:
'Ezq6jTC3CwnsXDSdtgy8Sa4xi1iA6fxuEeXxWFPLG9sc'
,
//solana JUP token account that receives the fee
feePercent
:
1
,
}
,
}
,
}
,
8453
:
{
feePercent
:
3
,
referrerAddress
:
'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'
,
}
,
}
feePercent
#
发送给分佣地址的 fromTokenAmount 的百分比。剩余的代币数量将被设置为卖出数量。费率用基点 (BPS) 计算，一个基点等于 0.01% (万分之一)。费率不能超过 3% (300 BPS)。
referrerAddress
#
referrerAddress 是接收手续费的地址。
请确保接收手续费的地址存在于参数表中所定义的对应网络之上。
Widget 更新
#
updateParams
#
可更新的属性：theme、lang、width
// 1. Create and initialize the widget
const
widgetHandler
=
createOkxSwapWidget
(
container
,
initialConfig
)
;
// 2. Update the widget's parameters (e.g., change theme or size)
widgetHandler
.
updateParams
(
{
width
:
700
,
theme
:
'light'
,
lang
:
'tr_tr'
,
}
)
;
updateProvider
#
Widget 支持 EVM 和 Solana。当从 EVM 切换到 Solana 时，请记得更新相应的 Widget 提供方，反之亦然。
如果首次渲染时没有传递提供方信息，并想要 Widget 响应钱包绑定，就需要调用 updateProvider。
// 3. Update the provider if the user connects a different wallet, EVM => SOLANA
widgetHandler
.
updateProvider
(
window
.
solana
,
ProviderType
.
SOLANA
)
;
// SOLANA => EVM
// widgetHandler.updateProvider(window.ethereum, ProviderType.EVM);
updateListeners
#
你可以更新 Widget 监听的事件。
// 4. Modify event listeners to handle new types of events
widgetHandler
.
updateListeners
(
[
{
event
:
OkxEvents
.
ON_FROM_CHAIN_CHANGE
,
handler
:
(
payload
)
=>
{
//
}
,
}
,
]
)
;
Listeners 主要用于监听 Widget 向外部暴露的接口，通过不同事件进行定制化处理。而 updateListeners 则用于在切换链后更新定制化处理。
通过添加事件监听器，可以捕获并处理从 iframe 中传递出来的事件数据。这些数据通常是 iframe 内部发生的事件或状态变化，并通过事件传递到外部页面。
接收到的数据可以根据需求进行灵活处理和操作。这意味着你可以根据传递的数据类型或内容，执行不同的逻辑或更新界面元素。
通过 updateListeners 方法，你可以为不同类型的事件 (如 OkxEvents.ON_FROM_CHAIN_CHANGE) 添加处理函数。当事件触发时，处理函数会接收到相关的 payload 数据，以便你进一步操作。
destroy
#
当清除 Widget 模块时，调用此方法
const
widgetHandler
=
createOkxSwapWidget
(
container
,
initialConfig
)
;
widgetHandler
.
destory
(
)
;
注意：
#
每当你刷新和更新时，请确保调用 destroy 方法来清除先前绑定的事件，以避免出现重复订单请求。
事件监听
#
Widget 为 ON_CONNECT_WALLET 和 ON_FROM_CHAIN_CHANGE 提供事件监听。
ON_CONNECT_WALLET：当 Widget 未连接钱包并点击了连接钱包按钮时触发此事件。
ON_FROM_CHAIN_CHANGE： 当 fromChain 发生变化时会触发此事件。
使用方法如下：
import
{
createOkxSwapWidget
,
OkxSwapWidgetParams
,
OkxEventListeners
,
OkxEvents
}
from
'@okxweb3/dex-widget'
const
params
:
OkxSwapWidgetParams
=
{
// ...
}
const
listeners
:
OkxEventListeners
=
[
{
event
:
OkxEvents
.
ON_CONNECT_WALLET
,
handler
:
(
)
=>
{
// open connect wallet method, eg openConnectModal of the rainbow kit.
window
.
ethereum
.
enable
(
)
}
}
,
{
event
:
OkxEvents
.
ON_FROM_CHAIN_CHANGE
,
handler
:
(
token
)
=>
{
//
}
}
,
]
const
{
updateListeners
}
=
createOkxSwapWidget
(
container
,
{
params
,
listeners
,
provider
}
)

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="使用-widget">使用 Widget<a class="index_header-anchor__Xqb+L" href="#使用-widget" style="opacity:0">#</a></h1>
<!-- -->
<p>本文将告诉你如何将功能强大的欧易 Widget 与你的产品进行整合，让你只需 30 分钟即可搭建一个高效交易界面！</p>
<!-- -->
<h2 data-content="安装" id="安装">安装<a class="index_header-anchor__Xqb+L" href="#安装" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">yarn</span> <span class="token function">add</span> @okxweb3/dex-widget
// or
<span class="token function">npm</span> <span class="token function">install</span> @okxweb3/dex-widget
// or
<span class="token function">pnpm</span> <span class="token function">add</span> @okxweb3/dex-widget
</code></pre></div>
<h2 data-content="快速开始" id="快速开始">快速开始<a class="index_header-anchor__Xqb+L" href="#快速开始" style="opacity:0">#</a></h2>
<!-- -->
<p>下方的例子将向你演示如何在一个 React 项目中使用 <code>@okxweb3/dex-widget</code>。你还可以通过此<a class="items-center" href="https://github.com/okx/dex-widget/tree/develop/packages/widget-configurator/src/react-cra" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">链接<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>查看更多例子。</p>
<p>实际 Demo：<a class="items-center" href="https://okx.github.io/dex-widget/" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://okx.github.io/dex-widget/<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">React</span><span class="token punctuation">,</span> <span class="token punctuation">{</span> useRef<span class="token punctuation">,</span> useEffect <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'react'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">ReactDOM</span></span> <span class="token keyword module">from</span> <span class="token string">'react-dom/client'</span><span class="token punctuation">;</span>

<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> createOkxSwapWidget <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@okxweb3/dex-widget'</span><span class="token punctuation">;</span>

<span class="token keyword">function</span> <span class="token function"><span class="token maybe-class-name">App</span></span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> widgetRef <span class="token operator">=</span> <span class="token function">useRef</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token function">useEffect</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">width</span><span class="token operator">:</span> <span class="token number">375</span><span class="token punctuation">,</span>
      <span class="token literal-property property">providerType</span><span class="token operator">:</span> <span class="token string">'EVM'</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token keyword">const</span> provider <span class="token operator">=</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">ethereum</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> listeners <span class="token operator">=</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">event</span><span class="token operator">:</span> <span class="token string">'ON_CONNECT_WALLET'</span><span class="token punctuation">,</span>
        <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
          provider<span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">;</span>

    <span class="token keyword">const</span> instance <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>widgetRef<span class="token punctuation">.</span><span class="token property-access">current</span><span class="token punctuation">,</span> <span class="token punctuation">{</span>
      params<span class="token punctuation">,</span>
      provider<span class="token punctuation">,</span>
      listeners<span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token keyword control-flow">return</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      instance<span class="token punctuation">.</span><span class="token method function property-access">destroy</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword control-flow">return</span> <span class="token operator">&lt;</span>div ref<span class="token operator">=</span><span class="token punctuation">{</span>widgetRef<span class="token punctuation">}</span> <span class="token operator">/</span><span class="token operator">&gt;</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> root <span class="token operator">=</span> <span class="token maybe-class-name">ReactDOM</span><span class="token punctuation">.</span><span class="token method function property-access">createRoot</span><span class="token punctuation">(</span><span class="token dom variable">document</span><span class="token punctuation">.</span><span class="token method function property-access">getElementById</span><span class="token punctuation">(</span><span class="token string">'root'</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
root<span class="token punctuation">.</span><span class="token method function property-access">render</span><span class="token punctuation">(</span>
  <span class="token operator">&lt;</span><span class="token maybe-class-name">React</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">StrictMode</span></span><span class="token operator">&gt;</span>
    <span class="token operator">&lt;</span><span class="token maybe-class-name">App</span> <span class="token operator">/</span><span class="token operator">&gt;</span>
  <span class="token operator">&lt;</span><span class="token operator">/</span><span class="token maybe-class-name">React</span><span class="token punctuation">.</span><span class="token property-access"><span class="token maybe-class-name">StrictMode</span></span><span class="token operator">&gt;</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h2 data-content="钱包提供方" id="钱包提供方">钱包提供方<a class="index_header-anchor__Xqb+L" href="#钱包提供方" style="opacity:0">#</a></h2>
<!-- -->
<p>如果需要连接钱包，你可以从你的应用中传递钱包提供方信息。同时添加 ON_CONNECT_WALLET 事件，即可无缝连接并使用 Widget。</p>
<!-- -->
<ul>
<li>如果提供方是在 Ethereum 或其他 EVM 网络上，它必须要符合 EIP-1193 才能创建交易界面。</li>
<li>如果提供方是在 Solana 网络上，它必须从你的应用中传递钱包提供方的信息。</li>
</ul>
<div class="remark-highlight"><pre class="language-typeScript"><code class="language-typeScript"><span class="token keyword">import</span> <span class="token punctuation">{</span> createOkxSwapWidget<span class="token punctuation">,</span> ProviderType <span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@okxweb3/dex-widget'</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> widgetEthInstance <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>
  document<span class="token punctuation">.</span><span class="token function">getElementById</span><span class="token punctuation">(</span><span class="token string">'widget'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    params<span class="token operator">:</span> <span class="token punctuation">{</span>
      providerType<span class="token operator">:</span> ProviderType<span class="token punctuation">.</span><span class="token constant">EVM</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    provider<span class="token operator">:</span> window<span class="token punctuation">.</span>ethereum<span class="token punctuation">,</span> <span class="token comment">// e.g. window.okexchain</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> widgetSolanaInstance <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>
  document<span class="token punctuation">.</span><span class="token function">getElementById</span><span class="token punctuation">(</span><span class="token string">'widget'</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
  <span class="token punctuation">{</span>
    params<span class="token operator">:</span> <span class="token punctuation">{</span>
      providerType<span class="token operator">:</span> ProviderType<span class="token punctuation">.</span><span class="token constant">SOLANA</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    provider<span class="token operator">:</span> window<span class="token punctuation">.</span>solana<span class="token punctuation">,</span> <span class="token comment">// window.okexchain.solana</span>
  <span class="token punctuation">}</span>
<span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<!-- -->
<p>Rainbow 连接钱包组件的示例可参考这个<a class="items-center" href="https://github.com/okx/dex-widget/blob/faf69c76b90268f2352507c9a90fb37bb80fdbc7/example/widget-demo/src/main.tsx#L22" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">链接<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a>。</p>
<!-- -->
<h2 data-content="参数" id="参数">参数<a class="index_header-anchor__Xqb+L" href="#参数" style="opacity:0">#</a></h2>
<!-- -->
<p>下方表格内是对 Params 的描述。</p>
<!-- -->
<div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>默认值</th><th>描述</th></tr></thead><tbody><tr><td><code>width</code></td><td><code>number</code></td><td>450</td><td>用 css 值 (px) 表示的 Widget 宽度。如果未设置宽度，则宽度的展示样式为：&gt;767px 显示为 450 px， &lt;768 px 显示为 100%， &lt; 375 px 则显示为 375 px。</td></tr><tr><td><code>theme</code></td><td><code>THEME</code></td><td>light</td><td>兑换 Widget 提供默认的日间、夜间主题选项。你可以按下方示例来切换 Widget 的主题。</td></tr><tr><td><code>lang</code></td><td><code>string</code></td><td>en_us</td><td>你可以调整 Widget 所使用的语言，请在多语言配置部分了解更多细节信息。</td></tr><tr><td><code>tradeType</code></td><td><code>TradeType</code></td><td>auto</td><td>交易的类型，可以是“swap”、“bridge”，或“auto”。注意：“自动”包含“swap”和“bridge”。</td></tr><tr><td><code>chainIds</code></td><td><code>Array&lt;string&gt;</code></td><td>[]</td><td>承载单链兑换的区块链的 ID，请在 ChainId 配置部分查看你可选的所有网络。</td></tr><tr><td><code>feeConfig</code></td><td><code>IFeeConfig</code></td><td>{}</td><td>你可以选择在 Widget 中为所有交易类型设置一个费率，请在自定义费率部分了解详情。</td></tr><tr><td><code>tokenPair</code></td><td><code>ITokenPair</code></td><td>{}</td><td>你所设定使用的兑换默认代币对，请在默认币对配置部分了解详情。</td></tr><tr><td><code>bridgeTokenPair</code></td><td><code>ITokenPair</code></td><td>{}</td><td>你所设定使用的跨链默认代币对，请在默认币对配置部分了解详情。</td></tr><tr><td><code>providerType</code></td><td><code>ProviderType</code></td><td>' '</td><td>ProviderType 是和提供方一致的类型参数，例如，如果提供方是 Solana，那么 providerType 就会是 SOLANA。</td></tr></tbody></table></div>
<h2 data-content="类型描述" id="类型描述">类型描述<a class="index_header-anchor__Xqb+L" href="#类型描述" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typeScript"><code class="language-typeScript"><span class="token keyword">interface</span> <span class="token class-name">IFeeConfig</span> <span class="token punctuation">{</span>
    <span class="token punctuation">[</span>key<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        feePercent<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
        referrerAddress<span class="token operator">?</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token punctuation">[</span>key<span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
                feePercent<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">interface</span> <span class="token class-name">ITokenPair</span> <span class="token punctuation">{</span>
    fromChain<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
    toChain<span class="token operator">:</span> <span class="token builtin">string</span> <span class="token operator">|</span> <span class="token builtin">number</span><span class="token punctuation">;</span>
    fromToken<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
    toToken<span class="token operator">?</span><span class="token operator">:</span> <span class="token builtin">string</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token keyword">enum</span> ProviderType <span class="token punctuation">{</span>
    <span class="token constant">EVM</span> <span class="token operator">=</span> <span class="token string">'EVM'</span><span class="token punctuation">,</span>
    <span class="token constant">SOLANA</span> <span class="token operator">=</span> <span class="token string">'SOLANA'</span><span class="token punctuation">,</span>
    <span class="token constant">WALLET_CONNECT</span> <span class="token operator">=</span> <span class="token string">'WALLET_CONNECT'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token keyword">enum</span> TradeType <span class="token punctuation">{</span>
    <span class="token constant">SWAP</span> <span class="token operator">=</span> <span class="token string">'swap'</span><span class="token punctuation">,</span>
    <span class="token constant">BRIDGE</span> <span class="token operator">=</span> <span class="token string">'bridge'</span><span class="token punctuation">,</span>
    <span class="token constant">AUTO</span> <span class="token operator">=</span> <span class="token string">'auto'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token keyword">enum</span> <span class="token constant">THEME</span> <span class="token punctuation">{</span>
    <span class="token constant">LIGHT</span> <span class="token operator">=</span> <span class="token string">'light'</span><span class="token punctuation">,</span>
    <span class="token constant">DARK</span> <span class="token operator">=</span> <span class="token string">'dark'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="多语言配置" id="多语言配置">多语言配置<a class="index_header-anchor__Xqb+L" href="#多语言配置" style="opacity:0">#</a></h2>
<div class="index_table__kvZz5"><table><thead><tr><th>lang</th><th>描述</th></tr></thead><tbody><tr><td><code>en_us</code></td><td>English，默认</td></tr><tr><td><code>zh_cn</code></td><td>简体中文</td></tr><tr><td><code>zh_tw</code></td><td>繁體中文</td></tr><tr><td><code>fr_fr</code></td><td>Français (Afrique)</td></tr><tr><td><code>id_id</code></td><td>Bahasa Indonesia</td></tr><tr><td><code>ru_ru</code></td><td>Русский</td></tr><tr><td><code>tr_tr</code></td><td>Türkçe</td></tr><tr><td><code>vi_vn</code></td><td>Tiếng Việt</td></tr><tr><td><code>de_de</code></td><td>Deutsch</td></tr><tr><td><code>it_it</code></td><td>Italiano</td></tr><tr><td><code>pl_pl</code></td><td>Polski</td></tr><tr><td><code>pt_pt</code></td><td>Português (Portugal)</td></tr><tr><td><code>es_es</code></td><td>Español (España)</td></tr><tr><td><code>pt_br</code></td><td>Português (Brasil)</td></tr><tr><td><code>es_419</code></td><td>Español (Latinoamérica)</td></tr><tr><td><code>cs_cz</code></td><td>Čeština</td></tr><tr><td><code>ro_ro</code></td><td>Română</td></tr><tr><td><code>uk_ua</code></td><td>Українська</td></tr><tr><td><code>ar_eh</code></td><td>العربية</td></tr><tr><td><code>nl_nl</code></td><td>Nederlands</td></tr></tbody></table></div>
<h2 data-content="ChainId 配置" id="chainid-配置">ChainId 配置<a class="index_header-anchor__Xqb+L" href="#chainid-配置" style="opacity:0">#</a></h2>
<div class="index_table__kvZz5"><table><thead><tr><th>网络</th><th>ChainId</th><th>主网币合约地址</th></tr></thead><tbody><tr><td>Ethereum</td><td>1</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Solana</td><td>501</td><td>11111111111111111111111111111111</td></tr><tr><td>Arbitrum</td><td>42161</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Base</td><td>8453</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Sonic</td><td>146</td><td>0x4Efa4b8545a3a77D80Da3ECC8F81EdB1a4bda783</td></tr><tr><td>Optimism</td><td>10</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>zkSync Era</td><td>324</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>BNB Chain</td><td>56</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Linea</td><td>59144</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Polygon</td><td>137</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Avalanche C</td><td>43114</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Mantle</td><td>5000</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Scroll</td><td>534352</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>X layer</td><td>196</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr><tr><td>Blast</td><td>81457</td><td>0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE</td></tr></tbody></table></div>
<h2 data-content="默认币对配置" id="默认币对配置">默认币对配置<a class="index_header-anchor__Xqb+L" href="#默认币对配置" style="opacity:0">#</a></h2>
<!-- -->
<p><code>tokenPair</code>: 如果没有配置，则单链兑换将默认设置在 Ethereum 网络，且 <code>fromToken</code> 为 ETH，<code>toToken</code> 为 USDC。</p>
<!-- -->
<!-- -->
<p><code>bridgeTokenPair</code>: 如果没有配置，则跨链兑换将默认设置为从 Ethereum 跨链至 BNB Chain，且 <code>fromToken</code> 为 ETH，<code>toToken</code> 为 BNB。</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token keyword module">import</span> <span class="token imports"><span class="token maybe-class-name">React</span><span class="token punctuation">,</span> <span class="token punctuation">{</span> useEffect<span class="token punctuation">,</span> useRef <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'react'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span>
  <span class="token maybe-class-name">OkxSwapWidgetParams</span><span class="token punctuation">,</span>
  <span class="token maybe-class-name">ProviderType</span><span class="token punctuation">,</span>
  <span class="token maybe-class-name">TradeType</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@okxweb3/dex-widget'</span><span class="token punctuation">;</span>

<span class="token keyword">const</span> provider <span class="token operator">=</span> <span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">ethereum</span><span class="token punctuation">;</span>

<span class="token keyword module">export</span> <span class="token keyword">function</span> <span class="token function"><span class="token maybe-class-name">EvmWidget</span></span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
  <span class="token keyword">const</span> widgetRef <span class="token operator">=</span> <span class="token function">useRef</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword">const</span> params <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">chainIds</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token string">'1'</span><span class="token punctuation">,</span> <span class="token string">'10'</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token literal-property property">lang</span><span class="token operator">:</span> <span class="token string">'zh_cn'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">providerType</span><span class="token operator">:</span> <span class="token maybe-class-name">ProviderType</span><span class="token punctuation">.</span><span class="token constant">EVM</span><span class="token punctuation">,</span>
    <span class="token literal-property property">theme</span><span class="token operator">:</span> <span class="token string">'dark'</span><span class="token punctuation">,</span>
    <span class="token literal-property property">tradeType</span><span class="token operator">:</span> <span class="token maybe-class-name">TradeType</span><span class="token punctuation">.</span><span class="token constant">AUTO</span><span class="token punctuation">,</span>
    <span class="token literal-property property">tokenPair</span><span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">fromChain</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token comment">//ETH</span>
      <span class="token literal-property property">toChain</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token comment">// ETH</span>
      <span class="token literal-property property">fromToken</span><span class="token operator">:</span> <span class="token string">'0xdac17f958d2ee523a2206206994597c13d831ec7'</span><span class="token punctuation">,</span> <span class="token comment">// USDT</span>
      <span class="token literal-property property">toToken</span><span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// ETH</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token literal-property property">bridgeTokenPair</span><span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token literal-property property">fromChain</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span> <span class="token comment">//ETH</span>
      <span class="token literal-property property">toChain</span><span class="token operator">:</span> <span class="token number">56</span><span class="token punctuation">,</span> <span class="token comment">// BNB</span>
      <span class="token literal-property property">fromToken</span><span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// ETH</span>
      <span class="token literal-property property">toToken</span><span class="token operator">:</span> <span class="token string">'0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'</span><span class="token punctuation">,</span> <span class="token comment">// BNB</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token keyword">const</span> initialConfig <span class="token operator">=</span> <span class="token punctuation">{</span>
    params<span class="token punctuation">,</span>
    provider<span class="token punctuation">,</span>
    <span class="token literal-property property">listeners</span><span class="token operator">:</span> <span class="token punctuation">[</span>
      <span class="token punctuation">{</span>
        <span class="token literal-property property">event</span><span class="token operator">:</span> <span class="token string">'ON_CONNECT_WALLET'</span><span class="token punctuation">,</span>
        <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token parameter">token<span class="token punctuation">,</span> preToken</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
          provider<span class="token punctuation">.</span><span class="token method function property-access">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">]</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">;</span>

  <span class="token function">useEffect</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
    <span class="token keyword">const</span> widgetHandler <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>widgetRef<span class="token punctuation">.</span><span class="token property-access">current</span><span class="token punctuation">,</span> initialConfig<span class="token punctuation">)</span><span class="token punctuation">;</span>

    <span class="token keyword control-flow">return</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      widgetHandler<span class="token operator">?.</span><span class="token method function property-access">destroy</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span> <span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

  <span class="token keyword control-flow">return</span> <span class="token operator">&lt;</span>div ref<span class="token operator">=</span><span class="token punctuation">{</span>widgetRef<span class="token punctuation">}</span> <span class="token operator">/</span><span class="token operator">&gt;</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>
</code></pre></div>
<div class="index_table__kvZz5"><table><thead><tr><th>参数</th><th>类型</th><th>描述</th></tr></thead><tbody><tr><td>fromChain</td><td>String</td><td>fromToken 所属的源链 ID (例如，1：Ethereum，可在 ChainId 配置部分查看所有已支持的网络和对应的链 ID)。</td></tr><tr><td>fromToken</td><td>String</td><td>试图卖出的代币的合约地址，例如 ETH：0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE。如果 fromToken 是某一区块链的主网币，请查看链 ID 以获取合约地址。</td></tr><tr><td>toChain</td><td>String</td><td>toToken 所属的目标链 ID (例如，1：Ethereum，可在 ChainId 配置部分查看所有已支持的网络和对应的链 ID)。</td></tr><tr><td>toToken</td><td>String</td><td>试图卖出的代币的合约地址，例如 USDC：0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48。如果 toToken 是某一区块链的主网币，请查看链 ID 以获取合约地址。</td></tr></tbody></table></div>
<h2 data-content="自定义费率" id="自定义费率">自定义费率<a class="index_header-anchor__Xqb+L" href="#自定义费率" style="opacity:0">#</a></h2>
<!-- -->
<p>添加下列参数后，你即可启用 feeConfig 在你的用户在各个网络上执行交易时，通过 Widget 收取手续费：</p>
<p>你需要声明 chainId、feePercent 和 referrerAddress。</p>
<p>在 Ethereum 和其他 EVM 网络，设置 feePercent 和 referrerAddress 即可收取手续费。</p>
<p>在 Solana 网络，SOL 和 SPL 代币的分佣有些不同。SOL 分佣使用的是钱包地址，而 SPL 代币分佣使用的是代币账号。</p>
<p>你可以添加 feePercent 以调整 referrerAddress 所收到的分佣的费率。</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token comment">// EVM feeConfig example</span>
<span class="token literal-property property">feeConfig</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token punctuation">[</span>chainId<span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token string">'xxx'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token number">0</span><span class="token operator">-</span><span class="token number">3</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Solana feeConfig example</span>

<span class="token literal-property property">feeConfig</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token punctuation">[</span>chainId<span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token punctuation">[</span><span class="token number">0</span><span class="token operator">-</span><span class="token number">3</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
        <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token punctuation">{</span>
          <span class="token punctuation">[</span>tokenContractA<span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">referrerAccount</span><span class="token operator">:</span> <span class="token string">'account/abc'</span><span class="token punctuation">,</span>
            <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token string">'1'</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span><span class="token punctuation">,</span>
          <span class="token punctuation">[</span>tokenContractB<span class="token punctuation">]</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">referrerAccount</span><span class="token operator">:</span> <span class="token string">'account/abc'</span><span class="token punctuation">,</span>
            <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token string">'2'</span><span class="token punctuation">,</span>
          <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>

<span class="token comment">// Full Example</span>
<span class="token literal-property property">feeConfig</span><span class="token operator">:</span> <span class="token punctuation">{</span>
  <span class="token number">1</span><span class="token operator">:</span> <span class="token punctuation">{</span><span class="token comment">// Ethereum chainId</span>
    <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token comment">// The percentage of Fee</span>
    <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token string">'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'</span><span class="token punctuation">,</span> <span class="token comment">// eth address that receives the fee</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token number">56</span><span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">// Bnb Chain chainId</span>
    <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span> <span class="token comment">//</span>
    <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token string">'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'</span><span class="token punctuation">,</span> <span class="token comment">// bnb address that receives the fee</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token number">501</span><span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">// solana chainId</span>
    <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token punctuation">{</span>
      <span class="token string-property property">'11111111111111111111111111111111'</span><span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">//solana SOL contract address</span>
        <span class="token literal-property property">account</span><span class="token operator">:</span> <span class="token string">'6rocMMKG1DNg93RDfVL2xVdrA5nbAT8cFMbdvVTHUF4m'</span><span class="token punctuation">,</span>
        <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token literal-property property">EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v</span><span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">//solana USDC contract address</span>
        <span class="token literal-property property">account</span><span class="token operator">:</span> <span class="token string">'C6XW7mFvCuVxYFTi9zTQrUcwkvhfGYAvuosXz6pLDZsa'</span><span class="token punctuation">,</span> <span class="token comment">//solana USDC token account that receives the fee</span>
        <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
      <span class="token literal-property property">JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN</span><span class="token operator">:</span> <span class="token punctuation">{</span> <span class="token comment">//solana JUP contract address</span>
        <span class="token literal-property property">account</span><span class="token operator">:</span> <span class="token string">'Ezq6jTC3CwnsXDSdtgy8Sa4xi1iA6fxuEeXxWFPLG9sc'</span><span class="token punctuation">,</span> <span class="token comment">//solana JUP token account that receives the fee</span>
        <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">1</span><span class="token punctuation">,</span>
      <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token number">8453</span><span class="token operator">:</span> <span class="token punctuation">{</span>
    <span class="token literal-property property">feePercent</span><span class="token operator">:</span> <span class="token number">3</span><span class="token punctuation">,</span>
    <span class="token literal-property property">referrerAddress</span><span class="token operator">:</span> <span class="token string">'0x38a3b108eb2b97c307bf5788909f8c12afd0cd6b'</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>
</code></pre></div>
<h2 data-content="feePercent" id="feepercent">feePercent<a class="index_header-anchor__Xqb+L" href="#feepercent" style="opacity:0">#</a></h2>
<!-- -->
<p>发送给分佣地址的 fromTokenAmount 的百分比。剩余的代币数量将被设置为卖出数量。费率用基点 (BPS) 计算，一个基点等于 0.01% (万分之一)。费率不能超过 3% (300 BPS)。</p>
<!-- -->
<h2 data-content="referrerAddress" id="referreraddress">referrerAddress<a class="index_header-anchor__Xqb+L" href="#referreraddress" style="opacity:0">#</a></h2>
<!-- -->
<p>referrerAddress 是接收手续费的地址。</p>
<p>请确保接收手续费的地址存在于参数表中所定义的对应网络之上。</p>
<!-- -->
<h2 data-content="Widget 更新" id="widget-更新">Widget 更新<a class="index_header-anchor__Xqb+L" href="#widget-更新" style="opacity:0">#</a></h2>
<h3 id="updateparams">updateParams<a class="index_header-anchor__Xqb+L" href="#updateparams" style="opacity:0">#</a></h3>
<!-- -->
<p>可更新的属性：theme、lang、width</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token comment">// 1. Create and initialize the widget</span>
<span class="token keyword">const</span> widgetHandler <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>container<span class="token punctuation">,</span> initialConfig<span class="token punctuation">)</span><span class="token punctuation">;</span>

<span class="token comment">// 2. Update the widget's parameters (e.g., change theme or size)</span>
widgetHandler<span class="token punctuation">.</span><span class="token method function property-access">updateParams</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
  <span class="token literal-property property">width</span><span class="token operator">:</span> <span class="token number">700</span><span class="token punctuation">,</span>
  <span class="token literal-property property">theme</span><span class="token operator">:</span> <span class="token string">'light'</span><span class="token punctuation">,</span>
  <span class="token literal-property property">lang</span><span class="token operator">:</span> <span class="token string">'tr_tr'</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h3 id="updateprovider">updateProvider<a class="index_header-anchor__Xqb+L" href="#updateprovider" style="opacity:0">#</a></h3>
<!-- -->
<p>Widget 支持 EVM 和 Solana。当从 EVM 切换到 Solana 时，请记得更新相应的 Widget 提供方，反之亦然。</p>
<p>如果首次渲染时没有传递提供方信息，并想要 Widget 响应钱包绑定，就需要调用 updateProvider。</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token comment">// 3. Update the provider if the user connects a different wallet, EVM =&gt; SOLANA</span>
widgetHandler<span class="token punctuation">.</span><span class="token method function property-access">updateProvider</span><span class="token punctuation">(</span><span class="token dom variable">window</span><span class="token punctuation">.</span><span class="token property-access">solana</span><span class="token punctuation">,</span> <span class="token maybe-class-name">ProviderType</span><span class="token punctuation">.</span><span class="token constant">SOLANA</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token comment">// SOLANA =&gt; EVM</span>
<span class="token comment">// widgetHandler.updateProvider(window.ethereum, ProviderType.EVM);</span>
</code></pre></div>
<h3 id="updatelisteners">updateListeners<a class="index_header-anchor__Xqb+L" href="#updatelisteners" style="opacity:0">#</a></h3>
<!-- -->
<p>你可以更新 Widget 监听的事件。</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javaScript"><code class="language-javaScript"><span class="token comment">// 4. Modify event listeners to handle new types of events</span>
widgetHandler<span class="token punctuation">.</span><span class="token method function property-access">updateListeners</span><span class="token punctuation">(</span><span class="token punctuation">[</span>
  <span class="token punctuation">{</span>
    <span class="token literal-property property">event</span><span class="token operator">:</span> <span class="token maybe-class-name">OkxEvents</span><span class="token punctuation">.</span><span class="token constant">ON_FROM_CHAIN_CHANGE</span><span class="token punctuation">,</span>
    <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token parameter">payload</span><span class="token punctuation">)</span> <span class="token arrow operator">=&gt;</span> <span class="token punctuation">{</span>
      <span class="token comment">//</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
  <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<ul>
<li>Listeners 主要用于监听 Widget 向外部暴露的接口，通过不同事件进行定制化处理。而 updateListeners 则用于在切换链后更新定制化处理。</li>
<li>通过添加事件监听器，可以捕获并处理从 iframe 中传递出来的事件数据。这些数据通常是 iframe 内部发生的事件或状态变化，并通过事件传递到外部页面。</li>
<li>接收到的数据可以根据需求进行灵活处理和操作。这意味着你可以根据传递的数据类型或内容，执行不同的逻辑或更新界面元素。</li>
<li>通过 updateListeners 方法，你可以为不同类型的事件 (如 OkxEvents.ON_FROM_CHAIN_CHANGE) 添加处理函数。当事件触发时，处理函数会接收到相关的 payload 数据，以便你进一步操作。</li>
</ul>
<h3 id="destroy">destroy<a class="index_header-anchor__Xqb+L" href="#destroy" style="opacity:0">#</a></h3>
<!-- -->
<p>当清除 Widget 模块时，调用此方法</p>
<!-- -->
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"><span class="token keyword">const</span> widgetHandler <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>container<span class="token punctuation">,</span> initialConfig<span class="token punctuation">)</span><span class="token punctuation">;</span>

widgetHandler<span class="token punctuation">.</span><span class="token method function property-access">destory</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
</code></pre></div>
<h4 id="注意：">注意：<a class="index_header-anchor__Xqb+L" href="#注意：" style="opacity:0">#</a></h4>
<ul>
<li>每当你刷新和更新时，请确保调用 destroy 方法来清除先前绑定的事件，以避免出现重复订单请求。</li>
</ul>
<h2 data-content="事件监听" id="事件监听">事件监听<a class="index_header-anchor__Xqb+L" href="#事件监听" style="opacity:0">#</a></h2>
<!-- -->
<p>Widget 为 ON_CONNECT_WALLET 和 ON_FROM_CHAIN_CHANGE 提供事件监听。</p>
<!-- -->
<ul>
<li>ON_CONNECT_WALLET：当 Widget 未连接钱包并点击了连接钱包按钮时触发此事件。</li>
<li>ON_FROM_CHAIN_CHANGE： 当 fromChain 发生变化时会触发此事件。</li>
</ul>
<!-- -->
<p>使用方法如下：</p>
<!-- -->
<div class="remark-highlight"><pre class="language-typeScript"><code class="language-typeScript"><span class="token keyword">import</span> <span class="token punctuation">{</span>createOkxSwapWidget<span class="token punctuation">,</span> OkxSwapWidgetParams<span class="token punctuation">,</span> OkxEventListeners<span class="token punctuation">,</span> OkxEvents<span class="token punctuation">}</span> <span class="token keyword">from</span> <span class="token string">'@okxweb3/dex-widget'</span>

<span class="token keyword">const</span> params<span class="token operator">:</span> OkxSwapWidgetParams <span class="token operator">=</span> <span class="token punctuation">{</span>
    <span class="token comment">// ...</span>
<span class="token punctuation">}</span>

<span class="token keyword">const</span> listeners<span class="token operator">:</span> OkxEventListeners <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token punctuation">{</span>
        event<span class="token operator">:</span> OkxEvents<span class="token punctuation">.</span><span class="token constant">ON_CONNECT_WALLET</span><span class="token punctuation">,</span>
        <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token comment">// open connect wallet method, eg openConnectModal of the rainbow kit.</span>
            window<span class="token punctuation">.</span>ethereum<span class="token punctuation">.</span><span class="token function">enable</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
    <span class="token punctuation">{</span>
        event<span class="token operator">:</span> OkxEvents<span class="token punctuation">.</span><span class="token constant">ON_FROM_CHAIN_CHANGE</span><span class="token punctuation">,</span>
        <span class="token function-variable function">handler</span><span class="token operator">:</span> <span class="token punctuation">(</span>token<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
            <span class="token comment">//</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span><span class="token punctuation">,</span>
<span class="token punctuation">]</span>

<span class="token keyword">const</span> <span class="token punctuation">{</span> updateListeners <span class="token punctuation">}</span> <span class="token operator">=</span> <span class="token function">createOkxSwapWidget</span><span class="token punctuation">(</span>container<span class="token punctuation">,</span> <span class="token punctuation">{</span> params<span class="token punctuation">,</span> listeners<span class="token punctuation">,</span> provider <span class="token punctuation">}</span><span class="token punctuation">)</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "资源",
    "DEX Widget"
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
    "安装",
    "快速开始",
    "钱包提供方",
    "参数",
    "类型描述",
    "多语言配置",
    "ChainId 配置",
    "默认币对配置",
    "自定义费率",
    "feePercent",
    "referrerAddress",
    "Widget 更新",
    "事件监听"
  ]
}
```

</details>
