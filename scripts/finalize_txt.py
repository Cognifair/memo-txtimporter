#!/usr/bin/env python3
"""Validate a TXT file and print the mandatory delivery block (tutorial + GIF + self-check)."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINT = Path(__file__).with_name("lint_txt.py")
GIF = ROOT / "references" / "assets" / "import-flow-36b59d.gif"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="TXT file to validate")
    parser.add_argument("--require-answer-line", action="store_true",
                        help="Require exactly one answer line per card")
    args = parser.parse_args()

    if not GIF.is_file():
        print(f"GIF missing: {GIF.as_posix()}; fix the package before delivery.", file=sys.stderr)
        return 1

    command = [sys.executable, str(LINT), str(args.path)]
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
    print(f"![TXT 导入流程]({GIF.as_posix()})")
    print()
    print("单张卡片正文上限 5000 字符；整份牌组的 TXT 导入没有总量限制，可以一次导入。")
    print()
    print(f"结构检查：通过（{chapters} 章 / {cards} 卡，{errors} error {warnings} warning）")
    print()
    print("交付自检：导入教程已附")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
