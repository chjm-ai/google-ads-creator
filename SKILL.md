  ---
name: google-ads-creator
description: Google Ads 投放助手，支持两个独立任务：(1) 通过问答引导生成投放计划文档；(2) 根据投放计划生成 Google Ads Editor 可导入的 CSV 文件。Use when the user wants to create Google Ads campaigns, generate ad import files, prepare search ads, plan ad strategy, or says things like "帮我生成广告投放文件", "create google ads campaign", "生成谷歌广告", "准备投放素材", "制定投放计划", "plan my ad campaign".
---

# Google Ads Campaign Creator

本 skill 提供两个独立任务，可以按顺序执行，也可以单独运行：

| 任务 | 说明 | 输出 |
|------|------|------|
| **任务一：生成投放计划** | 通过问答引导，收集用户业务信息，AI 生成完整投放策略文档 | `投放计划.md` |
| **任务二：生成导入文件** | 根据投放计划，生成 Google Ads Editor 可导入的 CSV 文件 | 5 个 CSV 文件 |

## 路由逻辑

收到用户请求后，先判断用户意图：

```
用户说了什么？
├── 已有完整投放计划 → 直接进入「任务二」
├── 只有产品/业务信息，没有投放计划 → 从「任务一」开始
├── "帮我制定投放计划" / "plan my campaign" → 「任务一」
├── "帮我生成导入文件" / "generate CSV" → 「任务二」（检查是否有计划）
└── 不确定 → 询问用户："你是需要我先帮你制定投放计划，还是已经有计划只需要生成导入文件？"
```

---

# 任务一：生成投放计划

## 目标

通过结构化问答，收集用户的业务信息和投放需求，由 AI 生成一份完整的 Google Ads 投放策略文档。

## 问答流程

**分轮询问，每轮不超过 3-5 个问题。** 不要一次性抛出所有问题。根据用户回答动态调整后续问题。

### 第一轮：业务基本面

必问：
1. **你的公司/品牌叫什么？主营什么产品或服务？**
2. **你的目标客户是谁？** （B2B 还是 B2C？什么行业？什么角色的人会搜索你？）
3. **你的核心竞争优势是什么？** （价格、品质、速度、定制能力、地理位置...列 2-3 个）

### 第二轮：投放目标与预算

必问：
4. **你的投放目标是什么？** （获取询盘/电话、网站流量、品牌曝光、App 下载...）
5. **每日预算大概多少？** （给出货币单位，如人民币/美元）
6. **这是试水还是已有经验？** （决定策略激进程度）

### 第三轮：市场与竞争

必问：
7. **你想投放哪些国家/地区？有没有要排除的？**
8. **你的落地页/网站 URL 是什么？** （没有也可以，后续可以补）

可选（根据上下文判断是否需要问）：
9. 你的产品关键词，客户通常会搜什么来找到你？
10. 你知道竞争对手在投什么词吗？
11. 你的网站上有 WhatsApp / 在线聊天 / 询盘表单吗？
12. 你有投放时段偏好吗？（如只在工作日）

### 第四轮：多语言与技术细节（如适用）

根据前面的回答动态决定是否需要问：

13. **你的网站支持哪些语言？** （判断是否需要多语言广告组和对应着陆页）
14. **目标国家买家主要用什么语言搜索？** （如印尼买家可能用印尼语搜索 `pemasok PVC`）
15. 产品的价格区间 / 单笔订单价值（判断出价策略和 ROI 预期）
16. 是否有线下展厅或可以验厂（决定是否增加地标词组）
17. 主要沟通方式（WhatsApp / Email / 电话）
18. 是否有产品认证（如 REACH、RoHS、ISO 等，影响文案和信任度）

## 网站结构分析（用户提供 URL 后自动执行）

当用户在问答中提供了网站 URL 后，**在生成计划之前**，必须先爬取和分析网站结构。这一步的目的是为计划和 CSV 文件中的着陆页 URL、Sitelink URL、Path 字段提供真实数据，而不是用占位符。

### 分析流程

1. **爬取首页**：使用 `defuddle` 或 `WebFetch` 获取首页内容，提取导航菜单结构
2. **爬取关键子页面**：根据导航菜单，重点访问以下类型的页面：
   - 产品/服务页面（Products、Services、Solutions）
   - 产品分类页（各品类入口）
   - 关于我们页面（About、Company）
   - 联系页面（Contact、Inquiry）
   - 如有多语言，访问各语言版本的对应页面
