# Google Ads Creator

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that helps you plan Google Ads campaigns and generate import-ready CSV files — no Google Ads expertise required.

## What It Does

| Task | Description | Output |
|------|-------------|--------|
| **Task 1: Campaign Planning** | Interactive Q&A collects your business info → AI generates a complete ad strategy with keywords, ad copy, budget allocation, and KPIs | `投放计划.md` |
| **Task 2: CSV Generation** | Converts a campaign plan into Google Ads Editor-compatible CSV files, ready to import | 5 CSV files |

Both tasks run independently or sequentially. Missing a plan? Task 1 builds one. Already have a plan? Jump straight to Task 2.

## How It Works

```
You: "帮我做谷歌广告投放"

Claude: asks 3-5 questions about your business
        ↓
Claude: asks about budget, markets, goals
        ↓
Claude: crawls your website to find real landing page URLs
        ↓
Claude: generates a full campaign plan (you review & approve)
        ↓
Claude: generates 5 CSV files → ~/Desktop/GoogleAds_YourBrand_20260401/
        ↓
Claude: shows you how to import into Google Ads Editor
```

## Features

- **Smart Q&A Flow** — Asks questions in rounds (3-5 per round), not all at once
- **Website Analysis** — Crawls your site to find real product pages, contact forms, WhatsApp links, and multi-language URLs — no placeholder URLs in your ads
- **Multi-language Support** — Detects site languages and creates local-language keyword groups with matching landing pages
- **Strict CSV Validation** — Enforces Google Ads Editor format: correct column count, EU political ads field, device naming, country name spelling (Turkey → Turkiye), character limits
- **Budget-aware Strategy** — Recommends campaign structure based on your budget level (<$1K / $1-5K / >$5K per month)
- **Missing Info Prompts** — Won't generate broken files; prompts for Customer ID, landing page URL, etc.

## Generated Files

```
~/Desktop/GoogleAds_BrandName_20260401/
├── 投放计划.md              # Campaign strategy document
├── campaign.csv             # Campaign settings, budget, targeting
├── ad_group.csv             # Ad group definitions and bids
├── keyword.csv              # Keywords with match types
├── negative_keyword.csv     # Negative keywords
├── responsive_search_ad.csv # Responsive Search Ads (headlines + descriptions)
└── README_导入指南.txt       # Import instructions
```

All CSVs follow the official Google Ads Editor import format and can be imported via:
- **Google Ads Editor** → Account → Import → From file
- **Google Ads Web** → Tools & Settings → Bulk Actions → Uploads

## Usage

Tell Claude what you need:

```
"帮我制定 Google Ads 投放计划"          → Task 1 only
"帮我生成 Google Ads 导入文件"          → Task 2 only
"create a google ads campaign"          → Both tasks
"I have a plan, generate the CSV files" → Task 2 with your existing plan
```

## Installation

### Option A: Clone and symlink (recommended)

```bash
git clone https://github.com/chjm-ai/google-ads-creator.git ~/Desktop/Repos/google-ads-creator
ln -s ~/Desktop/Repos/google-ads-creator ~/.claude/skills/google-ads-creator
```

### Option B: Copy directly

```bash
git clone https://github.com/chjm-ai/google-ads-creator.git
cp -r google-ads-creator ~/.claude/skills/
```

## Templates

The `templates/` directory contains:

| File | Purpose |
|------|---------|
| `campaign_plan_template.md` | 11-section campaign plan template (used by Task 1) |
| `campaign_mcc_template.csv` | Official Google Ads campaign CSV format |
| `ad_group_mcc_template.csv` | Official Google Ads ad group CSV format |
| `keyword_mcc_template.csv` | Official Google Ads keyword CSV format |
| `ad_group_negative_keyword_mcc_template.csv` | Official Google Ads negative keyword CSV format |
| `responsive_search_ad_mcc_template.csv` | Official Google Ads RSA CSV format |

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI or IDE extension
- A Google Ads account (for the Customer ID and importing files)
- No API keys or additional dependencies needed

## License

MIT
