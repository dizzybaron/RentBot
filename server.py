from flask import Flask, request
import requests, json
import logging
from crawFunc import *
import pandas as pd
import numpy as np
# set up logging file
logging.basicConfig(filename='log',level=logging.DEBUG)


app = Flask(__name__)


ACCESS_TOKEN = "EAAHqP0d6yQ4BAEcj87lDEzT1j7nZABVtfovA3HigtQsgf2ZCBz6mYx0nAwbKi6ldXclfsCMqggQH4bcghJTcTBEBg8QLdzAWecNZBveiKISHDZAudXs4ge1CqLfvJmPi5YkEo35m4gH5dNpFlfO10MCvCWZArUDXwQb89lGV7fBXC0BRahvBH"
VERIFY_TOKEN = "superbug"
#load userdata



@app.route('/', methods=['GET'])
def handle_verification():
    if request.args['hub.verify_token'] == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    # load latest userdata
    user_data = pd.read_pickle("./user_data")

    data = request.get_json()
    logging.info(data)
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    print(messaging_event['message'])
                    message_text = messaging_event['message']['text']
                    if messaging_event['message'].get("quick_reply"):
                        if 'SEARCH' not in messaging_event['message']['quick_reply']['payload']:
                            col = messaging_event['message']['quick_reply']['payload'].split('_')[0]
                            val = messaging_event['message']['quick_reply']['payload'].split('_')[1]
                            user_data.loc[str(sender_id), col] = val
                            user_data.to_pickle("user_data")
                            main_way(sender_id)
                        else:
                            result = messaging_event['message']['text']
                            if result == '要':
                                
                                user_data.loc[str(sender_id), :] = np.nan
                                user_data.to_pickle("user_data")
                                
                                main_way(sender_id)
                            else:
                                main_way(sender_id)
                    # if new user
                    elif str(sender_id) not in user_data.index:
                        send_text_message(sender_id, '歡迎來到租霸')
                        # create id
                        user_data.loc[str(sender_id), :] = np.nan
                        user_data.to_pickle("user_data")
                        main_way(sender_id)
                        # main ask
                    else:
                        display_param(sender_id)
                        
                
    return "ok"
                                         
def display_param(sender_id):
    user_data = pd.read_pickle("./user_data")
    text_for_old_usr = '這是你的搜尋紀錄/n/n'+str(user_data.loc[str(sender_id), :])+'/n/n是否要清除搜尋條件?'
    send_quick_reply(sender_id, quick_reply_json(list_to_dict(search_clean, 'SEARCH')),text_for_old_usr)
                        
def send_quick_reply(sender_id, options, text_message):
    # Send the message text to recipient with id recipient.
    
    r = requests.post("https://graph.facebook.com/v2.11/me/messages",
        params={"access_token": ACCESS_TOKEN},
        data=json.dumps({
            "recipient": {"id": sender_id},
            "message": {"text": text_message,
            "quick_replies":json.dumps(options)}
            }),
        headers={'Content-type': 'application/json'})
    
    if r.status_code != requests.codes.ok:
        print(r.text)
        
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
    

def main_way(sender_id):
    # load latest userdata
    user_data = pd.read_pickle("./user_data")

    #if np.isnan(user_data.loc[str(sender_id), 'region']):
    if type(user_data.loc[str(sender_id), 'region']) == float:
        send_quick_reply(sender_id, quick_reply_json(region_list), '想住哪區')
    elif type(user_data.loc[str(sender_id), 'city']) == float:
        send_quick_reply(sender_id, quick_reply_json(list_to_dict(region_to_city[user_data.loc[str(sender_id), 'region']],'city')), '哪個城市')
    elif type(user_data.loc[str(sender_id), 'housetype'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(disp_type, 'housetype')
        ), '想種房型？')
    elif type(user_data.loc[str(sender_id), 'floor'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(floor, 'floor')
        ), '幾樓')
    elif type(user_data.loc[str(sender_id), 'rooftop'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(rooftop, 'rooftop')
        ), '要不要排除頂樓加蓋')
    elif type(user_data.loc[str(sender_id), 'cook'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(cook, 'cook')
        ), '要能煮飯嘛')
    elif type(user_data.loc[str(sender_id), 'elevator'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(elevator, 'elevator')
        ), '要電梯ㄇ')
    elif type(user_data.loc[str(sender_id), 'budgetMax'])==float:
        send_quick_reply(sender_id, quick_reply_json(
            list_to_dict(budgetMax, 'budgetMax')
        ), '預算上限')
    else:
        send_text_message(sender_id, '完成填寫')
        display_param(sender_id)
        
if __name__ == '__main__':
    context = ('ssl/fullchain.pem', 'ssl/privkey.pem')
    app.run(host = '0.0.0.0', debug=True, ssl_context = context)
