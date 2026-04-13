---
target_repo: Canner/WrenAI
level: mid
goal: A
generated_at: 20260413T150610Z
provider: gemini
model: gemini-2.5-flash-lite
---

# Wren AI 學習指南

Wren AI 是一個開源的 GenBI (生成式商業智能) 代理，它能讓使用者用自然語言向資料庫提問，並自動生成精確的 SQL、圖表和商業洞察。其核心特色在於一個語意層 (Semantic Layer)，確保 LLM 生成的查詢結果能準確反映業務定義，避免歧義。

本指南旨在幫助您全面掌握 Wren AI 的各個層面，從架構、內部機制、開發流程、測試策略到部署與維護。

## 第一階段：入門與環境設定

此階段的目標是讓您對 Wren AI 的整體架構有初步認識，並成功搭建本地開發環境。

- [ ] **閱讀 `README.md`**：
    - [ ] 了解 Wren AI 的核心功能與價值主張。
    - [ ] 熟悉其支援的資料來源與 LLM 模型。
    - [ ] 概覽專案的架構圖，理解各組件的職責。
    - [ ] 檢視「開發者」部分，了解各服務 (UI, AI Service, Engine) 的技術棧。
- [ ] **理解授權條款**：
    - [ ] 閱讀 `LICENSE` 文件，了解專案採用的 GNU Affero General Public License v3 (AGPL-3.0) 授權條款。
- [ ] **熟悉貢獻流程**：
    - [ ] 閱讀 `CONTRIBUTING.md`，了解貢獻的整體流程、行為準則及各服務的貢獻指南。
    - [ ] 了解如何參與討論、報告問題或提交 PR。
- [ ] **設定本地開發環境**：
    - [ ] **Wren AI Service (Python/FastAPI)**：
        - [ ] 確認已安裝 Python 3.12+。建議使用 `pyenv` 管理 Python 版本。
        - [ ] 安裝 Poetry (版本 1.8.3)。
        - [ ] 安裝 Just 命令執行器 (版本 1.36+)。
        - [ ] 複製 `.env.example` 至 `.env.dev` 並設定 `OPENAI_API_KEY` 等必要環境變數。
        - [ ] 複製 `config.example.yaml` 至 `config.yaml`，並根據需求進行調整（參考 `wren-ai-service/docs/configuration.md`）。
        - [ ] 執行 `just init` 初始化設定檔。
        - [ ] 執行 `poetry install` 安裝依賴。
        - [ ] (可選) 安裝 pre-commit hooks (`poetry run pre-commit install`) 以確保程式碼品質。
        - [ ] 執行 `just up` 啟動必要的 Docker 服務 (如 Qdrant)。
        - [ ] 執行 `just start` 啟動 Wren AI Service。
        - [ ] 透過 `http://localhost:5556` (預設) 訪問 API 文件。
    - [ ] **Wren UI (Next.js/TypeScript)**：
        - [ ] 確認已安裝 Node.js 版本 18。
        - [ ] 執行 `yarn` (或 `npm install`) 安裝依賴。
        - [ ] (可選) 設定資料庫類型為 PostgreSQL (`export DB_TYPE=pg` 和 `export PG_URL=...`) 或保留預設 SQLite。
        - [ ] 執行 `yarn migrate` (或 `npm run migrate`) 執行資料庫遷移。
        - [ ] 執行 `yarn dev` (或 `npm run dev`) 啟動開發伺服器。
        - [ ] 透過 `http://localhost:3000` (預設) 訪問 UI。
    - [ ] **Wren Engine (Rust)**：
        - [ ] 檢閱 `wren-engine` 專案的 README，了解其建置與執行方式。
        - [ ] 根據 `CONTRIBUTING.md` 中的指示，若有需要，可自行建置或執行 Wren Engine。通常，`docker-compose` 會處理啟動。
- [ ] **理解 Docker Compose 設定**：
    - [ ] 檢閱 `docker/README.md`，了解如何使用 `docker-compose` 啟動所有服務。
    - [ ] 熟悉 `docker/docker-compose-dev.yaml`，了解各服務的映像檔、網路和卷掛載設定。
    - [ ] 嘗試執行 `docker-compose --env-file .env.local up -d` 啟動所有服務。

## 第二階段：深入理解架構與核心組件

此階段將深入探討 Wren AI 的各個核心組件及其交互方式。

