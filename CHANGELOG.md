# 变更记录

遵循语义化版本：修 bug → patch，新增能力 → minor，改变契约 → major。

## v1.3.12 — 2026-10-30

影响面：memo-txtimporter(README.md, references/satellites.md)

### 变更

- Memo 系列清单加入「卡跳跳 Memo-CardLink」，同步 README 系列表与 satellites。

## v1.3.11 — 2026-10-30

影响面：memo-txtimporter(README.md)

### 变更

- README 顶部增加「墨卡大师 · 专业制卡工作流」在线介绍页链接。

## v1.3.10 — 2026-10-28

影响面：memo-txtimporter(references/satellite-framework.md)

### 变更

- 文档中的发布器名称由 `skill-publisher` 更新为 `maimemo-publisher`，与当前技能名保持一致。

## v1.3.9 — 2026-10-26

影响面：memo-txtimporter(SKILL.md, scripts/import_guide.py, scripts/finalize_txt.py)

### 修复

- 导入教程与交付尾注改为把 GIF 复制到工作区并使用相对路径，修复客户端无法预览技能目录图片的问题。
- 新增 `scripts/import_guide.py` 供纯问答使用；`finalize_txt.py` 同步复制预览图。

## v1.3.8 — 2026-10-26

影响面：memo-txtimporter(SKILL.md, scripts/check_updates.py, scripts/test_check_updates.py) / memo-cardest(scripts/check_updates.py, scripts/test_check_updates.py)

### 修复

- 更新器与 cardest 对齐：状态锁竞争返回 `busy`，不再误报 `state_lock_failed`；锁获取带 2 秒退避重试，加锁前不读取被锁字节。

## v1.3.7 — 2026-10-25

影响面：memo-txtimporter(SKILL.md, scripts/finalize_txt.py) / memo-cardest(SKILL.md, references/txt-workflow.md)

### 修复

- 交付教程必须按普通 Markdown 粘贴，禁止用代码块包住；否则 GIF 只会显示成文字。`finalize_txt.py` 在 stderr 增加对应提示。

## v1.3.6 — 2026-10-25

影响面：memo-txtimporter(SKILL.md, scripts/finalize_txt.py) / memo-cardest(SKILL.md)

### 变更

- 新增 `scripts/finalize_txt.py`：先跑 `lint_txt.py`，通过后输出四步教程、GIF 绝对路径、5000 / 无总量限制说明和 `交付自检：导入教程已附`；校验失败退出 1。
- 交付规则改为必须原样附 `finalize_txt.py` 输出；删除 `scripts/import_guide.py`。

## v1.3.5 — 2026-10-25

影响面：memo-txtimporter(SKILL.md, scripts/import_guide.py)

### 修复

- 交付教程改为强制运行 `scripts/import_guide.py` 并贴出动图，不再只给文字步骤或 `import-guide.md` 链接。

## v1.3.4 — 2026-10-25

影响面：memo-txtimporter(SKILL.md, references/import-guide.md, references/import-guide.html)

### 修复

- 修正导入上限说明：单张卡片正文上限为 5000 字符，整份牌组的 TXT 导入没有总量限制；删除“单次粘贴 2000 字符、长文件分批”的错误说法。

## v1.3.3 — 2026-10-25

影响面：memo-txtimporter(SKILL.md, README.md, references/import-guide.md, references/import-guide.html, references/assets/import-menu-36b59d.gif, references/assets/import-dialog-36b59d.png, references/assets/import-flow-36b59d.gif)

### 新增

- 交付 TXT 时**自动附四步导入教程**，不等用户问；教程注明 2000 字符上限与“不代操作导入”。
- 新增「把 TXT 导入墨墨记忆卡」图文指南：四步操作、步骤截图与 GIF、导入前检查；SKILL.md 与 README 增加入口。
- 补充导入弹窗截图与填写要点：简单/专业模式、保持 `###` / `===` / `---` 默认、先看预览、2000 字符上限。
- 指南以文字为主、HTML 为离线辅助；截图裁掉了账号区域，只指示按钮位置。

## v1.3.2 — 2026-10-24

### 修复

- 图片回填幂等改为按资产判断（标记消失且本资产 `file.id` 存在），修复同卡第二张图被跳过。
- 回填验收改为「基线 + 仅替换标记行」的逐字符比较；写入响应的 content 不再冒充回读，需另发 GET。
- 补「TXT + 自动回填需要 API 凭证与单独授权」的前置说明，修正「直角/圆角」和「版本源未配置」的过期描述。
- 作为 cardest 支链在同一任务中调用时跳过自身 S0；更新器支持 `.git` 文件（worktree）。

## v1.3.1 — 2026-10-24

### 变更

- 新增 MIT `LICENSE`，README 补 License 说明。

## v1.3.0 — 2026-10-23

### 变更

- 支链更新框架升级到与墨卡大师同一代：启动同步、更新前核验远端/分支/目标版本，只做 fast-forward；非 git 安装、脏工作区、远端不符都会跳过并给出原因。
- 支链清单从 2 个补齐到 5 个（cardest、mineruocr、table、ankitransfer、qahelper），安装来源改为 GitHub 公开仓库，并接入已核验的 `version.json`。
- 移除过时的 `platform_marketplace` 配置与「去平台技能市场查找」说法，与 README 的 GitHub 分发一致。
- README 的「Memo 系列」表与 `references/satellites.md` 改由 `memo-series.json` 生成（`sync-series`）。

## v1.3.1 — 2026-10-24

### 变更

- 新增 MIT `LICENSE`，README 补 License 说明。

## v1.2.1 — 2026-10-19

### 变更

- 文档术语更新：发布器名称由 Memo-Publisher 改为 `skill-publisher`，与当前发布流程一致。

## v1.3.1 — 2026-10-24

### 变更

- 新增 MIT `LICENSE`，README 补 License 说明。

## v1.2.0 — 2026-10-16

- TXT 导入后用官方 OpenAPI 回填表格与配图。

