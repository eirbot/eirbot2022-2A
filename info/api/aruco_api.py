"""
API flask for the video module with frontend
"""
from math import sqrt

import cv2
import imutils as imutils
import numpy as np
from flask import render_template, Blueprint, request, Response
from cv2 import aruco

REFERENCE = 42


def draw_aruco(corners, ids, frame):
    """
    Dessine-les aruco sur la video
    """
    for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners

        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
        cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
        cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)
        cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

        cv2.putText(frame, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)


class ArucoVideo:
    """
    Class for the video blueprint
    """

    def __init__(self):
        self.device_id = None
        self.bp = Blueprint('video', __name__, url_prefix='/video')
        self.cap = None
        self.camera = None
        self.camera_list = []
        self.center_x = None
        self.center_y = None
        self.aruco_size = 5.0
        self.aruco_size_ref = 10.0

        self.ratio = None
        self.pixels_ref = None

        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters_create()

        self.bp.route('/scan', methods=['GET'])(self.scan)
        self.bp.route('/choose_device', methods=['POST'])(self.choose_device)
        self.bp.route('/video_stream/<device>')(self.video_stream)
        self.bp.route('/stop')(self.stop)

        self.DIM = (640, 480)
        self.K = np.array([[379.6688975804594, 0.0, 312.0300482074414], [0.0, 379.5133193658524, 227.21496286416718],
                      [0.0, 0.0, 1.04]])
        self.D = np.array([[-0.08455712051937993], [-0.13201934759139028], [0.21704389572592145], [-0.11366112601728705]])

    def scan(self):
        """
        Scan les cameras et retourne la liste des devices disponibles
        """
        self.camera_list = []
        for i in range(0, 10):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    self.camera_list.append(i)
                    cap.release()
            except:
                pass
        if len(self.camera_list) == 0:
            return render_template('index.html')
        return render_template('index.html', devices=self.camera_list)

    def choose_device(self):
        """
        Choisit la camera a utiliser
        """
        # Choose device
        try:
            device = int(request.form['device_id'])
        except KeyError:
            return render_template('index.html', alert='No device selected')
        self.camera = device
        return render_template('index.html', devices=self.camera_list, device_id=self.camera)

    def angle_corner(self, corner, id):
        d_x = corner[0][0][0] - corner[0][1][0]
        d_y = corner[0][0][1] - corner[0][1][1]
        angle = np.arctan2(d_y, d_x) * 180 / 3.14
        print(id, angle, "°")
        return angle

    def gen_frames(self):
        """
        Génère les frames de la video et les retourne
        """
        self.cap = cv2.VideoCapture(self.device_id)
        while True:
            success, frame = self.cap.read()
            h, w = frame.shape[:2]
            map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM, cv2.CV_16SC2)
            frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            if not success:
                break
            else:
                frame = imutils.resize(frame, width=1000)
                kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])

                (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                                                   self.aruco_dict,
                                                                   parameters=self.parameters)
                aruco.drawDetectedMarkers(frame, corners)  # Draw A square around the markers

                # verify *at least* one ArUco marker was detected
                if len(corners) > 0:
                    ids = ids.flatten()
                    self.find_origin(corners, ids)
                    if np.all(ids is not None):  # If there are markers found by detector
                        for i in range(0, len(ids)):  # Iterate in markers
                            center = (corners[i][0][0] + corners[i][0][2]) / 2
                            cv2.circle(frame, (int(center[0]), int(center[1])), 2, (255, 0, 0), 1)
                            self.angle_corner(corners[i], ids[i])
                            cv2.putText(frame, "Pos: x " + str(center[0]) + " y " + str(center[1]) + ".", (int(center[0]), int(center[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            if self.center_x != None and self.center_y != None and ids[i] != REFERENCE:
                                hauteur = 1.5 if ids[i] >= 11 and ids[i] <= 50 else 43.
                                dist_diag = (1 - hauteur / 100) *  sqrt((center[0] - self.center_x) ** 2 + (center[1] - self.center_y) ** 2) * self.aruco_size_ref / self.pixels_ref
                                dist_y = (1 - hauteur / 100) *  (center[0] - self.center_x) * self.aruco_size_ref / self.pixels_ref
                                dist_y *= -1
                                dist_x = (1 - hauteur / 100) *  (center[1] - self.center_y) * self.aruco_size_ref / self.pixels_ref
                                print(ids[i], dist_diag, " CM.", dist_x + 150, "x", dist_y + 125, "y")

                            # Display the resulting frame
                    #self.calibrate_unit(corners, ids)
                    #self.distance_from_origin(corners, ids, frame)
                    #draw_aruco(corners, ids, frame)
                    # loop over the detected ArUCo corners
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def video_stream(self, device):
        """
        Retourne la video
        """
        self.device_id = int(device)
        return Response(self.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    def stop(self):
        """
        Stoppe la video
        """
        self.cap.release()
        return render_template('index.html', success="Stream stopped")

    def find_origin(self, corners, ids):
        """
        Trouve l'origine
        """
        for id in range(len(ids)):
            if ids[id] == REFERENCE:
                center = (corners[id][0][0] + corners[id][0][2]) / 2
                self.center_x = center[0]
                self.center_y = center[1]
                d_x = corners[id][0][0][0] - corners[id][0][1][0]
                d_y = corners[id][0][0][1] - corners[id][0][1][1]
                self.pixels_ref = sqrt(d_x ** 2 + d_y ** 2)
                print(self.pixels_ref / self.aruco_size_ref, " for 1cm. ref")
                
        # if REFERENCE is not in the list, then the origin is None
        if REFERENCE not in ids:
            self.center_y = None
            self.center_x = None
            self.pixels_ref = None

    def distance_from_origin(self, corners, ids, frame):
        """
        Trouve la distance de l'origine
        """
        for id in range(len(ids)):
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[id], 0.05, self.K, self.D)
            cv2.aruco.drawAxis(frame, self.K, self.D, rvec, tvec, 0.03)
            if ids[id] != REFERENCE:
                try:
                    center = (corners[id][0][0] + corners[id][0][2]) / 2
                    cv2.line(frame, (int(center[0]), int(center[1])), (int(self.center_x), int(self.center_y)),
                             (0, 255, 0),
                             2)
                    diag = ((center[0] - self.center_x) ** 2 + (center[1] - self.center_y) ** 2) ** 0.5 * self.ratio
                    haut = 1.5 if ids[id] >= 11 and ids[id] <= 50 else 43
                    distance = sqrt(abs(diag ** 2 - haut ** 2))
                    cv2.putText(frame, "Distance: " + str(round(distance, 2)) + "cm", (int(center[0]), int(center[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                except TypeError:
                    pass

    def calibrate_unit(self, corners, ids):
        """
        Calcule le ratio entre pixel et cm
        """
        pixel_size = []
        for id in range(len(ids)):
            pixel_size_x_1 = abs(corners[id][0][0][0] - corners[id][0][2][0])
            pixel_size_y_1 = abs(corners[id][0][0][1] - corners[id][0][2][1])

            pixel_size_x_2 = abs(corners[id][0][1][0] - corners[id][0][3][0])
            pixel_size_y_2 = abs(corners[id][0][1][1] - corners[id][0][3][1])

            pixel_size_1 = (pixel_size_x_1 + pixel_size_y_1) / 2
            pixel_size_2 = (pixel_size_x_2 + pixel_size_y_2) / 2
            if sqrt(self.aruco_size/pixel_size_1 ** 2 + pixel_size_2 ** 2) > 0.0001:
                pixel_size.append(self.aruco_size/sqrt(pixel_size_1 ** 2 + pixel_size_2 ** 2))
        self.ratio = sum(pixel_size) / len(pixel_size)

