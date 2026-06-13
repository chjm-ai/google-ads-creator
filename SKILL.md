---
name: google-ads-creator
description: 离线生成 Google Ads Editor 可导入的 CSV 文件（不连接账户、不写线上数据）。三个独立任务：(1) 问答引导生成投放计划文档；(2) 按计划生成「首次新建广告」的导入 CSV；(3) 基于用户从 Google Ads/Editor 导出的现有数据，生成「更新现有广告」的 CSV。Use when the user wants to create Google Ads campaigns offline, generate import/bulk-upload CSV files, prepare search ads, plan ad strategy, or says "帮我生成投放文件"、"帮我更新投放CSV"、"create google ads campaign"、"generate ad import file"、"制定投放计划"、"plan my ad campaign"。**不要用于**直接读写线上账户（查搜索词/加否定词/改预算/暂停关键词/审计账户走 google-ads-api；本 skill 只产离线文件供用户手动上传）。
---

# Google Ads Campaign Creator

离线生成 Google Ads Editor 可导入的 CSV（不连账户）。三个独立任务，可顺序执行也可单独运行。

| 任务 | 触发 | 输出 | 详细流程 |
|------|------|------|---------|
| **任务一：生成投放计划** | 只有产品/业务信息，无计划 | `投放计划.md` | `references/qa-flow.md` |
| **任务二：生成新建导入 CSV** | 已有投放计划，要首次建广告 | 5 个 CSV | 本文件 + `references/csv-field-rules.md` |
| **任务三：生成更新 CSV** | 有 Google Ads/Editor 导出数据，要改后再传 | `*_update.csv` | `references/update-flow.md` |

## 路由逻辑

```
用户说了什么？
├── 已有完整投放计划 ────────────────→ 任务二
├── 已有 Google Ads 导出数据，想改后上传 → 任务三
├── 说"更新/改预算/改URL/改文案后再上传"但没导出数据 → 先让用户导出，再任务三
├── 只有产品/业务信息，没有计划 ─────→ 任务一
├── "制定投放计划"/"plan my campaign" → 任务一
├── "生成导入文件"/"generate CSV" ───→ 任务二（先检查有无计划）
├── "更新CSV"/"refresh bulk upload" ─→ 任务三（先检查有无导出数据）
└── 不确定 → 问用户："先帮你制定投放计划，还是已有计划只需生成导入文件？"
```

路由判断点（见 Gotchas 的对应条目）：
- 说"后续更新/重新上传报错/改完再导入" → 默认判任务三，不要拿任务二新建 CSV 当更新用。
- 任务三缺导出数据 → 先提示导出，不要凭空造"更新模板"覆盖线上广告。

---

# 任务一：生成投放计划

完整问答流程 + 网站结构分析 + 计划生成规则见 **`references/qa-flow.md`**。

要点：分轮问（每轮 ≤5 问）→ 用户给 URL 后先爬站取真实 URL → 按 `templates/campaign_plan_template.md` 的 11 章节输出 → 存到 `~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/投放计划.md` → 确认后问是否进任务二。

---

# 任务二：生成新建导入 CSV

## 前置检查（缺一不可，缺则提示补充）

| 必需信息 | 来源 | 缺失提示 |
|----------|------|---------|
| Google Ads Customer ID | 用户提供 | "请提供客户 ID，格式 `123-456-7890`，在后台右上角。" |
| 投放计划 | 任务一 / 用户上传 | "我需要一份投放计划。可让我帮你做（任务一）或直接提供。" |
| 落地页 URL | 计划 / 用户 | "请提供广告落地页网址。" |
| 广告系列名称 | 计划 / 自动生成 | 可由品牌名+日期生成，如 `BrandName_Search_202603` |

## 生成流程

1. 读 **`references/csv-field-rules.md`** 获取 5 个文件的逐字段规则。
2. 列头**永远以 `templates/*_mcc_template.csv` 为权威来源**，不要手敲列头/数列。
3. 生成 5 个 CSV，写入输出目录。
4. **生成后必做：跑校验脚本**（见下）。
5. 校验通过后，按 **`references/import-guide.md`** 生成 `README_导入指南.txt` 并向用户展示导入步骤与顺序。

## 校验入口（确定性校验交给脚本，不要人工逐字段比对）

```bash
python scripts/validate_csv.py ~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/
```

脚本自动检查：列头/列数对齐模板、每行列数一致、RSA 字符限制（Headline≤30/Description≤90/Path≤15）、Devices 禁用项、Broad match 禁用项、EU political ads 必填。
出现 `[FAIL]` 必须先修复再交付。用户明确要 Broad match 时加 `--allow-broad`。

---

# 任务三：生成「更新现有广告」CSV

完整流程见 **`references/update-flow.md`**。

核心：**必须基于用户从 Google Ads/Editor 导出的现有数据修改**（保留 ID 列），不要拿任务二的新建模板当更新用。缺导出数据先提示用户导出。命名为 `*_update.csv`，附 `README_更新说明.txt`。

---

## Gotchas

来自真实失败的负面边界。每条具体、可判定。校验脚本已覆盖标 ✅ 的项，仍要人工守住其余项。

**CSV 字段（任务二）**
- ✅ **严禁 Devices 写 `All devices`/`all`/`All`**：留空=所有设备；要调整必须三种设备全写（`Computers:+0%; Mobile devices with full browsers:-20%; Tablets with full browsers:-20%`），设备名一字不差。
- ✅ **EU political ads 必填 `No`**：留空会导入失败（Required on create）。
- ✅ **关键词严禁 Broad match**：除非用户明确要求，只用 `Phrase match`/`Exact match`。
- ✅ **RSA 硬性字符限制**：Headline ≤30、Description ≤90、Path ≤15（含空格）。超限改写，不要截断造成语义不通。
- ✅ **列数必须等于模板**：空列也要用逗号占位，不能省。列数不一致字段会整体错位。
- **列头不要手敲**：永远从 `templates/*_mcc_template.csv` 复制，凭记忆敲 34 列必错。
- **字段值含逗号必须用双引号包裹**：如 `"Indonesia; Vietnam; Thailand"`，否则被当多列。
- **Networks 只填 `Google search`**：不要加 Search partners 或 Display Network。
- **Customer ID 每行都要填**：缺失会导入失败，不能只在第一行写。
- **Campaign/Ad group 名跨文件必须完全一致**（含大小写空格），否则子对象挂不上父对象。
- **国家名用 Google 认可名称**：最常见例外 `Turkey → Turkiye`（见 `references/country-names.md`），用错会被忽略。

**投放计划（任务一）**
- **URL 严禁编造**：着陆页/Sitelink/Path 的 URL 必须是从网站实际爬到的真实链接。期望页面不存在就在备注标"不存在，建议创建"，不要造路径。
- **着陆页不能全落首页**：每个 Ad Group 对应自己的着陆页。
- **广告组按搜索意图分，不按产品分**：典型分法产品词/地标词/OEM 定制词/品牌词。

**更新（任务三）**
- **没有导出数据就不要生成更新模板**：先纠正用户去导出。
- **不要删 ID 列**（`Campaign ID`/`Ad group ID`/`Ad ID`/`Keyword ID`/`#Original`），更新靠它匹配线上对象。
- **不要把任务二的创建 CSV 当任务三更新用**：有 ID 的行不要把 Action 改成 `Add`。

**路由 / 范围**
- **本 skill 不连接 Google Ads API**，只产离线文件。要直接读写线上账户（查搜索词/加否定词/改预算/审计）走 **google-ads-api**。
- **生成后不跑校验脚本不算完成**：必须 PASS 才交付。