- [ ] **Wren UI (Frontend & Backend)**：
    - [ ] 檢閱 `wren-ui/README.md`，了解其開發流程與設定。
    - [ ] 探索 `wren-ui/src/apollo/server` 目錄，理解其 GraphQL API 和後端邏輯。
    - [ ] 了解 UI 如何處理使用者輸入、與 AI Service 溝通以及顯示結果。
    - [ ] 檢閱 `wren-ui/src/components` 目錄，熟悉 UI 組件結構。
- [ ] **Wren AI Service (Python Backend)**：
    - [ ] 深入閱讀 `wren-ai-service/README.md` 和 `wren-ai-service/CONTRIBUTING.md`。
    - [ ] 檢閱 `wren-ai-service/docs/configuration.md`，理解 `config.yaml` 的結構與參數，特別是 LLM、Embedder 和 Document Store 的配置。
    - [ ] 探索 `wren-ai-service/pipelines` 目錄，理解 RAG (Retrieval-Augmented Generation) 和 SQL 生成的流程。
    - [ ] 了解 `wren-ai-service/eval` 目錄下的評估框架，包括資料集準備、預測與評估流程。
    - [ ] 檢閱 `wren-ai-service/tools` 目錄，了解輔助工具。
- [ ] **Wren Engine (Rust Backend)**：
    - [ ] 檢閱 `wren-engine` 專案的 README (若有提供，或從 Wren AI 的 README 連結進入)。
    - [ ] 理解 Wren Engine 作為查詢執行核心的角色，以及它如何解析 MDL (Model Definition Language) 並與資料庫互動。
    - [ ] 了解其與 Apache DataFusion 的整合。
    - [ ] 檢閱 `wren-launcher/commands/dbt/README.md`，了解如何將 dbt 模型轉換為 Wren Engine 可用的格式。
- [ ] **語意層 (MDL)**：
    - [ ] 閱讀 `README.md` 中關於語意層的說明，理解其重要性。
    - [ ] 探索 `wren-ui/src/apollo/server/dataSource.ts` 和相關檔案，了解語意模型 (MDL) 的定義與儲存方式。
    - [ ] 理解 MDL 如何定義 Schema、Metrics 和 Joins，以確保 LLM 輸出的準確性。
- [ ] **資料來源連接器**：
    - [ ] 檢閱 `CONTRIBUTING.md` 中關於新增資料來源連接器的說明。
    - [ ] 了解 Wren Engine 如何支援多種資料來源 (BigQuery, Snowflake, PostgreSQL 等)。
    - [ ] 檢閱 `wren-launcher/commands/dbt/README.md`，了解如何為新的資料來源實作 `DataSource` 介面並整合。

## 第三階段：測試、部署與維護

此階段將專注於專案的測試策略、部署方式以及如何進行維護和貢獻。

- [ ] **測試策略**：
    - [ ] 檢閱 `.github/workflows/ai-service-test.yaml`，了解 AI Service 的單元測試流程。
    - [ ] 檢閱 `.github/workflows/ui-test.yaml`，了解 Wren UI 的單元測試流程。
    - [ ] 檢閱 `wren-ui/e2e/README.md`，了解端對端 (E2E) 測試的設定與執行方式。
    - [ ] 檢閱 `wren-ai-service/eval/README.md`，了解評估框架的指標與使用方式。
- [ ] **部署**：
    - [ ] 閱讀 `deployment/README.md`，了解支援的部署策略 (Docker, Kubernetes)。
    - [ ] **Docker 部署**：
        - [ ] 參考 `docker/README.md`，了解如何使用 `docker-compose` 部署生產環境。
        - [ ] 熟悉 `.env.example` 和 `config.yaml` 在生產環境中的配置。
    - [ ] **Kubernetes 部署**：
        - [ ] 閱讀 `deployment/kustomizations/README.md`，了解使用 Kustomize 部署到 Kubernetes 的步驟。
        - [ ] 熟悉 `deployment/kustomizations/examples` 目錄下的範例檔案，特別是 Secret (`secret-wren_example.yaml`) 和 Ingress (`wrenai-ingress-example.yaml`) 的配置。
        - [ ] 了解如何處理 TLS 憑證 (`certificate-wren_example.yaml`)。
        - [ ] 了解如何配置 PostgreSQL 作為 Wren UI 的資料庫。
