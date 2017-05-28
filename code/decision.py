import numpy as np
import cv2


# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    
    correctForBadState(Rover)
    if Rover.nav_angles is not None and not Rover.picking_up:
        if not Rover.wasExtreme:
            # Check for Rover.mode status
            if Rover.mode == "move to ball":
                moveToBall(Rover)

            elif Rover.mode == 'pick_up':
                pickUpBall(Rover)

            #elif Rover.mode == 'forward': 
                #movingForward(Rover)
            #elif Rover.mode == 'stop':
            #    isStoped(Rover)

            elif Rover.mode == 'corner':
                inCorner(Rover)
            else:
                hugWall(Rover)

    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    printDebugInfo(Rover)
    return Rover

def inOpenAreaQuestion(Rover):
    return (Rover.sandArea > 12500 and Rover.sandAreaLeft > 500 and Rover.sandAreaRight > 500 and Rover.sandAreaForward > 500) \
            or (Rover.sandAreaLeft >= Rover.minOpenAreaLR and Rover.sandAreaRight >= Rover.minOpenAreaLR and Rover.sandAreaForward >= Rover.minOpenAreaF)

def inFullCornerQuestion(Rover):

    return Rover.sandAreaForward < Rover.minOpenAreaF \
            and Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.rockAreaRight >= Rover.minWallAreaLR \
            and Rover.rockAreaForward >= Rover.minWallAreaF \


def inLeftCornerQuestion(Rover):
    return Rover.rockAreaRight < Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.rockAreaForward >= Rover.minWallAreaF \
            and Rover.rockAreaRight < Rover.rockAreaForward 

def inRightCornerQuestion(Rover):
    return Rover.rockAreaLeft < Rover.rockAreaRight >= Rover.minWallAreaLR and Rover.rockAreaForward >= Rover.minWallAreaF



def inCorridorQuestion(Rover):
    return Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.rockAreaRight  < 3 * Rover.rockAreaLeft \
            and Rover.rockAreaLeft  < 3 * Rover.rockAreaRight \
            and Rover.sandAreaForward > Rover.rockAreaForward

def onLeftWallQuestion(Rover):
    return Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.rockAreaRight < Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.sandAreaRight >= Rover.minOpenAreaLR

def onRightWallQuestion(Rover):
    return Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.rockAreaLeft < Rover.rockAreaRight >= Rover.minWallAreaLR \
            and Rover.sandAreaLeft >= Rover.minOpenAreaLR

def onFrontWallQuestion(Rover):
    return Rover.rockAreaForward > Rover.minWallAreaF and Rover.sandAreaLeft >= Rover.minOpenAreaLR and Rover.sandAreaRight >= Rover.minOpenAreaLR

def needToTurnAroundQuestion(Rover):
    return Rover.rockArea > 15000 and Rover.sandAreaForward < 400

def seeBallQuestion(Rover):
    return len(Rover.ball_angles) > 0

def amPickingUpBall(Rover):
    return Rover.picking_up

def isRockAheadQuestion(Rover):
    return Rover.sandAreaUpper > 2000 and Rover.rockAreaLower > 2000

def hugWall(Rover):
    
    findOutMode(Rover)
    if Rover.mode == "Picking Up":
        hugWallPickUpBall(Rover)

    elif Rover.mode == "Full Corner":
        hugWallInCornerState(Rover)

    elif Rover.mode == "Left Corner":
        hugWallLeftCorner(Rover)

    elif Rover.mode == "Right Corner":
        hugWallRightCorner(Rover)

    elif Rover.mode == "Corridor":
        hugWallInCorridorState(Rover)

    elif Rover.mode == "Left Wall":
        hugWallOnLeft(Rover)

    elif Rover.mode == "Right Wall":
        hugWallOnRight(Rover)

    elif Rover.mode == "Open Area":
        hugWallOpenArea(Rover)
    
    elif Rover.mode == 'stop':
        hugWallStopState(Rover)
    
    elif Rover.mode == "Turn Around":
        hugWallBackup(Rover)
    
    elif Rover.mode == "Move To Ball 2":
         hugWallMoveToBall(Rover)

    elif Rover.mode == "Rock Ahead":
        hugWallAvoidRock(Rover)
    
    elif Rover.mode == "forward":
        hugWallMoveForward(Rover)

    else:
        printDebugInfo(Rover)
        Rover.mode = "stop"
        

