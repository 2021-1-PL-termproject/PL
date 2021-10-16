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


class Suni:
    def __init__(self, user_id, data):
        self.id = user_id
        self.data = data

    def num_response(self, sliced=None):
        """
        This function counts the number of response the AI gets from the user.
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :return: (int) the number of response
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

        num_response = 0
        for i in range(len(data)):
            if not pd.isna(data["STT_1"][i]):
                num_response += 1
            if not pd.isna(data["STT_2"][i]):
                num_response += 1
            if not pd.isna(data["STT_3"][i]):
                num_response += 1
        return num_response

    def participated_program(self, sliced=None):
        """
        This function returns list of programs the user participated.
        The list includes tuples of (program_names, number of participation), in descending order.
        requirement: (library)operator
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :return: (list) list of programs with the number of participation (in descending order)
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

        program = {}
        for i in range(len(data)):
            if data["Z"][i] == "프로그램":
                if data["State"][i] in program:
                    program[data["State"][i]] += 1
                else:
                    program[data["State"][i]] = 1
        sorted_program = sorted(program.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_program

    def participated_program2(self, sliced=None):
        """
        This function returns list of programs the user participated.
        The list includes tuples of (program_names, number of participated days), in descending order.
        requirement: (library)operator
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :return: (list) list of programs with the number of participated days (in descending order)
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

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

    def extract_user_name(self, sliced=None):
        """
        This function extract user name from system message.
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :return: (str) name of the user (Default: "Unknown")
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

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

    def probability_to_response_to_action(self, sliced=None, col="State"):
        """
        This function calculates probability of user response to each actions.
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :param col: (str) column name ("Z"|"Act"|"State", Default: "State")
        :return: (list) list of programs probability of user response (in descending order)
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

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

    def probability_to_response_to_msg(self, sliced=None):
        """
        This function calculates probability of user response to each message type.
        :param sliced: (pandas dataframe) sliced data (Default: None)
        :return: (list) list of programs probability of user response (in descending order)
        """
        if sliced is not None:
            data = sliced
        else:
            data = self.data

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







