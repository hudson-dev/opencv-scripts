import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)

myColors = [[0, 187, 151, 13, 255, 255], #orange
            [80, 129, 68, 104, 231, 255], #cyan
            [40, 112, 62, 112, 255, 154]] #green

myColorValues = [[0, 165, 255], #orange    ## BGR Colorspace not RGB
                [255, 255, 102], #cyan
                [0, 204, 0]] #green

myPoints = [] ## [x_, y_, colorId]

def findColor(img, myColor, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []

    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower, upper)
        x,y = getContours(mask)
        cv2.circle(imgResult, (x,y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            # cv2.drawContours(imgResult, contour, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(contour, True)
            approxCornerPoints = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approxCornerPoints)
    return x+w//2, y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorValues)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints):
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Video", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
