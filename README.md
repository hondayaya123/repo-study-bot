# repo-study-bot

A GitHub Actions workflow that automatically generates a structured Markdown learning guide for any public GitHub repository using an LLM.

## Supported Providers

### Gemini (Google AI Studio) — default
Uses `GEMINI_API_KEY` to call Google Gemini models (e.g. `gemini-2.5-flash`).

**Setup:**
1. Get a free API key at [Google AI Studio](https://aistudio.google.com/app/apikey).
2. In your fork of this repo go to **Settings → Secrets and variables → Actions → New repository secret**.
3. Name: `GEMINI_API_KEY`, Value: your key.

### GitHub Models
Uses `GITHUB_TOKEN` (automatically provided) and a model from [GitHub Models](https://models.inference.ai.azure.com/models).

## Running the Workflow

1. Go to **Actions → Generate Repo Learning Guide → Run workflow**.
2. Fill in the inputs:

| Input | Description | Default |
|-------|-------------|---------|
| `target_repo` | Repository to analyse (`owner/repo`) | *(required)* |
| `level` | Learner level: `newbie`, `junior`, `mid` | `newbie` |
| `goal` | Depth: `A` (comprehensive), `B` (core), `C` (quick start) | `C` |
| `provider` | `gemini` or `github_models` | `gemini` |
| `gemini_model` | Gemini model id | `gemini-2.5-flash` |
| `max_context_chars` | Max total chars sent to model (prevents quota errors) | `800000` |
| `max_file_chars` | Max chars per file included in context | `50000` |
| `max_files` | Max files fetched from target repo | `80` |
| `max_file_bytes` | Max bytes per file from GitHub API | `200000` |
| `model_id` | GitHub Models model id (only for `github_models` provider) | `CHANGE_ME` |

3. The generated Markdown guide is committed to `reports/` and uploaded as a workflow artifact.
