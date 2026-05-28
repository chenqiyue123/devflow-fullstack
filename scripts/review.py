#!/usr/bin/env python3
"""
DevFlow Fullstack - Code Review & Analysis
Usage: python review.py [--mode scan|readability|security|deps|deadcode|a11y|duplication|metrics] [--file FILE | --dir DIR]
"""

import argparse, os, re, json, sys
from pathlib import Path
from collections import defaultdict

SEVERITY = {"L1": "[!!]??", "L2": "[!]??", "L3": "[*]??", "L4": "[i]??"}

# Security patterns
SECURITY_PATTERNS = [
    (r"execute\s*\(.*\\+", "L4", "SQL ?? -> ??????"),
    (r"os\.system\(", "L4", "os.system() ???????? -> subprocess.run(shell=False)"),
    (r"eval\(", "L4", "eval() ???? -> ? ast.literal_eval ???????"),
    (r"innerHTML\s*=", "L4", "innerHTML ? XSS ?? -> ? textContent ? DOMPurify"),
    (r"dangerouslySetInnerHTML", "L4", "React dangerouslySetInnerHTML -> ? DOMPurify ??"),
    (r"\.md5\(|\.sha1\(", "L4", "????? -> ?? SHA256/bcrypt"),
    (r"password\s*=\s*[\x27\x22][^\x27\x22]+[\x27\x22]", "L4", "????? -> ?????"),
    (r"os\.popen\(|subprocess\.call\(.*shell\s*=\s*True", "L4", "?????? -> subprocess.run(shell=False)"),
    (r"\.execute\([^)]*f[\x27\x22]|\.execute\([^)]*%", "L4", "SQL??: f-string/?????? -> ?????"),
    (r"xml\.etree|defusedxml|xml\.dom\.minidom", "L4", "XML ?? -> ? defusedxml ? XXE"),
    (r"pickle\.loads?\(|yaml\.load\(", "L4", "?????? -> ? yaml.safe_load() / ?? pickle"),
    (r"assert\s+.*password|assert\s+.*token", "L4", "assert ??????? -> ?????? assert"),
]

# Logic patterns
LOGIC_PATTERNS = [
    (r"except\s*:\s*pass", "L2", "??? -> ?????????"),
    (r"if\s+\w+\s*==\s*None:\s*\n\s*\w+\s*=\s*\[\]", "L2", "???????? -> ? None + ?????"),
    (r"==\s*True\b|==\s*False\b", "L2", "? True/False ?? -> ??? if x / if not x"),
    (r"is\s+not\s+.*\s*==|is\s+.*\s*!=", "L2", "?? is ? == -> is ?????== ???"),
]

# Performance patterns
PERF_PATTERNS = [
    (r"for\s+.*\n\s*for\s+.*\n\s*.*\.find|\.filter|\.query", "L3", "??????? -> ??? N+1 ??"),
    (r"\.forEach.*\.query|\.map.*\.query", "L3", "???????? -> ? JOIN/batch ??"),
    (r"console\.log\(", "L3", "?????? console.log -> ????????"),
    (r"JSON\.parse\(JSON\.stringify", "L3", "????? -> ? structuredClone() ? lodash.cloneDeep"),
    (r"\.concat\(", "L3", "??????? -> ? StringBuilder/join"),
    (r"\.readlines\(\)", "L3", "readlines() ?????????? -> ????"),
    (r"sleep\(\d+\)", "L3", "??? sleep -> ??????????"),
    (r"\+\s*=\s*[\x27\x22].*for\s+\w+\s+in", "L3", "???????? -> ? join() ? StringBuilder"),
    (r"import\s+\*", "L3", "????? -> ?????????????"),
]


def is_pattern_definition(line):
    """Skip lines that define security/perf patterns (false positives)"""
    return bool(re.search(r"SECURITY_PATTERNS|PERF_PATTERNS|r'|\"\"\"", line))

def scan_file(filepath):



    """Multi-level bug scan on a single file"""
    results = []
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")

        for i, line in enumerate(lines, 1):
            for pattern, level, msg in SECURITY_PATTERNS + LOGIC_PATTERNS + PERF_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE) and not re.search(r"// devflow-ignore|^\s*(#|//|/\*)", line) and not is_pattern_definition(line):
                    results.append(f"[{level}] {filepath}:{i} - {msg}")
        return results
    except Exception as e:
        return [f"[ERR] {filepath}: {e}"]

