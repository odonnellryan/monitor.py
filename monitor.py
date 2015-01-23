# noinspection PyUnresolvedReferences
from multiprocessing import Process, Queue, Pipe

from time import sleep

class BaseMonitor(Process):
    def __init__(self):
        super().__init__()
        self.data_source = []
        self.query_interval = 0

class BooleanMonitor(BaseMonitor):
    def __init__(self):
        self.pipe = None
        super().__init__()

    def register(self, data_source):
        self.data_source.append(data_source)

    def run(self):
        while True:
            self.pipe = ([i for func in self.data_source for i in func()])
            sleep(self.query_interval)