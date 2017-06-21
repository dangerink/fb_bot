import unittest
from app.fsm.fsm_bot import handle_weather_reply, handle_question, handle_category, handle_straight
from app.fsm.fsm import FSM
from app.test.fsm_test.fsm_test import MockUser, MockMessageContext, MockModelHelper


def set_context1(fsm, context):
    context.user.name = "name1"

def set_context2(fsm, context):
    context.user.name = "name2"


class FSMBotTest(unittest.TestCase):

    def setUp(self):
        user = MockUser(_id="id", uid="uid", name="", state="state1", location="london",
                        topics = ["topic", "top2", "top3"], straight_query="computer", category_query=["topic", "cat_b"])
        message = {"messaging_event": "message", "message": {"text" : "topic"}}
        model_helper = MockModelHelper()
        self.context = MockMessageContext(user=user, sender_id="sender",event_type="input_a", messaging_event=message, model_helper=model_helper)
        self.fsm = FSM("init")

    def handle_weather_reply_test(self):
        handle_weather_reply(self.fsm, self.context)

    def handle_question_test(self, ):
        handle_question(self.fsm, self.context)
        message = self.context.messaging_event["message"]["text"]
        assert self.context.user.topics == message
        assert self.context.user.category_query == message

    def handle_category_fail_test(self):
        self.context.user.topics = ["top3"]
        handle_category(self.fsm, self.context)
        assert not self.context.user.topics == ["topic"]

    def handle_category_pass_test(self):
        handle_category(self.fsm, self.context)
        assert self.context.user.topics == [""]

    def handle_straight_pass_test(self):
        handle_straight(self.fsm, self.context)
        assert self.context.user.topics == [""]

if __name__ == "__main__":
    unittest.main()

