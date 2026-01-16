import abc
import math
import multiprocessing
import time
import random

from dragon.conf import SimulationMode, SIMULATION_SLEEP_S
from .controller_abc import ControllerABC
from ..tank_info import TankInfo

import platform
if platform.machine().startswith("arm"):
    from dragon.io.wheels import Wheels


class MotionABC(ControllerABC):
    """
    Motion aims to control the wheels. It sends information about the movement: forward, backward or turns.
    It implements some sort of mechanism to avoid collision without intervention of the Driver.
    """

    @abc.abstractmethod
    def walk(self):
        raise NotImplementedError

    @abc.abstractmethod
    def turn(self, angle):
        raise NotImplementedError

    def loop(self):

        move_away_from_obstacle = 0
        while True:
            is_obstacle = self.tank_info.get_distance() <= 20
            if is_obstacle:
                self.find_free_space()
                move_away_from_obstacle = 100
            else:
                direction = self.tank_info.get_driver_direction()
                if direction == 0 or move_away_from_obstacle > 0:
                    self.walk()
                    move_away_from_obstacle -= 1
                else:
                    self.turn(angle=direction)

    def find_free_space(self):
        max_d, max_i = self.tank_info.get_distance(), 0
        left = -1 if random.random() < 0.5 else 1
        for i in range(36):  # 360 turn to find a space without obstacles
            self.turn(10 * left)
            d = self.tank_info.get_distance()
            if d > max_d:
                max_d = d
                max_i = i

        max_i += 1
        self.turn(max_i*10*left)

class MotionReal(MotionABC):
    def __init__(self, *args, **kwargs):
        print("Motion Real")
        super().__init__(*args, **kwargs)
        self.wheels = Wheels()
        self.wheels.setup()

    def walk(self):
        self.wheels.forward(50)
        self.tank_info.update_wheels(1, 0)

    def turn(self, angle):
        self.wheels.turn_degrees(angle)
        self.tank_info.update_wheels(0, angle)


class MotionSim(MotionABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.step_size = 1

    def walk(self):
        time.sleep(SIMULATION_SLEEP_S)
        self.tank_info.update_wheels(self.step_size, 0)

    def turn(self, angle):
        time.sleep(SIMULATION_SLEEP_S)
        self.tank_info.update_wheels(0, angle)



class MotionFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo,
               mode:SimulationMode = SimulationMode.SIMULATION) -> MotionABC:
        if mode == SimulationMode.SIMULATION:
            return MotionSim(tank_info).loop()
        else:
            return MotionReal(tank_info).loop()