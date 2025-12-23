import numpy as np
from collections import deque
from angle_calculator import AngleCalculator
import mediapipe as mp

mp_pose = mp.solutions.pose

class RightArmCounter:
    def __init__(self):
        self.count = 0
        self.stage = None
        self.smooth_window = deque(maxlen=7)

    def update(self, landmarks):

        shoulder = [
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        ]
        elbow = [
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y
        ]
        wrist = [
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y
        ]


        angle = AngleCalculator.calculate_angle(shoulder, elbow, wrist)

        # smooth 
        self.smooth_window.append(angle)
        smooth_angle = np.mean(self.smooth_window)


        if smooth_angle > 110:
            self.stage = "down"

        if smooth_angle < 40 and self.stage == "down":
            self.stage = "up"
            self.count += 1

        return smooth_angle, self.count, elbow
