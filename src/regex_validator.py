import re


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex

    def validate(self):
        try:
            re.compile(self.regex)
            return True
        except re.error:
            return False
