import time
import traceback
from collections import deque
from threading import Thread, RLock


class Manager:
    def __init__(self, runner_count=1, interval=0.1):
        self.interval = interval
        self.runner_count = runner_count
        self.task_in_progress = 0
        self.queue = deque()
        self.lock = RLock()
        self.alive = False
        self.runners = []
        for i in range(self.runner_count):
            self.runners.append(
                Thread(name=f"runner_{i}", target=self.runner)
            )

    def runner(self):
        while self.alive:
            with self.lock:
                self.alive = self._check_alive()
                if len(self.queue) == 0:
                    time.sleep(self.interval)
                    continue

                task = self.queue.popleft()
                self.task_in_progress += 1

            try:
                task()
            except Exception as e:
                traceback.print_exception(Exception, e, e.__traceback__)

            with self.lock:
                self.task_in_progress -= 1

    def _check_alive(self):
        """Thread unsave"""
        return self.task_in_progress > 0 or len(self.queue) > 0

    def run(self):
        self.alive = True
        for runner in self.runners:
            runner.start()

        for runner in self.runners:
            runner.join()
