import abc

from .controller_abc import ControllerABC
from ..tank_info import TankInfo


class DriverABC(ControllerABC):
    """
    Driver aims to collect all the information from the sensors, integrates them and decides what movement to do next.
    """

    @abc.abstractmethod
    def locate(self):
        raise NotImplementedError

class DriverReal(DriverABC):

    def locate(self):
        pass

    def loop(self):
        while True:
            self.locate()


class DriverFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo
               ) -> DriverABC:
        return DriverReal(tank_info)