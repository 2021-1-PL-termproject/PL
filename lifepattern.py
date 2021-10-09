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
