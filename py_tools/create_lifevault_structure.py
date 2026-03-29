#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
create_lifevault_structure.py

用途：
1. 在 Windows / macOS / Linux 本地创建一个长期可用的个人知识与职业资产总仓库
2. 同时预留：
   - 学习计划 / 周学习 / 月复盘
   - 长期知识库
   - 工作项目 / side project / AI demo
   - 简历 / 英文 / 面试模板 / 图 / 故障案例
   - 自媒体 / 投资 / 钓鱼 / 羽毛球 / 摄影 / AI 作图作视频 / ComfyUI
   - GitHub 代码与脚本仓库工作区

用法（Windows PowerShell 示例）：
python .\create_lifevault_structure.py
python .\create_lifevault_structure.py --root "D:\Wilson\LifeVault"
python .\create_lifevault_structure.py --root "D:\LifeVault" --with-readme
"""

from pathlib import Path
import argparse

DEFAULT_ROOT_NAME = "LifeVault"

DIRECTORY_TREE = {
    "00_Home": {
        "_files": [
            "00_总导航.md",
            "01_人生路线图.md",
            "02_五年计划.md",
            "03_年度计划.md",
            "04_当前重点.md",
        ]
    },
    "01_Career": {
        "职业规划": {},
        "求职与跳槽": {},
        "面试准备": {},
        "英文表达": {},
        "简历": {},
        "薪资与机会判断": {},
    },
    "02_Projects": {
        "Work": {
            "HSBC": {},
            "BEA": {},
            "Other_Projects": {},
        },
        "SideProjects": {},
        "AI_Demos": {},
        "产品想法": {},
        "创业草稿": {},
        "第三方API接入": {
            "微信支付": {},
            "支付类API": {},
            "地图与短信邮件API": {},
            "认证与登录API": {},
            "其他第三方API": {},
        },
    },
    "03_Knowledge": {
        "00_Maps": {
            "_files": [
                "技术总地图.md",
                "后端路线图.md",
                "云与运行时路线图.md",
                "AI工程化路线图.md",
                "金融科技路线图.md",
            ]
        },
        "01_ComputerScience": {
            "数据结构与算法": {},
            "操作系统": {},
            "计算机网络": {},
            "数据库基础": {},
            "编译与原理": {},
        },
        "02_Programming": {
            "Java": {
                "基础语法": {},
                "集合": {},
                "泛型": {},
                "注解与反射": {},
                "IO_NIO": {},
                "JUC_并发": {},
                "Lombok": {},
                "规则与编码规范": {},
            },
            "JVM": {
                "类加载": {},
                "内存模型": {},
                "GC": {},
                "调优": {},
                "故障排查": {},
            },
            "Spring": {
                "Spring_Core": {},
                "Spring_Boot": {},
                "Spring_MVC": {},
                "Spring_AOP": {},
                "Spring_Transaction": {},
                "Spring_Security": {},
                "Spring_Cloud": {},
            },
            "ORM": {
                "JPA_Hibernate": {},
                "MyBatis": {},
            },
            "设计模式": {},
            "重构与代码质量": {},
        },
        "03_Architecture": {
            "系统设计": {},
            "分布式系统": {},
            "微服务": {},
            "缓存": {},
            "消息队列": {},
            "API设计": {},
            "高可用与容灾": {},
            "技术方案": {},
        },
        "04_Runtime_Infra": {
            "Linux": {},
            "Nginx": {},
            "Docker": {},
            "Kubernetes": {},
            "CI_CD": {
                "Git": {},
                "Maven": {},
                "Jenkins": {},
                "SVN": {},
            },
            "Gateway_LoadBalancer_Ingress": {},
            "DNS_Route_NAT": {},
            "TLS_mTLS_Certificates": {},
            "Cloud_AWS": {},
            "Cloud_AliCloud": {},
            "Observability": {},
            "Server_运行环境": {},
            "Services_服务治理": {},
        },
        "05_Data": {
            "MySQL": {},
            "Redis": {},
            "搜索与索引": {},
            "数据建模": {},
            "数据一致性": {},
        },
        "06_AI_Engineering": {
            "LLM_API": {},
            "Prompting": {},
            "Structured_Output": {},
            "Tool_Calling": {},
            "RAG": {},
            "Workflow_Agent": {},
            "AI_Deployment": {},
            "AI_Observability": {},
            "AI_Security": {},
            "AI_Cost_Control": {},
            "ComfyUI": {},
            "AI_作图": {},
            "AI_作视频": {},
            "AI_脚本与工作流": {},
        },
        "07_Domain": {
            "Banking": {},
            "Payment": {},
            "Risk_Control": {},
            "Enterprise_Systems": {},
            "业务术语": {},
        },
        "08_Tools": {
            "Git": {},
            "Maven": {},
            "JMeter": {},
            "IDE": {},
            "Obsidian_Excalidraw": {},
            "常用效率工具": {},
        },
    },
    "04_Learning": {
        "Plans": {},
        "Weekly": {},
        "Monthly_Reviews": {},
        "Reading_Notes": {},
        "Course_Notes": {},
    },
    "05_Assets": {
        "Diagrams": {
            "Cloud": {},
            "TLS": {},
            "Kubernetes": {},
            "Observability": {},
            "AI": {},
        },
        "CheatSheets": {},
        "CaseStudies": {
            "故障案例": {},
            "发布案例": {},
            "面试题案例": {},
            "工作真实案例": {},
        },
        "Interview_Templates": {},
        "English_Scripts": {},
        "Resume_Materials": {},
        "Publishable_Content": {},
        "Demo_Documents": {},
    },
    "06_Life_and_Content": {
        "自媒体": {
            "选题池": {},
            "脚本草稿": {},
            "发布复盘": {},
            "账号策略": {},
        },
        "投资": {
            "基础认知": {},
            "策略研究": {},
            "复盘": {},
            "观察清单": {},
        },
        "钓鱼": {
            "装备": {},
            "钓点": {},
            "技巧": {},
            "出钓记录": {},
        },
        "羽毛球": {
            "技术动作": {},
            "训练计划": {},
            "装备": {},
            "对局复盘": {},
        },
        "摄影": {
            "器材": {},
            "构图": {},
            "后期": {},
            "作品集": {},
        },
        "Vlog": {},
        "写作素材": {},
        "个人思考": {},
        "生活系统": {},
    },
    "07_GitHub_Labs": {
        "Code_Projects": {
            "Java_Backend": {},
            "AI_Demos": {},
            "Workflow_Agents": {},
            "Utilities": {},
        },
        "Scripts": {
            "Python": {},
            "Shell": {},
            "Windows_Batch": {},
            "Automation": {},
            "AI_Video_Scripts": {},
        },
        "Templates": {
            "Project_Templates": {},
            "README_Templates": {},
            "Prompt_Templates": {},
        },
        "Open_Source_Notes": {},
    },
    "99_Archive": {
        "Old_Notes": {},
        "Deprecated": {},
        "Temp": {},
    },
}

HOME_README = """# LifeVault

