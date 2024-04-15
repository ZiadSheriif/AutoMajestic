from collections import deque
from utils.helpers import dump_json
import graphviz


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.dfa_states = self.construct_dfa()
        
    def get_symbols(self):
        return self.nfa.get_symbols()
    def get_states(self):
        return self.nfa.get_states()

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
        # print("First Epsilon Closure: ", dfa_start)
        self.dfa_states = {'startingState': dfa_start}

        queue = deque([dfa_start])
        visited = set([dfa_start])

        while queue:
            current_state = queue.popleft()
            # print("current_state: ", current_state)
            for symbol in symbols:
                next_moves = self._move(current_state, symbol)
                if not next_moves:
                    continue
                next_states = self._epsilon_closure(next_moves)
                # print("Current State: ", current_state)
                # print("Symbol: ", symbol)
                # print("Moves: ", [state.label for state in next_moves])
                # print("Epsilon Closures: ", next_states)
                if next_states == " " or next_states == "":
                    continue
                if next_states not in visited:
                    queue.append(next_states)
                    visited.add(next_states)
                self.dfa_states.setdefault(current_state, {})[symbol] = next_states
            states_by_label = self.nfa.get_states_by_label(current_state)
            self.dfa_states.setdefault(current_state, {})["isTerminatingState"] = self.nfa.is_accepting_state_reachable(states_by_label)

        # TODO complete the implementation after Eid break :)
        dump_json({**self.dfa_states}, "output/dfa/dfa.json")
        return self.dfa_states
        

        
    def visualize(self, name="output/dfa/dfa.gv", view=True, pattern=None):
        graph = graphviz.Digraph(name="DFA", engine="dot")
        
        for state, transitions in self.dfa_states.items():

            if state == "startingState":
                graph.node("", shape="none", color="blue")  
                graph.edge("", transitions, color="blue")  
                continue
            if transitions["isTerminatingState"]:
                graph.node(state, shape="doublecircle", color="red")  
            else:
                graph.node(state, shape="circle", color="green") 
                
            for symbol, next_state in transitions.items():
                if symbol == "isTerminatingState":
                    continue
                children = next_state.split(",")
                for child in children:
                    graph.edge(state, child, label=symbol, color="black")  

        graph.format = "png"
        graph.attr(rankdir="LR", label="DFA's pattern: " + pattern, fontname='bold', bgcolor='lightyellow')  
        graph.render(name, view=view)

        


    def to_graph(self):
        return self.dfa_states
