from src.state import State
from utils.helpers import dump_json
import graphviz
import base64


class NFA:

    current_state_number = 1 # static variable to keep track of the state number
    
    def __init__(self, start=None, accept=None, postfix=None):
        self.start = start
        self.accept = accept
        if postfix and not start and not accept:
            self.nfa = self.construct_nfa(postfix)
            self.start = self.nfa.start
            self.accept = self.nfa.accept
            
    @staticmethod
    def get_new_state():
        state = State("S" + str(NFA.current_state_number))
        NFA.current_state_number += 1
        return state 

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
      
        states= self.rename_states(states)
            
        return states
        
    def rename_states(self,states):
        for i in range(len(states)):
            states[i].label = "S" + str(i+1)
        states.sort(key=lambda x: x.label)
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
        # print("Symbols: ", list(symbols))
        return list(symbols)
        
        
    # *   
    def handle_closure(char, nfa_stack):
        state_1 = nfa_stack.pop()
        start =  NFA.get_new_state()
        accept =  NFA.get_new_state()
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", accept)
        state_1.accept.add_transition("ε", start)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))
    # |   
    def handle_alternation(char, nfa_stack):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()
        start =  NFA.get_new_state()
        accept =  NFA.get_new_state()
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", state_2.start)
        state_1.accept.add_transition("ε", accept)
        state_2.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))

        
     # .   
    def handle_concatenation(char, nfa_stack):
        state_2 = nfa_stack.pop()
        state_1 = nfa_stack.pop()                
        state_1.accept.add_transition("ε", state_2.start)
        nfa_stack.append(NFA(state_1.start, state_2.accept))

     # +   
    def handle_positive_closure(char, nfa_stack):
        state_1 = nfa_stack.pop()
        start =  NFA.get_new_state()
        accept =  NFA.get_new_state()
        start.add_transition("ε", state_1.start)
        state_1.accept.add_transition("ε", start)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))

     # ?   
    def handle_optional(char, nfa_stack):
        state_1 = nfa_stack.pop()
        start =  NFA.get_new_state()
        accept =  NFA.get_new_state()
        start.add_transition("ε", state_1.start)
        start.add_transition("ε", accept)
        state_1.accept.add_transition("ε", accept)
        nfa_stack.append(NFA(start, accept))

     # a-z, A-Z, 0-9   
    def handle_alpha_numeric(char, nfa_stack):
        start =  NFA.get_new_state()
        accept =  NFA.get_new_state()
        start.add_transition(char, accept)
        nfa_stack.append(NFA(start, accept))


    def construct_nfa(self, postfix):
        nfa_stack = []
        for char in postfix:
            if char == "*":
                NFA.handle_closure(char, nfa_stack)
            elif char == "|":
                 NFA.handle_alternation(char, nfa_stack)
            elif char == ".":
                 NFA.handle_concatenation(char, nfa_stack)
                
            elif char == "+":
                 NFA.handle_positive_closure(char, nfa_stack)
            
            elif char == "?":
                 NFA.handle_optional(char, nfa_stack)
            else:
                NFA.handle_alpha_numeric(char, nfa_stack)

        return nfa_stack.pop()

    def to_graph(self,group_mapping):

        states = {}
        # print("States: ", [state.label for state in self.get_states()])
        for state in self.get_states():
            state_graph = {
                "isTerminatingState": state.is_accepting,
            }
            for symbol, transition in state.transitions:
                if symbol != "ε":
                    if symbol in group_mapping:
                        symbol = group_mapping[symbol]
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

    def visualize(self, pattern, name="output/nfa/nfa.gv", view=False,group_mapping=None):
        nfa_graph = self.to_graph(group_mapping)
        graph = graphviz.Digraph(name="NFA", engine="dot")

        for state, transitions in nfa_graph.items():
            if state == "startingState":
                graph.node("", shape="none")
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
        graph.attr(rankdir="LR", label="NFA's pattern: " + pattern, fontname='bold', bgcolor='lightyellow')  
        graph.render(name, view=view)

        
        # image_data = graph.pipe(format='png')
        # base64_image = base64.b64encode(image_data).decode('utf-8')
        # return graph
