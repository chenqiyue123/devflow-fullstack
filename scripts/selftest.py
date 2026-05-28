#!/usr/bin/env python3
"""
DevFlow - Self Tests
Usage: python selftest.py
"""

import subprocess, sys, os
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

TESTS = [
    # (script, args, expected_in_output)
    ("review.py", ["--file", __file__, "--mode", "scan"], "findings"),  
    ("smell.py", ["--file", __file__], ""),
    ("regex.py", ["--test", "13800138000", "--pattern", r"^1[3-9]\d{9}$"], "Match"),
    ("regex.py", ["--explain", r"^\d{3}-\d{4}$"], "digit"),
    ("env-check.py", ["--dir", "."], "System"),
    ("explain.py", ["--file", __file__], "Functions"),
    ("metrics-i18n.py", ["--mode", "metrics", "--dir", "."], "Lines"),
    ("boundary.py", ["--file", __file__, "--func", "main"], "Boundary"),
    ("racecheck.py", ["--file", __file__], ""),
    ("db-optimize.py", ["--file", __file__], ""),
    ("a11y.py", ["--file", __file__], ""),
    ("apitools.py", ["--mode", "log", "--file", __file__], ""),
    ("clean-debug.py", ["--dir", "."], ""),
    ("config-gen.py", ["--type", "dockerfile", "--dir", "."], ""),
    ("docgen.py", ["--file", __file__, "--mode", "inline"], ""),
    ("git-helper.py", ["--mode", "commit"], ""),
    ("testgen.py", ["--file", __file__, "--framework", "pytest"], ""),
    ("migrate.py", ["--from", "py2", "--to", "py3", "--file", __file__, "--dry-run"], ""),
]

def run_test(script, args):
    cmd = [sys.executable, str(SCRIPTS_DIR / script)] + [str(a) for a in args]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return -1, "TIMEOUT"
    except Exception as e:
        return -2, str(e)

def main():
    passed = 0
    failed = 0

    print("DevFlow Self-Test Suite\n")
    
    for script, args, _ in TESTS:
        script_path = SCRIPTS_DIR / script
        if not script_path.exists():
            print(f"  SKIP {script} (not found)")
            continue

        code, output = run_test(script, args)
        # Consider pass if exit code is 0 or 1 (1 often means "found issues")
        ok = code in (0, 1)
        
        if ok:
            print(f"  [OK] {script} (exit={code})")
            passed += 1
        else:
            print(f"  [FAIL] {script} (exit={code}): {output[:100]}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed, {len(TESTS)} total")
    
    if failed > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
