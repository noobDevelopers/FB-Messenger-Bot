import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
app=Flask(__name__)
PAGE_ACCESS_t='EAAEJqMETQLYBAO2jc2tCZC1AEizI3Bm7ZA5M79bkkeXQ2uE0lW1BVNL8j0TFvCZC7AQfpUILz9TO6kAx9TFbl5k8NBGq5VuXGRgzCLdiZC21YPlOyZB4u2ZB3sHyrkX72WnIbd1PRdrWaWfsD4vkb9zOFAPlZADQLtpteUz0kF3rzl4GPZAZBbt5l'
bot=Bot(PAGE_ACCESS_t)

@app.route('/', methods=['GET'])

def verify():
    if request.args.get("hub.mode")=="subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")=="hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200


@app.route('/', methods=["POST"])
def webhook():
    data=request.get_json()
    log(data)
    if(data['object']=='page'):
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                sender_id=messaging_event['sender']['id']
                recipient_id=messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text=messaging_event['message']['text']
                    else:
                        messaging_text='no text'

                    response=None
                    entity, value=wit_response(messaging_text)
                    if entity=='newstype':
                        response="Ok, I will send you {} news".format(str(value))
                    elif entity=='location':
                        response="Ok, You live in {0}. I will send you top headlines from {0}".format(str(value)) 
                    elif entity=='gaali':
                        response="{}".format(str(value))
                    elif entity=="hi":
                        response="{}".format(str(value))
                    elif entity=="master":
                        response="{}".format(str(value))
                    elif entity=="special":
                        response="{}".format(str(value))

                    if response==None:
                        response="Sorry, I didn't understand!"
                    bot.send_text_message(sender_id, response)
    return "ok", 200                

def log(message):
    print(message)
    sys.stdout.flush()


if __name__=="__main__":
    app.run(debug=True, port=80)     