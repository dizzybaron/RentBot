from flask import Flask, request
import requests, json
import logging

# set up logging file
logging.basicConfig(filename='log',level=logging.DEBUG)

app = Flask(__name__)

ACCESS_TOKEN = "EAAHqP0d6yQ4BAJRkGwAYcDpt5WOlNx5yWbtZCntMRwqSwRop9fNBDMNAg03ZCDpC4OJ3pnz56EWqr9ERrN9Dti0EImUJFsk34NSuAYgJqxNhxC7HfsV7CL5UYiZA8eCqUoDPrZCyZBHDZAIsVf0nWidFg3ZAcdKSWZBeeMxCWaE6nEcj0wymhYut"
VERIFY_TOKEN = "superbug"
     

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.get_json()
    logging.info(data)
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = "we don't care"
                    # send to initiation
                    send_button_message(sender_id)
    return "ok"

def send_text_message(sender_id, message_text):
    # Send the message text to recipient with id recipient.

    r = requests.post("https://graph.facebook.com/v2.11/me/messages",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({
            "recipient": {"id": sender_id},
            "message": {"text": message_text}
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)
        
def send_post_back(sender_id):
    # post_back
    r = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({
            "recipient": {"id": sender_id},
            "message":{
                "get_started": {"payload": "Start"}
                }
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)
    
def send_button_message(sender_id):
    # Send the message with button template

    r = requests.post("https://graph.facebook.com/v2.11/me/messages",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({
            "recipient": {"id": sender_id},
            "message": {
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"button",
                    "text":"想叫我做什麼呢？",
                    "buttons":[
                      {
                        "type":"postback",
                          "payload": "TAIPEI",
                        "title":"台北市"
                      },
                      {
                        "type":"web_url",
                        "url":"https://www.messenger.com",
                        "title":"Visit Messenger"
                      },
                    ]
                  }
                }
              }
        }),
        headers={'Content-type': 'application/json'})
    if r.status_code != requests.codes.ok:
        print(r.text)

if __name__ == '__main__':
    context = ('ssl/fullchain.pem', 'ssl/privkey.pem')
    app.run(host = '0.0.0.0', debug=True, ssl_context = context)
