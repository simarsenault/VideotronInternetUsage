from twilio.rest import TwilioRestClient


class Twilio_SMS_Sender:
    def __init__(self, account_sid, auth_token):
        self.client = TwilioRestClient(account_sid, auth_token)

    def send_sms(self, from_number, to_number, body):
        self.client.messages.create(to=to_number, from_=from_number, body=body)