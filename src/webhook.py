import os, dotenv
dotenv.load_dotenv()

from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = os.getenv('WASENDER_WEBHOOK_SECRET')


def verify_signature(req):
  signature = req.headers.get("x-webhook-signature")

  if not signature or signature != WEBHOOK_SECRET:
    return False

  return True


@app.route("/webhook", methods=["POST"])
def webhook():
  if not verify_signature(request):
    return jsonify({"error": "Invalid signature"}), 401

  payload = request.json
  event_type = payload["event"]

  print("Received webhook event:", event_type)

  if event_type == "messages.upsert":
    message_data = payload["data"]["messages"]
    key = message_data["key"]
    message = message_data["messageBody"]
    from_ = key["cleanedSenderPn"] if not key.get("fromMe") else 'me'
    message_timestamp = message_data["messageTimestamp"]
    timestamp = (
        message_timestamp
        if not message_timestamp.get("low") and not message_timestamp.get("high")
        else message_timestamp.get("high") if message_timestamp.get("low") == 0
        else message_timestamp.get("low")
    )

    sent_date = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')

    print(f"New message from {from_}: {message} ({sent_date})")

  return jsonify({"received": True}), 200


if __name__ == "__main__":
  app.run(port=3000)
