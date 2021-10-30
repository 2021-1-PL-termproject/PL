from flask import render_template, redirect, url_for, request
from flaskapp import app
from .mean_std import *

@app.route('/', methods=["POST", "GET"])
@app.route('/main/', methods=["POST", "GET"])
def main():
    if request.method == "POST":
        usrid=request.form["ownerid"]
        return redirect(url_for("user", usr=usrid))
    else:
        return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    if type(get_csv(usr)) == str:
        return 'No User'
    return render_template('main.html', usr=usr)
