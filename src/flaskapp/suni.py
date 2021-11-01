import pandas as pd
import operator


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


def is_valid_user(user_id, user_profile):
    """
    This function checks whether the user is in the user_profile data.
    :param user_id: (int) id of user
    :param user_profile: (pandas dataframe) user profile data from spreadsheet file
    :return: (bool) True if given id is in the data

    +) xlsx 파일 읽으려면 openpyxl 필요함.
    """
    num_users = len(user_profile["id"])
    valid = False
    for i in range(num_users):
        if user_profile["id"][i] == user_id:
            valid = True
    return valid


def slice_data(data, start_date, end_date):
    """
    This function slices user data by given time
    :param data: (pandas dataframe) whole user data
    :param start_date: (int) start date to cut
    :param end_date: (int) end date to cut
    :return: (pandas dataframe) trimmed data
    """
    # create empty dataframe to save slices
    trimmed = pd.DataFrame({})
    for date in range(start_date, end_date + 1):
        # make date to string format
        if date < 10:
            d = "2021-08-0" + str(date)
        else:
            d = "2021-08-" + str(date)
        # cut data
        cur_t = data.loc[data["Time"].str.contains(d)]
        # concatenate previous slices
        t = pd.concat([t, cur_t])
    # reset index
    trimmed = trimmed.reset_index(drop=True)
    return trimmed


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


def participated_program(data):
    """
    This function returns list of programs the user participated.
    The list includes tuples of (program_names, number of participation), in descending order.
    requirement: (library)operator
    :param data: (pandas dataframe) dataframe to analyze
    :return: (list) list of programs with the number of participation (in descending order)
    """
    program = {}
    for i in range(len(data)):
        if data["Z"][i] == "프로그램":
            if data["State"][i] in program:
                program[data["State"][i]] += 1
            else:
                program[data["State"][i]] = 1
    sorted_program = sorted(program.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_program


def participated_program2(data):
    """
    This function returns list of programs the user participated.
    The list includes tuples of (program_names, number of participated days), in descending order.
    requirement: (library)operator
    :param data: (pandas dataframe) dataframe to analyze
    :return: (list) list of programs with the number of participated days (in descending order)
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
    sorted_program = sorted(program.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_program


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
    sorted_prob = sorted(prob_response.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_prob


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

    # add total response
    total_msgs = 0
    total_response = 0
    for item in num_msg:
        total_msgs += num_msg[item]
        total_response += response[item]
    num_msg["전체"] = total_msgs
    response["전체"] = total_response

    # calculate probability
    prob_response = {}
    for item in num_msg:
        if num_msg[item] >= 5:   # refine data
            prob_response[item] = round(response[item] / num_msg[item], 2)
    sorted_prob = sorted(prob_response.items(), key=operator.itemgetter(1), reverse=True)
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


def avg_probability_to_response(user_data):
    """
    This function calculates average probability of user responses to whole actions.
    :param user_data: dictionary that contains user data (key = user id)
    :return: (float) the average probability of user responses to whole actions.
    """
    total_prob = 0
    for user in user_data:
        for (action, prob) in probability_to_response_to_action(user_data[user]):
            if action == "전체":
                total_prob += prob
    return round((total_prob / len(user_data.keys())), 2)


def std_response(user_data):
    """
        This function calculates standard deviation of probability of user responses to whole actions.
        :param user_data: dictionary that contains user data (key = user id)
        :return: (float) the standard deviation of probability of user responses to whole actions.
    """
    var_response = 0
    avg = avg_response(user_data)
    for user in user_data:
        var_response += (num_response(user_data[user]) - avg)**2
    return round(var_response**(1/2), 2)


def std_response_length(user_data):
    """
        This function calculates standard deviation of number of word segments in the responses of whole users.
        :param user_data: dictionary that contains user data (key = user id)
        :return: (float) the standard deviation of number of word segments in the response of whole users.
    """
    var_response_length = 0
    avg = avg_response_length(user_data)
    for user in user_data:
        var_response_length += (len_response(user_data[user]) - avg)**2
    return round(var_response_length**(1/2), 2)


def std_probability_to_response(user_data):
    """
        This function calculates standard deviation of probability of user responses to whole actions.
        :param user_data: dictionary that contains user data (key = user id)
        :return: (float) the standard deviation of probability of user responses to whole actions.
    """
    var_prob = 0
    avg = avg_probability_to_response(user_data)
    for user in user_data:
        for (action, prob) in probability_to_response_to_action(user_data[user]):
            if action == "전체":
                var_prob += (prob - avg)**2
    return round(var_prob**(1/2), 2)


def z_value(x, mean, std):
    """
    This function calculates Z-value of x
    :param x: target to calculates Z-value
    :param mean: mean of the data
    :param std: standard deviation of the data
    :return: (float) Z-value of x
    """
    return round(((x - mean) / std), 2)






