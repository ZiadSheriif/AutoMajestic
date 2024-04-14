from src.regex_processor import RegexProcessor

if __name__ == "__main__":
    test_cases = [
        # r"ab[ce-df]",
        # r"ab[ce-df",
        r"ab+",
        # r"ab]",
        # r"abb+a?(a|b)",
        # r"aab+a*ba(a|b)",
    ]

    for idx, test_case in enumerate(test_cases, start=1):
        print(f"\033[1;33m{'#' * 30}\n#     TEST CASE {idx}     #\n{'#' * 30}\033[0m\n")

        print("Regex:", test_case)

        processor = RegexProcessor(test_case)
        status, nfa, minimized_dfa = processor.process(idx)

        if status == "Success":
            print("Processing successful!")
        else:
            print("Invalid regex")
