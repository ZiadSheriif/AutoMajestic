from flask import Flask, jsonify, request
import fitz
import base64
from flask_cors import CORS

from src.regex_validator import RegexValidator
from src.nfa import NFA
from src.dfa import DFA
from src.min_dfa import MIN_DFA
from utils.helpers import create_directory

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

create_directory("output/nfa")
create_directory("output/dfa")
create_directory("output/min-dfa")
group_mapping = {}


def pdf_to_png(pdf_path, png_path):
    pdf = fitz.open(pdf_path)
    for page_number in range(len(pdf)):
        page = pdf.load_page(page_number)
        pix = page.get_pixmap()
        png_path = png_path.format(page_number)
        pix.save(png_path, "png")


def run_pipeline(regex, step):
    print("##########  VALIDATION  #############")
    print("Regex:", regex)

    # Validate the regex
    regex_validator = RegexValidator(regex)
    if not regex_validator.validate():
        return None

    # Convert the regex to postfix notation
    postfix_regex = regex_validator.post_validate(group_mapping)
    print("Postfix notation:", postfix_regex)

    # Convert the regex to an NFA
    nfa = NFA(postfix=postfix_regex)
    nfa.to_graph(group_mapping)
    nfa.visualize(name=f"output/nfa/nfa.gv", view=False, pattern=regex, group_mapping=group_mapping)

    if step == "dfa" or step == "min-dfa":
        dfa = DFA(nfa)
        dfa.visualize(name=f"output/dfa/dfa.gv", view=False, pattern=regex)
        if step == "min-dfa":
            dfa_min = MIN_DFA(dfa)
            dfa_min.to_graph(group_mapping)
            dfa_min.visualize(name="output/min-dfa/min-dfa.gv", view=False, pattern=regex)
            return dfa_min
        return dfa

    return nfa


def compile_regex_pipeline(step):
    regex = request.args.get("regex")
    automaton = run_pipeline(regex, step)
    if automaton is None:
        return "Invalid regex", 400

    # pdf_to_png(f"output/{step}/{step}.gv.pdf", f"output/{step}/{step}.png")

    with open(f"output/{step}/{step}.gv.png", "rb") as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

    return jsonify({"image": encoded_image})


@app.route("/compile/nfa", methods=["GET"])
def compile_nfa():
    return compile_regex_pipeline("nfa")


@app.route("/compile/dfa", methods=["GET"])
def compile_dfa():
    return compile_regex_pipeline("dfa")


@app.route("/compile/min-dfa", methods=["GET"])
def compile_min_dfa():
    return compile_regex_pipeline("min-dfa")


@app.route("/", methods=["GET"])
def home():
    return """
<html>
    <head>
        <title>AutoMajestic</title>
        <style>
            body {
                 background-color: #1e1e1e;
                color: #eee;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #61dafb;

            }
            ul {
                list-style-type: none;
                padding-left: 0;
                margin-top: 20px;
            }
            li {
                margin-bottom: 10px;
            }
            p {
                margin-top: 20px;
            }
            footer {
                margin-top: 50px;
                color: #777;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to AutoMajestic!</h1>
        <p>AutoMajestic is your go-to server for exploring the world of regular expressions and finite automata.</p>
        <ul>
            <li>Developed as a part of the Compiler Language course.</li>
            <li>Project aims to demonstrate the conversion of regular expressions to NFAs and DFAs.</li>
            <li>Includes visualization of DFA and Minimized DFA (min-DFA).</li>
        </ul>
        <footer>
            &copy; 2024 Ziad & Rome. All rights reserved. Under the supervision of Eng. Omar Samir.
        </footer>
    </body>
</html>

    """


if __name__ == "__main__":
    app.run(port=5000, debug=False)
