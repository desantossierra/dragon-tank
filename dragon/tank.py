import math
import multiprocessing
import time

from .conf import SimulationMode
from .controllers import EchoFactory, MotionFactory, VisionFactory, LocationFactory
from .tank_info import TankInfo
from .ui.dashboard import update_dashboard

import platform


class Tank:
    @classmethod
    def create(cls) -> None:

        if platform.machine().startswith("arm"):
            mode = SimulationMode.REAL
        else:
            mode = SimulationMode.SIMULATION

        tank_info = TankInfo()
        tank_info.update_wheels(step_size=0, dangle=0)
        tank_info.update_sonar(distance=50)

        motion = multiprocessing.Process(target=MotionFactory.create, args=(tank_info, mode))
        echo = multiprocessing.Process(target=EchoFactory.create, args=(tank_info, mode))
        vision = multiprocessing.Process(target=VisionFactory.create, args=(tank_info, mode))
        geolocation = multiprocessing.Process(target=LocationFactory.create, args=(tank_info,))

        dashboard = multiprocessing.Process(target=update_dashboard, args=(tank_info,))

        motion.start(), echo.start(), vision.start(), geolocation.start(), dashboard.start()
