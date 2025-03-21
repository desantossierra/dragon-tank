import abc
import multiprocessing


class ControllerABC(abc.ABC):
    def __init__(self,
                 location: multiprocessing.Array = None):
        self.location = location

