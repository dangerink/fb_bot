from app import app
from flask import request
from app import db
from app.fsm.fsm_bot import fsm
from app.models.user import User
from tools.logger import log
from tools.parse_message import MessageContext


@app.route('/', methods=['GET'])
def verify(VERIFY_TOKEN="1"):
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "eh??", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log("RECEIVED {}".format(data))
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                context = None
                user = User.query.filter_by(uid=sender_id).first()
                if not user:
                    user = User(sender_id)
                    db.session.add(user)

                if "message" in messaging_event:
                    #context = MessageContext(user, db, sender_id, get_message_type(user, messaging_event), messaging_event)
                    context = MessageContext(user, sender_id, "message", messaging_event)

                elif "postback" in messaging_event:
                    postback_type = messaging_event["postback"].get("payload")
                    if postback_type:
                        context = MessageContext(user, sender_id, postback_type, messaging_event)

                else:
                    log("Can't parse messaging event.")

                if context:
                    fsm.set_state(user.state)
                    fsm.process(context)
                    user.state = fsm.next_state
                db.session.commit()
    return "ok", 200