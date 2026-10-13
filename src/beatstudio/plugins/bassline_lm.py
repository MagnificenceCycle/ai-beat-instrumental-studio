"""bassline-lm — language-model-style bassline generator over scale degrees."""
from __future__ import annotations

import numpy as np

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.contracts.render import RenderRequest, StemBuffer
from beatstudio.models.bass_synth import BassSynth
from beatstudio.utils.seeding import rng_for


class BasslineLmPlugin(GeneratorPlugin):
    id = "bassline-lm"
    kind = "generator"

    def generate(self, request: RenderRequest, context) -> StemBuffer:
        rng = rng_for(request.seed, self.id)
        synth = BassSynth(sample_rate=context.sample_rate, rng=rng)
        degrees = self._walk(request, rng)
        audio = synth.render(degrees, bpm=request.bpm, bars=request.bars)
        return StemBuffer(plugin_id=self.id, audio=audio, sample_rate=context.sample_rate,
                          meta={"degrees": ",".join(map(str, degrees))})

    @staticmethod
    def _walk(request: RenderRequest, rng: np.random.Generator) -> list[int]:
        # degenerate "LM": random walk constrained to a pentatonic root set
        steps = max(4, request.bars)
        return [int(rng.integers(0, 5)) for _ in range(steps)]