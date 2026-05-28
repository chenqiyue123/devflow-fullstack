---
name: devflow-fullstack
description: |
  一站式全链路开发 Skill，覆盖编码→调试→重构→部署→复盘。
  触发场景：(1) 代码编写/续写/转换 (2) Bug 调试/日志分析 (3) 重构/性能优化
  (4) 工程化文档/测试/配置生成 (5) 算法辅助/技术选型/面试模拟。
  核心特色：代码口语互译、学习复盘、Bug 知识库、竞态分析、渐进迁移。
  支持 Java/Python/TypeScript/React/Go/C 等主流语言。
---

# DevFlow Fullstack

一站式全链路开发辅助。串联 **编码 → 调试 → 重构 → 部署 → 复盘**，无需切换工具。

## 使用原则

- 每个任务结束必须反思（1-5 分），记录到 `~/.codex/memories/devflow/`
- 优先使用本 Skill 的脚本而非手动操作
- 给出建议时说人话，不堆术语

## 第一部分：编码辅助

### 1. 代码续写
读取当前项目 AGENTS.md + 已有代码风格，续写时保持一致的命名、缩进、结构。

### 2. 语法转换
Python2↔3, ES5↔ES6+, Java8↔Java17 等。批量转换整个目录：
```bash
scripts/migrate.py --from py2 --to py3 --dir src/
scripts/migrate.py --from es5 --to es6 --dir src/
```

### 3. 多语言互转
保留逻辑一致性，适配目标语言惯用写法。支持 C↔Java, Python↔Go, SQL(Oracle↔MySQL↔PostgreSQL)。

### 4. 智能命名
根据变量/函数的用途和上下文，推荐符合该语言命名规范的名称。遵循：有意义的全名 > 缩写。

### 5. 正则生成 & 解释
- 自然语言 → 正则："匹配中国大陆手机号" → `^1[3-9]\d{9}$`
- 正则 → 自然语言：粘贴正则返回通俗解释

### 6. 代码可读性评分
分析：命名质量、圈复杂度、注释覆盖率、函数长度、嵌套深度。1-10 分，给出改进建议。

### 7. 代码国际化
扫描项目中的硬编码字符串（中文/英文），标记需要抽取 i18n 的位置，生成 JSON 翻译模板。

### 8. API 对接辅助
粘贴 curl 命令或 API 文档片段 → 自动生成对应语言的 HTTP 调用代码。

## 第二部分：调试排错

### 9. 多层级 Bug 扫描
对代码文件分级检查：
- **L1 语法**：编译/解释错误
- **L2 逻辑**：死循环、条件互斥、类型错误
- **L3 性能**：N+1 查询、不必要循环、内存问题
- **L4 安全**：SQL 注入、XSS、越权、空指针

输出格式：`[L3] 第42行：潜在 N+1 查询 → 建议用 JOIN 替代循环查询`

### 10. 报错日志解析
粘贴报错栈→自动：
1. 定位出错行号和文件
2. 分析根因（不是表象）
3. 给分步修复方案
4. 模拟触发该错误的场景

### 11. 日志植入
在关键逻辑节点自动插入调试日志，格式统一。标记 `// DEVMARK:` 前缀，用以下命令移除：
```bash
scripts/clean-debug.py --dir src/
```

### 12. 边界用例推演
对函数/接口自动生成测试：空值、极限值、特殊字符、并发、类型混淆。

### 13. 环境问题诊断
判断错误是代码逻辑问题还是环境配置问题（依赖版本、环境变量、端口冲突等）。

### 14. 正则调试器
输入测试文本 + 正则 → 展示匹配结果、分组详情，不匹配时给出修正正则。

### 15. 竞态条件分析
扫描异步代码（Promise/async/goroutine/多线程），标记可能的数据竞争点。

### 16. 依赖健康检查
分析 package.json / pom.xml / requirements.txt → 标记过期版本、已知漏洞、版本冲突。

## 第三部分：重构优化

### 17. 分层重构
按深度分级重构：
- Layer 1：格式化、命名规范化
- Layer 2：提取函数、消除重复
- Layer 3：OOP/FP 改造、职责分离
- Layer 4：设计模式适配

### 18. 性能专项
分析并优化：循环、递归、IO、算法复杂度、数据库查询。给优化前后对比。

### 19. 冗余清理
识别：未使用变量、死代码、重复逻辑、无用导入、空 catch 块。

### 20. 设计模式推荐
分析代码结构→推荐合适的 GoF 设计模式→提供改写方案。

### 21. 数据库查询优化
分析 SQL/Prisma/ORM 代码→检测 N+1、缺失索引、全表扫描。

