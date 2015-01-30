# noinspection PyUnresolvedReferences
from monitor import BooleanMonitor, BaseMonitor
import monitor_manager
import time

def test_func():
    return [(1,2), ('a', 'b')]

def test_func2():
    return [("43", True), ("2", False)]

man = monitor_manager.MonitorManager()

email_monitor = BooleanMonitor()
email_monitor.query_interval = 5
email_monitor.register(test_func)

s_monitor = BooleanMonitor()
s_monitor.query_interval = 1
s_monitor.register(test_func2)

man.register(email_monitor)
man.register(s_monitor)

if __name__ == '__main__':
    man.reload()
    while True:
        print(man.get(email_monitor))
        print(man.get(s_monitor))
