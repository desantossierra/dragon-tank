import abc
import multiprocessing


class ControllerABC(abc.ABC):
    def __init__(self,
                 distance: multiprocessing.Queue = None,
                 position: multiprocessing.Queue = None):
        self.distance, self.position = distance, position

