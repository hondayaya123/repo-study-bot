"""
Repo Learning Guide Generator
Fetches context from a target GitHub repo and generates a markdown checklist
learning guide using GitHub Models (OpenAI-compatible API).
"""

import base64
import json
import os
import re
import sys
import datetime
from pathlib import Path

import requests
from openai import OpenAI

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
TARGET_REPO = os.environ["TARGET_REPO"]       # owner/repo
LEVEL = os.environ.get("LEVEL", "newbie")     # newbie | junior | mid
GOAL = os.environ.get("GOAL", "C")            # A | B | C
MAX_FILES = int(os.environ.get("MAX_FILES", "80"))
MAX_FILE_BYTES = int(os.environ.get("MAX_FILE_BYTES", "200000"))

MODEL = os.environ.get("MODEL_ID") or os.environ.get("MODEL") or "CHANGE_ME"

GITHUB_API = "https://api.github.com"
GITHUB_MODELS_BASE = "https://models.inference.ai.azure.com"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# Files / patterns to always try fetching (exact paths first, then patterns)
PRIORITY_GLOBS = [
    # Root-level docs
    "README.md", "README.rst", "README.txt", "README",
    "CONTRIBUTING.md", "CONTRIBUTING.rst", "CONTRIBUTING",
    "LICENSE", "LICENSE.md", "LICENSE.txt",
    "CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.rst",
    # Dependency / build files
    "package.json", "pnpm-lock.yaml", "yarn.lock",
    "requirements.txt", "pyproject.toml", "poetry.lock",
    "go.mod", "Cargo.toml", "pom.xml", "build.gradle",
    "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
]

DIRECTORY_PATTERNS = [
    "docs",
    ".github/workflows",
]


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def api_get(url: str, params: dict | None = None) -> dict | list | None:
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def get_file_content(owner: str, repo: str, path: str) -> str | None:
    """Return decoded text content of a file, or None if unavailable / too large."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    data = api_get(url)
    if not data or isinstance(data, list):
        return None
    size = data.get("size", 0)
    if size > MAX_FILE_BYTES:
        return f"[File too large: {size} bytes — skipped]"
    try:
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except Exception:
        return None


def list_tree(owner: str, repo: str, sha: str = "HEAD") -> list[dict]:
    """Return the full git tree (flat) for the repo."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/git/trees/{sha}"
    data = api_get(url, params={"recursive": "1"})
    if not data:
        return []
    return data.get("tree", [])


def get_default_branch(owner: str, repo: str) -> str:
    data = api_get(f"{GITHUB_API}/repos/{owner}/{repo}")
    if data:
        return data.get("default_branch", "main")
    return "main"


# ---------------------------------------------------------------------------
# Context assembly
# ---------------------------------------------------------------------------

def collect_context(owner: str, repo: str) -> str:
    """Fetch repo files and return a single context string."""
    files_collected: list[tuple[str, str]] = []   # (path, content)
    collected_paths: set[str] = set()
    file_count = 0

    print(f"Fetching tree for {owner}/{repo} …", flush=True)
    branch = get_default_branch(owner, repo)
    tree = list_tree(owner, repo, branch)
    blob_paths = {item["path"] for item in tree if item["type"] == "blob"}

    # Top-level directory listing
    top_level = sorted({p.split("/")[0] for p in blob_paths})
    dir_listing = "## Top-level directory / file listing\n" + "\n".join(top_level)
    files_collected.append(("_directory_listing_", dir_listing))

    def fetch_and_add(path: str) -> bool:
        nonlocal file_count
        if file_count >= MAX_FILES:
            return False
        if path not in blob_paths:
            return False
        if path in collected_paths:
            return False
        content = get_file_content(owner, repo, path)
        if content is None:
            return False
        files_collected.append((path, content))
        collected_paths.add(path)
        file_count += 1
        print(f"  + {path} ({len(content)} chars)", flush=True)
        return True

    # 1. Priority files (exact names)
    for fname in PRIORITY_GLOBS:
        fetch_and_add(fname)

    # 2. README* / CONTRIBUTING* / CODE_OF_CONDUCT* by pattern
    for path in sorted(blob_paths):
        name = path.split("/")[-1].upper()
        if (
            name.startswith("README")
            or name.startswith("CONTRIBUTING")
            or name.startswith("CODE_OF_CONDUCT")
        ) and path not in collected_paths:
            fetch_and_add(path)

    # 3. docs/** and .github/workflows/**
    for prefix in DIRECTORY_PATTERNS:
        for path in sorted(blob_paths):
            if path.startswith(prefix + "/") or path == prefix:
                fetch_and_add(path)
                if file_count >= MAX_FILES:
                    break

    # 4. docker-compose*.yml anywhere at root level
    for path in sorted(blob_paths):
        base = path.split("/")[-1]
        if "/" not in path and re.match(r"docker-compose.*\.(yml|yaml)$", base, re.I):
            fetch_and_add(path)

    # Assemble bundle
    parts = [f"# Context bundle for {owner}/{repo}\n"]
    for path, content in files_collected:
        parts.append(f"\n---\n## File: {path}\n\n```\n{content}\n```\n")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

