# noinspection PyUnresolvedReferences
from multiprocessing import Process, Pipe
import threading
from time import sleep
import datetime

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
        self._last_run = None
        self.max_run_count = None
        self._run_count = 0

    def job(self):
        while self._run:
            # this is here so if we want a job to only run x times a day
            if not self._last_run or self._last_run < datetime.date.today():
                self._run_count = 0
            if not self.max_run_count or self._run_count < self.max_run_count:
                # initiate!
                # if this gets hung for whatever reason we'll return None
                self.data = None
                self.data = [i for func in self.data_source for i in func()]
                # only really want to store this information if we need it?
                if self.max_run_count: 
                    self._run_count += 1
                self._last_run = datetime.date.today()
            # using sleep instead of thread.Timer, we don't need a new thread for each time this is run.
            sleep(self.query_interval)

    def handle_pipe(self):
        message = self.pipe.recv()
        if message == "stop":
            self._run = False
        elif message:
            self.pipe.send(self.data)


class SimpleMonitor(BaseMonitor):
    """
    monitor that returns data or false.
    """

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
