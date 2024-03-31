class NFA:
    def __init__(self, regex):
        self.regex = regex
        self.nfa = self.construct_nfa()

    def construct_nfa(self):
        pass
        # Convert the regex to an NFA using Thompson's construction algorithm

    def to_graph(self):
        pass
        # Generate a graph of the NFA