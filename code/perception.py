import numpy as np
import cv2

from threshold_functions import *


# Define a function to convert to rover-centric coordinates
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = np.absolute(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[0]).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to apply a rotation to pixel positions
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians and apply rotation
    yaw_rad = yaw * np.pi / 180.0
    xpix_rotated = xpix * np.cos(yaw_rad) - ypix * np.sin(yaw_rad)
    ypix_rotated = xpix * np.sin(yaw_rad) + ypix * np.cos(yaw_rad)
    
    return xpix_rotated, ypix_rotated

# Define a function to perform a translation
def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = np.int_(xpos + xpix_rot/scale)
    ypix_translated = np.int_(ypos + ypix_rot/scale)
    
    return xpix_translated, ypix_translated

def correct4Roll(xpix, ypix, roll):
    roll_rad = roll * np.pi / 180.0
    return np.cos(roll_rad)*xpix, ypix

def correct4Pitch(xpix, ypix, pitch):
    pitch_rad = pitch * np.pi / 180.0

    if pitch > 0:
        return xpix, np.cos(pitch_rad)*ypix
    return xpix, ypix

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, pitch, roll, world_size, scale):
    #xpix, ypix = correct4Roll(xpix, ypix, roll)
    xpix, ypix = correct4Pitch(xpix, ypix, pitch)
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world


def convertFindings2world(threshold, Rover):
    # 4) Convert thresholded image pixel values to rover-centric coords
    x_pixels, y_pixels = rover_coords(threshold)
    # 5) Convert rover-centric pixel values to world coords
    worldsize = 200
    scale = 22
    x_world, y_world = pix_to_world(x_pixels, y_pixels, Rover.pos[0], Rover.pos[1], Rover.yaw,Rover.pitch, Rover.roll, worldsize, scale)

    return x_world, y_world

def correctForAngles(img, roll, pitch, yaw):
    roll_rad = roll * np.pi / 180.0
    pitch_rad = pitch * np.pi / 180.0
    yaw_rad = yaw * np.pi / 180.0

    R_x = np.array([np.array([1, 0, 0 ]),
                    np.array([0, np.cos(roll_rad), -np.sin(roll_rad)]),
                    np.array([0, np.sin(roll_rad), np.cos(roll_rad)])
                    ])

    R_y = np.array([np.array([np.cos(pitch_rad), 0, np.sin(pitch_rad)]),
                    np.array([0, 1, 0]),
                    np.array([-np.sin(pitch_rad), 0, np.cos(pitch_rad)])
                    ])

    R_z = np.array([np.array([np.cos(yaw_rad), -np.sin(yaw_rad), 0]),
                    np.array([np.sin(yaw_rad), np.cos(yaw_rad), 0]),
                    np.array([0, 0, 1])
                    ])
    R = R_z * R_y * R_x
    
    outputImage = cv2.warpPerspective(img, R, (img.shape[1], img.shape[0]))
    return outputImage

def extremeAngles(pitch, roll):
    p_thresh = 0.75
    r_thresh = 1.1

    return (pitch > p_thresh and pitch < 360-p_thresh) or (roll > r_thresh and roll < 360-r_thresh)

import numpy as np

def correctRotateImage(img, angle):
  
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h//2 )

    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
 
    # perform the actual rotation and return the image
    return cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR)

