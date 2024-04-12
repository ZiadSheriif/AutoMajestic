# imports
from flask import Flask, send_file, request
import fitz
from flask_cors import CORS, cross_origin
from src.regex_validator import RegexValidator
from src.nfa import NFA
from utils.helpers import create_directory

# CORS configuration
origin = "http://localhost:5173"
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"


create_directory("output/nfa")
create_directory("output/dfa")


def pdf_to_png(pdf_path, png_path):
    pdf = fitz.open(pdf_path)
    for page_number in range(len(pdf)):
        page = pdf.load_page(page_number)
        pix = page.get_pixmap()
        png_path = png_path.format(page_number)
        pix.save(png_path, "png")


def run_pipeline(regex):
    print("##########  VALIDATION  #############")
    print("Regex:", regex)

    # Validate the regex
    regex_validator = RegexValidator(regex)
    if not regex_validator.validate():
        return None

    # Convert the regex to postfix notation
    postfix_regex = regex_validator.post_validate()
    print("Postfix notation:", postfix_regex)

    # Convert the regex to an NFA
    nfa = NFA(postfix=postfix_regex)
    nfa.visualize(name="output/nfa/nfa.gv", view=False)
    return nfa

@cross_origin(origins="*")
@app.route("/compile/nfa", methods=["GET"])
def compile_regex():

    regex = request.args.get("regex")

    nfa = run_pipeline(regex)

    if nfa is None:
        return "Invalid regex", 400

    pdf_to_png("output/nfa/nfa.gv.pdf", "output/nfa/nfa{}.png")

    return send_file("output/nfa/nfa0.png", mimetype="image/png")

    # ? in case of using base64 encoding
    with open("output/nfa/nfa.png", "rb") as f:
        image_data = f.read()
        encoded_image = base64.b64encode(image_data).decode("utf-8")

    return jsonify({"image": encoded_image})


if __name__ == "__main__":
    app.run(port=5000, debug=False)
