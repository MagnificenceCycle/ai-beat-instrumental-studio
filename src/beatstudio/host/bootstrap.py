"""HostBootstrap — wires config, loader, registry, and pipeline into one object."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from beatstudio.config.settings import HostSettings, load_settings
from beatstudio.host.context import HostContext
from beatstudio.host.pipeline import RenderPipeline
from beatstudio.plugins.registry import PluginRegistry
from beatstudio.services.audio_engine import AudioEngine
from beatstudio.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class HostBootstrap:
    """Top-level composition root. Owns the registry and pipeline."""

    settings: HostSettings
    registry: PluginRegistry
    pipeline: RenderPipeline
    context: HostContext

    @classmethod
    def from_config(cls, config_path: Path | None = None) -> "HostBootstrap":
        settings = load_settings(config_path)
        engine = AudioEngine(sample_rate=settings.sample_rate, buffer=settings.buffer_frames)
        registry = PluginRegistry(settings=settings, engine=engine)
        registry.load_all()
        context = HostContext(settings=settings, engine=engine, registry=registry)
        pipeline = RenderPipeline(context=context)
        log.info("host booted", extra={"plugins": len(registry.specs())})
        return cls(settings=settings, registry=registry, pipeline=pipeline, context=context)

    def render(self, *, prompt: str, bpm: int, bars: int, seed: int, out: Path) -> Path:
        out.parent.mkdir(parents=True, exist_ok=True)
        return self.pipeline.run(prompt=prompt, bpm=bpm, bars=bars, seed=seed, out=out)

    def close(self) -> None:
        for plugin in self.registry.instances():
            try:
                plugin.teardown()
            except Exception:  # noqa: BLE001 - teardown must never block shutdown
                log.exception("plugin teardown failed", extra={"plugin": plugin.id})