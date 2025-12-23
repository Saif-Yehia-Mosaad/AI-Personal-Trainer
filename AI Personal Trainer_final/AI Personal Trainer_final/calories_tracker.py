class CaloriesCalculator:
    def __init__(self, left_arm_factor=0.3, right_arm_factor=0.3, squat_factor=0.5):
        self.left_arm_factor = left_arm_factor
        self.right_arm_factor = right_arm_factor
        self.squat_factor = squat_factor
        self.calories = 0

    def update(self, count_L, count_R, count_squat):
        self.calories = (count_L * self.left_arm_factor +
                         count_R * self.right_arm_factor +
                         count_squat * self.squat_factor)
        return self.calories

    def get_calories(self):
        return int(self.calories)
