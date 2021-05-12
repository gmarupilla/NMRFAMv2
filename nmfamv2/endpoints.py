from flask import Flask, jsonify, render_template, request

from nmfamv2.metabolite.metabolite_name_translator import translate_list_to_gizzmo_names

app = Flask(__name__)


@app.route("/translatenames", methods=["POST"])
def translate_names():
    if request.is_json:
        # print(request.get_json())

        namelist = translate_list_to_gizzmo_names(request.get_json()["metabolitenames"])
        json_ = {
            "metabolitenames": namelist
        }

        return jsonify(json_)


@app.route("/estimate", methods=["POST"])
def estimate():
    return "hello"


@app.route("/lookupmetabolitename", methods=["GET"])
def lookup_metabolite_name():
    return render_template("wasYourMetabolite.html", data="metab")


@app.route("/choice", methods=["GET"])
def choice():
    choice_req = request.args.get("choice")
    print("Choice: ", choice_req)
    if choice_req == "Algorithm":
        return render_template("algorithm_page.html")
    elif choice_req == "Metabolite Lookup":
        return render_template("metabolite_lookup.html")
    else:
        return render_template("error.html")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
