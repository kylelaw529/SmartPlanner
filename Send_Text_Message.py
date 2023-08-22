from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_sid = os.environ.get('TWILIO_SID')
api_token = os.environ.get('TWILIO_TOKEN')

if api_sid is None:
    print("API sid not found in environment variables.")
if api_token is None:
    print("API token not found in environment variables.")

def send_message(message, phone_num):
    account_sid = api_sid
    auth_token = api_token

    pnumber = '+1'+str(phone_num)
    
    client = Client(account_sid, auth_token)

    ''' Change the value of 'from' with the number 
    received from Twilio and the value of 'to'
    with the number in which you want to send message.'''
    message = client.messages.create(
                                from_='+18148854366',
                                body =message,
                                to =pnumber
                            )

    print(message.sid)
