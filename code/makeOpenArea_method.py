
areaLower = 3000
areaUpper = 5250
angleLower = -5
angleUpper = -15
stepSizeArea = 20


n = (areaUpper - areaLower) // stepSizeArea
stepSizeAngle = (angleUpper-angleLower) / n

angles_file = open('hugWallOpenArea_method.py', 'w')

angles_file.writelines("import numpy as np\n\n")
angles_file.writelines("def hugWallOpenArea(Rover):\n")
angles_file.writelines("\tangle = {}\n".format(angleLower))
angles_file.writelines("\tif Rover.sandAreaForwardR > {}:\n".format(areaUpper))
angles_file.writelines("\t\tangle = {}\n".format(angleUpper))

for i in range(1, n):
	area = areaUpper - i*stepSizeArea
	angle = angleUpper - i*stepSizeAngle
	angles_file.writelines("\telif Rover.sandAreaForwardR > {}:\n".format(area))
	angles_file.writelines("\t\tangle = {}\n".format(angle))

angles_file.writelines("\telif Rover.sandAreaForwardR > {}:\n".format(areaLower))
angles_file.writelines("\t\tangle = {}\n".format(angleLower))
angles_file.writelines("\tmoveInDirectionOf(Rover, angle, Rover.max_vel)\n\n")

function = '''def moveInDirectionOf(Rover, angle, max_vel):
    # If velocity is below max, then throttle
    if Rover.vel < max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    
    Rover.brake = 0
    Rover.steer = np.clip(angle, -15, 15)'''

angles_file.writelines(function)
angles_file.close()