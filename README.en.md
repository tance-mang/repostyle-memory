# RepoStyle Memory · 仓库文风

**Your repositories. Your writing style.**

A portable agent skill for developers tired of explaining their documentation preferences every time they change projects or AI tools.

[中文说明](README.md) · [Test evidence](docs/TESTING.md) · [Changelog](CHANGELOG.md)

## Start

```bash
git clone https://github.com/tance-mang/repostyle-memory.git
```

Ask your coding agent to read `repostyle-memory/SKILL.md` and apply it to your target repository. Copy `examples/profile.json` to a personal location and provide its path. Project-specific preferences live in `.repostyle.json`. Register the complete directory through your client's supported skill mechanism if available; automatic discovery is client-dependent.

## What it provides

- Portable personal preferences with project overrides.
- Evidence-based, incremental README and changelog maintenance by the agent.
- Repository type signals and Git inspection through a Python helper.
- Explicit command execution records without invented test counts.
- Guidance for names, descriptions, Topics and first-time visitor experience.

The helper needs Python 3.11+ and Git, with no third-party Python dependencies:

```bash
python scripts/repostyle.py inspect . --profile examples/profile.json
python -m unittest discover -s tests -v
python scripts/repostyle.py record --root . --output work/test-run.json -- python -m unittest discover -s tests -v
```

This is an agent workflow with supporting scripts, not a standalone README generator or background service. Cross-agent consistency and real-world incremental editing remain to be validated. Publishing follows the user's existing authorization and Git workflow.

Created by tance-mang with OpenAI Codex assistance. Presentation inspired by the author's [Chinese Webnovel Skills](https://github.com/tance-mang/chinese-webnovel-skills). Not an official OpenAI product.

[MIT License](LICENSE).
