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
    print("Current mode:", Rover.mode, "!")
    if Rover.nav_angles is not None:
        # Check for Rover.mode status
        if Rover.near_sample and not Rover.picking_up:
            Rover.send_pickup = True
            Rover.throttle = 0
            Rover.brake = Rover.brake_set
            Rover.mode = 'pick_up'
            

            
        elif Rover.mode == 'pick_up' and not Rover.picking_up and not Rover.near_sample:
            Rover.mode = 'forward'
            Rover.picking_up = 0
            Rover.send_pickup = 0
            Rover.throttle = Rover.throttle_set
            Rover.brake = 0

        elif Rover.mode == 'forward': 
            movingForward(Rover)

        elif Rover.mode == 'stop':
            isStoped(Rover)

        elif Rover.mode == 'corner':
            inCorner(Rover)


    # Just to make the rover do something 
    # even if no modifications have been made to the code
    else:
        Rover.throttle = Rover.throttle_set
        Rover.steer = 0
        Rover.brake = 0

    return Rover



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
        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
    # If there's a lack of navigable terrain pixels then go to 'stop' mode
    else:
    #if len(Rover.nav_angles) < Rover.stop_forward:
        # Set mode to "stop" and hit the brakes!
        Rover.throttle = 0
        # Set brake to stored brake value
        Rover.brake = Rover.brake_set
        Rover.steer = 0
        Rover.mode = 'corner'
        Rover.inCorner = True
        Rover.angleInCorner = Rover.yaw



def isStoped(Rover):
    # If we're in stop mode but still moving keep braking
    if Rover.vel > 0.2:
        Rover.throttle = 0
        Rover.brake = Rover.brake_set
        Rover.steer = 0
    # If we're not moving (vel < 0.2) then do something else
    elif Rover.vel <= 0.2:
        if len(Rover.nav_angles) < Rover.go_forward:
            Rover.throttle = 0
            # Release the brake to allow turning
            Rover.brake = 0
            # Turn range is +/- 15 degrees, when stopped the next line will induce 4-wheel turning
            Rover.steer = 15 # Could be more clever here about which way to turn
        # If we're stopped but see sufficient navigable terrain in front then go!
        if len(Rover.nav_angles) >= Rover.go_forward:
            # Set throttle back to stored value
            Rover.throttle = Rover.throttle_set
            # Release the brake
            Rover.brake = 0
            # Set steer to mean angle
            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
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
        if Rover.sandArea >= Rover.rockArea:
            Rover.throttle = Rover.throttle_set
            Rover.inCorner = False
            Rover.brake = 0
            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -15, 15)
            Rover.mode = 'forward'