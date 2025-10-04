# 错误码 | 跨链 API | 交易 API | DEX API | DEX API 文档 | 欧易

**URL:** https://web3.okx.com/zh-hans/build/dev-docs/dex-api/dex-crosschain-error-code#错误码  
**抓取时间:** 2025-05-27 01:01:40  
**字数:** 89

## 导航路径
DEX API > 交易 API > 错误码

## 目录
- 搭建兑换应用
- 搭建跨链应用
- 介绍
- API 参考
- 设置分佣
- DEX 集成
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 支持的跨链桥
- 智能合约
- 错误码
- FAQ
- 介绍
- API 参考
- 错误码

---

错误码
#
错误码
HTTP 状态
提示信息
0
200
操作成功
50011
429
用户请求频率过快，超过该接口允许的限额。请参考 API 文档并限制请求
50014
400
必填参数 {param0} 不能为空
50026
500
系统错误，请稍后重试
50103
401
请求头“OK_ACCESS_KEY”不能为空
50104
401
请求头“OK_ACCESS_PASSPHRASE“不能为空
50105
401
请求头“OK_ACCESS_PASSPHRASE“错误
50106
401
请求头“OK_ACCESS_SIGN“不能为空
50107
401
请求头“OK_ACCESS_TIMESTAMP“不能为空
50111
401
无效的 OK_ACCESS_KEY
50112
401
无效的 OK_ACCESS_TIMESTAMP
50113
401
无效的签名
51000
400
{param0} 参数错误
80000
200
重复提交
82000
200
流动性不足
82001
500
分佣服务暂不可用
82102
200
最小数量是 {0}
82103
200
最大数量是 {0}
82104
200
不支持该币种
82105
200
不支持该链
82112
200
当前交易的询价路径价差超过 {num}，可能造成用户的资产损失。
82114
200
滑点过小，建议你提高滑点到 {num}
82115
200
该链没有币对
82116
200
没有合适的跨链桥

---

<details>
<summary>原始HTML内容</summary>

```html
<div class="routes_md__xWlGF"><!--$--><h1 id="错误码">错误码<a class="index_header-anchor__Xqb+L" href="#错误码" style="opacity:0">#</a></h1>
<div class="index_table__kvZz5"><table><thead><tr><th>错误码</th><th>HTTP 状态</th><th>提示信息</th></tr></thead><tbody><tr><td>0</td><td>200</td><td>操作成功</td></tr><tr><td>50011</td><td>429</td><td>用户请求频率过快，超过该接口允许的限额。请参考 API 文档并限制请求</td></tr><tr><td>50014</td><td>400</td><td>必填参数 {param0} 不能为空</td></tr><tr><td>50026</td><td>500</td><td>系统错误，请稍后重试</td></tr><tr><td>50103</td><td>401</td><td>请求头“OK_ACCESS_KEY”不能为空</td></tr><tr><td>50104</td><td>401</td><td>请求头“OK_ACCESS_PASSPHRASE“不能为空</td></tr><tr><td>50105</td><td>401</td><td>请求头“OK_ACCESS_PASSPHRASE“错误</td></tr><tr><td>50106</td><td>401</td><td>请求头“OK_ACCESS_SIGN“不能为空</td></tr><tr><td>50107</td><td>401</td><td>请求头“OK_ACCESS_TIMESTAMP“不能为空</td></tr><tr><td>50111</td><td>401</td><td>无效的 OK_ACCESS_KEY</td></tr><tr><td>50112</td><td>401</td><td>无效的 OK_ACCESS_TIMESTAMP</td></tr><tr><td>50113</td><td>401</td><td>无效的签名</td></tr><tr><td>51000</td><td>400</td><td>{param0} 参数错误</td></tr><tr><td>80000</td><td>200</td><td>重复提交</td></tr><tr><td>82000</td><td>200</td><td>流动性不足</td></tr><tr><td>82001</td><td>500</td><td>分佣服务暂不可用</td></tr><tr><td>82102</td><td>200</td><td>最小数量是 {0}</td></tr><tr><td>82103</td><td>200</td><td>最大数量是 {0}</td></tr><tr><td>82104</td><td>200</td><td>不支持该币种</td></tr><tr><td>82105</td><td>200</td><td>不支持该链</td></tr><tr><td>82112</td><td>200</td><td>当前交易的询价路径价差超过 {num}，可能造成用户的资产损失。</td></tr><tr><td>82114</td><td>200</td><td>滑点过小，建议你提高滑点到 {num}</td></tr><tr><td>82115</td><td>200</td><td>该链没有币对</td></tr><tr><td>82116</td><td>200</td><td>没有合适的跨链桥</td></tr></tbody></table></div><!--/$--></div>
```

</details>

<details>
<summary>导航信息</summary>

```json
{
  "breadcrumbs": [
    "DEX API",
    "交易 API",
    "错误码"
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
  ]
}
```

</details>
