# noinspection PyUnresolvedReferences
from multiprocessing.sharedctypes import Array
# noinspection PyUnresolvedReferences
from multiprocessing import Manager
import zmq
import json
import config

class MonitorManager:
    def __init__(self):
        self.monitors = {}

    def server(port=config.port):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % port)
        print("Running server on port: ", port)
        message = socket.recv()
        print("Received request #%s: %s" % (reqnum, message))
        socket.send("World from %s" % port)

    def register_monitor(self, monitor):
        # TODO: use zmq to manage info from various processes
        monitor.data = self.data
        self.monitors[monitor] = monitor.data

    def run(self):
        for monitor in self.monitors:
            monitor.start()

    def get(self, monitor):
        return self.monitors[monitor].recv()