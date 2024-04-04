############################
#! Entry point
############################

from src.regex_validator import RegexValidator

if __name__ == "__main__":

    print("##########  VALIDATION  #############")
    regex_one = RegexValidator(r"ab(c|d)")
    regex_three = RegexValidator(r"(A+B)*(C+D)")

    print("#######################")
    postfix_regex = regex_three.post_validate()
