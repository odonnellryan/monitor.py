from flask import Flask, render_template, g
from email_monitor import EmailMonitor, weekly_schedule
from monitors import SimpleMonitor
from monitor_manager import MonitorManager

# setup backup monitors
acg_schedule = weekly_schedule('backup_jobs/acg.json')
email_monitor = EmailMonitor(acg_schedule)

backup_monitor = SimpleMonitor()
backup_monitor.register(email_monitor.run)

backup_monitor.query_interval = 10
backup_monitor.max_run_count = 1

manager = MonitorManager()
manager.register(backup_monitor)

app = Flask(__name__)


@app.route('/', defaults={'page':1})
@app.route('/<int:page>/')
def main(page):
    data = backup_data.get(backup_monitor)
    return render_template('main.html', data=data)

if __name__ == '__main__':
    backup_data = manager
    backup_data.start()
    app.run(debug=True)