from operator import length_hint
from turtle import distance
import cv2
import time
import numpy as np

from matplotlib import image
import imutils
from imutils.video import VideoStream
import numpy as np

arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
arucoParams = cv2.aruco.DetectorParameters_create()

def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def distance_from_ref(centers, ids, dist_ref, value_ref):
    ref_pos = np.where(ids == value_ref)[0][0]
    print(ref_pos)
    distances = []
    for i in range(len(centers)):
        if i != ref_pos:
            distances.append(distance(centers[ref_pos], centers[i])*dist_ref)
    return distances


vs = VideoStream("/dev/video0").start()
while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 1000)
    (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
    print(ids, corners)
    if corners != ():
        centres = []
        for k in range(0,len(ids)):
            sum_x = 0
            sum_y = 0
            for i in range(0,4):
                cv2.line(frame, (int(corners[k][0][(i+1)%4][0]), int(corners[k][0][(i+1)%4][1])),(int(corners[k][0][(i)%4][0]), int(corners[k][0][(i)%4][1])), (255, 0, 0),5)
                sum_x += corners[k][0][(i)%4][0]
                sum_y += corners[k][0][(i)%4][1]
            centre_x = sum_x/4
            centre_y = sum_y/4
            centres.append((int(centre_x), int(centre_y)))
            cv2.putText(frame, str(ids[k][0]),centres[k],cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2,cv2.LINE_AA)
        distance_ref = distance((corners[0][0][0][0], corners[0][0][0][1]),(corners[0][0][1][0], corners[0][0][1][1]))
        print(distance_from_ref(centres,ids[0], 5/distance_ref,17)) 
    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()