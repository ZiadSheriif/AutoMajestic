import re


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = None

    def validate(self):
        try:
            if self.regex.count("[") != self.regex.count("]"):
                print("Invalid regular expression: unmatched brackets")
                return False
            re.compile(self.regex)
        except re.error:
            print("Invalid regex:", self.regex)
            return False
        return True

    # replace hyphen with operator "|" to separate the range of characters in the character class
    # as example: [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.
    #!   as example: [a-z] will be converted to (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z) and so on.
    def replace_range(self, match):
        start = None
        end = None
        flag = False
        idx = 0
        replaced = ""
        while idx < len(match.group()):
            char = match.group()[idx]
            if char == "[":
                replaced += "("
            elif char == "]":
                if replaced[-1] == "|":
                    replaced = replaced[:-1] + ")"  # remove the last character
                else:
                    replaced += ")"
            elif char == "-":
                flag = True
            else:
                if flag:
                    end = char
                    flag = False
                    for i in range(ord(start), ord(end) + 1):
                        replaced += chr(i)
                        replaced += "|"
                else:
                    start = char
                    replaced += chr(ord(char))
                    replaced += "|"
            idx += 1
        return replaced

    # insert . operator between adjacent characters
    def insert_dot(self, match):
        new_pattern = []
        for i in range(len(match) - 1):
            a = match[i]
            b = match[i + 1]
            # catches [*(  , +( , ?( , )( , a( ] || [ab or )a , *a , +a , ?a]
            new_pattern.append(a)
            if (a.isalnum() or a == ")" or a in "*+?") and (b.isalnum() or b == "("):
                new_pattern.append(".")
        new_pattern.append(match[-1])
        return "".join(new_pattern)

    def clean_regex(self):
        pattern = re.sub(r"\[.*?\]", self.replace_range, self.regex)
        self.postfix = self.insert_dot(pattern)
        return self.postfix

    def shunting_yard(self):
        # apply the shunting yard algorithm to convert the infix regular expression to postfix

        # we will order regular expressions syntax is listed as in the documentation
        # supported regex syntax
        operators = {"|": 1, ".": 2, "*": 3, "+": 3, "?": 3}
        stack = []
        postfix = []
        for operator in self.postfix:
            if operator == "(":
                stack.append(operator)
            elif operator == ")":
                while stack[-1] != "(":
                    postfix.append(stack.pop())
                stack.pop()  #! ==> remove the left parenthesis '('
            elif (
                stack and operator in operators and stack[-1] == "("
            ):  #! ==> if the operator is an operator and the top of the stack is a left parenthesis
                stack.append(operator)
            elif operator in operators:
                while (
                    stack
                    and operators[operator] <= operators[stack[-1]]
                    and stack[-1] != "("
                ):
                    postfix += stack.pop()
                stack.append(operator)
            else:
                postfix.append(operator)
            # print("stack: ", stack)
            # print("postfix: ", postfix)
        while stack:
            postfix.append(stack.pop())

        prefix = "".join(postfix)
        return postfix, prefix
