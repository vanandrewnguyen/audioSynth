from librosa import note_to_hz
from src.oscillators.base_oscillator import Generator
from src.oscillators.oscillators import (
    SineOscillator,
    TriangleOscillator,
    SquareOscillator,
    SawtoothOscillator,
)
from src.wave_chain import Chain, WaveAdder
from src.modulator import ModulatedOscillator
from src.modifier import Panner, Volume, ModulatedVolume, ModulatedPanner
from src.envelopes import ADSREnvelope
from typing import Union, Optional
import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from scipy.io import wavfile


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

    # If mono, single graph is plotted.
    # If stereo, we plot L, R and combined graphs
    def plot_waveform(
        self,
        wav: Union[list[float], list[tuple[float, float]], npt.NDArray[np.float64]],
        fname: str,
        title: str = "Waveform",
    ) -> None:
        wav_arr = np.array(wav)
        time_axis = np.linspace(0, self._sample_duration_sec, len(wav_arr))

        if wav_arr.ndim == 1:
            # MONO
            plt.figure(figsize=(10, 4))
            plt.plot(time_axis, wav_arr, linewidth=0.5)
            plt.title(title)
            plt.xlabel("Time (s)")
            plt.ylabel("Amplitude")
            plt.grid(True)
            plt.tight_layout()
        elif wav_arr.ndim == 2 and wav_arr.shape[1] == 2:
            # STEREO
            left = wav_arr[:, 0]
            right = wav_arr[:, 1]
            # combined = (left + right) / 2

            fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

            axes[0].plot(time_axis, left, color="tab:blue", linewidth=0.5)
            axes[0].set_title(f"{title} - Left Channel")
            axes[0].set_ylabel("Amplitude")
            axes[0].grid(True)

            axes[1].plot(time_axis, right, color="tab:orange", linewidth=0.5)
            axes[1].set_title(f"{title} - Right Channel")
            axes[1].set_ylabel("Amplitude")
            axes[1].grid(True)

            axes[2].plot(time_axis, wav_arr, linewidth=0.5)
            axes[2].set_title(f"{title} - Combined (Mono Mix)")
            axes[2].set_xlabel("Time (s)")
            axes[2].set_ylabel("Amplitude")
            axes[2].grid(True)

            plt.tight_layout()
        else:
            raise ValueError("Waveform must be mono or stereo (Nx2 array)")

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
        # TODO Move all this generator code into generators folder
        # gen: WaveAdder = WaveAdder(
        #     SineOscillator(freq=880, amp=0.8),
        #     TriangleOscillator(freq=220, amp=0.4),
        #     # SquareOscillator(freq=55, amp=0.4),
        # )

        # ADSR Env
        # gen = ModulatedOscillator(
        #     SineOscillator(freq=880, amp=0.8),
        #     ADSREnvelope(0.01, 0.02, 0.6, 0.1),
        #     amp_mod=amp_mod,
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

        # gen: Generator = WaveAdder(
        #     ModulatedOscillator(
        #         SineOscillator(note_to_hz("A2")),
        #         ADSREnvelope(0.01, 0.1, 0.4),
        #         amp_mod=amp_mod,
        #     ),
        #     ModulatedOscillator(
        #         SineOscillator(note_to_hz("A2") + 3),
        #         ADSREnvelope(0.01, 0.1, 0.4),
        #         amp_mod=amp_mod,
        #     ),
        #     Chain(
        #         ModulatedOscillator(
        #             TriangleOscillator(note_to_hz("C4")),
        #             ADSREnvelope(0.5),
        #             amp_mod=amp_mod,
        #         ),
        #         Panner(0.7),
        #     ),
        #     Chain(
        #         ModulatedOscillator(
        #             TriangleOscillator(note_to_hz("E3")),
        #             ADSREnvelope(0.5),
        #             amp_mod=amp_mod,
        #         ),
        #         Panner(0.3),
        #     ),
        #     stereo=True,
        # )

        # gen: Generator = WaveAdder(
        #     ModulatedOscillator(
        #         SineOscillator(note_to_hz("A2")),
        #         ADSREnvelope(0.01, 0.1, 0.4),
        #         amp_mod=amp_mod,
        #     ),
        #     Chain(
        #         WaveAdder(
        #             SineOscillator(note_to_hz("A2")),
        #             SineOscillator(note_to_hz("A2") + 3),
        #         ),
        #         ModulatedVolume(
        #             ADSREnvelope(0.01, 0.1, 0.4),
        #         ),
        #     ),
        #     Chain(
        #         WaveAdder(
        #             Chain(TriangleOscillator(note_to_hz("C4")), Panner(0.7)),
        #             Chain(TriangleOscillator(note_to_hz("E3")), Panner(0.3)),
        #             stereo=True,
        #         ),
        #         ModulatedVolume(ADSREnvelope(0.5)),
        #     ),
        #     stereo=True,
        # )

        # gen: Generator = WaveAdder(
        #     Chain(
        #         TriangleOscillator(freq=note_to_hz("C4")),
        #         ModulatedPanner(
        #             SineOscillator(freq=3, wave_range=(-1,1))
        #         ),
        #     ),
        #     Chain(
        #         SineOscillator(freq=note_to_hz("E4")),
        #         ModulatedPanner(
        #             SineOscillator(freq=2, wave_range=(-1,1))
        #         ),
        #     ),
        #     Chain(
        #         TriangleOscillator(freq=note_to_hz("G4")),
        #         ModulatedPanner(
        #             SineOscillator(freq=3, phase=180, wave_range=(-1,1))
        #         ),
        #     ),
        #     Chain(
        #         SineOscillator(freq=note_to_hz("B4")),
        #         ModulatedPanner(
        #             SineOscillator(freq=2, phase=180, wave_range=(-1,1))
        #         ),
        #     ),
        #     stereo=True
        # )

        gen = Chain(
            WaveAdder(
                Chain(
                    ModulatedOscillator(
                        SineOscillator(freq=note_to_hz("A4")),
                        ModulatedOscillator(
                            SineOscillator(freq=20),
                            ADSREnvelope(0, 4, 0),
                            freq_mod=amp_mod
                        ),
                        freq_mod=freq_mod
                    ),
                    Panner(r=0)
                ),
                Chain(
                    ModulatedOscillator(
                        SineOscillator(freq=note_to_hz("A4")),
                        ModulatedOscillator(
                            SineOscillator(freq=20),
                            ADSREnvelope(4),
                            freq_mod=amp_mod
                        ),
                        freq_mod=freq_mod
                    ),
                    Panner(r=1)
                ),
                stereo=True
            )
        )

        iter(gen)
        duration: int = self._sample_rate * int(self._sample_duration_sec)

        # Generate float values for oscillators at x time in 0..duration
        wav = [next(gen) for _ in range(duration)]

        filename: str = "prelude_one"
        self.plot_waveform(wav[:1000], fname=filename)
        self.wave_to_file(wav, fname=f"{filename}.wav")

        print("DONE.")
