from multiprocessing import Process, Manager
from time import sleep

class BaseMonitor:
    def __init__(self):
        self.data_source = []
        self.query_interval = 0

class BooleanMonitor(BaseMonitor):
    def __init__(self, data):
        self.data = data
        super().__init__()

    def register(self, data_source: (str, bool)):
        self.data_source.append(data_source)

    def _monitor(self, d):
        while True:
            d['boolean_monitor'] = [func() for func in self.data_source]
            #print(self.data)
            sleep(self.query_interval)

    def start(self):
        self.p = Process(target=self._monitor, args=(self.data,))
        self.p.start()

    def stop(self):
        self.p.stop()