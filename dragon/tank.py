import multiprocessing

from .conf import SimulationMode
from .controllers import EchoFactory, MotionFactory, VisionFactory, LocationFactory
from .ui.dashboard import update_dashboard


class Tank:
    @classmethod
    def create(cls, mode:SimulationMode = SimulationMode.SIMULATION) -> None:
        sensors = multiprocessing.Array('d', 4)
        location = multiprocessing.Array('d', 4)

        sensors[0], sensors[1], sensors[2], sensors[3] = 250, 250, 0, 50
        manager = multiprocessing.Manager()
        obstacles = manager.list()

        echo = multiprocessing.Process(target=EchoFactory.create, args=(mode, sensors))
        motion = multiprocessing.Process(target=MotionFactory.create, args=(mode, sensors))
        vision = multiprocessing.Process(target=VisionFactory.create, args=(mode, sensors))
        geolocation = multiprocessing.Process(target=LocationFactory.create, args=(mode, sensors, obstacles))

        dashboard = multiprocessing.Process(target=update_dashboard, args=(location,))

        echo.start(), motion.start(), vision.start(), geolocation.start(), dashboard.start()
