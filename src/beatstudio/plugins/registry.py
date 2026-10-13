"""PluginRegistry — holds specs, loads instances, exposes generators."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.plugins.loader import PluginLoader
from beatstudio.utils.logging import get_logger

if TYPE_CHECKING:
    from beatstudio.config.settings import HostSettings
    from beatstudio.services.audio_engine import AudioEngine

log = get_logger(__name__)


@dataclass(slots=True)
class PluginSpec:
    id: str
    module: str
    entry: str
    enabled: bool = True


@dataclass(slots=True)
class PluginRegistry:
    settings: "HostSettings"
    engine: "AudioEngine"
    _specs: list[PluginSpec] = field(default_factory=list)
    _instances: dict[str, GeneratorPlugin] = field(default_factory=dict)

    def load_all(self) -> None:
        loader = PluginLoader(allowlist=list(self.settings.loader.allowlist))
        self._specs = list(self.settings.plugin_specs)
        from beatstudio.host.context import HostContext  # local import: avoid cycle

        ctx = HostContext(settings=self.settings, engine=self.engine, registry=self)
        for spec in self._specs:
            if not spec.enabled or spec.id in self.settings.loader.disabled:
                spec.enabled = False
                continue
            plugin = loader.load(spec)
            if plugin is None:
                spec.enabled = False
                continue
            plugin.setup(ctx)
            self._instances[spec.id] = plugin

    def specs(self) -> list[PluginSpec]:
        return list(self._specs)

    def instances(self) -> list[GeneratorPlugin]:
        return list(self._instances.values())

    def generators(self) -> list[GeneratorPlugin]:
        return [p for p in self._instances.values() if getattr(p, "kind", "") == "generator"]

    def get(self, plugin_id: str) -> GeneratorPlugin | None:
        return self._instances.get(plugin_id)