# 任务三：生成「更新现有广告」的 CSV

## 适用场景
用户已在 Google Ads 建好 Campaign/Ad Group/Keyword/Ad，只想更新：预算/状态/出价、Final URL/Tracking Template/Labels、关键词出价或暂停、或基于现有广告改文案再上传。这类都走任务三，不要重复生成任务二的新建 CSV。

## 核心原则
**更新必须基于 Google Ads / Google Ads Editor 导出的现有数据修改。**
原因：更新需要 `Campaign ID`/`Ad group ID`/`Ad ID`/`Keyword ID` 或 `#Original` 列——用户编不出、也不该猜。直接拿新建模板改内容上传，系统会识别成"新建"或因缺 ID 报错。

## 前置检查
| 必需信息 | 来源 | 缺失提示 |
|----------|------|---------|
| Google Ads 导出文件 | 用户从网页版或 Editor 导出 | "更新现有广告需要你先从 Google Ads 或 Editor 导出当前数据再发我。不能拿首次创建模板更新。" |
| 更新目标 | 用户说明 | "你要更新什么：预算、出价、关键词、文案、URL、状态？" |
| 作用范围 | 用户说明 / 导出文件识别 | "更新全部 Campaign 还是只某几个国家/广告组/关键词？" |

## 提示用户如何导出
**网页版**：打开 Google Ads → 进入要更新的对象页面 → 右上角下载图标 → "更多选项" → 勾选"用于批量上传的可修改列" → 下载 CSV/Excel
**Editor**：打开并同步账户 → 进入对象视图 → 导出当前视图到 CSV → 尽量保留 `#Original` 列便于精准匹配

提示语模板：
> 你这是"更新现有广告"，不是"首次创建"。请先从 Google Ads 网页版导出带"用于批量上传的可修改列"的文件，或从 Editor 导出当前数据；拿到导出文件我再生成更新版 CSV。否则直接改创建模板重新上传大概率报错或被识别成新建。

## 生成规则
1. **保留原始标识列**：不删 `Campaign ID`/`Ad group ID`/`Ad ID`/`Keyword ID`/`#Original`
2. **只改用户要求更新的字段**，其余保持原值
3. **不要把更新误改成新建**：导出行已有 ID 时不要把 Action 改成 `Add`，需要时按原文件语义用 `Edit`
4. **文案更新要谨慎**：改 RSA 文案优先基于 Editor 导出的广告文件处理，不要用任务二新建 CSV 去"覆盖更新"
5. **命名**：`campaign_update.csv` / `keyword_update.csv` / `responsive_search_ad_update.csv`，或原名加 `_update`

## 输出目录
```
~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/
├── campaign_update.csv
├── ad_group_update.csv
├── keyword_update.csv
├── negative_keyword_update.csv
├── responsive_search_ad_update.csv
└── README_更新说明.txt
```

## README_更新说明.txt 必须包含
- 这是"更新现有广告"用，不是"首次创建"用
- 本次修改了哪些字段
- 基于哪份官方导出数据改写
- 建议先在 Editor 预览变更再发布
- 如需回滚，可重新导出当前线上数据作为备份
