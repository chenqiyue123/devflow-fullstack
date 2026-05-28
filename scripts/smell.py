#!/usr/bin/env python3
"""
DevFlow - Code Smell Detector
Usage: python smell.py --file foo.py
       python smell.py --dir src/
"""

import argparse, os, re
from pathlib import Path
from collections import defaultdict

SMELLS = [
    # ─── Bloaters (臃肿) ───
    ("long_method", r"", lambda lines, f: sum(1 for l in lines if l.strip() and not l.strip().startswith(("//","#","/*","*"))) > 80,
     "函数过长 (>80行) -> 拆分为多个小函数"),
    ("long_param", r"(?:def|function|func|public|private)\s+\w+\s*\(([^)]+)\)",
     lambda m: m and len([p for p in m.group(1).split(",") if p.strip()]) > 5,
     "参数过多 -> 用对象/struct 封装"),
    ("long_file", r"", lambda lines, f: len(lines) > 400,
     "文件过大 (>400行) -> 拆分模块"),

    # ─── OOP Abusers (面向对象滥用) ───
    ("switch_statement", r"switch\s*\(|if\s+.*==.*else\s+if\s+.*==.*else\s+if",
     lambda m: True, "类型判断过多 -> 考虑用多态/策略模式"),
    ("refused_bequest", r"extends\s+\w+.*\n.*@Override.*throw new UnsupportedOperationException",
     lambda m: True, "子类拒绝父类方法 -> 组合优于继承"),

    # ─── Change Preventers (牵一发动全身) ───
    ("shotgun_surgery", r"", lambda lines, f: False,  # needs cross-file analysis
     "散弹式修改 -> 相关逻辑散落多文件，需集中"),
    ("divergent_change", r"", lambda lines, f: False,
     "发散式变更 -> 一个类承担多种职责"),

    # ─── Dispensables (冗余) ───
    ("dead_code", r"//\s*TODO.*\d{4}|//\s*FIXME.*\d{4}",
     lambda m: True, "过期 TODO/FIXME -> 清理或跟进"),
    ("magic_number", r"[^a-zA-Z\d](\d{2,})[^a-zA-Z\d]",
     lambda m: m and not m.group(1).startswith(("200","201","400","401","403","404","500")),
     "魔法数字 -> 提取为命名常量"),
    ("duplicate_code", r"", lambda lines, f: False,
     "疑似重复代码 -> 用 IDE 检测或手动审查"),
    ("lazy_class", r"class\s+\w+\s*\{?\s*$",
     lambda lines, f: sum(1 for l in lines if l.strip() and not l.strip().startswith(("//","/*","*","#"))) < 10,
     "过小的类 (<10行有效代码) -> 合并到相关类"),

    # ─── Couplers (耦合) ───
    ("feature_envy", r"(\w+)\.\w+\.\w+\.\w+",
     lambda m: True, "过度链式调用 -> 违反迪米特法则"),
    ("inappropriate_intimacy", r"import\s+\w+\.\*|from\s+\w+\s+import\s+\*",
     lambda m: True, "通配符导入 -> 明确导入所需"),

    # ─── Naming (命名) ───
    ("bad_name", r"\b(a|b|c|d|e|foo|bar|baz|x|y|z|tmp|temp|var|val)\b",
     lambda m: m and len(m.group(1)) <= 2,
     "单字母/无意义变量名 -> 用描述性名称"),
]

def analyze_file(filepath):
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        results = []

        for smell_name, pattern, condition, advice in SMELLS:
            if pattern:
                for i, line in enumerate(lines, 1):
                    m = re.search(pattern, line)
                    if m and condition(m):
                        results.append(f"[{smell_name}] {filepath}:{i} - {advice}")
                        if smell_name in ("switch_statement", "feature_envy", "inappropriate_intimacy"):
                            break  # one per file is enough
            else:
                if condition(lines, filepath):
                    results.append(f"[{smell_name}] {filepath} - {advice}")

        return results
    except Exception:
        return []

def main():
    parser = argparse.ArgumentParser(description="Code Smell Detector")
    parser.add_argument("--file")
    parser.add_argument("--dir", default=".")
    args = parser.parse_args()

    exts = {".py",".js",".ts",".tsx",".jsx",".java",".go"}
    ignore = {"node_modules",".git","dist","build","__pycache__",".next"}

    all_results = []
    targets = [args.file] if args.file else []

    if not args.file:
        for root, dirs, files in os.walk(args.dir):
            dirs[:] = [d for d in dirs if d not in ignore]
            for f in files:
                if Path(f).suffix in exts:
                    targets.append(os.path.join(root, f))

    for t in targets:
        all_results.extend(analyze_file(t))

    if all_results:
        print(f"发现 {len(all_results)} 个代码坏味道:\n")
        for r in all_results:
            print(r)
    else:
        print("未发现明显坏味道 [OK]")

if __name__ == "__main__":
    main()
