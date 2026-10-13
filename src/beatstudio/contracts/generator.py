"""GeneratorPlugin — the base every beat/instrument generator implements."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from beatstudio.contracts.render import RenderRequest, StemBuffer

if TYPE_CHECKING:
    from beatstudio.host.context import HostContext


class GeneratorPlugin(ABC):
    """A generator emits one stereo stem for a render request.

    Subclass, set `id`/`kind`, implement `generate`. `setup` receives the
    HostContext once at load; `teardown` is called at host shutdown.
    """

    id: str = "unnamed"
    kind: str = "generator"

    def setup(self, context: "HostContext") -> None:
        self._context = context

    @abstractmethod
    def generate(self, request: RenderRequest, context: "HostContext") -> StemBuffer:
        """Return one stereo stem. Must be deterministic for a given seed."""

    def teardown(self) -> None:
        """Override to release model handles / threads."""
        return None