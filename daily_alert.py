import json
import videotron
import email_sender


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)

    videotron = videotron.Videotron(config['videotron_account'])
    mailer = email_sender.Email_Sender(config['smtp'])

    current_month_usage = videotron.get_current_month_usage()

    message = 'Usage: {usage}<br/>Maximum: {maximum}<br/>Day(s) remaining: {days_remaining}'.format(**current_month_usage)
    mailer.send(config['email'], message)