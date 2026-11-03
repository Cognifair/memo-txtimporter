#!/usr/bin/env python3
"""Validate a TXT file and print the mandatory delivery block (tutorial + GIF + self-check)."""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = Path(__file__).with_name("lint_txt.py")
GIF = ROOT / "references" / "assets" / "import-flow-36b59d.gif"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print("NOTE: paste stdout as plain Markdown; do not wrap it in a code fence, "
          "or the GIF will not render.", file=sys.stderr)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="TXT file to validate")
    parser.add_argument("--member", choices=["pro", "free"], default="free",
                        help="Account tier; pro hard limit 4500, free hard limit 1800 (default: free)")
    parser.add_argument("--require-answer-line", action="store_true",
                        help="Require exactly one answer line per card")
    args = parser.parse_args()
    hard_limit = 4500 if args.member == "pro" else 1800
    warn_limit = 4000 if args.member == "pro" else 1600

    if not GIF.is_file():
        print(f"GIF missing: {GIF.as_posix()}; fix the package before delivery.", file=sys.stderr)
        return 1

    # DSH / WorkBuddy only preview images inside the workspace; copy next to the chat CWD.
    preview_dir = Path.cwd()
    if ROOT == preview_dir or ROOT in preview_dir.parents:
        preview_dir = args.path.resolve().parent
    try:
        preview_dir.mkdir(parents=True, exist_ok=True)
        preview = preview_dir / "memo-txt-import.gif"
        shutil.copyfile(GIF, preview)
        try:
            image_link = preview.relative_to(Path.cwd()).as_posix()
        except ValueError:
            image_link = preview.as_posix()
    except OSError as exc:
        preview = None
        image_link = GIF.as_posix()
        print(f"GIF preview copy failed: {exc}", file=sys.stderr)

    command = [sys.executable, str(LINT), str(args.path),
               "--char-limit", str(hard_limit), "--warn-limit", str(warn_limit)]
    if args.require_answer_line:
        command.append("--require-answer-line")
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print("LINT FAILED; fix the TXT before delivery:", file=sys.stderr)
        print((result.stdout or result.stderr).strip(), file=sys.stderr)
        return 1
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        report = {}

    chapters = report.get("chapter_count", "?")
    cards = report.get("card_count", "?")
    errors = len(report.get("errors", []))
    warnings = len(report.get("warnings", []))

    print("## 导入教程")
    print()
    print("导入方式（电脑版 Markji）：")
    print("1. 打开制卡桌面，进入目标牌组")
    print("2. 右上角「批量制卡」→「从文本导入」")
    print("3. 粘贴 TXT，保持 ### / === / --- 默认，先看预览，再点「导入」")
    print()
    print(f"![TXT 导入流程]({image_link})")
    print()
    print("平台单卡正文上限：专业版 5000 / 非专业版 2000 字符。")
    print(f"本次按 {args.member} 账号校验：硬上限 {hard_limit} 字符，软提醒 {warn_limit} 字符；单卡最大 {report.get('max_card_length', '?')} 字符。")
    if args.member == "free":
        print("未指定专业版时按非专业版校验；专业版请显式传 --member pro。")
    print("整份牌组的 TXT 导入没有总量限制，可以一次导入。")
    print()
    print(f"结构检查：通过（{chapters} 章 / {cards} 卡，{errors} error {warnings} warning）")
    print()
    print("交付自检：导入教程已附")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
