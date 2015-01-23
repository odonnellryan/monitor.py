from multiprocessing import Process, Queue
from time import sleep

class BaseMonitor(Process):
    def __init__(self):
        super().__init__()
        self.data_source = []
        self.query_interval = 0

class BooleanMonitor(BaseMonitor):
    def __init__(self, data_queue):
        self.data_queue = data_queue
        super().__init__()

    def register(self, data_source: (str, bool)):
        self.data_source.append(data_source)

    def run(self):
        while True:
            if not self.data_queue.empty(): self.data_queue.get()
            self.data_queue.put([i for func in self.data_source for i in func()])
            print(self.data_source)
            sleep(self.query_interval)