def findOutMode(Rover):
    if amPickingUpBall(Rover):
        Rover.mode = "Picking Up"
    
    elif isRockAheadQuestion(Rover):
        Rover.mode = "Rock Ahead"

    elif seeBallQuestion(Rover):
        Rover.mode = "Move To Ball 2"

    elif needToTurnAroundQuestion(Rover):
        Rover.mode = "Turn Around"

    elif inOpenAreaQuestion(Rover):
        Rover.mode = "Open Area"

    elif inCorridorQuestion(Rover):
        Rover.mode = "Corridor"

    elif onLeftWallQuestion(Rover):
        Rover.mode = "Left Wall"

    elif onRightWallQuestion(Rover):
        Rover.mode = "Right Wall"

    elif inFullCornerQuestion(Rover):
        Rover.mode = 'Full Corner'
    
    elif inLeftCornerQuestion(Rover):
        Rover.mode = "Left Corner"

    elif inRightCornerQuestion(Rover):
        Rover.mode = "Right Corner"

    else:
        printDebugInfo(Rover)
        Rover.mode = 'stop'

def movingForward(Rover):
    # Check the extent of navigable terrain
    if Rover.sandArea >= Rover.minOpenArea: # len(Rover.nav_angles) >= Rover.stop_forward:  
        # If mode is forward, navigable terrain looks good 
        # and velocity is below max, then throttle 
        if Rover.vel < Rover.max_vel:
            # Set throttle value to throttle setting
            Rover.throttle = Rover.throttle_set
        else: # Else coast
            Rover.throttle = 0
        Rover.brake = 0
        # Set steering to average angle clipped to the range +/- 15
        Rover.steer = np.clip(np.mean(Rover.nav_angles)* 180/np.pi, -15, 15)
    # If there's a lack of navigable terrain pixels then go to 'stop' mode
    else:
    #if len(Rover.nav_angles) < Rover.stop_forward:
        # Set mode to "stop" and hit the brakes!
        Rover.throttle = 0
        # Set brake to stored brake value
        Rover.brake = Rover.brake_set
        Rover.steer = 0
        Rover.mode = 'Corner'
        Rover.inCorner = True
        Rover.angleInCorner = Rover.yaw

def hugWallAvoidRock(Rover):
    slowDown(Rover)
    roate(Rover, Rover.turnRight)

def hugWallPickUpBall(Rover):
    if not Rover.picking_up and not Rover.near_sample:
        Rover.seeTheBall = False
        Rover.mode = 'stop'
        Rover.picking_up = False
        Rover.throttle = 0
        Rover.brake = 0


def hugWallMoveToBall(Rover):
    if Rover.near_sample:
        Rover.near_sample_time = Rover.time
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.pick_up = True
        
        Rover.send_pickup = True
        Rover.mode = "Picking Up"


    elif len(Rover.ball_angles) > 0:
        #if there is a rock, move *slowly* directly towards it
        Rover.throttle = 0.575
        Rover.brake = 0
        Rover.steer = np.clip(np.mean(Rover.ball_angles) * 180/np.pi, -15, 15)
        
    Rover.ball_angles = [0]


def hugWallBackup(Rover):
    Rover.throttle = -1*Rover.throttle_set
    Rover.brake = 0
    steer = -15

    if Rover.sandAreaForward > 1500:
        Rover.state = "Right Wall"
        Rover.throttle = Rover.throttle_set

