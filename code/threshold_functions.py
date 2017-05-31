import numpy as np
import cv2


def get_perspect_transform(img, src, dst):     
    M = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))# keep same size as input image
    
    return warped

def perspect_transform_mapping(image):
    dst_size = 18
    bottom_offset = 7
    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    destination = np.float32([
                  [image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])

    return get_perspect_transform(image, source, destination)

def perspect_transform(image):
    dst_size = 11
    bottom_offset = 7
    source = np.float32([[14, 140], [301 ,140],[200, 96], [118, 96]])
    destination = np.float32([
                  [image.shape[1]/2 - dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - bottom_offset],
                  [image.shape[1]/2 + dst_size, image.shape[0] - 2*dst_size - bottom_offset], 
                  [image.shape[1]/2 - dst_size, image.shape[0] - 2*dst_size - bottom_offset],
                  ])

    return get_perspect_transform(image, source, destination)


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
    #YUV = YUV_find_sand(img)
    Lab = Lab_find_sand(img)
    kernel = np.ones((5,5),np.uint8)
    img2 = Lab
    #img2 = approxByContour(img2)
    
    
    #img2 = cv2.dilate(img2,kernel,iterations = 1)
    #img2 = cv2.erode(img2,kernel,iterations = 1)
    #img2 = approxByContour(img2)
    return img2


### Rock Functions ###
def LUV_find_rock(img):
    return LUV_threshold(img,(35,100, 100), (65, 160, 160)) 

def LUV2_find_rock(img):
    return LUV2_threshold(img, (65,50,40), (255,255,255))

def HSV_find_rock(img):
    return HSV_threshold(img, (0,30,0), (80,255,100))

def YCC_find_rock(img):
    return YCC_threshold(img, (0,112, 0), (102, 168, 127))

def YUV_find_rock(img, mask=None):
    YUV = YUV_threshold(img, (0, 20, 20), (100, 200, 200))
    if mask is None:
        mask = np.ones_like(YUV)
        mask = perspect_transform(mask)
    return maskImg(YUV, mask)

def HSL_find_rock(img):
    return HSL_threshold(img, (0,0,10),(31,102,163))

def Lab_find_rock(img,mask=None):
    Lab = Lab_threshold(img, (0,108, 128), (102, 148, 255))
    if mask is None:
        mask = np.ones_like(Lab)
        mask = perspect_transform(mask)
    return maskImg(Lab, mask)

def rock_threshold(img, mask=None):
    rock = YUV_find_rock(img, mask)
    kernel = np.ones((5,5),np.uint8)
    
    rock = cv2.dilate(rock,kernel,iterations = 2)
    rock = approxByContour(rock)
    rock = cv2.erode(rock,kernel,iterations = 2)
    
    return rock
def reducedWalls(rock):
    
    notRock = np.zeros_like(rock)
    cv2.bitwise_not(rock, notRock)
    notRock = maskROI(notRock)
    
    kernel = np.ones((5,5),np.uint8)
    
    rock = cv2.dilate(rock,kernel,iterations = 1)
    notRock = cv2.dilate(notRock,kernel,iterations = 1)
    rock = maskROI(rock)
    notRock = maskROI(notRock)
    
    rock = cv2.bitwise_and(rock, notRock)
    return rock
    #return cv2.erode(rock, kernel, iterations = 1)

def reducedWalls2(rock, sand):
    
    
    notRock = np.zeros_like(rock)
    cv2.bitwise_not(rock, notRock)
    notRock = maskROI(notRock)
    
    notSand = np.zeros_like(sand)
    cv2.bitwise_not(rock, notSand)
    notSand = maskROI(notSand)
    
    
    kernel = np.ones((3,3),np.uint8)
    
    
    rock = cv2.dilate(rock,kernel,iterations = 1)
    notRock = cv2.dilate(notRock,kernel,iterations = 1)
    sand = cv2.dilate(sand, kernel, iterations = 2)
    notSand = cv2.dilate(notSand, kernel, iterations = 2)
    
    
    rock = maskROI(rock)
    notRock = maskROI(notRock)
    sand = maskROI(sand)
    notSand = maskROI(notSand)
    
    
    
    rockWall = cv2.bitwise_and(rock, notRock)
    sandWall = cv2.bitwise_and(sand, notSand)
    
    rockWall = maskROI(cv2.dilate(rockWall, kernel, iterations = 2))
    sandWall = maskROI(cv2.dilate(sandWall, kernel, iterations = 2))
    
    wall = cv2.bitwise_and(rockWall, sandWall)
    wall = cv2.erode(wall, kernel, iterations = 1)
    
    return maskROI(wall)


def inSideOfWalls(warped, rock):
    walls = reducedWalls(warped)
    
    outside = cv2.bitwise_or(walls, rock)
    inside = cv2.bitwise_not(outside)
    inside = maskROI(inside)
    return inside

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
    return cv2.inRange(img, (100, 0, 0), (255, 255, 20)) # (100, 100, 0), (210, 210, 55))

def ball_threshold(img):
    return RGB_find_ball(img)



def getBestContour(threshold):
    im2,contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt = None
    area = 0
    for ct in contours:
        ctArea = cv2.contourArea(ct)
        if ctArea > area:
            area = ctArea
            cnt = ct
            
    return cnt, area

def approxByContour(threshold):
    im2,contours,hierarchy = cv2.findContours(threshold,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img = np.zeros_like(threshold)
    
    for cnt in contours:
        epsilon = 0.002 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        cv2.fillPoly(img, [approx] , 255)
    return img

def maskImg(img, mask):
    return cv2.bitwise_and(img,img, mask=mask)

def maskRightSide(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape

    mask[w*52/100:,h*75/100:] = 1
    
    mask = perspect_transform(mask)
    return maskImg(img, mask)

def maskLeftSide(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape

    
    mask[w*52/100:,:h*25/100] = 1
    mask = perspect_transform(mask)
    return maskImg(img, mask)

def maskStraightAhead(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape

    mask[w*52/100:,h*25/100: h*75/100] = 1
    
    mask = perspect_transform(mask)
    return maskImg(img, mask)

def maskStraightLeftAhead(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape
    mask[int(w*52/100):,int(h*25/100): int(h*50/100)] = 1
    mask = perspect_transform(mask)
    return maskImg(img, mask)

def maskStraightRightAhead(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape
    mask[int(w*52/100):,int(h*50/100): int(h*75/100) ] = 1
    mask = perspect_transform(mask)
    return maskImg(img, mask)


def maskROI(img):
    if len(img.shape) == 3:
        mask = np.ones_like(img[:,:,0])
    else:
        mask = np.ones_like(img[:,:])

    mask = perspect_transform(mask)
    kernel = np.ones((3,3),np.uint8)
    
    (h,w) = mask.shape
    
    mask[0:5,:] = 0
    mask[:,0:5] = 0
    mask[:,w-6:w-1] = 0
    mask = cv2.erode(mask, kernel, iterations=1)
    return maskImg(img, mask)

def maskBias(img):
    if len(img.shape) == 3:
        mask = np.zeros_like(img[:,:,0])
    else:
        mask = np.zeros_like(img[:,:])

    (w, h) = mask.shape
    mask[:,int(h*50/100):] = 1
    mask = perspect_transform(mask)
    mask[:, :int(h*2/10)] = 0
    mask[:, int(h*9/10):] = 0
    return maskImg(img, mask)

def maskUpper(img):
    if len(img.shape) == 3:
        mask = np.ones_like(img[:,:,0])
    else:
        mask = np.ones_like(img[:,:])

    (h,w) = mask.shape
    mask = perspect_transform(mask)
    
    mask[:,:int(w*4/10)] = 0
    mask[:,int(w*6/10):] = 0
    mask[int(h*5/10):, int(w*4/10) : int(w*6/10)] = 0
    return maskImg(img, mask)

def maskLower(img):
    if len(img.shape) == 3:
        mask = np.ones_like(img[:,:,0])
    else:
        mask = np.ones_like(img[:,:])

    (h,w) = mask.shape
    mask = perspect_transform(mask)
    
    mask[:,:int(w*4/10)] = 0
    mask[:,int(w*6/10):] = 0
    mask[:int(h*5/10), int(w*4/10) : int(w*6/10)] = 0
    return maskImg(img, mask)


def maskReduceMap(img):
    if len(img.shape) == 3:
        mask = np.ones_like(img[:,:,0])
    else:
        mask = np.ones_like(img[:,:])

    (h,w) = mask.shape
    mask[:, : int(w*25/100)] = 0
    mask[: int(h*20/100), :] = 0
    return maskImg(img, mask)    