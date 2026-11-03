import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parent / "lint_txt.py"
SPEC = importlib.util.spec_from_file_location("lint_txt", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def txt(card_body):
    return "牌组名称：测试\n牌组简介：\n\n### 第一章\n" + card_body + "\n===\n"


class LimitTests(unittest.TestCase):
    def test_utf16_length_counts_emoji_as_two_units(self):
        self.assertEqual(MODULE.utf16_length("a😀"), 3)

    def test_card_over_hard_limit_is_an_error(self):
        result = MODULE.lint_text(txt("正面\n---\n" + "答" * 20), char_limit=10)
        self.assertFalse(result["ok"])
        self.assertTrue(any(item["code"] == "card_too_long" for item in result["errors"]))

    def test_card_over_soft_limit_is_a_warning(self):
        result = MODULE.lint_text(txt("正面\n---\n" + "答" * 20), char_limit=100, warn_limit=10)
        self.assertTrue(result["ok"])
        self.assertTrue(any(item["code"] == "card_near_limit" for item in result["warnings"]))

    def test_max_card_length_is_reported(self):
        result = MODULE.lint_text(txt("正面\n---\n短答案"), char_limit=100, warn_limit=50)
        self.assertGreater(result["max_card_length"], 0)
        self.assertEqual(result["char_limit"], 100)


if __name__ == "__main__":
    unittest.main()
