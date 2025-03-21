import abc
import math
import multiprocessing
import time

from dragon.conf import SimulationMode, SIMULATION_SLEEP_S
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
        self.step_size = 1

    def walk(self):

        # Convert angle to radians
        angle_rad = math.radians(self.location[2])

        # Calculate the change in x and y
        dx = self.step_size * math.cos(angle_rad)
        dy = self.step_size * math.sin(angle_rad)

        # Update the position
        self.location[0] += dx
        self.location[1] += dy

    def turn(self):
        self.location[2] = (self.location[2] + 100) % 360
        self.walk()

    def loop(self):
        print("Motion loop")
        while True:
            aux = {'x': self.location[0],
                   'y': self.location[1],
                   'angle': self.location[2],
                   'sonar_distance': self.location[3]}
            if self.location[3] > 20:
                print(f"Moving forward: {aux}")
                self.walk()
            else:

                print(f"Oh oh, obstacle! let's turn: {aux}")
                self.turn()

            time.sleep(SIMULATION_SLEEP_S)

class MotionFactory:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION,
               location: multiprocessing.Array = None
               ) -> MotionABC:
        if mode == SimulationMode.SIMULATION:
            return MotionSim(location).loop()
        else:
            return MotionReal(location)