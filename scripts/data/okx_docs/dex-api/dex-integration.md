# DEX 集成 | 兑换 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-integration#amm-接入示例  
**抓取时间:** 2025-05-27 01:40:25  
**字数:** 3485

## 导航路径
DEX API > 交易 API > DEX 集成

## 目录
- AMM 接入示例
- 基于 Raydium CLMM 的实现例子

---

DEX 集成
#
为了成功将您的 DEX 集成到 OKX 路由引擎中，请按照以下步骤操作：
提供与 OKX DEX AMM 接口兼容的 DEX SDK：
我们需要一个与我们的 AMM（自动化市场制造商）接口完全兼容的 DEX SDK。该SDK将允许我们与您的 DEX 进行通信并集成其功能，使流动性提供和交易执行能够在我们的平台上无缝进行。SDK 应能够处理定价、订单匹配、流动性池交互和交易执行等关键功能。
允许我们分叉您的 SDK：
为了确保长期的维护和用户支持，我们需要能够分叉您的 SDK。这意味着我们需要创建自己版本的 SDK 以供集成使用。通过这样做，我们可以：
确保 SDK 的稳定性。
独立维护和更新 SDK，修复潜在的错误并解决与您 DEX 集成相关的问题。
根据我们的特定需求定制 SDK，进行性能优化。
遵循我们提供的指南和示例：
我们将提供详细的集成指南和示例代码，确保集成过程顺利进行。这将帮助您理解技术要求和结构，使过程更加简便和高效。通过遵循这些文档，您可以确保您的 DEX SDK 与我们的平台需求和集成标准对齐。
通过满足这些指南，我们将能够为您的DEX提供可靠的支持，并确保您的流动性能够通过 OKX DEX 路由引擎进行访问。
注意
目前，该接口仅适用于基于 Solana 的 DEX。
AMM 接入示例
#
use async_trait
:
:
async_trait
;
use solana_client
:
:
rpc_client
:
:
RpcClient
;
use solana_sdk
:
:
pubkey
:
:
Pubkey
;
use std
:
:
collections
:
:
HashMap
;
use std
:
:
error
:
:
Error
;
use tokio
:
:
sync
:
:
mpsc
:
:
Sender
;
pub mod raydium_clmm
;
// 其他 DEX 模块声明
// pub mod raydium_amm;
// pub mod orca_amm;
// ...
#
[
async_trait
]
pub trait Dex
:
Send
+
Sync
{
// 返回 DEX 名称
fn
dex_name
(
&
self
)
-
>
String
;
// 返回 DEX 的程序 ID
fn
dex_program_id
(
&
self
)
-
>
Pubkey
;
// 报价函数
fn
quote
(
&
self
,
amount_in
:
f64
,
metadata
:
&
PoolMetadata
)
-
>
f64
;
// 扫描链上所有池子地址
fn
fetch_pool_addresses
(
&
self
,
client
:
&
RpcClient
)
-
>
Vec
<
String
>
;
// 监听新池子和数据变化的池子
async
fn
listen_new_pool_addresses
(
&
self
,
client
:
&
RpcClient
,
address_tx
:
Sender
<
String
>
,
)
-
>
Result
<
(
)
,
Box
<
dyn Error
>>
;
// 从池子地址导出报价参数
fn
fetch_pool_metadata
(
&
self
,
client
:
&
RpcClient
,
pool_address
:
&
str
)
-
>
Option
<
PoolMetadata
>
;
}
// 池子元数据（抽象设计）
#
[
derive
(
Clone
)
]
pub struct PoolMetadata
{
pub pool_address
:
String
,
pub base_mint
:
String
,
pub quote_mint
:
String
,
pub base_reserve
:
Option
<
f64
>
,
pub quote_reserve
:
Option
<
f64
>
,
pub trade_fee
:
Option
<
f64
>
,
pub extra
:
HashMap
<
String
,
PoolMetadataValue
>
,
}
// 池子元数据的扩展值类型
#
[
derive
(
Clone
)
]
pub
enum
PoolMetadataValue
{
String
(
String
)
,
Number
(
f64
)
,
Bool
(
bool
)
,
Array
(
Vec
<
PoolMetadataValue
>
)
,
Map
(
HashMap
<
String
,
PoolMetadataValue
>
)
,
}
// 通用宏简化 HashMap 访问
macro_rules
!
get_extra
{
(
$metadata
:
expr
,
$key
:
expr
,
$variant
:
path
)
=>
{
$metadata
.
extra
.
get
(
$key
)
.
and_then
(
|
v
|
match v
{
$variant
(
val
)
=>
Some
(
val
.
clone
(
)
)
,
_
=>
None
,
}
)
}
;
}
pub
(
crate
)
use get_extra
;
基于 Raydium CLMM 的实现例子
#
use async_trait
:
:
async_trait
;
use solana_client
:
:
rpc_client
:
:
RpcClient
;
use solana_sdk
:
:
{
pubkey
:
:
Pubkey
,
signature
:
:
Signature
,
commitment_config
:
:
CommitmentConfig
,
}
;
use std
:
:
collections
:
:
HashMap
;
use std
:
:
error
:
:
Error
;
use std
:
:
sync
:
:
{
Arc
,
Mutex
}
;
use tokio
:
:
sync
:
:
mpsc
:
:
Sender
;
use base58
:
:
{
FromBase58
,
ToBase58
}
;
use log
:
:
{
info
,
error
}
;
use tokio_tungstenite
:
:
{
connect_async
,
tungstenite
:
:
protocol
:
:
Message
}
;
use
super
:
:
{
Dex
,
PoolMetadata
,
get_extra
}
;
// Raydium CLMM 程序 ID
const
PROGRAM_ID
:
&
str
=
"CLMM9tUush29+wnRVN2QqohW5Ns5mYAPbXTRmbn6kYH"
;
// 全局映射表
lazy_static
:
:
lazy_static
!
{
static
ref
POOL_ADDRESS_MAP
:
Arc
<
Mutex
<
HashMap
<
String
,
PoolDerivedAccounts
>>>
=
Arc
:
:
new
(
Mutex
:
:
new
(
HashMap
:
:
new
(
)
)
)
;
}
// Raydium CLMM 的池子派生账户
#
[
derive
(
Clone
)
]
struct PoolDerivedAccounts
{
pool_address
:
String
,
base_mint
:
String
,
quote_mint
:
String
,
base_vault
:
String
,
quote_vault
:
String
,
fee_state
:
String
,
tick_array_current
:
String
,
tick_array_prev
:
String
,
tick_array_next
:
String
,
observation_state
:
String
,
}
pub struct RaydiumCLMM
;
#
[
async_trait
]
impl Dex
for
RaydiumCLMM
{
fn
dex_name
(
&
self
)
-
>
String
{
"RaydiumCLMM"
.
to_string
(
)
}
fn
dex_program_id
(
&
self
)
-
>
Pubkey
{
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
}
fn
quote
(
&
self
,
amount_in
:
f64
,
metadata
:
&
PoolMetadata
)
-
>
f64
{
if
amount_in
<=
0.0
{
return
0.0
;
}
let
fee_rate
=
metadata
.
trade_fee
.
unwrap_or
(
0.0
)
;
let
amount_in_with_fee
=
amount_in
*
(
1.0
-
fee_rate
)
;
let
mut remaining_in
=
amount_in_with_fee
;
let
mut total_out
=
0.0
;
let
sqrt_price_x64
=
get_extra
!
(
metadata
,
"sqrt_price_x64"
,
PoolMetadataValue
:
:
Number
)
.
unwrap_or
(
0.0
)
;
let
tick_current_index
=
get_extra
!
(
metadata
,
"tick_current_index"
,
PoolMetadataValue
:
:
Number
)
.
unwrap_or
(
0.0
)
as
i32
;
let
tick_array
=
get_extra
!
(
metadata
,
"tick_array"
,
PoolMetadataValue
:
:
Array
)
.
unwrap_or
(
vec
!
[
]
)
;
if
tick_array
.
is_empty
(
)
{
return
0.0
;
}
let
current_price
=
sqrt_price_x64
/
2_f64
.
powi
(
64
)
;
let
mut current_tick
=
tick_current_index
;
let
mut ticks
:
Vec
<
(
i32
,
f64
)
>
=
tick_array
.
iter
(
)
.
filter_map
(
|
v
|
match v
{
PoolMetadataValue
:
:
Map
(
m
)
=>
{
let
tick_index
=
get_extra
!
(
m
,
"tick_index"
,
PoolMetadataValue
:
:
Number
)
?
as
i32
;
let
liquidity
=
get_extra
!
(
m
,
"liquidity"
,
PoolMetadataValue
:
:
Number
)
?
;
Some
(
(
tick_index
,
liquidity
)
)
}
,
_
=>
None
,
}
)
.
collect
(
)
;
ticks
.
sort_by
(
|
a
,
b
|
a
.
0.
cmp
(
&
b
.
0
)
)
;
for
(
tick_index
,
liquidity
)
in
ticks
{
if
tick_index
<=
current_tick
{
continue
;
}
let
sqrt_price_lower
=
(
1
.
0001_f64
.
powf
(
current_tick
as
f64
)
)
.
sqrt
(
)
;
let
sqrt_price_upper
=
(
1
.
0001_f64
.
powf
(
tick_index
as
f64
)
)
.
sqrt
(
)
;
let
delta_sqrt_price
=
sqrt_price_upper
-
sqrt_price_lower
;
let
max_amount_out
=
liquidity
*
delta_sqrt_price
;
let
cost
=
max_amount_out
*
(
sqrt_price_upper
+
sqrt_price_lower
)
/
2.0
;
if
remaining_in
>=
cost
{
total_out
+=
max_amount_out
;
remaining_in
-=
cost
;
current_tick
=
tick_index
;
}
else
{
let
fraction
=
remaining_in
/
cost
;
total_out
+=
max_amount_out
*
fraction
;
remaining_in
=
0.0
;
break
;
}
if
remaining_in
<=
0.0
{
break
;
}
}
total_out
}
fn
fetch_pool_addresses
(
&
self
,
client
:
&
RpcClient
)
-
>
Vec
<
String
>
{
let
program_id
=
self
.
dex_program_id
(
)
;
let
accounts
=
match client
.
get_program_accounts
(
&
program_id
)
{
Ok
(
accs
)
=>
accs
,
Err
(
e
)
=>
{
error
!
(
"Failed to fetch {} pool addresses: {}"
,
self
.
dex_name
(
)
,
e
)
;
return
Vec
:
:
new
(
)
;
}
}
;
let
mut pool_addresses
=
Vec
:
:
new
(
)
;
for
(
pubkey
,
account
)
in
accounts
{
if
account
.
owner
!=
program_id
{
continue
;
}
let
data
=
account
.
data
;
if
data
.
len
(
)
<
200
{
continue
;
}
let
base_mint
=
data
[
0.
.32
]
.
to_base58
(
)
;
let
quote_mint
=
data
[
32.
.64
]
.
to_base58
(
)
;
if
base_mint
.
is_empty
(
)
||
quote_mint
.
is_empty
(
)
{
continue
;
}
let
discriminator
=
u64
:
:
from_le_bytes
(
data
[
0.
.8
]
.
try_into
(
)
.
unwrap
(
)
)
;
if
discriminator
==
0
{
continue
;
}
let
pool_address
=
pubkey
.
to_string
(
)
;
pool_addresses
.
push
(
pool_address
.
clone
(
)
)
;
if
let
Some
(
accounts
)
=
self
.
derive_accounts_from_pool_address
(
client
,
&
pool_address
)
{
POOL_ADDRESS_MAP
.
lock
(
)
.
unwrap
(
)
.
insert
(
pool_address
,
accounts
)
;
}
}
pool_addresses
}
async
fn
listen_new_pool_addresses
(
&
self
,
client
:
&
RpcClient
,
address_tx
:
Sender
<
String
>
,
)
-
>
Result
<
(
)
,
Box
<
dyn Error
>>
{
let
program_id
=
self
.
dex_program_id
(
)
;
let
ws_url
=
"wss://api.mainnet-beta.solana.com"
;
let
(
mut ws_stream
,
_
)
=
connect_async
(
ws_url
)
.
await
?
;
let
subscribe_msg
=
format
!
(
r#
"{"
jsonrpc
":"
2.0
","
id
":1,"
method
":"
logsSubscribe
","
params
":["
mentions
","
{
}
"]}"
#
,
program_id
)
;
ws_stream
.
send
(
Message
:
:
Text
(
subscribe_msg
)
)
.
await
?
;
while
let
Some
(
msg
)
=
ws_stream
.
next
(
)
.
await
{
let
msg
=
msg
?
;
if
let
Message
:
:
Text
(
text
)
=
msg
{
let
log
:
serde_json
:
:
Value
=
serde_json
:
:
from_str
(
&
text
)
?
;
if
log
.
get
(
"result"
)
.
is_some
(
)
{
continue
;
}
let
params
=
log
.
get
(
"params"
)
.
and_then
(
|
p
|
p
.
get
(
"result"
)
)
.
ok_or
(
"No params"
)
?
;
let
tx_sig
=
params
.
get
(
"signature"
)
.
and_then
(
|
s
|
s
.
as_str
(
)
)
.
ok_or
(
"No signature"
)
?
;
let
logs
=
params
.
get
(
"logs"
)
.
and_then
(
|
l
|
l
.
as_array
(
)
)
.
ok_or
(
"No logs"
)
?
;
let
tx
=
client
.
get_transaction
(
&
Signature
:
:
from_str
(
tx_sig
)
?
,
CommitmentConfig
:
:
confirmed
(
)
,
)
?
;
if
tx
.
meta
.
is_some
(
)
&&
tx
.
meta
.
unwrap
(
)
.
err
.
is_some
(
)
{
continue
;
}
let
log_str
=
logs
.
iter
(
)
.
filter_map
(
|
l
|
l
.
as_str
(
)
)
.
collect
:
:
<
Vec
<
&
str
>>
(
)
.
join
(
" "
)
;
let
account_keys
=
tx
.
transaction
.
message
.
account_keys
;
for
(
i
,
key
)
in
account_keys
.
iter
(
)
.
enumerate
(
)
{
if
tx
.
transaction
.
message
.
is_writable
(
i
)
{
let
pool_address
=
self
.
find_pool_address_from_account
(
&
key
.
to_string
(
)
)
;
if
pool_address
.
is_empty
(
)
&&
self
.
is_valid_pool_address
(
client
,
&
key
.
to_string
(
)
)
{
if
let
Some
(
accounts
)
=
self
.
derive_accounts_from_pool_address
(
client
,
&
key
.
to_string
(
)
)
{
POOL_ADDRESS_MAP
.
lock
(
)
.
unwrap
(
)
.
insert
(
key
.
to_string
(
)
,
accounts
)
;
info
!
(
"Detected new {} pool address: {}"
,
self
.
dex_name
(
)
,
key
)
;
address_tx
.
send
(
key
.
to_string
(
)
)
.
await
?
;
}
}
else
if
!
pool_address
.
is_empty
(
)
{
info
!
(
"Detected writable account affecting pool: {}, Pool: {}"
,
tx_sig
,
pool_address
)
;
address_tx
.
send
(
pool_address
)
.
await
?
;
}
}
}
if
log_str
.
contains
(
"initialize"
)
{
if
let
Some
(
pool_address
)
=
self
.
extract_new_pool_address
(
client
,
tx_sig
)
{
if
self
.
is_valid_pool_address
(
client
,
&
pool_address
)
{
if
let
Some
(
accounts
)
=
self
.
derive_accounts_from_pool_address
(
client
,
&
pool_address
)
{
POOL_ADDRESS_MAP
.
lock
(
)
.
unwrap
(
)
.
insert
(
pool_address
.
clone
(
)
,
accounts
)
;
info
!
(
"Detected new {} pool address: {}"
,
self
.
dex_name
(
)
,
pool_address
)
;
address_tx
.
send
(
pool_address
)
.
await
?
;
}
}
}
}
}
}
Ok
(
(
)
)
}
fn
fetch_pool_metadata
(
&
self
,
client
:
&
RpcClient
,
pool_address
:
&
str
)
-
>
Option
<
PoolMetadata
>
{
let
derived_accounts
=
self
.
derive_accounts_from_pool_address
(
client
,
pool_address
)
?
;
let
out
=
client
.
get_account_data
(
&
Pubkey
:
:
from_str
(
pool_address
)
.
ok
(
)
?
)
.
ok
(
)
?
;
if
out
.
len
(
)
<
200
{
error
!
(
"Pool data too short for {}"
,
pool_address
)
;
return
None
;
}
let
base_reserve
=
self
.
get_vault_balance
(
client
,
&
derived_accounts
.
base_vault
)
;
let
quote_reserve
=
self
.
get_vault_balance
(
client
,
&
derived_accounts
.
quote_vault
)
;
let
fee_data
=
client
.
get_account_data
(
&
Pubkey
:
:
from_str
(
&
derived_accounts
.
fee_state
)
.
ok
(
)
?
)
.
ok
(
)
?
;
let
fee_numerator
=
u64
:
:
from_le_bytes
(
fee_data
[
0.
.8
]
.
try_into
(
)
.
unwrap
(
)
)
;
let
fee_denominator
=
u64
:
:
from_le_bytes
(
fee_data
[
8.
.16
]
.
try_into
(
)
.
unwrap
(
)
)
;
let
trade_fee
=
if
fee_denominator
>
0
{
Some
(
fee_numerator
as
f64
/
fee_denominator
as
f64
)
}
else
{
None
}
;
let
sqrt_price_x64
=
u64
:
:
from_le_bytes
(
out
[
64.
.72
]
.
try_into
(
)
.
unwrap
(
)
)
;
let
tick_current_index
=
i32
:
:
from_le_bytes
(
out
[
72.
.76
]
.
try_into
(
)
.
unwrap
(
)
)
;
let
tick_array_data
=
client
.
get_account_data
(
&
Pubkey
:
:
from_str
(
&
derived_accounts
.
tick_array_current
)
.
ok
(
)
?
)
.
unwrap_or_default
(
)
;
let
mut tick_array
=
Vec
:
:
new
(
)
;
if
!
tick_array_data
.
is_empty
(
)
{
for
i
in
(
8.
.
tick_array_data
.
len
(
)
-
12
)
.
step_by
(
12
)
{
let
tick_index
=
i32
:
:
from_le_bytes
(
tick_array_data
[
i
.
.
i
+
4
]
.
try_into
(
)
.
unwrap
(
)
)
;
let
liquidity
=
f64
:
:
from_le_bytes
(
tick_array_data
[
i
+
4.
.
i
+
12
]
.
try_into
(
)
.
unwrap
(
)
)
/
1_000_000.0
;
let
mut tick_map
=
HashMap
:
:
new
(
)
;
tick_map
.
insert
(
"tick_index"
.
to_string
(
)
,
PoolMetadataValue
:
:
Number
(
tick_index
as
f64
)
)
;
tick_map
.
insert
(
"liquidity"
.
to_string
(
)
,
PoolMetadataValue
:
:
Number
(
liquidity
)
)
;
tick_array
.
push
(
PoolMetadataValue
:
:
Map
(
tick_map
)
)
;
}
}
let
mut extra
=
HashMap
:
:
new
(
)
;
extra
.
insert
(
"sqrt_price_x64"
.
to_string
(
)
,
PoolMetadataValue
:
:
Number
(
sqrt_price_x64
as
f64
)
)
;
extra
.
insert
(
"tick_current_index"
.
to_string
(
)
,
PoolMetadataValue
:
:
Number
(
tick_current_index
as
f64
)
)
;
extra
.
insert
(
"tick_array"
.
to_string
(
)
,
PoolMetadataValue
:
:
Array
(
tick_array
)
)
;
Some
(
PoolMetadata
{
pool_address
:
pool_address
.
to_string
(
)
,
base_mint
:
derived_accounts
.
base_mint
,
quote_mint
:
derived_accounts
.
quote_mint
,
base_reserve
:
Some
(
base_reserve
)
,
quote_reserve
:
Some
(
quote_reserve
)
,
trade_fee
,
extra
,
}
)
}
}
impl RaydiumCLMM
{
fn
derive_accounts_from_pool_address
(
&
self
,
client
:
&
RpcClient
,
pool_address
:
&
str
)
-
>
Option
<
PoolDerivedAccounts
>
{
let
out
=
client
.
get_account_data
(
&
Pubkey
:
:
from_str
(
pool_address
)
.
ok
(
)
?
)
.
ok
(
)
?
;
if
out
.
len
(
)
<
200
{
error
!
(
"Pool data too short for {}"
,
pool_address
)
;
return
None
;
}
let
base_mint
=
out
[
0.
.32
]
.
to_base58
(
)
;
let
quote_mint
=
out
[
32.
.64
]
.
to_base58
(
)
;
let
base_vault
=
out
[
96.
.128
]
.
to_base58
(
)
;
let
quote_vault
=
out
[
128.
.160
]
.
to_base58
(
)
;
let
fee_state
=
out
[
160.
.192
]
.
to_base58
(
)
;
let
tick_array_current_seed
=
format
!
(
"tick_array{}"
,
pool_address
)
;
let
tick_array_current
=
Pubkey
:
:
create_program_address
(
&
[
&
tick_array_current_seed
.
as_bytes
(
)
]
,
&
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
,
)
.
ok
(
)
?.
to_string
(
)
;
let
tick_array_prev_seed
=
format
!
(
"tick_array_prev{}"
,
pool_address
)
;
let
tick_array_prev
=
Pubkey
:
:
create_program_address
(
&
[
&
tick_array_prev_seed
.
as_bytes
(
)
]
,
&
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
,
)
.
ok
(
)
?.
to_string
(
)
;
let
tick_array_next_seed
=
format
!
(
"tick_array_next{}"
,
pool_address
)
;
let
tick_array_next
=
Pubkey
:
:
create_program_address
(
&
[
&
tick_array_next_seed
.
as_bytes
(
)
]
,
&
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
,
)
.
ok
(
)
?.
to_string
(
)
;
let
observation_state_seed
=
format
!
(
"observation_state{}"
,
pool_address
)
;
let
observation_state
=
Pubkey
:
:
create_program_address
(
&
[
&
observation_state_seed
.
as_bytes
(
)
]
,
&
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
,
)
.
ok
(
)
?.
to_string
(
)
;
Some
(
PoolDerivedAccounts
{
pool_address
:
pool_address
.
to_string
(
)
,
base_mint
,
quote_mint
,
base_vault
,
quote_vault
,
fee_state
,
tick_array_current
,
tick_array_prev
,
tick_array_next
,
observation_state
,
}
)
}
fn
find_pool_address_from_account
(
&
self
,
account_address
:
&
str
)
-
>
String
{
let
map
=
POOL_ADDRESS_MAP
.
lock
(
)
.
unwrap
(
)
;
for
(
pool_address
,
accounts
)
in
map
.
iter
(
)
{
if
account_address
==
pool_address
||
account_address
==
&
accounts
.
base_vault
||
account_address
==
&
accounts
.
quote_vault
||
account_address
==
&
accounts
.
tick_array_current
||
account_address
==
&
accounts
.
tick_array_prev
||
account_address
==
&
accounts
.
tick_array_next
{
return
pool_address
.
clone
(
)
;
}
}
String
:
:
new
(
)
}
fn
is_valid_pool_address
(
&
self
,
client
:
&
RpcClient
,
pool_address
:
&
str
)
-
>
bool
{
let
out
=
match client
.
get_account_data
(
&
Pubkey
:
:
from_str
(
pool_address
)
.
unwrap
(
)
)
{
Ok
(
data
)
=>
data
,
Err
(
_
)
=>
return
false
,
}
;
if
out
.
len
(
)
<
200
{
return
false
;
}
if
Pubkey
:
:
from_str
(
&
out
.
owner
.
to_string
(
)
)
.
unwrap
(
)
!=
Pubkey
:
:
from_str
(
PROGRAM_ID
)
.
unwrap
(
)
{
return
false
;
}
let
base_mint
=
out
[
0.
.32
]
.
to_base58
(
)
;
let
quote_mint
=
out
[
32.
.64
]
.
to_base58
(
)
;
if
base_mint
.
is_empty
(
)
||
quote_mint
.
is_empty
(
)
{
return
false
;
}
let
discriminator
=
u64
:
:
from_le_bytes
(
out
[
0.
.8
]
.
try_into
(
)
.
unwrap
(
)
)
;
if
discriminator
==
0
{
return
false
;
}
true
}
fn
get_vault_balance
(
&
self
,
client
:
&
RpcClient
,
vault
:
&
str
)
-
>
f64
{
match client
.
get_token_account_balance
(
&
Pubkey
:
:
from_str
(
vault
)
.
unwrap
(
)
,
CommitmentConfig
:
:
confirmed
(
)
)
{
Ok
(
resp
)
=>
resp
.
ui_amount
.
unwrap_or
(
0.0
)
,
Err
(
_
)
=>
0.0
,
}
}
fn
extract_new_pool_address
(
&
self
,
client
:
&
RpcClient
,
tx_sig
:
&
str
)
-
>
Option
<
String
>
{
let
tx
=
client
.
get_transaction
(
&
Signature
:
:
from_str
(
tx_sig
)
.
ok
(
)
?
,
CommitmentConfig
:
:
confirmed
(
)
,
)
.
ok
(
)
?
;
for
key
in
tx
.
transaction
.
message
.
account_keys
{
if
key
.
is_writable
(
)
&&
!
key
.
is_signer
(
)
{
return
Some
(
key
.
to_string
(
)
)
;
}
}
None
}
}

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="dex-集成">DEX 集成<a class="index_header-anchor__Xqb+L" href="#dex-集成" style="opacity:0">#</a></h1>
<p>为了成功将您的 DEX 集成到 OKX 路由引擎中，请按照以下步骤操作：</p>
<ol>
<li>
<p>提供与 OKX DEX AMM 接口兼容的 DEX SDK：
我们需要一个与我们的 AMM（自动化市场制造商）接口完全兼容的 DEX SDK。该SDK将允许我们与您的 DEX 进行通信并集成其功能，使流动性提供和交易执行能够在我们的平台上无缝进行。SDK 应能够处理定价、订单匹配、流动性池交互和交易执行等关键功能。</p>
</li>
<li>
<p>允许我们分叉您的 SDK：
为了确保长期的维护和用户支持，我们需要能够分叉您的 SDK。这意味着我们需要创建自己版本的 SDK 以供集成使用。通过这样做，我们可以：</p>
</li>
</ol>
<ul>
<li>确保 SDK 的稳定性。</li>
<li>独立维护和更新 SDK，修复潜在的错误并解决与您 DEX 集成相关的问题。</li>
<li>根据我们的特定需求定制 SDK，进行性能优化。</li>
</ul>
<ol start="3">
<li>遵循我们提供的指南和示例：
我们将提供详细的集成指南和示例代码，确保集成过程顺利进行。这将帮助您理解技术要求和结构，使过程更加简便和高效。通过遵循这些文档，您可以确保您的 DEX SDK 与我们的平台需求和集成标准对齐。</li>
</ol>
<p>通过满足这些指南，我们将能够为您的DEX提供可靠的支持，并确保您的流动性能够通过 OKX DEX 路由引擎进行访问。</p>
<div class="index_wrapper__x5A2Q"><div aria-labelledby=":Rdbf:" class="okui-alert info-alert"><i aria-label="信息" class="icon iconfont okui-alert-icon doc-ssr-okds-information-circle-fill" role="img"></i><div class="okui-alert-msg-box"><div class="okui-alert-title" id=":Rdbf:">注意</div><div class="okui-alert-desc"><div class="index_desc__5fNBE">目前，该接口仅适用于基于 Solana 的 DEX。</div></div></div></div></div>
<h2 data-content="AMM 接入示例" id="amm-接入示例">AMM 接入示例<a class="index_header-anchor__Xqb+L" href="#amm-接入示例" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">use async_trait<span class="token operator">:</span><span class="token operator">:</span>async_trait<span class="token punctuation">;</span>
use solana_client<span class="token operator">:</span><span class="token operator">:</span>rpc_client<span class="token operator">:</span><span class="token operator">:</span>RpcClient<span class="token punctuation">;</span>
use solana_sdk<span class="token operator">:</span><span class="token operator">:</span>pubkey<span class="token operator">:</span><span class="token operator">:</span>Pubkey<span class="token punctuation">;</span>
use std<span class="token operator">:</span><span class="token operator">:</span>collections<span class="token operator">:</span><span class="token operator">:</span>HashMap<span class="token punctuation">;</span>
use std<span class="token operator">:</span><span class="token operator">:</span>error<span class="token operator">:</span><span class="token operator">:</span>Error<span class="token punctuation">;</span>
use tokio<span class="token operator">:</span><span class="token operator">:</span>sync<span class="token operator">:</span><span class="token operator">:</span>mpsc<span class="token operator">:</span><span class="token operator">:</span>Sender<span class="token punctuation">;</span>

