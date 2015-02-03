# noinspection PyUnresolvedReferences
from multiprocessing import Manager, Pipe

class MonitorManager:
    """
    MonitorManager manages the monitors!
    pass it a monitor, and it will run that job
    it allows for us to easily communicate with the monitors while ensuring they all run on different processes
    (one might break sometimes!)
    it uses pipes to communicate.

    """
    def __init__(self):
        self.monitors = {}

    def register(self, monitor):
        parent_pipe, child_pipe = Pipe()
        monitor.pipe = child_pipe
        self.monitors[monitor] = parent_pipe

    def start(self):
        for monitor in self.monitors:
            monitor.start()

    def get(self, monitor):
        """
        this gets the data - whatever it may be - from the specified monitor
        """
        self.monitors[monitor].send('continue')
        return self.monitors[monitor].recv()

    def stop(self, monitor):
        self.monitors[monitor].send('stop')
        monitor.terminate()
        self.monitors[monitor].close()

    def stop_all(self):
        for monitor in self.monitors:
            monitor.terminate()