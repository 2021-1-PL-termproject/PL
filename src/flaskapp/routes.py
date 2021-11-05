from flask import render_template, redirect, url_for, request
from flaskapp import app
from .lifepattern import *
from .suni import *
from .Shin import *


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        usrid = request.form["ownerid"]
        return redirect(url_for("user", usr=usrid))
    return render_template('login.html')


@app.route('/<usr>')
def user(usr):
    # open files
    user_profile = pd.read_excel("hs_g73_m08/user_profile.xlsx")
    user_data = read_data(user_profile, "hs_g73_m08/")

    # 순이 대화
    name = extract_user_name(user_data[int(usr)])  # 사용자 이름
    num_res = num_response(user_data[int(usr)])  # 응답 횟수
    len_res = len_response(user_data[int(usr)])  # 평균 응답 길이

    prob_res, sorted_prob_res = probability_to_response_to_action(user_data[int(usr)])  # 응답률
    avg_prob_res = int(prob_res["전체"] * 100)  # 평균 응답률(유저)

    more_than_3_res_type = True if (len(prob_res) >= 3) else False

    avg_res = avg_response(user_data)  # 전체 평균 응답 횟수
    avg_len = avg_response_length(user_data)  # 전체 평균 응답 길이
    avg_prob = avg_probability_to_response(user_data)  # 전체 평균 응답률

    # 프로그램 참여
    program_times = participated_times(user_data[int(usr)])  # 프로그램 참여량
    program_days, sorted_program_days = participated_days(user_data[int(usr)])

    len_programs = len(program_times)
    avg_participation = avg_participated_times(user_data)

    total_programs = 0
    for p in program_times:
        total_programs += program_times[p]
    if len_programs >= 3:
        preference = program_preference(user_data, sorted_program_days[0][0])

    # 활동량
    exer = exercise(usr)
    exermean = exerciseMean(usr)
    exerMent = exerciseMent(usr)
    zValueSc = zValueScore(usr)
    goout = goOut(usr)
    gooutMean = goOutMean(usr)

    # 생활패턴

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

    return render_template('main.html', usr=usr, name=name,
                           num_res=num_res, len_res=len_res,
                           prob_res=sorted_prob_res, prob_res2=avg_prob_res, more_than_3_res_type=more_than_3_res_type,
                           avg_res=avg_res, avg_len=avg_len, avg_prob=avg_prob,
                           programs=sorted_program_days, len_programs=len_programs, program_days=program_days,
                           preference=preference,
                           total_programs=total_programs, avg_programs=avg_participation,
                           exer=exer, exermean=exermean, exerMent=exerMent, zValueSc=zValueSc, goout=goout,
                           gooutMean=gooutMean,
                           toilet=toilet, hobby=hobby, bm=bm, lm=lm, dm=dm, bs=bs, ls=ls, ds=ds,
                           rmm=rmm, rms=rms, stm=stm, sts=sts, atm=atm, ats=ats, avs=avs)