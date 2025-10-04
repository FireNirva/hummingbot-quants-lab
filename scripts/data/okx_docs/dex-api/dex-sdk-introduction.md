# 介绍   | DEX SDK  | 资源 | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-sdk-introduction#客户端初始化  
**抓取时间:** 2025-05-27 01:10:44  
**字数:** 260

## 导航路径
DEX API > 资源 > 介绍

## 目录
- 安装 SDK
- 环境设置
- 客户端初始化

---

介绍
#
OKX DEX SDK 是一个 typescript 工具包，可供开发人员将 OKX DEX API 功能集成到他们的 App 里。
GitHub 存储库：
https://github.com/okx/okx-dex-sdk
如何操作：
https://github.com/okx/okx-dex-sdk?tab=readme-ov-file#usage
安装 SDK
#
npm
install
@okx-dex/okx-dex-sdk
# or
yarn
add
@okx-dex/okx-dex-sdk
# or
pnpm
add
@okx-dex/okx-dex-sdk
环境设置
#
请使用你的 API 凭证和钱包信息来创建一个 .env 文件。
# OKX API Credentials
OKX_API_KEY
=
your_api_key
OKX_SECRET_KEY
=
your_secret_key
OKX_API_PASSPHRASE
=
your_passphrase
OKX_PROJECT_ID
=
your_project_id
# Solana Configuration
SOLANA_RPC_URL
=
your_solana_rpc_url
SOLANA_WALLET_ADDRESS
=
your_solana_wallet_address
SOLANA_PRIVATE_KEY
=
your_solana_private_key
客户端初始化
#
为 DEX 客户端创建文件 (例如 DexClient.ts):
本文以 Solana 为例，你可以根据你的开发需要更改依赖组件。
#
OKX
API
Credentials
// DexClient.ts
import
{
OKXDexClient
}
from
'@okx-dex/okx-dex-sdk'
;
import
'dotenv/config'
;
// Validate environment variables
const
requiredEnvVars
=
[
'OKX_API_KEY'
,
'OKX_SECRET_KEY'
,
'OKX_API_PASSPHRASE'
,
'OKX_PROJECT_ID'
,
'SOLANA_WALLET_ADDRESS'
,
'SOLANA_PRIVATE_KEY'
,
'SOLANA_RPC_URL'
]
;
for
(
const
envVar
of
requiredEnvVars
)
{
if
(
!
process
.
env
[
envVar
]
)
{
throw
new
Error
(
`
Missing required environment variable:
${
envVar
}
`
)
;
}
}
// Initialize the client
export
const
client
=
new
OKXDexClient
(
{
apiKey
:
process
.
env
.
OKX_API_KEY
!
,
secretKey
:
process
.
env
.
OKX_SECRET_KEY
!
,
apiPassphrase
:
process
.
env
.
OKX_API_PASSPHRASE
!
,
projectId
:
process
.
env
.
OKX_PROJECT_ID
!
,
solana
:
{
connection
:
{
rpcUrl
:
process
.
env
.
SOLANA_RPC_URL
!
,
wsEndpoint
:
process
.
env
.
SOLANA_WS_URL
,
confirmTransactionInitialTimeout
:
5000
}
,
walletAddress
:
process
.
env
.
SOLANA_WALLET_ADDRESS
!
,
privateKey
:
process
.
env
.
SOLANA_PRIVATE_KEY
!
,
computeUnits
:
300000
,
maxRetries
:
3
}
}
)
;

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="介绍">介绍<a class="index_header-anchor__Xqb+L" href="#介绍" style="opacity:0">#</a></h1>
<p>OKX DEX SDK 是一个 typescript 工具包，可供开发人员将 OKX DEX API 功能集成到他们的 App 里。<br/></p>
<p>GitHub 存储库： <a class="items-center" href="https://github.com/okx/okx-dex-sdk" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/okx-dex-sdk<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a> <br/></p>
<p>如何操作： <a class="items-center" href="https://github.com/okx/okx-dex-sdk?tab=readme-ov-file#usage" rel="nofollow noreferrer" style="display:inline-flex;line-height:16px" target="_blank">https://github.com/okx/okx-dex-sdk?tab=readme-ov-file#usage<i aria-hidden="true" class="icon iconfont doc-ssr-okds-open-link" role="img" style="font-size:24px;color:#0569FF;margin-left:2px"></i></a></p>
<h2 data-content="安装 SDK" id="安装-sdk">安装 SDK<a class="index_header-anchor__Xqb+L" href="#安装-sdk" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token function">npm</span> <span class="token function">install</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">yarn</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
<span class="token comment"># or</span>
<span class="token function">pnpm</span> <span class="token function">add</span> @okx-dex/okx-dex-sdk
</code></pre></div>
<h2 data-content="环境设置" id="环境设置">环境设置<a class="index_header-anchor__Xqb+L" href="#环境设置" style="opacity:0">#</a></h2>
<p>请使用你的 API 凭证和钱包信息来创建一个 .env 文件。</p>
<div class="remark-highlight"><pre class="language-bash"><code class="language-bash"><span class="token comment"># OKX API Credentials</span>
<span class="token assign-left variable">OKX_API_KEY</span><span class="token operator">=</span>your_api_key
<span class="token assign-left variable">OKX_SECRET_KEY</span><span class="token operator">=</span>your_secret_key
<span class="token assign-left variable">OKX_API_PASSPHRASE</span><span class="token operator">=</span>your_passphrase
<span class="token assign-left variable">OKX_PROJECT_ID</span><span class="token operator">=</span>your_project_id
<span class="token comment"># Solana Configuration</span>
<span class="token assign-left variable">SOLANA_RPC_URL</span><span class="token operator">=</span>your_solana_rpc_url
<span class="token assign-left variable">SOLANA_WALLET_ADDRESS</span><span class="token operator">=</span>your_solana_wallet_address
<span class="token assign-left variable">SOLANA_PRIVATE_KEY</span><span class="token operator">=</span>your_solana_private_key
</code></pre></div>
<h2 data-content="客户端初始化" id="客户端初始化">客户端初始化<a class="index_header-anchor__Xqb+L" href="#客户端初始化" style="opacity:0">#</a></h2>
<p>为 DEX 客户端创建文件 (例如 DexClient.ts):
本文以 Solana 为例，你可以根据你的开发需要更改依赖组件。</p>
<div class="remark-highlight"><pre class="language-javascript"><code class="language-javascript"># <span class="token constant">OKX</span> <span class="token constant">API</span> <span class="token maybe-class-name">Credentials</span>
<span class="token comment">// DexClient.ts</span>
<span class="token keyword module">import</span> <span class="token imports"><span class="token punctuation">{</span> <span class="token maybe-class-name">OKXDexClient</span> <span class="token punctuation">}</span></span> <span class="token keyword module">from</span> <span class="token string">'@okx-dex/okx-dex-sdk'</span><span class="token punctuation">;</span>
<span class="token keyword module">import</span> <span class="token string">'dotenv/config'</span><span class="token punctuation">;</span>
<span class="token comment">// Validate environment variables</span>
<span class="token keyword">const</span> requiredEnvVars <span class="token operator">=</span> <span class="token punctuation">[</span>
    <span class="token string">'OKX_API_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_SECRET_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_API_PASSPHRASE'</span><span class="token punctuation">,</span>
    <span class="token string">'OKX_PROJECT_ID'</span><span class="token punctuation">,</span>
    <span class="token string">'SOLANA_WALLET_ADDRESS'</span><span class="token punctuation">,</span>
    <span class="token string">'SOLANA_PRIVATE_KEY'</span><span class="token punctuation">,</span>
    <span class="token string">'SOLANA_RPC_URL'</span>
<span class="token punctuation">]</span><span class="token punctuation">;</span>
<span class="token keyword control-flow">for</span> <span class="token punctuation">(</span><span class="token keyword">const</span> envVar <span class="token keyword">of</span> requiredEnvVars<span class="token punctuation">)</span> <span class="token punctuation">{</span>
    <span class="token keyword control-flow">if</span> <span class="token punctuation">(</span><span class="token operator">!</span>process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">[</span>envVar<span class="token punctuation">]</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
        <span class="token keyword control-flow">throw</span> <span class="token keyword">new</span> <span class="token class-name">Error</span><span class="token punctuation">(</span><span class="token template-string"><span class="token template-punctuation string">`</span><span class="token string">Missing required environment variable: </span><span class="token interpolation"><span class="token interpolation-punctuation punctuation">${</span>envVar<span class="token interpolation-punctuation punctuation">}</span></span><span class="token template-punctuation string">`</span></span><span class="token punctuation">)</span><span class="token punctuation">;</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
<span class="token comment">// Initialize the client</span>
<span class="token keyword module">export</span> <span class="token keyword">const</span> client <span class="token operator">=</span> <span class="token keyword">new</span> <span class="token class-name">OKXDexClient</span><span class="token punctuation">(</span><span class="token punctuation">{</span>
    <span class="token literal-property property">apiKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">secretKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_SECRET_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">apiPassphrase</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_API_PASSPHRASE</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">projectId</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">OKX_PROJECT_ID</span><span class="token operator">!</span><span class="token punctuation">,</span>
    <span class="token literal-property property">solana</span><span class="token operator">:</span> <span class="token punctuation">{</span>
        <span class="token literal-property property">connection</span><span class="token operator">:</span> <span class="token punctuation">{</span>
            <span class="token literal-property property">rpcUrl</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_RPC_URL</span><span class="token operator">!</span><span class="token punctuation">,</span>
            <span class="token literal-property property">wsEndpoint</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_WS_URL</span><span class="token punctuation">,</span>
            <span class="token literal-property property">confirmTransactionInitialTimeout</span><span class="token operator">:</span> <span class="token number">5000</span>
        <span class="token punctuation">}</span><span class="token punctuation">,</span>
        <span class="token literal-property property">walletAddress</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_WALLET_ADDRESS</span><span class="token operator">!</span><span class="token punctuation">,</span>
        <span class="token literal-property property">privateKey</span><span class="token operator">:</span> process<span class="token punctuation">.</span><span class="token property-access">env</span><span class="token punctuation">.</span><span class="token constant">SOLANA_PRIVATE_KEY</span><span class="token operator">!</span><span class="token punctuation">,</span>
        <span class="token literal-property property">computeUnits</span><span class="token operator">:</span> <span class="token number">300000</span><span class="token punctuation">,</span>
        <span class="token literal-property property">maxRetries</span><span class="token operator">:</span> <span class="token number">3</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
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
    "介绍"
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
    "安装 SDK",
    "环境设置",
    "客户端初始化"
  ]
}
```

</details>
