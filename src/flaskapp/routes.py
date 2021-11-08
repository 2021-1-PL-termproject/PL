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
    try:
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

        if more_than_3_res_type:
            tmp = sorted_prob_res[0][1]
            prob1 = tmp
            tmp = sorted_prob_res[1][1]
            prob2 = tmp
            tmp = sorted_prob_res[2][1]
            prob3 = tmp
        else:
            prob1 = 0
            prob2 = 0
            prob3 = 0

        avg_res = avg_response(user_data)  # 전체 평균 응답 횟수
        avg_len = avg_response_length(user_data)  # 전체 평균 응답 길이
        avg_prob = avg_probability_to_response(user_data)  # 전체 평균 응답률

        std_res = std_response(user_data)   # 응답 횟수 표준편차
        conv_score = score(zvalue(num_res, avg_res, std_res))
        
        # 프로그램 참여
        program_times = participated_times(user_data[int(usr)])  # 프로그램 참여량
        program_days, sorted_program_days = participated_days(user_data[int(usr)])

        len_programs = len(program_times)
        total_programs = total_participation(user_data[int(usr)])
        if len_programs >= 3:
            preference = program_preference(user_data, sorted_program_days[0][0])
            tmp = program_days[sorted_program_days[0][0]]
            day1 = tmp
            tmp = program_days[sorted_program_days[1][0]]
            day2 = tmp
            tmp = program_days[sorted_program_days[2][0]]
            day3 = tmp
            day_others = 0
            if len_programs >= 4:
                for i in range(3, len_programs):
                    day_others += sorted_program_days[3][1]
                day_others = round(day_others / (len_programs - 3), 2)
        more_than_3_pref = True if len(program_preference) >= 3 else False

        avg_part = avg_participation(user_data)
        std_part = std_participation(user_data)
        program_score = score(zvalue(total_programs, avg_part, std_part))

        suni_score = int((conv_score + program_score) / 2)

        # 활동량
        exer = exercise(usr)
        exermean = exerciseMean(usr)
        exerMent = exerciseMent(usr)
        zValueSc = zValueScore(usr)
        goout = goOut(usr)
        zgraph = zValue(usr)
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

        sleep_point = 5
        awake_point = 5
        breakfast_point = 5
        lunch_point = 5
        dinner_point = 5
        if int(sts.split(':')[0]) < 3:
            sleep_point += (3 - int(sts.split(':')[0])) * 5
        if int(ats.split(':')[0]) < 3:
            awake_point += (3 - int(ats.split(':')[0])) * 5
        if int(bs.split(':')[0]) < 3:
            breakfast_point += (3 - int(bs.split(':')[0])) * 5
        if int(ls.split(':')[0]) < 3:
            lunch_point += (3 - int(ls.split(':')[0])) * 5
        if int(ds.split(':')[0]) < 3:
            dinner_point += (3 - int(ds.split(':')[0])) * 5          
        lifepattern_point = int(sleep_point) + int(awake_point) + int(breakfast_point) + int(lunch_point) + int(dinner_point)
        if int(avs.split(':')[0]) != 7 and int(avs.split(':')[0]) != 8:
            lifepattern_point = lifepattern_point - 10
        
        return render_template('main.html', usr=usr, name=name,
                            num_res=num_res, len_res=len_res,
                            sorted_prob_res=sorted_prob_res, avg_prob_res=avg_prob_res,
                            more_than_3_res_type=more_than_3_res_type,
                            avg_res=avg_res, avg_len=avg_len, avg_prob=avg_prob,
                            prob1=prob1, prob2=prob2, prob3=prob3,
                            programs=sorted_program_days, len_programs=len_programs, program_days=program_days,
                            day1=day1, day2=day2, day3=day3, day_others=day_others, preference=preference, more_than_3_pref=more_than_3_pref,
                            total_programs=total_programs, avg_part=avg_part,
                            suni_score=suni_score, conv_score=conv_score, program_score=program_score,
                            exer=exer, exermean=exermean, exerMent=exerMent, zValueSc=zValueSc, goout=goout,
                            gooutMean=gooutMean, zgraph =zgraph,
                            toilet=toilet, hobby=hobby, bm=bm, lm=lm, dm=dm, bs=bs, ls=ls, ds=ds,
                            rmm=rmm, rms=rms, stm=stm, sts=sts, atm=atm, ats=ats, avs=avs, lifepattern_point=lifepattern_point)
    except:
        return 'No data'
