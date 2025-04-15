import math
import multiprocessing
import time

OBSTACLE_MEMORY = 2000


class TankInfo:
    def __init__(self):
        self.wheels = multiprocessing.Array('d', 4)
        self.wheels[1], self.wheels[2] = 250, 250

        self.sonar = multiprocessing.Array('d', 2)
        self.obstacles = multiprocessing.Array('d', OBSTACLE_MEMORY)
        self.obstacles_idx = multiprocessing.Array('d', 2)
        self.obstacles_idx[0] = 0      # ix
        self.obstacles_idx[1] = 0      # counter

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

        ix = int(self.obstacles_idx[0])
        c = int(self.obstacles_idx[1])

        if c >= 2:
            last_x, last_y = self.obstacles[(ix-2)%OBSTACLE_MEMORY], self.obstacles[(ix-1)%OBSTACLE_MEMORY]
            distance = math.sqrt((last_x - x_final) ** 2 + (last_y - y_final) ** 2)
            if distance < 10.01:
                return

        self.obstacles[ix] = x_final
        self.obstacles[ix+1] = y_final
        self.obstacles_idx[0] = (ix + 2) % OBSTACLE_MEMORY
        self.obstacles_idx[1] = min((c + 2), OBSTACLE_MEMORY)

    def obstacles_coordinates(self):
        return [(self.obstacles[i], self.obstacles[i+1])
                for i in range(0, int(self.obstacles_idx[1]), 2)]


