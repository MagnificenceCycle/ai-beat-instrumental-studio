"""DrumSynth — synthesized kick/snare/hat voices, deterministic per rng."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class DrumSynth:
    sample_rate: int
    rng: np.random.Generator

    def render(self, pattern: str, *, bpm: int, bars: int, swing: float) -> np.ndarray:
        spb = 60.0 / bpm
        step_s = spb / 4.0
        total = int(bars * 4 * spb * self.sample_rate)
        out = np.zeros((total, 2), dtype=np.float32)
        hits = self._hits(pattern)
        for step, (voice, gain) in enumerate(hits):
            t = int(step * step_s * self.sample_rate)
            if t >= total:
                break
            voice_buf = self._voice(voice, int(step_s * self.sample_rate))
            end = min(total, t + voice_buf.shape[0])
            out[t:end] += voice_buf[: end - t] * gain
        return np.clip(out, -1.0, 1.0)

    def _hits(self, pattern: str) -> list[tuple[str, float]]:
        table = {
            "boom-bap": [("kick", 1.0), ("hat", 0.3), ("snare", 0.9)] * 8,
            "trap": [("kick", 1.0), ("hat", 0.4), ("hat", 0.4), ("snare", 0.8)] * 6,
            "house": [("kick", 1.0), ("hat", 0.35)] * 12,
            "drill": [("kick", 1.0), ("snare", 0.7), ("hat", 0.3)] * 8,
        }
        return table.get(pattern, table["boom-bap"])

    def _voice(self, name: str, n: int) -> np.ndarray:
        t = np.arange(n) / self.sample_rate
        if name == "kick":
            env = np.exp(-t * 18.0)
            tone = np.sin(2 * np.pi * (60.0 * np.exp(-t * 12.0) + 40.0) * t)
        elif name == "snare":
            env = np.exp(-t * 24.0)
            tone = self.rng.normal(0, 1, n)
        else:
            env = np.exp(-t * 60.0)
            tone = self.rng.normal(0, 1, n)
        mono = (env * tone).astype(np.float32)
        return np.stack([mono, mono], axis=1)