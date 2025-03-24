import math
import multiprocessing
import time
import traceback


class TankInfo:
    def __init__(self):
        self.wheels = multiprocessing.Array('d', 4)
        self.wheels[1], self.wheels[2] = 250, 250

        self.sonar = multiprocessing.Array('d', 2)
        self.obstacles = multiprocessing.Array('d', 2002)
        self.obstacles[2000] = 0
        self.obstacles[2001] = 0

    def get_distance(self):
        return self.sonar[1]

    def get_position(self):
        return self.wheels[1], self.wheels[2]

    def get_direction(self):
        return self.wheels[3]

    def update_wheels(self, step_size, dangle):
        self.wheels[3] = (self.wheels[3] + dangle) % 360
        angle_rad = math.radians(self.wheels[3])
        self.wheels[1] += step_size * math.cos(angle_rad)
        self.wheels[2] += step_size * math.sin(angle_rad)
        self.wheels[0] = time.time()

    def update_sonar(self, distance):
        self.sonar[1] = distance
        self.sonar[0] = time.time()

    def add_obstacle(self):
        direction = self.get_direction()
        distance = self.get_distance()
        x, y = self.get_position()

        angle = math.radians(direction)
        x_final = x + distance * math.cos(angle)
        y_final = y + distance * math.sin(angle)

        ix = int(self.obstacles[2000])
        # for i in range(0, int(self.obstacles[2001]), 2):
        #     if self.obstacles[i] == x_final  and self.obstacles[i+1] == y_final:
        #         return
        self.obstacles[ix] = x_final
        self.obstacles[ix+1] = y_final
        self.obstacles[2000] = (ix + 2) % 2000
        self.obstacles[2001] = min((self.obstacles[2001] + 2), 2000)

    def obstacles_coordinates(self):
        return [(self.obstacles[i], self.obstacles[i+1])
                for i in range(0, int(self.obstacles[2001]), 2)]


