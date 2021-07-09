import cv2

# Image Import

img = cv2.imread("Resources/test.png")

cv2.imshow("Output", img)
cv2.waitKey(0)

# Video Import

cap = cv2.VideoCapture("Resources/test.mp4")

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Webcam Import

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
# cap.set(10, 100)

while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
