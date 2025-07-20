from src.oscillator import SineOscillator, TriangleOscillator, SquareOscillator
from typing import Iterator, List, Union, Optional
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from scipy.io import wavfile


class WaveAdder:
    _oscillators: tuple[Iterator[float], ...]
    _num_oscillators: int

    def __init__(self, *oscillators: Iterator[float]) -> None:
        self._oscillators = oscillators
        self._num_oscillators = len(oscillators)

    def __iter__(self) -> "WaveAdder":
        # Init all osc in list, calling _initialize_osc
        [iter(osc) for osc in self._oscillators]
        return self

    def __next__(self) -> float:
        # Additive Synthesis
        return sum(next(osc) for osc in self._oscillators) / self._num_oscillators


class SynthEngine:
    _sample_rate: int
    _channels: int
    _sample_duration_sec: float

    def __init__(self, sample_rate: int = 44100) -> None:
        self._sample_rate = sample_rate
        self._channels = 1
        self._sample_duration_sec = 2

    def wave_to_file(
        self,
        wav: Union[list[float], npt.NDArray[np.float64]],
        wav2: Optional[Union[list[float], npt.NDArray[np.float64]]] = None,
        fname: str = "temp.wav",
        amp: float = 0.1,
        sample_rate: int = 44100,
    ) -> None:
        wav_arr: npt.NDArray[np.float64] = np.array(wav)
        wav_arr = np.int16(wav_arr * amp * (2**15 - 1))

        if wav2 is not None:
            wav2_arr: npt.NDArray[np.float64] = np.array(wav2)
            wav2_arr = np.int16(wav2_arr * amp * (2**15 - 1))
            wav = np.stack([wav, wav2]).T

        wavfile.write(fname, sample_rate, wav_arr)

    def plot_waveform(
        self,
        wav: Union[list[float], npt.NDArray[np.float64]],
        fname:str,
        title: str = "Waveform",
    ) -> None:
        wav_arr = np.array(wav)
        time_axis = np.linspace(0, self._sample_duration_sec, len(wav_arr))

        plt.figure(figsize=(10, 4))
        plt.plot(time_axis, wav_arr, linewidth=0.5)
        plt.title(title)
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.grid(True)
        plt.tight_layout()

        plt.savefig(f"{fname}.png")
        plt.close()

    def run(self) -> None:
        # TODO Add this generator code into a specific instrument, that can be used on a voice in a channel
        gen: WaveAdder = WaveAdder(
            SineOscillator(freq=880, amp=0.8),
            TriangleOscillator(freq=220, amp=0.4),
            SquareOscillator(freq=55, amp=0.4),
        )

        iter(gen)
        duration: int = self._sample_rate * int(self._sample_duration_sec)
        # Generate float values for oscillators at x time in 0..duration
        wav = [next(gen) for _ in range(duration)]

        filename: str = "prelude_one"
        self.plot_waveform(wav[:2000], fname=filename)
        self.wave_to_file(wav, fname=f"{filename}.wav")
