from app.fsm.fsm import FSM
from config import WEATHER_POSTBACK, QUESTION_POSTBACK, STRAIGHT_QUERY_POSITIVE, STRAIGHT_QUERY_NEGATIVE
from tools.extention import get_intersection
from tools.fb_api import send_fb_message, send_fb, postback_template, WIKI_URL
from tools.logger import log
from tools.owm_api import owm_get_weather
from tools.parse_message import get_words_from_message, get_text_from_message, format_to_user, format_to_wiki


def error(fsm, context):
    log("FSM error in state {}. Received Message = {}".format(fsm.current_state, context.messaging_event))

def handle_say_hello(fsm, context):
    recipient = context.sender_id
    send_fb_message(recipient, format_to_user("Hi! Speak with me, if you can :))"))
    send_fb(recipient, postback_template("Want to know weather?", "Show Weather", WEATHER_POSTBACK))
    send_fb(recipient, postback_template("Want to play?", "Question game", QUESTION_POSTBACK))


def handle_weather_ask(fsm, context):
    recipient = context.sender_id
    send_fb_message(recipient, format_to_user("Hi, i'm from heroku, give me your city name, and I'll tell you what is outside."))


# get current weather from owm api and sends it to chat
def handle_weather_reply(fsm, context):
    location = get_text_from_message(context.messaging_event).strip()
    if location:
        message = owm_get_weather(location)
        context.user.set_location(location)
    else:
        message = "No location, sorry."
    recipient = context.sender_id
    send_fb_message(recipient, format_to_user(message))


def handle_prepare_question(fsm, context):
    recipient = context.sender_id
    send_fb_message(recipient, format_to_user("Ask Your question about data science."))


# stores list of available answers and asks about relevant category
def handle_question(fsm, context):
    words = get_words_from_message(context.messaging_event)
    user = context.user
    message = None
    if words:
        model_helper = context.model_helper
        topics = model_helper.get_relevant_refs_topics(words)
        user.set_topics(topics)
        log("relevant_topics = {}".format(topics))
        categories = model_helper.get_relevant_topics_cats(topics)
        log("Categories: " + str(categories))
        question_cats = categories[-3:]
        if len(question_cats) > 1:
            question_or = ''.join([" or {}".format(c) for c in question_cats[1:]])
            message = "Is it from {}{} category?".format(question_cats[0], question_or)
        else:
            message = "Is it from {} category?".format(question_cats[0])
        user.set_category_query(question_cats)
    else:
        fsm.next_state = "init"

    recipient = context.sender_id
    send_fb_message(recipient, format_to_user(message))


# removes wrong category answers, asks about topic
def handle_category(fsm, context):
    user = context.user

    # parse user answer
    reply_words = get_text_from_message(context.messaging_event)
    reply = format_to_wiki(reply_words)

    model_helper = context.model_helper
    # find out what category is in answer
    reply_cat = get_intersection([reply], user.category_query)
    recipient = context.sender_id

    message = None

    # answer should contain one word from request
    if len(reply_cat) == 1:
        category_name = reply_cat[0]
        topics = model_helper.filter_topics_by_cat(user.topics, category_name)
        user.set_topics(topics)
        message = "Got {}.".format(category_name)

    # answer to user
    send_fb_message(recipient, format_to_user(message))

    # try to get most relevant topic
    straight_ask(fsm, user, recipient)


# receives straight question reply, asks ones more
def handle_straight(fsm, context):
    user = context.user
    reply = format_to_wiki(get_text_from_message(context.messaging_event))
    question_topic = user.straight_query
    topics = user.topics
    recipient = context.sender_id

    log("Topics: " + str(topics))
    if get_intersection([reply], STRAIGHT_QUERY_NEGATIVE):

        # "no" answer
        log("Got no!")
    elif get_intersection([reply], STRAIGHT_QUERY_POSITIVE):

        # "yes" answer: return wiki url and go to init state
        log("Got yes!")
        message = WIKI_URL + str(format_to_wiki(question_topic))
        recipient = context.sender_id
        send_fb_message(recipient, message)
        fsm.next_state = 'init'
        return
    straight_ask(fsm, user, recipient)


def straight_ask(fsm, user, recipient):
    # try to get most relevant topic
    if user.topics and len(user.topics):
        user.set_straight_query(user.topics[-1])
        user.set_topics(user.topics[:-1])
        # got question
        question = "Is it {} topic?".format(user.straight_query)
        send_fb_message(recipient, format_to_user(question))
    else:
        send_fb_message(recipient, format_to_user("No variants."))
        fsm.next_state = 'init'
    log("user.topics" + str(user.topics))


fsm = FSM('init')
fsm.set_default_transition(error, 'init')
fsm.add_transition_any('init', handle_say_hello, 'init')

fsm.add_transition(WEATHER_POSTBACK, 'init', handle_weather_ask, 'weather_ask')
fsm.add_transition_any('weather_ask', handle_weather_reply, 'init')

fsm.add_transition(QUESTION_POSTBACK, 'init', handle_prepare_question, 'question')
fsm.add_transition_any('question', handle_question, 'category_question')
fsm.add_transition_any('category_question', handle_category, 'straight_question')
fsm.add_transition_any('straight_question', handle_straight, 'straight_question')