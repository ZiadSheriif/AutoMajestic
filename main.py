############################
#! Entry point
############################

from src.regex_validator import RegexValidator
from src.nfa import NFA

if __name__ == "__main__":

    print("##########  VALIDATION  #############")
    regex_one = RegexValidator(r"ab(c|d)")
    regex_three = RegexValidator(r"ab*")

    print("#######################")
    postfix_regex = regex_three.post_validate()
    nfa = NFA(postfix=postfix_regex)
    print("NFA ",nfa.to_graph())
    print("#######################")
    nfa.visualize(name="output/nfa.gv",view=False)
    
    
    
    
