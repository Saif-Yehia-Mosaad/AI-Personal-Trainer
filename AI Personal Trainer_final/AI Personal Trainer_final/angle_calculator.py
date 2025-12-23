import numpy as np

class AngleCalculator:
    @staticmethod
    def calculate_angle(a, b, c):
        """
        Calculate angle between three points a, b, c
        b is the joint (vertex)
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])

        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
