import abc
import math
import multiprocessing
import time

from dragon.conf import SimulationMode
from .controller_abc import ControllerABC


class MotionABC(ControllerABC):

    @abc.abstractmethod
    def walk(self):
        raise NotImplementedError

class MotionReal(MotionABC):
    def walk(self):
        pass

class MotionSim(MotionABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = 0
        self.x, self.y = 250, 250
        self.step_size = 1

    def walk(self):

        # Convert angle to radians
        angle_rad = math.radians(self.angle)

        # Calculate the change in x and y
        dx = self.step_size * math.cos(angle_rad)
        dy = self.step_size * math.sin(angle_rad)

        # Update the position
        self.x += dx
        self.y += dy
        self.position.put((self.x, self.y, self.angle))

    def turn(self):
        self.angle = (self.angle + 45) % 360
        self.walk()

    def loop(self):
        print("Motion loop")
        while True:
            queue_empty = self.distance.empty()
            distance = 50 if queue_empty else self.distance.get()
            if queue_empty or distance > 20:
                print(f"Moving forward: {self.x}, {self.y}, {self.angle} {queue_empty}, {distance}")
                self.walk()
            else:
                print(f"Oh oh, obstacle! let's turn:{queue_empty}, {distance}")
                self.turn()

            time.sleep(0.2)

class MotionFactory:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION,
               distance: multiprocessing.Queue = None,
               position: multiprocessing.Queue = None
               ) -> MotionABC:
        if mode == SimulationMode.SIMULATION:
            return MotionSim(distance, position).loop()
        else:
            return MotionReal(distance, position)