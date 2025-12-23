import cv2
import numpy as np

# MediaPipe updated imports
from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

# Workout modules
from left_arm_counter import LeftArmCounter
from right_arm_counter import RightArmCounter
from squat_counter import SquatCounter
from timer import WorkoutTimer
from calories_tracker import CaloriesCalculator
from data_manager import WorkoutDataManager

# ================= INIT MODULES =================
left_arm = LeftArmCounter()
right_arm = RightArmCounter()
squat = SquatCounter()
calories_tracker = CaloriesCalculator()
data_manager = WorkoutDataManager()
timer = WorkoutTimer()

cap = cv2.VideoCapture(0)
timer.start()

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False
        results = pose.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            h, w, _ = img.shape

            # Left arm
            angleL, count_L, elbowL = left_arm.update(landmarks)
            cv2.putText(
                img,
                str(int(angleL)),
                tuple(np.multiply(elbowL, [w, h]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Right arm
            angleR, count_R, elbowR = right_arm.update(landmarks)
            cv2.putText(
                img,
                str(int(angleR)),
                tuple(np.multiply(elbowR, [w, h]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Squat
            angle_squat, count_squat, kneeL = squat.update(landmarks)
            cv2.putText(
                img,
                str(int(angle_squat)),
                tuple(np.multiply(kneeL, [w, h]).astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Timer
            timer_text = timer.get_elapsed()

            # Calories
            calories = calories_tracker.update(count_L, count_R, count_squat)

            # Info box
            cv2.rectangle(img, (0, 0), (180, 220), (175, 223, 228), -1)
            cv2.putText(img, "Left: {}".format(count_L), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(img, "Right: {}".format(count_R), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(img, "Squat: {}".format(count_squat), (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(img, "Time: {}".format(timer_text), (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            cv2.putText(img, "Kcal: {}".format(int(calories)), (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2),

        except:
            pass

        # ================= DRAW POSE =================
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                img,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(48, 196, 222), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(79, 98, 81), thickness=2, circle_radius=2)
            )

        cv2.imshow('MediaPipe Feed', img)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            print("Exiting program...")
            break

cap.release()
cv2.destroyAllWindows()

# ================= SAVE WORKOUT =================
data_manager.save(
    left_count=left_arm.count,
    right_count=right_arm.count,
    squat_count=squat.count,
    calories=int(calories),
    duration=timer.get_elapsed()
)
