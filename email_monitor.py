from monitor import BooleanMonitor, BaseMonitor
import monitor_manager
import requests
import config
import json

folder_id = {'Old': 'AAMkADlmY2IwYTFkLWMxNDAtNGIyNy04NDM0LTJhMDQ4NTc2YmYyZAAuAAAAAAAofRrKZvRgQ4RoTUPPf3uJAQDvpmjL_PTZTLP1WRdlp2cYAAAB6fBfAAA='}

class BackupSchedule:


class BackupMonitor:
    def __init__(self):

def get_emails():
    r = requests.get('https://outlook.office365.com/api/v1.0/me/messages', auth=(config.o365['email'], config.o365['password']))
    return r.json()

def move_emails(emails):
    """
    Move each email that's passed into the Old folder.
    :param emails: dict
    :return: error or
    """
    for email in emails['value']:
        data = {'DestinationId': folder_id['Old']}
        headers = {'Content-Type': 'Application/Json'}
        r = requests.post(email['@odata.id'] + '/move', data=json.dumps(data),
                         auth=(config.o365['email'], config.o365['password']), headers=headers)
        return r.json()

def get_folders():
    """
    helper function to return the folders on o365 (so we can get the folder id for later use)
    :return:
    """
    r = requests.get('https://outlook.office365.com/api/v1.0/me/folders', auth=(config.o365['email'], config.o365['password']))
    return r.json()

#print(get_folders())
print(move_emails(get_emails()))