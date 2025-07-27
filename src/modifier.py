from typing import Tuple


# A modifier modifies the signal of a generator but doesn't generate its own signal
class Panner:
    def __init__(self, r: float = 0.5) -> None:
        self.r = r

    def __call__(self, val: float):
        # Return tuple value for l r channel
        r: float = self.r * 2.0
        l: float = 2.0 - r
        return (l * val, r * val)
