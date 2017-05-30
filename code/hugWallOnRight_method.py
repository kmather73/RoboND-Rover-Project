import numpy as np

def hugWallOnRight(Rover):
	angle = 8.2
	if Rover.sandAreaForwardR > 3000:
		angle = -5
	elif Rover.sandAreaForwardR > 2980:
		angle = -4.887179487179488
	elif Rover.sandAreaForwardR > 2960:
		angle = -4.774358974358974
	elif Rover.sandAreaForwardR > 2940:
		angle = -4.661538461538462
	elif Rover.sandAreaForwardR > 2920:
		angle = -4.5487179487179485
	elif Rover.sandAreaForwardR > 2900:
		angle = -4.435897435897436
	elif Rover.sandAreaForwardR > 2880:
		angle = -4.323076923076923
	elif Rover.sandAreaForwardR > 2860:
		angle = -4.21025641025641
	elif Rover.sandAreaForwardR > 2840:
		angle = -4.097435897435897
	elif Rover.sandAreaForwardR > 2820:
		angle = -3.9846153846153847
	elif Rover.sandAreaForwardR > 2800:
		angle = -3.871794871794872
	elif Rover.sandAreaForwardR > 2780:
		angle = -3.758974358974359
	elif Rover.sandAreaForwardR > 2760:
		angle = -3.6461538461538465
	elif Rover.sandAreaForwardR > 2740:
		angle = -3.533333333333333
	elif Rover.sandAreaForwardR > 2720:
		angle = -3.420512820512821
	elif Rover.sandAreaForwardR > 2700:
		angle = -3.307692307692308
	elif Rover.sandAreaForwardR > 2680:
		angle = -3.194871794871795
	elif Rover.sandAreaForwardR > 2660:
		angle = -3.082051282051282
	elif Rover.sandAreaForwardR > 2640:
		angle = -2.9692307692307693
	elif Rover.sandAreaForwardR > 2620:
		angle = -2.8564102564102565
	elif Rover.sandAreaForwardR > 2600:
		angle = -2.7435897435897436
	elif Rover.sandAreaForwardR > 2580:
		angle = -2.630769230769231
	elif Rover.sandAreaForwardR > 2560:
		angle = -2.5179487179487183
	elif Rover.sandAreaForwardR > 2540:
		angle = -2.4051282051282055
	elif Rover.sandAreaForwardR > 2520:
		angle = -2.2923076923076926
	elif Rover.sandAreaForwardR > 2500:
		angle = -2.1794871794871797
	elif Rover.sandAreaForwardR > 2480:
		angle = -2.066666666666667
	elif Rover.sandAreaForwardR > 2460:
		angle = -1.953846153846154
	elif Rover.sandAreaForwardR > 2440:
		angle = -1.8410256410256416
	elif Rover.sandAreaForwardR > 2420:
		angle = -1.7282051282051287
	elif Rover.sandAreaForwardR > 2400:
		angle = -1.6153846153846159
	elif Rover.sandAreaForwardR > 2380:
		angle = -1.502564102564103
	elif Rover.sandAreaForwardR > 2360:
		angle = -1.3897435897435901
	elif Rover.sandAreaForwardR > 2340:
		angle = -1.2769230769230773
	elif Rover.sandAreaForwardR > 2320:
		angle = -1.1641025641025644
	elif Rover.sandAreaForwardR > 2300:
		angle = -1.0512820512820515
	elif Rover.sandAreaForwardR > 2280:
		angle = -0.9384615384615387
	elif Rover.sandAreaForwardR > 2260:
		angle = -0.8256410256410263
	elif Rover.sandAreaForwardR > 2240:
		angle = -0.712820512820513
	elif Rover.sandAreaForwardR > 2220:
		angle = -0.6000000000000005
	elif Rover.sandAreaForwardR > 2200:
		angle = -0.4871794871794872
	elif Rover.sandAreaForwardR > 2180:
		angle = -0.3743589743589748
	elif Rover.sandAreaForwardR > 2160:
		angle = -0.2615384615384624
	elif Rover.sandAreaForwardR > 2140:
		angle = -0.14871794871794908
	elif Rover.sandAreaForwardR > 2120:
		angle = -0.03589743589743666
	elif Rover.sandAreaForwardR > 2100:
		angle = 0.07692307692307665
	elif Rover.sandAreaForwardR > 2080:
		angle = 0.18974358974358907
	elif Rover.sandAreaForwardR > 2060:
		angle = 0.3025641025641024
	elif Rover.sandAreaForwardR > 2040:
		angle = 0.4153846153846148
	elif Rover.sandAreaForwardR > 2020:
		angle = 0.5282051282051272
	elif Rover.sandAreaForwardR > 2000:
		angle = 0.6410256410256405
	elif Rover.sandAreaForwardR > 1980:
		angle = 0.7538461538461529
	elif Rover.sandAreaForwardR > 1960:
		angle = 0.8666666666666663
	elif Rover.sandAreaForwardR > 1940:
		angle = 0.9794871794871787
	elif Rover.sandAreaForwardR > 1920:
		angle = 1.092307692307692
	elif Rover.sandAreaForwardR > 1900:
		angle = 1.2051282051282044
	elif Rover.sandAreaForwardR > 1880:
		angle = 1.3179487179487168
	elif Rover.sandAreaForwardR > 1860:
		angle = 1.4307692307692301
	elif Rover.sandAreaForwardR > 1840:
		angle = 1.5435897435897425
	elif Rover.sandAreaForwardR > 1820:
		angle = 1.6564102564102559
	elif Rover.sandAreaForwardR > 1800:
		angle = 1.7692307692307683
	elif Rover.sandAreaForwardR > 1780:
		angle = 1.8820512820512816
	elif Rover.sandAreaForwardR > 1760:
		angle = 1.994871794871794
	elif Rover.sandAreaForwardR > 1740:
		angle = 2.1076923076923073
	elif Rover.sandAreaForwardR > 1720:
		angle = 2.2205128205128197
	elif Rover.sandAreaForwardR > 1700:
		angle = 2.333333333333332
	elif Rover.sandAreaForwardR > 1680:
		angle = 2.4461538461538455
	elif Rover.sandAreaForwardR > 1660:
		angle = 2.558974358974358
	elif Rover.sandAreaForwardR > 1640:
		angle = 2.671794871794871
	elif Rover.sandAreaForwardR > 1620:
		angle = 2.7846153846153836
	elif Rover.sandAreaForwardR > 1600:
		angle = 2.897435897435897
	elif Rover.sandAreaForwardR > 1580:
		angle = 3.01025641025641
	elif Rover.sandAreaForwardR > 1560:
		angle = 3.1230769230769226
	elif Rover.sandAreaForwardR > 1540:
		angle = 3.235897435897435
	elif Rover.sandAreaForwardR > 1520:
		angle = 3.3487179487179475
	elif Rover.sandAreaForwardR > 1500:
		angle = 3.46153846153846
	elif Rover.sandAreaForwardR > 1480:
		angle = 3.574358974358974
	elif Rover.sandAreaForwardR > 1460:
		angle = 3.6871794871794865
	elif Rover.sandAreaForwardR > 1440:
		angle = 3.799999999999999
	elif Rover.sandAreaForwardR > 1420:
		angle = 3.9128205128205114
	elif Rover.sandAreaForwardR > 1400:
		angle = 4.0256410256410255
	elif Rover.sandAreaForwardR > 1380:
		angle = 4.138461538461538
	elif Rover.sandAreaForwardR > 1360:
		angle = 4.25128205128205
	elif Rover.sandAreaForwardR > 1340:
		angle = 4.364102564102563
	elif Rover.sandAreaForwardR > 1320:
		angle = 4.476923076923075
	elif Rover.sandAreaForwardR > 1300:
		angle = 4.589743589743589
	elif Rover.sandAreaForwardR > 1280:
		angle = 4.702564102564102
	elif Rover.sandAreaForwardR > 1260:
		angle = 4.815384615384614
	elif Rover.sandAreaForwardR > 1240:
		angle = 4.928205128205127
	elif Rover.sandAreaForwardR > 1220:
		angle = 5.041025641025639
	elif Rover.sandAreaForwardR > 1200:
		angle = 5.153846153846153
	elif Rover.sandAreaForwardR > 1180:
		angle = 5.266666666666666
	elif Rover.sandAreaForwardR > 1160:
		angle = 5.379487179487178
	elif Rover.sandAreaForwardR > 1140:
		angle = 5.492307692307691
	elif Rover.sandAreaForwardR > 1120:
		angle = 5.605128205128205
	elif Rover.sandAreaForwardR > 1100:
		angle = 5.717948717948717
	elif Rover.sandAreaForwardR > 1080:
		angle = 5.83076923076923
	elif Rover.sandAreaForwardR > 1060:
		angle = 5.943589743589742
	elif Rover.sandAreaForwardR > 1040:
		angle = 6.056410256410254
	elif Rover.sandAreaForwardR > 1020:
		angle = 6.169230769230769
	elif Rover.sandAreaForwardR > 1000:
		angle = 6.282051282051281
	elif Rover.sandAreaForwardR > 980:
		angle = 6.3948717948717935
	elif Rover.sandAreaForwardR > 960:
		angle = 6.507692307692306
	elif Rover.sandAreaForwardR > 940:
		angle = 6.62051282051282
	elif Rover.sandAreaForwardR > 920:
		angle = 6.7333333333333325
	elif Rover.sandAreaForwardR > 900:
		angle = 6.846153846153845
	elif Rover.sandAreaForwardR > 880:
		angle = 6.958974358974357
	elif Rover.sandAreaForwardR > 860:
		angle = 7.07179487179487
	elif Rover.sandAreaForwardR > 840:
		angle = 7.184615384615384
	elif Rover.sandAreaForwardR > 820:
		angle = 7.297435897435896
	elif Rover.sandAreaForwardR > 800:
		angle = 7.410256410256409
	elif Rover.sandAreaForwardR > 780:
		angle = 7.523076923076921
	elif Rover.sandAreaForwardR > 760:
		angle = 7.635897435897434
	elif Rover.sandAreaForwardR > 740:
		angle = 7.748717948717948
	elif Rover.sandAreaForwardR > 720:
		angle = 7.86153846153846
	elif Rover.sandAreaForwardR > 700:
		angle = 7.974358974358973
	elif Rover.sandAreaForwardR > 680:
		angle = 8.087179487179485
	elif Rover.sandAreaForwardR > 650:
		angle = 8.2
	moveInDirectionOf(Rover, angle, Rover.max_vel)

def moveInDirectionOf(Rover, angle, max_vel):
    # If velocity is below max, then throttle
    if Rover.vel < max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    
    Rover.brake = 0
    Rover.steer = np.clip(angle, -15, 15)