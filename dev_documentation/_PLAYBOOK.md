彈性 SDL 開發手冊 (Playbook)這是一份統整的開發手冊，說明了 documentation 資料夾的完整結構、工作流程、以及所有關鍵文件的範例。第一部分：核心理念本計畫的核心是將 documentation 資料夾分為「當前工作區」和「歷史歸檔區」，使其兼具進度追蹤的即時性與未來回溯的彈性。我們承認開發工作不只一種，並將其分為三類，彈性調整各階段的產出物：類型 A：功能迭代 (Feature Iteration)目標：開發新功能 (e.g., trailing_stop 策略)。規格：BDD (.feature 檔)。驗證：TDD (pytest)。類型 B：技術迭代 (Technical Iteration)目標：改善專案體質 (e.g., CI/CD, Linting, Monorepo 重構)。規格：技術設計文件 (.md 檔) 與「驗收檢查表」。驗證：手動檢查表驗證 (e.g., 檢查 CI 是否通過)。類型 C：複雜迭代 (Complex Iteration)目標：開發大型、跨系統功能 (e.g., Frontend 整合)。規格：流程圖 + E2E 規格 (.feature 檔)。驗證：E2E 測試 (Cypress/Playwright) + 元件測試 + 手動測試。第二部分：documentation 資料夾結構此結構完全獨立於您的程式碼 (src/, tests/)，確保了最大的彈性。documentation/
│
├── _PLAYBOOK.md         # (本文件) 您的最高指導原則
│
├── README.md            # 【儀表板】永遠追蹤「當前」迭代的進度與時間
│
├── PROJECT_WORKFLOW.md    # (可選) 將第三部分獨立出來的SOP
│
├── 01_Exploration_and_Definition/
│   # 【工作區】存放「所有」的想法、研究、痛點
│   ├── README.md
│   ├── strategy_ideas.md
│   └── tech_debt_backlog.md
│
├── 02_Specification_Workshop/
│   # 【工作區】存放「當前正在開發」的 .feature 規格
│   ├── README.md
│   ├── (範例).feature
│   └── (範例).md
│
├── 03_Build_and_Verify/
│   # 【工作區】存放「當前正在開發」的實作日誌
│   ├── README.md
│   └── (範例)_impl.md
│
├── 04_Review_and_Deliver/
│   # 【工作區】存放「當前即將發布」的版本說明草稿
│   ├── README.md
│   └── Release_Notes_WIP.md
│
├── 05_Operate_and_Iterate/
│   # 【工作區】存放「近期」具代表性的分析報告
│   ├── README.md
│   └── (範例)_report.txt
│
└── _archive/
    # 【歸檔區】存放所有「已完成並發布」的版本產出物
    │
    ├── README.md
    │
    └── v1.0/
        ├── 02_fixed_lag.feature
        ├── 03_fixed_lag_impl.md
        ├── 04_Release_Notes_v1.0.md
        └── 05_summary_report_v1.0_final.txt
第三部分：專案工作流程 (SOP)這份文件說明如何使用此 documentation 資料夾來管理一個迭代 (Iteration)。A. 迭代開始 (Start of Iteration)決定目標: 從 01_Exploration/ 的積壓 (backlog) 中，決定本次迭代的主要目標 (e.g., "v1.1: 實作移動停利" 或 "v1.2: 建立 CI/CD")。重設儀表板:打開 documentation/README.md (儀表板)。清除所有舊的「開始/結束時間」。填寫「當前迭代」、「迭代目標」和「迭代類型」。開始工作: 在 README.md 填上「階段一：開始時間」，然後進入 01_.../ 開始工作。B. 執行五階段 (Execute the 5 Stages)您將依序填寫 README.md 上的起訖時間，並在對應資料夾中產出文件：階段一 (Explore):產出: 在 01_Exploration/ 中撰寫或更新您的想法文件 (e.g., strategy_ideas.md)。階段二 (Specify):產出: 根據「迭代類型」，在 02_Specification/ 建立對應的規格文件：類型 A (功能): 建立 .feature 檔 (e.g., trailing_stop.feature)。類型 B (技術): 建立 .md 規格 (e.g., cicd_spec.md)。類型 C (複雜): 建立 .md 流程圖 + .feature E2E 規格。階段三 (Build & Verify):產出: 根據「迭代類型」，在 03_Build_and_Verify/ 建立對應的實作日誌：類型 A (功能): 建立 _impl.md，記錄 TDD/BDD 過程。類型 B (技術): 建立 _impl.md，記錄手動檢查表和試誤過程 (e.g., cicd_impl.md)。類型 C (複雜): 建立 _impl.md，記錄 E2E 測試和元件測試過程。(執行): 在 src/, tests/, .github/ 等資料夾中實際撰寫程式碼。階段四 (Review):產出: 進入 04_Review_and_Deliver/，撰寫 Release_Notes_WIP.md。務必包含「新功能」和「技術變更」兩個區塊，以總結所有類型的工作。階段五 (Operate):產出: 進入 05_Operate_and_Iterate/，存放一份「證明」。類型 A: 存放一份有代表性的 summary_report_...txt。類型 B: 存放一張 CI 成功運作的截圖或 Log，或 lint 通過的 Log。類型 C: 存放 E2E 測試報告。C. 迭代結束 (End of Iteration)歸檔 (Archive):在 _archive/ 建立一個新資料夾 (e.g., v1.1/)。將「工作區」 (02~05) 中所有與此迭代相關的最終產出物，「移動」到 _archive/v1.1/ 中。(可選) 在 01_Exploration/ 的文件中，將對應項目的狀態改為 archived 或 done。清空工作區: 您的 02~05 資料夾（工作區）現在又變乾淨了。發布 (Release): (建議) 在 GitHub 上建立一個 v1.1 的 Tag，並將 _archive/v1.1/04_Release_Notes_v1.1.md 的內容複製上去。重複: 回到 README.md 儀表板，準備開始 v1.2 的開發。第四部分：儀表板與各階段文件範本儀表板 (documentation/README.md)目的：作為「當前迭代」的中央儀表板，追蹤五個階段的起訖時間。範本 (Template)：# SDL 迭代追蹤儀表板
(更新時間：YYYY-MM-DD HH:MM AM/PM)

