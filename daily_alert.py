import json
from videotron import Videotron
from email_sender import Email_Sender


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)

    videotron = Videotron(config['videotron_account'])
    mailer = Email_Sender(config['smtp'])

    current_month_usage = videotron.get_current_month_usage()

    message = 'Usage: {usage} {unit}<br/>Maximum: {maximum} {unit}<br/>Day(s) remaining: {days_remaining}'.format(**current_month_usage)
    mailer.send(config['email'], message)