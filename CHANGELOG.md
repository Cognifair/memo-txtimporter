# 变更记录

遵循语义化版本：修 bug → patch，新增能力 → minor，改变契约 → major。

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

