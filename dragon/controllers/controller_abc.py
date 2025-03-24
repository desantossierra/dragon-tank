import abc

from dragon.tank_info import TankInfo


class ControllerABC(abc.ABC):
    def __init__(self,
                 tank_info: TankInfo):
        self.tank_info = tank_info

