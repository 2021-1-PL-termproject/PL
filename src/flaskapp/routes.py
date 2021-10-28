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
        return render_template('index.html')

@app.route('/<usr>')
def user(usr):
    if type(get_csv(usr)) == str:
        return 'No User'
    stm = mean_time_of_state(usr, '수면')
    sts = std_time_of_state(usr, '수면')
    atm = mean_time_of_state(usr, '기상하기')
    ats = std_time_of_state(usr, '기상하기')
    avs = angle_to_hms(angle_dif(atm, stm))

    rmm = mean_time_of_state(usr, '일반 약 복용')
    rms = std_time_of_state(usr, '일반 약 복용')

    toilet = average_num_use(usr, '화장실 이용')
    hobby = average_num_use(usr, '취미활동')

    bm = mean_time_of_state(usr, '조식')
    bs = std_time_of_state(usr, '조식')
    lm = mean_time_of_state(usr, '중식')
    ls = std_time_of_state(usr, '중식')
    dm = mean_time_of_state(usr, '석식')
    ds = std_time_of_state(usr, '석식')

    return render_template('user.html', usr=usr, stm=stm, sts=sts, atm=atm, ats=ats, avs=avs, rmm=rmm, rms=rms, toilet=toilet, hobby=hobby, bm=bm, bs=bs, lm=lm, ls=ls, dm=dm, ds=ds)
