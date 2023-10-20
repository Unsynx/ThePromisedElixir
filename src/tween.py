from math import sin, cos, pi
from time import time_ns


class Tween:
    def __init__(self, start_value: int, end_value: int, duration: float, easing_func=None):
        """
        Class used to create animations in one dimension
        :param start_value: start position in pixels
        :param end_value: end position in pixels
        :param duration: duration in milliseconds
        :param easing_func: default linear, options: sine_in_easing, sine_out_easing, quad_in_easing, quad_out_easing
        """
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.current_time = 0
        self.easing_func = easing_func if easing_func else self.linear_easing
        self.start_time = time_ns() // 1_000_000

    def update(self):
        self.current_time = time_ns() // 1_000_000 - self.start_time

    def get_current_value(self):
        if self.current_time >= self.duration:
            return self.end_value
        t = self.current_time / self.duration  # time as float from 0 start to 1 end
        pos = self.start_value + (self.end_value - self.start_value) * self.easing_func(t)
        return int(pos)

    # Easing functions
    @staticmethod
    def linear_easing(t):
        return t

    @staticmethod
    def sine_in_easing(t):
        return 1 - cos((t * pi) / 2)

    @staticmethod
    def sine_out_easing(t):
        return 1 - sin((t * pi) / 2)

    @staticmethod
    def quad_in_easing(t):
        return t * t

    @staticmethod
    def quad_out_easing(t):
        return 1 - (1 - t) * (1 - t)
