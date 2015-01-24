# noinspection PyUnresolvedReferences
from multiprocessing import Manager, Pipe

class MonitorManager:
    def __init__(self):
        self.monitors = {}

    def register_monitor(self, monitor):
        parent_pipe, child_pipe = Pipe()
        monitor.pipe = child_pipe
        self.monitors[monitor] = parent_pipe

    def run(self):
        for monitor in self.monitors:
            monitor.start()

    def get(self, monitor):
        self.monitors[monitor].send('continue')
        return self.monitors[monitor].recv()

    def stop(self, monitor):
        self.monitors[monitor].send('stop')
        monitor.terminate()
        self.monitors[monitor].close()