from utils.helpers import get_keys_by_group_state
import graphviz

class MIN_DFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.min_dfa_states = self.minimize()
        

    def minimize(self):

        states = self.dfa.to_graph()
        symbols = self.dfa.get_symbols()
        print("############################################ Min Dfa #########################################")
        print("Symbols: ", symbols)
        print("States: ", states)
        # for key in list(states.keys())[1:]:
        #     print(f"{key}: {states[key]}")
        states.pop("startingState")

        #! Step 1: Split the states into two groups
        # Group 1: Accepting states
        # Group 2: Non-accepting states
        group1 = []
        group2 = []
        all_groups = []

        # for key in list(states.keys())[1:]:
        #     if states[key]["isTerminatingState"]:
        #         group1.append(states[key])
        #     else:
        #         group2.append(states[key])
        for key, value in states.items():
            if value["isTerminatingState"]:
                group1.append({key: value})
            else:
                group2.append({key: value})

        all_groups.append(group1)
        all_groups.append(group2)

        # print("Group1: ", group1)
        # print("Group2: ", group2)
        # print("All Groups: ", all_groups)
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
            print("\n")
            print("\n")
            print("i ==> ",i)
            print("length ==> ",length)
            current_group = all_groups[i]
            print("Current Group: ",current_group)
            
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
                                            print(symbol,current_state, " is looking in group ",k)
                                            if symbol not in symbol_groups:
                                                symbol_groups[symbol] = {}
                                            if k not in symbol_groups[symbol]:
                                                symbol_groups[symbol][k] = [current_state]
                                            else:
                                                symbol_groups[symbol][k].append(current_state)
                                            print(symbol_groups)

                            else:
                                print(symbol,current_state," don't have")
                                k = "none"
                                if symbol not in symbol_groups:
                                    symbol_groups[symbol] = {}
                                if k not in symbol_groups[symbol]:
                                    symbol_groups[symbol][k] = [current_state]
                                else:
                                    symbol_groups[symbol][k].append(current_state)
                                print(symbol_groups)    
                
                for key, value in symbol_groups.items():
                    print("Key: ", key, " value: ", value)
                    # Check if the symbol is present in multiple groups
                    if len(value) > 1:
                        all_groups[i] = []
                        isSplitted = True
                        # Extract states associated with each group
                        for group_index, states in value.items():
                            print("group_index",group_index)
                            print("states: ",states)
                            all_groups.append(states)
                            # Remove original group from all_groups
                        # Insert the extracted states into all_groups and reset i to 0
                        
                        i = -1
                        break
                print("All groups: ", all_groups) 
                length = len(all_groups)       
        # Remove empty groups from all_groups            
        all_groups = [group for group in all_groups if group]     



                    
        #! Step 3: Create the minimized DFA
        self.min_dfa_states = self.create_minimized_states(all_groups)

        return self.min_dfa_states

    def create_minimized_states(self, groups):
        print("########################################################################################")
        print("\n\n")
        print("Groups in MIN_DFA: ", groups)
        print("########################################################################################")
        print("\n\n")
        #![[{'S2 S3 S5 S6': {'b': 'S4 S6', 'isTerminatingState': True}}], [{'S4 S6': {'isTerminatingState': True}}], [{'S1': {'a': 'S2 S3 S5 S6', 'isTerminatingState': False}}]]
        condensed_states = {}
        # print("Groups in MIN_DFA: ", groups)
        
        for idx, group in enumerate(groups,start=1):
            for state in group:
                # for all states in the group, update the name of the state to the index of the group
                for key, value in state.items():
                    condensed_states[key] = str(idx)
        
        print("condensed_states: ",condensed_states)
        new_groups = {'startingState': 1}
    
        for idx, group in enumerate(groups,start=1):
            # iterate over each state in the group    
            for state in group:
                # iterate over each symbol in the state
                for key, value in state.items():
                    # iterate over each symbol in the state
                    for symbol, next_state in value.items():
                        if symbol!='isTerminatingState':
                            print(next_state)
                            # check if the next state is in the condensed states , then update the value of the state
                            if next_state in condensed_states:
                                value[symbol] = str(condensed_states[next_state])
                                new_groups[str(idx)] = value
                                
        for state, group_index in condensed_states.items():
            if group_index not in new_groups:
                new_groups[group_index] = {'isTerminatingState': True}
        print("New Groups in DFA: ", new_groups)
        #! New Groups in DFA: {'startingState': 1, '1': {'b': '2', 'isTerminatingState': True}, '3': {'a': '1', 'isTerminatingState': False}}            
        return new_groups

    def to_graph(self):
        return self.min_dfa_states

    def visualize(self, name="output/min-dfa/min-dfa.gv", view=True):
        graph = graphviz.Digraph(name="MIN_DFA", engine="dot")
        # print("Minimized DFA States: ", self.min_dfa_states)
        #! Minimized DFA States:  {'startingState': 1, '1': {'b': '2', 'isTerminatingState': True}, '3': {'a': '1', 'isTerminatingState': False}, '2': {'b': '2', 'isTerminatingState': True}}
        for state, transitions in self.min_dfa_states.items():
            if state == "startingState":
                # graph.node("", shape="none")
                # graph.edge("", "1")
                continue
                
            if transitions["isTerminatingState"]:
                graph.node(state, shape="doublecircle")
            else:
                graph.node(state, shape="circle")
            
            
            for symbol, next_state in transitions.items():
                if symbol == "isTerminatingState":
                    continue
                    
                children_states = next_state.split(",")
                for child in children_states:
                    graph.edge(state, child, label=symbol)
                
        graph._format = "png"
        graph.attr(rankdir="LR")
        graph.render(name, view=view)
        return graph
        
