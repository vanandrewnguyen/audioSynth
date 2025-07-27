from __future__ import annotations
import math
import random
from typing import List, Union


class Vec3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.e: List[float] = [x, y, z]

    def __getitem__(self, i: int):
        return self.e[i]

    def __setitem__(self, i: int, value: float):
        self.e[i] = value

    def __add__(self, other: Vec3) -> Vec3:
        return Vec3(self[0] + other[0], self[1] + other[1], self[2] + other[2])

    def __sub__(self, other: Vec3) -> Vec3:
        return Vec3(self[0] - other[0], self[1] - other[1], self[2] - other[2])

    def __mul__(self, other: Union[Vec3, float]) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self[0] * other[0], self[1] * other[1], self[2] * other[2])
        return Vec3(self[0] * other, self[1] * other, self[2] * other)

    def __rmul__(self, other: Union[Vec3, float]) -> Vec3:
        return self * other

    def __truediv__(self, other: Union[Vec3, float]) -> Vec3:
        if isinstance(other, Vec3):
            return Vec3(self[0] / other[0], self[1] / other[1], self[2] / other[2])
        return Vec3(self[0] / other, self[1] / other, self[2] / other)

    def __neg__(self):
        return Vec3(-self[0], -self[1], -self[2])

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self[0] ** 2 + self[1] ** 2 + self[2] ** 2

    def make_unit_vec(self):
        k = 1.0 / self.length()
        self.e = [self[0] * k, self[1] * k, self[2] * k]

    def near_zero(self):
        s = 1e-8
        return abs(self[0]) < s and abs(self[1]) < s and abs(self[2]) < s

    def fract(self):
        return Vec3(
            math.fmod(self[0], 1.0), math.fmod(self[1], 1.0), math.fmod(self[2], 1.0)
        )

    def floor(self):
        return Vec3(math.floor(self[0]), math.floor(self[1]), math.floor(self[2]))

    def mod(self, other: Vec3, scale: Vec3):
        return Vec3(
            math.fmod(self[0] + other[0], scale[0]),
            math.fmod(self[1] + other[1], scale[1]),
            math.fmod(self[2] + other[2], scale[2]),
        )

    @staticmethod
    def dot(v1: Vec3, v2: Vec3):
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]

    @staticmethod
    def cross(v1: Vec3, v2: Vec3):
        return Vec3(
            v1[1] * v2[2] - v1[2] * v2[1],
            -(v1[0] * v2[2] - v1[2] * v2[0]),
            v1[0] * v2[1] - v1[1] * v2[0],
        )

    @staticmethod
    def unit_vector(v: Vec3) -> Vec3:
        return v / v.length()

    @staticmethod
    def rand_in_unit_sphere():
        while True:
            p = Vec3(
                random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
            )
            if p.length_squared() < 1.0:
                return p

    @staticmethod
    def reflect(v: Vec3, n: Vec3):
        return v - 2 * Vec3.dot(v, n) * n

    @staticmethod
    def refract(v: Vec3, n: Vec3, ior: float):
        uv = Vec3.unit_vector(v)
        dt = Vec3.dot(uv, n)
        discriminant = 1.0 - ior * ior * (1 - dt * dt)
        if discriminant > 0:
            return True, ior * (uv - n * dt) - n * math.sqrt(discriminant)
        return False, None

    @staticmethod
    def shlick(cosine: float, ior: float):
        r0 = (1 - ior) / (1 + ior)
        r0 = r0 * r0
        return r0 + (1 - r0) * math.pow((1 - cosine), 5)

    @staticmethod
    def mix(a: Vec3, b: Vec3, t: float):
        return a * (1.0 - t) + b * t
