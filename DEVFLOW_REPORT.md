# DevFlow Pipeline Report

- **Target**: `D:\CodexSkills\devflow-fullstack\scripts`
- **Time**: 2026-05-28 19:49:10
- **Duration**: 1.3s

## Summary: 7/7 checks passed

| Step | Result | Time |
|------|--------|------|
| Environment & Project Detection | [OK] | 0.4s |
| Code Metrics | [OK] | 0.1s |
| Bug & Security & Readability Scan | [OK] | 0.2s |
| Code Smell Detection | [OK] | 0.2s |
| Race Condition Analysis | [OK] | 0.2s |
| Database Query Optimization | [OK] | 0.1s |
| i18n Hardcoded String Detection | [OK] | 0.1s |

### Environment & Project Detection

```
系统: Windows 10 (AMD64)
Python: 3.11.9
Node.js: v24.15.0
Git: 已安装
Java: 已安装
Docker: 未安装

项目类型: 未知

建议添加: .gitignore, README.md
```

### Code Metrics

```
# Code Metrics Report

## 概览
- 总文件: 19
- 总行数: 2,261
- 平均每文件: 119 行

## 语言分布
- .py: 19 文件

## 最大文件
- `D:\CodexSkills\devflow-fullstack\scripts\review.py`: 224 行

## 建议
- [OK] 文件大小合理
- [OK] 项目规模适中
```

### Bug & Security & Readability Scan

```
=== Bug 扫描 ===
[L3] D:\CodexSkills\devflow-fullstack\scripts\db-optimize.py:12 - ??????? -> ??? N+1 ??
[L4] D:\CodexSkills\devflow-fullstack\scripts\review.py:16 - os.system() ???????? -> subprocess.run(shell=False)
[L4] D:\CodexSkills\devflow-fullstack\scripts\review.py:17 - eval() ???? -> ? ast.literal_eval ???????
[L4] D:\CodexSkills\devflow-fullstack\scripts\review.py:19 - React dangerouslySetInnerHTML -> ? DOMPurify ??
[L4] D:\CodexSkills\devflow-fullstack\scripts\review.py:24 - XML ?? -> ? defusedxml ? XXE
[L3] D:\CodexSkills\devflow-fullstack\scripts\review.py:39 - ??????? -> ??? N+1 ??
[L3] D:\CodexSkills\devflow-fullstack\scripts\review.py:40 - ??????? -> ??? N+1 ??
[L3] D:\CodexSkills\devflow-fullstack\scripts\review.py:40 - ???????? -> ? JOIN/batch ??
[L3] D:\CodexSkills\devflow-fullstack\scripts\testgen.py:40 - ????? -> ?????????????

=== 可读性评估 ===
  D:\CodexSkills\devflow-fullstack\scripts\a11y.py: 7/10
  D:\CodexSkills\devflow-fullstack\scripts\apitools.py: 6.5/10
  D:\CodexSkills\devflow-fullstack\scripts\boundary.py: 7.5/10
  D:\CodexSkills\devflow-fullstack\scripts\clean-debug.py: 8/10
  D:\CodexSkills\devflow-fullstack\scripts\config-gen.py: 8/10
  D:\CodexSkills\devflow-fullstack\scripts\db-optimize.py: 8.0/10
  D:\CodexSkills\devflow-fullstack\scripts\devflow.py: 7.0/10
  D:\CodexSkills\devflow-fullstack\scripts\docgen.py: 9.0/10
  D:\CodexSkills\devflow-fullstack\scripts\env-check.py: 8.5/10
  D:\CodexSkills\devflow-fullstack\scripts\explain.py: 7.0/10
  D:\CodexSkills\devflow-fullstack\scripts\git-helper.py: 8/10
  D:\CodexSkills\devflow-fullstack\scripts\metrics-i18n.py: 9.0/10
  D:\CodexSkills\devflow-fullstack\scripts\migrate.py: 4.5/10
  D:\CodexSkills\devflow-fullstack\scripts\racecheck.py: 3.5/10
  D:\CodexSkills\devflow-fullstack\scripts\regex.py: 8/10
  D:\CodexSkills\devflow-fullstack\scripts\review.py: 3.0/10
  D:\CodexSkills\devflow-fullstack\scripts\selftest.py: 8/10
  D:\CodexSkills\devflow-fullstack\scripts\smell.py: 9/10
  D:\Cod
... (truncated)
```

### Code Smell Detection

```
发现 161 个代码坏味道:

[magic_number] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:16 - 魔法数字 -> 提取为命名常量
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:11 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:12 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:13 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:16 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:17 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:18 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:19 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\a11y.py:54 - 单字母/无意义变量名 -> 用描述性名称
[long_method] D:\CodexSkills\devflow-fullstack\scripts\apitools.py - 函数过长 (>80行) -> 拆分为多个小函数
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:3 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:123 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:124 - 魔法数字 -> 提取为命名常量
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:36 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:91 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:130 - 单字母/无意义变量名 -> 用描述性名称
[bad_name] D:\CodexSkills\devflow-fullstack\scripts\apitools.py:132 - 单字母/无意义变量名 -> 用描述性名称
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\boundary.py:3 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\boundary.py:14 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\boundary.py:16 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\boundary.py:18 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullstack\scripts\boundary.py:20 - 魔法数字 -> 提取为命名常量
[magic_number] D:\CodexSkills\devflow-fullst
... (truncated)
```

### Race Condition Analysis

```
未发现明显并发问题 [OK]
```

### Database Query Optimization

```
未发现数据库查询问题 [OK]
```

### i18n Hardcoded String Detection

```
未发现硬编码中文字符串 [OK]
```
