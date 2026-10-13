"""RenderPipeline — orders generator plugins into a stem pass, then mixdown."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from beatstudio.contracts.render import RenderRequest, StemBuffer
from beatstudio.host.context import HostContext
from beatstudio.utils.logging import get_logger

log = get_logger(__name__)


@dataclass(slots=True)
class RenderPipeline:
    context: HostContext

    def run(self, *, prompt: str, bpm: int, bars: int, seed: int, out: Path) -> Path:
        request = RenderRequest(prompt=prompt, bpm=bpm, bars=bars, seed=seed)
        generators = self.context.registry.generators()
        stems: list[StemBuffer] = []
        for gen in generators:
            stem = gen.generate(request, self.context)
            log.info("stem rendered", extra={"plugin": gen.id, "frames": stem.frames})
            stems.append(stem)

        mix = self._sum_stems(stems, self.context.sample_rate)
        self.context.engine.write_wav(out, mix)
        return out

    @staticmethod
    def _sum_stems(stems: list[StemBuffer], sample_rate: int) -> np.ndarray:
        if not stems:
            return np.zeros((sample_rate, 2), dtype=np.float32)
        length = max(s.audio.shape[0] for s in stems)
        bus = np.zeros((length, 2), dtype=np.float32)
        for stem in stems:
            pad = length - stem.audio.shape[0]
            bus[: stem.audio.shape[0]] += stem.audio
            if pad:
                log.debug("stem shorter than bus", extra={"plugin": stem.plugin_id, "pad": pad})
        peak = float(np.max(np.abs(bus))) or 1.0
        return (bus / peak * 0.97).astype(np.float32)