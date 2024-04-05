############################
#! Entry point
############################

from src.regex_validator import RegexValidator
from src.nfa import NFA
from utils.helpers import create_directory

if __name__ == "__main__":

    # Create the output directories
    create_directory("output/nfa")
    create_directory("output/dfa")
    
    # Validate the regex
    print("##########  VALIDATION  #############")
    regex_one = RegexValidator(r"ab(c|d)")
    regex_two = RegexValidator(r"ab[c-d")
    regex_three = RegexValidator(r"ab*")
    
    
    if regex_three.validate():
        print("Regex is valid")
    else:
        print("Regex is invalid")
        raise Exception("Invalid regex")
    
    
    
    # convert the regex to postfix notation
    postfix_regex = regex_three.post_validate()
    
    # Convert the regex to an NFA
    nfa = NFA(postfix=postfix_regex)
    print("NFA ",nfa.to_graph())
    nfa.visualize(name="output/nfa/nfa.gv",view=False)
    
    
    
    
