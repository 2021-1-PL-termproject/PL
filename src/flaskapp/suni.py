import pandas as pd
import operator


# --- 데이터 관련 ---
def read_data(user_profile, path):
    """
    This function load user data to a dictionary.
    :param user_profile: (pandas dataframe) user profile data from spreadsheet file
    :param path: (str) path of folder that contains user data
    :return: (dict) dictionary that contains user data (key = user id)
    """
    user_data = {}
    for item in user_profile["id"]:
        if item < 30064:
            filename = "hs_"+str(item)+"_m08_0903_1355.csv"
        else:
            filename = "hs_"+str(item)+"_m08_0903_1356.csv"
        data = pd.read_csv(path+filename, encoding='CP949')
        user_data[item] = data
    return user_data


def trim_data(user_data, start_date, end_date):
    """
    This function slices user data to given time period(start_date ~ end_date)
    :param user_data: dictionary that contains user data (key = user id)
    :param start_date: (int) start date to cut
    :param end_date: (int) end date to cut
    :return: (pandas dataframe) trimmed data
    """
    trimmed_data = {}
    for user in user_data:
        # create empty dataframe to save slices
        trimmed = pd.DataFrame({})
        for date in range(start_date, end_date + 1):
            # make date to string format
            if date < 10:
                d = "2021-08-0" + str(date)
            else:
                d = "2021-08-" + str(date)
            # cut data
            cur_t = user_data[user].loc[user_data[user]
                                        ["Time"].str.contains(d)]
            # concatenate previous slices
            t = pd.concat([t, cur_t])
        # reset index
        trimmed = trimmed.reset_index(drop=True)
        trimmed_data[user] = trimmed
    return trimmed_data


# --- 순이 대화 관련 ---
# 응답 횟수
def num_response(data):
    """
    This function counts the number of response the AI gets from the user.
    :param data: (pandas dataframe) dataframe to analyze
    :return: (int) the number of response
    """
    num_res = 0
    for i in range(len(data)):
        if not pd.isna(data["STT_1"][i]):
            num_res += 1
        if not pd.isna(data["STT_2"][i]):
            num_res += 1
        if not pd.isna(data["STT_3"][i]):
            num_res += 1
    return num_res


def avg_response(user_data):
    """
    This function calculates average number of responses of whole users.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) the average number of responses of whole users
    """
    total_response = 0
    for user in user_data:
        total_response += num_response(user_data[user])
    return round((total_response / len(user_data.keys())), 2)


def std_response(user_data):
    """
    This function calculates standard deviation of user responses of whole users.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) the standard deviation of responses of whole users
    """
    var = 0
    avg = avg_response(user_data)
    for user in user_data:
        var += (num_response(user_data[user]) - avg)**2
    var /= len(user_data.keys())
    return round(var**(1/2), 2)


# 응답 길이
def len_response(data):
    """
    This function calculates average length of user responses
    (by counting word segments in each response).
    :param data: (pandas dataframe) dataframe to analyze
    :return: (float) the average number of word segments in user response
    """
    num_res = 0
    total_segments = 0
    for i in range(len(data)):
        if not pd.isna(data["STT_1"][i]):
            msg = data["STT_1"][i]
            total_segments += len(msg.split())
            num_res += 1
        if not pd.isna(data["STT_2"][i]):
            msg = data["STT_2"][i]
            total_segments += len(msg.split())
            num_res += 1
        if not pd.isna(data["STT_3"][i]):
            msg = data["STT_3"][i]
            total_segments += len(msg.split())
            num_res += 1

    avg = total_segments/num_res if num_res != 0 else 0
    return round(avg, 2)


def avg_response_length(user_data):
    """
    This function calculates average number of word segments in the responses of whole users.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) the average number of word segments in the response of whole users.
    """
    total_length = 0
    for user in user_data:
        total_length += len_response(user_data[user])
    return round((total_length / len(user_data.keys())), 2)


