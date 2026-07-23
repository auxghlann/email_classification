# Agent Rules & Context

Welcome to this project! This file serves as the workspace customization root for all AI agents working on the Email Classification codebase.

## Absolute Source of Truth
**CRITICAL**: You must refer to the `spec/` directory for the definitive truth regarding this project's requirements and architecture. Do not guess or hallucinate features; read the specs first.
- For product goals and feature requirements, read `spec/prd.md`.
- For system design and the technology stack, read `spec/architecture.md`.
- For historical context and major engineering decisions, read `spec/decisions.md`.

Always align your proposed implementation plans and code changes with the documents in the `spec/` directory before writing code.

## Tech Stack & Architecture
- **Language**: Python 3.13+
- **Framework**: FastAPI (Structured under `app/api/v1/`)
- **Machine Learning**: `scikit-learn`, `pandas`, `numpy`
- **Model Artifacts**: Pre-trained `.pkl` files stored in `pkl_files/` (`spam_model.pkl`, `feature_names.pkl`)
- **Package & Dependency Management**: `uv` (`pyproject.toml` & `uv.lock`)

## Core Directives
1. **Dependency Management**: Always use `uv add <package>` (or `uv add --dev <package>`) when introducing new python dependencies so `pyproject.toml` and `uv.lock` stay synchronized.
2. **ML Artifact Loading**: Safely load pre-trained models from `pkl_files/` during application startup or request context; avoid online model re-training during API requests.
3. **API Validation**: Use Pydantic schemas for FastAPI request and response models.
4. **Terminal Commands**: Use PowerShell when suggesting or executing shell commands on Windows.
5. **Type Safety & Modularity**: Write clean, modular Python code with type annotations and concise docstrings.
6. **No Emojis**: Strictly avoid adding emojis in code, docstrings, or markdown documentation.
7. **Security**: Never commit secrets, `.env` files, API keys, or hardcoded authentication tokens.
