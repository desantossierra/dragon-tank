import multiprocessing

from .conf import SimulationMode
from .controllers import EchoFactory, MotionFactory, VisionFactory

class Tank:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION) -> None:
        distance_queue = multiprocessing.Queue()
        position_queue = multiprocessing.Queue()

        echo = multiprocessing.Process(target=EchoFactory.create, args=(mode, distance_queue, position_queue))
        motion = multiprocessing.Process(target=MotionFactory.create, args=(mode, distance_queue, position_queue))
        vision = multiprocessing.Process(target=VisionFactory.create, args=(mode, distance_queue, position_queue))

        echo.start(), motion.start(), vision.start()
