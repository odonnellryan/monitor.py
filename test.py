# noinspection PyUnresolvedReferences
from monitor import BooleanMonitor, BaseMonitor, Queue
import monitormanager
import time

def test_func():
    return [("testing", True), ("1", False)]

def test_func2():
    return [("43", True), ("2", False)]

man = monitormanager.MonitorManager()

email_monitor = BooleanMonitor()
email_monitor.query_interval = 5
email_monitor.register(test_func)

s_monitor = BooleanMonitor()
s_monitor.query_interval = 1
s_monitor.register(test_func2)

man.register_monitor(email_monitor)
man.register_monitor(s_monitor)

if __name__ == '__main__':
    man.run()
    time.sleep(10)
    while True:
        print(man.get(email_monitor))
        print(man.get(s_monitor))
