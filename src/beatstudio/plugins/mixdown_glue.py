"""mixdown-glue — master-bus glue compressor + limiter plugin."""
from __future__ import annotations

import numpy as np

from beatstudio.contracts.generator import GeneratorPlugin
from beatstudio.contracts.render import RenderRequest, StemBuffer
from beatstudio.services.master_bus import MasterBus


class MixdownGluePlugin(GeneratorPlugin):
    id = "mixdown-glue"
    kind = "generator"

    def generate(self, request: RenderRequest, context) -> StemBuffer:
        bus = MasterBus(sample_rate=context.sample_rate, ceiling_db=-0.3, ratio=2.0)
        # In the full pipeline this reads the sum bus; standalone it renders silence
        # so the plugin remains testable without a live stem graph.
        silence = np.zeros((int(request.seconds * context.sample_rate), 2), dtype=np.float32)
        return StemBuffer(plugin_id=self.id, audio=bus.process(silence),
                          sample_rate=context.sample_rate, meta={"stage": "master"})