import re


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = None

    def validate(self):
        try:
            if self.regex.count('[') != self.regex.count(']'):
                print("Invalid regular expression: unmatched brackets")
                return False
            re.compile(self.regex)
        except re.error:
            print("Invalid regex:" , self.regex)
            return False
        return True

    def post_validate(self):
        # we will order regular expressions syntax is listed as in the documentation
        # supported regex syntax
        operators = {"(":0,"|": 1, ".": 2, "?": 3, "+": 4, "*": 5}
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
                        print("regex[j + 1:]: ", regex[j + 1:])
                        print("regex[: j + 1]: ", regex[: j + 1])
                    j += 1

        # then, replace the character class with the new alternation
        regex = regex.replace("[", "(").replace("]", ")")
        print(regex)

        ############################################################
        ############################################################

        # replace hyphen with operator "|" to separate the range of characters in the character class
        # as example: [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.
        # as example: [a-z] will be converted to (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z) and so on.
        self.postfix = regex[:]
        print(self.postfix)
        hyphens_count = self.postfix.count("-")
        # print("hyphens_count: ", hyphens_count)
        # print("self.postfix: ", len(self.postfix))
        for i in range(hyphens_count):
            for j in range(len(self.postfix)):
                operator = self.postfix[j]
                # if (a-z) ==> (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)
                if operator == "-":
                    temp = ""
                    end = ord(self.postfix[j + 1])
                    start = ord(self.postfix[j - 1])
                    print("start: ", start)
                    print("end: ", end)
                    print("regex[j]: ", self.postfix)
                    print("regex[j - 1]: ", self.postfix[j - 1])
                    print("regex[j + 1]: ", self.postfix[j + 1])
                    for z in range(int(end - start)):
                        temp += "|"
                        char = chr(start + z + 1)
                        temp += char
                    self.postfix = self.postfix[0:j] + temp + self.postfix[j + 2 :]
                    break
        print("regex after replacing hyphens with alternation: ", self.postfix)
        
        # insert . operator between adjacent characters
        dots_container = []
        start_ops = ["*", ")", "+"]
        end_ops = ["*", "+",".", ")", "|"]

        for i in range(len(self.postfix) - 1):
            if self.postfix[i].isalnum() and (self.postfix[i + 1].isalnum() or self.postfix[i + 1] == "("):
                dots_container.append(i)
            elif self.postfix[i] in start_ops and self.postfix[i + 1] not in end_ops:
                dots_container.append(i)

        for i in range(len(dots_container)):
            self.postfix = self.postfix[: dots_container[i] + i+ 1] + "." + self.postfix[dots_container[i] +i + 1 :]

        ############################################################
        ############################################################
        print("regex after inserting . operator: ", self.postfix)

        # apply the shunting yard algorithm to convert the infix regular expression to postfix
        stack = []
        postfix = ""
        for i in range(len(self.postfix)):
            operator = self.postfix[i]
            if operator == "(":
                stack.append(operator)
            elif operator == ")":
                while stack[-1] != "(":
                    postfix += stack.pop()
                stack.pop() #! ==> remove the left parenthesis '('
            elif operator in operators:
                while stack and operators[operator] <= operators[stack[-1]]:
                    postfix += stack.pop() 
                stack.append(operator)
            else:
                postfix += operator
            # print("stack: ", stack)
            # print("postfix: ", postfix)
        while stack:
            postfix += stack.pop()

        print("final postfix: ", postfix)

        return postfix
