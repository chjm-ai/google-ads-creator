#!/usr/bin/env python3
"""
Google Ads Editor 导入 CSV 校验器（确定性校验，不靠模型逐字段比对）。

校验内容：
  1. 列头是否与官方模板一致（顺序 + 名称），列数是否正确
  2. RSA 文案字符限制：Headline ≤30、Description ≤90、Path ≤15
  3. 设备字段禁用项：严禁 "All devices"
  4. 匹配类型禁用项：严禁 Broad match（除非 --allow-broad）
  5. EU political ads 必填（campaign 必须为 No，不可留空）
  6. 每行列数与表头一致（防止字段错位）

用法：
  python validate_csv.py campaign.csv
  python validate_csv.py ~/Desktop/GoogleAds_Brand_20260613/   # 校验整个目录
  python validate_csv.py campaign.csv --type campaign          # 显式指定类型
  python validate_csv.py keyword.csv --allow-broad             # 用户明确要 Broad 时放行

退出码：所有文件 PASS -> 0；任一 FAIL -> 1。
表头以同 skill 的 templates/*_mcc_template.csv 为权威来源，模板更新校验器自动跟随。
"""
import argparse
import csv
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"

# 文件类型 -> 官方模板文件名
TEMPLATE_MAP = {
    "campaign": "campaign_mcc_template.csv",
    "ad_group": "ad_group_mcc_template.csv",
    "keyword": "keyword_mcc_template.csv",
    "negative_keyword": "ad_group_negative_keyword_mcc_template.csv",
    "responsive_search_ad": "responsive_search_ad_mcc_template.csv",
}

# 文件名关键词 -> 类型（用于自动识别）
FILENAME_HINTS = [
    ("responsive_search_ad", "responsive_search_ad"),
    ("rsa", "responsive_search_ad"),
    ("negative", "negative_keyword"),
    ("ad_group", "ad_group"),
    ("adgroup", "ad_group"),
    ("keyword", "keyword"),
    ("campaign", "campaign"),
]

CHAR_LIMITS_RSA = {
    "Headline": 30,
    "Description": 90,
    "Path": 15,
}


def detect_type(path: Path) -> str | None:
    name = path.name.lower()
    for hint, t in FILENAME_HINTS:
        if hint in name:
            return t
    return None


def read_rows(path: Path):
    """读取 CSV，跳过以 # 开头的注释行（Editor 模板含注释/说明行）。返回 (header, data_rows)。"""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    header = None
    data = []
    for r in rows:
        if not r or all(c.strip() == "" for c in r):
            continue
        first = r[0].strip()
        if header is None:
            if first.startswith("#"):
                continue  # 模板顶部说明行
            header = r
            continue
        if first.startswith("#"):
            continue  # 字段说明行
        data.append(r)
    return header, data


def template_header(file_type: str):
    tpl = TEMPLATES_DIR / TEMPLATE_MAP[file_type]
    if not tpl.exists():
        return None
    h, _ = read_rows(tpl)
    return h


def validate_file(path: Path, forced_type: str | None, allow_broad: bool):
    violations = []
    file_type = forced_type or detect_type(path)
    if file_type is None:
        return ("SKIP", file_type, ["无法识别文件类型，请用 --type 指定（campaign/ad_group/keyword/negative_keyword/responsive_search_ad）"])

    header, data = read_rows(path)
    if header is None:
        return ("FAIL", file_type, ["文件没有有效表头行"])

    # 1. 表头校验
    expected = template_header(file_type)
    if expected is None:
        violations.append(f"找不到模板 {TEMPLATE_MAP[file_type]}，无法校验表头")
    else:
        if len(header) != len(expected):
            violations.append(f"列数不符：实际 {len(header)} 列，官方模板 {len(expected)} 列")
        if header != expected:
            # 给出具体差异
            for i, exp in enumerate(expected):
                act = header[i] if i < len(header) else "<缺失>"
                if act != exp:
                    violations.append(f"第 {i+1} 列应为 '{exp}'，实际为 '{act}'")
            extra = header[len(expected):]
            if extra:
                violations.append(f"多出列：{extra}")

    ncols = len(header)
    col_index = {name: i for i, name in enumerate(header)}

    # 2. 逐行校验
    for ln, row in enumerate(data, start=1):
        if len(row) != ncols:
            violations.append(f"数据行 {ln}：列数 {len(row)} 与表头 {ncols} 不一致（字段会错位）")
            continue

        def cell(colname):
            idx = col_index.get(colname)
            return row[idx].strip() if idx is not None and idx < len(row) else ""

        # 2a. RSA 字符限制（只看内容列 "Headline N"/"Description N"/"Path N"，跳过 position 列）
        if file_type == "responsive_search_ad":
            for col, idx in col_index.items():
                if "position" in col.lower():
                    continue
                val = row[idx].strip() if idx < len(row) else ""
                if not val:
                    continue
                parts = col.rsplit(" ", 1)
                base = parts[0]
                if len(parts) == 2 and parts[1].isdigit() and base in CHAR_LIMITS_RSA:
                    limit = CHAR_LIMITS_RSA[base]
                    if len(val) > limit:
                        violations.append(f"数据行 {ln}：{col}='{val}' 超出 {limit} 字符（实际 {len(val)}）")

        # 2b. 设备禁用项（campaign 的 Devices 列）
        if file_type == "campaign":
            dev = cell("Devices")
            if dev and dev.lower().replace(" ", "") in ("alldevices", "all"):
                violations.append(f"数据行 {ln}：Devices='{dev}' 非法。留空=所有设备，调整须写全三种设备出价")
            # 2d. EU political ads 必填
            eu = cell("EU political ads")
            rowtype = cell("Row Type").lower()
            if rowtype == "campaign" and eu == "":
                violations.append(f"数据行 {ln}：EU political ads 留空（Required on create，须填 No）")

        # 2c. 匹配类型禁用项
        if file_type in ("keyword", "negative_keyword"):
            mt = cell("Type")
            if mt and "broad" in mt.lower() and not allow_broad:
                violations.append(f"数据行 {ln}：Type='{mt}' 使用了 Broad match（严禁，除非用户明确要求；放行用 --allow-broad）")

    status = "PASS" if not violations else "FAIL"
    return (status, file_type, violations)


def main():
    ap = argparse.ArgumentParser(description="Google Ads Editor 导入 CSV 校验器")
    ap.add_argument("path", help="CSV 文件或包含 CSV 的目录")
    ap.add_argument("--type", choices=list(TEMPLATE_MAP.keys()), help="显式指定文件类型")
    ap.add_argument("--allow-broad", action="store_true", help="放行 Broad match（用户明确要求时）")
    args = ap.parse_args()

    target = Path(args.path).expanduser()
    if not target.exists():
        print(f"路径不存在: {target}")
        sys.exit(2)

    files = []
    if target.is_dir():
        files = sorted(p for p in target.glob("*.csv") if not p.name.endswith("_template.csv"))
        if not files:
            print(f"目录中没有 CSV 文件: {target}")
            sys.exit(2)
    else:
        files = [target]

    any_fail = False
    for f in files:
        status, ftype, violations = validate_file(f, args.type, args.allow_broad)
        tag = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]"}[status]
        print(f"{tag} {f.name}  (类型: {ftype})")
        for v in violations:
            print(f"       - {v}")
        if status == "FAIL":
            any_fail = True
    print("-" * 50)
    print("结果：FAIL" if any_fail else "结果：全部 PASS")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
