import os
import json
import graphviz


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# dumping the nfa to a file json
def dump_json(nfa, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(nfa, f, ensure_ascii=False, indent=6)


def get_keys_by_group_state(group):
    keys = []
    for state in group:
        for key, value in state.items():
            keys.append(key)

    return keys
    
    
    
    
    
def visualize(nfa_graph,name="output/nfa/nfa.gv", view=False,pattern=None):
   
    print("NFA Graph: ", nfa_graph)
    graph = graphviz.Digraph(name="NFA", engine="dot")
    for state in nfa_graph:
        if state == "startingState":
            graph.node(state, style="invisible")
        else:
            shape= "doublecircle" if nfa_graph[state]["isTerminatingState"] else "circle"
            graph.node(state, shape=shape)

    # Add the edges to the graph
    for from_state in nfa_graph:
        if from_state == "startingState":
            graph.edge(tail_name=from_state, head_name=nfa_graph["startingState"])
            continue

        for input in nfa_graph[from_state]:
            if input == "isTerminatingState":
                continue
            to_states = nfa_graph[from_state][input]
            # Decide to Draw edge or edges based on
            # whether have a single destination or a list of destinations
            if type(to_states) == list:
                for to_state in to_states:
                    graph.edge(tail_name=from_state, head_name=to_state, label=input)
            else:
                graph.edge(tail_name=from_state, head_name=to_states, label=input)

    # graph.format = "png"
    graph.attr(rankdir="LR")
    graph.attr(label="NFA's pattern: " + pattern, fontname='bold')
    graph.render(name, view=view)

    return graph    
