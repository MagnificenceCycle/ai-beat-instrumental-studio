"""BassSynth — saw/square bass voice from scale-degree walk."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class BassSynth:
    sample_rate: int
    rng: np.random.Generator

    PENTATONIC = [0, 3, 5, 7, 10]

    def render(self, degrees: list[int], *, bpm: int, bars: int) -> np.ndarray:
        beat_s = 60.0 / bpm
        note_s = beat_s / 2.0
        total = int(bars * 4 * beat_s * self.sample_rate)
        out = np.zeros((total, 2), dtype=np.float32)
        for i, deg in enumerate(degrees):
            t0 = int(i * note_s * self.sample_rate)
            if t0 >= total:
                break
            semis = self.PENTATONIC[deg % len(self.PENTATONIC)]
            freq = 55.0 * (2 ** (semis / 12.0))
            buf = self._voice(freq, int(note_s * self.sample_rate))
            end = min(total, t0 + buf.shape[0])
            out[t0:end] += buf[: end - t0] * 0.8
        return np.clip(out, -1.0, 1.0)

    def _voice(self, freq: float, n: int) -> np.ndarray:
        t = np.arange(n) / self.sample_rate
        saw = 2.0 * (t * freq - np.floor(0.5 + t * freq))
        env = np.exp(-t * 3.5) * (1.0 - np.exp(-t * 200.0))
        mono = (saw * env).astype(np.float32)
        return np.stack([mono, mono], axis=1)