def hugWallOpenArea(Rover):
    angle = np.mean(Rover.nav_angles) * 180 / np.pi if len(Rover.nav_angles) > 0 else 0.1
    if Rover.sandAreaForwardR > 5250:
        angle = -12
    elif Rover.sandAreaForwardR > 5200:
        angle = -11.5
    elif Rover.sandAreaForwardR > 5150:
        angle = -11
    elif Rover.sandAreaForwardR > 5100:
        angle = -10.5
    elif Rover.sandAreaForwardR > 5050:
        angle = -10
    elif Rover.sandAreaForwardR > 5000:
        angle = -9.5
    elif Rover.sandAreaForwardR > 4950:
        angle = -9
    elif Rover.sandAreaForwardR > 4900:
        angle = -8.5
    elif Rover.sandAreaForwardR > 4850:
        angle = -8
    elif Rover.sandAreaForwardR > 4800:
        angle = -7.5
    elif Rover.sandAreaForwardR > 4750:
        angle = -7
    elif Rover.sandAreaForwardR > 4700:
        angle = -6.5
    elif Rover.sandAreaForwardR > 4650:
        angle = -6
    elif Rover.sandAreaForwardR > 4600:
        angle = -5.5
    elif Rover.sandAreaForwardR > 4550:
        angle = -5
    elif Rover.sandAreaForwardR > 4500:
        angle = -4.5
    elif Rover.sandAreaForwardR > 4450:
        angle = -4.0
    elif Rover.sandAreaForwardR > 4400:
        angle = -3.5
    elif Rover.sandAreaForwardR > 4350:
        angle = -3
    elif Rover.sandAreaForwardR > 4300:
        angle = -2.5
    elif Rover.sandAreaForwardR > 4250:
        angle = -2
    elif Rover.sandAreaForwardR > 4200:
        angle = -1.5
    elif Rover.sandAreaForwardR > 4150:
        angle = -1
    elif Rover.sandAreaForwardR > 4100:
        angle = -0.5
    elif Rover.sandAreaForwardR > 4050:
        angle = -0
    elif Rover.sandAreaForwardR > 4000:
        angle = 0.5
    elif Rover.sandAreaForwardR > 3950:
        angle = 1
    elif Rover.sandAreaForwardR > 3900:
        angle = 1.5
    elif Rover.sandAreaForwardR > 3850:
        angle = 2
    elif Rover.sandAreaForwardR > 3800:
        angle = 2.5


    elif Rover.sandAreaRight > 4000 and Rover.sandAreaForward > 9000:
        angle = Rover.turnRight
    elif Rover.sandAreaRight > 3000 and Rover.sandAreaForward > 7000:
        angle = -12
    elif Rover.sandAreaRight > 3000 and Rover.sandAreaForward > 6000:
        angle = -10
    moveInDirectionOf(Rover, angle, Rover.max_vel)
    
