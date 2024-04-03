############################
#! Entry point
############################


from src.regex_validator import RegexValidator


if __name__ == "__main__":
    regex_one = RegexValidator(r"(\d+)")
    regex_two = RegexValidator(r"[A-Za-z")
    regex_three = RegexValidator(r"[a-zA-Z]")
    print(regex_one.validate())
    print(regex_two.validate())
    print(regex_three.validate())
    regex_three.post_validate()