3. **记录 URL 清单**：整理出可用于广告投放的 URL 列表

### 需要提取的信息

| 信息 | 用途 | 示例 |
|------|------|------|
| **产品分类 URL** | Ad Group 对应的着陆页 | `/products/pvc-resin/`, `/products/pvc-pipe/` |
| **多语言 URL 结构** | 本地语言 Ad Group 的着陆页 | `/id/products/`, `/vi/products/` |
| **联系/询盘页 URL** | Sitelink Extension | `/contact/`, `/inquiry/` |
| **About/资质页 URL** | Sitelink Extension | `/about/`, `/certifications/` |
| **是否有 WhatsApp 按钮** | 决定是否设 Call Extension 和转化追踪 | 页面上的 `wa.me` 链接 |
| **是否有询盘表单** | 转化追踪设置 | Contact form、Quick Inquiry |
| **网站支持的语言** | 多语言策略 | EN / ID / VI / TH |
| **页面加载速度印象** | 着陆页优化建议 | 是否有大量未优化图片 |
| **产品/服务列表** | 关键词生成的依据 | 具体产品名、型号、应用领域 |

### 分析输出

将分析结果整理成一个 URL 映射表，后续直接嵌入计划和 CSV：

```markdown
### 网站 URL 映射（自动生成）

| 用途 | URL | 语言 | 备注 |
|------|-----|------|------|
| 主着陆页 | https://example.com/products/ | EN | 产品总览页 |
| PVC 原料着陆页 | https://example.com/products/pvc-resin/ | EN | Campaign 1 对应 |
| PVC 管材着陆页 | https://example.com/products/pvc-pipe/ | EN | Campaign 2 对应 |
| 印尼语产品页 | https://example.com/id/products/ | ID | 印尼语 Ad Group |
| 越南语产品页 | https://example.com/vi/products/ | VI | 越南语 Ad Group |
| 联系/询盘页 | https://example.com/contact/ | EN | Sitelink + 转化追踪 |
| 关于我们 | https://example.com/about/ | EN | Sitelink |
| 资质认证页 | https://example.com/certifications/ | EN | Sitelink |
| WhatsApp | wa.me/8613800138000 | — | Call Extension |
```

**重要规则：**
- 所有 URL 必须是从网站上实际找到的真实链接，**严禁编造不存在的路径**
- 如果某个期望的页面不存在（如没有独立的认证页），在备注中标注"不存在，建议创建"
- 如果网站没有多语言版本，在计划中如实说明并建议后续添加
- URL 映射表会被直接引用到：投放计划的着陆页章节、CSV 文件的 Final URL 列、Sitelink Extensions

## 计划生成规则

收集到足够信息后（问答完成 + 网站分析完成），AI 根据以下框架生成投放计划：

### 投放计划文档结构

**完整模板见** `templates/campaign_plan_template.md`，包含 11 个章节：

1. 执行摘要
2. 目标市场分析（含各国 CPC 预估、买家特征、语言）
3. 广告账户结构（Campaign 划分、国家级出价调整）
4. 关键词策略（核心词组 + 长尾词 + **本地语言关键词** + 否定词）
5. 广告文案（含 A/B 测试版本、Ad Extensions）
6. 网站分析与着陆页策略（含 **网站结构概览**、**URL 清单**、**Ad Group → 着陆页对应表**、**Sitelink URL 表**）
7. 转化跟踪设置（GTM 事件配置清单）
8. 预算分配与出价策略（含 **投放时段** 和 **设备出价调整**）
9. 投放时间表（按月规划：基建期 → 优化期 → 扩量期）
10. 核心 KPI 与预期效果
11. 上线前 Checklist

生成计划时，严格按照模板文件的章节和表格结构输出，确保每个章节都有实质内容。

### AI 生成时的专业规则

