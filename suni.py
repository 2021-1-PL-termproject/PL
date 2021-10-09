import pandas as pd
import operator


def is_valid_user(user_id, user_profile):
    """
    This function checks whether the user is in the user_profile data.
    :input:
            user_id: (int) id of user
            user_profile: (pandas dataframe) user profile data from spreadsheet file
    :return:
            (bool)valid: True if given id is in the data

    +) 분석할 땐 필요 없는데 xlsx 파일 읽으려면 openpyxl 필요함.
    """
    num_users = len(user_profile["id"])
    valid = False
    for i in range(num_users):
        if user_profile["id"][i] == user_id:
            valid = True
    return valid


class Suni:
    def __init__(self, user_id, data):
        self.id = user_id
        # py 파일이 hs_g73_m08 폴더와 같은 위치에 있다고 가정함. 나중에 위치 맞춰서 바꿔야 함.
        # path = "hs_g73_m08/hs_" + str(user_id) + "_m08_0903_1355.csv"  # path for sensor data
        # self.data = pd.read_csv(path, encoding='CP949')
        self.data = data

    def num_response(self):
        """
        This function counts the number of response the AI gets from the user.
        :input:
                None
        :return:
                (int)num_response: the number of response
        """
        num_response = 0
        for i in range(len(self.data)):
            if not pd.isna(self.data["STT_1"][i]):
                num_response += 1
            if not pd.isna(self.data["STT_2"][i]):
                num_response += 1
            if not pd.isna(self.data["STT_3"][i]):
                num_response += 1
        return num_response

    def participated_program(self):
        """
                This function returns list of programs the user participated.
                The list includes tuples of (program_names, number of participation),
                in descending order.
                :requirement:
                        (library)operator
                :input:
                        None
                :return:
                        (list)sorted_program: list of programs(in descending order)
                """
        program = {}
        for i in range(len(self.data)):
            if self.data["Z"][i] == "프로그램":
                if self.data["State"][i] in program:
                    program[self.data["State"][i]] += 1
                else:
                    program[self.data["State"][i]] = 1
        sorted_program = sorted(program.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_program
