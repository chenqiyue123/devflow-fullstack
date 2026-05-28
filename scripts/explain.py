#!/usr/bin/env python3
"""
DevFlow - Code <-> Natural Language Translator (#30)
Usage:
  python explain.py --file foo.py              # code -> human language
  python explain.py --file foo.py --line 42    # explain specific line

NOTE: Full natural language -> code requires LLM. This script provides
structure analysis; combine with Skills for full translation.
"""

import argparse, re
from pathlib import Path

LANG_MAP = {".py":"Python", ".js":"JavaScript", ".ts":"TypeScript", ".tsx":"React+TS",
            ".jsx":"React", ".java":"Java", ".go":"Go", ".c":"C", ".cpp":"C++", ".rs":"Rust"}

def analyze_structure(filepath):
    """Extract code structure: imports, functions, classes, complexity hints"""
    content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    ext = Path(filepath).suffix
    lang = LANG_MAP.get(ext, "Unknown")

    result = [f"# 代码分析: {Path(filepath).name}", f"语言: {lang}", f"总行数: {len(lines)}", ""]

    # Functions
    funcs = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"(?:def|function|func|public|private|protected|static|async)\s+(\w+)\s*\(([^)]*)\)", line.strip())
        if m:
            funcs.append({"line": i, "name": m.group(1), "params": m.group(2)})

    if funcs:
        result.append("## 函数列表")
        for f in funcs:
            params_str = f['params'].strip() if f['params'].strip() else "无参数"
            result.append(f"- **{f['name']}**(第{f['line']}行): 参数={params_str}")
    else:
        result.append("- 未检测到函数定义")

    # Imports
    imports = [l.strip() for l in lines if l.strip().startswith(("import ","from ","require(","use "))]
    if imports:
        result.append(f"\n## 依赖导入 ({len(imports)}个)")
        for imp in imports[:5]:
            result.append(f"- `{imp}`")

    # Complexity indicators
    loops = sum(1 for l in lines if re.search(r"\b(for|while)\s*\(", l))
    conditionals = sum(1 for l in lines if re.search(r"\bif\s+", l))
    try_blocks = sum(1 for l in lines if re.search(r"\btry\s*:", l))

    result.append(f"\n## 复杂度概览")
    result.append(f"- 循环: {loops} 个")
    result.append(f"- 条件分支: {conditionals} 个")
    result.append(f"- 异常处理: {try_blocks} 个")

    if loops > 5:
        result.append("  [!] 循环较多，检查是否有优化空间")
    if conditionals > 10:
        result.append("  [!] 条件分支较多，考虑策略模式或多态")

    return "\n".join(result)

def explain_line(filepath, line_num, context=3):
    """Explain what a specific line does"""
    content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")
    start = max(0, line_num - context - 1)
    end = min(len(lines), line_num + context)

    result = [f"# 行 {line_num} 上下文分析\n"]
    result.append("```")
    for i in range(start, end):
        marker = "-> " if i == line_num - 1 else "  "
        result.append(f"{marker}{i+1}: {lines[i]}")
    result.append("```")

    target = lines[line_num - 1].strip() if line_num <= len(lines) else ""
    if target:
        result.append(f"\n**代码**: `{target[:80]}`")
        # Pattern-based explanations
        if "=" in target and "==" not in target:
            result.append("- 这是一个**赋值**操作")
        if re.search(r"\bif\b", target):
            result.append("- 这是一个**条件判断**")
        if re.search(r"\bfor\b|\bwhile\b", target):
            result.append("- 这是一个**循环**")
        if re.search(r"\bdef\b|\bfunction\b", target):
            result.append("- 这是一个**函数定义**")
        if re.search(r"\breturn\b", target):
            result.append("- 这是函数的**返回**语句")
        if re.search(r"\btry\b", target):
            result.append("- 这是**异常处理**的开始")
        if re.search(r"\bprint\b|\bconsole\.log\b", target):
            result.append("- 这是**调试输出**")

    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description="Code <-> Natural Language Translator")
    parser.add_argument("--file", required=True)
    parser.add_argument("--line", type=int, help="解释特定行")
    args = parser.parse_args()

    if args.line:
        print(explain_line(args.file, args.line))
    else:
        print(analyze_structure(args.file))

if __name__ == "__main__":
    main()
