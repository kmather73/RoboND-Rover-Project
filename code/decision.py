import numpy as np
import cv2
from hugWallOnRight_method import *
from hugWallOpenArea_method import *

# This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function
def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check if we have vision data to make decisions with
    
    correctForBadState(Rover)
    if Rover.nav_angles is not None and not Rover.picking_up and Rover.mode != "Completed Challenge":
        if True or not Rover.wasExtreme:
            # Check for Rover.mode status
            hugWall(Rover)
        else:
            print("### EXTREME ANGLE")
    
    elif Rover.mode == "Completed Challenge":
        #printDebugInfo(Rover)
        print("******** Challenge Completed, NASA Take Me Home!!!  ********")

    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        print('''%%%%%% no nav angles''')
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    
    return Rover

def inOpenAreaQuestion(Rover):
    return Rover.rockAreaForwardLeft < 1900 \
            and Rover.rockAreaForwardRight < 1900 \
            and Rover.rockAreaUpper < 1500 \
            and Rover.rockAreaLower < 1000 \
            and Rover.sandAreaRight > 500

def inFullCornerQuestion(Rover):
    return Rover.sandArea < 1900 \
            and Rover.sandAreaForward < Rover.minOpenAreaF \
            and Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.rockAreaRight >= Rover.minWallAreaLR \
            and Rover.rockAreaForward >= Rover.minWallAreaF \


def inLeftCornerQuestion(Rover):
    return Rover.rockAreaRight < Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.rockAreaForward >= Rover.minWallAreaF \
            and Rover.rockAreaRight < Rover.rockAreaForward 

def inRightCornerQuestion(Rover):
    return Rover.rockAreaLeft < Rover.rockAreaRight >= Rover.minWallAreaLR \
    and Rover.rockAreaForward >= Rover.minWallAreaF \
    and Rover.sandAreaForward < Rover.minOpenAreaF



def inCorridorQuestion(Rover):
    return (Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.rockAreaLeft  < 1.25 * Rover.rockAreaRight \
            and Rover.rockAreaRight  < 1.25 * Rover.rockAreaLeft \
            and Rover.sandAreaLower > Rover.rockAreaLower \
            and 1.5*Rover.rockArea > Rover.sandArea ) \
            or ( 12000 > Rover.sandArea > 7000 and Rover.rockAreaForward < 3000)


def onLeftWallQuestion(Rover):
    return Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.rockAreaRight < Rover.rockAreaLeft >= Rover.minWallAreaLR \
            and Rover.sandAreaRight >= Rover.minOpenAreaLR

def onRightWallQuestion(Rover):
    return Rover.sandAreaForward >= Rover.minOpenAreaF \
            and Rover.sandAreaLeft >= Rover.minOpenAreaLR \
            and Rover.rockAreaForwardLeft < 3000 \
            and Rover.rockAreaRight >= Rover.minWallAreaLR \
            and Rover.rockAreaLower < 2500
            

def onFrontWallQuestion(Rover):
    return Rover.rockAreaUpper > 3000 \
            and  Rover.rockAreaLower > 200
    #return Rover.rockAreaForward > Rover.minWallAreaF and Rover.sandAreaLeft >= Rover.minOpenAreaLR and Rover.sandAreaRight >= Rover.minOpenAreaLR

def needToTurnAroundQuestion(Rover):
    return Rover.rockArea > 15000 and Rover.sandAreaForward < 400

def seeBallQuestion(Rover):
    return len(Rover.ball_angles) > 0

def amPickingUpBall(Rover):
    return Rover.picking_up

def isRockAheadQuestion(Rover):
    return Rover.sandAreaUpper > 2000 and Rover.rockAreaLower > 2000

def amStuckQuestion(Rover):
    returnValueA = Rover.prevLocationValid and Rover.sameState > 200 and (Rover.preListSum / Rover.preN) < 0.35
    returnValueB = Rover.prevLocationValid and roverDist(Rover) < 0.001
    returnValueC = Rover.mode == "Stuck"
    returnValue = returnValueA or returnValueB or returnValueC

    if returnValue:
        print((returnValueA, returnValueB, returnValueC))

    return returnValue

def canPickUpQuestion(Rover):
    return Rover.near_sample and not Rover.picking_up and abs(Rover.vel) < 0.05

def returnHomeQuestion(Rover):
    return Rover.rocksCollected >= 6 and distanceHome(Rover) < 12

def distanceHome(Rover):
    return L2(Rover.pos, Rover.startPos)

