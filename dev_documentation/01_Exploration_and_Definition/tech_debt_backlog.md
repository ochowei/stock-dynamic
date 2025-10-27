# 技術/架構 積壓
(2025-10-27 更新)

## 導入 Linting (Ruff)
* **Topics**: `#workflow` `#code-quality`
* **Status**: `#in-progress`
* **問題**: 目前沒有一致的程式碼風格，且潛在的錯誤只能在執行階段發現。
* **假設**: 導入 Ruff 作為 Linter 和 Formatter，並在 CI 流程中強制執行，可以顯著提升程式碼品質與開發效率。
* **預計迭代**: `v1.2` (進行中)

## 導入 CI/CD
* **Topics**: `#workflow` `#ai-tools`
* **Status**: `#idea`
* **問題**: 目前都是手動測試，推送 (push) `main` 分支時沒有保障。
* **假設**: 導入 GitHub Actions 自動執行 Lint (Ruff) 和 Test (Pytest) 能大幅提高程式碼品質。
* **預計迭代**: `v1.2`

## 升級為 Monorepo
* **Topics**: `#system-design` `#workflow`
* **Status**: `#idea`
* **問題**: 未來若要加入 Node.js 前端，目前架構難以管理。
* **預計迭代**: `v1.4`