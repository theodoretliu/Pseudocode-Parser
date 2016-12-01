import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from power import *
from parser import *


# configure application
app = Flask(__name__)

roots = dict()
currents = dict()

@app.route("/")
def index():
	roots[request.remote_addr] = Parent()
	currents[request.remote_addr] = roots[request.remote_addr]

	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/parse")
def parse():
	pseudocode = request.args.get("input")
	currents[request.remote_addr] = parse_input(pseudocode, currents[request.remote_addr])

	return str(roots[request.remote_addr])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
