from abc import ABC, abstractmethod
import itertools
from typing import Optional, Iterator, List


# Generic class to contain ADSR and ADBSSR
class Envelope(ABC):
    sample_rate: int

    attack_duration: float
    decay_duration: float
    sustain_level: float
    release_duration: float
    val: float
    ended: bool


class ADSREnvelope(Envelope):
    _stepper: Optional[Iterator[float]]

    def __init__(
        self,
        attack_duration: float = 0.05,
        decay_duration: float = 0.2,
        sustain_level: float = 0.7,
        release_duration: float = 0.3,
        sample_rate: int = 44100,
    ) -> None:
        self.attack_duration = attack_duration
        self.decay_duration = decay_duration
        self.sustain_level = sustain_level
        self.release_duration = release_duration
        self._sample_rate = sample_rate
        self.val = 0.0
        self.ended = False
        self._stepper = None

    def get_ads_stepper(self) -> Iterator[float]:
        steppers: List[Iterator[float]] = []

        if self.attack_duration > 0:
            steppers.append(
                itertools.count(
                    start=0, step=1 / (self.attack_duration * self._sample_rate)
                )
            )
        if self.decay_duration > 0:
            steppers.append(
                itertools.count(
                    start=1,
                    step=-(1 - self.sustain_level)
                    / (self.decay_duration * self._sample_rate),
                )
            )

        # Switch between ADR between points
        # When amp (val) reaches 1, attack stops
        # Decay stops when val reaches sustain
        # Sustain stops when note is stopped (only via trigger release)
        # Release stops when amp reaches 0
        while True:
            l = len(steppers)
            if l > 0:
                val = next(steppers[0])
                if l == 2 and val > 1:
                    steppers.pop(0)
                    val = next(steppers[0])
                elif l == 1 and val < self.sustain_level:
                    steppers.pop(0)
                    val = self.sustain_level
            else:
                val = self.sustain_level
            yield val

    def get_r_stepper(self) -> Iterator[float]:
        val: float = self.val

        if self.release_duration > 0:
            release_step = -val / (self.release_duration * self._sample_rate)
            stepper = itertools.count(val, step=release_step)
        else:
            # Exit
            val = -1
            stepper = iter([0.0])  # dummy to avoid unbound error

        while True:
            if val <= 0:
                self.ended = True
                val = 0.0
            else:
                val = next(stepper)
            yield val

    def __iter__(self) -> "ADSREnvelope":
        self.val = 0.0
        self.ended = False
        self._stepper = self.get_ads_stepper()

        return self

    def __next__(self) -> float:
        if self._stepper is None:
            raise StopIteration

        self.val = next(self._stepper)
        return self.val

    def trigger_release(self) -> None:
        # Switch steppers
        self._stepper = self.get_r_stepper()
