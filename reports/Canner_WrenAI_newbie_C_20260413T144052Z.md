---
target_repo: Canner/WrenAI
level: newbie
goal: C
generated_at: 20260413T144052Z
provider: gemini
model: gemini-2.5-flash-lite
---

# Wren AI 開源專案學習指南

Wren AI 是一個開源的 GenBI (Generative Business Intelligence) 代理，旨在讓使用者能夠以自然語言與資料庫互動，並快速生成 SQL 查詢、圖表和商業洞察。它透過一個語義層 (Semantic Layer) 來確保 LLM (大型語言模型) 生成的結果是準確且可信的。

本指南旨在幫助您快速入門 Wren AI，包含專案的基礎認識、本地環境設定，以及如何為專案做出貢獻。

## 第一階段：專案概覽與初步認識

在本階段，您將了解 Wren AI 的核心功能、架構以及它解決的問題。

- [ ] **閱讀 `README.md` 文件**：
    - [ ] 了解 Wren AI 的核心價值：以自然語言與資料互動，生成 SQL、圖表和 BI 洞察。
    - [ ] 認識「語義層 (Semantic Layer)」的重要性，它如何確保 LLM 生成的 SQL 準確無誤。
    - [ ] 瀏覽「功能 (Features)」章節，了解其主要特色，例如：與資料對話、GenBI 洞察、語義層、透過 API 嵌入等。
    - [ ] 了解 Wren AI 支援的「資料來源 (Data Sources)」和「LLM 模型 (LLM Models)」。
    - [ ] 快速瀏覽「架構 (Architecture)」圖，了解使用者問題如何從 UI 流向 AI 服務、Wren Engine，最終到達資料庫。
    - [ ] 了解「開發者 (For Developers)」部分，認識專案的技術堆疊（Next.js, Python/FastAPI, Rust）。
- [ ] **了解專案授權**：
    - [ ] 閱讀 `LICENSE` 文件，了解 Wren AI 使用的是 GNU Affero General Public License v3.0。

## 第二階段：本地環境設定

本階段將引導您在本地電腦上設定 Wren AI 的開發環境，以便您可以運行專案並進行測試。

- [ ] **確認系統需求**：
    - [ ] 確保您的電腦已安裝 Docker。
    - [ ] 根據 `wren-ai-service/README.md`，確認已安裝 Python 3.12.*。
    - [ ] 根據 `wren-ai-service/README.md`，確認已安裝 Poetry (版本 1.8.3)。
    - [ ] 根據 `wren-ai-service/README.md`，確認已安裝 Just 命令執行器 (版本 1.36 或更高)。
    - [ ] 根據 `wren-ui/README.md`，確認您的 Node.js 版本為 18。
- [ ] **設定 Docker 環境**：
    - [ ] 導覽至專案根目錄下的 `docker` 資料夾。
    - [ ] 複製 `.env.example` 檔案為 `.env`。
    - [ ] **重要：** 編輯 `.env` 檔案，填入您的 OpenAI API 金鑰（或您選擇的其他 LLM 提供者金鑰）。
    - [ ] 複製 `config.example.yaml` 檔案為 `config.yaml`。
    - [ ] 啟動所有必要的 Docker 服務：在 `docker` 資料夾下執行 `docker-compose --env-file .env up -d`。
- [ ] **設定 Wren AI Service (Python)**：
    - [ ] 導覽至 `wren-ai-service` 資料夾。
    - [ ] 安裝 Poetry 依賴：執行 `poetry install`。
    - [ ] 初始化設定檔：執行 `just init`。這會生成 `.env.dev` 和 `config.yaml`。
    - [ ] （可選）安裝 pre-commit hooks 以確保程式碼品質：執行 `poetry run pre-commit install`。
    - [ ] 啟動 Wren AI Service：執行 `just start`。
- [ ] **設定 Wren UI (Next.js)**：
    - [ ] 導覽至 `wren-ui` 資料夾。
    - [ ] 安裝 Node.js 依賴：執行 `yarn install`。
    - [ ] （可選）若要使用 PostgreSQL 作為 Wren UI 的資料庫，請設定 `DB_TYPE=pg` 和 `PG_URL` 環境變數。預設使用 SQLite。
    - [ ] 執行資料庫遷移：執行 `yarn migrate`。
    - [ ] **重要：** 確保您的 `wren-ai-service` 正在運行，並且 `wren-ui` 可以訪問它。如果 `wren-ai-service` 是透過 Docker 運行，可能需要設定 `OTHER_SERVICE_USING_DOCKER=true` 環境變數。
    - [ ] 啟動 Wren UI 開發伺服器：執行 `yarn dev`。
