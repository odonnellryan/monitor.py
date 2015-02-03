from monitor import BooleanMonitor, BaseMonitor
import monitor_manager
import requests
import config
import json
import datetime

# scope of this project is weekly jobs
# the idea is to also check on the backup jobs manually from time-to-time
# TODO: make the backup jobs config files! (JSON probably)

folder_ids = {
    'Old': 'AAMkADlmY2IwYTFkLWMxNDAtNGIyNy04NDM0LTJhMDQ4NTc2YmYyZAAuAAAAAAAofRrKZvRgQ4RoTUPPf3uJAQDvpmjL_PTZTLP1WRdlp2cYAAAB6fBfAAA='}


def weekly_schedule(schedule):
    with open(schedule) as f:
        return (json.load(f))


def get_previous_day():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    return(yesterday.strftime("%A"))


class BackupMonitor:
    """
    backup monitor monitors backups!
    we have it get a weekly schedule and access a mailbox to see if we've gotten success emails for that job (backup exec.)
    if we don't get a success email we return false. if there is an exception, we'll send that along!
    """

    def __init__(self, schedule):
        self.last_run = None
        self.schedule = schedule

    def get_emails(self):
        """
        get all emails in inbox
        """
        r = requests.get('https://outlook.office365.com/api/v1.0/me/messages',
                         auth=(config.o365['email'], config.o365['password']))
        return r.json()

    def move_emails(self, emails):
        """
        Move each email in `emails` into the Old folder.
        """
        response = []
        for email in emails['value']:
            data = json.dumps({'DestinationId': folder_ids['Old']})
            headers = {'Content-Type': 'Application/Json'}
            r = requests.post(email['@odata.id'] + '/move', data=data,
                              auth=(config.o365['email'], config.o365['password']), headers=headers)
            response.append(r.json())

    def run(self):
        # we only care if this runs once a day
        if not self.last_run or self.last_run < datetime.datetime.today():
            day = get_previous_day()
            processed_emails = []
            emails = self.get_emails()
            for email in emails['value']:
                print(email)
            self.last_run = datetime.datetime.today()
        pass


def get_folders():
    """
    helper function to return the folders on o365 (so we can get the folder id for later use)
    """
    r = requests.get('https://outlook.office365.com/api/v1.0/me/folders',
                     auth=(config.o365['email'], config.o365['password']))
    return r.json()

acg_schedule = weekly_schedule('backup_jobs/acg.json')

email_monitor = BackupMonitor(acg_schedule)
emails = email_monitor.get_emails()
for i in emails['value']:
    print(i)
print(emails)
#email_monitor.run()