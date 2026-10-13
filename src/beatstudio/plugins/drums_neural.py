"""drums-neural — neural drum pattern generator (kick/snare/hat synthesis)."""
from __future__ import annotations

import numpy as np

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.contracts.render import RenderRequest, StemBuffer
from beatstudio.models.drum_synth import DrumSynth
from beatstudio.utils.seeding import rng_for


class DrumsNeuralPlugin(GeneratorPlugin):
    id = "drums-neural"
    kind = "generator"

    def generate(self, request: RenderRequest, context) -> StemBuffer:
        rng = rng_for(request.seed, self.id)
        synth = DrumSynth(sample_rate=context.sample_rate, rng=rng)
        beat = self._pattern(request, rng)
        audio = synth.render(beat, bpm=request.bpm, bars=request.bars, swing=request.swing)
        return StemBuffer(plugin_id=self.id, audio=audio, sample_rate=context.sample_rate,
                          meta={"pattern": beat})

    @staticmethod
    def _pattern(request: RenderRequest, rng: np.random.Generator) -> str:
        styles = ["boom-bap", "trap", "house", "drill"]
        return styles[int(rng.integers(0, len(styles)))]