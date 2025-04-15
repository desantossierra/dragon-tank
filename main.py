import multiprocessing
import queue
import time

from dragon.conf import SimulationMode
from dragon.tank import Tank
from dragon.ui.dashboard import app, update_dashboard
from dragon.utils.math import two_point_angle


def wheels_and_clip(distance_queue, position_queue):
    x, y = 250, 250
    while True:
        if distance_queue.empty():
            print(f"wheels_and_clip: Me estoy desplazando {x}")
            x += 1
            y += 1
            position_queue.put((x, y))
        else:
            distance = distance_queue.get()
            if distance < 10:
                print(f"wheels_and_clip: Me paro")
            else:
                print(f"wheels_and_clip: Me estoy desplazando {x}")
                x += 1
                position_queue.put((x, y))

        time.sleep(1)

def sonar(distance_queue):
    distance = 3
    while True:
        distance = (distance + 3) % 25
        distance_queue.put(distance)
        print(f"sonar: {distance}")
        time.sleep(2.5)

def mapa(distance_queue, position_queue):
    x, y, angle, distance = 250, 250, 0, 0
    while True:
        new_pos = False
        if not distance_queue.empty():
            distance = distance_queue.get()
            new_pos = True
        if not position_queue.empty():
            xn, yn = position_queue.get()
            x, y, angle = xn, yn, two_point_angle((x, y), (xn, yn))
            new_pos = True
        if new_pos:
            shared_data = {'x': x, 'y': y, 'angle': angle, 'sonar_distance': distance}
            update_dashboard(shared_data)

if __name__ == "__main__":

    Tank.create()
    app.run(debug=True, use_reloader=False) #use_reloader=False para evitar que se dupliquen los procesos.

#     try:
#         while True:
#             time.sleep(100)
#     except:
#         from dragon.io.wheels import Wheels
#         wheels = Wheels()
#         wheels.setup()
#         wheels.stop()
#         wheels.cleanup()

    print("Todos los procesos han terminado.")