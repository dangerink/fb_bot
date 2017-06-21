import json
import requests
from const import ACCESS_TOKEN, SUCCESS_STATUS
from tools.logger import log

WIKI_URL = "https://en.wikipedia.org/wiki/"

def send_fb_message(recipient_id, text):
    send_fb(recipient_id, {"text": text})

def send_fb(recipient_id, message):
    if message and recipient_id:
        params = {"access_token": ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}
        data = _get_data(recipient_id, message)
        log("SENDING... {}".format(data))
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != SUCCESS_STATUS:
            log(r.status_code)
            log(r.text)
    else:
        log("can't send message {} to {}".format(message, recipient_id))

def _get_data(recipient_id, message):
    data = {"recipient": {"id": recipient_id},
            "message": message}
    return json.dumps(data)

def postback_template(text, title, payload):
    msg = '{"attachment": {"type": "template", "payload": {"template_type": "button", "text": "%s","buttons":' \
          ' [{"type": "postback", "title": "%s", "payload": "%s"}]}}}' % (text, title, payload)
    return msg