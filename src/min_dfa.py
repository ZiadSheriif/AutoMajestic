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
        condensed_states = {}
        
        for idx, group in enumerate(groups):
            for state in group:
                for key, value in state.items():
                    condensed_states[key] = str(idx)
        
        new_groups = {'startingState': 0}
        copy_groups = groups.copy()
        for idx, group in enumerate(copy_groups):
            for state in group:
                for key, value in state.items():
                    for symbol,next_state in value.items():
                        if next_state in condensed_states:
                            value[symbol] = str(condensed_states[next_state])
                            new_groups[str(idx)] = value
        
                    
        return new_groups

    def to_graph(self):
        return self.min_dfa_states

    def visualize(self, name="output/min-dfa/min-dfa.gv", view=True):
        graph = graphviz.Digraph(name="MIN_DFA", engine="dot")
        
        for state, transitions in self.min_dfa_states.items():
            if state == "startingState":
                continue
                
            if transitions["isTerminatingState"]:
                graph.node(state, shape="doublecircle")
            else:
                graph.node(state, shape="circle")
            
            
            for symbol, next_state in transitions.items():
                if symbol == "isTerminatingState":
                    continue
                    
                children_states = next_state.split(" ")
                for child in children_states:
                    graph.edge(state, child, label=symbol)
                
        graph._format = "png"
        graph.attr(rankdir="LR")
        graph.render(name, view=view)
        return graph
        
