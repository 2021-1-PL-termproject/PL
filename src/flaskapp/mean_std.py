from get_csv import time, state
from collections import Counter
from cmath import rect, phase
from math import sqrt, radians, degrees


def to_angle(time):
    angles = (int(time[0:2]) * 15) + (int(time[3:5]) * 0.25) + (int(time[6:]) / 240)
    return angles

def angle_to_hms(angle):
    if angle == 'No data':
        return 'No data'
    else:
        hours = int(round(angle // 15))
        left = angle % 15
        minutes = int(round(left // 0.25))
        seconds = int(round((left % 0.25) * 240))
        time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        return time

def angle_dif(a, b):
    if a == 'No data' or b == 'No data':
        return 'No data'
    else:
        if type(a) == str:
            a = to_angle(a)
            if type(b) == str:
                b = to_angle(b)
        angle_difference = a- b
        angle_difference = (angle_difference + 180) % 360 - 180
        return angle_difference

def std_of_angles(angles, mean):
    sum = 0
    for i in angles:
        dev = angle_dif(i, mean)
        dev_sqr = dev * dev
        sum += dev_sqr
    std = sqrt(sum / int(len(angles)))
    return std

def mean_angle(deg):
    return degrees(phase(sum(rect(1, radians(d)) for d in deg)/len(deg)))
 
def mean_time(times):
    if times:
        t = (time.split(':') for time in times)
        seconds = ((float(s) + int(m) * 60 + int(h) * 3600) 
                for h, m, s in t)
        day = 24 * 60 * 60
        to_angles = [s * 360. / day for s in seconds]
        mean_as_angle = mean_angle(to_angles)
        mean_seconds = mean_as_angle * day / 360.
        if mean_seconds < 0:
            mean_seconds += day
        h, m = divmod(mean_seconds, 3600)
        m, s = divmod(m, 60)
        return '%02i:%02i:%02i' % (h, m, s)
    else:
        return 'No data'

def time_val_of_state(State):
    time_data = time[state == State]
    len_time_data = len(time_data.index)
    time_list = []
    for i in range(len_time_data):
        time_d = time[state == State].str[12:].values[i]
        time_list.append(time_d)
    return time_list

def time_angle_list(State):
    time_ang_list = []
    time_list = time_val_of_state(State)
    for i in time_list:
        time_to_angle = to_angle(i)
        time_ang_list.append(time_to_angle)
    return time_ang_list

def mean_time_of_state(state):
    time_mean = mean_time(time_val_of_state(state))
    if time_mean == 'No data':
        return 'No data'
    else:
        return time_mean

def std_time_of_state(state):
    mtos = mean_time_of_state(state)
    if mtos == 'No data':
        return 'No data'
    else:
        time_mean_ang = to_angle(mtos)
        time_std_ang = std_of_angles(time_angle_list(state), time_mean_ang)
        time_std = angle_to_hms(time_std_ang)
        return time_std

def date_val_of_state(State):
    time_data = time[state == State]
    len_time_data = len(time_data.index)
    date_list = []
    for i in range(len_time_data):
        date_val = time[state == State].str[9:11].values[i]
        date_list.append(date_val)
    return date_list

def average_num_use(State):
    c = Counter(date_val_of_state(State))
    c_sum = 0
    for i in range(1, 32):
        c_sum += int(c[str(i).zfill(2)])
    c_ave = round(c_sum / 31, 2)
    if c_sum == 0:
        return 'No data'
    else:
        return str(c_ave)
