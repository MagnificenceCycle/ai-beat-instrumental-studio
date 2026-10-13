# Security Policy

## Reporting

Email `security@ai-beat-instrumental-studio.dev` with a description, repro,
and the plugin/extension id if applicable. We aim to acknowledge within 72h.

## Scope

- The host process (`src/beatstudio/host/`).
- The plugin loader (`src/beatstudio/plugins/loader.py`).
- Shared contracts (`src/beatstudio/contracts/`).

Out of scope: third-party plugin binaries, model weights pulled by
`tools/fetch_models.py`, and anything under `runs/` or `renders/`.

## Threat model notes

Plugins execute in-process. The loader enforces an allowlist from
`config/plugins.toml` and refuses unsigned extensions when
`[loader].require_signature = true`. Do not disable this on shared machines.