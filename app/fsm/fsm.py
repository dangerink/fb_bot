from tools.logger import log


class FSM:

    def __init__(self, initial_state):

        # Map (input, current_state) --> (action, next_state).
        self.state_transitions = {}

        # Map (current_state) --> (action, next_state).
        self.transitions_any = {}

        self.default_transition = None
        self.initial_state = initial_state

        # At begining, state is initial
        self.current_state = self.initial_state
        self.next_state = self.initial_state

    def reset(self):
        self.current_state = self.initial_state

    # Adds (input, current_state) - > (action, next_state) transition
    def add_transition(self, input, state, action=None, next_state=None):
        if next_state is None:
            next_state = state
        self.state_transitions[(input, state)] = (action, next_state)

    # Add  (current_state) - > (action, next_state) transition, with any input
    def add_transition_any (self, state, action=None, next_state=None):
        if next_state is None:
            next_state = state
        self.transitions_any[state] = (action, next_state)

    # Default is transition when fsm_test doesn't know that to do
    def set_default_transition (self, action, next_state):
        self.default_transition = (action, next_state)

    # Looks for transition in state_transition then in state_transition_any,
    # then use default_transition, if it is None raise exception
    def get_transition (self, input, state):
        if self.state_transitions.has_key((input, state)):
            return self.state_transitions[(input, state)]
        elif self.transitions_any.has_key (state):
            return self.transitions_any[state]
        elif self.default_transition is not None:
            return self.default_transition
        else:
            raise Exception('Transition is undefined: (%s, %s).' %
                (str(input), str(state)))

    # set FSM state before process
    def set_state(self, state):
        self.current_state = state

    def process(self, context):
        log("FSM in state {}. Received Message = {}".format(self.current_state, context.messaging_event))

        # Get action and next_state from defined configuration
        action, self.next_state = self.get_transition(context.event_type, self.current_state)

        if action is not None:
            action(self, context)
