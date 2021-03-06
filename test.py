# noinspection PyUnresolvedReferences
from monitors import SimpleMonitor, BaseMonitor
import monitor_manager
import time

def test_func():
    return [(1,2), ('a', 'b')]

def test_func2():
    return [("43", True), ("2", False)]

man = monitor_manager.MonitorManager()

email_monitor = SimpleMonitor()
email_monitor.query_interval = 5
email_monitor.register(test_func)

s_monitor = SimpleMonitor()
s_monitor.query_interval = 1
s_monitor.max_run_count = 5
s_monitor.register(test_func2)

man.register(email_monitor)
man.register(s_monitor)

if __name__ == '__main__':
    man.start()
    while True:
        print(man.get(email_monitor))
        print(man.get(s_monitor))
        time.sleep(1)

