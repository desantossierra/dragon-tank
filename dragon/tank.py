import multiprocessing

from .conf import SimulationMode
from .controllers import EchoFactory, MotionFactory, VisionFactory
from .ui.dashboard import update_dashboard


class Tank:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION) -> None:
        location = multiprocessing.Array('d', 4)
        location[0], location[1], location[2], location[3] = 250, 250, 0, 50

        echo = multiprocessing.Process(target=EchoFactory.create, args=(mode, location))
        motion = multiprocessing.Process(target=MotionFactory.create, args=(mode, location))
        vision = multiprocessing.Process(target=VisionFactory.create, args=(mode, location))

        dashboard = multiprocessing.Process(target=update_dashboard, args=(location,))

        echo.start(), motion.start(), vision.start(), dashboard.start()
