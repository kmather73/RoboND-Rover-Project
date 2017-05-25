import numpy as np
import cv2

from threshold_functions import ball_threshold, rock_threshold, sand_threshold


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
    ypix_rotated = xpix * np.sin(yaw_rad) + ypix * np.sin(yaw_rad)
    
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
    return xpix, np.cos(pitch_rad)*ypix

# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, pitch, roll, world_size, scale):
    xpix, ypix = correct4Roll(xpix, ypix, roll)
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

# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
           
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped


def convertFindings2world(threshold, Rover):
    # 4) Convert thresholded image pixel values to rover-centric coords
    x_pixels, y_pixels = rover_coords(threshold)
    # 5) Convert rover-centric pixel values to world coords
    worldsize = 200
    scale = 20
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
    p_thresh = 1
    r_thresh = 1
    return (pitch > p_thresh and pitch < 360-p_thresh) or (roll > r_thresh and roll < 360-r_thresh)
    
# Apply the above functions in succession and update the Rover state accordingly
def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    image = Rover.img
    dst_size = 10
    bottom_offset = 7
    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    destination = np.float32([[image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])
    # 2) Apply perspective transform
    img = Rover.img#correctForAngles(Rover.img, 0, 0, 0)
    warped = perspect_transform(img, source, destination)
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    sand = sand_threshold(warped)
    rock = rock_threshold(warped)
    ball = ball_threshold(warped)
    
    
    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
    Rover.vision_image[:,:, 0] = rock
    Rover.vision_image[:,:, 1] = ball
    Rover.vision_image[:,:, 2] = sand
        # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
        #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
        #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image

    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates

    sand_x_world, sand_y_world = convertFindings2world(sand, Rover)
    rock_x_world, rock_y_world = convertFindings2world(rock, Rover)
    ball_x_world, ball_y_world = convertFindings2world(ball, Rover)
    # 7) Update Rover worldmap (to be displayed on right side of screen)
        # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
        #          Rover.worldmap[rock_y_world, roc0k_x_world, 1] += 1
        #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    if not extremeAngles(Rover.pitch, Rover.roll):
        Rover.worldmap[rock_y_world, rock_x_world, 0] += 1
        Rover.worldmap[ball_y_world, ball_x_world, 1] += 1
        Rover.worldmap[sand_y_world, sand_x_world, 2] += 1
    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
        # Rover.nav_dists = rover_centric_pixel_distances
        # Rover.nav_angles = rover_centric_angles
    x_pixels, y_pixels = rover_coords(sand)
    dist, angles = to_polar_coords(x_pixels, y_pixels)
    Rover.nav_dists = dist
    Rover.nav_angles = angles
 
    
    
    return Rover