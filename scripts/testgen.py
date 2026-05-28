#!/usr/bin/env python3
"""
DevFlow - Test Generator
Usage:
  python testgen.py --file calculator.py --framework pytest
  python testgen.py --file UserService.java --framework junit
  python testgen.py --dir src/ --framework jest
"""

import argparse, os, re
from pathlib import Path

FRAMEWORKS = {
    "pytest": {"imports": "import pytest\nimport sys\nsys.path.insert(0, '.')\n\n{module_import}", "func_template": 'def test_{func_name}():\n    """正常路径"""\n    {setup}\n    result = {func_name}({sample_args})\n    assert result is not None\n\n\ndef test_{func_name}_edge_cases():\n    """边界场景"""\n    # 空值\n    try:\n        {func_name}({edge_args})\n    except Exception as e:\n        assert isinstance(e, (ValueError, TypeError))\n\n    # 零值\n    # TODO: 添加零值测试\n\n    # 极大值\n    # TODO: 添加极限值测试\n\n\ndef test_{func_name}_error_handling():\n    """异常处理"""\n    with pytest.raises(Exception):\n        {func_name}({error_args})\n'},
    "junit": {"imports": 'import org.junit.jupiter.api.Test;\nimport org.junit.jupiter.api.BeforeEach;\nimport static org.junit.jupiter.api.Assertions.*;\n\n{module_import}', "func_template": '@Test\nvoid test{func_cap}() {\n    // 正常路径\n    {setup}\n    var result = {func_name}({sample_args});\n    assertNotNull(result);\n}\n\n@Test\nvoid test{func_cap}_edgeCases() {\n    // 边界场景\n    // 空值\n    assertThrows(Exception.class, () -> {func_name}({error_args}));\n\n    // 零值\n    // TODO: 添加零值测试\n}\n'},
    "jest": {"imports": "{module_import}\n\ndescribe('{func_cap}', () => {\n  it('should handle normal input', () => {\n    {setup}\n    const result = {func_name}({sample_args})\n    expect(result).toBeDefined()\n  })\n\n  it('should handle edge cases', () => {\n    // 空值\n    expect(() => {func_name}({error_args})).toThrow()\n\n    // 零值\n    // TODO: 添加零值测试\n  })\n})\n"},
}

def extract_functions(filepath):
    content = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    funcs = []
    patterns = [
        (r"def\s+(\w+)\s*\(([^)]*)\)", "python"),
        (r"public\s+\w+\s+(\w+)\s*\(([^)]*)\)", "java"),
        (r"export\s+(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)", "ts"),
        (r"(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>", "ts"),
    ]
    for pattern, lang in patterns:
        for m in re.finditer(pattern, content):
            name = m.group(1)
            if not name.startswith("_") and name not in ("main","init","constructor"):
                funcs.append({"name": name, "params": m.group(2), "lang": lang})
    return funcs

def generate_tests(funcs, framework, module_name):
    if framework not in FRAMEWORKS:
        return f"不支持的框架: {framework}"
    
    config = FRAMEWORKS[framework]
    module_import = f"from {module_name} import *" if framework == "pytest" else f"import {{ {', '.join(f['name'] for f in funcs[:3])} }} from './{module_name}'"
    imports = config["imports"].format(module_import=module_import)
    
    result = [imports]
    for func in funcs[:5]:  # Max 5 functions
        setup = ""
        sample_args = "1, 2" if func["params"] else ""
        edge_args = "None" if func["params"] else ""
        error_args = "None, None" if func["params"] else ""
        template = config["func_template"].format(
            func_name=func["name"],
            func_cap=func["name"][0].upper() + func["name"][1:],
            setup=setup,
            sample_args=sample_args,
            edge_args=edge_args,
            error_args=error_args
        )
        result.append(template)
    
    if framework == "jest":
        result.append("})")
    
    return "\n".join(result)

def main():
    parser = argparse.ArgumentParser(description="Test Generator")
    parser.add_argument("--file", required=True)
    parser.add_argument("--framework", default="pytest", choices=list(FRAMEWORKS.keys()))
    parser.add_argument("--output")
    args = parser.parse_args()

    funcs = extract_functions(args.file)
    if not funcs:
        print("未检测到可测试的函数")
        return

    module_name = Path(args.file).stem
    tests = generate_tests(funcs, args.framework, module_name)
    
    if args.output:
        Path(args.output).write_text(tests, encoding="utf-8")
        print(f"已生成测试文件: {args.output}")
    else:
        print(tests)

if __name__ == "__main__":
    main()
