import abc
import math
import multiprocessing
import time

from dragon.conf import SimulationMode, SIMULATION_SLEEP_S
from .controller_abc import ControllerABC
from ..tank_info import TankInfo

import platform
if platform.machine().startswith("arm"):
    from dragon.io.wheels import Wheels


class MotionABC(ControllerABC):

    @abc.abstractmethod
    def walk(self):
        raise NotImplementedError

class MotionReal(MotionABC):
    def __init__(self, *args, **kwargs):
        print("Motion Real")
        super().__init__(*args, **kwargs)
        self.wheels = Wheels()
        self.wheels.setup()

    def walk(self):
        self.wheels.forward(50)
        self.tank_info.update_wheels(1, 0)

    def turn(self):
        print("Motion Real turning")
        self.wheels.turn_left(90, 1)
        while self.tank_info.get_distance() < 50:
            pass
        self.wheels.forward(50)

    def loop(self):
        print("Motion loop")
        while True:
            if self.tank_info.get_distance() > 30:
                self.walk()
            else:
                self.turn()

class MotionSim(MotionABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step_size = 1

    def walk(self):
        self.tank_info.update_wheels(self.step_size, 0)

    def turn(self):
        self.tank_info.update_wheels(0, 100)

    def loop(self):
        print("Motion loop")
        while True:
            if self.tank_info.get_distance() > 20:
                self.walk()
            else:
                self.turn()

            time.sleep(SIMULATION_SLEEP_S)

class MotionFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo,
               mode:SimulationMode = SimulationMode.SIMULATION) -> MotionABC:
        if mode == SimulationMode.SIMULATION:
            return MotionSim(tank_info).loop()
        else:
            return MotionReal(tank_info).loop()