GOAL_DESCRIPTIONS = {
    "A": (
        "comprehensive mastery — the learner wants to deeply understand every layer "
        "of the project (architecture, internals, contribution workflow, testing strategy, "
        "deployment, and how to extend or maintain the codebase)."
    ),
    "B": (
        "solid working knowledge — the learner wants to understand the core concepts, "
        "key components, and how to contribute meaningfully to the project."
    ),
    "C": (
        "quick-start overview — the learner wants to set up the project locally, "
        "understand what it does at a high level, and make small contributions."
    ),
}

LEVEL_DESCRIPTIONS = {
    "newbie": "a complete beginner with little or no programming experience",
    "junior": "a junior developer with basic programming skills but new to this tech stack",
    "mid": "a mid-level developer comfortable with software engineering but new to this project",
}


def build_prompt(context: str, owner: str, repo: str) -> str:
    goal_desc = GOAL_DESCRIPTIONS.get(GOAL, GOAL_DESCRIPTIONS["C"])
    level_desc = LEVEL_DESCRIPTIONS.get(LEVEL, LEVEL_DESCRIPTIONS["newbie"])

    system = (
        "You are an expert software educator. Your task is to generate a structured, "
        "actionable learning guide for a GitHub repository. "
        "The guide must be a Markdown document with numbered checklist items using '- [ ]' syntax. "
        "Organise items into clear sections. Be specific — reference actual files, commands, "
        "concepts, and components found in the context. Avoid generic advice."
        "Output MUST be in Traditional Chinese (繁體中文, Taiwan style)."
    )

    user = f"""You are generating a learning guide for the repository **{owner}/{repo}**.

**Learner profile:** {level_desc}
**Learning goal:** {goal_desc}

Use the repository context below to produce a Markdown checklist learning guide.

Guidelines:
- Start with a short (2–3 sentence) description of what the project does.
- Organise the guide into logical phases/sections (e.g. "Phase 1 – Orientation", "Phase 2 – Local Setup", etc.).
- Each phase should contain specific, actionable checklist items using `- [ ]` syntax.
- Reference real file names, commands, URLs, and concepts from the context.
- Tailor depth and terminology to the learner profile.
- End with a "Resources" section listing key files and links from the repo.
- The entire document must be Traditional Chinese (繁體中文).
- Use Markdown checklists (- [ ]) for all actionable items.

--- REPOSITORY CONTEXT START ---
{context}
--- REPOSITORY CONTEXT END ---

Now write the complete Markdown learning guide:
"""
    return system, user


# ---------------------------------------------------------------------------
# Call GitHub Models
# ---------------------------------------------------------------------------

def call_github_models(system: str, user: str) -> str:
    client = OpenAI(
        base_url=GITHUB_MODELS_BASE,
        api_key=GITHUB_TOKEN,
    )
    print(f"Calling GitHub Models ({MODEL}) …", flush=True)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
        max_tokens=4096,
    )
    return response.choices[0].message.content


def list_available_models() -> None:
    """Fetch and print available models from GitHub Models, then exit 0."""
    url = f"{GITHUB_MODELS_BASE}/models"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    print("Available models:")
    if isinstance(data, list):
        for item in data:
            model_id = item.get("id") or item.get("name") or str(item)
            print(f"  {model_id}")
    else:
        print(json.dumps(data, indent=2))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if os.environ.get("LIST_MODELS") == "1":
        list_available_models()
        sys.exit(0)

    if not MODEL or MODEL == "CHANGE_ME":
        print(
            "ERROR: No model configured. Set the MODEL_ID input (or MODEL env var) "
            "to a valid GitHub Models model id from "
            "https://models.inference.ai.azure.com/models",
            file=sys.stderr,
        )
        sys.exit(1)

    if "/" not in TARGET_REPO:
        print("ERROR: TARGET_REPO must be in 'owner/repo' format.", file=sys.stderr)
        sys.exit(1)

    owner, repo = TARGET_REPO.split("/", 1)

    print(f"=== Repo Learning Guide Generator ===")
    print(f"Target:    {owner}/{repo}")
    print(f"Level:     {LEVEL}")
    print(f"Goal:      {GOAL}")
    print(f"Max files: {MAX_FILES}  Max file bytes: {MAX_FILE_BYTES}")
    print()

    # Fetch context
    context = collect_context(owner, repo)
    print(f"\nContext bundle size: {len(context)} chars\n", flush=True)

    # Build prompt
    system, user = build_prompt(context, owner, repo)

    # Call model
    guide_md = call_github_models(system, user)

    # Write output
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)

    safe_repo = TARGET_REPO.replace("/", "_")
    timestamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{safe_repo}_{LEVEL}_{GOAL}_{timestamp}.md"
    out_path = reports_dir / filename

    header = (
        f"---\n"
        f"target_repo: {TARGET_REPO}\n"
        f"level: {LEVEL}\n"
        f"goal: {GOAL}\n"
        f"generated_at: {timestamp}\n"
        f"model: {MODEL}\n"
        f"---\n\n"
    )

    out_path.write_text(header + guide_md, encoding="utf-8")
    print(f"\nReport written to: {out_path}", flush=True)


if __name__ == "__main__":
    main()
