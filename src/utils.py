from dataclasses import dataclass
from enum import Enum
import math
import random

# from src.vec3 import Vec3


@dataclass
class Constants:
    INFINITY = float("inf")
    PI = math.pi
    EPSILON = 1e-4
    SCALE_DEFAULT = 0


def random_double_normalised():
    return random.random()


def random_double():
    return random.uniform(-1.0, 1.0)


def random_double_range(min_range: float, max_range: float) -> float:
    return min_range + (max_range - min_range) * random_double()


def random_int(min_range: int, max_range: int) -> int:
    return random.randint(min_range, max_range)


# def hash21(co):
#     return math.fmod(math.sin(co[0] * 12.9898 + co[1] * 78.233) * 43758.5453, 1.0)


# def hash31(p):
#     fract = Vec3(math.fmod(p[0], 1.0), math.fmod(p[1], 1.0), math.fmod(p[2], 1.0))
#     fract *= Vec3(0.1031, 0.11369, 0.13787)
#     res = math.fmod(Vec3.dot(fract, Vec3(1.0, 1.0, 1.0)), 19.19)
#     fract += Vec3(res, res, res)
#     return -1.0 + 2.0 * math.fmod((fract[0] + fract[1]) * fract[2], 1.0)


# def hash33(p3):
#     p = p3 * Vec3(0.1031, 0.11369, 0.13787)
#     p = p.fract()
#     dot_prod = Vec3.dot(p, Vec3(p[1], p[0], p[2]) + Vec3(19.19, 19.19, 19.19))
#     p += Vec3(dot_prod, dot_prod, dot_prod)
#     return Vec3(
#         -1.0 + 2.0 * math.fmod((p[0] + p[1]) * p[2], 1.0),
#         -1.0 + 2.0 * math.fmod((p[0] + p[2]) * p[1], 1.0),
#         -1.0 + 2.0 * math.fmod((p[1] + p[2]) * p[0], 1.0),
#     )


def clamp(x: float, a_min: float, a_max: float) -> float:
    return max(a_min, min(a_max, x))


def freq_to_vel(hz: float) -> float:
    return hz * 2.0 * Constants.PI


def scale(note_id: int, scale_id: int = Constants.SCALE_DEFAULT):
    if scale_id == Constants.SCALE_DEFAULT:
        return 256 * math.pow(1.0594630943592952645618252949463, note_id)
    return 0.0


class WaveForm(Enum):
    OSC_SINE = 0
    OSC_SQUARE = 1
    OSC_TRIANGLE = 2
    OSC_SAW_LIM = 3
    OSC_SAW = 4
    OSC_NOISE = 5


def osc(
    time: float,
    hz: float,
    wave_type: WaveForm = WaveForm.OSC_SINE,
    lfo_hz: float = 0.0,
    lfo_amp: float = 0.0,
    custom: float = 50.0,
):
    freq = freq_to_vel(hz) * time + lfo_amp * hz * math.sin(freq_to_vel(lfo_hz) * time)

    if wave_type == WaveForm.OSC_SINE:
        return math.sin(freq)
    elif wave_type == WaveForm.OSC_SQUARE:
        return 1.0 if math.sin(freq) > 0.0 else -1.0
    elif wave_type == WaveForm.OSC_TRIANGLE:
        return math.asin(math.sin(freq)) * 2.0 / Constants.PI
    elif wave_type == WaveForm.OSC_SAW_LIM:
        return sum(math.sin(i * freq) / i for i in range(1, 100)) * (2.0 / Constants.PI)
    elif wave_type == WaveForm.OSC_SAW:
        return (2.0 / Constants.PI) * (
            hz * Constants.PI * math.fmod(time, 1.0 / hz) - (Constants.PI / 2.0)
        )
    elif wave_type == WaveForm.OSC_NOISE:
        return random_double()
    else:
        return 0.0
