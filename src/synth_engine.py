class SynthEngine:
    _sample_rate: int
    _channels: int
    _num_blocks: int
    _num_block_samples: int

    def __init__(self):
        self._sample_rate = 44100
        self._channels = 1
        self._num_blocks = 8
        self._num_block_samples = 512

    def run(self) -> None:
        pass
