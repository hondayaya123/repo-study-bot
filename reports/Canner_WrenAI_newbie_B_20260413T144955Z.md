---
target_repo: Canner/WrenAI
level: newbie
goal: B
generated_at: 20260413T144955Z
provider: gemini
model: gemini-2.5-flash-lite
---

# Wren AI 學習指南

Wren AI 是一個開源的生成式商業智慧 (GenBI) 代理，它能讓使用者用自然語言與資料庫互動，並自動生成 SQL 查詢、圖表和商業洞察。其核心特色在於一個語義層 (Semantic Layer)，能確保 AI 生成的結果精確且可信。

本指南旨在幫助您從零開始，逐步掌握 Wren AI 的核心概念、關鍵組件，並具備為專案貢獻的能力。

---

## Phase 1: 專案概覽與環境準備

在開始深入研究程式碼之前，先了解專案的目標、架構以及如何設定開發環境至關重要。

- [ ] **閱讀 `README.md`**: 了解 Wren AI 的整體功能、特色、架構圖以及為何需要語義層。
- [ ] **了解授權條款**: 閱讀 `LICENSE` 文件，了解 Wren AI 使用的開源授權 (GNU Affero General Public License v3)。
- [ ] **熟悉社群規範**: 閱讀 `CODE_OF_CONDUCT.md`，了解社群行為準則。
- [ ] **了解貢獻流程**: 閱讀 `CONTRIBUTING.md`，了解如何貢獻程式碼、提交問題與建立 Pull Request。
- [ ] **探索專案結構**: 瀏覽專案頂層目錄，了解各個主要目錄和檔案的功能：
    - `wren-ai-service`: 核心 AI 服務，負責自然語言處理、SQL 生成等。
    - `wren-ui`: 使用者介面，基於 Next.js 開發。
    - `wren-engine`: 資料庫查詢引擎，負責執行 SQL 並處理語義層。
    - `deployment`: 部署相關的設定，包含 Docker 和 Kubernetes。
    - `docker`: Docker Compose 設定檔，用於快速啟動開發環境。
    - `wren-launcher`: 用於建構和發布的工具。
- [ ] **設定開發環境**: 根據您想貢獻的組件，參考對應的 `README.md` 文件進行環境設定。
    - **Wren AI Service (Python/FastAPI)**: 參考 `wren-ai-service/README.md`，安裝 Python、Poetry、Just，並設定 `.env.dev` 和 `config.yaml`。
    - **Wren UI (Next.js/TypeScript)**: 參考 `wren-ui/README.md`，安裝 Node.js (建議 18 版本) 和 Yarn，並設定資料庫連線。
    - **Wren Engine (Rust)**: 目前 `wren-engine` 是獨立的專案，若要貢獻此部分，請參考其獨立的 README 文件。

---

## Phase 2: 啟動開發環境

在本地運行 Wren AI 的各個組件是理解其運作方式的最佳途徑。

- [ ] **使用 Docker Compose 啟動開發環境**:
    - 導覽至 `docker` 目錄。
    - 複製 `.env.example` 為 `.env`，並填入必要的 API 金鑰 (例如 `OPENAI_API_KEY`)。
    - 複製 `config.example.yaml` 為 `config.yaml`，並根據需求進行修改 (特別是 LLM 設定)。
    - 執行 `docker-compose --env-file .env up -d` 來啟動所有服務 (AI 服務、UI、資料庫等)。
    - 執行 `docker-compose --env-file .env down` 來停止所有服務。
- [ ] **本地運行 Wren UI**:
    - 導覽至 `wren-ui` 目錄。
    - 執行 `yarn` 或 `npm install` 安裝依賴。
    - 執行 `yarn migrate` 或 `npm run migrate` 來運行資料庫遷移 (如果需要)。
    - 執行 `yarn dev` 或 `npm run dev` 來啟動開發伺服器。
    - 在瀏覽器中開啟 `http://localhost:3000`，應能看到 Wren AI 的使用者介面。
- [ ] **本地運行 Wren AI Service**:
    - 導覽至 `wren-ai-service` 目錄。
    - 執行 `just init` 來生成 `.env.dev` 和 `config.yaml`。
    - 設定 `.env.dev` 和 `config.yaml` (參考 `wren-ai-service/docs/configuration.md`)。
    - 執行 `just up` 來啟動必要的容器 (如 Qdrant)。
    - 執行 `just start` 來啟動 AI 服務。
    - API 應可透過 `http://localhost:5556` 訪問 (請根據您的 `.env.dev` 設定調整)。

---

