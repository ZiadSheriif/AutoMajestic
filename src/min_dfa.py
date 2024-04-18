from utils.helpers import dump_json
import graphviz

class MIN_DFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.min_dfa_states = self.minimize()
        

    def minimize(self):

        states = self.dfa.to_graph()
        symbols = self.dfa.get_symbols()
        states.pop("startingState")

        #! Step 1: Split the states into two groups
        # Group 1: Accepting states
        # Group 2: Non-accepting states
        group1 = []
        group2 = []
        all_groups = []

        for key, value in states.items():
            if value["isTerminatingState"]:
                group1.append({key: value})
            else:
                group2.append({key: value})

        all_groups.append(group1)
        all_groups.append(group2)

        #! [[{'S2 S3 S5 S6': {'b': 'S4 S6', 'isTerminatingState': True}}, {'S4 S6': {'isTerminatingState': True}}], [{'S1': {'a': 'S2 S3 S5 S6', 'isTerminatingState': False}}]]

        #! #############    Step 2: Split the groups until no further splits are possible  #############
        #! for each group split the group into subgroups based on the transitions of each state ,
        #! if there is a transition to a state in another group then split the group
        symbol_groups = {}
        i = -1
        length = len(all_groups)
        while i < length:
            i += 1
            if i < 0:
                i = 0
            if i >= len(all_groups):
                break    
            current_group = all_groups[i]
            
            isSplitted = False
            if len(current_group) < 2:
                continue
            for symbol in symbols:
                if isSplitted:
                    break
                symbol_groups = {}
                for j in range(len(current_group)):
                    current_state = current_group[j]
                    for key, value in current_state.items():
                            if symbol in value:
                                for k in range(len(all_groups)):
                                    for state in all_groups[k]:
                                        if (value[symbol] in state):
                                            if symbol not in symbol_groups:
                                                symbol_groups[symbol] = {}
                                            if k not in symbol_groups[symbol]:
                                                symbol_groups[symbol][k] = [current_state]
                                            else:
                                                symbol_groups[symbol][k].append(current_state)

                            else:
                                k = "none"
                                if symbol not in symbol_groups:
                                    symbol_groups[symbol] = {}
                                if k not in symbol_groups[symbol]:
                                    symbol_groups[symbol][k] = [current_state]
                                else:
                                    symbol_groups[symbol][k].append(current_state)
                                
                for key, value in symbol_groups.items():
                    # Check if the symbol is present in multiple groups
                    if len(value) > 1:
                        all_groups[i] = []
                        isSplitted = True
                        # Extract states associated with each group
                        for group_index, states in value.items():
                        
                            all_groups.append(states)
                                    
                        i = -1
                        break
                length = len(all_groups)       
        # Remove empty groups from all_groups            
        all_groups = [group for group in all_groups if group]     



                    
        #! Step 3: Create the minimized DFA
        self.min_dfa_states = self.create_minimized_states(all_groups)
        
        

        return self.min_dfa_states

    def create_minimized_states(self, groups):
        # print("########################################################################################")
        # print("\n\n")
        # print("Groups in MIN_DFA: ", groups)
        # print("########################################################################################")
        # print("\n\n")
        #![[{'S2 S3 S5 S6': {'b': 'S4 S6', 'isTerminatingState': True}}], [{'S4 S6': {'isTerminatingState': True}}], [{'S1': {'a': 'S2 S3 S5 S6', 'isTerminatingState': False}}]]
        condensed_states = {}

        # This function to sort groups to visualize it correct
        def sort_key(group):
            first_state = list(group[0].keys())[0]
            first_state_num = int(first_state.split("S")[-1])
            return first_state_num

    
        groups = sorted(groups, key=sort_key)

        for idx, group in enumerate(groups,start=1):
            for state in group:
                # for all states in the group, update the name of the state to the index of the group
                for key, value in state.items():
                    condensed_states[key] = str(idx)
        
        new_groups = {'startingState': 1}
    
        for idx, group in enumerate(groups,start=1):
            # iterate over each state in the group    
            for state in group:
                # iterate over each symbol in the state
                for key, value in state.items():
                    # iterate over each symbol in the state
                    for symbol, next_state in value.items():
                        if symbol!='isTerminatingState':
                            # check if the next state is in the condensed states , then update the value of the state
                            if next_state in condensed_states:
                                value[symbol] = str(condensed_states[next_state])
                                new_groups[str(idx)] = value
                                
        for state, group_index in condensed_states.items():
            if group_index not in new_groups:
                new_groups[group_index] = {'isTerminatingState': True}
        #! New Groups in DFA: {'startingState': 1, '1': {'b': '2', 'isTerminatingState': True}, '3': {'a': '1', 'isTerminatingState': False}}            
        return new_groups

    def to_graph(self, group_mapping):
        for state_label, state_info in self.min_dfa_states.items():
            if state_label == "startingState":
                continue
            updated_state_info = {"isTerminatingState": state_info["isTerminatingState"]}
            for symbol, next_state_label in state_info.items():
                if symbol == "isTerminatingState":
                    continue
                if symbol in group_mapping:
                    updated_symbol = group_mapping[symbol]
                else:
                    updated_symbol = symbol
                updated_state_info[updated_symbol] = next_state_label
            self.min_dfa_states[state_label] = updated_state_info
        dump_json({**self.min_dfa_states}, "output/min-dfa/min-dfa.json")
        return self.min_dfa_states

    def visualize(self, name="output/min-dfa/min-dfa.gv", view=True, pattern=None):
        graph = graphviz.Digraph(name="MIN_DFA", engine="dot")
        
        for state, transitions in self.min_dfa_states.items():
            if state == "startingState":
                graph.node("", shape="none")
                graph.edge("", "1", color="blue",)
                continue
                
            if transitions["isTerminatingState"]:
                graph.node(state, shape="doublecircle", color="red") 
            else:
                graph.node(state, shape="circle", color="green")  
                
            for symbol, next_state in transitions.items():
                if symbol == "isTerminatingState":
                    continue
                children_states = next_state.split(",")
                for child in children_states:
                    graph.edge(state, child, label=symbol, color="black") 

        graph.format = "png"
        graph.attr(rankdir="LR", label="MIN-DFA's pattern: " + pattern, fontname='bold', bgcolor='lightyellow',format='png')
        graph.render(name, view=view)
        return graph

        
