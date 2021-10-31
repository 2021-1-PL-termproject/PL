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
    hobby = average_num_use(usr, '취미활동')
    bm = mean_time_of_state(usr, '조식')
    lm = mean_time_of_state(usr, '중식')
    dm = mean_time_of_state(usr, '석식')
    bs = std_time_of_state(usr, '조식')
    ls = std_time_of_state(usr, '중식')
    ds = std_time_of_state(usr, '석식')
    rmm = mean_time_of_state(usr, '일반 약 복용')
    rms = std_time_of_state(usr, '일반 약 복용')
    stm = mean_time_of_state(usr, '수면')
    sts = std_time_of_state(usr, '수면')
    atm = mean_time_of_state(usr, '기상하기')
    ats = std_time_of_state(usr, '기상하기')
    avs = angle_to_hms(angle_dif(atm, stm))
    return render_template('main.html', usr=usr, toilet=toilet, hobby=hobby, bm=bm, lm=lm, dm=dm, bs=bs, ls=ls, ds=ds, rmm=rmm, rms=rms, stm=stm, sts=sts, atm=atm, ats=ats, avs=avs)
