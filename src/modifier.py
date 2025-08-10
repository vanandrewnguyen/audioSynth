from typing import Tuple, Iterable
from src.modulator import TriggerableFloatGenerator


# A modifier modifies the signal of a generator but doesn't generate its own signal
class Modifier:
    pass


class Panner(Modifier):
    def __init__(self, r: float = 0.5) -> None:
        self.r = r

    def __call__(self, val: float) -> Tuple[float, float]:
        # Return tuple value for l r channel
        r: float = self.r * 2.0
        l: float = 2.0 - r
        return (l * val, r * val)


class Volume(Modifier):
    def __init__(self, amp: float = 1.0):
        self.amp = amp

    def __call__(self, val: float):
        _val = None
        if isinstance(val, Iterable):
            # Loop through generator and scale amp
            _val = tuple(v * self.amp for v in val)
        elif isinstance(val, (int, float)):
            _val = val * self.amp
        return _val


# Modulated modifier, a modifier produces its own signal but modifies a give signal too
class ModulatedPanner(Panner):
    def __init__(self, modulator):
        super().__init__(r=0.0)
        self.modulator = modulator

    def __iter__(self) -> "ModulatedPanner":
        iter(self.modulator)
        return self

    def __next__(self) -> float:
        self.r = (next(self.modulator) + 1) / 2
        return self.r


class ModulatedVolume(Volume):
    def __init__(self, modulator):
        super().__init__(0.0)
        self.modulator = modulator

    def __iter__(self) -> "ModulatedVolume":
        iter(self.modulator)
        return self

    def __next__(self) -> float:
        self.amp = next(self.modulator)
        return self.amp

    def trigger_release(self) -> None:
        if isinstance(self.modulator, TriggerableFloatGenerator):
            self.modulator.trigger_release()

    @property
    def ended(self):
        ended = False
        if isinstance(self.modulator, TriggerableFloatGenerator):
            ended = self.modulator.ended
        return ended
