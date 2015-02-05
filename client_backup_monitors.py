import email_monitor
import monitor
import monitor_manager
import time

acg_schedule = email_monitor.weekly_schedule('./backup_jobs/acg.json')
e_monitor = email_monitor.BackupMonitor(acg_schedule)
backup_monitor = monitor.SimpleMonitor()
backup_monitor.register(e_monitor.run)
backup_monitor.query_interval = 10
backup_monitor.max_run_count = 1

manager = monitor_manager.MonitorManager()
manager.register(backup_monitor)

#print(e_monitor.run())

if __name__ == '__main__':
    manager.start()
    while True:
        print(manager.get(backup_monitor))
        time.sleep(5)