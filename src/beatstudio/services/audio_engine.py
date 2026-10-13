"""AudioEngine — WAV I/O and playback device abstraction."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf


class AudioEngine:
    """Owns sample rate + buffer size. Writes float32 stems to disk as PCM."""

    def __init__(self, *, sample_rate: int = 48000, buffer: int = 512) -> None:
        self.sample_rate = sample_rate
        self.buffer = buffer

    def write_wav(self, path: Path, audio: np.ndarray, *, subtype: str = "PCM_24") -> Path:
        if audio.ndim != 2 or audio.shape[1] != 2:
            raise ValueError(f"expected stereo (frames, 2), got {audio.shape}")
        sf.write(str(path), audio, self.sample_rate, subtype=subtype)
        return path

    def read_wav(self, path: Path) -> np.ndarray:
        data, rate = sf.read(str(path), dtype="float32", always_2d=True)
        if rate != self.sample_rate:
            raise ValueError(f"sample-rate mismatch: file={rate} engine={self.sample_rate}")
        return data

    def peak_db(self, audio: np.ndarray) -> float:
        peak = float(np.max(np.abs(audio))) or 1e-12
        return 20.0 * float(np.log10(peak))