
from twilio.rest import Client
import json

class WhatsApp():
    def __init__(self):
        with open("config.json",'r') as j:
            creds = json.loads(j.read())
        self.account_sid = creds['whatsapp']['whatsapp_sid']
        self.auth_token = creds['whatsapp']['whatsapp_token']
        self.from_number = creds['whatsapp']['whatsapp_from']
        self.to_number = creds['whatsapp']['whatsapp_to']

    def send_message(self, message):
        client = Client(self.account_sid, self.auth_token)
        client.messages.create(
            body=message,
            from_='whatsapp:'+self.from_number,
            to='whatsapp:'+self.to_number
        )