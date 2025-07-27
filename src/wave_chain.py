from collections.abc import Iterable, Iterator
from src.oscillators.base_oscillator import Generator
from src.modulator import TriggerableFloatGenerator, ModulatorType
from typing import Union, Iterator, Callable, Tuple, Any


class WaveAdder(Generator):
    # By default stereo is false, no panning
    def __init__(self, *generators: Iterator, stereo: bool = False) -> None:
        self.generators: Tuple[Iterator, ...] = generators
        self.stereo: bool = stereo

    def _mod_channels(
        self, _val: Union[float, int, Iterable]
    ) -> Union[float, Tuple[float, float]]:
        val: Union[float, Tuple[float, float]] = _val

        if isinstance(_val, (int, float)) and self.stereo:
            val = (_val, _val)
        elif isinstance(_val, Iterable) and not self.stereo:
            nums = list(_val)
            val = sum(nums) / len(nums)
        return val

    def trigger_release(self) -> None:
        for gen in self.generators:
            if isinstance(gen, TriggerableFloatGenerator):
                gen.trigger_release()

    @property
    def ended(self) -> bool:
        return all(getattr(gen, "ended", False) for gen in self.generators)

    def __iter__(self) -> "WaveAdder":
        for gen in self.generators:
            iter(gen)

        return self

    def __next__(self):
        vals = [self._mod_channels(next(gen)) for gen in self.generators]

        if self.stereo:
            l, r = zip(*vals)
            return (sum(l) / len(l), sum(r) / len(r))
        else:
            return sum(vals) / len(vals)


class Chain:
    def __init__(
        self, generator: Union[Iterator[float], ModulatorType], *modifiers: Any
    ) -> None:
        self.generator: Union[Iterator[float], ModulatorType] = generator
        self.modifiers: Any = modifiers

    def __getattr__(self, attr: str):
        if hasattr(self.generator, attr):
            return getattr(self.generator, attr)

        for modifier in self.modifiers:
            if hasattr(modifier, attr):
                return getattr(modifier, attr)

        raise AttributeError(f"attribute '{attr}' does not exist")

    def trigger_release(self) -> None:
        for modulator in self.modulators:
            if isinstance(modulator, TriggerableFloatGenerator):
                modulator.trigger_release()

        if isinstance(self.oscillator, TriggerableFloatGenerator):
            self.oscillator.trigger_release()

    @property
    def ended(self) -> bool:
        ended = []

        if isinstance(self.generator, TriggerableFloatGenerator):
            ended.append(self.generator.ended)
        ended.extend(
            [
                mod.ended
                for mod in self.modifiers
                if isinstance(mod, TriggerableFloatGenerator)
            ]
        )

        return all(ended)

    def __iter__(self) -> "Chain":
        iter(self.generator)

        for mod in self.modifiers:
            if isinstance(mod, TriggerableFloatGenerator):
                iter(mod)

        return self

    def __next__(self) -> float:
        val = next(self.generator)

        for mod in self.modifiers:
            if isinstance(mod, TriggerableFloatGenerator):
                next(mod)

        for mod in self.modifiers:
            val = mod(val)

        return val
