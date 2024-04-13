from utils.helpers import get_keys_by_group_state
import graphviz

class MIN_DFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.min_dfa_states = self.minimize()
        

    def minimize(self):

        states = self.dfa.to_graph()
        symbols = self.dfa.get_symbols()
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

        print("Group1: ", group1)
        print("Group2: ", group2)
        print("All Groups: ", all_groups)
        #! [[{'S2 S3 S5 S6': {'b': 'S4 S6', 'isTerminatingState': True}}, {'S4 S6': {'isTerminatingState': True}}], [{'S1': {'a': 'S2 S3 S5 S6', 'isTerminatingState': False}}]]

        #! #############    Step 2: Split the groups until no further splits are possible  #############
        #! for each group split the group into subgroups based on the transitions of each state ,
        #! if there is a transition to a state in another group then split the group
        
        is_split = True
        while is_split: #All Groups:  [[{'b': 'S3 S4 S5 S6', 'isTerminatingState': True}, {'b': 'S3 S4 S5 S6', 'isTerminatingState': True}], [{'a': 'S2 S3 S5 S6', 'isTerminatingState': False}]]
            is_split = False 
            for idx, group in enumerate(all_groups): #Group:  [{'b': 'S3 S4 S5 S6', 'isTerminatingState': True}, {'b': 'S3 S4 S5 S6', 'isTerminatingState': True}], idx: 0, [{'a': 'S2 S3 S5 S6', 'isTerminatingState': False}] idx:  1
                if not group:
                    continue
                new_groups = {}
                first_state = next(iter(group)) # {'b': 'S3 S4 S5 S6', 'isTerminatingState': True}
                print("First State: ", first_state)
                for key, value in first_state.items():
                    for symbol in symbols:
                        print("Symbol: ", value, symbol)
                        if symbol in value:
                           new_groups[symbol] = [jdy for jdy,group in enumerate(all_groups) if value[symbol] in get_keys_by_group_state(group)][0]
                print("New Groups: ", new_groups)
            
                separated_states = []
                for k, v in enumerate(group):
                    out_groups={}
                    for key, value in v.items():
                        for symbol in symbols:
                            if symbol in value:
                                list_of_groups = [jdy for jdy,group in enumerate(all_groups) if value[symbol] in get_keys_by_group_state(group)]
                                out_groups[symbol] = list_of_groups[0]
                    if out_groups != new_groups:
                        separated_states.append(v)
                        is_split = True
                if len(separated_states) > 0:
                    all_groups.insert(idx+1, list(separated_states))
                    all_groups[idx] = [x for x in group if x not in separated_states]
                

                    
        #! Step 3: Create the minimized DFA
        self.min_dfa_states = self.create_minimized_states(all_groups)

        return self.min_dfa_states

    def create_minimized_states(self, groups):
        print("Groups in MIN_DFA: ", groups)
        #![[{'S2 S3 S5 S6': {'b': 'S4 S6', 'isTerminatingState': True}}], [{'S4 S6': {'isTerminatingState': True}}], [{'S1': {'a': 'S2 S3 S5 S6', 'isTerminatingState': False}}]]
        condensed_states = {}
        # print("Groups in MIN_DFA: ", groups)
        
        for idx, group in enumerate(groups,start=1):
            for state in group:
                # for all states in the group, update the name of the state to the index of the group
                for key, value in state.items():
                    condensed_states[key] = str(idx)
        
        new_groups = {'startingState': 1}
        copy_groups = groups.copy()
        for idx, group in enumerate(copy_groups,start=1):
            # iterate over each state in the group    
            for state in group:
                # iterate over each symbol in the state
                for key, value in state.items():
                    # iterate over each symbol in the state
                    for symbol, next_state in value.items():
                        # check if the next state is in the condensed states , then update the value of the state
                        if next_state in condensed_states:
                            value[symbol] = str(condensed_states[next_state])
                            new_groups[str(idx)] = value
        
        print("New Groups in DFA: ", new_groups)
        #! New Groups in DFA: {'startingState': 1, '1': {'b': '2', 'isTerminatingState': True}, '3': {'a': '1', 'isTerminatingState': False}}            
        return new_groups

    def to_graph(self):
        return self.min_dfa_states

    def visualize(self, name="output/min-dfa/min-dfa.gv", view=True):
        graph = graphviz.Digraph(name="MIN_DFA", engine="dot")
        print("Minimized DFA States: ", self.min_dfa_states)
        #! Minimized DFA States:  {'startingState': 1, '1': {'b': '2', 'isTerminatingStx`ate': True}, '3': {'a': '1', 'isTerminatingState': False}}
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
        