- [ ] **CI/CD 與自動化**：
    - [ ] 檢閱 `.github/workflows` 目錄下的各個 GitHub Actions 工作流程檔案：
        - [ ] `ai-service-release-image.yaml`, `ai-service-release-nightly-image.yaml`, `ai-service-release-stable-image.yaml`：了解 AI Service Docker 映像檔的建置與發佈流程。
        - [ ] `ui-release-image.yaml`, `ui-release-image-stable.yaml`：了解 Wren UI Docker 映像檔的建置與發佈流程。
        - [ ] `wren-launcher-ci.yaml`：了解 Wren Launcher 的 CI 流程 (Lint, Test, Security Scan)。
        - [ ] `pr-tagger.yaml`：了解 PR 標籤自動化流程。
        - [ ] `pull-request-title-validator.yaml`：了解 PR 標題驗證。
        - [ ] `create-rc-release-pr.yaml`, `create-rc-release.yaml`：了解 RC 版本發佈的自動化流程。
- [ ] **程式碼貢獻**：
    - [ ] 回顧 `CONTRIBUTING.md`，了解如何提交 Pull Request。
    - [ ] 熟悉 PR 標題的命名規範 (如 `feat(wren-ai-service): ...`)。
    - [ ] 了解如何處理合併衝突。
    - [ ] 參與 Discord 社群或 GitHub Issues，與團隊及其他貢獻者交流。

## 第四階段：進階主題與深入探索

此階段鼓勵您探索更進階的主題，並為專案做出貢獻。

- [ ] **擴展性與客製化**：
    - [ ] 閱讀 `wren-ai-service/CONTRIBUTING.md` 中關於新增客製化 LLM、Embedder 或 Document Store 的說明。
    - [ ] 思考如何為新的資料來源新增連接器 (參考 `CONTRIBUTING.md` 和 `wren-launcher/commands/dbt/README.md`)。
    - [ ] 探索 `wren-engine` 的架構，了解如何擴展其支援的資料來源或查詢功能。
- [ ] **效能優化**：
    - [ ] 檢閱 `wren-ai-service/README.md` 中的「Estimate the Speed of the Pipeline」部分，了解如何進行負載測試。
    - [ ] 關注 `wren-engine` 的效能表現，特別是查詢計畫的生成與執行。
- [ ] **安全性**：
    - [ ] 檢閱 `SECURITY.md` (若存在)。
    - [ ] 了解部署時的 Secret 管理 (如 Kubernetes 中的 Secrets)。
    - [ ] 關注 CI 中的安全掃描 (如 `wren-launcher-ci.yaml` 中的 Gosec)。
- [ ] **參與社群**：
    - [ ] 加入 Wren AI 的 Discord 社群，與開發者和使用者交流。
    - [ ] 在 GitHub Issues 中提出問題、功能請求或參與討論。
    - [ ] 關注專案的公開路線圖。

## 資源列表

以下是 Wren AI 專案中的關鍵檔案與連結，便於您快速查找：

- **專案主頁與說明**：
    - `README.md`: 專案總覽、架構、功能介紹與快速入門。
    - [Docs.getwren.ai](https://docs.getwren.ai): 官方文件站。
- **貢獻指南**：
    - `CONTRIBUTING.md`: 貢獻流程、行為準則與各服務貢獻細節。
    - `CODE_OF_CONDUCT.md`: 社群行為準則。
- **核心組件**：
    - `wren-ui/README.md`: Wren UI 開發與設定。
    - `wren-ai-service/README.md`: Wren AI Service 開發與設定。
    - `wren-ai-service/docs/configuration.md`: AI Service 組態詳細說明。
    - `wren-engine` (獨立專案，請參考其 GitHub 頁面)：Rust 核心引擎。
- **部署**：
    - `docker/README.md`: Docker Compose 部署指南。
    - `deployment/kustomizations/README.md`: Kubernetes Kustomize 部署指南。
- **CI/CD 與測試**：
    - `.github/workflows/`: 存放所有 GitHub Actions 工作流程。
    - `wren-ui/e2e/README.md`: UI 端對端測試指南。
    - `wren-ai-service/eval/README.md`: AI Service 評估框架指南。
- **授權**：
    - `LICENSE`: GNU Affero General Public License v3。
- **社群**：
    - [Discord 連結](https://discord.gg/5DvshJqG8Z)
    - [GitHub Issues](https://github.com/Canner/WrenAI/issues)
    - [公開路線圖](https://wrenai.notion.site/)