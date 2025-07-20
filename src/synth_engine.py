from src.oscillator import Oscillator, SineOscillator
from typing import Iterator
import numpy as np
from scipy.io import wavfile


def wave_to_file(wav, wav2=None, fname="temp.wav", amp=0.1, sample_rate=44100):
    wav = np.array(wav)
    wav = np.int16(wav * amp * (2**15 - 1))
    
    if wav2 is not None:
        wav2 = np.array(wav2)
        wav2 = np.int16(wav2 * amp * (2 ** 15 - 1))
        wav = np.stack([wav, wav2]).T
    
    wavfile.write(fname, sample_rate, wav)

class WaveAdder:
    def __init__(self, *oscillators: Iterator[float]) -> None:
        self.oscillators: tuple[Iterator[float], ...] = oscillators
        self.n: int = len(oscillators)
    
    def __iter__(self) -> 'WaveAdder':
        [iter(osc) for osc in self.oscillators]
        return self
    
    def __next__(self) -> float:
        return sum(next(osc) for osc in self.oscillators) / self.n


class SynthEngine:
    _sample_rate: int
    _channels: int

    def __init__(
        self, sample_rate: int = 44100
    ) -> None:
        self._sample_rate = sample_rate
        self._channels = 1

    def run(self) -> None:
        gen = WaveAdder(
            SineOscillator(freq = 440, amp = 0.5),
        )
        iter(gen)
        wav = [next(gen) for _ in range(44100 * 4)] # 4 Seconds
        wave_to_file(wav, fname="prelude_one.wav")
