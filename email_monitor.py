from monitor import SimpleMonitor, BaseMonitor
import monitor_manager
import requests
import config
import json
import datetime

# scope of this project is weekly jobs
# the idea is to also check on the backup jobs manually from time-to-time

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
        self.schedule = schedule

    def get_emails(self):
        """
        get all emails in inbox
        """
        r = requests.get('https://outlook.office365.com/api/v1.0/me/messages',
                         auth=(config.o365['email'], config.o365['password']))
        return r.json()['value']

    def move_emails(self, emails):
        """
        Move each email in `emails` into the Old folder.
        """
        response = []
        for email in emails:
            data = json.dumps({'DestinationId': folder_ids['Old']})
            headers = {'Content-Type': 'Application/Json'}
            r = requests.post(email['@odata.id'] + '/move', data=data,
                              auth=(config.o365['email'], config.o365['password']), headers=headers)
            response.append(r.json())
        return response

    def get_jobs(self):
        """
        Get today's backup jobs
        """
        day = get_previous_day().lower()
        jobs = self.schedule['daily'] + self.schedule[day]
        return jobs

    def process_emails(self):
        """
        goes through the emails and builds the return dictionary.
        """
        processed_emails = []
        jobs = self.get_jobs()
        emails = self.get_emails()
        processed_jobs = {job: None for job in jobs}
        for email in emails:
            for job in jobs:
                if job in email['Subject']:
                    processed_emails.append(email)
                    processed_jobs[job] = email['Body']['Content']
        return processed_emails, [(k,v) for k,v in processed_jobs.items()]

    def run(self):
        emails, jobs = self.process_emails()
        self.move_emails(emails)
        return jobs


def get_folders():
    """
    helper function to return the folders on o365 (so we can get the folder id for later use)
    """
    r = requests.get('https://outlook.office365.com/api/v1.0/me/folders',
                     auth=(config.o365['email'], config.o365['password']))
    return r.json()