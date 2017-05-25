import numpy as np
import cv2

def HSL_threshold(img, lower, upper):
    HSL = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    HSL = cv2.inRange(HSL, lower, upper)
    return HSL

def LUV_threshold(img, lower, upper):
    LUV = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    LUV = cv2.inRange(LUV, lower, upper)
    return LUV

def LUV2_threshold(img, lower, upper):
    LUV = cv2.cvtColor(img, cv2.COLOR_RGB2LUV)
    LUV = cv2.inRange(LUV, lower, upper)
    LUV2 = np.zeros_like(img[:,:,0])
    
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    LUV2[(LUV == 0)  & (gray!=0)] = 1
    return LUV2

def HSV_threshold(img, lower, upper):
    HSV = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    HSV = cv2.inRange(HSV,lower, upper)
    return HSV

def YCC_threshold(img, lower, upper):
    yCrCb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    yCrCb = cv2.inRange(yCrCb, lower, upper)
    return yCrCb

def YUV_threshold(img, lower, upper):
    yuv = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    yuv = cv2.inRange(yuv, lower, upper)
    return yuv

def Lab_threshold(img, lower, upper):
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2Lab)
    lab = cv2.inRange(lab, lower, upper)
    return lab


### Sand Functions ###
def LUV_find_sand(img):
    return LUV_threshold(img,(80,50,40), (255,255,255))

def LUV2_find_sand(img):
    return LUV2_threshold(img, (0,50,40), (100,255,255))

def HSV_find_sand(img):
    return HSV_threshold(img, (0,30,180), (80,255,255))

def YCC_find_sand(img):
    return YCC_threshold(img, (127,100, 0), (255, 157, 147))

def YUV_find_sand(img):
    return YUV_threshold(img, (127,100, 0), (255, 157, 147))

def HSL_find_sand(img):
    return HSL_threshold(img, (0,50,80),(63,255,255))

def Lab_find_sand(img):
    return Lab_threshold(img, (127,100, 128), (255, 255, 255))

def sand_threshold(img):
    #HSL = HSL_find_sand(img)
    #LUV = LUV_find_sand(img)
    #LUV2 = LUV2_find_sand(img)
    #HSV = HSV_find_sand(img)
    #YCC = YCC_find_sand(img)
    YUV = YUV_find_sand(img)
    #Lab = Lab_find_sand(img)
    return YUV


### Rock Functions ###
def LUV_find_rock(img):
    return LUV_threshold(img,(35,100, 100), (65, 160, 160)) 

def LUV2_find_rock(img):
    return LUV2_threshold(img, (65,50,40), (255,255,255))

def HSV_find_rock(img):
    return HSV_threshold(img, (0,30,0), (80,255,100))

def YCC_find_rock(img):
    return YCC_threshold(img, (0,112, 0), (102, 168, 127))

def YUV_find_rock(img):
    return YUV_threshold(img, (1, 20, 20), (100, 200, 200))

def HSL_find_rock(img):
    return HSL_threshold(img, (0,0,10),(31,102,163))

def Lab_find_rock(img):
    return Lab_threshold(img, (1,108, 128), (102, 148, 255))

def rock_threshold(img):
    return Lab_find_rock(img)

### Ball Functions ###
def LUV_find_ball(img):
    return LUV_threshold(img,(35,100, 100), (65, 160, 160)) 

def LUV2_find_ball(img):
    return LUV2_threshold(img, (65,50,40), (255,255,255))

def HSV_find_ball(img):
    return HSV_threshold(img, (0,30,0), (80,255,100))

def YCC_find_ball(img):
    return YCC_threshold(img, (0,112, 0), (102, 168, 127))

def YUV_find_ball(img):
    return YUV_threshold(img, (1, 20, 20), (100, 200, 200))

def HSL_find_ball(img):
    return HSL_threshold(img, (0,0,10),(31,102,163))

def Lab_find_ball(img):
    return Lab_threshold(img, (1,108, 128), (102, 148, 255))

def RGB_find_ball(img):
    return cv2.inRange(img, (100, 0, 0), (255, 255, 20))

def ball_threshold(img):
    return RGB_find_ball(img)