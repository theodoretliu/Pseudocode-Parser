from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

    
# configure application
app = Flask(__name__)

Session(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/parse")
def parse():
	code = request.args.get("input")
	return code