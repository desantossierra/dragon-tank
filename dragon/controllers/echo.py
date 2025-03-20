import math
import multiprocessing
import time

import numpy as np

from dragon.conf import SimulationMode
from .controller_abc import ControllerABC
from ..ui.dashboard import update_dashboard


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

        self.x, self.y, self.angle = 0, 0, 0  # to store last known robot position

    def echo(self):
        if not self.position.empty():
            x, y, angle = self.position.get()
            if x != self.x or y != self.y or angle != self.angle:
                self.x, self.y, self.angle = x, y, angle
                if not (0 <= x < self.map.shape[0] and 0 <= y < self.map.shape[1]):
                    self.distance.put(0)
                    return 0
                angle_rad = math.radians(angle)
                dx, dy = math.cos(angle_rad), math.sin(angle_rad)
                distance = 0

                while 0 <= x < self.map.shape[0] and 0 <= y < self.map.shape[1]:
                    if self.map[int(x), int(y)] == 1:
                        self.distance.put(distance)
                        return distance

                    x += dx
                    y += dy
                    distance += 1
                    if distance > EchoSim.MAX_DISTANCE:
                        self.distance.put(distance)
                        return distance

                self.distance.put(distance)
                return distance
        else:
            print("Echo, position queue empty")

    def loop(self):
        while True:
            d = self.echo()
            update_dashboard({'x': self.x,
                              'y': self.y,
                              'angle': self.angle,
                              'sonar_distance': d})
            time.sleep(0.2)


class EchoFactory:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION,
               distance: multiprocessing.Queue = None,
               position: multiprocessing.Queue = None) -> EchoABC:
        if mode == SimulationMode.SIMULATION:
            return EchoSim(500, 500, distance, position).loop()
        else:
            return EchoReal(distance, position)