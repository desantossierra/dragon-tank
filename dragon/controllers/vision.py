import multiprocessing

from dragon.conf import SimulationMode
from dragon.controllers.controller_abc import ControllerABC
from dragon.tank_info import TankInfo


class VisionABC(ControllerABC):
    """
    Vision controls the camera.
    TODO: it detects objects and decides if something is of interest. It tries to locate it into the space and send the
    TODO: position as new target.
    """
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