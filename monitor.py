# noinspection PyUnresolvedReferences
from multiprocessing import Process, Queue, Pipe
import config
import zmq
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
            context = zmq.Context()
            print("Connecting to server with ports %s" % config.port)
            socket = context.socket(zmq.REQ)
            socket.connect ("tcp://localhost:%s" % config.port)
            socket.send([i for func in self.data_source for i in func()])
            message = socket.recv()
            print("Received reply [", message, "]")
            sleep(self.query_interval)