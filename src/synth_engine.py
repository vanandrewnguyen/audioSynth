from librosa import note_to_hz
from src.oscillator import (
    Generator,
    SineOscillator,
    TriangleOscillator,
    SquareOscillator,
    SawtoothOscillator,
)
from src.wave_chain import Chain, WaveAdder
from src.modulator import ModulatedOscillator
from src.modifier import Panner
from src.envelopes import ADSREnvelope
from typing import Iterator, List, Union, Optional
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from scipy.io import wavfile


# class WaveAdder(Generator):
#     _oscillators: tuple[Iterator[float], ...]
#     _num_oscillators: int

#     def __init__(self, *oscillators: Iterator[float]) -> None:
#         self._oscillators = oscillators
#         self._num_oscillators = len(oscillators)

#     def __iter__(self) -> "WaveAdder":
#         # Init all osc in list, calling _initialize_osc
#         [iter(osc) for osc in self._oscillators]
#         return self

#     def __next__(self) -> float:
#         # Additive Synthesis
#         return sum(next(osc) for osc in self._oscillators) / self._num_oscillators


class SynthEngine:
    _sample_rate: int
    _channels: int
    _sample_duration_sec: float

    def __init__(self, sample_rate: int = 44100) -> None:
        self._sample_rate = sample_rate
        self._channels = 1
        self._sample_duration_sec = 4

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
        fname: str,
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
        def amp_mod(init_amp: float, env: float) -> float:
            return env * init_amp

        def freq_mod(init_freq, env, mod_amt=0.01, sustain_level=0.7):
            return init_freq + ((env - sustain_level) * init_freq * mod_amt)

        def simple_freq_mod(init_freq: float, val: float) -> float:
            return init_freq * val

        # TODO Add this generator code into a specific instrument, that can be used on a voice in a channel
        # gen: WaveAdder = WaveAdder(
        #     SineOscillator(freq=880, amp=0.8),
        #     TriangleOscillator(freq=220, amp=0.4),
        #     # SquareOscillator(freq=55, amp=0.4),
        # )

        # ADSR Env
        # gen = ModulatedOscillator(
        #     SineOscillator(freq=880, amp=0.8),
        #     ADSREnvelope(0.01, 0.02, 0.6, 0.1),
        #     amp_mod=amp_mod
        # )

        # LFO Wave AM
        # gen = ModulatedOscillator(
        #     SquareOscillator(freq=110),
        #     SineOscillator(freq=5, wave_range=(0.2, 1)),
        #     amp_mod=amp_mod
        # )

        # LFO Wave FM
        # gen: Generator = ModulatedOscillator(
        #     SquareOscillator(freq=110),
        #     SawtoothOscillator(freq=5, wave_range=(0.2, 1)),
        #     freq_mod=simple_freq_mod
        # )

        gen: Generator = WaveAdder(
            ModulatedOscillator(
                SineOscillator(note_to_hz("A2")), ADSREnvelope(0.01, 0.1, 0.4), amp_mod=amp_mod
            ),
            ModulatedOscillator(
                SineOscillator(note_to_hz("A2") + 3),
                ADSREnvelope(0.01, 0.1, 0.4),
                amp_mod=amp_mod,
            ),
            Chain(
                ModulatedOscillator(
                    TriangleOscillator(note_to_hz("C4")), ADSREnvelope(0.5), amp_mod=amp_mod
                ),
                Panner(0.7),
            ),
            Chain(
                ModulatedOscillator(
                    TriangleOscillator(note_to_hz("E3")), ADSREnvelope(0.5), amp_mod=amp_mod
                ),
                Panner(0.3),
            ),
            stereo=True,
        )

        iter(gen)
        duration: int = self._sample_rate * int(self._sample_duration_sec)
        # Generate float values for oscillators at x time in 0..duration
        wav = [next(gen) for _ in range(duration)]

        filename: str = "prelude_one"
        self.plot_waveform(wav[:20000], fname=filename)
        self.wave_to_file(wav, fname=f"{filename}.wav")
