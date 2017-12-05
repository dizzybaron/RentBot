from flask import Flask, request
import requests

app = Flask(__name__)

ACCESS_TOKEN = "EAAHqP0d6yQ4BAJRkGwAYcDpt5WOlNx5yWbtZCntMRwqSwRop9fNBDMNAg03ZCDpC4OJ3pnz56EWqr9ERrN9Dti0EImUJFsk34NSuAYgJqxNhxC7HfsV7CL5UYiZA8eCqUoDPrZCyZBHDZAIsVf0nWidFg3ZAcdKSWZBeeMxCWaE6nEcj0wymhYut"
VERIFY_TOKEN = "superbug"

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.11/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']
    reply(sender, message)

    return "ok"

def messaging_events(payload):
    # Generate tuples of (sender_id, message_text) from the provided payload.
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
        else:
            yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
    # Send the message text to recipient with id recipient.

    r = requests.post("https://graph.facebook.com/v2.11/me/messages",
        params={"access_token": token},
        data=json.dumps({
            "recipient": {"id": recipient},
            "message": {"text": text.decode('unicode_escape')}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)

if __name__ == '__main__':
    context = ('ssl/fullchain.pem', 'ssl/privkey.pem')
    app.run(host = '0.0.0.0', debug=True, ssl_context = context)
