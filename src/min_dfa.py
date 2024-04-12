class MIN_DFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.min_dfa = None
        self.min_dfa_states = None

    def minimize(self):
        #! Step 1: Split the states into two groups
        # Group 1: Accepting states
        # Group 2: Non-accepting states
        group1 = []
        group2 = []

        for state in self.dfa.states:
            if state in self.dfa.accepting_states:
                group1.append(state)
            else:
                group2.append(state)

        #! Step 2: Split the groups until no further splits are possible
        groups = [group1, group2]
        new_groups = []

        while groups != new_groups:
            new_groups = groups
            groups = self.split_groups(groups)

        #! Step 3: Create the minimized DFA
        self.min_dfa_states = self.create_minimized_states(groups)
        self.min_dfa = self.create_minimized_dfa()

        return self.min_dfa

    def create_minimized_states(self, groups):
        states = []

        # for idx, group in enumerate(groups):
        #    state = State(f"q{idx}")
        #   state.is_accepting = any([state in self.dfa.accepting_states for state in group])
        #   states.append(state)

        return states

    def to_graph(self):
        pass

    def visualize(self):
        pass
