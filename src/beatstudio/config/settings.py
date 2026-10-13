"""HostSettings — pydantic-validated view of config/default.toml + plugins.toml."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib

from beatstudio.plugins.registry import PluginSpec

DEFAULT_CONFIG = Path("config/default.toml")
DEFAULT_PLUGINS = Path("config/plugins.toml")


@dataclass(slots=True)
class LoaderSettings:
    plugin_paths: list[str] = field(default_factory=list)
    require_signature: bool = False
    allowlist: list[str] = field(default_factory=list)
    disabled: list[str] = field(default_factory=list)


@dataclass(slots=True)
class HostSettings:
    name: str
    sample_rate: int
    buffer_frames: int
    render_dir: Path
    run_dir: Path
    default_bpm: int
    default_key: str
    swing: float
    stem_format: str
    bit_depth: int
    normalize_lufs: float
    loader: LoaderSettings
    plugin_specs: list[PluginSpec]


def load_settings(config_path: Path | None = None,
                  plugins_path: Path | None = None) -> HostSettings:
    cfg_path = config_path or DEFAULT_CONFIG
    plg_path = plugins_path or DEFAULT_PLUGINS
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    plg = tomllib.loads(plg_path.read_text(encoding="utf-8")) if