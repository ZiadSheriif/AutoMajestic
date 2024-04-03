############################
#! Entry point
############################


from src.regex_validator import RegexValidator


if __name__ == "__main__":
    regex_one = RegexValidator(r"ab(c|d)")
    regex_two = RegexValidator(r"[A-Za-z")
    regex_three = RegexValidator(r"[a-zA-Z]")

    print("##########  VALIDATION  #############")
    print(regex_one.validate())
    print(regex_two.validate())
    print(regex_three.validate())

    print("#######################")
    postfix_regex = regex_one.post_validate()
    print(postfix_regex)
    postfix_regex = regex_three.post_validate()
    print(postfix_regex)
