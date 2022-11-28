
from twilio.rest import Client

class WhatsApp():
    def __init__(self, account_sid, auth_token, from_number, to_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.to_number = to_number

    def send_message(self, message):
        client = Client(self.account_sid, self.auth_token)
        client.messages.create(
            body=message,
            from_='whatsapp:'+self.from_number,
            to='whatsapp:'+self.to_number
        )