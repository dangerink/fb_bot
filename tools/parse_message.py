from app.models.model_helpers import ModelHelper


class MessageContext():
    def __init__(self, user=None, sender_id=None, event_type=None, messaging_event=None):
        self.user = user
        self.state = user.state
        self.sender_id = sender_id
        self.event_type = event_type
        self.messaging_event = messaging_event
        self.model_helper = ModelHelper()


def get_words_from_message(messaging_event):
    text = get_text_from_message(messaging_event).strip()
    return [word.lower() for word in text.split(" ") if len(word) > 2]


def get_text_from_message(messaging_event):
    return messaging_event.get("message", {}).get("text", "").strip().replace('.','')


def format_to_wiki(text):
    return text.replace(' ','_')


def format_to_user(message):
    if message:
        return message.replace('_', ' ')
    return "Can't understand you, sorry."