pub mod raydium_clmm<span class="token punctuation">;</span>
<span class="token comment">// 其他 DEX 模块声明</span>
<span class="token comment">// pub mod raydium_amm;</span>
<span class="token comment">// pub mod orca_amm;</span>
<span class="token comment">// ...</span>

#<span class="token punctuation">[</span>async_trait<span class="token punctuation">]</span>
pub trait Dex<span class="token operator">:</span> Send <span class="token operator">+</span> Sync <span class="token punctuation">{</span>
    <span class="token comment">// 返回 DEX 名称</span>
    fn <span class="token function">dex_name</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> String<span class="token punctuation">;</span>

    <span class="token comment">// 返回 DEX 的程序 ID</span>
    fn <span class="token function">dex_program_id</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Pubkey<span class="token punctuation">;</span>

    <span class="token comment">// 报价函数</span>
    fn <span class="token function">quote</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> amount_in<span class="token operator">:</span> f64<span class="token punctuation">,</span> metadata<span class="token operator">:</span> <span class="token operator">&amp;</span>PoolMetadata<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> f64<span class="token punctuation">;</span>

    <span class="token comment">// 扫描链上所有池子地址</span>
    fn <span class="token function">fetch_pool_addresses</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Vec<span class="token operator">&lt;</span>String<span class="token operator">&gt;</span><span class="token punctuation">;</span>

