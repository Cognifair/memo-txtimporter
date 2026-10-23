# 变更记录

遵循语义化版本：修 bug → patch，新增能力 → minor，改变契约 → major。

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
