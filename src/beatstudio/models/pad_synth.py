"""PadSynth — stacked-oscillator pad from chord symbols."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class PadSynth:
    sample_rate: int
    rng: np.random.Generator

    ROMAN = {"i": 0, "iv": 5, "VI": 8, "III": 3, "VII": 10, "I": 0, "V": 7, "vi": 9, "IV": 5}

    def render(self, chords: list[str], *, bpm: int, bars: int) -> np.ndarray:
        bar_s = 4 * 60.0 / bpm
        total = int(bars * bar_s * self.sample_rate)
        out = np.zeros((total, 2), dtype=np.float32)
        per = max(1, bars // max(1, len(chords)))
        for i, chord in enumerate(chords):
            t0 = int(i * per * bar_s * self.sample_rate)
            if t0 >= total:
                break
            root = self.ROMAN.get(chord, 0)
            buf = self._voice(root, int(per * bar_s * self.sample_rate))
            end = min(total, t0 + buf.shape[0])
            out[t0:end] += buf[: end - t0] * 0.55
        return np.clip(out, -1.0, 1.0)

    def _voice(self, root_semis: int, n: int) -> np.ndarray:
        t = np.arange(n) / self.sample_rate
        acc = np.zeros(n, dtype=np.float32)
        for interval in (0, 3, 7, 10):
            freq = 220.0 * (2 ** ((root_semis + interval) / 12.0))
            acc += np.sin(2 * np.pi * freq * t).astype(np.float32)
        env = np.minimum(1.0, t * 4.0) * np.exp(-t * 0.4)
        mono = (acc / 4.0 * env).astype(np.float32)
        return np.stack([mono, mono], axis=1)