def fillMapHoles(Rover):
    worldmap = np.copy(Rover.worldmap[:,:, 2]).astype(np.uint8)
    
    mask = cv2.bitwise_not(np.copy(Rover.hiddenRockMap).astype(np.uint8))
    worldmap = maskImg(worldmap, mask)


    im2, contours, hierarchy = cv2.findContours(worldmap, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    img = np.zeros_like(worldmap)
    cv2.fillPoly(img, contours , 1)
    
    kernel = np.ones((5,5), np.uint8)
    cv2.erode(img, kernel, iterations = 1)
    cv2.dilate(img, kernel, iterations = 1)

    ypos, xpos = img.nonzero()
    Rover.worldmap[ypos, xpos, 2] += 1



    
    
def perception_look_for_sand(Rover, warped):
    # 3) Apply color threshold to identify terrain
    sand = sand_threshold(warped)
    left_sand = maskLeftSide(sand)
    right_sand = maskRightSide(sand)

    forward_sand = maskStraightAhead(sand)
    forward_sand_left = maskStraightLeftAhead(sand)
    forward_sand_right = maskStraightRightAhead(sand)
    
    upper_sand = maskUpper(sand)
    lower_sand = maskLower(sand)

    sn, sandArea = getBestContour(np.copy(sand))
    snl, sandAreaLeft = getBestContour(left_sand)
    snr, sandAreaRight = getBestContour(right_sand)

    snf, sandAreaForward = getBestContour(np.copy(forward_sand))
    snfl, sandAreaForwardL = getBestContour(forward_sand_left)
    snfr, sandAreaForwardR = getBestContour(forward_sand_right)

    snup, sandAreaUpper = getBestContour(upper_sand)
    snlow, sandAreaLower = getBestContour(lower_sand)
    

    Rover.sandArea = sandArea if sn is not None else 0
    Rover.sandAreaLeft = sandAreaLeft if snl is not None else 0
    Rover.sandAreaRight = sandAreaRight if snr is not None else 0

    Rover.sandAreaForward = sandAreaForward if snf is not None else 0
    Rover.sandAreaForwardL = sandAreaForwardL if snfl is not None else 0
    Rover.sandAreaForwardR = sandAreaForwardR if snfr is not None else 0

    Rover.sandAreaUpper = sandAreaUpper if snup is not None else 0
    Rover.sandAreaLower = sandAreaLower if snlow is not None else 0


    # 4) Update Rover.vision_image
    rock = rock_threshold(warped)
    sand2 = inSideOfWalls(sand, rock)

    kernel = np.ones((5,5),np.uint8)
    #sand = cv2.erode(sand, kernel, iterations = 1)
    sand = cv2.dilate(sand, kernel,iterations = 1)
    
    #sand2 = cv2.erode(sand2, kernel, iterations = 1)
    #sand2 = cv2.dilate(sand2,kernel,iterations = 1)

    ssand = cv2.bitwise_and(sand, sand2)
    
    
    ssand = cv2.erode(ssand, kernel, iterations = 1)
    #ssand = cv2.dilate(ssand, kernel,iterations = 1)
    ssand = maskReduceMap(ssand)

    Rover.vision_image[:,:, 2] = ssand


    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates
    sand_x_world, sand_y_world = convertFindings2world(sand, Rover)

    
    # 7) Update Rover worldmap
    if not extremeAngles(Rover.pitch, Rover.roll):
        Rover.worldmap[sand_y_world, sand_x_world, 2] += 1

    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
    x_pixels, y_pixels = rover_coords(sand)
    dist, angles = to_polar_coords(x_pixels, y_pixels)
    Rover.nav_dists = dist
    Rover.nav_angles = angles


    x_pixelsF, y_pixelsF = rover_coords(forward_sand)
    distF, anglesF = to_polar_coords(x_pixelsF, y_pixelsF)
    Rover.nav_distsF = distF
    Rover.nav_anglesF = anglesF

    


def perception_look_for_rocks(Rover, warped):
    # 3) Apply color threshold to identify walls and rocks
    rock = rock_threshold(warped, Rover.coneMask)
    left_rock = maskLeftSide(rock)
    right_rock = maskRightSide(rock)

    forward_left_rock = maskStraightLeftAhead(rock)
    forward_right_rock = maskStraightRightAhead(rock)
    
    upper_rock = maskUpper(rock)
    lower_rock = maskLower(rock)

    rn, rockArea = getBestContour(np.copy(rock))
    rnl, rockAreaLeft = getBestContour(left_rock)
    rnr, rockAreaRight = getBestContour(right_rock)

    rnfl, rockAreaForwardLeft = getBestContour(forward_left_rock)
    rnfr, rockAreaForwardRight = getBestContour(forward_right_rock)
    
    rnup, rockAreaUpper = getBestContour(upper_rock)
    rnlow, rockAreaLower = getBestContour(lower_rock)

    Rover.rockArea = rockArea if rn is not None else 0
    Rover.rockAreaLeft = rockAreaLeft if rnl is not None else 0
    Rover.rockAreaRight = rockAreaRight if rnr is not None else 0

    Rover.rockAreaForwardLeft = rockAreaForwardLeft if rnfl is not None else 0
    Rover.rockAreaForwardRight = rockAreaForwardRight if rnfr is not None else 0
    
    Rover.rockAreaUpper = rockAreaUpper
    Rover.rockAreaLower = rockAreaLower

    Rover.rockAreaForward = Rover.rockAreaForwardLeft + Rover.rockAreaForwardRight
    # 4) Update Rover.vision_image
    sand = sand_threshold(warped)
    reduecdRock = reducedWalls2(rock, sand)

    reduecdRock = maskReduceMap(reduecdRock)
    rock = maskReduceMap(rock)

    Rover.vision_image[:,:, 0] = reduecdRock

    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates
    reduecdRock_x_world, reduecdRock_y_world = convertFindings2world(reduecdRock, Rover)
    rock_x_world, rock_y_world = convertFindings2world(rock, Rover)
    
    # 7) Update Rover worldmap
    if not extremeAngles(Rover.pitch, Rover.roll):
        Rover.worldmap[reduecdRock_y_world, reduecdRock_x_world, 0] += 2
        Rover.hiddenRockMap[rock_y_world, rock_x_world] += 1

def perception_look_for_balls(Rover, warped):
    
    ball = ball_threshold(warped)
    ball2 = ball_threshold(Rover.img)
    bn, ballArea = getBestContour(np.copy(ball))
    Rover.ballArea = ballArea if bn is not None else 0
    Rover.seeTheBall = True if bn is not None else False

    # 4) Update Rover.vision_image
    Rover.vision_image[:,:, 1] = ball
    
    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates
    ball_x_world, ball_y_world = convertFindings2world(ball, Rover)
    
    # 7) Update Rover worldmap
    if not extremeAngles(Rover.pitch, Rover.roll):
        Rover.worldmap[ball_y_world, ball_x_world, 1] += 1

    x_pixels, y_pixels = rover_coords(ball)
    ball_dists, ball_angles = to_polar_coords(x_pixels, y_pixels)
    Rover.ball_dists = ball_dists
    Rover.ball_angles = ball_angles


def blurImg(img):
    blur = cv2.blur(img,(5,5))
    #blur = cv2.GaussianBlur(img,(11,11),0)
    return blur

# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # NOTE: camera image is coming to you in Rover.img
    
    #Rover.img = blurImg(Rover.img)
    img = blurImg(Rover.img)
    img = Rover.img

    #correctionAngle = Rover.roll-360 if Rover.roll > 180 else -Rover.roll
    correctionAngle = Rover.roll
    Rover.img = img = correctRotateImage(img, correctionAngle)
    warped = perspect_transform(img)


    perception_look_for_sand(Rover, warped)
    perception_look_for_rocks(Rover, warped)
    perception_look_for_balls(Rover, warped)
    fillMapHoles(Rover)

    Rover.wasExtreme = extremeAngles(Rover.pitch, Rover.roll)
    return Rover