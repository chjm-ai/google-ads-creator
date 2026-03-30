# Google Ads Creator

一个用于 Google Ads 投放规划与批量文件生成的技能，适合：

- 制定 Google Ads 投放计划
- 生成“首次创建广告”用的导入 CSV
- 生成“更新现有广告”用的更新 CSV

## 能做什么

| 任务 | 说明 | 输出 |
|------|------|------|
| **任务一：生成投放计划** | 通过分轮问答收集业务信息、目标市场、预算、网站结构，生成完整投放策略文档 | `投放计划.md` |
| **任务二：生成新建导入文件** | 根据投放计划生成“首次创建广告”所需的 Google Ads Editor / 批量上传 CSV | 5 个 CSV 文件 |
| **任务三：生成更新文件** | 基于用户从 Google Ads 或 Google Ads Editor 导出的现有数据，生成“更新现有广告/预算/URL/文案”所需 CSV | `*_update.csv` |

## 典型工作流

### 场景 A：从零开始投放

```text
你：帮我做 Google Ads 投放
  ↓
技能：分轮提问，收集业务、预算、市场、网站信息
  ↓
技能：分析网站结构，提取真实 URL
  ↓
技能：生成投放计划
  ↓
技能：生成首次创建广告用 CSV
```

### 场景 B：后续更新线上广告

```text
你：我想改预算 / 改 URL / 改文案后重新上传
  ↓
技能：先判断这是“更新现有广告”，不是“首次创建”
  ↓
技能：提示你先从 Google Ads / Google Ads Editor 导出当前数据
  ↓
你：上传导出的 CSV/XLSX
  ↓
技能：基于导出文件生成 update CSV
```

## 重要原则

### 1. 首次创建和后续更新是两套流程

- **首次创建**：可以使用技能生成的新建 CSV
- **后续更新**：必须基于 Google Ads / Google Ads Editor 导出的现有数据来改

### 2. 更新现有广告时，不能直接改“创建模板”

原因：

- 更新时往往需要 `Campaign ID`、`Ad group ID`、`Ad ID`、`Keyword ID` 或 `#Original` 列
- 这些列通常只能从 Google Ads 或 Google Ads Editor 导出获得
- 直接修改“首次创建用 CSV”再上传，系统很容易报错，或把更新识别成新建

## 更新现有广告时，用户需要先做什么

如果你要改的是已经在线上的 Campaign / 广告组 / 关键词 / 广告，请先导出当前数据。

### 方式 A：Google Ads 网页版导出

1. 打开 Google Ads
2. 进入要更新的对象页面
   - 广告系列
   - 广告组
   - 关键词
   - 广告
3. 点击右上角下载图标
4. 选择“更多选项”
5. 勾选“用于批量上传的可修改列”
6. 下载为 CSV 或 Excel

### 方式 B：Google Ads Editor 导出

1. 打开 Google Ads Editor
2. 同步账户
3. 进入要更新的对象视图
4. 导出当前数据
5. 如可选，保留 `#Original` 列

## 技能的特点

- **分轮问答**：不会一次抛出所有问题，每轮 3-5 个问题
- **网站结构分析**：自动抓取首页、产品页、关于页、联系页，提取真实着陆页 URL
- **多语言支持**：识别网站语言结构，为多语言投放提供 URL 和关键词策略依据
- **严格 CSV 校验**：校验列数、字符限制、国家名称、设备字段、`EU political ads`
- **更新流程保护**：遇到“更新现有广告”场景，会先要求导出数据，不会误用创建模板

## 生成的文件

### 首次创建广告

```text
~/Desktop/GoogleAds_BrandName_20260401/
├── 投放计划.md
├── campaign.csv
├── ad_group.csv
├── keyword.csv
├── negative_keyword.csv
├── responsive_search_ad.csv
└── README_导入指南.txt
```

### 更新现有广告

```text
~/Desktop/GoogleAds_BrandName_20260401/
├── campaign_update.csv
├── ad_group_update.csv
├── keyword_update.csv
├── negative_keyword_update.csv
├── responsive_search_ad_update.csv
└── README_更新说明.txt
```

## 使用示例

```text
帮我制定 Google Ads 投放计划
帮我生成 Google Ads 导入文件
我有投放计划，帮我生成创建用 CSV
我想更新现有广告的预算和 URL
我已经从 Google Ads 导出了数据，帮我生成 update CSV
```

## 模板文件

`templates/` 目录包含：

| 文件 | 用途 |
|------|------|
| `campaign_plan_template.md` | 投放计划模板 |
| `campaign_mcc_template.csv` | Campaign 导入模板 |
| `ad_group_mcc_template.csv` | Ad Group 导入模板 |
| `keyword_mcc_template.csv` | Keyword 导入模板 |
| `ad_group_negative_keyword_mcc_template.csv` | Negative Keyword 导入模板 |
| `responsive_search_ad_mcc_template.csv` | RSA 导入模板 |

## 要求

- 需要能访问 Google Ads 或 Google Ads Editor 导出的数据
- 首次创建时，需要 Google Ads Customer ID
- 不需要 Google Ads API

## 备注

- 本技能生成的是**离线导入文件**
- 最终导入和发布仍需用户自己在 Google Ads 或 Google Ads Editor 中完成
