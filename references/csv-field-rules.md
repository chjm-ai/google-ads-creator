# 任务二 CSV 逐字段规则（Google Ads Editor 导入格式）

> 生成 CSV 时参考本文件。**确定性校验交给 `scripts/validate_csv.py`，不要手工逐字段比对。**
> 权威列头永远以 `templates/*_mcc_template.csv` 为准；本文件解释每个字段填什么。
> 所有 CSV 一律 **UTF-8** 编码。字段值含逗号时用双引号包裹。空列不可省略（用逗号占位），列数必须与模板一致。

---

## campaign.csv（对应 `templates/campaign_mcc_template.csv`，34 列）

| 字段 | 值 | 说明 |
|------|-----|------|
| Row Type | `Campaign` | 固定 |
| Action | `Add` | 新建 |
| Campaign status | `Paused` | 建议先 Paused，用户检查后再启用 |
| Customer ID | `123-456-7890` | 必填，用户提供 |
| Campaign ID | 留空 | 新建时无 ID |
| Campaign | 广告系列名 | 如 `SEA_PVCResin_Search_EN` |
| Campaign type | `Search` | 搜索广告 |
| Networks | `Google search` | 不加 Search partners / Display |
| Budget | `15.00` | 纯数字日预算 |
| Delivery method | `Standard` | 不要留空 |
| Budget type | `Daily` | 不要留空 |
| Bid strategy type | `Manual CPC` | 低预算推荐。合法值：`Maximize clicks`/`Target CPA`/`Maximize Conversions` |
| Bid strategy | 留空 | 非 Portfolio 策略时留空 |
| Campaign start date | `2026-04-01` | YYYY-MM-DD |
| Campaign end date | 留空 | 试水期不设 |
| Language | `en; vi; id` | ISO 代码，分号分隔 |
| Location | 见 `country-names.md` | 必须用 Google 认可名称，分号分隔 |
| Exclusion | 同 Location 格式 | 排除地区 |
| Devices | 留空 | 留空=所有设备。调整须写全三种，**严禁 "All devices"**（见下） |
| Label | 留空 | |
| Target CPA / Target ROAS | 留空 | Manual CPC 时留空 |
| Display URL option | 留空 | |
| Website description | 留空 | |
| Target Impression Share | 留空 | |
| Max CPC Bid Limit for Target IS | 留空 | |
| Location Goal for Target IS | 留空 | |
| Tracking template | 留空 | 除非用户提供 |
| Final URL suffix | 留空 | 除非用户提供 |
| Custom parameter | 留空 | |
| Inventory type | 留空 | Search 不需要 |
| Campaign subtype | 留空 | Search 不需要 |
| Video ad formats | 留空 | Search 不需要 |
| **EU political ads** | **`No`** | **必填！Required on create，留空会导入失败** |

### Devices 字段（高频出错）
- 留空 = 所有设备，不调整（最常用）
- 调整须三种设备全写：`Computers:+0%; Mobile devices with full browsers:-20%; Tablets with full browsers:-20%`
- 设备名必须精确：`Computers`、`Mobile devices with full browsers`、`Tablets with full browsers`
- **严禁** `All devices` / `all` / `All`
- Location 带出价调整格式：`Indonesia : +20% ; Vietnam ; Thailand : -10%`

---

## ad_group.csv（对应 `templates/ad_group_mcc_template.csv`，22 列）

- Row Type = `Ad group`，Action = `Add`
- Ad group type = `Standard`
- Default max. CPC：数字如 `0.70`
- Campaign 列必须与 campaign.csv 的 Campaign 名完全一致（含大小写空格）

---

## keyword.csv（对应 `templates/keyword_mcc_template.csv`，19 列）

- Row Type = `Keyword`，Action = `Add`
- Type：`Phrase match` 或 `Exact match`（**严禁 Broad match 除非用户明确要求**）
- Keyword：纯文本，不加引号括号（Google 按 Type 列套用匹配方式）
- Campaign / Ad group 列必须与上游文件完全一致

---

## negative_keyword.csv（对应 `templates/ad_group_negative_keyword_mcc_template.csv`，12 列）

- Row Type = `Negative keyword`，Action = `Add`
- Level：`Campaign`（全局否定）或 `Ad group`（组级否定）
- Type：通常 `Phrase match`

---

## responsive_search_ad.csv（对应 `templates/responsive_search_ad_mcc_template.csv`，56 列）

- Row Type = `Ad`，Action = `Add`，Ad type = `Responsive search ad`
- **至少 5 个不重复 Headline**，每个 ≤30 字符
- **至少 2 个 Description**，每个 ≤90 字符
- Headline/Description position：`1`/`2`/`3` 固定位置，留空则自动轮播
- Path 1 / Path 2：展示 URL 路径，每段 ≤15 字符
- Final URL：落地页完整 URL

### 字符限制（硬性，校验器会逐条检查）
```
Headline:    ≤30 字符（含空格）  超出则改写，不要截断造成语义不通
Description: ≤90 字符（含空格）
Path 1/2:    ≤15 字符
```

---

## 生成后必做：脚本校验

CSV 全部写入后，对输出目录运行：
```bash
python scripts/validate_csv.py ~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/
```
校验器自动检查：列头/列数、RSA 字符限制、Devices 禁用项、Broad match 禁用项、EU political ads 必填、每行列数一致。
出现 FAIL 必须先修复再交付给用户。用户明确要 Broad match 时加 `--allow-broad`。
