import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from power import *
from parser import parse_input

roots = dict()
currents = dict()
counter = 0
# configure application
app = Flask(__name__)
app.secret_key = b"}\xa8\x1b\xa6/\xf4\x91\xc3\xb2cQ\xa5Ec\x08\x13B$\x0f\x87\x07a\xec\xea"

@app.route("/")
def index():
	global counter

	if counter > 10000:
		counter = 0

	session["id"] = counter
	app.logger.debug(session["id"])
	counter += 1

	roots[session["id"]] = Parent()
	currents[session["id"]] = roots[session["id"]]

	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/help")
def help():
	return render_template("help.html")

@app.route("/parse")
def parse():
	pseudocode = request.args.get("input")
	is_error = False

	try:
		currents[session["id"]] = parse_input(pseudocode, currents[session["id"]])
	except:
		is_error = True

	return jsonify(isError=is_error, code=str(roots[session["id"]]))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
