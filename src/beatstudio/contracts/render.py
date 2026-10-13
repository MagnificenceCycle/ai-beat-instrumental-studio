"""Render request + stem buffer contracts shared across host and plugins."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass(slots=True)
class RenderRequest:
    prompt: str
    bpm: int = 92
    bars: int = 16
    seed: int = 6767
    key: str = "F#min"
    swing: float = 0.14

    @property
    def seconds(self) -> float:
        return self.bars * 4 * (60.0 / self.bpm)


@dataclass(slots=True)
class StemBuffer:
    plugin_id: str
    audio: np.ndarray  # shape (frames, 2), float32, [-1, 1]
    sample_rate: int = 48000
    meta: dict[str, str] = field(default_factory=dict)

    @property
    def frames(self) -> int:
        return int(self.audio.shape[0])

    @property
    def duration_s(self) -> float:
        return self.frames / float(self.sample_rate)