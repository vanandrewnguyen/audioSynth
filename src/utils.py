from dataclasses import dataclass
import math
import random
from src.vec3 import Vec3


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


def hash31(p: Vec3) -> float:
    fract = Vec3(math.fmod(p[0], 1.0), math.fmod(p[1], 1.0), math.fmod(p[2], 1.0))
    fract *= Vec3(0.1031, 0.11369, 0.13787)
    res = math.fmod(Vec3.dot(fract, Vec3(1.0, 1.0, 1.0)), 19.19)
    fract += Vec3(res, res, res)
    return -1.0 + 2.0 * math.fmod((fract[0] + fract[1]) * fract[2], 1.0)


def hash33(p3: Vec3) -> Vec3:
    p = p3 * Vec3(0.1031, 0.11369, 0.13787)
    p = p.fract()
    dot_prod = Vec3.dot(p, Vec3(p[1], p[0], p[2]) + Vec3(19.19, 19.19, 19.19))
    p += Vec3(dot_prod, dot_prod, dot_prod)
    return Vec3(
        -1.0 + 2.0 * math.fmod((p[0] + p[1]) * p[2], 1.0),
        -1.0 + 2.0 * math.fmod((p[0] + p[2]) * p[1], 1.0),
        -1.0 + 2.0 * math.fmod((p[1] + p[2]) * p[0], 1.0),
    )


def clamp(x: float, a_min: float, a_max: float) -> float:
    return max(a_min, min(a_max, x))


def freq_to_vel(hz: float) -> float:
    return hz * 2.0 * Constants.PI


def scale(note_id: int, scale_id: int = Constants.SCALE_DEFAULT):
    if scale_id == Constants.SCALE_DEFAULT:
        return 256 * math.pow(1.0594630943592952645618252949463, note_id)
    return 0.0
