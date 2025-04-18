import abc

from .controller_abc import ControllerABC
from ..tank_info import TankInfo


class LocationABC(ControllerABC):

    @abc.abstractmethod
    def locate(self):
        raise NotImplementedError

class LocationReal(LocationABC):

    def locate(self):
        pass

    def loop(self):
        while True:
            self.locate()


class LocationFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo
               ) -> LocationABC:
        return LocationReal(tank_info)