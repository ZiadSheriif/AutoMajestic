############################
#! Entry point
############################


from src.regex_validator import RegexValidator


if __name__ == "__main__":
    regex_one = RegexValidator(r"(\d+)")
    regex_two = RegexValidator(r"[A-Za-z")
    print(regex_one.validate())
    print(regex_two.validate())
