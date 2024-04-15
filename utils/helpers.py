import os
import json


def create_directory(directory):
    directory = os.path.join('/tmp', directory)
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