1. **关键词生成**：基于用户行业 + 产品自动生成，每组 6-10 个英文关键词。关键词要从买家搜索视角出发，不是卖家自嗨词。
2. **广告文案**：必须严格遵守字符限制（Headline ≤30 chars, Description ≤90 chars），生成时逐个验证。
3. **市场选择**：根据产品类型和预算合理推荐，低预算（<$30/天）建议集中 1-2 个市场。
4. **出价策略**：低预算推荐 Manual CPC；中高预算可推荐 Maximize Clicks 或 Target CPA。
5. **否定关键词**：必须包含通用否定词（retail, shop, amazon, job, pdf, free 等），再根据行业补充。
6. **广告组划分**：按搜索意图分组，不是按产品分组。典型分法：产品词、地标词、OEM/定制词、品牌词。
7. **多语言策略**：如网站支持多语言，必须为主力市场增加本地语言关键词 Ad Group，并在着陆页 URL 对应到相应语言版本（如 `/id/products/`）。
8. **Campaign 结构决策**：
   - 预算 <$1000/月：按产品线分 Campaign，国家用 Location Bid Adjustment 调控
   - 预算 $1000-5000/月：可按国家分 Campaign，产品线用 Ad Group 区分
   - 预算 >$5000/月：国家 × 产品线矩阵，每个组合独立 Campaign
9. **投放时段**：B2B 默认周一至周五当地时间 08:00-18:00。需说明各目标国与中国的时差。
10. **设备出价**：初始不调整，建议用户跑 2 周后根据转化数据调（移动端转化差则 -20%，桌面端好则 +15%）。
11. **着陆页对应**：每个 Ad Group 必须明确对应的着陆页 URL，不能所有组都落到首页。URL 必须来自网站分析步骤中确认存在的真实页面，严禁编造路径。
12. **Ad Extensions**：必须包含 Sitelink、Callout、Structured Snippets。如有 WhatsApp 则加 Call Extension。
13. **A/B 文案**：每个广告组至少准备 2 套文案版本进行 A/B 测试。
14. **预算分配表**：必须包含月预算、日预算、预估 CPC、预估月点击量的对应计算。

## 计划输出

生成的投放计划保存为 Markdown 文件：
- 路径：`~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/投放计划.md`
- 同时在对话中展示摘要，让用户确认或修改
- **用户确认后**，询问是否继续「任务二」生成导入文件

---

# 任务二：生成 Google Ads 导入文件（CSV）

## 前置检查

进入任务二前，必须确认以下信息已就绪。**缺一不可，缺少则提示用户补充：**

| 必需信息 | 来源 | 缺失时的提示 |
|----------|------|-------------|
| **Google Ads Customer ID** | 用户提供 | "请提供你的 Google Ads 客户 ID，格式如 `123-456-7890`。在 Google Ads 后台右上角可以找到。" |
| **投放计划** | 任务一输出 / 用户上传 | "我需要一份投放计划来生成文件。你可以：(1) 让我帮你制定一份（进入任务一）；(2) 直接提供你的投放计划文档。" |
| **落地页 URL** | 计划中 / 用户提供 | "请提供广告的落地页网址（用户点击广告后跳转的页面）。" |
| **广告系列名称** | 计划中 / 自动生成 | 可从品牌名+日期自动生成，如 "BrandName_Search_202603" |

## CSV 生成规则

所有 CSV 文件**严格遵循** Google Ads Editor 导入格式。生成前参考 `templates/` 目录下的官方模板确认列头。

### campaign.csv

**列头（必须完整，不可省略任何列）：**

```
Row Type,Action,Campaign status,Customer ID,Campaign,Campaign type,Networks,Budget,Delivery method,Budget type,Bid strategy type,Bid strategy,Campaign start date,Campaign end date,Language,Location,Exclusion,Devices,Label,Target CPA,Target ROAS,Display URL option,Website description,Target Impression Share,Max CPC Bid Limit for Target IS,Location Goal for Target IS,Tracking template,Final URL suffix,Custom parameter,Inventory type,Campaign subtype,Video ad formats,EU political ads
```

**逐字段规则：**

