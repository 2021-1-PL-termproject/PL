from flask import render_template, redirect, url_for, request
from flaskapp import app
from .mean_std import *

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usrid=request.form["ownerid"]
        return redirect(url_for("user", usr=usrid))
    return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    toilet = average_num_use(usr, '화장실 이용')
    return render_template('main.html', usr=usr, toilet=toilet)
