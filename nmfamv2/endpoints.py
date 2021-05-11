from flask import Flask
from flask import request
from flask import jsonify

from MetaboliteNameTranslator import translateListToGizzmoNames

from flask import render_template

app = Flask(__name__)


@app.route("/translatenames", methods=["POST"])
def translatenames():
    if request.is_json:
        # print(request.get_json())

        namelist = translateListToGizzmoNames(request.get_json()["metabolitenames"])
        json_ = {
            "metabolitenames": namelist
        }

        return jsonify(json_)


@app.route("/estimate", methods=["POST"])
def estimate():
    return "hello"


@app.route("/lookupmetabolitename", methods=["GET"])
def lookupmetabolitename():
    return render_template("wasYourMetabolite.html", data="metab")


@app.route("/choice", methods=["GET"])
def choice():
    choice = request.args.get("choice")
    print("Choice: ", choice)
    if choice == "Algorithm":
        return render_template("algorithm_page.html")
    elif choice == "Metabolite Lookup":
        return render_template("metabolite_lookup.html")
    else:
        return render_template("error.html")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
