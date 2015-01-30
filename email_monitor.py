from monitor import BooleanMonitor, BaseMonitor
import monitor_manager
import requests
import config
import json

# scope of this project is weekly jobs
# the idea is to also check on the backup jobs manually from time-to-time
# TODO: make the backup jobs config files! (JSON probably)

folder_ids = {'Old': 'AAMkADlmY2IwYTFkLWMxNDAtNGIyNy04NDM0LTJhMDQ4NTc2YmYyZAAuAAAAAAAofRrKZvRgQ4RoTUPPf3uJAQDvpmjL_PTZTLP1WRdlp2cYAAAB6fBfAAA='}

def weekly_schedule(daily):
    return dict(sunday=daily[:], monday=daily[:], tuesday=daily[:], wednesday=daily[:],
                thursday=daily[:], friday=daily[:], saturday=daily[:])

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
        r = requests.get('https://outlook.office365.com/api/v1.0/me/messages', auth=(config.o365['email'], config.o365['password']))
        return r.json()

    def move_emails(self, emails):
        """
        Move each email in `emails` into the Old folder.
        """
        for email in emails['value']:
            data = json.dumps({'DestinationId': folder_ids['Old']})
            headers = {'Content-Type': 'Application/Json'}
            r = requests.post(email['@odata.id'] + '/move', data=data,
                             auth=(config.o365['email'], config.o365['password']), headers=headers)
            return r.json()

def get_folders():
    """
    helper function to return the folders on o365 (so we can get the folder id for later use)
    """
    r = requests.get('https://outlook.office365.com/api/v1.0/me/folders', auth=(config.o365['email'], config.o365['password']))
    return r.json()

schedule = weekly_schedule(['ACGCORE (Daily)', 'NETSTORAGE General (Daily)', 'ACGDC (Daily)', 'ACGEX (Daily)'])
schedule['monday'].extend(['(M) W7MLANGLEY', '(M) W7MFEBBI'])
schedule['wednesday'].extend(['(W) NETSTORAGE USERS'])
schedule['tuesday'].extend(['(T) OLYMPUS'])
schedule['thursday'].extend(['(Th) AOSORACLE'])
schedule['friday'].extend(['(F) Netstorage Consulting Shares'])

acg_monitor = BackupMonitor(schedule)

