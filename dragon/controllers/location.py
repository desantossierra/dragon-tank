import abc
import math
import multiprocessing
from multiprocessing.managers import ListProxy
import time

from dragon.conf import SimulationMode, SIMULATION_SLEEP_S
from .controller_abc import ControllerABC


class LocationABC(ControllerABC):

    @abc.abstractmethod
    def locate(self):
        raise NotImplementedError

class LocationReal(LocationABC):
    def __init__(self, sensors, obstacles):
        self.sensors = sensors
        self.obstacles = obstacles

    def locate(self):
        pass

    def loop(self):
        while True:
            self.locate()


class LocationFactory:
    @classmethod
    def create(cls,
               sensors: multiprocessing.Array = None,
               obstacles: multiprocessing.managers.ListProxy = None
               ) -> LocationABC:
        return LocationReal(sensors, obstacles)