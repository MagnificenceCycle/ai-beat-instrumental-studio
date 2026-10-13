"""keys-diffusion — diffusion-style pad/keys generator (chord-stacked noise)."""
from __future__ import annotations

import numpy as np

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.contracts.render import RenderRequest, StemBuffer
from beatstudio.models.pad_synth import PadSynth
from beatstudio.utils.seeding import rng_for


class KeysDiffusionPlugin(GeneratorPlugin):
    id = "keys-diffusion"
    kind = "generator"

    def generate(self, request: RenderRequest, context) -> StemBuffer:
        rng = rng_for(request.seed, self.id)
        synth = PadSynth(sample_rate=context.sample_rate, rng=rng)
        chords = self._progression(request, rng)
        audio = synth.render(chords, bpm=request.bpm, bars=request.bars)
        return StemBuffer(plugin_id=self.id, audio=audio, sample_rate=context.sample_rate,
                          meta={"chords": "|".join(chords)})

    @staticmethod
    def _progression(request: RenderRequest, rng: np.random.Generator) -> list[str]:
        pool = [["i", "VI", "III", "VII"], ["i", "iv", "VII", "III"], ["I", "V", "vi", "IV"]]
        return pool[int(rng.integers(0, len(pool)))]