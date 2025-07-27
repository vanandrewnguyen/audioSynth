from src.oscillators.base_oscillator import Oscillator
import math


class SineOscillator(Oscillator):
    def _post_freq_set(self):
        self._step = (2 * math.pi * self._f) / self._sample_rate

    def _post_phase_set(self):
        self._p = (self._p / 360) * 2 * math.pi

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        val: float = math.sin(self._i + self._p)
        self._i = self._i + self._step

        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)

        return val * self._a


class SquareOscillator(SineOscillator):
    def __init__(
        self,
        freq: float = 440.0,
        phase: float = 0.0,
        amp: float = 1.0,
        sample_rate: int = 44100,
        wave_range: tuple[float, float] = (-1, 1),
        threshold: float = 0,
    ):
        super().__init__(freq, phase, amp, sample_rate, wave_range)
        self.threshold = threshold

    def __next__(self):
        val: float = math.sin(self._i + self._p)
        self._i = self._i + self._step

        # Fixed value based on time step
        val = self._wave_range[0] if val < self.threshold else self._wave_range[1]

        return val * self._a


class SawtoothOscillator(Oscillator):
    def _post_freq_set(self):
        self._period = self._sample_rate / self._f
        self._post_phase_set

    def _post_phase_set(self):
        self._p = ((self._p + 90) / 360) * self._period

    def _initialize_osc(self):
        self._i = 0

    def __next__(self):
        div: float = (self._i + self._p) / self._period
        val: float = 2 * (div - math.floor(0.5 + div))
        self._i = self._i + 1

        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)

        return val * self._a


class TriangleOscillator(SawtoothOscillator):
    def __next__(self):
        div: float = (self._i + self._p) / self._period
        val: float = 2 * (div - math.floor(0.5 + div))
        val = (abs(val) - 0.5) * 2
        self._i = self._i + 1

        if self._wave_range != (-1, 1):
            val = self.squish_val(val, *self._wave_range)

        return val * self._a
