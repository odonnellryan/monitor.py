from flask import Flask, render_template, g
import client_backup_monitors

app = Flask(__name__)

@app.route('/', defaults={'page':1})
@app.route('/<int:page>/')
def main(page):
    data = backup_data.get(client_backup_monitors.backup_monitor)
    return render_template('main.html', data=data)

if __name__ == '__main__':
    backup_data = client_backup_monitors.manager
    backup_data.start()
    app.run(debug=True)