| 字段 | 值 | 说明 |
|------|-----|------|
| Row Type | `Campaign` | 固定值 |
| Action | `Add` | 新建用 Add |
| Campaign status | `Enabled` 或 `Paused` | 建议先 Paused 让用户检查后再启用 |
| Customer ID | `123-456-7890` | **必填**，用户提供 |
| Campaign | 广告系列名称 | 如 `SEA_PVCResin_Search_EN` |
| Campaign type | `Search` | 搜索广告 |
| Networks | `Google search` | **不要**加 Search partners 或 Display Network |
| Budget | `15.00` | 纯数字，日预算 |
| Delivery method | `Standard` | 固定值 |
| Budget type | `Daily` | 固定值 |
| Bid strategy type | `Manual CPC` | 低预算推荐。其他合法值：`Maximize clicks`, `Target CPA`, `Maximize Conversions` |
| Bid strategy | | 留空（非 Portfolio 策略时） |
| Campaign start date | `2026-04-01` | 格式 YYYY-MM-DD |
| Campaign end date | | 留空（试水期不设结束日期） |
| Language | `en; vi; id` | ISO 代码，分号分隔 |
| Location | 见下方国家名称表 | **必须使用 Google 认可的名称**，分号分隔 |
| Exclusion | 同 Location 格式 | 排除地区 |
| Devices | | **留空表示所有设备**。如需调整：`Computers:+10%; Mobile devices with full browsers:-20%; Tablets with full browsers:+0%`。**严禁写 "All devices"** |
| Label | | 留空或自定义标签 |
| Target CPA | | Manual CPC 时留空 |
| Target ROAS | | Manual CPC 时留空 |
| Display URL option | | 留空（非药品账户） |
| Website description | | 留空 |
| Target Impression Share | | 留空 |
| Max CPC Bid Limit for Target IS | | 留空 |
| Location Goal for Target IS | | 留空 |
| Tracking template | | 留空（除非用户提供） |
| Final URL suffix | | 留空（除非用户提供） |
| Custom parameter | | 留空 |
| Inventory type | | 留空（Search 类型不需要） |
| Campaign subtype | | 留空（Search 类型不需要） |
| Video ad formats | | 留空（Search 类型不需要） |
| **EU political ads** | **`No`** | **必填！Required on create。不填会导入失败** |

**Location 国家名称（必须使用 Google 认可名称）：**

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

带出价调整格式：`Indonesia : +20% ; Vietnam ; Thailand : -10%`

**Devices 字段关键规则：**
- **留空** = 所有设备，不做调整（最常用）
- **严禁**写 `All devices`、`all`、`All` 等非法值
- 如需调整，三种设备都要写全：`Computers:+0%; Mobile devices with full browsers:-20%; Tablets with full browsers:-20%`
- 设备名称必须是精确的英文：`Computers`、`Mobile devices with full browsers`、`Tablets with full browsers`

### ad_group.csv

```
Row Type,Action,Ad group status,Customer ID,Campaign,Ad group,Ad group type,Default max. CPC
```

**规则：**
- Row Type = `Ad group`
- Action = `Add`
- Ad group type = `Standard`
- Default max. CPC：数字如 `0.70`

### keyword.csv

```
Row Type,Action,Customer ID,Keyword status,Campaign,Ad group,Keyword,Type,Default max. CPC
```

**规则：**
- Row Type = `Keyword`
- Action = `Add`
- Type：`Phrase match` 或 `Exact match`（**严禁使用 Broad match 除非用户明确要求**）
- Keyword：纯文本，不加引号和括号（Google Ads 根据 Type 列应用匹配方式）

### negative_keyword.csv

```
Row Type,Action,Keyword status,Customer ID,Level,Campaign,Ad group,Negative keyword,Type
```

**规则：**
- Row Type = `Negative keyword`
- Action = `Add`
- Level：`Campaign`（全局否定）或 `Ad group`（组级否定）
- Type：通常用 `Phrase match`

### responsive_search_ad.csv

```
Row Type,Action,Ad status,Customer ID,Campaign,Ad group,Ad type,Headline 1,Headline 2,Headline 3,Headline 4,Headline 5,Headline 6,Headline 7,Headline 8,Headline 9,Headline 10,Headline 11,Headline 12,Headline 13,Headline 14,Headline 15,Description 1,Description 2,Description 3,Description 4,Headline 1 position,Headline 2 position,Headline 3 position,Headline 4 position,Headline 5 position,Headline 6 position,Headline 7 position,Headline 8 position,Headline 9 position,Headline 10 position,Headline 11 position,Headline 12 position,Headline 13 position,Headline 14 position,Headline 15 position,Description 1 position,Description 2 position,Description 3 position,Description 4 position,Path 1,Path 2,Final URL
```

**规则：**
- Row Type = `Ad`
- Action = `Add`
- Ad type = `Responsive search ad`
- **至少 5 个不重复的 Headline**（每个 ≤30 字符）
- **至少 2 个 Description**（每个 ≤90 字符）
- Headline position：`1`/`2`/`3` 固定位置，留空则自动轮播
- Path 1/2：展示 URL 路径，每段 ≤15 字符
- Final URL：落地页完整 URL

### 字符限制验证（生成时必须执行）

生成每条广告文案时，逐条检查：

