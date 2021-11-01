from flask import render_template, redirect, url_for, request
from flaskapp import app
from .mean_std import *
from .suni import *

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usrid=request.form["ownerid"]
        return redirect(url_for("user", usr=usrid))
    return render_template('login.html')

@app.route('/<usr>')
def user(usr):
    # open files
    user_profile = pd.read_excel("../hs_g73_m08/user_profile.xlsx")   # 임시
    user_data = read_data(user_profile, "..//hs_g73_m08/")             # 임시

    # 순이 대화
    name = extract_user_name(user_data[int(usr)])       # 사용자 이름
    num_res = num_response(user_data[int(usr)])         # 응답 횟수
    len_res = len_response(user_data[int(usr)])         # 평균 응답 길이
    prob_res = probability_to_response_to_action(user_data[int(usr)])  # 응답률(list)
    for (action, prob) in prob_res:
        if action == "전체":
            prob_res2 = int(prob * 100)
    more_than_3_res_type = True if (len(prob_res) >= 3) else False

    avg_res = avg_response(user_data)                       # 전체 평균 응답 횟수
    avg_len = avg_response_length(user_data)                # 전체 평균 응답 길이
    avg_prob = avg_probability_to_response(user_data)       # 전체 평균 응답률

    # 프로그램 참여
    programs = participated_program(user_data[int(usr)])    # 프로그램 참여량
    len_programs = len(programs)
    more_than_3_programs = True if (len_programs > 3) else False    # 전체 평균 포함되어있어서 1 추가.
    total_programs = 0
    for item in programs:
        total_programs += item[1]
    avg_programs = 0
    for person in user_data:
        tmp = participated_program(user_data[person])
        for item in tmp:
            avg_programs += item[1]
    avg_programs = round(avg_programs / len(user_data.keys()), 2)

    return render_template('main.html', usr=usr, name=name,
                           num_res=num_res, len_res=len_res,
                           prob_res=prob_res, prob_res2=prob_res2, more_than_3_res_type=more_than_3_res_type,
                           avg_res=avg_res, avg_len=avg_len, avg_prob=avg_prob,
                           programs=programs, len_programs=len_programs, more_than_3_programs=more_than_3_programs,
                           total_programs=total_programs, avg_programs=avg_programs)

    # toilet = average_num_use(usr, '화장실 이용')
    # hobby = average_num_use(usr, '취미활동')
    # bm = mean_time_of_state(usr, '조식')
    # lm = mean_time_of_state(usr, '중식')
    # dm = mean_time_of_state(usr, '석식')
    # bs = std_time_of_state(usr, '조식')
    # ls = std_time_of_state(usr, '중식')
    # ds = std_time_of_state(usr, '석식')
    # rmm = mean_time_of_state(usr, '일반 약 복용')
    # rms = std_time_of_state(usr, '일반 약 복용')
    # stm = mean_time_of_state(usr, '수면')
    # sts = std_time_of_state(usr, '수면')
    # atm = mean_time_of_state(usr, '기상하기')
    # ats = std_time_of_state(usr, '기상하기')
    # avs = angle_to_hms(angle_dif(atm, stm))
    #return render_template('main.html', usr=usr)
    # return render_template('main.html', usr=usr, toilet=toilet, hobby=hobby, bm=bm, lm=lm, dm=dm, bs=bs, ls=ls, ds=ds, rmm=rmm, rms=rms, stm=stm, sts=sts, atm=atm, ats=ats, avs=avs)
