from src.state import State
import graphviz

class NFA:
    def __init__(self, start=None, accept=None, postfix=None):
        self.start = start
        self.accept = accept
        if postfix and not start and not accept:
            self.nfa = self.construct_nfa(postfix)
            self.start = self.nfa.start
            self.accept = self.nfa.accept

    def _get_state_by_label(self, label):
        for state in self._get_states():
            if state.label == label:
                return state

    def _get_states(self):
        states = []
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        while queue:
            state = queue.pop(0)
            print("state: ", state.label)
            states.append(state)
            for  (transition) in state.transitions:
                if transition[1] not in visited:
                    queue.append(transition[1])
                    visited.add(transition[1])
            
                   
        return states

    def _get_accepting_states(self):
        return [state for state in self._get_states() if state.is_accepting]

    def _check_acceptance(self, state):
        return state in self._get_accepting_states()

    def _get_states_by_label(self, labels):
        labels = labels.split(",")
        states_by_label = []
        for label in labels:
            states_by_label.append(self._get_state_by_label(label))
        return states_by_label

    def _get_symbols(self):
        symbols = set()
        states = self._get_states()
        for state in states:
            for symbol in state.transitions.keys():
                if symbol != "ε":
                    symbols.add(symbol)
        return list(symbols)

    def construct_nfa(self, postfix):
        nf_stack = []
        i = 0
        for char in postfix:
            if char == "*" or char == "+":
                state_1 = nf_stack.pop()
                start = State("S" + str(i))
                accept = State("S" + str(i + 1))
                start.add_transition("ε", state_1.start)
                start.add_transition("ε", accept)
                state_1.accept.add_transition("ε", state_1.start)
                state_1.accept.add_transition("ε", accept)
                nf_stack.append(NFA(start, accept))
                i += 2

            elif char == "|":
                state_2 = nf_stack.pop()
                state_1 = nf_stack.pop()
                start = State("S" + str(i))
                accept = State("S" + str(i + 1))
                start.add_transition("ε", state_1.start)
                start.add_transition("ε", state_2.start)
                state_1.accept.add_transition("ε", accept)
                state_2.accept.add_transition("ε", accept)
                nf_stack.append(NFA(start, accept))
                i += 2
            elif char == ".":
                state_2 = nf_stack.pop()
                state_1 = nf_stack.pop()
                state_1.accept.add_transition("ε", state_2.start)
                nf_stack.append(NFA(state_1.start, state_2.accept))
                i += 2
            elif char == "?":
                state_1 = nf_stack.pop()
                start = State("S" + str(i))
                accept = State("S" + str(i + 1))
                start.add_transition("ε", state_1.start)
                start.add_transition("ε", accept)
                state_1.accept.add_transition("ε", accept)
                nf_stack.append(NFA(start, accept))
                i += 2
            else:
                start = State("S" + str(i))
                accept = State("S" + str(i + 1))
                start.add_transition(char, accept)
                nf_stack.append(NFA(start, accept))
                i += 2

        return nf_stack.pop()
        # Convert the regex to an NFA using Thompson's construction algorithm

    def to_graph(self):

        states = {}
        for state in self._get_states():
            state_graph = {
                "isTerminateState": state.is_accepting,
            }
            for symbol, transition in state.transitions:
                if symbol not in state_graph:
                    state_graph[symbol] = transition.label
                else:
                    state_graph[symbol] += "," + transition.label
            states[state.label] = state_graph

            return {
                "startingState": self.start.label,
                **states,
            }
            
        
    def visualize(self,name="output/nfa.gv",view=False):
        nfa_graph = self.to_graph()
        graph = graphviz.Digraph(engine="dot")
        
        for state, transitions in nfa_graph.items():
            if state == "startingState":
                continue
            if transitions["isTerminateState"]:
                graph.node(state, shape="doublecircle")
            else:
                graph.node(state, shape="circle")
                
                
            for symbol, next_state in transitions.items():
                if symbol == "isTerminateState":
                    continue
                children = next_state.split(",")
                for child in children:
                    graph.edge(state, child, label=symbol)
                
                

        graph.render(name, view=view)
        
        return graph