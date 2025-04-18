from wheels import Wheels
from sonar import Sonar
from time import time, sleep
import pandas as pd
from rich.prompt import Prompt
import numpy as np

DEGREE_TS_100 = 0.007
DEGREE_TS_50  = 0.02481
CM_TS = 0.033

wheels = Wheels()
wheels.setup()

sonar = Sonar()
sonar.setup()

def direction(cm):
    t0 = time()
    d0 = sonar.distance()
    if cm > 0:
        wheels.forward(100)
        sleep(CM_TS*cm)
        wheels.stop()
    else:
        wheels.backward(100)

        sleep(CM_TS*-1*cm)
        wheels.stop()
    print((time()-t0)/cm)

def rotate(degrees):
    if degrees>0:
        wheels.turn_left(100, 1)
        sleep(degrees*DEGREE_TS_100)
        wheels.stop()
    else:
        wheels.turn_right(100, 1)
        sleep(-1*degrees*DEGREE_TS_100)
        wheels.stop()

if __name__ == '__main__':



    stop = False
    while not stop:
        option = Prompt.ask("Selecciona d/r/s mas numero: e.g d50 avanza 50 cm. r45 gira 45 grados")
        if option[0] == 'd':
            direction(int(option[1:]))
        elif option[0] == 'r':
            rotate(int(option[1:]))
        elif option[0] == 's':
            stop = True

    # #let's find the maximum distance
    # distances = []
    # t0 = time()
    # while (time() - t0) < 60:
    #     wheels.stop()
    #     d = sonar.distance()
    #     distances.append(d)
    #     wheels.turn_left(100, 1)
    #     sleep(0.2)
    #
    # maxd = np.array(d).max()
    # print(maxd)
    #
    # wheels.turn_left(100, 1)
    # distances = []
    # t0 = time()
    # while (time() - t0) < 60:
    #     d = sonar.distance()
    #     if abs(d-maxd) < 0.1:
    #         print(time())
    #     distances.append(d)
    #
    # #
    # distances = []
    # for i in range(5):
    #     t0 = time()
    #     wheels.forward(20*(i + 1))
    #     while (time() - t0) < 2:
    #         d = sonar.distance()
    #         distances.append((i, time(), d))
    #
    #     t0 = time()
    #     wheels.backward(20*(i + 1))
    #     while (time() - t0) < 2:
    #         d = sonar.distance()
    #         distances.append((i, time(), d))
    # pd.DataFrame.from_records(distances, columns=['it', 'ts', 'distances']).to_csv('forward_backward.csv', index=False)
    #

    #
    # distances = []
    # t0 = time()
    # wheels.turn_left(100, 1)
    # while (time() - t0) < 60:
    #     d = sonar.distance()
    #     distances.append((time(), d))
    # pd.DataFrame.from_records(distances, columns=['ts', 'distances']).to_csv('left_100.csv', index=False)
    #
    # distances = []
    # t0 = time()
    # wheels.turn_right(50, 1)
    # while (time() - t0) < 60:
    #     d = sonar.distance()
    #     distances.append((time(), d))
    # pd.DataFrame.from_records(distances, columns=['ts', 'distances']).to_csv('right_50.csv', index=False)
    #
    # distances = []
    # t0 = time()
    # wheels.turn_right(100, 1)
    # while (time() - t0) < 60:
    #     d = sonar.distance()
    #     distances.append((time(), d))
    # pd.DataFrame.from_records(distances, columns=['ts', 'distances']).to_csv('right_100.csv', index=False)
