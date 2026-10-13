"""MasterBus — glue compressor + soft limiter for the render bus."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class MasterBus:
    sample_rate: int
    ceiling_db: float = -0.3
    ratio: float = 2.0

    def process(self, audio: np.ndarray) -> np.ndarray:
        if audio.size == 0:
            return audio
        ceiling = 10 ** (self.ceiling_db / 20.0)
        x = np.tanh(audio * self.ratio) / np.tanh(self.ratio)
        peak = float(np.max(np.abs(x))) or 1.0
        if peak > ceiling:
            x = x * (ceiling / peak)
        return x.astype(np.float32)