import re


class RegexValidator:
    def __init__(self, regex):
        self.regex = regex
        self.postfix = None

    def validate(self):
        try:
            if self.regex.count('[') != self.regex.count(']') or self.regex.count('(') != self.regex.count(')'):
                print("Invalid regular expression: unmatched brackets")
                return False
            re.compile(self.regex)
        except re.error:
            print("Invalid regex:" , self.regex)
            return False
        return True

    
    # Check if the regular expression contains any character classes (denoted by square brackets).
    # If a character class is found, the function converts it to an "alternation" #!`() between the characters inside the class`.
    # as example: [xyz] => (x|y|z) and [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.
    def replace_class(self,regex,group_mapping):
        in_class = False
        result = ""
        current_group = ""
        # alphabet = ord('A')
        alphabet = ['&', '%', '$', '#', '@', '!', '^', '=', '~', '/', '\\', ':', ';', '<', '>']
        idx=0
        for char in regex:
            if char == '[':
                in_class = True
                result += char
            elif char == ']':
                in_class = False
                group_key= alphabet[idx]
                group_mapping[group_key] = '[' + current_group+ ']'
                result += group_key+char
                idx += 1
                current_group = ""
            elif in_class:
                    current_group+= char
            else:
                result += char
        return result
        
        
    #! replace hyphen with operator "|" to separate the range of characters in the character class
    # as example: [0-9] will be converted to (0|1|2|3|4|5|6|7|8|9) and so on.
    # as example: [a-z] will be converted to (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z) and so on.   
    def detect_hyphen(self,regex):
        hyphens_count = regex.count("-")
        for i in range(hyphens_count):
            for j in range(len(regex)):
                operator = regex[j]
                # if (a-z) ==> (a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z)
                if operator == "-":
                    temp = ""
                    end = ord(regex[j + 1])
                    start = ord(regex[j - 1])
                    for z in range(int(end - start)):
                        temp += "|"
                        char = chr(start + z + 1)
                        temp += char
                    regex = regex[0:j] + temp + regex[j + 2 :]
                    break
        return regex
    def post_validate(self,group_mapping):
        # we will order regular expressions syntax is listed as in the documentation
        # supported regex syntax
        operators = {"(":0,"|": 1, ".": 2, "?": 3, "+": 4, "*": 5}
        regex = self.regex
        
        
        
        #! first, replace the character class with a new character class
        self.postfix = self.replace_class(regex,group_mapping)

        #! then, replace the character class with the new alternation
        self.postfix = self.postfix.replace("[", "(").replace("]", ")")
        print("regex after replacing character classes: ", self.postfix)

        ############################################################
        ############################################################
        # self.postfix = self.detect_hyphen(self.postfix)
        # print("regex after replacing hyphens with alternation: ", self.postfix)
        
        # insert . operator between adjacent characters
        dots_container = []
        start_ops = ["*", ")", "+","?"]
        end_ops = ["*", "+",".", ")", "|", "?"]

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

        # print("final postfix: ", postfix)
        return postfix
