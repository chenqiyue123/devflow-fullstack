# DevFlow Fullstack

一站式全链路开发辅助 Skill。串联 **编码 → 调试 → 重构 → 部署 → 复盘**，无需切换工具。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Scripts](https://img.shields.io/badge/Scripts-18-orange)](scripts/)

## 为什么用 DevFlow

代码写完 → Bug扫描 → 重构 → 测试 → 文档 → 部署 → 复盘，一条龙。19 个 Python 脚本 + 6 个参考库，覆盖 37 个功能点。

## 快速开始

```bash
# 一键跑全流程
python scripts/devflow.py --dir .

# 只看安全问题
python scripts/review.py --mode security --dir .

# 代码到人类语言
python scripts/explain.py --file main.py

# 生成测试
python scripts/testgen.py --file calculator.py --framework pytest
```

## 功能一览

| 模块 | 脚本 | 功能 |
|------|------|------|
| **编码** | `migrate.py` `explain.py` `apitools.py` `regex.py` `metrics-i18n.py` | 语法转换、代码解释、API对接、正则生成、度量 |
| **调试** | `review.py` `boundary.py` `racecheck.py` `env-check.py` `clean-debug.py` | Bug扫描、边界推演、竞态分析、环境诊断、调试清理 |
| **重构** | `smell.py` `db-optimize.py` `a11y.py` | 坏味道检测、SQL优化、无障碍审查 |
| **工程** | `docgen.py` `testgen.py` `config-gen.py` `git-helper.py` | 文档生成、测试生成、配置生成、Commit辅助 |
| **特色** | `devflow.py` `explain.py` | 全链路编排、代码↔口语互译、学习复盘 |

## 安装

```bash
git clone https://github.com/chenqiyue123/devflow-fullstack.git
cd devflow-fullstack
# 零依赖，直接跑
python scripts/selftest.py
```

## 用作 Codex Skill

```bash
# 创建软链接
mklink /J %USERPROFILE%\.codex\skills\devflow-fullstack D:\CodexSkills\devflow-fullstack
```

之后在 Codex 中自动触发，支持 `/devflow-review`、`/devflow-explain` 等指令。

## 参考库

| 文件 | 内容 |
|------|------|
| `references/patterns.md` | 设计模式速查 |
| `references/security.md` | 安全漏洞清单 |
| `references/naming.md` | 多语言命名规范 |
| `references/pr-checklist.md` | PR Review 检查清单 |
| `references/mermaid-templates.md` | 架构图模板 |
| `references/snippets.md` | 常用代码模板 |

## 作者

**陈启粤 (Queyue)** 

[![GitHub](https://img.shields.io/badge/GitHub-chenqiyue123-181717?logo=github)](https://github.com/chenqiyue123)

---

## 致谢

感谢每一位使用 DevFlow 的开发者。

这个项目的诞生源于一个简单的想法：写代码应该是一气呵成的事，不该在七八个工具之间反复横跳。如果你觉得它帮到了你，点个 Star 就是最好的支持。发现 Bug 或有想法？欢迎提 Issue 和 PR。

愿 DevFlow 陪你写出更干净的代码。

---

## 许可

MIT License
