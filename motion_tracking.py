import cv2
import numpy as np

cam = cv2.VideoCapture(0)
cam.set(3, 600)
cam.set(4, 300)
fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
bool, pre = cam.read()

while True:
    bool, cur = cam.read()
    if not bool:
        break
    cur_g = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
    cur_g = cv2.GaussianBlur(cur_g, (21, 21), 0)
    pre_g = cv2.cvtColor(pre, cv2.COLOR_BGR2GRAY)
    pre_g = cv2.GaussianBlur(pre_g, (21, 21), 0)
    diff = cv2.absdiff(pre_g, cur_g)
    thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh.copy(), None, iterations=52)

    frame = cur.copy()

    image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        vertices = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) < 1000:
            continue
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.drawContours(thresh, [cnt], -1, (255, 255, 0), -1)
        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(frame, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.rectangle(thresh, (cX - 50, cY - 150), (cX + 50, cY + 50), (255, 255, 0), 255, -1)
        cv2.rectangle(frame, (vertices[0], vertices[1]), (vertices[0] + vertices[2], vertices[1] + vertices[3]), (255, 255, 0), 3)

    cv2.imshow("Video", frame)
    cv2.imshow("Thresh", thresh)
    x = cv2.waitKey(20)
    if chr(x & 0xFF) == "q":
        break
    pre = cur

cam.release()
cv2.destroyAllWindows()
