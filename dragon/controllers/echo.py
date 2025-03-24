import math
import multiprocessing
import time
from multiprocessing.util import MAXFD

import numpy as np

from dragon.conf import SimulationMode, SIMULATION_SLEEP_S
from .controller_abc import ControllerABC
from ..tank_info import TankInfo


class EchoABC(ControllerABC):
    pass

class EchoReal(EchoABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EchoSim(EchoABC):
    MAX_DISTANCE = 50
    def __init__(self, width=800, height=800, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = np.zeros((width, height))
        self.map[:100,:100] = 1 # a couple of obstacles
        self.map[400:450, 400:450] = 1

    def echo(self):
        (x, y), angle = self.tank_info.get_position(), self.tank_info.get_direction()
        if not (0 <= x < self.map.shape[0] and 0 <= y < self.map.shape[1]):
            return 0

        angle_rad = math.radians(angle)
        dx, dy = math.cos(angle_rad), math.sin(angle_rad)
        distance = 0

        while 0 <= x < self.map.shape[0] and 0 <= y < self.map.shape[1]:
            if self.map[int(x), int(y)] == 1:
                return distance

            x += dx
            y += dy
            distance += 1
            if distance > EchoSim.MAX_DISTANCE:
                return distance

        return distance

    def loop(self):
        while True:
            d = self.echo()
            self.tank_info.update_sonar(d)
            if d < EchoSim.MAX_DISTANCE:
                self.tank_info.add_obstacle()

            time.sleep(SIMULATION_SLEEP_S)


class EchoFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo,
               mode:SimulationMode = SimulationMode.SIMULATION) -> EchoABC:
        if mode == SimulationMode.SIMULATION:
            return EchoSim(500, 500, tank_info).loop()
        else:
            return EchoReal(tank_info)