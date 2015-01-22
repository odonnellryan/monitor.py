from monitor import BooleanMonitor, BaseMonitor, Manager

def test_func() -> (str, bool):
    return [("testing", True),("testing", True)]

def test_func2() -> (str, bool):
    return test_func()

if __name__ == '__main__':
    d = Manager().dict()
    email_monitor = BooleanMonitor(d)
    email_monitor.query_interval = 1
    email_monitor.register(test_func)
    email_monitor.register(test_func2)
    email_monitor.start()
    #print(email_monitor.data)
