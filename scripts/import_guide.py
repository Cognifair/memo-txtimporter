#!/usr/bin/env python3
"""Print the TXT import tutorial; copy the GIF into the current workspace for preview."""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GIF = ROOT / "references" / "assets" / "import-flow-36b59d.gif"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if not GIF.is_file():
        print(f"GIF missing: {GIF.as_posix()}", file=sys.stderr)
        return 1
    try:
        preview = Path.cwd() / "memo-txt-import.gif"
        shutil.copyfile(GIF, preview)
        link = preview.name
    except OSError as exc:
        print(f"GIF preview copy failed: {exc}", file=sys.stderr)
        link = GIF.as_posix()

    print("## 导入教程")
    print()
    print("导入方式（电脑版 Markji）：")
    print("1. 打开制卡桌面，进入目标牌组")
    print("2. 右上角「批量制卡」→「从文本导入」")
    print("3. 粘贴 TXT，保持 ### / === / --- 默认，先看预览，再点「导入」")
    print()
    print(f"![TXT 导入流程]({link})")
    print()
    print("单张卡片正文上限 5000 字符；整份牌组的 TXT 导入没有总量限制，可以一次导入。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
