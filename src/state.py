class State:
    def __init__(self, label,  transitions=[], parents=[], is_accepting=True,is_starting=False):
        self.label = label
        self.transitions = transitions
        self.is_starting = is_starting
        self.is_accepting = is_accepting
        self.parents = parents

    def add_transition(self, symbol, state):
        # if symbol not in self.transitions:
            # self.transitions[symbol] = []
        self.transitions.append((symbol, state))
        state.parents.append(self)
        self.is_accepting = False

    def get_parents(self):
        return self.parents.copy()