    <span class="token comment">// 监听新池子和数据变化的池子</span>
    <span class="token keyword">async</span> fn <span class="token function">listen_new_pool_addresses</span><span class="token punctuation">(</span>
        <span class="token operator">&amp;</span>self<span class="token punctuation">,</span>
        client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span>
        address_tx<span class="token operator">:</span> Sender<span class="token operator">&lt;</span>String<span class="token operator">&gt;</span><span class="token punctuation">,</span>
    <span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Result<span class="token operator">&lt;</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> Box<span class="token operator">&lt;</span>dyn Error<span class="token operator">&gt;&gt;</span><span class="token punctuation">;</span>

    <span class="token comment">// 从池子地址导出报价参数</span>
    fn <span class="token function">fetch_pool_metadata</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> pool_address<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Option<span class="token operator">&lt;</span>PoolMetadata<span class="token operator">&gt;</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// 池子元数据（抽象设计）</span>
#<span class="token punctuation">[</span><span class="token function">derive</span><span class="token punctuation">(</span>Clone<span class="token punctuation">)</span><span class="token punctuation">]</span>
pub struct PoolMetadata <span class="token punctuation">{</span>
    pub pool_address<span class="token operator">:</span> String<span class="token punctuation">,</span>
    pub base_mint<span class="token operator">:</span> String<span class="token punctuation">,</span>
    pub quote_mint<span class="token operator">:</span> String<span class="token punctuation">,</span>
    pub base_reserve<span class="token operator">:</span> Option<span class="token operator">&lt;</span>f64<span class="token operator">&gt;</span><span class="token punctuation">,</span>
    pub quote_reserve<span class="token operator">:</span> Option<span class="token operator">&lt;</span>f64<span class="token operator">&gt;</span><span class="token punctuation">,</span>
    pub trade_fee<span class="token operator">:</span> Option<span class="token operator">&lt;</span>f64<span class="token operator">&gt;</span><span class="token punctuation">,</span>
    pub extra<span class="token operator">:</span> HashMap<span class="token operator">&lt;</span>String<span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">&gt;</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token comment">// 池子元数据的扩展值类型</span>
#<span class="token punctuation">[</span><span class="token function">derive</span><span class="token punctuation">(</span>Clone<span class="token punctuation">)</span><span class="token punctuation">]</span>
pub <span class="token keyword">enum</span> PoolMetadataValue <span class="token punctuation">{</span>
    <span class="token function">String</span><span class="token punctuation">(</span>String<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token function">Number</span><span class="token punctuation">(</span>f64<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token function">Bool</span><span class="token punctuation">(</span>bool<span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token function">Array</span><span class="token punctuation">(</span>Vec<span class="token operator">&lt;</span>PoolMetadataValue<span class="token operator">&gt;</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
    <span class="token function">Map</span><span class="token punctuation">(</span>HashMap<span class="token operator">&lt;</span>String<span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">&gt;</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
<span class="token punctuation">}</span>

<span class="token comment">// 通用宏简化 HashMap 访问</span>
macro_rules<span class="token operator">!</span> get_extra <span class="token punctuation">{</span>
    <span class="token punctuation">(</span>$metadata<span class="token operator">:</span>expr<span class="token punctuation">,</span> $key<span class="token operator">:</span>expr<span class="token punctuation">,</span> $variant<span class="token operator">:</span>path<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
        $metadata<span class="token punctuation">.</span>extra<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span>$key<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">and_then</span><span class="token punctuation">(</span><span class="token operator">|</span>v<span class="token operator">|</span> match v <span class="token punctuation">{</span>
            <span class="token function">$variant</span><span class="token punctuation">(</span>val<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token function">Some</span><span class="token punctuation">(</span>val<span class="token punctuation">.</span><span class="token function">clone</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            _ <span class="token operator">=&gt;</span> None<span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token function">pub</span><span class="token punctuation">(</span>crate<span class="token punctuation">)</span> use get_extra<span class="token punctuation">;</span>

</code></pre></div>
<h2 data-content="基于 Raydium CLMM 的实现例子" id="基于-raydium-clmm-的实现例子">基于 Raydium CLMM 的实现例子<a class="index_header-anchor__Xqb+L" href="#基于-raydium-clmm-的实现例子" style="opacity:0">#</a></h2>
<div class="remark-highlight"><pre class="language-typescript"><code class="language-typescript">use async_trait<span class="token operator">:</span><span class="token operator">:</span>async_trait<span class="token punctuation">;</span>
use solana_client<span class="token operator">:</span><span class="token operator">:</span>rpc_client<span class="token operator">:</span><span class="token operator">:</span>RpcClient<span class="token punctuation">;</span>
use solana_sdk<span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>
    pubkey<span class="token operator">:</span><span class="token operator">:</span>Pubkey<span class="token punctuation">,</span>
    signature<span class="token operator">:</span><span class="token operator">:</span>Signature<span class="token punctuation">,</span>
    commitment_config<span class="token operator">:</span><span class="token operator">:</span>CommitmentConfig<span class="token punctuation">,</span>
<span class="token punctuation">}</span><span class="token punctuation">;</span>
use std<span class="token operator">:</span><span class="token operator">:</span>collections<span class="token operator">:</span><span class="token operator">:</span>HashMap<span class="token punctuation">;</span>
use std<span class="token operator">:</span><span class="token operator">:</span>error<span class="token operator">:</span><span class="token operator">:</span>Error<span class="token punctuation">;</span>
use std<span class="token operator">:</span><span class="token operator">:</span>sync<span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>Arc<span class="token punctuation">,</span> Mutex<span class="token punctuation">}</span><span class="token punctuation">;</span>
use tokio<span class="token operator">:</span><span class="token operator">:</span>sync<span class="token operator">:</span><span class="token operator">:</span>mpsc<span class="token operator">:</span><span class="token operator">:</span>Sender<span class="token punctuation">;</span>
use base58<span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>FromBase58<span class="token punctuation">,</span> ToBase58<span class="token punctuation">}</span><span class="token punctuation">;</span>
use log<span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>info<span class="token punctuation">,</span> error<span class="token punctuation">}</span><span class="token punctuation">;</span>
use tokio_tungstenite<span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>connect_async<span class="token punctuation">,</span> tungstenite<span class="token operator">:</span><span class="token operator">:</span>protocol<span class="token operator">:</span><span class="token operator">:</span>Message<span class="token punctuation">}</span><span class="token punctuation">;</span>

use <span class="token keyword">super</span><span class="token operator">:</span><span class="token operator">:</span><span class="token punctuation">{</span>Dex<span class="token punctuation">,</span> PoolMetadata<span class="token punctuation">,</span> get_extra<span class="token punctuation">}</span><span class="token punctuation">;</span>

<span class="token comment">// Raydium CLMM 程序 ID</span>
<span class="token keyword">const</span> <span class="token constant">PROGRAM_ID</span><span class="token operator">:</span> <span class="token operator">&amp;</span>str <span class="token operator">=</span> <span class="token string">"CLMM9tUush29+wnRVN2QqohW5Ns5mYAPbXTRmbn6kYH"</span><span class="token punctuation">;</span>

<span class="token comment">// 全局映射表</span>
lazy_static<span class="token operator">:</span><span class="token operator">:</span>lazy_static<span class="token operator">!</span> <span class="token punctuation">{</span>
    <span class="token keyword">static</span> ref <span class="token constant">POOL_ADDRESS_MAP</span><span class="token operator">:</span> Arc<span class="token operator">&lt;</span>Mutex<span class="token operator">&lt;</span>HashMap<span class="token operator">&lt;</span>String<span class="token punctuation">,</span> PoolDerivedAccounts<span class="token operator">&gt;&gt;&gt;</span> <span class="token operator">=</span> Arc<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span>Mutex<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span>HashMap<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
<span class="token punctuation">}</span>

<span class="token comment">// Raydium CLMM 的池子派生账户</span>
#<span class="token punctuation">[</span><span class="token function">derive</span><span class="token punctuation">(</span>Clone<span class="token punctuation">)</span><span class="token punctuation">]</span>
struct PoolDerivedAccounts <span class="token punctuation">{</span>
    pool_address<span class="token operator">:</span> String<span class="token punctuation">,</span>
    base_mint<span class="token operator">:</span> String<span class="token punctuation">,</span>
    quote_mint<span class="token operator">:</span> String<span class="token punctuation">,</span>
    base_vault<span class="token operator">:</span> String<span class="token punctuation">,</span>
    quote_vault<span class="token operator">:</span> String<span class="token punctuation">,</span>
    fee_state<span class="token operator">:</span> String<span class="token punctuation">,</span>
    tick_array_current<span class="token operator">:</span> String<span class="token punctuation">,</span>
    tick_array_prev<span class="token operator">:</span> String<span class="token punctuation">,</span>
    tick_array_next<span class="token operator">:</span> String<span class="token punctuation">,</span>
    observation_state<span class="token operator">:</span> String<span class="token punctuation">,</span>
<span class="token punctuation">}</span>

pub struct RaydiumCLMM<span class="token punctuation">;</span>

#<span class="token punctuation">[</span>async_trait<span class="token punctuation">]</span>
impl Dex <span class="token keyword">for</span> RaydiumCLMM <span class="token punctuation">{</span>
    fn <span class="token function">dex_name</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> String <span class="token punctuation">{</span>
        <span class="token string">"RaydiumCLMM"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">dex_program_id</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Pubkey <span class="token punctuation">{</span>
        Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">quote</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> amount_in<span class="token operator">:</span> f64<span class="token punctuation">,</span> metadata<span class="token operator">:</span> <span class="token operator">&amp;</span>PoolMetadata<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> f64 <span class="token punctuation">{</span>
        <span class="token keyword">if</span> amount_in <span class="token operator">&lt;=</span> <span class="token number">0.0</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token number">0.0</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> fee_rate <span class="token operator">=</span> metadata<span class="token punctuation">.</span>trade_fee<span class="token punctuation">.</span><span class="token function">unwrap_or</span><span class="token punctuation">(</span><span class="token number">0.0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> amount_in_with_fee <span class="token operator">=</span> amount_in <span class="token operator">*</span> <span class="token punctuation">(</span><span class="token number">1.0</span> <span class="token operator">-</span> fee_rate<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> mut remaining_in <span class="token operator">=</span> amount_in_with_fee<span class="token punctuation">;</span>
        <span class="token keyword">let</span> mut total_out <span class="token operator">=</span> <span class="token number">0.0</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> sqrt_price_x64 <span class="token operator">=</span> get_extra<span class="token operator">!</span><span class="token punctuation">(</span>metadata<span class="token punctuation">,</span> <span class="token string">"sqrt_price_x64"</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span>Number<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap_or</span><span class="token punctuation">(</span><span class="token number">0.0</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_current_index <span class="token operator">=</span> get_extra<span class="token operator">!</span><span class="token punctuation">(</span>metadata<span class="token punctuation">,</span> <span class="token string">"tick_current_index"</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span>Number<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap_or</span><span class="token punctuation">(</span><span class="token number">0.0</span><span class="token punctuation">)</span> <span class="token keyword">as</span> i32<span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_array <span class="token operator">=</span> get_extra<span class="token operator">!</span><span class="token punctuation">(</span>metadata<span class="token punctuation">,</span> <span class="token string">"tick_array"</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token builtin">Array</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap_or</span><span class="token punctuation">(</span>vec<span class="token operator">!</span><span class="token punctuation">[</span><span class="token punctuation">]</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">if</span> tick_array<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token number">0.0</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>
        <span class="token keyword">let</span> current_price <span class="token operator">=</span> sqrt_price_x64 <span class="token operator">/</span> 2_f64<span class="token punctuation">.</span><span class="token function">powi</span><span class="token punctuation">(</span><span class="token number">64</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> mut current_tick <span class="token operator">=</span> tick_current_index<span class="token punctuation">;</span>
        <span class="token keyword">let</span> mut ticks<span class="token operator">:</span> Vec<span class="token operator">&lt;</span><span class="token punctuation">(</span>i32<span class="token punctuation">,</span> f64<span class="token punctuation">)</span><span class="token operator">&gt;</span> <span class="token operator">=</span> tick_array<span class="token punctuation">.</span><span class="token function">iter</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
            <span class="token punctuation">.</span><span class="token function">filter_map</span><span class="token punctuation">(</span><span class="token operator">|</span>v<span class="token operator">|</span> match v <span class="token punctuation">{</span>
                PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Map</span><span class="token punctuation">(</span>m<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
                    <span class="token keyword">let</span> tick_index <span class="token operator">=</span> get_extra<span class="token operator">!</span><span class="token punctuation">(</span>m<span class="token punctuation">,</span> <span class="token string">"tick_index"</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span>Number<span class="token punctuation">)</span><span class="token operator">?</span> <span class="token keyword">as</span> i32<span class="token punctuation">;</span>
                    <span class="token keyword">let</span> liquidity <span class="token operator">=</span> get_extra<span class="token operator">!</span><span class="token punctuation">(</span>m<span class="token punctuation">,</span> <span class="token string">"liquidity"</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span>Number<span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
                    <span class="token function">Some</span><span class="token punctuation">(</span><span class="token punctuation">(</span>tick_index<span class="token punctuation">,</span> liquidity<span class="token punctuation">)</span><span class="token punctuation">)</span>
                <span class="token punctuation">}</span><span class="token punctuation">,</span>
                _ <span class="token operator">=&gt;</span> None<span class="token punctuation">,</span>
            <span class="token punctuation">}</span><span class="token punctuation">)</span>
            <span class="token punctuation">.</span><span class="token function">collect</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        ticks<span class="token punctuation">.</span><span class="token function">sort_by</span><span class="token punctuation">(</span><span class="token operator">|</span>a<span class="token punctuation">,</span> b<span class="token operator">|</span> a<span class="token punctuation">.</span><span class="token number">0.</span><span class="token function">cmp</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>b<span class="token punctuation">.</span><span class="token number">0</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">for</span> <span class="token punctuation">(</span>tick_index<span class="token punctuation">,</span> liquidity<span class="token punctuation">)</span> <span class="token keyword">in</span> ticks <span class="token punctuation">{</span>
            <span class="token keyword">if</span> tick_index <span class="token operator">&lt;=</span> current_tick <span class="token punctuation">{</span>
                <span class="token keyword">continue</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
            <span class="token keyword">let</span> sqrt_price_lower <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">.</span>0001_f64<span class="token punctuation">.</span><span class="token function">powf</span><span class="token punctuation">(</span>current_tick <span class="token keyword">as</span> f64<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">sqrt</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">let</span> sqrt_price_upper <span class="token operator">=</span> <span class="token punctuation">(</span><span class="token number">1</span><span class="token punctuation">.</span>0001_f64<span class="token punctuation">.</span><span class="token function">powf</span><span class="token punctuation">(</span>tick_index <span class="token keyword">as</span> f64<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">sqrt</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">let</span> delta_sqrt_price <span class="token operator">=</span> sqrt_price_upper <span class="token operator">-</span> sqrt_price_lower<span class="token punctuation">;</span>

            <span class="token keyword">let</span> max_amount_out <span class="token operator">=</span> liquidity <span class="token operator">*</span> delta_sqrt_price<span class="token punctuation">;</span>
            <span class="token keyword">let</span> cost <span class="token operator">=</span> max_amount_out <span class="token operator">*</span> <span class="token punctuation">(</span>sqrt_price_upper <span class="token operator">+</span> sqrt_price_lower<span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token number">2.0</span><span class="token punctuation">;</span>

            <span class="token keyword">if</span> remaining_in <span class="token operator">&gt;=</span> cost <span class="token punctuation">{</span>
                total_out <span class="token operator">+=</span> max_amount_out<span class="token punctuation">;</span>
                remaining_in <span class="token operator">-=</span> cost<span class="token punctuation">;</span>
                current_tick <span class="token operator">=</span> tick_index<span class="token punctuation">;</span>
            <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span>
                <span class="token keyword">let</span> fraction <span class="token operator">=</span> remaining_in <span class="token operator">/</span> cost<span class="token punctuation">;</span>
                total_out <span class="token operator">+=</span> max_amount_out <span class="token operator">*</span> fraction<span class="token punctuation">;</span>
                remaining_in <span class="token operator">=</span> <span class="token number">0.0</span><span class="token punctuation">;</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
            <span class="token keyword">if</span> remaining_in <span class="token operator">&lt;=</span> <span class="token number">0.0</span> <span class="token punctuation">{</span>
                <span class="token keyword">break</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
        total_out
    <span class="token punctuation">}</span>

    fn <span class="token function">fetch_pool_addresses</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Vec<span class="token operator">&lt;</span>String<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">let</span> program_id <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">dex_program_id</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> accounts <span class="token operator">=</span> match client<span class="token punctuation">.</span><span class="token function">get_program_accounts</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>program_id<span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token function">Ok</span><span class="token punctuation">(</span>accs<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> accs<span class="token punctuation">,</span>
            <span class="token function">Err</span><span class="token punctuation">(</span>e<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token punctuation">{</span>
                error<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Failed to fetch {} pool addresses: {}"</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span><span class="token function">dex_name</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> e<span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">return</span> Vec<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> mut pool_addresses <span class="token operator">=</span> Vec<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">for</span> <span class="token punctuation">(</span>pubkey<span class="token punctuation">,</span> account<span class="token punctuation">)</span> <span class="token keyword">in</span> accounts <span class="token punctuation">{</span>
            <span class="token keyword">if</span> account<span class="token punctuation">.</span>owner <span class="token operator">!=</span> program_id <span class="token punctuation">{</span>
                <span class="token keyword">continue</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>

            <span class="token keyword">let</span> data <span class="token operator">=</span> account<span class="token punctuation">.</span>data<span class="token punctuation">;</span>
            <span class="token keyword">if</span> data<span class="token punctuation">.</span><span class="token function">len</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&lt;</span> <span class="token number">200</span> <span class="token punctuation">{</span>
                <span class="token keyword">continue</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>

            <span class="token keyword">let</span> base_mint <span class="token operator">=</span> data<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.32</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">let</span> quote_mint <span class="token operator">=</span> data<span class="token punctuation">[</span><span class="token number">32.</span><span class="token number">.64</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">if</span> base_mint<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">||</span> quote_mint<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token keyword">continue</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>

            <span class="token keyword">let</span> discriminator <span class="token operator">=</span> u64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>data<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.8</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">if</span> discriminator <span class="token operator">==</span> <span class="token number">0</span> <span class="token punctuation">{</span>
                <span class="token keyword">continue</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>

            <span class="token keyword">let</span> pool_address <span class="token operator">=</span> pubkey<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            pool_addresses<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">.</span><span class="token function">clone</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

            <span class="token keyword">if</span> <span class="token keyword">let</span> <span class="token function">Some</span><span class="token punctuation">(</span>accounts<span class="token punctuation">)</span> <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">derive_accounts_from_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>pool_address<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token constant">POOL_ADDRESS_MAP</span><span class="token punctuation">.</span><span class="token function">lock</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">,</span> accounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
        pool_addresses
    <span class="token punctuation">}</span>

    <span class="token keyword">async</span> fn <span class="token function">listen_new_pool_addresses</span><span class="token punctuation">(</span>
        <span class="token operator">&amp;</span>self<span class="token punctuation">,</span>
        client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span>
        address_tx<span class="token operator">:</span> Sender<span class="token operator">&lt;</span>String<span class="token operator">&gt;</span><span class="token punctuation">,</span>
    <span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Result<span class="token operator">&lt;</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> Box<span class="token operator">&lt;</span>dyn Error<span class="token operator">&gt;&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">let</span> program_id <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">dex_program_id</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> ws_url <span class="token operator">=</span> <span class="token string">"wss://api.mainnet-beta.solana.com"</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> <span class="token punctuation">(</span>mut ws_stream<span class="token punctuation">,</span> _<span class="token punctuation">)</span> <span class="token operator">=</span> <span class="token function">connect_async</span><span class="token punctuation">(</span>ws_url<span class="token punctuation">)</span><span class="token punctuation">.</span>await<span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> subscribe_msg <span class="token operator">=</span> format<span class="token operator">!</span><span class="token punctuation">(</span>
            r#<span class="token string">"{"</span>jsonrpc<span class="token string">":"</span><span class="token number">2.0</span><span class="token string">","</span>id<span class="token string">":1,"</span>method<span class="token string">":"</span>logsSubscribe<span class="token string">","</span>params<span class="token string">":["</span>mentions<span class="token string">","</span><span class="token punctuation">{</span><span class="token punctuation">}</span><span class="token string">"]}"</span>#<span class="token punctuation">,</span>
            program_id
        <span class="token punctuation">)</span><span class="token punctuation">;</span>
        ws_stream<span class="token punctuation">.</span><span class="token function">send</span><span class="token punctuation">(</span>Message<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Text</span><span class="token punctuation">(</span>subscribe_msg<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>await<span class="token operator">?</span><span class="token punctuation">;</span>

        <span class="token keyword">while</span> <span class="token keyword">let</span> <span class="token function">Some</span><span class="token punctuation">(</span>msg<span class="token punctuation">)</span> <span class="token operator">=</span> ws_stream<span class="token punctuation">.</span><span class="token function">next</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>await <span class="token punctuation">{</span>
            <span class="token keyword">let</span> msg <span class="token operator">=</span> msg<span class="token operator">?</span><span class="token punctuation">;</span>
            <span class="token keyword">if</span> <span class="token keyword">let</span> Message<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Text</span><span class="token punctuation">(</span>text<span class="token punctuation">)</span> <span class="token operator">=</span> msg <span class="token punctuation">{</span>
                <span class="token keyword">let</span> log<span class="token operator">:</span> serde_json<span class="token operator">:</span><span class="token operator">:</span>Value <span class="token operator">=</span> serde_json<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>text<span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
                <span class="token keyword">if</span> log<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token string">"result"</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">is_some</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword">continue</span><span class="token punctuation">;</span>
                <span class="token punctuation">}</span>

                <span class="token keyword">let</span> params <span class="token operator">=</span> log<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token string">"params"</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">and_then</span><span class="token punctuation">(</span><span class="token operator">|</span>p<span class="token operator">|</span> p<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token string">"result"</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok_or</span><span class="token punctuation">(</span><span class="token string">"No params"</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
                <span class="token keyword">let</span> tx_sig <span class="token operator">=</span> params<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token string">"signature"</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">and_then</span><span class="token punctuation">(</span><span class="token operator">|</span>s<span class="token operator">|</span> s<span class="token punctuation">.</span><span class="token function">as_str</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok_or</span><span class="token punctuation">(</span><span class="token string">"No signature"</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
                <span class="token keyword">let</span> logs <span class="token operator">=</span> params<span class="token punctuation">.</span><span class="token function">get</span><span class="token punctuation">(</span><span class="token string">"logs"</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">and_then</span><span class="token punctuation">(</span><span class="token operator">|</span>l<span class="token operator">|</span> l<span class="token punctuation">.</span><span class="token function">as_array</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok_or</span><span class="token punctuation">(</span><span class="token string">"No logs"</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>

                <span class="token keyword">let</span> tx <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_transaction</span><span class="token punctuation">(</span>
                    <span class="token operator">&amp;</span>Signature<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>tx_sig<span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">,</span>
                    CommitmentConfig<span class="token operator">:</span><span class="token operator">:</span><span class="token function">confirmed</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
                <span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
                <span class="token keyword">if</span> tx<span class="token punctuation">.</span>meta<span class="token punctuation">.</span><span class="token function">is_some</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&amp;&amp;</span> tx<span class="token punctuation">.</span>meta<span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span>err<span class="token punctuation">.</span><span class="token function">is_some</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword">continue</span><span class="token punctuation">;</span>
                <span class="token punctuation">}</span>

                <span class="token keyword">let</span> log_str <span class="token operator">=</span> logs<span class="token punctuation">.</span><span class="token function">iter</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">filter_map</span><span class="token punctuation">(</span><span class="token operator">|</span>l<span class="token operator">|</span> l<span class="token punctuation">.</span><span class="token function">as_str</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>collect<span class="token operator">:</span><span class="token operator">:</span><span class="token operator">&lt;</span>Vec<span class="token operator">&lt;</span><span class="token operator">&amp;</span>str<span class="token operator">&gt;&gt;</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">join</span><span class="token punctuation">(</span><span class="token string">" "</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">let</span> account_keys <span class="token operator">=</span> tx<span class="token punctuation">.</span>transaction<span class="token punctuation">.</span>message<span class="token punctuation">.</span>account_keys<span class="token punctuation">;</span>

                <span class="token keyword">for</span> <span class="token punctuation">(</span>i<span class="token punctuation">,</span> key<span class="token punctuation">)</span> <span class="token keyword">in</span> account_keys<span class="token punctuation">.</span><span class="token function">iter</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">enumerate</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword">if</span> tx<span class="token punctuation">.</span>transaction<span class="token punctuation">.</span>message<span class="token punctuation">.</span><span class="token function">is_writable</span><span class="token punctuation">(</span>i<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                        <span class="token keyword">let</span> pool_address <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">find_pool_address_from_account</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                        <span class="token keyword">if</span> pool_address<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&amp;&amp;</span> self<span class="token punctuation">.</span><span class="token function">is_valid_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                            <span class="token keyword">if</span> <span class="token keyword">let</span> <span class="token function">Some</span><span class="token punctuation">(</span>accounts<span class="token punctuation">)</span> <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">derive_accounts_from_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                                <span class="token constant">POOL_ADDRESS_MAP</span><span class="token punctuation">.</span><span class="token function">lock</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> accounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
                                info<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Detected new {} pool address: {}"</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span><span class="token function">dex_name</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> key<span class="token punctuation">)</span><span class="token punctuation">;</span>
                                address_tx<span class="token punctuation">.</span><span class="token function">send</span><span class="token punctuation">(</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span>await<span class="token operator">?</span><span class="token punctuation">;</span>
                            <span class="token punctuation">}</span>
                        <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token keyword">if</span> <span class="token operator">!</span>pool_address<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                            info<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Detected writable account affecting pool: {}, Pool: {}"</span><span class="token punctuation">,</span> tx_sig<span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
                            address_tx<span class="token punctuation">.</span><span class="token function">send</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span><span class="token punctuation">.</span>await<span class="token operator">?</span><span class="token punctuation">;</span>
                        <span class="token punctuation">}</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">}</span>

                <span class="token keyword">if</span> log_str<span class="token punctuation">.</span><span class="token function">contains</span><span class="token punctuation">(</span><span class="token string">"initialize"</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                    <span class="token keyword">if</span> <span class="token keyword">let</span> <span class="token function">Some</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span> <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">extract_new_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> tx_sig<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                        <span class="token keyword">if</span> self<span class="token punctuation">.</span><span class="token function">is_valid_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>pool_address<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                            <span class="token keyword">if</span> <span class="token keyword">let</span> <span class="token function">Some</span><span class="token punctuation">(</span>accounts<span class="token punctuation">)</span> <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">derive_accounts_from_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>pool_address<span class="token punctuation">)</span> <span class="token punctuation">{</span>
                                <span class="token constant">POOL_ADDRESS_MAP</span><span class="token punctuation">.</span><span class="token function">lock</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">.</span><span class="token function">clone</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> accounts<span class="token punctuation">)</span><span class="token punctuation">;</span>
                                info<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Detected new {} pool address: {}"</span><span class="token punctuation">,</span> self<span class="token punctuation">.</span><span class="token function">dex_name</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
                                address_tx<span class="token punctuation">.</span><span class="token function">send</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span><span class="token punctuation">.</span>await<span class="token operator">?</span><span class="token punctuation">;</span>
                            <span class="token punctuation">}</span>
                        <span class="token punctuation">}</span>
                    <span class="token punctuation">}</span>
                <span class="token punctuation">}</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
        <span class="token function">Ok</span><span class="token punctuation">(</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">fetch_pool_metadata</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> pool_address<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Option<span class="token operator">&lt;</span>PoolMetadata<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">let</span> derived_accounts <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">derive_accounts_from_pool_address</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> out <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_account_data</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> out<span class="token punctuation">.</span><span class="token function">len</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&lt;</span> <span class="token number">200</span> <span class="token punctuation">{</span>
            error<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Pool data too short for {}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> None<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> base_reserve <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">get_vault_balance</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>derived_accounts<span class="token punctuation">.</span>base_vault<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> quote_reserve <span class="token operator">=</span> self<span class="token punctuation">.</span><span class="token function">get_vault_balance</span><span class="token punctuation">(</span>client<span class="token punctuation">,</span> <span class="token operator">&amp;</span>derived_accounts<span class="token punctuation">.</span>quote_vault<span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> fee_data <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_account_data</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>derived_accounts<span class="token punctuation">.</span>fee_state<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> fee_numerator <span class="token operator">=</span> u64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>fee_data<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.8</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> fee_denominator <span class="token operator">=</span> u64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>fee_data<span class="token punctuation">[</span><span class="token number">8.</span><span class="token number">.16</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> trade_fee <span class="token operator">=</span> <span class="token keyword">if</span> fee_denominator <span class="token operator">&gt;</span> <span class="token number">0</span> <span class="token punctuation">{</span> <span class="token function">Some</span><span class="token punctuation">(</span>fee_numerator <span class="token keyword">as</span> f64 <span class="token operator">/</span> fee_denominator <span class="token keyword">as</span> f64<span class="token punctuation">)</span> <span class="token punctuation">}</span> <span class="token keyword">else</span> <span class="token punctuation">{</span> None <span class="token punctuation">}</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> sqrt_price_x64 <span class="token operator">=</span> u64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>out<span class="token punctuation">[</span><span class="token number">64.</span><span class="token number">.72</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_current_index <span class="token operator">=</span> i32<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>out<span class="token punctuation">[</span><span class="token number">72.</span><span class="token number">.76</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> tick_array_data <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_account_data</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>derived_accounts<span class="token punctuation">.</span>tick_array_current<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap_or_default</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> mut tick_array <span class="token operator">=</span> Vec<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> <span class="token operator">!</span>tick_array_data<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">for</span> i <span class="token keyword">in</span> <span class="token punctuation">(</span><span class="token number">8.</span><span class="token punctuation">.</span>tick_array_data<span class="token punctuation">.</span><span class="token function">len</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">-</span> <span class="token number">12</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">step_by</span><span class="token punctuation">(</span><span class="token number">12</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token keyword">let</span> tick_index <span class="token operator">=</span> i32<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>tick_array_data<span class="token punctuation">[</span>i<span class="token punctuation">.</span><span class="token punctuation">.</span>i<span class="token operator">+</span><span class="token number">4</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                <span class="token keyword">let</span> liquidity <span class="token operator">=</span> f64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>tick_array_data<span class="token punctuation">[</span>i<span class="token operator">+</span><span class="token number">4.</span><span class="token punctuation">.</span>i<span class="token operator">+</span><span class="token number">12</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token operator">/</span> <span class="token number">1_000_000.0</span><span class="token punctuation">;</span>
                <span class="token keyword">let</span> mut tick_map <span class="token operator">=</span> HashMap<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                tick_map<span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span><span class="token string">"tick_index"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Number</span><span class="token punctuation">(</span>tick_index <span class="token keyword">as</span> f64<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                tick_map<span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span><span class="token string">"liquidity"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Number</span><span class="token punctuation">(</span>liquidity<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
                tick_array<span class="token punctuation">.</span><span class="token function">push</span><span class="token punctuation">(</span>PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Map</span><span class="token punctuation">(</span>tick_map<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> mut extra <span class="token operator">=</span> HashMap<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        extra<span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span><span class="token string">"sqrt_price_x64"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Number</span><span class="token punctuation">(</span>sqrt_price_x64 <span class="token keyword">as</span> f64<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        extra<span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span><span class="token string">"tick_current_index"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Number</span><span class="token punctuation">(</span>tick_current_index <span class="token keyword">as</span> f64<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        extra<span class="token punctuation">.</span><span class="token function">insert</span><span class="token punctuation">(</span><span class="token string">"tick_array"</span><span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> PoolMetadataValue<span class="token operator">:</span><span class="token operator">:</span><span class="token function">Array</span><span class="token punctuation">(</span>tick_array<span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token function">Some</span><span class="token punctuation">(</span>PoolMetadata <span class="token punctuation">{</span>
            pool_address<span class="token operator">:</span> pool_address<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            base_mint<span class="token operator">:</span> derived_accounts<span class="token punctuation">.</span>base_mint<span class="token punctuation">,</span>
            quote_mint<span class="token operator">:</span> derived_accounts<span class="token punctuation">.</span>quote_mint<span class="token punctuation">,</span>
            base_reserve<span class="token operator">:</span> <span class="token function">Some</span><span class="token punctuation">(</span>base_reserve<span class="token punctuation">)</span><span class="token punctuation">,</span>
            quote_reserve<span class="token operator">:</span> <span class="token function">Some</span><span class="token punctuation">(</span>quote_reserve<span class="token punctuation">)</span><span class="token punctuation">,</span>
            trade_fee<span class="token punctuation">,</span>
            extra<span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
impl RaydiumCLMM <span class="token punctuation">{</span>
    fn <span class="token function">derive_accounts_from_pool_address</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> pool_address<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Option<span class="token operator">&lt;</span>PoolDerivedAccounts<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">let</span> out <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_account_data</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> out<span class="token punctuation">.</span><span class="token function">len</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&lt;</span> <span class="token number">200</span> <span class="token punctuation">{</span>
            error<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"Pool data too short for {}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token keyword">return</span> None<span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> base_mint <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.32</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> quote_mint <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">32.</span><span class="token number">.64</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> base_vault <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">96.</span><span class="token number">.128</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> quote_vault <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">128.</span><span class="token number">.160</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> fee_state <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">160.</span><span class="token number">.192</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> tick_array_current_seed <span class="token operator">=</span> format<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"tick_array{}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_array_current <span class="token operator">=</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">create_program_address</span><span class="token punctuation">(</span>
            <span class="token operator">&amp;</span><span class="token punctuation">[</span><span class="token operator">&amp;</span>tick_array_current_seed<span class="token punctuation">.</span><span class="token function">as_bytes</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> tick_array_prev_seed <span class="token operator">=</span> format<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"tick_array_prev{}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_array_prev <span class="token operator">=</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">create_program_address</span><span class="token punctuation">(</span>
            <span class="token operator">&amp;</span><span class="token punctuation">[</span><span class="token operator">&amp;</span>tick_array_prev_seed<span class="token punctuation">.</span><span class="token function">as_bytes</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> tick_array_next_seed <span class="token operator">=</span> format<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"tick_array_next{}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> tick_array_next <span class="token operator">=</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">create_program_address</span><span class="token punctuation">(</span>
            <span class="token operator">&amp;</span><span class="token punctuation">[</span><span class="token operator">&amp;</span>tick_array_next_seed<span class="token punctuation">.</span><span class="token function">as_bytes</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token keyword">let</span> observation_state_seed <span class="token operator">=</span> format<span class="token operator">!</span><span class="token punctuation">(</span><span class="token string">"observation_state{}"</span><span class="token punctuation">,</span> pool_address<span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> observation_state <span class="token operator">=</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">create_program_address</span><span class="token punctuation">(</span>
            <span class="token operator">&amp;</span><span class="token punctuation">[</span><span class="token operator">&amp;</span>observation_state_seed<span class="token punctuation">.</span><span class="token function">as_bytes</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">]</span><span class="token punctuation">,</span>
            <span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>

        <span class="token function">Some</span><span class="token punctuation">(</span>PoolDerivedAccounts <span class="token punctuation">{</span>
            pool_address<span class="token operator">:</span> pool_address<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            base_mint<span class="token punctuation">,</span>
            quote_mint<span class="token punctuation">,</span>
            base_vault<span class="token punctuation">,</span>
            quote_vault<span class="token punctuation">,</span>
            fee_state<span class="token punctuation">,</span>
            tick_array_current<span class="token punctuation">,</span>
            tick_array_prev<span class="token punctuation">,</span>
            tick_array_next<span class="token punctuation">,</span>
            observation_state<span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">find_pool_address_from_account</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> account_address<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> String <span class="token punctuation">{</span>
        <span class="token keyword">let</span> map <span class="token operator">=</span> <span class="token constant">POOL_ADDRESS_MAP</span><span class="token punctuation">.</span><span class="token function">lock</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">for</span> <span class="token punctuation">(</span>pool_address<span class="token punctuation">,</span> accounts<span class="token punctuation">)</span> <span class="token keyword">in</span> map<span class="token punctuation">.</span><span class="token function">iter</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">if</span> account_address <span class="token operator">==</span> pool_address <span class="token operator">||</span>
               account_address <span class="token operator">==</span> <span class="token operator">&amp;</span>accounts<span class="token punctuation">.</span>base_vault <span class="token operator">||</span>
               account_address <span class="token operator">==</span> <span class="token operator">&amp;</span>accounts<span class="token punctuation">.</span>quote_vault <span class="token operator">||</span>
               account_address <span class="token operator">==</span> <span class="token operator">&amp;</span>accounts<span class="token punctuation">.</span>tick_array_current <span class="token operator">||</span>
               account_address <span class="token operator">==</span> <span class="token operator">&amp;</span>accounts<span class="token punctuation">.</span>tick_array_prev <span class="token operator">||</span>
               account_address <span class="token operator">==</span> <span class="token operator">&amp;</span>accounts<span class="token punctuation">.</span>tick_array_next <span class="token punctuation">{</span>
                <span class="token keyword">return</span> pool_address<span class="token punctuation">.</span><span class="token function">clone</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
        String<span class="token operator">:</span><span class="token operator">:</span><span class="token keyword">new</span><span class="token punctuation">(</span><span class="token punctuation">)</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">is_valid_pool_address</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> pool_address<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> bool <span class="token punctuation">{</span>
        <span class="token keyword">let</span> out <span class="token operator">=</span> match client<span class="token punctuation">.</span><span class="token function">get_account_data</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>pool_address<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token function">Ok</span><span class="token punctuation">(</span>data<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> data<span class="token punctuation">,</span>
            <span class="token function">Err</span><span class="token punctuation">(</span>_<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token keyword">return</span> <span class="token boolean">false</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span><span class="token punctuation">;</span>

        <span class="token keyword">if</span> out<span class="token punctuation">.</span><span class="token function">len</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&lt;</span> <span class="token number">200</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token boolean">false</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">if</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>out<span class="token punctuation">.</span>owner<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">!=</span> Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span><span class="token constant">PROGRAM_ID</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token boolean">false</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> base_mint <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.32</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">let</span> quote_mint <span class="token operator">=</span> out<span class="token punctuation">[</span><span class="token number">32.</span><span class="token number">.64</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">to_base58</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> base_mint<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">||</span> quote_mint<span class="token punctuation">.</span><span class="token function">is_empty</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token boolean">false</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token keyword">let</span> discriminator <span class="token operator">=</span> u64<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_le_bytes</span><span class="token punctuation">(</span>out<span class="token punctuation">[</span><span class="token number">0.</span><span class="token number">.8</span><span class="token punctuation">]</span><span class="token punctuation">.</span><span class="token function">try_into</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
        <span class="token keyword">if</span> discriminator <span class="token operator">==</span> <span class="token number">0</span> <span class="token punctuation">{</span>
            <span class="token keyword">return</span> <span class="token boolean">false</span><span class="token punctuation">;</span>
        <span class="token punctuation">}</span>

        <span class="token boolean">true</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">get_vault_balance</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> vault<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> f64 <span class="token punctuation">{</span>
        match client<span class="token punctuation">.</span><span class="token function">get_token_account_balance</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>Pubkey<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>vault<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">unwrap</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span> CommitmentConfig<span class="token operator">:</span><span class="token operator">:</span><span class="token function">confirmed</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
            <span class="token function">Ok</span><span class="token punctuation">(</span>resp<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> resp<span class="token punctuation">.</span>ui_amount<span class="token punctuation">.</span><span class="token function">unwrap_or</span><span class="token punctuation">(</span><span class="token number">0.0</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
            <span class="token function">Err</span><span class="token punctuation">(</span>_<span class="token punctuation">)</span> <span class="token operator">=&gt;</span> <span class="token number">0.0</span><span class="token punctuation">,</span>
        <span class="token punctuation">}</span>
    <span class="token punctuation">}</span>

    fn <span class="token function">extract_new_pool_address</span><span class="token punctuation">(</span><span class="token operator">&amp;</span>self<span class="token punctuation">,</span> client<span class="token operator">:</span> <span class="token operator">&amp;</span>RpcClient<span class="token punctuation">,</span> tx_sig<span class="token operator">:</span> <span class="token operator">&amp;</span>str<span class="token punctuation">)</span> <span class="token operator">-</span><span class="token operator">&gt;</span> Option<span class="token operator">&lt;</span>String<span class="token operator">&gt;</span> <span class="token punctuation">{</span>
        <span class="token keyword">let</span> tx <span class="token operator">=</span> client<span class="token punctuation">.</span><span class="token function">get_transaction</span><span class="token punctuation">(</span>
            <span class="token operator">&amp;</span>Signature<span class="token operator">:</span><span class="token operator">:</span><span class="token function">from_str</span><span class="token punctuation">(</span>tx_sig<span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">,</span>
            CommitmentConfig<span class="token operator">:</span><span class="token operator">:</span><span class="token function">confirmed</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">,</span>
        <span class="token punctuation">)</span><span class="token punctuation">.</span><span class="token function">ok</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token operator">?</span><span class="token punctuation">;</span>
        <span class="token keyword">for</span> key <span class="token keyword">in</span> tx<span class="token punctuation">.</span>transaction<span class="token punctuation">.</span>message<span class="token punctuation">.</span>account_keys <span class="token punctuation">{</span>
            <span class="token keyword">if</span> key<span class="token punctuation">.</span><span class="token function">is_writable</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token operator">&amp;&amp;</span> <span class="token operator">!</span>key<span class="token punctuation">.</span><span class="token function">is_signer</span><span class="token punctuation">(</span><span class="token punctuation">)</span> <span class="token punctuation">{</span>
                <span class="token keyword">return</span> <span class="token function">Some</span><span class="token punctuation">(</span>key<span class="token punctuation">.</span><span class="token function">to_string</span><span class="token punctuation">(</span><span class="token punctuation">)</span><span class="token punctuation">)</span><span class="token punctuation">;</span>
            <span class="token punctuation">}</span>
        <span class="token punctuation">}</span>
        None
    <span class="token punctuation">}</span>
<span class="token punctuation">}</span>
</code></pre></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "DEX 集成"
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
    "AMM 接入示例",
    "基于 Raydium CLMM 的实现例子"
  ]
}
```

</details>
