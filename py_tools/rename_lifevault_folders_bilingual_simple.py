#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
rename_lifevault_folders_bilingual_v2.py

用途：
- 只重命名 LifeVault 的第一层和第二层目录
- 在原英文目录名前补一个中文说明
- 跳过 99_Archive 及其内部所有内容
- 跳过 .git / .obsidian 等隐藏或无关目录
- 已经是目标名字的目录会自动跳过
- 支持 dry-run 预览

用法（PowerShell）：
py .\rename_lifevault_folders_bilingual_v2.py --root "D:\LifeVault" --dry-run
py .\rename_lifevault_folders_bilingual_v2.py --root "D:\LifeVault"
"""

from pathlib import Path
import argparse
import sys


# =========================
# 配置区
# =========================

ROOT_SKIP_NAMES = {
    "99_Archive",
    ".git",
    ".obsidian",
    "__pycache__",
    "node_modules",
    ".vscode",
    ".idea",
}

# 第一层目录：原名 -> 新名
LEVEL1_MAP = {
    "00_Home": "00_总览主页_Home",
    "01_Career": "01_职业生涯_Career",
    "02_Projects": "02_项目实践_Projects",
    "03_Knowledge": "03_知识体系_Knowledge",
    "04_Learning": "04_学习成长_Learning",
    "05_Assets": "05_成果资产_Assets",
    "06_Life_and_Content": "06_生活内容_Life_and_Content",
    "07_GitHub_Labs": "07_GitHub实验室_GitHub_Labs",
}

# 第二层目录：原名 -> 新名
LEVEL2_MAP = {
    # 01_Career
    "职业规划": "职业规划_Career_Planning",
    "求职与跳槽": "求职跳槽_Job_Search",
    "面试准备": "面试准备_Interview_Prep",
    "英文表达": "英文表达_English",
    "简历": "简历_Resume",
    "薪资与机会判断": "机会判断_Offer_Decisions",

    # 你当前实际已有目录
    "Admin_Documents": "管理资料_Admin_Documents",
    "Interview": "面试资料_Interview",
    "Job_Search": "求职管理_Job_Search",
    "Resume": "简历管理_Resume",
    "Strategy": "职业策略_Strategy",

    # 02_Projects
    "Work": "工作项目_Work",
    "SideProjects": "个人项目_SideProjects",
    "AI_Demos": "AI演示_AI_Demos",
    "产品想法": "产品想法_Product_Ideas",
    "创业草稿": "创业草稿_Startups",
    "第三方API接入": "第三方API_Third_Party_APIs",

    # 03_Knowledge
    "00_Maps": "00_总地图_Maps",
    "01_ComputerScience": "01_计算机基础_ComputerScience",
    "02_Programming": "02_编程开发_Programming",
    "03_Architecture": "03_架构设计_Architecture",
    "04_Runtime_Infra": "04_运行时基础设施_Runtime_Infra",
    "05_Data": "05_数据技术_Data",
    "06_AI_Engineering": "06_AI工程_AI_Engineering",
    "07_Domain": "07_领域知识_Domain",
    "08_Tools": "08_工具体系_Tools",

    # 04_Learning
    "Plans": "计划_Plans",
    "Weekly": "每周学习_Weekly",
    "Monthly_Reviews": "月度复盘_Monthly_Reviews",
    "Reading_Notes": "阅读笔记_Reading_Notes",
    "Course_Notes": "课程笔记_Course_Notes",

    # 你当前实际已有目录
    "Weekly_Assets": "每周产出_Weekly_Assets",
    "Weekly_Plans": "每周计划_Weekly_Plans",

    # 05_Assets
    "Diagrams": "图表图解_Diagrams",
    "CheatSheets": "速查表_CheatSheets",
    "CaseStudies": "案例库_CaseStudies",
    "Interview_Templates": "面试模板_Interview_Templates",
    "English_Scripts": "英文脚本_English_Scripts",
    "Resume_Materials": "简历素材_Resume_Materials",
    "Publishable_Content": "可发布内容_Publishable_Content",
    "Demo_Documents": "演示文档_Demo_Documents",

    # 06_Life_and_Content
    "自媒体": "自媒体_Social_Content",
    "投资": "投资_Investing",
    "钓鱼": "钓鱼_Fishing",
    "羽毛球": "羽毛球_Badminton",
    "摄影": "摄影_Photography",
    "Vlog": "视频记录_Vlog",
    "写作素材": "写作素材_Writing_Materials",
    "个人思考": "个人思考_Personal_Reflections",
    "生活系统": "生活系统_Life_Systems",

    # 07_GitHub_Labs
    "Code_Projects": "代码项目_Code_Projects",
    "Scripts": "脚本_Scripts",
    "Templates": "模板_Templates",
    "Open_Source_Notes": "开源笔记_Open_Source_Notes",
}

# 为了支持“已经改过一级目录后再次运行”，这里建立“逻辑一级目录”的别名
LEVEL1_ALIASES = {
    "00_Home": ["00_Home", "00_总览主页_Home"],
    "01_Career": ["01_Career", "01_职业生涯_Career"],
    "02_Projects": ["02_Projects", "02_项目实践_Projects"],
    "03_Knowledge": ["03_Knowledge", "03_知识体系_Knowledge"],
    "04_Learning": ["04_Learning", "04_学习成长_Learning"],
    "05_Assets": ["05_Assets", "05_成果资产_Assets"],
    "06_Life_and_Content": ["06_Life_and_Content", "06_生活内容_Life_and_Content"],
    "07_GitHub_Labs": ["07_GitHub_Labs", "07_GitHub实验室_GitHub_Labs"],
}


# =========================
# 工具函数
# =========================

def is_hidden_or_skipped(path: Path) -> bool:
    return path.name in ROOT_SKIP_NAMES


def rename_one(path: Path, new_name: str, dry_run: bool):
    target = path.with_name(new_name)

    if path.name == new_name:
        return "skip", f"[SKIP] {path} (已经是目标名称)"

    if target.exists():
        return "conflict", f"[CONFLICT] {path}  ->  {target} (目标已存在)"

    if dry_run:
        return "dry-run", f"[DRY-RUN] {path}  ->  {target}"

    path.rename(target)
    return "ok", f"[OK] {path}  ->  {target}"


def resolve_level1_actual_paths(root: Path):
    """
    根据别名表，找到每个逻辑一级目录当前实际存在的路径。
    支持：
    - 原始英文名
    - 已经改过的双语名
    """
    result = {}

    for logical_name, candidates in LEVEL1_ALIASES.items():
        for name in candidates:
            p = root / name
            if p.exists() and p.is_dir():
                result[logical_name] = p
                break

    return result


# =========================
# 一级目录处理
# =========================

def process_level1(root: Path, dry_run: bool, verbose_skip: bool = False):
    logs = []
    stats = {
        "ok": 0,
        "dry-run": 0,
        "skip": 0,
        "conflict": 0,
    }

    for child in sorted(root.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue

        if is_hidden_or_skipped(child):
            if verbose_skip:
                if child.name == "99_Archive":
                    logs.append(f"[SKIP] {child} (按要求跳过 99_Archive)")
                else:
                    logs.append(f"[SKIP] {child} (隐藏或系统目录)")
            continue

        new_name = LEVEL1_MAP.get(child.name)
        if not new_name:
            # 已经是双语目录的也不报噪音
            if child.name not in LEVEL1_MAP.values():
                if verbose_skip:
                    logs.append(f"[SKIP] {child} (一级目录未配置映射)")
            continue

        status, msg = rename_one(child, new_name, dry_run)
        logs.append(msg)
        stats[status] += 1

    return logs, stats


# =========================
# 二级目录处理
# =========================

def process_level2(root: Path, dry_run: bool, verbose_skip: bool = False):
    logs = []
    stats = {
        "ok": 0,
        "dry-run": 0,
        "skip": 0,
        "conflict": 0,
    }

    level1_paths = resolve_level1_actual_paths(root)

    for logical_name, level1_path in sorted(level1_paths.items(), key=lambda x: x[0]):
        if level1_path.name == "99_Archive":
            continue

        for child in sorted(level1_path.iterdir(), key=lambda p: p.name):
            if not child.is_dir():
                continue

            if is_hidden_or_skipped(child):
                continue

            new_name = LEVEL2_MAP.get(child.name)
            if not new_name:
                # 已经是双语名就静默跳过
                if child.name not in LEVEL2_MAP.values():
                    if verbose_skip:
                        logs.append(f"[SKIP] {child} (二级目录未配置映射)")
                continue

            status, msg = rename_one(child, new_name, dry_run)
            logs.append(msg)
            stats[status] += 1

    return logs, stats


# =========================
# 主程序
# =========================

def main():
    parser = argparse.ArgumentParser(
        description="Rename LifeVault level-1 and level-2 folders into bilingual names."
    )
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help=r'LifeVault 根目录，例如：D:\LifeVault'
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只预览，不实际执行"
    )
    parser.add_argument(
        "--verbose-skip",
        action="store_true",
        help="显示跳过项（默认关闭，避免输出太吵）"
    )

    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()

    if not root.exists():
        print(f"❌ 根目录不存在：{root}")
        return 1

    if not root.is_dir():
        print(f"❌ 提供的路径不是目录：{root}")
        return 1

    print(f"📂 LifeVault 根目录：{root}")
    print("规则：只处理第一层和第二层，跳过 99_Archive")
    print()

    level1_logs, level1_stats = process_level1(root, args.dry_run, args.verbose_skip)
    level2_logs, level2_stats = process_level2(root, args.dry_run, args.verbose_skip)

    all_logs = level1_logs + level2_logs
    for line in all_logs:
        print(line)

    total_ok = level1_stats["ok"] + level2_stats["ok"]
    total_dry = level1_stats["dry-run"] + level2_stats["dry-run"]
    total_skip = level1_stats["skip"] + level2_stats["skip"]
    total_conflict = level1_stats["conflict"] + level2_stats["conflict"]

    print()
    print("统计：")
    if args.dry_run:
        print(f"  预览将改名：{total_dry}")
    else:
        print(f"  实际改名成功：{total_ok}")
    print(f"  冲突数量：{total_conflict}")

    if args.dry_run:
        print()
        print("🟡 当前为 dry-run，仅预览，不实际修改。")
    else:
        print()
        print("🎉 处理完成。")

    return 0 if total_conflict == 0 else 2


if __name__ == "__main__":
    sys.exit(main())