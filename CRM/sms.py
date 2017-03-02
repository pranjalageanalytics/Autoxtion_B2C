from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from twilio.rest import TwilioRestClient
from Autoxtion_B2C.settings import production_settings

ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID
AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def send_lead_sms(phonenumber, message):
     print('sms sending lead    ')
     message = client.messages.create(
            body=message,
            to=phonenumber,
            from_=settings.TWILIO_NUMBER,
        )