- [ ] **驗證本地運行**：
    - [ ] 在瀏覽器中打開 `http://localhost:3000`，應能看到 Wren UI 的介面。
    - [ ] 嘗試連接一個資料來源（您可能需要在 UI 中設定資料庫連接資訊）。
    - [ ] 在 UI 中輸入一個簡單的自然語言問題，觀察是否能成功生成 SQL。

## 第三階段：程式碼結構與貢獻入門

在本階段，您將了解專案的主要程式碼結構，並學習如何為專案做出貢獻。

- [ ] **了解專案架構與模組**：
    - [ ] **`wren-ui`**: 前端介面，使用 Next.js 開發。負責語義模型 UI 和連接後端的 BFF (Backend For Frontend)。
    - [ ] **`wren-ai-service`**: 後端 AI 服務，使用 Python/FastAPI 開發。負責意圖分類、向量檢索、LLM 提示和 SQL 校正循環。
    - [ ] **`wren-engine`**: 核心查詢引擎，使用 Rust 開發。負責解析語義層定義 (MDL)，並跨多個資料來源執行查詢。
    - [ ] **`docker`**: 包含 Docker Compose 設定檔，用於啟動和管理所有服務。
    - [ ] **`deployment`**: 包含部署相關的設定，例如 Kubernetes 的 Kustomizations。
    - [ ] **`wren-launcher`**: 一個 Go 程式，可能用於啟動或管理其他服務。
- [ ] **閱讀貢獻指南**：
    - [ ] 仔細閱讀根目錄下的 `CONTRIBUTING.md` 文件。
    - [ ] 了解貢獻流程：開 issue、提交 Pull Request (PR)。
    - [ ] 閱讀各服務的貢獻指南（例如 `wren-ai-service/CONTRIBUTING.md`），了解特定服務的貢獻細節。
- [ ] **尋找貢獻機會**：
    - [ ] 查看 GitHub Issues 頁面，尋找標記為 "good first issue" 或與您感興趣的領域相關的 issue。
    - [ ] 考慮為專案添加新的資料來源連接器（這通常需要修改 `wren-engine` 和 `wren-ui`）。
    - [ ] 嘗試改進 LLM 的提示工程，以提高 SQL 生成的品質。
    - [ ] 協助測試和回報 Bug。
- [ ] **提交您的第一個貢獻**：
    - [ ] **Fork** 本專案到您的 GitHub 帳戶。
    - [ ] 在您的 fork 中建立一個新的分支來進行開發。
    - [ ] 根據 `CONTRIBUTING.md` 中的指示，進行程式碼修改。
    - [ ] 確保您的程式碼通過所有測試和 CI 檢查（參考 `.github/workflows/` 目錄下的 CI 設定檔）。
    - [ ] 提交一個 Pull Request (PR) 到主專案。
    - [ ] 在 PR 描述中清楚說明您的變更內容，並連結相關的 issue。

## 第四階段：進階探索 (可選)

在您熟悉基本操作後，可以進一步探索專案的更多功能和細節。

- [ ] **了解語義層 (MDL)**：
    - [ ] 探索 `wren-ui` 中與語義模型定義相關的程式碼，了解如何定義資料表、欄位、指標和關聯。
- [ ] **研究 AI 服務的 pipeline**：
    - [ ] 閱讀 `wren-ai-service/docs/configuration.md`，了解如何配置不同的 LLM、Embedder 和 Document Store。
    - [ ] 探索 `wren-ai-service/eval/README.md`，了解如何進行評估和測試。
- [ ] **深入了解 Wren Engine**：
    - [ ] 如果您對 Rust 或資料庫查詢引擎感興趣，可以研究 `wren-engine` 專案（雖然它是一個獨立的專案，但與 Wren AI 緊密相關）。
- [ ] **部署選項**：
    - [ ] 閱讀 `deployment/README.md`，了解不同的部署策略，例如 Docker 和 Kubernetes。

## 資源連結

以下是一些關鍵的檔案和連結，方便您快速查閱：

- **專案主頁**: [README.md](README.md)
- **貢獻指南**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **行為準則**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **授權條款**: [LICENSE](LICENSE)
- **Docker 設定**: [docker/README.md](docker/README.md)
- **Wren AI Service 文件**: [wren-ai-service/README.md](wren-ai-service/README.md)
- **Wren UI 文件**: [wren-ui/README.md](wren-ui/README.md)
- **Wren Engine 專案**: [Canner/wren-engine](https://github.com/Canner/wren-engine) (外部連結)
- **官方文件**: [docs.getwren.ai](https://docs.getwren.ai/) (外部連結)
- **Discord 社群**: [Discord 邀請連結](https://discord.gg/5DvshJqG8Z) (外部連結)