def readability_score(filepath):
    """Score code readability 1-10"""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        total_lines = len(lines)

        if total_lines == 0:
            return {"file": filepath, "score": 0, "issues": ["Empty file"]}

        # Metrics
        non_empty = [l for l in lines if l.strip() and not l.strip().startswith("//") and not l.strip().startswith("#")]
        comment_lines = len([l for l in lines if l.strip().startswith("//") or l.strip().startswith("#") or l.strip().startswith("/*") or l.strip().startswith("*")])
        long_funcs = []
        current_func = None
        func_lines = 0
        nesting = 0
        max_nesting = 0

        for line in lines:
            stripped = line.strip()
            # Track nesting
            for ch in stripped:
                if ch in "{(":
                    nesting += 1
                elif ch in "})":
                    nesting -= 1
            max_nesting = max(max_nesting, nesting)

            # Track function length
            if re.match(r"(def |function |func |public |private |protected )", stripped):
                if current_func and func_lines > 30:
                    long_funcs.append(f"{current_func}({func_lines}行)")
                current_func = stripped[:40]
                func_lines = 0
            if current_func:
                func_lines += 1

        comment_ratio = comment_lines / total_lines if total_lines > 0 else 0
        issues = []

        # Scoring
        score = 10
        if comment_ratio < 0.05:
            issues.append(f"注释率仅 {comment_ratio:.1%} -> 建议 ≥10%")
            score -= 2
        if long_funcs:
            issues.append(f"函数过长: {', '.join(long_funcs[:3])}")
            score -= len(long_funcs) * 0.5
        if max_nesting > 3:
            issues.append(f"嵌套深度 {max_nesting} -> 建议 ≤3")
            score -= (max_nesting - 3) * 0.5
        if any(len(l) > 120 for l in non_empty):
            issues.append("存在超长行 (>120字符)")
            score -= 1

        return {
            "file": filepath,
            "score": max(1, round(score, 1)),
            "lines": total_lines,
            "comment_ratio": f"{comment_ratio:.1%}",
            "long_functions": len(long_funcs),
            "max_nesting": max_nesting,
            "issues": issues[:5]
        }
    except Exception as e:
        return {"file": filepath, "score": 0, "issues": [str(e)]}

def find_dead_code(filepath):
    """Find potentially dead code"""
    try:
        content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
        lines = content.split("\n")
        results = []

        # Unused imports
        imports = re.findall(r"import\s+(\w+)", content)

        for i, line in enumerate(lines, 1):
            # Empty catch blocks
            if re.search(r"catch\s*\(.*\)\s*\{\s*\}", line):
                results.append(f"{filepath}:{i} - 空 catch 块 -> 应至少记录日志")
            # Commented-out code blocks (>3 lines of commented code)
            # TODO/XXX without follow-up

        return results
    except Exception:
        return []

def scan_dir(dirpath, mode="scan"):
    """Scan entire directory"""
    all_results = []
    exts = {".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".c", ".cpp", ".rs", ".rb", ".php"}
    ignore = {"node_modules", ".git", "__pycache__", "dist", "build", ".next", "target", "vendor"}

    for root, dirs, files in os.walk(dirpath):
        dirs[:] = [d for d in dirs if d not in ignore]
        for f in files:
            if Path(f).suffix in exts:
                fp = os.path.join(root, f)
                if mode == "scan":
                    all_results.extend(scan_file(fp))
                elif mode == "readability":
                    all_results.append(readability_score(fp))
                elif mode == "deadcode":
                    all_results.extend(find_dead_code(fp))

    return all_results

def main():
    parser = argparse.ArgumentParser(description="DevFlow Code Review")
    parser.add_argument("--mode", default="scan", choices=["scan","readability","security","deadcode","all"])
    parser.add_argument("--file")
    parser.add_argument("--dir", default=".")
    args = parser.parse_args()

    target = args.file if args.file else args.dir

    if args.mode == "scan":
        results = scan_file(target) if args.file else scan_dir(target, "scan")
        for r in results:
            print(r)
        print(f"\n共 {len(results)} 条发现")

    elif args.mode == "readability":
        results = [readability_score(target)] if args.file else scan_dir(target, "readability")
        for r in results:
            print(f"{r['file']}: 评分 {r['score']}/10 | {r['lines']}行 | 注释率{r.get('comment_ratio','N/A')} | 嵌套{r.get('max_nesting','?')}层")
            for i in r.get("issues", []):
                print(f"  -> {i}")

    elif args.mode == "deadcode":
        results = find_dead_code(target) if args.file else scan_dir(target, "deadcode")
        for r in results:
            print(r)

    elif args.mode == "all":
        print("=== Bug 扫描 ===")
        scan_results = scan_dir(target, "scan")
        for r in scan_results:
            print(r)
        print(f"\n=== 可读性评估 ===")
        read_results = scan_dir(target, "readability")
        for r in read_results:
            print(f"  {r['file']}: {r['score']}/10")
        print(f"\n=== 死代码检测 ===")
        dead_results = scan_dir(target, "deadcode")
        for r in dead_results:
            print(r)

if __name__ == "__main__":
    main()
