import json
from videotron import Videotron
from emailsender import EmailSender
from twiliosmssender import TwilioSmsSender


if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)

    config_email = config['email']
    config_twilio_sms = config['twilio_sms']

    videotron = Videotron(config['videotron_account'])
    current_month_usage = videotron.get_current_month_usage()

    message = 'Usage: {usage} {unit}\nMaximum: {maximum} {unit}\nDay(s) remaining: {days_remaining}'.format(**current_month_usage)

    if config_email['enabled']:
        email_sender = EmailSender(config_email['smtp'])
        email_sender.send(config_email, message)

    if config_twilio_sms['enabled']:
        sms_sender = TwilioSmsSender(config_twilio_sms['account']['sid'], config_twilio_sms['account']['auth_token'])
        for number in config_twilio_sms['sms']["to_numbers"]:
            sms_sender.send_sms(config_twilio_sms['sms']["from_number"], number, message)
