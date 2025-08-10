import math
from typing import (
    Callable,
    Iterator,
    Optional,
    Tuple,
    Union,
    Protocol,
    runtime_checkable,
)
from src.envelopes import ADSREnvelope
from src.oscillators.oscillators import Oscillator
from src.oscillators.base_oscillator import Generator


# Modulators are anything that modulates the signal of a generator, it may be a generator itself
# Modulators can be any of:
# - plain Iterator[float]
# - or anything that follows the TriggerableFloatGenerator protocol
# Modulators can be any kind of generator, e.g. envelope, another ModulatedOscillator

# Stereo vs mono, can have 1/2 channels
NumberOrStereo = Union[float, tuple[float, float]]


@runtime_checkable
class TriggerableFloatGenerator(Protocol):
    ended: bool

    def __iter__(self) -> Iterator[NumberOrStereo]: ...
    def __next__(self) -> NumberOrStereo: ...
    def trigger_release(self) -> None: ...


ModulatorType = Union[Iterator[NumberOrStereo], TriggerableFloatGenerator]


class ModulatedOscillator(Generator):
    oscillator: Oscillator
    modulators: Tuple[Iterator[float], ...]
    amp_mod: Optional[Callable[[float, float], float]]
    freq_mod: Optional[Callable[[float, float], float]]
    phase_mod: Optional[Callable[[float, float], float]]
    _modulators_count: int

    def __init__(
        self,
        oscillator: Oscillator,
        *modulators: Iterator[float],
        amp_mod: Optional[Callable[[float, float], float]] = None,
        freq_mod: Optional[Callable[[float, float], float]] = None,
        phase_mod: Optional[Callable[[float, float], float]] = None,
    ) -> None:
        self.oscillator = oscillator
        self.modulators = modulators
        self.amp_mod = amp_mod
        self.freq_mod = freq_mod
        self.phase_mod = phase_mod
        self._modulators_count = len(modulators)

    def __iter__(self) -> "ModulatedOscillator":
        iter(self.oscillator)

        # Enter modulator setup
        for modulator in self.modulators:
            iter(modulator)

        return self

    def _modulate(self, mod_vals: list[float]) -> None:
        if self.amp_mod is not None:
            new_amp = self.amp_mod(self.oscillator.init_amp, mod_vals[0])
            self.oscillator.amp = new_amp

        if self.freq_mod is not None:
            mod_val = mod_vals[1] if self._modulators_count >= 2 else mod_vals[0]
            new_freq = self.freq_mod(self.oscillator.init_freq, mod_val)
            self.oscillator.freq = new_freq

        if self.phase_mod is not None:
            if self._modulators_count == 3:
                mod_val = mod_vals[2]
            else:
                mod_val = mod_vals[-1]
            new_phase = self.phase_mod(self.oscillator.init_phase, mod_val)
            self.oscillator.phase = new_phase

    def trigger_release(self) -> None:
        for modulator in self.modulators:
            if isinstance(modulator, TriggerableFloatGenerator):
                modulator.trigger_release()

        if isinstance(self.oscillator, TriggerableFloatGenerator):
            self.oscillator.trigger_release()

    @property
    def ended(self) -> bool:
        ended = []
        for modulator in self.modulators:
            if isinstance(modulator, TriggerableFloatGenerator):
                ended.append(modulator.ended)
        if isinstance(self.oscillator, TriggerableFloatGenerator):
            ended.append(self.oscillator.ended)
        return all(ended)

    def __next__(self) -> float:
        mod_vals = [next(mod) for mod in self.modulators]
        self._modulate(mod_vals)
        return next(self.oscillator)
