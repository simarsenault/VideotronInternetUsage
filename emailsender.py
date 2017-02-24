import smtplib
from email.mime.text import MIMEText


class EmailSender:
    def __init__(self, config):
        self.config = config

    def send(self, email, message):
        joined_to_addresses = ','.join(email['to'])

        mime_message = MIMEText(message, 'html')
        mime_message['From'] = '{0} <{1}>'.format(email['from']['name'], email['from']['address'])
        mime_message['To'] = joined_to_addresses
        mime_message['Subject'] = email['subject']

        server_ssl = smtplib.SMTP_SSL(self.config['server'], self.config['port'])
        server_ssl.ehlo()
        server_ssl.login(self.config['username'], self.config['password'])
        server_ssl.sendmail(email['from']['address'], joined_to_addresses, mime_message.as_string())
        server_ssl.quit()