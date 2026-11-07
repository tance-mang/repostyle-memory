"""Read-only repository evidence and explicit command recording; standard library only."""
import argparse
import datetime
import json
from pathlib import Path
import platform
import subprocess
import sys

DEFAULTS = {"language": "zh-CN", "preserve_manual_sections": True, "protected_sections": []}


def config(path):
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("Configuration must be a JSON object")
    return value


def merge(base, override):
    result = dict(base)
    for key, value in override.items():
        result[key] = merge(result[key], value) if isinstance(result.get(key), dict) and isinstance(value, dict) else value
    return result


def git(root, *args):
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}


def inspect(root, profile=None):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Repository directory does not exist")
    rules = merge(DEFAULTS, config(profile)) if profile else dict(DEFAULTS)
    if (root / ".repostyle.json").exists():
        rules = merge(rules, config(root / ".repostyle.json"))
    signals = []
    for kind, pattern in [("skill", "SKILL.md"), ("skill", "skills/*/SKILL.md"), ("web", "index.html"), ("application", "package.json"), ("tool", "pyproject.toml"), ("game", "project.godot"), ("game", "game.json")]:
        for path in root.glob(pattern):
            signals.append({"type": kind, "evidence": path.relative_to(root).as_posix()})
    return {"types": sorted({s["type"] for s in signals}) or ["unknown"], "signals": signals, "rules": rules,
            "head": git(root, "rev-parse", "HEAD"), "status": git(root, "status", "--porcelain=v1"),
            "unstaged": git(root, "diff", "--stat"), "staged": git(root, "diff", "--cached", "--stat"),
            "recent_commits": git(root, "log", "-5", "--format=%h %s")}


def record(root, command, output):
    if not command:
        raise ValueError("Provide an explicit command after --")
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    head = git(root, "rev-parse", "HEAD")
    status = git(root, "status", "--porcelain=v1")
    try:
        p = subprocess.run(command, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", shell=False)
        code, stdout, stderr = p.returncode, p.stdout, p.stderr
    except OSError as exc:
        code, stdout, stderr = 127, "", str(exc)
    evidence = {"started_utc": started, "platform": platform.platform(), "python": platform.python_version(), "head": head, "working_tree": status,
                "command": command, "exit_code": code, "status": "command_succeeded" if code == 0 else "command_failed", "stdout": stdout, "stderr": stderr}
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Refuse to silently overwrite earlier evidence.
    with target.open("x", encoding="utf-8") as stream:
        json.dump(evidence, stream, ensure_ascii=False, indent=2)
    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    scan = sub.add_parser("inspect")
    scan.add_argument("root")
    scan.add_argument("--profile")
    run = sub.add_parser("record")
    run.add_argument("--root", default=".")
    run.add_argument("--output", required=True)
    run.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == "inspect":
            print(json.dumps(inspect(args.root, args.profile), ensure_ascii=False, indent=2))
            return 0
        command = args.command[1:] if args.command[:1] == ["--"] else args.command
        if Path(args.output).exists():
            raise ValueError("Evidence output already exists")
        return record(args.root, command, args.output)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc) + "\n")


if __name__ == "__main__":
    sys.exit(main())