def roverDist(Rover):
    return L2(Rover.pos, Rover.prevLocation)

def L2(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def hugWall(Rover):
    findOutMode(Rover)
    
    if Rover.mode == "Picking Up":
        hugWallPickUpBall(Rover)
    
    elif Rover.mode == "Can Pick Up":
        hugwallStartPickUp(Rover)

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
    
    elif Rover.mode == "Move To Ball":
        hugWallMoveToBall(Rover)

    elif Rover.mode == "Rock Ahead":
        hugWallAvoidRock(Rover)
    
    elif Rover.mode == "Front Wall":
        hugWallFrontWall(Rover)
    
    elif Rover.mode == "Stuck":
        hugWallStuck(Rover)

    elif Rover.mode == "Forward":
        #movingForward(Rover)
        hugWallMoveForward(Rover)

    elif Rover.mode == "Return Home":
        hugWallReturnHome(Rover)
    else:
        print("$$$$$$$$$$$$$$4 doing somehting at stop")
        #printDebugInfo(Rover)
        Rover.mode = "stop"
    
    printDebugInfo(Rover)

def findOutMode(Rover):
    Rover.PreviousMode = Rover.mode

    if amStuckQuestion(Rover):
        nextMode = "Stuck"

    elif Rover.wasExtreme:
        nextMode = Rover.PreviousMode
    
    elif returnHomeQuestion(Rover):
        nextMode = "Return Home"

    elif canPickUpQuestion(Rover):
        nextMode = "Can Pick Up"

    elif amPickingUpBall(Rover):
        nextMode = "Picking Up"

    elif isRockAheadQuestion(Rover):
        nextMode = "Rock Ahead"

    elif seeBallQuestion(Rover):
        nextMode = "Move To Ball"

    elif needToTurnAroundQuestion(Rover):
        nextMode = "Turn Around"

    elif inOpenAreaQuestion(Rover):
        nextMode = "Open Area"

    elif inCorridorQuestion(Rover):
        nextMode = "Corridor"

    elif onLeftWallQuestion(Rover):
        nextMode = "Left Wall"

    elif onRightWallQuestion(Rover):
        nextMode = "Right Wall"

    elif inFullCornerQuestion(Rover):
        nextMode = 'Full Corner'
    
    elif inLeftCornerQuestion(Rover):
        nextMode = "Left Corner"

    elif inRightCornerQuestion(Rover):
        nextMode = "Right Corner"

    elif onFrontWallQuestion(Rover):
        nextMode = "Front Wall"
    
    elif Rover.mode == "Forward" or Rover.sandAreaLower > 2200:
        nextMode = "Forward"
    else:
        print('**************** doing somethign')
        nextMode = 'stop'


    if nextMode == Rover.mode:
        Rover.sameState += 1
    else:
        Rover.sameState = 0

    Rover.mode = nextMode



def hugWallStuck(Rover):
    n = 50
    nby2 = n // 2
    if Rover.sameState % (n+1) < nby2:
        if abs(Rover.vel) >  0.02:
            Rover.brake = 2*Rover.brake_set
        else:
            Rover.brake = 0
            roate(Rover, 12)

    elif Rover.sameState % (n+1) < n:
        Rover.steer = -15
        Rover.brake = 0
        Rover.throttle = -0.75
    else:
        Rover.mode = "Forward"
        Rover.sameState = 1

def runTurnAngle(Rover):
    dx = Rover.startPos[0] - Rover.pos[0]
    dy = Rover.startPos[1] - Rover.pos[1]

    #angle = np.arctan2(dy, dx) * 180/np.pi
    angle = np.mean(Rover.nav_anglesH) * 180/np.pi

    return angle

def hugWallReturnHome(Rover):
    if distanceHome(Rover) < 0.5:
            Rover.brake = 100
            Rover.mode = "Completed Challenge"
    
    elif Rover.vel > 0.45:
            Rover.throttle = -.175
            Rover.brakes = 1.5
    
    elif Rover.vel < -0.45:
            Rover.throttle = Rover.throttle_set
            Rover.brakes = 1.5
    else:
        
        Rover.brake = 0
        Rover.throttle = 0.125
        angle = runTurnAngle(Rover)
        Rover.steer = np.clip(angle, -15, 15)




def hugWallMoveForward(Rover):
    Rover.throttle = Rover.throttle_set
    Rover.brake = 0
    angle = 0
    if Rover.sandAreaForwardR > 2000:
        angle = np.mean(Rover.nav_anglesF) * 180 / np.pi
    elif Rover.sandAreaForwardR > 1000:
        angle = 0
    else:
        angle = 5
    moveInDirectionOf(Rover, angle, Rover.max_vel)


def hugWallAvoidRock(Rover):
    slowDown(Rover)
    angle = 0
    
    if Rover.sandAreaForwardR > 1200:
        angle = -10
    else:
        angle = 10
    roate(Rover, angle)

def hugwallStartPickUp(Rover):
    Rover.near_sample_time = Rover.time
    Rover.throttle = 0
    Rover.brake = Rover.brake_set
    Rover.pick_up = True
    
    Rover.send_pickup = True
    Rover.rocksCollected += 1
    Rover.mode = "Picking Up"

def hugWallPickUpBall(Rover):
    if not Rover.picking_up and not Rover.near_sample:
        Rover.seeTheBall = False
        Rover.mode = 'stop'
        Rover.picking_up = False
        Rover.throttle = 0
        Rover.brake = 0


def signOfNum(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0.

def hugWallMoveToBall(Rover):
    if Rover.near_sample:
        if Rover.vel > 0.25:
            Rover.throttle = -1.75
            Rover.brakes = 9.5
        elif Rover.vel < -0.25:
            Rover.throttle = Rover.throttle_set
            Rover.brakes = 9.5
        else:
            hugwallStartPickUp(Rover)


    elif len(Rover.ball_angles) > 0:
        #if there is a rock, move *slowly* directly towards it
        Rover.throttle = 0.12
        Rover.brake = 0
        Rover.steer = signOfNum(Rover.vel)*np.clip(np.mean(Rover.ball_angles) * 180/np.pi, -15, 15)
        


def hugWallBackup(Rover):
    Rover.throttle = 0
    Rover.brake = 0
    steer = -15

    if Rover.sandAreaForward > 800:
        Rover.state = "Right Wall"
        Rover.throttle = Rover.throttle_set

### Deal with Corner state
def hugWallInCornerState(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    else:
        if 2*Rover.sandAreaForwardL >= Rover.minOpenAreaF:
            moveStraight(Rover)
        else:
            Rover.brake = 0
            roate(Rover, Rover.turnLeft)

def hugWallRightCorner(Rover):
    if abs(Rover.vel) > 0.2:
        stopMoving(Rover)
    else:
        Rover.brakes = 0
        if Rover.sandAreaForwardL < Rover.sandAreaForwardR:
            roate(Rover, Rover.turnLeft)
        elif 1000 >= Rover.sandAreaForwardR and Rover.sandAreaForwardL > Rover.minOpenAreaLR:
            Rover.mode = 'Forward'
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
            Rover.mode = 'Forward'


### Deal with corridor state
def hugWallInCorridorState(Rover):
    angle = np.mean(Rover.nav_angles) * 180/np.pi
    moveInDirectionOf(Rover, np.clip(angle, -15, 15), Rover.max_vel)



def hugWallOnLeft(Rover):
    if 6*Rover.rockAreaForwardRight > Rover.rockAreaForward:
        angle = np.mean(Rover.nav_angles) * 180/np.pi
    else:
        angle = np.mean(Rover.nav_anglesF) * 180/np.pi    

    moveInDirectionOf(Rover, angle, Rover.max_vel)


def hugWallFrontWall(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    else:
        Rover.brakes = 0
        if Rover.sandAreaForward < Rover.minOpenAreaF:
            roate(Rover, Rover.turnLeft)
        else:
            Rover.mode = 'Right Wall'
            

def hugWallStopState(Rover):
    if Rover.vel > 0.2:
        stopMoving(Rover)
    # If we're not moving (vel < 0.2) then do something else
    elif Rover.vel <= 0.2:
        if Rover.sandAreaForward < Rover.minOpenAreaF:
            roate(Rover, Rover.turnLeft)
        else:
            Rover.mode = 'Forward'


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
    Rover.brake = 0
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
    print("-"*77)
    print("|    Mode    |  OldMode  |   Position   | Dist 2 last Postion | Dist 2 Home |")
    print("-"*77)
    print("|{:^12}|{:^12}| ({:4.1f}, {:4.1f}) |{:^19.4}|{:^14.4}|".format(Rover.mode, Rover.PreviousMode, Rover.pos[0], Rover.pos[1], roverDist(Rover), distanceHome(Rover)))
    print("-"*77)

    print()
    print("-"*60)
    print("| Near Sample |  Picking up | Rocks Collected | Same State |")
    print("-"*60)
    print("|{:^13}|{:^13}|{:^17}|{:^12}|".format(Rover.near_sample, Rover.picking_up, Rover.rocksCollected, Rover.sameState))
    print("-"*60)

    print()
    print("-"*70)
    print("| Steer | H-Angle | Throttle | Speed |  Break | M-Throttle | M-Speed |")
    print("-"*70)
    print("| {:^5.2f} |{:^9.3f}| {:^8.2f} | {:^5.2f} | {:^6} |{:^12.2f}|{:^9.2f}|".format(Rover.steer, runTurnAngle(Rover),  Rover.throttle, Rover.vel, Rover.brake, Rover.throttle_set, Rover.max_vel))
    print("-"*70)


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
















################################################################
###################### DEAD CODE ###############################
################################################################
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


def ______hugWallOnRight(Rover):
    angle = 100
    
    if Rover.sandAreaForwardR > 3000:
        angle = -5
    elif Rover.sandAreaForwardR > 2975:
        angle = -4.75
    elif Rover.sandAreaForwardR > 2950:
        angle = -4.5
    elif Rover.sandAreaForwardR > 2925:
        angle = -4.25
    elif Rover.sandAreaForwardR > 2900:
        angle = -4
    elif Rover.sandAreaForwardR > 2875:
        angle = -3.75
    elif Rover.sandAreaForwardR > 2850:
        angle = -3.5
    elif Rover.sandAreaForwardR > 2825:
        angle = -3.25
    elif Rover.sandAreaForwardR > 2800:
        angle = -3
    elif Rover.sandAreaForwardR > 2775:
        angle = -2.75
    elif Rover.sandAreaForwardR > 2750:
        angle = -2.5
    elif Rover.sandAreaForwardR > 2725:
        angle = -2.25
    elif Rover.sandAreaForwardR > 2700:
        angle = -2
    elif Rover.sandAreaForwardR > 2675:
        angle = -1.75
    elif Rover.sandAreaForwardR > 2650:
        angle = -1.5
    elif Rover.sandAreaForwardR > 2625:
        angle = -1.25
    elif Rover.sandAreaForwardR > 2600:
        angle = -1
    elif Rover.sandAreaForwardR > 2550:
        angle = -0.5
    elif Rover.sandAreaForwardR > 2500:
        angle = 0
    elif Rover.sandAreaForwardR > 2450:
        angle = 0.5
    elif Rover.sandAreaForwardR > 2425:
        angle = 0.75
    elif Rover.sandAreaForwardR > 2400:
        angle = 1
    elif Rover.sandAreaForwardR > 2375:
        angle = 1.25
    elif Rover.sandAreaForwardR > 2350:
        angle = 1.5
    elif Rover.sandAreaForwardR > 2325:
        angle = 1.75
    elif Rover.sandAreaForwardR > 2300:
        angle = 2
    elif Rover.sandAreaForwardR > 2275:
        angle = 2.25
    elif Rover.sandAreaForwardR > 2250:
        angle = 2.5
    elif Rover.sandAreaForwardR > 2225:
        angle = 3
    elif Rover.sandAreaForwardR > 2200:
        angle = 3.25
    elif Rover.sandAreaForwardR > 2175:
        angle = 3.5
    elif Rover.sandAreaForwardR > 2150:
        angle = 3.75
    elif Rover.sandAreaForwardR > 2125:
        angle = 4
    elif Rover.sandAreaForwardR > 2100:
        angle = 4.25
    elif Rover.sandAreaForwardR > 2075:
        angle = 4.5
    elif Rover.sandAreaForwardR > 2050:
        angle = 4.75
    elif Rover.sandAreaForwardR > 2025:
        angle = 5
    elif Rover.sandAreaForwardR > 2000:
        angle = 5.25
    elif Rover.sandAreaForwardR > 1950:
        angle = 5.5
    elif Rover.sandAreaForwardR > 1900:
        angle = 5.75
    elif Rover.sandAreaForwardR > 1850:
        angle = 6
    elif Rover.sandAreaForwardR > 1800:
        angle = 6.25
    elif Rover.sandAreaForwardR > 1750:
        angle = 6.5
    elif Rover.sandAreaForwardR > 1700:
        angle = 6.75
    elif Rover.sandAreaForwardR > 1650:
        angle = 7
    elif Rover.sandAreaForwardR > 1600:
        angle = 7.25
    elif Rover.sandAreaForwardR > 1550:
        angle = 7.5
    elif Rover.sandAreaForwardR > 1500:
        angle = 7.625
    elif Rover.sandAreaForwardR > 1450:
        angle = 7.75
    elif Rover.sandAreaForwardR > 1400:
        angle = 7.875
    elif Rover.sandAreaForwardR > 1350:
        angle = 8
    elif Rover.sandAreaForwardR > 1300:
        angle = 8.125
    elif Rover.sandAreaForwardR > 1250:
        angle = 8.25
    elif Rover.sandAreaForwardR > 1200:
        angle = 8.375
    elif Rover.sandAreaForwardR > 1150:
        angle = 8.5
    elif Rover.sandAreaForwardR > 1100:
        angle = 8.625
    elif Rover.sandAreaForwardR > 1050:
        angle = 8.75
    elif Rover.sandAreaForwardR > 1000:
        angle = 8.875
    elif Rover.sandAreaForwardR > 950:
        angle = 9
    elif Rover.sandAreaForwardR > 900:
        angle = 9.125
    elif Rover.sandAreaForwardR > 850:
        angle = 9.25 
    elif Rover.sandAreaForwardR > 800:
        angle = 9.375 
    elif Rover.sandAreaForwardR > 750:
        angle = 9.5 
    elif Rover.sandAreaForwardR > 700:
        agnle = 9.625 
    elif Rover.sandAreaForwardR > 650:
        angle = 9.75 
    elif Rover.sandAreaForwardR > 600:
        angle = 9.875 
    elif Rover.sandAreaForwardR > 550:
        angle = 10
    elif Rover.sandAreaForwardR > 500:
        angle = 10.125
    elif Rover.sandAreaForwardR > 450:
        angle = 10.25 
    elif Rover.sandAreaForwardR > 400:
        angle = 10.375 
    elif Rover.sandAreaForwardR > 350:
        angle = 10.5 
    elif Rover.sandAreaForwardR > 300:
        angle = 10.675
    elif Rover.sandAreaForwardR > 250:
        angle = 10.75
    elif Rover.sandAreaForwardR < 100:
        angle = 13
    elif len(Rover.nav_anglesF) > 100:
        angle = np.mean(Rover.nav_anglesF) * 180/np.pi
    elif len(Rover.nav_angles) > 100:
        angle = np.mean(Rover.nav_angles) * 180/np.pi 
    else:
        angle = 8
    moveInDirectionOf(Rover, angle, Rover.max_vel)

def ______hugWallOpenArea(Rover):
    angle = np.mean(Rover.nav_angles) * 180 / np.pi if len(Rover.nav_angles) > 0 else 0.1
    if Rover.sandAreaForwardR > 5250:
        angle = -15
    elif Rover.sandAreaForwardR > 5200:
        angle = -14.75
    elif Rover.sandAreaForwardR > 5150:
        angle = -14.5
    elif Rover.sandAreaForwardR > 5100:
        angle = -14
    elif Rover.sandAreaForwardR > 5050:
        angle = -13.5
    elif Rover.sandAreaForwardR > 5000:
        angle = -13
    elif Rover.sandAreaForwardR > 4950:
        angle = -12.5
    elif Rover.sandAreaForwardR > 4900:
        angle = -12
    elif Rover.sandAreaForwardR > 4850:
        angle = -11.5
    elif Rover.sandAreaForwardR > 4800:
        angle = -11
    elif Rover.sandAreaForwardR > 4750:
        angle = -10.5
    elif Rover.sandAreaForwardR > 4700:
        angle = -10
    elif Rover.sandAreaForwardR > 4650:
        angle = -9.5
    elif Rover.sandAreaForwardR > 4600:
        angle = -9
    elif Rover.sandAreaForwardR > 4550:
        angle = -8.5
    elif Rover.sandAreaForwardR > 4500:
        angle = -8
    elif Rover.sandAreaForwardR > 4450:
        angle = -7.5
    elif Rover.sandAreaForwardR > 4400:
        angle = -7
    elif Rover.sandAreaForwardR > 4350:
        angle = -6.5
    elif Rover.sandAreaForwardR > 4300:
        angle = -6
    elif Rover.sandAreaForwardR > 4250:
        angle = -6.5
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
    else:
        angle = -1
    moveInDirectionOf(Rover, angle, Rover.max_vel)