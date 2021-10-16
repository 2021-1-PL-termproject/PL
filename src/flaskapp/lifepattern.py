import mean_std as ms


sleep_time_mean = ms.mean_time_of_state('수면')
sleep_time_std = ms.std_time_of_state('수면')
awake_time_mean = ms.mean_time_of_state('기상하기')
awake_time_std = ms.std_time_of_state('기상하기')

average_sleep_ang = ms.angle_dif(awake_time_mean, sleep_time_mean)
average_sleep = ms.angle_to_hms(average_sleep_ang)

print("취침시간 평균: " + sleep_time_mean)
print("취침시간 표준편차: " + sleep_time_std)
print("기상시간 평균: " + awake_time_mean)
print("기상시간 표준편차: " + awake_time_std)
print("평균 수면시간: " + average_sleep)


reg_med_mean = ms.mean_time_of_state('일반 약 복용')
reg_med_std = ms.std_time_of_state('일반 약 복용')

print('일반 약 복용시간 평균: ' + reg_med_mean)
print('일반 약 복용시간 표준편차: ' + reg_med_std)


toilet = ms.average_num_use('화장실 이용')
hobby = ms.average_num_use('취미활동')

print("하루 평균 화장실 이용 횟수: " + toilet)
print("하루 평균 취미생활 횟수: " + hobby)

breakfast_mean = ms.mean_time_of_state('조식')
breakfast_std = ms.std_time_of_state('조식')
lunch_mean = ms.mean_time_of_state('중식')
lunch_std = ms.std_time_of_state('중식')
dinner_mean = ms.mean_time_of_state('석식')
dinner_std = ms.std_time_of_state('석식')


print('아침식사 시간 평균: ' + breakfast_mean)
print('아침식사 시간 표준편차: ' + breakfast_std)
print('점심식사 시간 평균: ' + lunch_mean)
print('점심식사 시간 표준편차: ' + lunch_std)
print('저녁식사 시간 평균: ' + dinner_mean)
print('저녁식사 시간 표준편차: ' + dinner_std)
