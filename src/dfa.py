from collections import deque
class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.construct_dfa()
        
    def _epsilon_closure(self, state):
        closure = set()
        stack = [state]
        while stack:
            current_state = stack.pop()
            closure.add(current_state)
            for symbol, next_state in current_state.transitions:
                if symbol == "ε" and next_state not in closure:
                    stack.append(next_state)
        closure = frozenset(closure)
        closure.sort(key=lambda x: x.label)
        
        # insert ' ' in the closure set
        closure = ' '.join([state.label for state in closure])
        return closure
        

    def construct_dfa(self,nfa):
        dfa_states = []
        dfa_transitions = {}
        nfa_states = nfa.get_states()
        symbols = nfa.get_symbols()
        
        dfa_start = self.epsilon_closure(nfa.start)
        queue = deque([dfa_start])
        visited = set([dfa_start])
        while queue:
            current_state = queue.popleft()
            for symbol in symbols:
                next_state = self.epsilon_closure(nfa.move(current_state, symbol))
                if next_state ==' ' or next_state == '':
                    continue
                if next_state not in visited:
                    queue.append(next_state)
                    visited.add(next_state)
                dfa_transitions[(current_state, symbol)] = next_state
                
        #TODO complete the implementation after Eid break :)
    
        
        pass
        # Convert the NFA to a DFA using the subset construction algorithm

    def minimize(self):
        pass
        # Minimize the DFA

    def to_graph(self):
        pass
        # Generate a graph of the DFA
