import os, dotenv, json
dotenv.load_dotenv()


def twilio_send():
  from twilio.rest import Client as TwilioClient

  account_sid = os.getenv('TWILIO_ACCOUNT_SID')
  auth_token = os.getenv('TWILIO_AUTH_TOKEN')
  from_number = os.getenv('TWILIO_PHONE_NUMBER')

  client = TwilioClient(account_sid, auth_token)
  message = client.messages.create(
    from_=f'whatsapp:{from_number}',
    to='whatsapp:+5516999664381',
    content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
    content_variables=json.dumps({"1": "22 July 2026", "2": "3:15pm"})
  )

  print(message.sid)


def wasender_send():
  from wasenderapi import WasenderSyncClient

  api_key = os.getenv('WASENDER_API_KEY')

  client = WasenderSyncClient(api_key)
  response = client.send_text(
    to='5516999664381',
    text_body='Hello from Wasender SDK'
  )


if __name__ == '__main__':
  wasender_send()
