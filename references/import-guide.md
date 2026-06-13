# 导入指南（生成 CSV 后展示给用户）

生成全部 CSV 并通过 `scripts/validate_csv.py` 校验后，把以下操作指引展示给用户。

## 如何导入 Google Ads

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

## 导入顺序（重要！必须按此顺序）

层级依赖决定顺序，乱序会因父对象不存在而报错：

1. `campaign.csv` — 先创建广告系列
2. `ad_group.csv` — 广告组属于广告系列
3. `keyword.csv` — 关键词属于广告组
4. `negative_keyword.csv` — 否定关键词（广告系列创建后即可导入）
5. `responsive_search_ad.csv` — 广告属于广告组

## 输出目录结构

```
~/Desktop/GoogleAds_[品牌名]_YYYYMMDD/
├── 投放计划.md              # 任务一输出（如执行了任务一）
├── campaign.csv
├── ad_group.csv
├── keyword.csv
├── negative_keyword.csv
├── responsive_search_ad.csv
└── README_导入指南.txt       # 把本文件内容写入，随 CSV 一起交付
```

所有 CSV 一律 **UTF-8** 编码。