## Phase 3: 核心組件與概念深入

了解各個組件的職責以及它們如何協同工作。

- [ ] **理解 Wren UI (`wren-ui`)**:
    - 探索 `wren-ui/src` 目錄，了解其 Next.js 架構、GraphQL 客戶端 (Apollo)、元件和頁面結構。
    - 了解如何透過 UI 進行語義模型 (MDL) 的定義、資料來源的設定。
    - 參考 `wren-ui/README.md` 中的「切換資料庫」部分，了解如何使用 PostgreSQL 或 SQLite。
- [ ] **理解 Wren AI Service (`wren-ai-service`)**:
    - 閱讀 `wren-ai-service/docs/configuration.md`，了解如何配置 LLM 模型、嵌入模型 (Embedder) 和向量資料庫 (Document Store)。
    - 了解其核心流程：接收使用者問題 -> 意圖分類 -> 向量檢索 (RAG) -> LLM 提示工程 -> SQL 生成 -> SQL 校驗。
    - 參考 `wren-ai-service/eval/README.md`，了解評估框架和指標。
- [ ] **理解 Wren Engine (`wren-engine`)**:
    - 雖然 `wren-engine` 是獨立專案，但了解其在 Wren AI 架構中的角色很重要。它負責解析語義模型 (MDL)，將 LLM 生成的 SQL 轉換為可在各種資料來源上執行的查詢計劃。
    - 參考 `README.md` 中的架構圖，了解 Wren Engine 如何接收 SQL 並與資料庫互動。
- [ ] **理解語義層 (MDL)**:
    - 閱讀 `README.md` 中關於「為什麼需要語義層」的說明。
    - 了解 MDL 如何定義資料庫結構、指標 (metrics) 和關聯 (joins)，以確保 LLM 生成的 SQL 準確無誤。
    - 雖然 MDL 的具體格式不在這個倉庫中，但理解其概念是關鍵。

---

## Phase 4: 貢獻與進階學習

在熟悉基本操作後，您可以開始為專案做出貢獻。

- [ ] **閱讀貢獻指南**: 再次仔細閱讀 `CONTRIBUTING.md`，特別是關於如何為不同服務 (UI, AI Service, Engine) 貢獻的章節。
- [ ] **尋找可貢獻的議題**: 瀏覽 GitHub Issues，尋找標記為 `good first issue` 或與您感興趣的領域相關的議題。
- [ ] **建立 Pull Request**:
    - 遵循 `CONTRIBUTING.md` 和 `wren-ai-service/CONTRIBUTING.md` 中的指示，建立包含程式碼變更的 Pull Request。
    - 確保 PR 標題符合規範 (例如 `feat(wren-ai-service): ...`)。
    - 連結相關的 Issue。
- [ ] **學習新增資料來源**:
    - 如果您想為 Wren AI 添加對新資料來源的支援，請閱讀 `CONTRIBUTING.md` 中關於「建立新的資料來源連接器」的說明。
    - 這通常需要修改 `wren-engine` (獨立專案) 和 `wren-ui`。
- [ ] **了解部署策略**:
    - 閱讀 `deployment/README.md` 和 `deployment/kustomizations/README.md`，了解如何使用 Docker 或 Kubernetes 部署 Wren AI。
- [ ] **探索 CI/CD 設定**:
    - 查看 `.github/workflows` 目錄下的 YAML 文件，了解專案的自動化測試、建構和發布流程。

---

## 資源列表

以下是本專案中重要的文件和連結，供您參考：

- **專案主頁**: [README.md](README.md)
- **貢獻指南**: [CONTRIBUTING.md](CONTRIBUTING.md)
- **社群規範**: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **授權條款**: [LICENSE](LICENSE)
- **Wren AI Service 文件**:
    - [README.md](wren-ai-service/README.md)
    - [設定指南](wren-ai-service/docs/configuration.md)
    - [貢獻指南](wren-ai-service/CONTRIBUTING.md)
    - [評估框架](wren-ai-service/eval/README.md)
- **Wren UI 文件**:
    - [README.md](wren-ui/README.md)
- **Docker 啟動指南**: [docker/README.md](docker/README.md)
- **Kubernetes 部署指南**: [deployment/kustomizations/README.md](deployment/kustomizations/README.md)
- **Wren Engine 專案**: [Canner/wren-engine](https://github.com/Canner/wren-engine) (獨立專案，需額外參考其文件)
- **官方文件站**: [docs.getwren.ai](https://docs.getwren.ai/)
- **社群 Discord**: [Discord 邀請連結](https://discord.gg/5DvshJqG8Z)