```
Headline:     最多 30 个字符（含空格）  → 超出则截短或改写
Description:  最多 90 个字符（含空格）  → 超出则截短或改写
Path 1/2:     最多 15 个字符            → 超出则缩写
```

### CSV 生成前验证清单（每次必须逐项检查）

生成所有 CSV 后，在写入文件前执行以下验证：

1. **campaign.csv 列数检查**：必须有 34 列（与官方模板 `campaign_mcc_template.csv` 列头一致）。缺列会导致字段错位
2. **EU political ads**：必须填 `No`，不能留空（Required on create）
3. **Devices**：留空或使用精确格式，**严禁写 "All devices"**
4. **Location 国家名**：使用 Google 认可名称（Turkey → Turkiye），可查阅 `templates/campaign_mcc_template.csv` 的示例
5. **Delivery method**：填 `Standard`，不要留空
6. **Budget type**：填 `Daily`，不要留空
7. **CSV 值中含逗号**：如果某个字段值包含逗号，必须用双引号包裹该值（如 `"Indonesia ; Vietnam ; Thailand"`）
8. **空列不能省略**：所有列必须存在（用逗号占位），即使值为空。列数不一致会导致导入错误
9. **Campaign 名称一致性**：ad_group.csv / keyword.csv / responsive_search_ad.csv 中引用的 Campaign 名必须与 campaign.csv 完全一致（包括大小写和空格）
10. **Ad Group 名称一致性**：keyword.csv / responsive_search_ad.csv 中引用的 Ad Group 名必须与 ad_group.csv 完全一致

## 文件输出

### 输出目录

```
~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/
├── 投放计划.md              # 任务一输出（如果执行了任务一）
├── campaign.csv
├── ad_group.csv
├── keyword.csv
├── negative_keyword.csv
├── responsive_search_ad.csv
└── README_导入指南.txt       # 导入步骤说明
```

文件夹命名示例：`GoogleAds_BrandName_20260330`

### CSV 编码

所有 CSV 文件使用 **UTF-8** 编码。

## 导入指南（生成文件后展示给用户）

生成文件后，必须向用户展示以下操作指引：

---

### 如何导入 Google Ads

**方式 A：Google Ads Editor（推荐）**
1. 下载安装 Google Ads Editor
2. 登录你的 Google Ads 账户
3. 点击 **账户 > 导入 > 从文件导入**
4. 选择生成的 CSV 文件
5. 检查预览中的变更
6. 点击 **发布** 推送到账户

**方式 B：Google Ads 网页后台**
1. 登录 Google Ads
2. 进入 **工具与设置 > 批量操作 > 上传**
3. 点击 **+ 上传** 选择 CSV 文件
4. 预览并应用

**导入顺序（重要！）：**
1. `campaign.csv` — 先创建广告系列
2. `ad_group.csv` — 广告组属于广告系列
3. `keyword.csv` — 关键词属于广告组
4. `negative_keyword.csv` — 否定关键词（广告系列创建后即可导入）
5. `responsive_search_ad.csv` — 广告属于广告组

---

## 投放计划模板

生成投放计划时，严格按照 `templates/campaign_plan_template.md` 的章节结构和表格格式输出。

该模板包含完整的 11 个章节，涵盖从执行摘要到上线 Checklist 的全流程。相比简单的 8 章节计划，模板额外要求：

- **目标市场分析表**：每国列出核心需求行业、买家特征、主要语言、预估 CPC
- **广告账户结构表**：Campaign 划分、预算占比、国家级 Location Bid Adjustment
- **本地语言关键词组**：网站支持多语言时必须包含
- **A/B 测试文案**：每个广告组至少 2 套版本
- **着陆页 URL 对应表**：Ad Group → 着陆页的精确映射
- **投放时段和设备出价**：具体时间段和初始调整比例
- **转化跟踪配置清单**：GTM 事件列表
- **分月执行时间表**：基建期 → 优化期 → 扩量期的 Checklist

## 重要注意事项

- **Customer ID 是必需的**：每行 CSV 都需要 Google Ads 客户 ID。缺失时必须提示："请提供你的 Google Ads 客户 ID，格式如 `123-456-7890`，在 Google Ads 后台右上角可以找到。"
- **字符限制是硬性的**：生成时逐条验证，超限则改写，不要截断造成语义不通。
- **本 skill 不连接 Google Ads API**：仅生成离线导入文件，用户需手动上传。
- **两个任务可独立运行**：用户可以只要投放计划不要 CSV，也可以带着现有计划直接生成 CSV。
