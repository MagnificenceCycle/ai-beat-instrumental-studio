"""HostContext — the one object every plugin receives. No globals."""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from beatstudio.config.settings import HostSettings
    from beatstudio.plugins.registry import PluginRegistry
    from beatstudio.services.audio_engine import AudioEngine


@dataclass(slots=True)
class HostContext:
    """Injected into every plugin at setup(). Services reachable here only."""

    settings: "HostSettings"
    engine: "AudioEngine"
    registry: "PluginRegistry"

    @property
    def sample_rate(self) -> int:
        return self.engine.sample_rate

    def resolve(self, plugin_id: str):
        return self.registry.get(plugin_id)