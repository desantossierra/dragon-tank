import abc
import math

from .controller_abc import ControllerABC
from ..tank_info import TankInfo
from ..utils.math import two_point_distance, calculate_forces


class DriverABC(ControllerABC):
    """
    Driver aims to collect all the information from the sensors, integrates them and decides what movement to do next.
    """

    @abc.abstractmethod
    def locate(self):
        raise NotImplementedError

    def direction_to_goal(self):
        x_goal, y_goal = self.tank_info.get_goal()
        x_robot, y_robot = self.tank_info.get_position()
        angle_robot = self.tank_info.get_direction()
        dx, dy = x_goal - x_robot, y_goal - y_robot

        radians = math.atan2(dy, dx)
        degrees = round(math.degrees(radians) - angle_robot) % 360
        return degrees

    def gradient_direction(self):
        x_goal, y_goal = self.tank_info.get_goal()
        x_robot, y_robot = self.tank_info.get_position()
        angle_robot = self.tank_info.get_direction()
        ang, force = calculate_forces((x_robot, y_robot), [(x_goal, y_goal)])
        rep_ang, rep_force = calculate_forces((x_robot, y_robot), self.tank_info.obstacles_coordinates(), attractive=False)

        if abs(ang - (rep_ang + 180) % 360) < 10:
            return 45
        ang = (ang * force + rep_ang * rep_force) / (force + rep_force)
        degrees = round(ang - angle_robot) % 360
        return degrees

    def loop(self):
        while True:
            degree = self.gradient_direction()
            self.tank_info.update_driver_direction(degree)

class DriverReal(DriverABC):

    def locate(self):
        pass



class DriverFactory:
    @classmethod
    def create(cls,
               tank_info: TankInfo
               ) -> DriverABC:
        return DriverReal(tank_info).loop()