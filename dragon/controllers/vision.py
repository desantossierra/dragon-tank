import multiprocessing

from dragon.conf import SimulationMode
from dragon.controllers.controller_abc import ControllerABC
from dragon.tank_info import TankInfo


class VisionABC(ControllerABC):
    pass

class VisionReal(VisionABC):
    pass

class VisionSim(VisionABC):
    pass

class VisionFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo,
               mode:SimulationMode = SimulationMode.SIMULATION) -> VisionABC:
        if mode == SimulationMode.SIMULATION:
            return VisionSim(tank_info)
        else:
            return VisionReal(tank_info)