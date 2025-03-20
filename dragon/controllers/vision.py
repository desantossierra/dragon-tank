import abc
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
               distance: multiprocessing.Queue = None,
               position: multiprocessing.Queue = None) -> VisionABC:
        if mode == SimulationMode.SIMULATION:
            return VisionSim(distance, position)
        else:
            return VisionReal(distance, position)