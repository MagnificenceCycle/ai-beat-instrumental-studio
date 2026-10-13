# Contributing to ai-beat-instrumental-studio

Thanks for wanting to poke the host. This repo is a plugin-host for AI beat
generation: the core host loads generator/effect extensions, the registry
resolves them, and the pipeline renders instrumental stems to disk.

## Dev loop

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev,cpu]"
pytest
beat-studio plugins list
```

## Adding a generator plugin

1. Drop a module under `src/beatstudio/plugins/`.
2. Subclass `GeneratorPlugin` from `beatstudio.contracts.generator`.
3. Decorate with `@register_plugin("your-name")`.
4. Add a smoke test under `tests/`.

Plugins must not import from `beatstudio.services.*` at module scope — the
loader imports plugins before services are wired. Use the `HostContext` passed
into `setup()` instead.

## Style

- `ruff` for lint, `mypy` for types, 100-col lines.
- No global state in plugins; everything flows through `HostContext`.
- Every render path must be deterministic given the same seed.