# 응답률
def probability_to_response_to_action(data, col="State"):
    """
    This function calculates probability of user response to each actions.
    :param data: (pandas dataframe) dataframe to analyze
    :param col: (str) column name ("Z"|"Act"|"State", Default: "State")
    :return: (list) list of programs probability of user response (in descending order)
    """
    num_action = {}
    response = {}
    for i in range(len(data)):
        # count the number of each action that the AI prints messages
        if (not pd.isna(data["Message_1"][i])) and (data["Z"][i] != "프로그램"):
            if data[col][i] in num_action:
                num_action[data[col][i]] += 1
            else:
                num_action[data[col][i]] = 1
            if data[col][i] not in response:
                response[data[col][i]] = 0
            if not pd.isna(data["Message_2"][i]):
                num_action[data[col][i]] += 1
            if not pd.isna(data["Message_3"][i]):
                num_action[data[col][i]] += 1

        # count the number of user response in each action
        if not pd.isna(data["STT_1"][i]):
            response[data[col][i]] += 1
        if not pd.isna(data["STT_2"][i]):
            response[data[col][i]] += 1
        if not pd.isna(data["STT_3"][i]):
            response[data[col][i]] += 1

    # add total response
    total_actions = 0
    total_response = 0
    for item in num_action:
        total_actions += num_action[item]
        total_response += response[item]
    num_action["전체"] = total_actions
    response["전체"] = total_response

    # calculate probability
    prob_response = {}
    for item in num_action:
        if num_action[item] >= 5:  # refine data
            prob_response[item] = round(response[item] / num_action[item], 2)
    sorted_prob = sorted(prob_response.items(),
                         key=operator.itemgetter(1), reverse=True)
    return prob_response, sorted_prob


def avg_probability_to_response(user_data):
    """
    This function calculates average probability of user responses to whole actions.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) the average probability of user responses to whole actions.
    """
    total_prob = 0
    for user in user_data:
        prob, _ = probability_to_response_to_action(user_data[user])
        if len(prob) > 0:
            total_prob += prob["전체"]
    return round((total_prob / len(user_data.keys())), 2)


# +) 메시지 유형 관련 분석 -> 리포트에는 표시 X
def probability_to_response_to_msg(data):
    """
    This function calculates probability of user response to each message type.
    :param data: (pandas dataframe) dataframe to analyze
    :return: (list) list of programs probability of user response (in descending order)
    """
    num_msg = {}
    response = {}
    for i in range(len(data)):
        # count the number of each action that the AI prints messages
        if (not pd.isna(data["Message_1"][i])) and (data["Z"][i] != "프로그램"):
            if data["Sequence"][i] in num_msg:
                num_msg[data["Sequence"][i]] += 1
            else:
                num_msg[data["Sequence"][i]] = 1
            if data["Sequence"][i] not in response:
                response[data["Sequence"][i]] = 0

        # count the number of user response in each action
        if not pd.isna(data["STT_1"][i]):
            response[data["Sequence"][i]] += 1
        if not pd.isna(data["STT_2"][i]):
            response[data["Sequence"][i]] += 1
        if not pd.isna(data["STT_3"][i]):
            response[data["Sequence"][i]] += 1

    # calculate probability
    prob_response = {}
    for item in num_msg:
        if num_msg[item] >= 5:   # refine data
            prob_response[item] = round(response[item] / num_msg[item], 2)
    sorted_prob = sorted(prob_response.items(),
                         key=operator.itemgetter(1), reverse=True)
    return sorted_prob


