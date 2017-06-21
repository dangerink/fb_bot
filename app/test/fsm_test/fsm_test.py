import unittest
from app.fsm.fsm import FSM
from tools.extention import get_intersection


class MockUser():

    def __init__(self, _id, uid, name, state, location, topics, straight_query, category_query):
        self.id = _id
        self.uid = uid
        self.name = name
        self.state = state
        self.location = location
        self.topics = topics
        self.straight_query = straight_query
        self.category_query = category_query


class MockMessageContext():

    def __init__(self, user=None, sender_id=None, event_type=None, messaging_event=None, model_helper=None):
        self.user = user
        self.state = user.state
        self.sender_id = sender_id
        self.event_type = event_type
        self.messaging_event = messaging_event
        self.model_helper = model_helper


class MockModelHelper():

    def get_relevant_refs_topics(self, ref_names):
        return ref_names

    def get_relevant_topics_cats(self, topic_names):
        return topic_names

    def filter_topics_by_cat(self, topic_names, cat):
        return get_intersection(topic_names, [cat])


def set_context1(fsm, context):
    context.user.name = "name1"

def set_context2(fsm, context):
    context.user.name = "name2"


class FSMTest(unittest.TestCase):
    def setUp(self):
        user = MockUser(_id="id", uid="uid", name="", state="state1", location="london", topics = ["top1", "top2", "top3"],straight_query="computer", category_query=["cat_a", "cat_b"])
        message = {"messaging_event": "message", "text":"message_text"}
        model_helper = MockModelHelper()
        self.context = MockMessageContext(user=user, sender_id="sender",event_type="input_a", messaging_event=message, model_helper=model_helper)
        self.fsm = FSM("init")

    def transition_test(self):
        assert self.fsm.current_state == "init"
        self.fsm.set_state("state1")
        assert self.fsm.current_state == "state1"
        self.fsm.add_transition("input_a", "state1", set_context1, "state2")
        self.fsm.add_transition("input_b", "state1", set_context2, "state3")
        self.fsm.process(self.context)
        assert self.context.user.name == "name1"
        assert self.fsm.current_state == "state1"
        assert self.fsm.next_state == "state2"

    def bad_transition_test(self):
        assert self.fsm.current_state == "state1"
        self.fsm.add_transition("input_a", "state1", set_context1, "state2")
        self.fsm.add_transition("input_b", "state1", set_context2, "state3")
        self.fsm.process(self.context)
        assert self.context.user.name == ""
        assert self.fsm.current_state == "state1"
        assert self.fsm.next_state == "init"

    def any_transition_test(self):
        assert self.fsm.current_state == "state1"
        self.fsm.add_transition("input_a", "state1", set_context1, "state2")
        self.fsm.add_transition_any("state1", set_context2, "state3")
        self.fsm.process(self.context)
        assert self.context.user.name == "name2"
        assert self.fsm.current_state == "state1"
        assert self.fsm.next_state == "state3"


if __name__ == "__main__":
    unittest.main()