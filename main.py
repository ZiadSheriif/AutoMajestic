############################
#! Entry point
############################

from src.regex_validator import RegexValidator
from src.nfa import NFA
from src.dfa import DFA
from src.min_dfa import MIN_DFA
from utils.helpers import create_directory


def run_pipeline(test_cases):
    # Create the output directories if they don't exist
    create_directory("output/nfa")
    create_directory("output/dfa")
    create_directory("output/min-dfa")

    for idx, test_case in enumerate(test_cases, start=1):
        print(f"##########  TEST CASE {idx}  #############")
        print("Regex:", test_case)

        # Validate the regex
        regex_validator = RegexValidator(test_case)

        if not regex_validator.validate():
            continue

        # Convert the regex to postfix notation
        postfix_regex = regex_validator.post_validate()
        # print("Postfix notation:", postfix_regex)

        # Convert the regex to an NFA
        nfa = NFA(postfix=postfix_regex)
        # print("NFA ", nfa.to_graph())
        nfa.visualize(name=f"output/nfa/nfa_{idx}.gv", view=False)
        
        print("##########  DFA  #############")
        # Convert the NFA to a DFA
        dfa = DFA(nfa)
        dfa.to_graph()
        dfa.visualize(name=f"output/dfa/dfa_{idx}.gv", view=False)

        # Minimize the DFA
        minimized_dfa = MIN_DFA(dfa)
        minimized_dfa.visualize(name=f"output/min-dfa/min-dfa_{idx}.gv", view=False)


if __name__ == "__main__":

    test_cases = [
        # r"ab[ce-df]",
        # r"ab[ce-df",
        r"ab?",
        # r"ab]",
        # r"aab+a*ba(a|b)",
        # r"aab+a*ba(a|b)",
    ]

    run_pipeline(test_cases)