这是一个长期使用的个人知识、职业、项目、内容与资产总仓库。

## 一级目录说明
- 00_Home：总导航、长期路线、年度重点
- 01_Career：职业、求职、英文、简历、薪资判断
- 02_Projects：工作项目、side project、AI demo、第三方 API 接入
- 03_Knowledge：长期知识库
- 04_Learning：周学习、月复盘、课程笔记、计划
- 05_Assets：图、案例、面试模板、可发布内容
- 06_Life_and_Content：自媒体、投资、钓鱼、羽毛球、摄影、Vlog、个人思考
- 07_GitHub_Labs：准备同步到 GitHub 的代码、脚本、模板和实验项目
- 99_Archive：旧资料和临时内容
"""

GENERIC_README_TEMPLATE = """# {name}

## 用途
- 

## 建议放什么
- 

## 相关内容
- 
"""

def safe_write_text(file_path: Path, content: str) -> None:
    if not file_path.exists():
        file_path.write_text(content, encoding="utf-8")

def create_tree(base: Path, tree: dict, with_readme: bool = False) -> None:
    for name, value in tree.items():
        current = base / name
        current.mkdir(parents=True, exist_ok=True)

        if with_readme:
            readme_path = current / "README.md"
            if not readme_path.exists():
                safe_write_text(readme_path, GENERIC_README_TEMPLATE.format(name=name))

        if isinstance(value, dict):
            files = value.get("_files", [])
            for f in files:
                safe_write_text(current / f, f"# {Path(f).stem}\n")

            sub_items = {k: v for k, v in value.items() if k != "_files"}
            if sub_items:
                create_tree(current, sub_items, with_readme=with_readme)

def main() -> int:
    parser = argparse.ArgumentParser(description="Create a long-term LifeVault directory structure.")
    parser.add_argument("--root", type=str, default=DEFAULT_ROOT_NAME,
                        help='Root directory path, e.g. D:\\LifeVault')
    parser.add_argument("--with-readme", action="store_true",
                        help="Create README.md for main folders")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    create_tree(root, DIRECTORY_TREE, with_readme=args.with_readme)

    safe_write_text(root / "README.md", HOME_README)
    safe_write_text(root / "00_Home" / "00_总导航.md", "# 总导航\n")
    safe_write_text(root / "04_Learning" / "Plans" / "README.md", "# Plans\n")
    safe_write_text(root / "04_Learning" / "Weekly" / "README.md", "# Weekly\n")
    safe_write_text(root / "05_Assets" / "CaseStudies" / "README.md", "# CaseStudies\n")
    safe_write_text(root / "07_GitHub_Labs" / "README.md",
                    "# GitHub Labs\n\n这里放适合独立同步到 GitHub 的代码、脚本、模板和实验项目。\n")

    print(f"✅ 已创建目录结构：{root}")
    print()
    print("建议下一步：")
    print("1. 把旧资料先整包迁进去，不要一开始就细拆")
    print("2. 以后 Weekly 放过程，Knowledge 放最终版")
    print("3. 可复用代码/脚本优先放到 07_GitHub_Labs")
    print("4. 第一次使用时，可以先打开 00_Home/00_总导航.md")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
