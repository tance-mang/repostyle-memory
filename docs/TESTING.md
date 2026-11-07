# 测试与验证记录

## 2026-11-07（Asia/Shanghai）本地验证

环境：Windows、Python 3.13.5、Git 2.53.0；首次提交前工作树。

执行：`python -m unittest discover -s tests -v`

结果：9 项测试通过，退出码 0。覆盖嵌套配置覆盖、项目规则优先级、非法配置、混合仓库、未知类型、无 HEAD 仓库及未跟踪文件、失败命令证据、成功命令不编造测试数、拒绝覆盖旧记录。原始输出见 [local-tests.txt](evidence/local-tests.txt)。

技能格式检查：`python -X utf8 <skill-creator>/scripts/quick_validate.py .`。Windows 默认 GBK 解码首次失败，启用 UTF-8 后重新验证；这是校验器的默认编码问题。

## 复现

```bash
python -m unittest discover -s tests -v
```

CI 配置覆盖 Windows / Ubuntu / macOS 与 Python 3.11 / 3.13；是否通过以 [实际 Actions 记录](https://github.com/tance-mang/repostyle-memory/actions/workflows/tests.yml)为准。

## 待验证

- 在小说 Skill、自动化工具、网页三个真实仓库连续维护三轮。
- 换 AI 后的风格一致性、受保护章节保持和内容准确性。
- 不同客户端的技能自动发现与隐式触发。

以上没有计入已通过的自动化测试，不承诺跨客户端效果。