def hugWallRightCorner(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    else:
        Rover.brakes = 0
        if Rover.sandAreaForwardL < Rover.sandAreaForwardR:
            roate(Rover, Rover.turnLeft)
        elif 1000 >= Rover.sandAreaForwardR and Rover.sandAreaForwardL > Rover.minOpenAreaLR:
            Rover.mode = 'forward'
        elif Rover.sandAreaForwardR < 1000 and Rover.sandAreaForwardL < 1000:
            roate(Rover, Rover.turnLeft)
        else:
            roate(Rover, Rover.turnLeft)

def hugWallLeftCorner(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    else:
        Rover.brakes = 0
        if Rover.sandAreaForward < Rover.minOpenAreaF:
            roate(Rover, Rover.turnLeft)
        else:
            Rover.mode = 'forward'

def hugWallStopState(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    # If we're not moving (vel < 0.2) then do something else
    elif Rover.vel <= 0.2:
        if Rover.sandAreaForward < Rover.minOpenAreaF:
            roate(Rover, Rover.turnLeft)
        else:
            Rover.mode = 'forward'

def hugWallInCorridorState(Rover):
    angle = np.mean(Rover.nav_angles) * 180/np.pi
    moveInDirectionOf(Rover, np.clip(angle, -15, 15), Rover.max_vel)

def hugWallInCornerState(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    else:
        if 2*Rover.sandAreaForwardL >= Rover.minOpenAreaF:
            moveStraight(Rover)
        else:
            Rover.brake = 0
            roate(Rover, Rover.turnLeft)

def hugWallOnLeft(Rover):
    if 6*Rover.rockAreaForwardRight > Rover.rockAreaForward:
        angle = np.mean(Rover.nav_angles) * 180/np.pi
    else:
        angle = np.mean(Rover.nav_anglesF) * 180/np.pi    

    moveInDirectionOf(Rover, angle, Rover.max_vel)


def hugWallMoveForward(Rover):
    moveInDirectionOf(Rover, 0, Rover,max_vel / 2)
    Rover.throttle = Rover.throttle_set*0.75

def hugWallOnRight(Rover):
    
    if Rover.sandAreaForwardR < 100:
        angle = 13
    if 2.5*Rover.sandAreaForwardR > Rover.minOpenAreaF and len(Rover.nav_anglesF) > 100:
        angle = np.mean(Rover.nav_anglesF) * 180/np.pi
    elif len(Rover.nav_angles) > 100:
        angle = np.mean(Rover.nav_angles) * 180/np.pi 
    else:
        angle = 8
    moveInDirectionOf(Rover, angle, Rover.max_vel)

def isStoped(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    # If we're not moving (vel < 0.2) then do something else
    elif Rover.vel <= 0.2:
        if len(Rover.nav_angles) < Rover.go_forward:
            rotateLeft(Rover)

        # If we're stopped but see sufficient navigable terrain in front then go!
        if len(Rover.nav_angles) >= Rover.go_forward:
            # Set throttle back to stored value
            Rover.throttle = Rover.throttle_set
            # Release the brake
            Rover.brake = 0
            # Set steer to mean angle
            Rover.steer = np.clip(np.mean(Rover.nav_angles) * 180/np.pi, -15, 15)
            Rover.mode = 'forward'



def inCorner(Rover):
    if Rover.vel > 0.1:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.steer = 0

    else:
        Rover.throttle = 0
        # Release the brake to allow turning
        Rover.brake = 0
        # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
        Rover.steer = 15 

        theta = np.mean(Rover.nav_angles)
        phi = Rover.angleInCorner
        c = np.sqrt(0.5)
        error = np.abs(np.cos(theta) - c* (np.cos(phi) - np.sin(phi)))
        if Rover.sandArea >= Rover.maxRockArea:
            Rover.throttle = Rover.throttle_set
            Rover.inCorner = False
            Rover.brake = 0
            Rover.steer = np.clip(np.mean(Rover.nav_angles) * 180/np.pi, -15, 15)
            Rover.mode = 'forward'

def roate(Rover, angle):
    Rover.throttle = 0
    # Release the brake to allow turning
    # Turn range is +/- 15 degrees
    Rover.steer = np.clip(angle, -15, 15)

def rotateLeft(Rover, angle=15):
    roate(Rover, -angle)

def rotateRight(Rover, angle=15):
    roate(Rover, angle)

def moveInDirectionOf(Rover, angle, max_vel):
    # If velocity is below max, then throttle
    if Rover.vel < max_vel:
        Rover.throttle = Rover.throttle_set
    else: # Else coast
        Rover.throttle = 0
    
    Rover.brake = 0
    Rover.steer = np.clip(angle, -15, 15)

def moveStraight(Rover, max_vel=None):
    m = Rover.max_vel if max_vel is None else max_vel 
    moveInDirectionOf(Rover,0, m)

def slowDown(Rover):
    if Rover.vel > 0.2:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.steer = 0
    else:
        Rover.throttle = Rover.throttle_set
        Rover.brake = 0

def stopMoving(Rover):
    
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    #Rover.steer = 0


def distAngle(theta, phi):
    return (np.cos(theta) - np.cos(phi))** 2 + (np.sin(theta)-np.sin(theta))**2


def moveToBall(Rover):

    #rx = Rover.pos[0]
    #ry = Rover.pos[1]

    #bx = Rover.ball_location[0]
    #by = Rover.ball_location[1]

    #angle = np.arctan2(by-ry, bx-rx)
    #dist = distAngle(angle, Rover.yaw * np.pi / 180) 

    #print("angle: {}, Rover yaw: {}, dist: {}".format(angle, Rover.yaw* np.pi / 180, dist))
    #print("rover at x: {}, y: {}".format(rx, ry, bx, by))
    #print("ball at x: {}, y:{}".format(bx, by))

    #epsilon = 0.1

    #if dist > epsilon:
    #    stopMoving(Rover)

    #    if distAngle(angle, (Rover.yaw* np.pi / 180) + 0.1) <  distAngle(angle, Rover.yaw* np.pi / 180):
            
    #        rotateLeft(Rover, 3)
    #    else:
    #        rotateRight(Rover, 3)
    slowDown(Rover)
    if Rover.turnAngle is None:
        Rover.mode = 'stop'

    elif Rover.near_sample:
            
            Rover.send_pickup = True
            Rover.throttle = 0
            Rover.brake = Rover.brake_set
            Rover.mode = 'pick_up'

    elif abs(Rover.turnAngle) > 10:
        rotateRight(Rover, Rover.turnAngle)

    else:
        moveStraight(Rover,0.5)


def pickUpBall(Rover):
    
    if not Rover.picking_up and not Rover.near_sample:
        Rover.seeTheBall = False
        Rover.mode = 'stop'
        Rover.picking_up = False
        Rover.throttle = 0
        Rover.brake = 0

    Rover.mode = 'stop'

def correctForBadState(Rover):
    if Rover.picking_up and not Rover.near_sample:
        Rover.mode = "Turn Around"
        Rover.picking_up = False
        Rover.send_pickup = False



def printDebugInfo(Rover):
    print()
    print("-"*58)
    print("|    Mode    |    Position   | Near Sample |  Picking up |")
    print("-"*58)
    print("|{:^12}| ({:4.1f}, {:4.1f}) | {:^11} | {:^11} |".format(Rover.mode, Rover.pos[0], Rover.pos[1], Rover.near_sample, Rover.picking_up))
    print("-"*58)

    print()
    print("-"*37)
    print("| Steer | Throttle | Speed |  Break |")
    print("-"*37)
    print("| {:^5.2f} | {:^8.2f} | {:^5.2f} | {:^6} |".format(Rover.steer, Rover.throttle, Rover.vel, Rover.brake))
    print("-"*37)

    print()
    print("-"*48)
    print("| Type |  Total  |   Left  |  Right  | Forward |")
    print("-"*48)
    print("| Sand | {:>7.1F} | {:>7.1F} | {:>7.1F} | {:>7.1F} |".format(Rover.sandArea, Rover.sandAreaLeft, Rover.sandAreaRight, Rover.sandAreaForward))
    print("-"*48)
    print("| Rock | {:>7.1F} | {:>7.1F} | {:>7.1F} | {:>7.1F} |".format(Rover.rockArea, Rover.rockAreaLeft, Rover.rockAreaRight, Rover.rockAreaForward))
    print("-"*48)
    
    print()
    print("-"*52)
    print("| Type |  Upper  |  Lower  | L-Forward | R-Forward |")
    print("-"*52)
    print("| Sand | {:>7.1F} | {:>7.1F} | {:>9.1F} | {:>9.1F} |".format(Rover.sandAreaUpper, Rover.sandAreaLower, Rover.sandAreaForwardL, Rover.sandAreaForwardR))
    print("-"*52)
    print("| Rock | {:>7.1F} | {:>7.1F} | {:>9.1F} | {:>9.1F} |".format(Rover.rockAreaUpper, Rover.rockAreaLower, Rover.rockAreaForwardLeft, Rover.rockAreaForwardRight))
    print("-"*52)