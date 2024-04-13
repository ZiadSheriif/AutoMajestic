import os
import json


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# dumping the nfa to a file json
def dump_json(nfa, filename):
    with open(filename, "w") as f:
        json.dump(nfa, f,ensure_ascii=False, indent=6)