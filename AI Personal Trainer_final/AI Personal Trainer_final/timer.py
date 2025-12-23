import time

class WorkoutTimer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def get_elapsed(self):
        if self.start_time is None:
            return "00:00"
        seconds = int(time.time() - self.start_time)
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
