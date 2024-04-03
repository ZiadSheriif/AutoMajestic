import re


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = None

    def validate(self):
        try:
            re.compile(self.regex)
            return True
        except re.error:
            return False

    def post_validate(self):
        # we will order regular expressions syntax is listed as in the documentation
        # supported regex syntax
        operators = {
            "|": 1,
            ".": 2,
            "?": 3,
            "*": 3,
            "+": 3,
            "^": 4,
            "$": 4,
            "(": 5,
            ")": 5,
        }
        regex = self.regex

        # Check if the regular expression contains any character classes (denoted by square brackets).
        # If a character class is found, the function converts it to an "alternation" #!`() between the characters inside the class`.
        # as example: [xyz] => (x|y|z) and [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.

        for i in range(len(regex)):
            operator = regex[i]
            if operator == "[":
                j = i + 1
                while regex[j] != "]":
                    if regex[j].isalnum() and regex[j + 1].isalnum():
                        regex = regex[: j + 1] + "|" + regex[j + 1 :]
                    j += 1

        # then, replace the character class with the new alternation
        regex = regex.replace("[", "(").replace("]", ")")
        print(regex)

        ############################################################
        ############################################################

        # replace hyphen with operator "|" to separate the range of characters in the character class
        # as example: [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.
        # as example: [a-z] will be converted to (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z) and so on.
        regex_copy = regex[:]
        print(regex_copy)
        hyphens_count = regex_copy.count("-")
        print("hyphens_count: ", hyphens_count)
        print("regex_copy: ", len(regex_copy))
        for i in range(hyphens_count):
            for j in range(len(regex_copy)):
                operator = regex_copy[j]
                # if (a-z) ==> (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)
                if operator == "-":
                    temp = ""
                    end = ord(regex_copy[j + 1])
                    start = ord(regex_copy[j - 1])
                    print("start: ", start)
                    print("end: ", end)
                    print("regex[j]: ", regex_copy)
                    print("regex[j - 1]: ", regex_copy[j - 1])
                    print("regex[j + 1]: ", regex_copy[j + 1])
                    for z in range(int(end - start)):
                        temp += "|"
                        char = chr(start + z + 1)
                        temp += char
                    regex_copy = regex_copy[0:j] + temp + regex_copy[j + 2 :]
                    break
        print("regex after replacing hyphens with alternation: ", regex_copy)

        # insert . operator between adjacent characters
        dots_container = []
        start_ops = ["*", "+", ")"]
        end_ops = ["*", "+", ")", "|", "."]

        for i in range(len(regex_copy) - 1):
            if regex_copy[i].isalnum() and regex_copy[i + 1].isalnum():
                dots_container.append(i)
            elif regex_copy[i] in start_ops and regex_copy[i + 1] not in end_ops:
                dots_container.append(i)

        for i in dots_container:
            regex_copy = regex_copy[: i + 1] + "." + regex_copy[i + 1 :]
        return regex_copy
