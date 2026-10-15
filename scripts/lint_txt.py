#!/usr/bin/env python3
"""Read-only linter for the user's Markji TXT container, not card syntax."""

import argparse
import json
from pathlib import Path
import re
import sys


def lint_text(text, require_answer_line=False):
    result = {
        "ok": False,
        "scope": "sample-based TXT structure only; no card-syntax or client validation",
        "deck_name": None,
        "chapters": [],
        "card_count": 0,
        "separator_count": 0,
        "answer_line_count": 0,
        "errors": [],
        "warnings": [],
    }
    current = None
    pending = []
    metadata_seen = set()

    def issue(level, line, code, message):
        result[level].append({"line": line, "code": code, "message": message})

    def nonempty():
        return any(value.strip() for _, value in pending)

    def finish_card():
        if not nonempty():
            pending.clear()
            return
        first_line = next(number for number, value in pending if value.strip())
        answers = [index for index, (_, value) in enumerate(pending) if value == "---"]
        result["card_count"] += 1
        result["answer_line_count"] += len(answers)
        if current is None:
            issue("errors", first_line, "missing_chapter", "Card has no preceding ### chapter.")
        else:
            current["card_count"] += 1
        if len(answers) != 1:
            level = "errors" if require_answer_line else "warnings"
            issue(level, first_line, "answer_line_count",
                  f"Card has {len(answers)} answer lines; review special type or missing separator.")
        else:
            split = answers[0]
            if not any(value.strip() for _, value in pending[:split]):
                issue("errors", first_line, "empty_front", "Question side is empty.")
            if not any(value.strip() for _, value in pending[split + 1:]):
                issue("errors", pending[split][0], "empty_back", "Answer side is empty.")
        pending.clear()

    if text.startswith("\ufeff"):
        text = text[1:]
        issue("warnings", 1, "utf8_bom", "UTF-8 BOM accepted; prefer no BOM for new files.")
    if "\x00" in text:
        issue("errors", 1, "nul_byte", "NUL characters found; check input encoding.")
    lines = text.splitlines()
    for number, value in enumerate(lines, start=1):
        stripped = value.strip()
        if stripped in {"===", "---"} and value != stripped:
            issue("errors", number, "padded_control_line", "Control line has surrounding whitespace.")
        if value.lstrip().startswith("```"):
            issue("warnings", number, "code_fence", "Review code fence; do not wrap the TXT in Markdown.")
        if value.startswith("###") and not value.startswith("####"):
            match = re.fullmatch(r"### (\S.*)", value)
            if not match or not match.group(1).strip():
                issue("errors", number, "invalid_chapter", "Expected ### followed by a space and chapter name.")
                continue
            if nonempty():
                issue("errors", number, "missing_separator", "Chapter changed before previous card ended with ===.")
                finish_card()
            if current is not None and current["card_count"] == 0:
                issue("warnings", current["line"], "empty_chapter", "Chapter has no cards.")
            current = {"name": match.group(1), "line": number, "card_count": 0}
            result["chapters"].append(current)
            pending.clear()
            continue
        if re.match(r"^\s+###(?: |$)", value):
            issue("errors", number, "indented_chapter", "Chapter marker must not be indented.")
        if value == "===":
            result["separator_count"] += 1
            if not nonempty():
                issue("errors", number, "empty_card", "Separator follows no nonempty card body.")
            finish_card()
            continue
        if current is None and result["card_count"] == 0 and not nonempty():
            if not stripped:
                continue
            key = next((key for key in ("牌组名称", "牌组简介") if value.startswith(key + "：")), None)
            if key:
                if key in metadata_seen:
                    issue("errors", number, "duplicate_metadata", "Metadata field occurs more than once.")
                metadata_seen.add(key)
                if key == "牌组名称":
                    result["deck_name"] = value.split("：", 1)[1].strip()
                    if not result["deck_name"]:
                        issue("errors", number, "empty_deck_name", "Deck name must not be empty.")
                continue
        pending.append((number, value))

    if nonempty():
        issue("warnings", len(lines), "missing_final_separator", "Final nonempty card lacks sample-style trailing ===.")
        finish_card()
    if current is not None and current["card_count"] == 0:
        issue("warnings", current["line"], "empty_chapter", "Chapter has no cards.")
    for key in ("牌组名称", "牌组简介"):
        if key not in metadata_seen:
            issue("errors", 1, "missing_metadata", f"Missing {key}： before first chapter.")
    if not result["card_count"]:
        issue("errors", 1, "no_cards", "No nonempty card blocks found.")
    result["chapter_count"] = len(result["chapters"])
    result["ok"] = not result["errors"]
    return result


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--require-answer-line", action="store_true",
                        help="Treat anything except one answer line per card as an error.")
    args = parser.parse_args()
    try:
        text = args.path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        return 2
    result = lint_text(text, args.require_answer_line)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