def len_response_for_msg(data):
    """
    This function calculates average length of user responses for each message type
    (by counting word segments in each response).
    :param data: (pandas dataframe) dataframe to analyze
    :return: (list) list of the average number of word segments in user response
                    for each message type (in descending order)
    """
    num_res = {}
    total_segments = {}
    for i in range(len(data)):
        if not pd.isna(data["STT_1"][i]):
            msg_type = data["Sequence"][i]
            if msg_type in num_res:
                num_res[msg_type] += 1
            else:
                num_res[msg_type] = 1
                total_segments[msg_type] = 0
            msg = data["STT_1"][i]
            total_segments[msg_type] += len(msg.split())

        if not pd.isna(data["STT_2"][i]):
            msg_type = data["Sequence"][i]
            num_res[msg_type] += 1
            msg = data["STT_2"][i]
            total_segments[msg_type] += len(msg.split())

        if not pd.isna(data["STT_3"][i]):
            msg_type = data["Sequence"][i]
            num_res[msg_type] += 1
            msg = data["STT_3"][i]
            total_segments[msg_type] += len(msg.split())

    avg = {}
    for item in num_res:
        if num_res[item] >= 5:     # refine data
            avg[item] = round(total_segments[item]/num_res[item], 2)
    sorted_avg = sorted(avg.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_avg


# --- 프로그램 관련 ---
def participated_times(data):
    """
    This function returns list of programs the user participated.
    The list includes tuples of (program_names, number of participation), in descending order.
    requirement: (library)operator
    :param data: (pandas dataframe) dataframe to analyze
    :return: (dict) the number of participation (key = program names)
    """
    program = {}
    for i in range(len(data)):
        if data["Z"][i] == "프로그램":
            if data["State"][i] in program:
                program[data["State"][i]] += 1
            else:
                program[data["State"][i]] = 1
    return program


def total_participation(data):
    """
    This function returns total program participation of the user
    :param data: (pandas dataframe) dataframe to analyze
    :return: (int) total number of program participation
    """
    num_participation = 0;
    for i in range(len(data)):
        if data["Z"][i] == "프로그램":
            num_participation += 1;
    return num_participation


def avg_participation(user_data):
    """
    This function returns average total program participation of whole user.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) average number of total participation
    """
    total = 0
    for user in user_data:
        total += total_participation(user_data[user])
    return round(total / len(user_data.keys()), 2)


def std_participation(user_data):
    """
    This function returns standard deviation of total program participation of whold user.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) standard deviation of total participation
    """
    var = 0
    avg = avg_participation(user_data)
    for user in user_data:
        var += (total_participation(user_data[user]) - avg) ** 2
    var /= len(user_data.keys())
    return round(var ** (1/2), 2)


def participated_days(data):
    """
    This function returns list of programs the user participated.
    The list includes tuples of (program_names, number of participated days), in descending order.
    :param data: (pandas dataframe) dataframe to analyze
    :return: (dict) the number of participated days (key = program names)
             (list) list of programs with the number of participated days (in descending order)
    """
    # count days
    program = {}
    for i in range(len(data)):
        if data["Z"][i] == "프로그램":
            date = data["Time"][i][1:11]
            if data["State"][i] in program:
                program[data["State"][i]].add(date)
            else:
                program[data["State"][i]] = {date}

    # change set of dates to number of participated days
    for item in program:
        program[item] = len(program[item])
    sorted_program = sorted(
        program.items(), key=operator.itemgetter(1), reverse=True)
    return program, sorted_program


def program_preference(user_data, program):
    """
    This function returns program preference of the user.
    :param user_data: dictionary that contains user data (key = user id)
    :param program: preffered program
    :return: (list) other preferred programs (in descending order)
    """
    preference = {}
    preference["user"] = 0
    for user in user_data:
        program_times = participated_times(user_data[user])
        program_days, sorted_program_days = participated_days(user_data[user])

        # counts total participation time
        total_participation = 0
        for program in program_times:
            total_participation += program_times[program]

        if (total_participation >= 5) and (len(program_times) >= 3):
            first = sorted_program_days[0][0]
            second = sorted_program_days[1][0]
            third = sorted_program_days[2][0]

            if program in [first, second, third]:
                # count user who prefers given program
                preference["user"] += 1
                for item in program_times:
                    if item == program:
                        pass
                    elif item not in preference:
                        preference[item] = program_times[item] / total_participation
                    else:
                        preference[item] += program_times[item] / total_participation

    # refine data
    if preference["user"] < 5:
        # if the users who prefer given program, ignore the result
        preference.clear()
    else:
        # delete user counts
        del preference["user"]
    return sorted(preference.items(), key=operator.itemgetter(1), reverse=True)


# --- 기타 ---
def extract_user_name(data):
    """
    This function extract user name from system message.
    :param data: (pandas dataframe) dataframe to analyze
    :return: (str) name of the user (Default: "Unknown")
    """
    msg = ""
    for i in range(len(data["Sequence"])):
        if not pd.isna(data["Sequence"][i]):
            if data["Sequence"][i][0] == "C":
                msg = data["Message_1"][i]
                break
    if msg == "":
        return "Unknown"    # Default name
    else:
        return msg.split("님")[0].split().pop()


def zvalue(x, mean, std):
    """
    This function calculates z-value of x
    :param x: target
    :param mean: mean of the data set
    :param std: standard deviation of the data set
    :return: (float) z-value of x
    """
    return round(((x - mean) / std), 2)


def score(z_score):
    """
    This function convert z-value to health score
    :param z_score: z-value of target
    :return: (int) health score of given z-value (maximum = 100)
    """
    return round(min(40 * z_score + 50, 100))
