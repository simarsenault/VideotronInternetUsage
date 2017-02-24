from twilio.rest import TwilioRestClient


class TwilioSmsSender:
    def __init__(self, account_sid, auth_token, from_number):
        self.client = TwilioRestClient(account_sid, auth_token)
        self.from_number = from_number

    def send_sms(self, to_number, body):
        self.client.messages.create(to=to_number, from_=self.from_number, body=body)