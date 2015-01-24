# noinspection PyUnresolvedReferences
from multiprocessing import Process, Queue, Pipe
import threading
from time import sleep

class BaseMonitor(Process):
    def __init__(self):
        super().__init__()
        self.data_source = []
        self.query_interval = 0
        self.data = None
        self._run = True
        self.pipe = None

    def job(self):
        while self._run:
            # initiate!
            self.data = [i for func in self.data_source for i in func()]
            sleep(self.query_interval)

    def handle_pipe(self):
        message = self.pipe.recv()
        if message == "stop":
            self._run = False
        elif message:
            self.pipe.send(self.data)


class BooleanMonitor(BaseMonitor):
    def __init__(self):
        super().__init__()

    def register(self, data_source):
        self.data_source.append(data_source)

    def run(self):
        t = threading.Thread(target=self.job)
        t.start()
        while self._run:
            self.handle_pipe()
