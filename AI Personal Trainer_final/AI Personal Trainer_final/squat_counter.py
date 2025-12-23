import numpy as np
from collections import deque
from angle_calculator import AngleCalculator
import mediapipe as mp

mp_pose = mp.solutions.pose

class SquatCounter:
    def __init__(self):
        self.count = 0
        self.stage = None
        self.smooth_window = deque(maxlen=10)

    def update(self, landmarks):

        hipL = [
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
        ]
        kneeL = [
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y
        ]
        ankleL = [
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
        ]
        angleL = AngleCalculator.calculate_angle(hipL, kneeL, ankleL)


        hipR = [
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y
        ]
        kneeR = [
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y
        ]
        ankleR = [
            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
        ]
        angleR = AngleCalculator.calculate_angle(hipR, kneeR, ankleR)

        avg_angle = (angleL + angleR) / 2


        self.smooth_window.append(avg_angle)
        smooth_angle = np.mean(self.smooth_window)


        if smooth_angle < 140:
            self.stage = "down"

        if smooth_angle > 160 and self.stage == "down":
            self.stage = "up"
            self.count += 1


        return smooth_angle, self.count, kneeL
