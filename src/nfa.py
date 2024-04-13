from src.state import State
from utils.helpers import dump_json
import graphviz

class NFA:
    def __init__(self, start=None, accept=None, postfix=None):
        self.start = start
        self.accept = accept
        if postfix and not start and not accept:
            self.nfa = self.construct_nfa(postfix)
            self.start = self.nfa.start
            self.accept = self.nfa.accept

    def get_state_by_label(self, label):
        for state in self.get_states():
            if state.label == label:
                return state

    def get_states(self):
        states = []
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        while queue:
            current_state = queue.pop(0)
            # print("state: ", current_state.label)
            # print ("Transitions of current state: ", [state.label for symbol, state in current_state.transitions])
            states.append(current_state)
            # print("Labels of States: ", [state.label for state in states])
            for _,state in current_state.transitions:
                if state not in visited:
                    queue.append(state)
                    visited.add(state)
        
        states.sort(key=lambda x: x.label)
        # print("Final Labels of States: ", [state.label for state in states])
            
        return states

    def get_accepting_states(self):
        return [state for state in self.get_states() if state.is_accepting]
        

    # check if one accpeting state is reachable from another accepting state
    def is_accepting_state_reachable(self,states):
        # print("States in is_accepting_state_reachable: ", states)
        for state in states:
            if state.is_accepting:
                return True
        return False
        
        

    def get_states_by_label(self, labels):
        labels = labels.split()
        states_by_label = []
        for label in labels:
            states_by_label.append(self.get_state_by_label(label))
        return states_by_label

    def get_symbols(self):
        symbols = set()
        states = self.get_states()
        for state in states:
            for symbol, _ in state.transitions:
                if symbol != "ε":
                    symbols.add(symbol)
        print("Symbols: ", list(symbols))
        return list(symbols)
        
        
        
    def handle_closure(char, nfa_stack, i):
        state_1 = nfa_stack.pop()
        start = State("S" + str(i))
        accept = State("S" + str(i + 1))
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", accept)
        state_1.accept.add_transition("ε", start)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))
        return i + 2 
        
    def handle_alternation(char, nfa_stack, i):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()
        start = State("S" + str(i))
        accept = State("S" + str(i + 1))
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", state_2.start)
        state_1.accept.add_transition("ε", accept)
        state_2.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))
        return i + 2
        
        
    def handle_concatenation(char, nfa_stack, i):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()                
        state_1.accept.add_transition("ε", state_2.start)
        nfa_stack.append(NFA(state_1.start, state_2.accept))
        return i 
        
    def handle_positive_closure(char, nfa_stack, i):
        state_1 = nfa_stack.pop()
        start = State("S" + str(i))
        accept = State("S" + str(i + 1))
        start.add_transition("ε", state_1.start)
        state_1.accept.add_transition("ε", start)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))
        return i + 2
        
    def handle_optional(char, nfa_stack, i):
        state_1 = nfa_stack.pop()
        start = State("S" + str(i))
        accept = State("S" + str(i + 1))
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", accept)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))
        return i + 2
        
    def handle_alpha_numeric(char, nfa_stack, i):
        start = State("S" + str(i))
        accept = State("S" + str(i + 1))
        start.add_transition(char, accept)
        nfa_stack.append(NFA(start, accept))
        return i + 2

    def construct_nfa(self, postfix):
        nfa_stack = []
        i = 1
        for char in postfix:
            if char == "*":
                i = NFA.handle_closure(char, nfa_stack, i)

            elif char == "|":
                i = NFA.handle_alternation(char, nfa_stack, i)
            elif char == ".":
                i = NFA.handle_concatenation(char, nfa_stack, i)
                
            elif char == "+":
                i = NFA.handle_positive_closure(char, nfa_stack, i)
            
            elif char == "?":
                i = NFA.handle_optional(char, nfa_stack, i)
            else:
                i = NFA.handle_alpha_numeric(char, nfa_stack, i)

        return nfa_stack.pop()

    def to_graph(self):

        states = {}
        for state in self.get_states():
            state_graph = {
                "isTerminatingState": state.is_accepting,
            }
            for symbol, transition in state.transitions:
                if symbol not in state_graph:
                    state_graph[symbol] = transition.label
                else:
                    state_graph[symbol] += "," + transition.label
            states[state.label] = state_graph
              
        # make a json object of the NFA graph
        dump_json({"startingState": self.start.label, **states}, "output/nfa/nfa.json")
            
            
        return {
            "startingState": self.start.label,
            **states,
        }

    def visualize(self, name="output/nfa/nfa.gv", view=False):
        nfa_graph = self.to_graph()
        graph = graphviz.Digraph(name="NFA",engine="dot")

        for state, transitions in nfa_graph.items():
            if state == "startingState":
                graph.node("", shape="none")
                graph.edge("", transitions)
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

        graph.format = "png"
        graph.attr(rankdir="LR")
        graph.render(name, view=view)

        return graph
