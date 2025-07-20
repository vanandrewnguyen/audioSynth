from abc import ABC, abstractmethod
import math


class Oscillator(ABC):
    _freq: float
    _amp: float
    _phase: float
    _sample_rate: int
    _wave_range: tuple[float, float]

    _f: float
    _a: float
    _p: float
    _i: float

    def __init__(
        self,
        freq: float = 440.0,
        phase: float = 0,
        amp: float = 1.0,
        sample_rate: int = 44100,
        wave_range: tuple[float, float] = (-1, 1),
    ):
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._sample_rate = sample_rate
        self._wave_range = wave_range

        self._f = freq
        self._a = amp
        self._p = phase

    @property
    def init_freq(self):
        return self._freq

    @property
    def init_amp(self):
        return self._amp

    @property
    def init_phase(self):
        return self._phase

    @property
    def freq(self) -> float:
        return self._f

    @freq.setter
    def freq(self, value: float) -> None:
        self._f = value
        self._post_freq_set()

    @property
    def amp(self):
        return self._a

    @amp.setter
    def amp(self, value: float) -> None:
        self._a = value
        self._post_amp_set()

    @property
    def phase(self):
        return self._p

    @phase.setter
    def phase(self, value: float) -> None:
        self._p = value
        self._post_phase_set()

    def _post_freq_set(self):
        pass

    def _post_amp_set(self):
        pass

    def _post_phase_set(self):
        pass

    @abstractmethod
    def _initialize_osc(self):
        pass

    @staticmethod
    def squish_val(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        # Normalise by higher range val
        return (((val + 1) / 2) * (max_val - min_val)) + min_val

    @abstractmethod
    def __next__(self) -> float:
        return 0.0

    def __iter__(self):
        self.freq = self._freq
        self.phase = self._phase
        self.amp = self._amp
        self._initialize_osc()
        return self


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