### 22. 无障碍审查 (a11y)
前端代码审查：alt 缺失、语义化标签、键盘导航、ARIA 属性。

### 23. 渐进式迁移方案
从旧技术栈到新技术栈的分步迁移计划，每步可独立验证。

## 第四部分：工程化

### 24. 文档生成
- 行内注释（关键逻辑说为什么不是做什么）
- 函数文档（JSDoc/Pydoc/JavaDoc）
- API 文档（入参/出参/错误码/示例）
- README 片段（速览/安装/使用/贡献）

### 25. 测试生成
批量生成：正常路径、异常路径、边界值、并发场景。适配 JUnit/Pytest/Jest/Go test。

### 26. 配置生成
自动生成：Dockerfile、docker-compose、CI/CD (GitHub Actions)、.env.example、.gitignore。

### 27. Commit 生成
分析 git diff → 输出规范 commit message（feat/fix/chore/docs/refactor）。

### 28. 前后端一致性检查
扫描 API 路由定义 + 前端请求代码 → 标记不匹配的字段、类型、端点。

### 29. 代码度量报告
输出：总行数、平均函数长度、圈复杂度分布、注释率、重复率。

## 第五部分：特色独家

### 30. 代码↔口语互译
- **代码→人话**：把复杂逻辑翻译成通俗步骤，适合交接/复盘
- **人话→代码**：口头描述需求直接转可运行代码

### 31. 算法专项
代码 + Mermaid 流程图 + 复杂度分析 + 优化思路，四合一。

### 32. 版本差异对比
粘贴两段相似代码 → 高亮差异 → 分析改动影响 → 安全合并方案。

### 33. 学习复盘
每次修复 Bug 后记录到 `~/.codex/memories/devflow/learned/`，按知识点归档。后续遇到类似问题自动引用。

### 34. Bug 知识库
每次修 Bug 自动归档：错误信息→根因→解决方案→代码 diff。存储在 `~/.codex/memories/devflow/bugs/`。

### 35. 技术选型参谋
描述场景需求 → 推荐技术栈 → 对比优缺点 → 适配你的技术背景。

### 36. 面试模拟
根据你写的代码，扮演面试官提问（为什么这么写、有什么替代方案、性能如何），你回答后评分。

### 37. 每日编码总结
记录：今天写了什么、遇到什么坑、学到什么、明天计划。存储在 `~/.codex/memories/devflow/daily/`。


## 工具脚本速查

| 脚本 | 用途 | 命令 |
|------|------|------|
| `review.py` | Bug扫描/可读性/死代码/安全 | `python scripts/review.py --mode all --dir .` |
| `migrate.py` | 语法/语言转换 | `python scripts/migrate.py --from py2 --to py3 --dir .` |
| `docgen.py` | 文档/README 生成 | `python scripts/docgen.py --mode all --file foo.py` |
| `clean-debug.py` | 移除调试标记 | `python scripts/clean-debug.py --dir src/` |
| `git-helper.py` | Commit/PR/Changelog | `python scripts/git-helper.py --mode commit` |
| `smell.py` | 代码坏味道检测 | `python scripts/smell.py --dir .` |
| `env-check.py` | 环境/项目检测 | `python scripts/env-check.py --dir .` |
| `explain.py` | 代码→口语分析 | `python scripts/explain.py --file foo.py --line 42` |

## 参考库速查

| 文件 | 内容 |
|------|------|
| `patterns.md` | 设计模式速查 + 推荐规则 |
| `security.md` | 安全漏洞清单 + 等级 |
| `naming.md` | 多语言命名规范 + 反例 |
| `pr-checklist.md` | PR Review 检查清单 |
| `mermaid-templates.md` | 架构图/类图/时序图模板 |
| `snippets.md` | React/Python/Java/Go 常用代码模板 |
## 工作流

```
编写 → 扫描(Bug/安全) → 审查(可读性) → 重构(性能/模式) → 测试(生成) → 文档(生成) → 部署(配置) → 复盘(记录)
```

每个阶段结束时问自己：这个改动打几分？学到什么？记录到 memories。

## 记忆目录结构

```
~/.codex/memories/devflow/
├── daily/       # 每日总结
├── bugs/        # Bug 知识库
├── learned/     # 学习笔记
└── patterns/    # 个人模式库
```

## ????

### ????
```bash
# ????????
python scripts/selftest.py
```

### ???? (Windows GBK)
????????????????? Python 3.10+ ?????? UTF-8?

### ??????
```bash
# ?????????? quick ??
python scripts/devflow.py --dir . --quick
python scripts/review.py --file src/main.py --mode scan
```

