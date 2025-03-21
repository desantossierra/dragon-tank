import multiprocessing

from dragon.conf import SimulationMode
from dragon.controllers.controller_abc import ControllerABC


class VisionABC(ControllerABC):
    pass

class VisionReal(VisionABC):
    pass

class VisionSim(VisionABC):
    pass

class VisionFactory:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION,
               location: multiprocessing.Array = None) -> VisionABC:
        if mode == SimulationMode.SIMULATION:
            return VisionSim(location)
        else:
            return VisionReal(location)