- **當前迭代**: `vX.X`
- **迭代目標**: [填入本次迭代的主要目標]
- **迭代類型**: [請選擇：功能迭代 / 技術迭代 / 複雜迭代]
  <!--
    - 功能迭代 (類型 A): 開發新功能 (e.g., 策略)
    - 技術迭代 (類型 B): 改善專案體質 (e.g., CI/CD, 重構)
    - 複雜迭代 (類型 C): 跨系統功能 (e.g., 前端)
  -->

---

### 階段一：探索與定義
- `開始時間`: `YYYY-MM-DD HH:MM`
- `結束時間`: `YYYY-MM-DD HH:MM`

### 階段二：規格化工作坊
- `開始時間`: `YYYY-MM-DD HH:MM`
- `結束時間`: `YYYY-MM-DD HH:MM`

### 階段三：建構與驗證
- `開始時間`: `YYYY-MM-DD HH:MM`
- `結束時間`: `YYYY-MM-DD HH:MM`

### 階段四：審查與交付
- `開始時間`: `YYYY-MM-DD HH:MM`
- `結束時間`: `YYYY-MM-DD HH:MM`

### 階段五：營運與迭代
- `開始時間`: `YYYY-MM-DD HH:MM`
- `結束時間`: `YYYY-MM-DD HH:MM`
階段一：探索與定義 (01_Exploration_and_Definition/)目的：此資料夾是專案的「想法積壓 (Idea Backlog)」，用於捕捉「為何做」與「做什麼」。這裡的檔案是持續性的，會不斷更新，而不是在每個迭代結束時被歸檔。範本 1：strategy_ideas.md (功能型想法)# 策略點子庫
(YYYY-MM-DD 更新)

## 移動停利 (Trailing Stop)
* **Topics**: `#quant-trading`
* **Status**: `#idea`
* **問題**: 如何在股價上漲時鎖定利潤，又避免太早賣出？
* **假設**: 設定一個距離歷史高點 5% 的回撤點作為賣出訊號，應可提高獲利。
* **預計迭代**: `v1.1` (已歸檔)
範本 2：tech_debt_backlog.md (技術型想法)# 技術/架構 積壓
(YYYY-MM-DD 更新)

## 導入 CI/CD
* **Topics**: `#workflow` `#ai-tools`
* **Status**: `#idea`
* **問題**: 目前都是手動測試，推送 (push) `main` 分支時沒有保障。
* **假設**: 導入 GitHub Actions 自動執行 Lint (Ruff) 和 Test (Pytest) 能大幅提高程式碼品質。
* **預計迭代**: `v1.2` (進行中)

## 升級為 Monorepo
* **Topics**: `#system-design` `#workflow`
* **Status**: `#idea`
* **問題**: 未來若要加入 Node.js 前端，目前架構難以管理。
* **預計迭代**: `v1.4`
階段二：規格化工作坊 (02_Specification_Workshop/)目的：此資料夾是「當前工作區」，用於存放當前迭代的「規格文件」。這些文件將在迭代結束時被移動到 _archive/ 中。範本 A (功能)：trailing_stop.featureFeature: 移動停利策略
  為了在回測中鎖定利潤
  作為一個量化分析師
  我想要在股價自高點回撤一定比例時執行賣出

Scenario: 股價觸發 5% 停利點
  Given 我的持股成本為 100 元
  And 股價最高漲到 120 元
  When 股價下跌到 114 元
  Then 系統應發出賣出訊號
範本 B (技術)：cicd_spec.md# 規格文件：CI/CD (v1.2)

## 1. 觸發條件
- `push` 到 `main` 分支時
- `pull_request` 到 `main` 分支時

## 2. 驗收標準 (Acceptance Criteria)
- [ ] 建立一個 PR 時，CI 必須被觸發。
- [ ] 故意提交一個 Lint 錯誤的 PR，CI 必須顯示為「紅色失敗」。
- [ ] 故意提交一個 Test 錯誤的 PR，CI 必須顯示為「紅色失敗」。
- [ ] 提交一個全對的 PR，CI 必須顯示為「綠色通過」。
範本 C (複雜)：frontend_design.md# 規格文件：前端回測儀表板 (v1.5)

