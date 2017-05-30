import numpy as np

def hugWallOpenArea(Rover):
	angle = -5
	if Rover.sandAreaForwardR > 5250:
		angle = -15
	elif Rover.sandAreaForwardR > 5230:
		angle = -14.910714285714286
	elif Rover.sandAreaForwardR > 5210:
		angle = -14.821428571428571
	elif Rover.sandAreaForwardR > 5190:
		angle = -14.732142857142858
	elif Rover.sandAreaForwardR > 5170:
		angle = -14.642857142857142
	elif Rover.sandAreaForwardR > 5150:
		angle = -14.553571428571429
	elif Rover.sandAreaForwardR > 5130:
		angle = -14.464285714285714
	elif Rover.sandAreaForwardR > 5110:
		angle = -14.375
	elif Rover.sandAreaForwardR > 5090:
		angle = -14.285714285714286
	elif Rover.sandAreaForwardR > 5070:
		angle = -14.196428571428571
	elif Rover.sandAreaForwardR > 5050:
		angle = -14.107142857142858
	elif Rover.sandAreaForwardR > 5030:
		angle = -14.017857142857142
	elif Rover.sandAreaForwardR > 5010:
		angle = -13.928571428571429
	elif Rover.sandAreaForwardR > 4990:
		angle = -13.839285714285714
	elif Rover.sandAreaForwardR > 4970:
		angle = -13.75
	elif Rover.sandAreaForwardR > 4950:
		angle = -13.660714285714285
	elif Rover.sandAreaForwardR > 4930:
		angle = -13.571428571428571
	elif Rover.sandAreaForwardR > 4910:
		angle = -13.482142857142858
	elif Rover.sandAreaForwardR > 4890:
		angle = -13.392857142857142
	elif Rover.sandAreaForwardR > 4870:
		angle = -13.303571428571429
	elif Rover.sandAreaForwardR > 4850:
		angle = -13.214285714285714
	elif Rover.sandAreaForwardR > 4830:
		angle = -13.125
	elif Rover.sandAreaForwardR > 4810:
		angle = -13.035714285714285
	elif Rover.sandAreaForwardR > 4790:
		angle = -12.946428571428571
	elif Rover.sandAreaForwardR > 4770:
		angle = -12.857142857142858
	elif Rover.sandAreaForwardR > 4750:
		angle = -12.767857142857142
	elif Rover.sandAreaForwardR > 4730:
		angle = -12.678571428571429
	elif Rover.sandAreaForwardR > 4710:
		angle = -12.589285714285715
	elif Rover.sandAreaForwardR > 4690:
		angle = -12.5
	elif Rover.sandAreaForwardR > 4670:
		angle = -12.410714285714285
	elif Rover.sandAreaForwardR > 4650:
		angle = -12.321428571428571
	elif Rover.sandAreaForwardR > 4630:
		angle = -12.232142857142858
	elif Rover.sandAreaForwardR > 4610:
		angle = -12.142857142857142
	elif Rover.sandAreaForwardR > 4590:
		angle = -12.053571428571429
	elif Rover.sandAreaForwardR > 4570:
		angle = -11.964285714285715
	elif Rover.sandAreaForwardR > 4550:
		angle = -11.875
	elif Rover.sandAreaForwardR > 4530:
		angle = -11.785714285714285
	elif Rover.sandAreaForwardR > 4510:
		angle = -11.696428571428571
	elif Rover.sandAreaForwardR > 4490:
		angle = -11.607142857142858
	elif Rover.sandAreaForwardR > 4470:
		angle = -11.517857142857142
	elif Rover.sandAreaForwardR > 4450:
		angle = -11.428571428571429
	elif Rover.sandAreaForwardR > 4430:
		angle = -11.339285714285715
	elif Rover.sandAreaForwardR > 4410:
		angle = -11.25
	elif Rover.sandAreaForwardR > 4390:
		angle = -11.160714285714285
	elif Rover.sandAreaForwardR > 4370:
		angle = -11.071428571428571
	elif Rover.sandAreaForwardR > 4350:
		angle = -10.982142857142858
	elif Rover.sandAreaForwardR > 4330:
		angle = -10.892857142857142
	elif Rover.sandAreaForwardR > 4310:
		angle = -10.803571428571429
	elif Rover.sandAreaForwardR > 4290:
		angle = -10.714285714285715
	elif Rover.sandAreaForwardR > 4270:
		angle = -10.625
	elif Rover.sandAreaForwardR > 4250:
		angle = -10.535714285714285
	elif Rover.sandAreaForwardR > 4230:
		angle = -10.446428571428571
	elif Rover.sandAreaForwardR > 4210:
		angle = -10.357142857142858
	elif Rover.sandAreaForwardR > 4190:
		angle = -10.267857142857142
	elif Rover.sandAreaForwardR > 4170:
		angle = -10.178571428571429
	elif Rover.sandAreaForwardR > 4150:
		angle = -10.089285714285715
	elif Rover.sandAreaForwardR > 4130:
		angle = -10.0
	elif Rover.sandAreaForwardR > 4110:
		angle = -9.910714285714285
	elif Rover.sandAreaForwardR > 4090:
		angle = -9.821428571428571
	elif Rover.sandAreaForwardR > 4070:
		angle = -9.732142857142858
	elif Rover.sandAreaForwardR > 4050:
		angle = -9.642857142857142
	elif Rover.sandAreaForwardR > 4030:
		angle = -9.553571428571429
	elif Rover.sandAreaForwardR > 4010:
		angle = -9.464285714285715
	elif Rover.sandAreaForwardR > 3990:
		angle = -9.375
	elif Rover.sandAreaForwardR > 3970:
		angle = -9.285714285714285
	elif Rover.sandAreaForwardR > 3950:
		angle = -9.196428571428571
	elif Rover.sandAreaForwardR > 3930:
		angle = -9.107142857142858
	elif Rover.sandAreaForwardR > 3910:
		angle = -9.017857142857142
	elif Rover.sandAreaForwardR > 3890:
		angle = -8.928571428571429
	elif Rover.sandAreaForwardR > 3870:
		angle = -8.839285714285715
	elif Rover.sandAreaForwardR > 3850:
		angle = -8.75
	elif Rover.sandAreaForwardR > 3830:
		angle = -8.660714285714285
	elif Rover.sandAreaForwardR > 3810:
		angle = -8.571428571428571
	elif Rover.sandAreaForwardR > 3790:
		angle = -8.482142857142858
	elif Rover.sandAreaForwardR > 3770:
		angle = -8.392857142857142
	elif Rover.sandAreaForwardR > 3750:
		angle = -8.303571428571429
	elif Rover.sandAreaForwardR > 3730:
		angle = -8.214285714285715
	elif Rover.sandAreaForwardR > 3710:
		angle = -8.125
	elif Rover.sandAreaForwardR > 3690:
		angle = -8.035714285714285
	elif Rover.sandAreaForwardR > 3670:
		angle = -7.946428571428571
	elif Rover.sandAreaForwardR > 3650:
		angle = -7.857142857142857
	elif Rover.sandAreaForwardR > 3630:
		angle = -7.767857142857142
	elif Rover.sandAreaForwardR > 3610:
		angle = -7.678571428571429
	elif Rover.sandAreaForwardR > 3590:
		angle = -7.589285714285714
	elif Rover.sandAreaForwardR > 3570:
		angle = -7.5
	elif Rover.sandAreaForwardR > 3550:
		angle = -7.410714285714286
	elif Rover.sandAreaForwardR > 3530:
		angle = -7.321428571428571
	elif Rover.sandAreaForwardR > 3510:
		angle = -7.232142857142857
	elif Rover.sandAreaForwardR > 3490:
		angle = -7.142857142857142
	elif Rover.sandAreaForwardR > 3470:
		angle = -7.053571428571429
	elif Rover.sandAreaForwardR > 3450:
		angle = -6.9642857142857135
	elif Rover.sandAreaForwardR > 3430:
		angle = -6.875
	elif Rover.sandAreaForwardR > 3410:
		angle = -6.785714285714285
	elif Rover.sandAreaForwardR > 3390:
		angle = -6.696428571428571
	elif Rover.sandAreaForwardR > 3370:
		angle = -6.607142857142858
	elif Rover.sandAreaForwardR > 3350:
		angle = -6.517857142857142
	elif Rover.sandAreaForwardR > 3330:
		angle = -6.428571428571429
	elif Rover.sandAreaForwardR > 3310:
		angle = -6.3392857142857135
	elif Rover.sandAreaForwardR > 3290:
		angle = -6.25
	elif Rover.sandAreaForwardR > 3270:
		angle = -6.160714285714285
	elif Rover.sandAreaForwardR > 3250:
		angle = -6.071428571428571
	elif Rover.sandAreaForwardR > 3230:
		angle = -5.982142857142858
	elif Rover.sandAreaForwardR > 3210:
		angle = -5.892857142857142
	elif Rover.sandAreaForwardR > 3190:
		angle = -5.803571428571429
	elif Rover.sandAreaForwardR > 3170:
		angle = -5.7142857142857135
	elif Rover.sandAreaForwardR > 3150:
		angle = -5.625
	elif Rover.sandAreaForwardR > 3130:
		angle = -5.535714285714285
	elif Rover.sandAreaForwardR > 3110:
		angle = -5.446428571428571
	elif Rover.sandAreaForwardR > 3090:
		angle = -5.357142857142858
	elif Rover.sandAreaForwardR > 3070:
		angle = -5.267857142857142
	elif Rover.sandAreaForwardR > 3050:
		angle = -5.178571428571429
	elif Rover.sandAreaForwardR > 3030:
		angle = -5.0892857142857135
	elif Rover.sandAreaForwardR > 3000:
		angle = -5
	moveInDirectionOf(Rover, angle, Rover.max_vel)

def moveInDirectionOf(Rover, angle, max_vel):
    # If velocity is below max, then throttle
    if Rover.vel < max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    
    Rover.brake = 0
    Rover.steer = np.clip(angle, -15, 15)