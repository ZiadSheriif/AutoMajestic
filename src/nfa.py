from utils.helpers import dump_json

current_state_number = 1


class NFA:
    def __init__(self, start=None, accept=None, state_input=None):
        if start is None or accept is None or state_input is None:
            self.start = NFA.get_new_state()
            self.accept = NFA.get_new_state()
            self.states = {self.start: {}, self.accept: {}}
        else:
            self.start = start
            self.accept = accept
            self.states = {self.start: {state_input: accept}, self.accept: {}}
    @staticmethod
    def reset_state_number():
        global current_state_number
        current_state_number = 1

    @staticmethod
    def get_new_state():
        global current_state_number
        state = "S" + str(current_state_number)
        current_state_number += 1
        return state

    def add_epsilon_transitions(self, from_state, to_state):
        if "ε" in self.states[from_state]:
            if type(self.states[from_state]["ε"]) == list:
                self.states[from_state]["ε"].append(to_state)
            else:
                self.states[from_state]["ε"] = [self.states[from_state]["ε"], to_state]
        else:
            self.states[from_state]["ε"] = to_state

    # (*)
    def handle_closure(self, nfa_stack):
        state_1 = nfa_stack.pop()
        start = NFA.get_new_state()
        accept = NFA.get_new_state()

        self.add_epsilon_transitions(self.accept, self.start)
        self.add_epsilon_transitions(self.accept, accept)
        self.states[start] = {"ε": self.start}
        self.states[accept] = {}

        self.start = start
        self.accept = accept
        self.add_epsilon_transitions(self.start, self.accept)

        nfa_stack.append(state_1)

    # (|)
    def handle_alternation(self, nfa_stack):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()
        start = NFA.get_new_state()
        accept = NFA.get_new_state()

        self.states[start] = {"ε": [state_1.start, state_2.start]}
        self.states[accept] = {}

        self.add_epsilon_transitions(self.accept, accept)
        state_2.add_epsilon_transitions(state_2.accept, accept)

        self.states.update(state_2.states)

        self.start = start
        self.accept = accept
        nfa_stack.append(state_1)

    # (.)
    def handle_concatenation(self, nfa_stack):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()

        self.add_epsilon_transitions(self.accept, state_2.start)
        self.states.update(state_2.states)
        self.accept = state_2.accept
        nfa_stack.append(state_1)

    # (+)
    def handle_positive_closure(self, nfa_stack):
        state_1 = nfa_stack.pop()
        start = NFA.get_new_state()
        accept = NFA.get_new_state()

        self.add_epsilon_transitions(self.accept, self.start)
        self.add_epsilon_transitions(self.accept, accept)
        self.states[start] = {"ε": self.start}
        self.states[accept] = {}

        self.start = start
        self.accept = accept
        nfa_stack.append(state_1)

    # (?)
    def handle_optional(self, nfa_stack):
        state_1 = nfa_stack.pop()
        self.add_epsilon_transitions(self.start, self.accept)
        nfa_stack.append(state_1)

    # (a-zAz , 0-9)
    def handle_alpha_numeric(self, char, nfa_stack):
        nfa = NFA(
            start=NFA.get_new_state(), accept=NFA.get_new_state(), state_input=char
        )
        nfa_stack.append(nfa)

    def to_graph(self):
        nfa_states = self.states
        for state in nfa_states:
            nfa_states[state]["isTerminatingState"] = state == self.accept
        nfa_states.update({"startingState": self.start})
        dump_json(nfa_states, "output/nfa/nfa.json")
        return nfa_states


def construct_nfa(postfix_reg):
    stack = []

    for symbol in postfix_reg:
        if symbol == "|":
            nfa_right = stack.pop()
            nfa_left = stack.pop()
            nfa_left.handle_alternation([nfa_left, nfa_right])
            stack.append(nfa_left)
        elif symbol == ".":
            nfa_right = stack.pop()
            nfa_left = stack.pop()
            nfa_left.handle_concatenation([nfa_left, nfa_right])
            stack.append(nfa_left)
        elif symbol == "*":
            nfa = stack.pop()
            nfa.handle_closure([nfa])
            stack.append(nfa)
        elif symbol == "+":
            nfa = stack.pop()
            nfa.handle_positive_closure([nfa])
            stack.append(nfa)
        elif symbol == "?":
            nfa = stack.pop()
            nfa.handle_optional([nfa])
            stack.append(nfa)
        else:
            nfa = NFA(
                start=NFA.get_new_state(),
                accept=NFA.get_new_state(),
                state_input=symbol,
            )
            stack.append(nfa)

    return stack.pop().to_graph()
