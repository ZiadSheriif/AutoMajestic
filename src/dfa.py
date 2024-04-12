from collections import deque
from utils.helpers import dump_json
import graphviz


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa_states = self.construct_dfa()

    def _epsilon_closure(self, states):
        closure = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            for symbol, next_state in current_state.transitions:
                if symbol == "ε" and next_state not in closure:
                    stack.append(next_state)
                    closure.add(next_state)

        closure = list(closure)
        closure.sort(key=lambda x: x.label)

        # insert ' ' in the closure set
        closure = " ".join([state.label for state in closure])
        # print("closure: ", closure)
        return closure

    def _move(self, state, symbol):
        next_states = set()

        states = state.split()
        states_list = []
        for label in states:
            state = self.nfa.get_state_by_label(label)
            # print("State in Move!: ", state.label)
            states_list.append(state)
        for state in states_list:
            for s, next_state in state.transitions:
                if s == symbol:
                    next_states.add(next_state)
        return next_states

    def construct_dfa(self):
        dfa_transitions = {}
        symbols = self.nfa.get_symbols()
        dfa_start = self._epsilon_closure([self.nfa.start])
        self.dfa_states = {'startingState': dfa_start}

        queue = deque([dfa_start])
        visited = set([dfa_start])

        while queue:
            current_state = queue.popleft()
            # print("current_state: ", current_state)
            for symbol in symbols:
                next_states = self._epsilon_closure(self._move(current_state, symbol))
                # print("next_states in DFA: ", next_states)
                if next_states == " " or next_states == "":
                    continue
                if next_states not in visited:
                    queue.append(next_states)
                    visited.add(next_states)
                self.dfa_states.setdefault(current_state, {})[symbol] = next_states
            states_by_label = self.nfa.get_states_by_label(current_state)
            self.dfa_states.setdefault(current_state, {})["isTerminatingState"] = self.nfa.is_accepting_state_reachable(states_by_label)

        # TODO complete the implementation after Eid break :)

        return self.dfa_states
        # Convert the NFA to a DFA using the subset construction algorithm
        

        
    def visualize(self, name="output/dfa/dfa.gv", view=True):
        graph = graphviz.Digraph(name="DFA", engine="dot")
        
        for state, transitions in self.dfa_states.items():
    
            if state == "startingState":
                # graph.node(state, shape="point")
                continue
            if transitions["isTerminatingState"]:
                graph.node(state, shape="doublecircle")
            else:
                graph.node(state, shape="circle")
                
                
            for symbol, next_state in transitions.items():
                if symbol == "isTerminatingState":
                    continue
                children = next_state.split(",")
                for child in children:
                    graph.edge(state, child, label=symbol)
        graph.render(name, view=view)
        

    def minimize(self):
        pass
        # Minimize the DFA

    def to_graph(self):
        dump_json({**self.dfa_states}, "output/dfa/dfa.json")
        return self.dfa_states
