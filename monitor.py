# noinspection PyUnresolvedReferences
from multiprocessing import Process, Pipe
import threading
from time import sleep


class BaseMonitor(Process):
    """
    sets up some information needed for any base monitor
    inherits from Process
    """
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
            # if this gets hung for whatever reason we'll return None
            self.data = None
            self.data = [i for func in self.data_source for i in func()]
            # using sleep instead of thread.Timer, we don't need a new thread for each time this is run.
            sleep(self.query_interval)

    def handle_pipe(self):
        message = self.pipe.recv()
        if message == "stop":
            self._run = False
        elif message:
            self.pipe.send(self.data)


class BooleanMonitor(BaseMonitor):
    """
    monitor that returns either data or false.
    """
    def __init__(self):
        super().__init__()

    def register(self, data_source):
        """
        each monitor can have several "jobs." one email monitor can monitor multiple clients for a single mailbox,
        for example. here we register the jobs the monitor will run.
        """
        self.data_source.append(data_source)

    def run(self):
        t = threading.Thread(target=self.job)
        t.start()
        while self._run:
            self.handle_pipe()
