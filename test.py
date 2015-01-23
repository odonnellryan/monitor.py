from monitor import BooleanMonitor, BaseMonitor, Queue

def test_func():
    return [("testing", True), ("1", False)]

def test_func2():
    return test_func()

if __name__ == '__main__':
    q = Queue()
    email_monitor = BooleanMonitor(q)
    email_monitor.query_interval = 1
    email_monitor.register(test_func)
    email_monitor.register(test_func2)
    email_monitor.start()
    while True:
        print(q.get())
    #print(email_monitor.data)
