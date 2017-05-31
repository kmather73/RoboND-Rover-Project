import numpy as np

def hugWallOnRight(Rover):
	angle = 8
	if Rover.sandAreaForwardR > 3000:
		angle = -5
	elif Rover.sandAreaForwardR > 2980:
		angle = -4.888888888888889
	elif Rover.sandAreaForwardR > 2960:
		angle = -4.777777777777778
	elif Rover.sandAreaForwardR > 2940:
		angle = -4.666666666666667
	elif Rover.sandAreaForwardR > 2920:
		angle = -4.555555555555555
	elif Rover.sandAreaForwardR > 2900:
		angle = -4.444444444444445
	elif Rover.sandAreaForwardR > 2880:
		angle = -4.333333333333333
	elif Rover.sandAreaForwardR > 2860:
		angle = -4.222222222222222
	elif Rover.sandAreaForwardR > 2840:
		angle = -4.111111111111111
	elif Rover.sandAreaForwardR > 2820:
		angle = -4.0
	elif Rover.sandAreaForwardR > 2800:
		angle = -3.888888888888889
	elif Rover.sandAreaForwardR > 2780:
		angle = -3.7777777777777777
	elif Rover.sandAreaForwardR > 2760:
		angle = -3.666666666666667
	elif Rover.sandAreaForwardR > 2740:
		angle = -3.5555555555555554
	elif Rover.sandAreaForwardR > 2720:
		angle = -3.4444444444444446
	elif Rover.sandAreaForwardR > 2700:
		angle = -3.3333333333333335
	elif Rover.sandAreaForwardR > 2680:
		angle = -3.2222222222222223
	elif Rover.sandAreaForwardR > 2660:
		angle = -3.111111111111111
	elif Rover.sandAreaForwardR > 2640:
		angle = -3.0
	elif Rover.sandAreaForwardR > 2620:
		angle = -2.888888888888889
	elif Rover.sandAreaForwardR > 2600:
		angle = -2.7777777777777777
	elif Rover.sandAreaForwardR > 2580:
		angle = -2.666666666666667
	elif Rover.sandAreaForwardR > 2560:
		angle = -2.555555555555556
	elif Rover.sandAreaForwardR > 2540:
		angle = -2.4444444444444446
	elif Rover.sandAreaForwardR > 2520:
		angle = -2.3333333333333335
	elif Rover.sandAreaForwardR > 2500:
		angle = -2.2222222222222223
	elif Rover.sandAreaForwardR > 2480:
		angle = -2.111111111111111
	elif Rover.sandAreaForwardR > 2460:
		angle = -2.0
	elif Rover.sandAreaForwardR > 2440:
		angle = -1.8888888888888893
	elif Rover.sandAreaForwardR > 2420:
		angle = -1.7777777777777781
	elif Rover.sandAreaForwardR > 2400:
		angle = -1.666666666666667
	elif Rover.sandAreaForwardR > 2380:
		angle = -1.5555555555555558
	elif Rover.sandAreaForwardR > 2360:
		angle = -1.4444444444444446
	elif Rover.sandAreaForwardR > 2340:
		angle = -1.3333333333333335
	elif Rover.sandAreaForwardR > 2320:
		angle = -1.2222222222222223
	elif Rover.sandAreaForwardR > 2300:
		angle = -1.1111111111111112
	elif Rover.sandAreaForwardR > 2280:
		angle = -1.0
	elif Rover.sandAreaForwardR > 2260:
		angle = -0.8888888888888893
	elif Rover.sandAreaForwardR > 2240:
		angle = -0.7777777777777777
	elif Rover.sandAreaForwardR > 2220:
		angle = -0.666666666666667
	elif Rover.sandAreaForwardR > 2200:
		angle = -0.5555555555555554
	elif Rover.sandAreaForwardR > 2180:
		angle = -0.44444444444444464
	elif Rover.sandAreaForwardR > 2160:
		angle = -0.3333333333333339
	elif Rover.sandAreaForwardR > 2140:
		angle = -0.22222222222222232
	elif Rover.sandAreaForwardR > 2120:
		angle = -0.1111111111111116
	elif Rover.sandAreaForwardR > 2100:
		angle = 0.0
	elif Rover.sandAreaForwardR > 2080:
		angle = 0.11111111111111072
	elif Rover.sandAreaForwardR > 2060:
		angle = 0.22222222222222232
	elif Rover.sandAreaForwardR > 2040:
		angle = 0.33333333333333304
	elif Rover.sandAreaForwardR > 2020:
		angle = 0.44444444444444375
	elif Rover.sandAreaForwardR > 2000:
		angle = 0.5555555555555554
	elif Rover.sandAreaForwardR > 1980:
		angle = 0.6666666666666661
	elif Rover.sandAreaForwardR > 1960:
		angle = 0.7777777777777777
	elif Rover.sandAreaForwardR > 1940:
		angle = 0.8888888888888884
	elif Rover.sandAreaForwardR > 1920:
		angle = 1.0
	elif Rover.sandAreaForwardR > 1900:
		angle = 1.1111111111111107
	elif Rover.sandAreaForwardR > 1880:
		angle = 1.2222222222222214
	elif Rover.sandAreaForwardR > 1860:
		angle = 1.333333333333333
	elif Rover.sandAreaForwardR > 1840:
		angle = 1.4444444444444438
	elif Rover.sandAreaForwardR > 1820:
		angle = 1.5555555555555554
	elif Rover.sandAreaForwardR > 1800:
		angle = 1.666666666666666
	elif Rover.sandAreaForwardR > 1780:
		angle = 1.7777777777777777
	elif Rover.sandAreaForwardR > 1760:
		angle = 1.8888888888888884
	elif Rover.sandAreaForwardR > 1740:
		angle = 2.0
	elif Rover.sandAreaForwardR > 1720:
		angle = 2.1111111111111107
	elif Rover.sandAreaForwardR > 1700:
		angle = 2.2222222222222214
	elif Rover.sandAreaForwardR > 1680:
		angle = 2.333333333333333
	elif Rover.sandAreaForwardR > 1660:
		angle = 2.4444444444444438
	elif Rover.sandAreaForwardR > 1640:
		angle = 2.5555555555555554
	elif Rover.sandAreaForwardR > 1620:
		angle = 2.666666666666666
	elif Rover.sandAreaForwardR > 1600:
		angle = 2.7777777777777777
	elif Rover.sandAreaForwardR > 1580:
		angle = 2.8888888888888884
	elif Rover.sandAreaForwardR > 1560:
		angle = 3.0
	elif Rover.sandAreaForwardR > 1540:
		angle = 3.1111111111111107
	elif Rover.sandAreaForwardR > 1520:
		angle = 3.2222222222222214
	elif Rover.sandAreaForwardR > 1500:
		angle = 3.333333333333332
	elif Rover.sandAreaForwardR > 1480:
		angle = 3.4444444444444446
	elif Rover.sandAreaForwardR > 1460:
		angle = 3.5555555555555554
	elif Rover.sandAreaForwardR > 1440:
		angle = 3.666666666666666
	elif Rover.sandAreaForwardR > 1420:
		angle = 3.777777777777777
	elif Rover.sandAreaForwardR > 1400:
		angle = 3.8888888888888893
	elif Rover.sandAreaForwardR > 1380:
		angle = 4.0
	elif Rover.sandAreaForwardR > 1360:
		angle = 4.111111111111111
	elif Rover.sandAreaForwardR > 1340:
		angle = 4.222222222222221
	elif Rover.sandAreaForwardR > 1320:
		angle = 4.333333333333332
	elif Rover.sandAreaForwardR > 1300:
		angle = 4.444444444444445
	elif Rover.sandAreaForwardR > 1280:
		angle = 4.555555555555555
	elif Rover.sandAreaForwardR > 1260:
		angle = 4.666666666666666
	elif Rover.sandAreaForwardR > 1240:
		angle = 4.777777777777777
	elif Rover.sandAreaForwardR > 1220:
		angle = 4.8888888888888875
	elif Rover.sandAreaForwardR > 1200:
		angle = 5.0
	elif Rover.sandAreaForwardR > 1180:
		angle = 5.111111111111111
	elif Rover.sandAreaForwardR > 1160:
		angle = 5.222222222222221
	elif Rover.sandAreaForwardR > 1140:
		angle = 5.333333333333332
	elif Rover.sandAreaForwardR > 1120:
		angle = 5.444444444444445
	elif Rover.sandAreaForwardR > 1100:
		angle = 5.555555555555555
	elif Rover.sandAreaForwardR > 1080:
		angle = 5.666666666666666
	elif Rover.sandAreaForwardR > 1060:
		angle = 5.777777777777777
	elif Rover.sandAreaForwardR > 1040:
		angle = 5.8888888888888875
	elif Rover.sandAreaForwardR > 1020:
		angle = 6.0
	elif Rover.sandAreaForwardR > 1000:
		angle = 6.111111111111111
	elif Rover.sandAreaForwardR > 980:
		angle = 6.222222222222221
	elif Rover.sandAreaForwardR > 960:
		angle = 6.333333333333332
	elif Rover.sandAreaForwardR > 940:
		angle = 6.444444444444445
	elif Rover.sandAreaForwardR > 920:
		angle = 6.555555555555555
	elif Rover.sandAreaForwardR > 900:
		angle = 6.666666666666666
	elif Rover.sandAreaForwardR > 880:
		angle = 6.777777777777777
	elif Rover.sandAreaForwardR > 860:
		angle = 6.8888888888888875
	elif Rover.sandAreaForwardR > 840:
		angle = 7.0
	elif Rover.sandAreaForwardR > 820:
		angle = 7.111111111111111
	elif Rover.sandAreaForwardR > 800:
		angle = 7.222222222222221
	elif Rover.sandAreaForwardR > 780:
		angle = 7.333333333333332
	elif Rover.sandAreaForwardR > 760:
		angle = 7.444444444444443
	elif Rover.sandAreaForwardR > 740:
		angle = 7.555555555555555
	elif Rover.sandAreaForwardR > 720:
		angle = 7.666666666666666
	elif Rover.sandAreaForwardR > 700:
		angle = 7.777777777777777
	elif Rover.sandAreaForwardR > 680:
		angle = 7.8888888888888875
	elif Rover.sandAreaForwardR > 650:
		angle = 8
	moveInDirectionOf(Rover, angle, Rover.max_vel)

def moveInDirectionOf(Rover, angle, max_vel):
    # If velocity is below max, then throttle
    if Rover.vel < max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    
    Rover.brake = 0
    Rover.steer = np.clip(angle, -15, 15)