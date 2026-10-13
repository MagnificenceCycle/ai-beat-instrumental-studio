"""PluginLoader — resolves allowlisted modules, imports them, instantiates."""
from __future__ import annotations

import importlib
import inspect
from dataclasses import dataclass

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.plugins.registry import PluginSpec
from beatstudio.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class PluginLoader:
    """Imports a PluginSpec's module and returns the plugin instance.

    Refuses to load anything not in the allowlist. Import errors are logged
    and the spec is marked failed — one bad plugin must not kill the host.
    """

    allowlist: list[str]

    def load(self, spec: PluginSpec) -> GeneratorPlugin | None:
        if spec.id not in self.allowlist:
            log.warning("plugin not allowlisted, skipping", extra={"plugin": spec.id})
            return None
        try:
            module = importlib.import_module(spec.module)
        except ImportError:
            log.exception("plugin import failed", extra={"plugin": spec.id, "module": spec.module})
            return None

        cls = getattr(module, spec.entry, None)
        if cls is None or not inspect.isclass(cls):
            log.error("plugin entry missing", extra={"plugin": spec.id, "entry": spec.entry})
            return None
        if not issubclass(cls, GeneratorPlugin):
            log.error("plugin does not implement GeneratorPlugin", extra={"plugin": spec.id})
            return None
        return cls()