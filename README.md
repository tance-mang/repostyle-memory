<div align="center">

# 仓库文风 · RepoStyle Memory

**你的仓库，你的文风。让 AI 接着维护，不必每次重新交代。**

个人规范 → 仓库识别 → 变更证据 → 文档增量更新 → 真实测试记录

[![Tests](https://github.com/tance-mang/repostyle-memory/actions/workflows/tests.yml/badge.svg)](https://github.com/tance-mang/repostyle-memory/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**简体中文** | [English](README.en.md)

</div>

你已经让 AI 开发了项目，却仍要反复解释 README 怎么写、测试怎么记、简介怎么介绍。RepoStyle Memory 把这些要求存成可迁移的规则，让后续维护有据可查。

适合维护多个 GitHub 项目的独立开发者，以及经常更换 AI 工具、希望保留个人文风的人。

## 快速上手

克隆技能：

```bash
git clone https://github.com/tance-mang/repostyle-memory.git
```

在能够读取本地文件的 AI 编程工具中，直接说：

> 读取 repostyle-memory/SKILL.md，按这个技能维护当前项目的 README、更新日志和测试记录。参考我指定的仓库风格，只更新本次变更涉及的内容。

复制 [examples/profile.json](examples/profile.json) 到你自己的配置目录，以后调用时指定这个文件。项目独有规则放到项目根目录 `.repostyle.json`。个人文件不用上传到公开仓库。

支持目录式技能的客户端可以将整个仓库目录注册为技能；具体安装位置和发现机制以客户端为准。这里提供标准 `SKILL.md`，不承诺所有客户端自动加载。普通聊天工具可阅读规则起草内容，但没有文件/终端权限就不能完成验证和推送。

## 能做什么

| 能力 | 实现方式与边界 |
|---|---|
| 保存文风 | JSON 个人配置 + 项目覆盖，随文件迁移 |
| 识别仓库 | Python 收集 Skill、应用、网页、工具、游戏线索；混合类型交给 AI 判断 |
| 增量维护 | 技能约束 AI 根据 diff 修改相关章节，保留手工保护区 |
| 真实测试记录 | 显式运行命令、记录环境、Git 状态、退出码和输出，不编造通过数量 |
| 版本维护 | AI 根据实际变化组织 Unreleased，保留历史 |
| GitHub 展示 | 命名、首屏定位、About 和相关 Topics；不保证获得 Star |

App 项目还可采用 [暖小圈风格参考](references/app-style.md)：产品任务开头、模块能力表、系统架构、分层技术栈与部署说明。只迁移写法，所有功能和验证结论来自当前项目。

**当前是可用的技能与辅助脚本初版，不是独立文档生成器或后台同步服务。** 文风一致性与跨 AI 行为仍需真实使用验证。

## 三种典型用法

**新项目展示**

> 用 RepoStyle Memory 整理这个仓库。给出名称、简介和 Topics，写清安装、示例和测试状态。参考 chinese-webnovel-skills 的信息层次，不复制它的功能和数字。

**开发后的维护**

> 根据本次 diff 更新文档，保留已有文风。没有执行的测试标待验证，变更加入 Unreleased。

**换 AI 继续维护**

> 读取这个技能、我的 profile.json 和项目 .repostyle.json，继续维护现有文档，不改变受保护章节。

## 辅助命令

需要 Python 3.11+ 和 Git，无第三方 Python 依赖。以下命令在本技能仓库根目录运行：

```bash
python scripts/repostyle.py inspect . --profile examples/profile.json
python -m unittest discover -s tests -v
python scripts/repostyle.py record --root . --output work/test-run.json -- python -m unittest discover -s tests -v
```

`inspect` 不修改目标仓库；输出包含 Git 错误状态，新仓库没有 HEAD 时也能收集其他信息。`record` 只运行显式给定的命令，拒绝覆盖已有记录；公开输出前检查是否包含私人信息。

## 测试与限制

[测试方法与记录](docs/TESTING.md)区分脚本验证、CI 和待验证的真实场景。运行成功不等于跨 AI 行为已验证；CI 徽章展示实际工作流状态。

暂未实现：自动偏好学习、无人值守同步、自动生成 README 的独立 CLI。不会自动改写用户全局规则或接管推送。

## 项目结构

```text
SKILL.md                 技能入口
agents/openai.yaml       技能展示信息
references/              展示规范、证据与版本规则
examples/profile.json    可迁移个人配置
scripts/repostyle.py     仓库检查与执行证据记录
tests/                   自动化测试
docs/TESTING.md           验证方法与真实记录
```

## 更新与贡献

见 [CHANGELOG.md](CHANGELOG.md) 和 [贡献指南](CONTRIBUTING.md)。欢迎提交真实的「更新前 → 代码变化 → 更新后」案例，说明期望保留的文风及误改位置。

## 致谢

展示结构参考作者的 [网文工坊 · chinese-webnovel-skills](https://github.com/tance-mang/chinese-webnovel-skills)：双语品牌、快速入口、能力表和维护记录。技能内容及脚本为本项目编写。

由 **tance-mang 发起，与 OpenAI Codex 协作开发**。Codex 参与技能设计、代码、文档和验证，不代表 OpenAI 官方项目或背书。

## 许可证

[MIT](LICENSE) © 2026 tance-mang
