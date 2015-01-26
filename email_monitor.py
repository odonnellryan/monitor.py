from monitor import BooleanMonitor, BaseMonitor
import monitor_manager
import requests
import config

def get_emails():
    r = requests.get('https://outlook.office365.com/api/v1.0/me/messages', auth=(config.o365['email'], config.o365['password']))
    return r.json()

def move_emails(emails):
    for email in emails['value']:
        print(email['Id'])
        data = {'DestinationId':'Old'}
        r = requests.post('https://outlook.office365.com/api/v1.0/me/messages/{0}/move'.format(email['Id']), data=data,
                         auth=(config.o365['email'], config.o365['password']))
        print(r)
    print(emails)


print(move_emails(get_emails()))