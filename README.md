# 墨记文档导入 Memo-Txtimporter

专注墨墨记忆卡（Markji）TXT 导入文档的文件容器格式：把已有卡片正文按牌组和章节组织为可交付的 UTF-8 TXT，并检查章节、分卡符与答案线。

调用名：`$memo-txtimporter`。版本以 [SKILL.md](SKILL.md) 的 `metadata.version` 和 [version.json](version.json) 为准。

## 核心格式

| 标记 | 含义 |
|---|---|
| `牌组名称：`、`牌组简介：` | 文件开头的牌组信息，简介可为空 |
| `### 章节名` | 独占一行，指定后续卡片所属章节 |
| `===` | 独占一行，分隔不同卡片 |
| `---` | 独占一行，同一卡片的题面与答案分界 |

空行只用于排版，不负责分卡。默认沿用样本在最后一张卡片后保留 `===`；其后的空白不算新卡。

以下是说明结构的纯文本示例；生成的 TXT 文件本身不含 Markdown 代码围栏：

```text
牌组名称：格式演示
牌组简介：两张简单问答卡

### 基础知识
水的化学式是什么？
---
H2O
===
常压下水的凝固点是多少？
---
0 ℃
===
```

完整规范与边界见 [references/container-format.md](references/container-format.md)。

## 能做什么

- 将现成的卡片正文、题面与答案列表、章节映射组织成导入文档。
- 保留原有正文标签、公式、选项与媒体引用，仅修改用户要求的文件结构。
- 统计牌组、章节、每章卡数、分卡符与答案线，报告问题及行号。
- 请求修复时默认另存新文件，避免覆盖原件。

## 使用示例

> 使用 $memo-txtimporter，把这些已有卡片按指定章节整理成 TXT，并检查分卡和答案线，不改动正文语法。

仅整理已有正文时不询问会员状态、不索取凭证、不访问账户。如果还需要从原始学习材料设计新卡，交由 [墨卡大师 Memo-Cardest](https://github.com/Cognifair/memo-cardest) 处理内容层；表格渲染属于可选 Memo-Table 技能。

## 结构校验

Python 3 标准库即可运行，检查器只读，不修改输入文件：

```text
python -B scripts/lint_txt.py path/to/cards.txt
python -B scripts/lint_txt.py path/to/cards.txt --require-answer-line
python -B scripts/test_check_updates.py
```

常规问答每卡恰有一条答案线时可加 `--require-answer-line`；特殊题型应结合报告中的警告判断。检查器不验证卡片内部标签语法、知识正确性或客户端显示。

## 使用边界与更新框架

文件格式来自经整理的用户样本，不代表所有客户端版本都已验证。交付后仍需使用者先少量试导入；不自动上传、不操作客户端、不保证覆盖原卡或保留旧 ID、链接和学习进度。

附带本地可选扩展识别与授权后只读版本检查。自动检查默认关闭，远端版本源尚未配置，不会下载或执行远端代码。详见 [references/satellite-framework.md](references/satellite-framework.md) 和 [references/satellites.md](references/satellites.md)。

