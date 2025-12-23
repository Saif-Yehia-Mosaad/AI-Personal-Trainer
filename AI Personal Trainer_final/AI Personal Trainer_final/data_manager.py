import csv
from datetime import datetime

class WorkoutDataManager:
    def __init__(self, filename='gym_history.csv'):
        self.filename = filename

    def save(self, left_count, right_count, squat_count, calories, duration):
        try:
            with open(self.filename, mode='a', newline='') as f:
                writer = csv.writer(f)

                date_str = datetime.now().strftime("%Y-%m-%d")
                time_str = datetime.now().strftime("%H:%M:%S")

                writer.writerow([
                    date_str,
                    time_str,
                    left_count,
                    right_count,
                    squat_count,
                    int(calories),
                    duration
                ])

            print("..................Workout Saved Successfully...................")

        except Exception as e:
            print(f"Error saving data: {e}")
