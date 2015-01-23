# noinspection PyUnresolvedReferences
from multiprocessing.sharedctypes import Array
# noinspection PyUnresolvedReferences
from multiprocessing import Manager
import zmq

class MonitorManager:
    def __init__(self):
        self.monitors = {}

    def register_monitor(self, monitor):
        # TODO: use zmq to manage info from various processes
        monitor.data = zmq
        self.monitors[monitor] = monitor.data

    def run(self):
        for monitor in self.monitors:
            monitor.start()

    def get(self, monitor):
        return self.monitors[monitor].recv()