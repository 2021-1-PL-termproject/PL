from flask import render_template, redirect, url_for, request
from flaskapp import app

@app.route('/', methods=["POST", "GET"])
@app.route('/main/', methods=["POST", "GET"])
def main():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template('index.html')

@app.route('/<usr>')
def user(usr):
    return render_template('user.html', content=usr)
