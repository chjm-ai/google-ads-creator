# Google Ads 认可的国家/地区名称

Location 字段必须使用 Google Ads 认可的英文名称，否则导入会被忽略或报错。常用对照：

| 常用名 | Google Ads 认可名称 |
|--------|-------------------|
| Turkey | **Turkiye** |
| Vietnam | Vietnam |
| Indonesia | Indonesia |
| Thailand | Thailand |
| Philippines | Philippines |
| Malaysia | Malaysia |
| UAE | United Arab Emirates |
| USA | United States |
| UK | United Kingdom |

格式规则：
- 多个地区用分号分隔：`Indonesia; Vietnam; Thailand`
- 带出价调整：`Indonesia : +20% ; Vietnam ; Thailand : -10%`
- 值含逗号时整体用双引号包裹

不在上表的国家，沿用 Google Ads 后台地理定向里显示的官方英文名（多数与通用英文名一致，Turkey→Turkiye 是最常见的例外）。
