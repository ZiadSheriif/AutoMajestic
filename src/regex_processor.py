from src.regex_validator import RegexValidator
from src.nfa import NFA, construct_nfa,visualize
from src.dfa import DFA
from src.min_dfa import MIN_DFA
from utils.helpers import create_directory


class RegexProcessor:
    def __init__(self, regex):
        self.regex = regex

    def process(self, idx):
        create_directory("output/nfa")
        create_directory("output/dfa")
        create_directory("output/min-dfa")

        print(f"\033[1;33m{'#' * 30}\n#     Regex Processor     #\n{'#' * 30}\033[0m\n")
        print(f"Regex: {self.regex}\n")

        # Validate the regex
        regex_validator = RegexValidator(self.regex)

        if not regex_validator.validate():
            return "Error", None, None

        # clean the regex
        cleaned_regex = regex_validator.clean_regex()
        print(f"\033[1;32mCleaned regex: {cleaned_regex}\n\033[0m")

        # Convert the regex to postfix notation
        postfix_regex,_ = regex_validator.shunting_yard()
        print(f"\033[1;32mPostfix notation: {postfix_regex}\n\033[0m")
        

        # Convert the regex to an NFA
        nfa = construct_nfa(postfix_regex)
        print(f"\033[1;36mNFA: {nfa.to_graph()}\n\033[0m")
        visualize(name=f"output/nfa/nfa_{idx}.gv", view=False)

        # # Convert the NFA to a DFA
        # dfa = DFA(nfa)
        # # print(f"\033[1;36mDFA: {dfa.to_graph()}\n\033[0m")
        # dfa.visualize(name=f"output/dfa/dfa_{idx}.gv", view=False)

        # # Minimize the DFA
        # minimized_dfa = MIN_DFA(dfa)
        # minimized_dfa.visualize(name=f"output/min-dfa/min-dfa_{idx}.gv", view=False)

        return "Success",None,None