## 1. 使用者流程 (User Flow)
1.  使用者進入 `/dashboard` 頁面。
2.  點擊「上傳報告」按鈕。
3.  選擇 `summary_report_...txt` 檔案。
4.  上傳成功後，頁面上的「總回報圖表」應自動更新。

## 2. E2E 規格 (Gherkin for Cypress/Playwright)
Feature: 圖表視覺化
Scenario: 使用者上傳回測報告
  Given 我在前端儀表板頁面 ("/dashboard")
  When 我上傳 "summary_report_v1.0.txt"
  Then 我應該在圖表區 (`#chart-wrapper`) 看到一張折線圖
階段三：建構與驗證 (03_Build_and_Verify/)目的：此資料夾是「當前工作區」，用於存放當前迭代的「實作日誌」。這份日誌記錄了如何達成階段二的規格。這些文件將在迭代結束時被移動到 _archive/ 中。範本 A (功能)：trailing_stop_impl.md# 實作日誌：移動停利 (v1.1)

- **規格文件**: `../02_Specification_Workshop/trailing_stop.feature`
- **主要程式碼**: `src/stock_analysis/core.py`
- **測試程式碼**: `tests/test_core.py`

---
## 狀態檢查表
- [x] TDD 單元測試
- [x] 程式碼實作
- [x] 手動測試 (run.py)

---
## 開發筆記
- `2025-10-20`: 
  - (TDD-Red) 撰寫 `test_trailing_stop_should_sell`，測試失敗。
  - (TDD-Green) 撰寫 `analyze_trailing_stop` 函式。
  - 測試通過，功能完成。
範本 B (技術)：cicd_impl.md# 實作日誌：CI/CD (v1.2)

- **規格文件**: `../02_Specification/cicd_spec.md`
- **主要程式碼**: `.github/workflows/main.yml`
- **相關分支**: `feature/cicd`

---
## 驗證日誌 (Trial & Error)

- `2025-10-27 11:55 AM`:
  - **動作**: 建立 `.yml` 並 PUSH (`commit: a1b2c3d`)
  - **結果**: 失敗 (Action 未觸發)。
  - **原因**: `.yml` 檔案路徑錯誤。

- `2025-10-27 12:15 PM`:
  - **動作**: 修正路徑 PUSH (`commit: e4f5g6h`)
  - **結果**: Lint Job 失敗。

- `2025-10-27 13:20 PM`:
  - **動作**: 修正 PUSH (`commit: m0n1p2q`)
  - **結果**: **全部通過**。
  - **結論**: 已滿足 `cicd_spec.md` 中的所有驗收標準。
階段四：審查與交付 (04_Review_and_Deliver/)目的：此資料夾是「當前工作區」，用於存放當前迭代的「版本說明 (Release Notes)」草稿。這份文件將在迭代結束時被重新命名並移動到 _archive/ 中。範本：Release_Notes_WIP.md# 版本 vX.X (草稿)

## ✨ 新功能 (New Features)
- (e.g., 移動停利策略)

## 🚀 技術與架構 (Technical & Architecture)
- (e.g., 導入 CI/CD)

## 🐞 錯誤修復 (Bug Fixes)
- (無)
階段五：營運與迭代 (05_Operate_and_Iterate/)目的：此資料夾是「當前工作區」，用於存放當前迭代的「最終產出證明」。這份文件將在迭代結束時被移動到 _archive/ 中。(範本)：(類型 A): 一份 summary_report_v1.1_TSLA_5pct.txt 報告。(類型 B): 一張 ci_pass_screenshot.png 截圖或 lint_log.txt。歸檔區 (_archive/)目的：此資料夾是唯讀的歷史紀錄區。工作流程：當一個迭代 (e.g., v1.1) 在儀表板上顯示所有五個階段都已完成時，執行歸檔動作：在此處建立一個新資料夾 (e.g., v1.1/)。將「工作區」 (02~05) 中所有與 v1.1 相關的最終產出物，「移動」到 _archive/v1.1/ 中。重新命名 04_Review_and_Deliver/Release_Notes_WIP.md 為 _archive/v1.1/04_Release_Notes_v1.1.md。(範例結構)：_archive/
    │
    └── v1.0/ (已歸檔)
        ├── 02_fixed_lag.feature
        ├── 03_fixed_lag_impl.md
        ├── 04_Release_Notes_v1.0.md
        └── 05_summary_report_v1.0_final.txt
    │
    └── v1.1/ (已歸檔)
        ├── 02_trailing_stop.feature
        ├── 03_trailing_stop_impl.md
        ├── 04_Release_Notes_v1.1.md
        └── 05_summary_report_TSLA_5pct.txt
    │
    └── v1.2/ (剛剛歸檔的)
        ├── 02_cicd_spec.md
        ├── 03_cicd_impl.md
        ├── 04_Release_Notes_v1.2.md
        └── 05_ci_pass_screenshot.png
