import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from power import *
from parser import *

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

@app.route("/parse")
def parse():
	pseudocode = request.args.get("input")
	currents[session["id"]] = parse_input(pseudocode, currents[session["id"]])

	return str(roots[session["id"]])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
