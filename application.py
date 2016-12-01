import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from power import *
from parser import *


# configure application
app = Flask(__name__)

root = Parent()
current = root

@app.route("/")
def index():
	global root
	global current
	root = Parent()
	current = root
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/parse")
def parse():
	global current
	global root
	pseudocode = request.args.get("input")
	current = parse_input(pseudocode, current)

	return str(root)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
