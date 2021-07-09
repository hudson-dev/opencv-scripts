import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            cv2.drawContours(imgContour, contour, -1, (255, 0, 0), 3)
            perimeter = cv2.arcLength(contour, True)
            print(perimeter)
            approxCornerPoints = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            print(len(approxCornerPoints))
            objCorner = len(approxCornerPoints)
            x, y, w, h = cv2.boundingRect(approxCornerPoints)

            if objCorner == 3: objectType = "Triangle"
            elif objCorner == 4:
                aspRatio = w/float(h)
                if aspRatio > 0.95 and aspRatio < 1.05:
                    objectType="Square"
                else:
                    objectType="Rectangle"
            elif objCorner > 4:
                objectType="Circles"
            else: objectType="None"

            cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(imgContour, objectType,
                        (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 0, 0), 2)

path = "Resources/document2.png"
img = cv2.imread(path)
imgContour = img.copy()

imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGrey, (7,7), 1)
imgCanny = cv2.Canny(imgBlur, 50, 50)
getContours(imgCanny)

imgBlack = np.zeros_like(img)

# cv2.imshow("Original", img)
# cv2.imshow("Grey", imgGrey)
# cv2.imshow("Blur", imgBlur)

imgStack = stackImages(0.6, ([img, imgGrey, imgBlur],
                             [imgCanny, imgContour, imgBlack]))
cv2.imshow("Stack", imgStack)

cv2.waitKey(0)