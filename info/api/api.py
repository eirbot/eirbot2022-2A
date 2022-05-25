"""
API using flask without frontend
"""
import cv2
import imutils
import math

import numpy as np
from cv2 import VideoCapture
from flask import Blueprint, request

REFERENCE = 42


class API:
    """
    Définition des points de terminaison de l'API classique pouvant être utilisées dans le cas de la coupe
    """

    def __init__(self):
        self.bp = Blueprint('api', __name__, url_prefix='/api')

        self.cap = None
        self.device_id = None
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.center_x = None
        self.center_y = None
        self.aruco_size = 5.0
        self.ratio = None

        self.bp.route('/initialize', methods=['POST'])(self.initialize)
        self.bp.route('/find', methods=['GET'])(self.find)
        self.bp.route('/find/<id>', methods=['GET'])(self.find_by_id)
        self.bp.route('/position', methods=['GET'])(self.position)
        self.bp.route('/release', methods=['GET'])(self.release)

        self.DIM = (640, 480)
        self.K = np.array([[379.6688975804594, 0.0, 312.0300482074414], [0.0, 379.5133193658524, 227.21496286416718],
                      [0.0, 0.0, 1.0]])
        self.D = np.array([[-0.08455712051937993], [-0.13201934759139028], [0.21704389572592145], [-0.11366112601728705]])

    def initialize(self):
        """
        Initialisation de la caméra avec l'id de la caméra donnée dans la requête
        :return: {'status': 'error', 'message': 'Device not found'}, 402 si la caméra n'est pas trouvée
        :return: {'status': 'success', 'message': 'Video with device id {} initialized'}, 200 si la caméra est
        initialisée
        """
        if request.method == 'POST':
            data = request.get_json()
            self.cap = VideoCapture(int(data['device_id']))
            try:
                success, frame = self.cap.read()
                h, w = frame.shape[:2]
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM,
                                                                 cv2.CV_16SC2)
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            except cv2.error:
                return {'status': 'error', 'message': 'Device not found'}, 402
            self.device_id = int(data['device_id'])
            self.cap.release()
            return {'status': 'success',
                    'message': 'Video with device id {} initialized'.format(data['device_id'])}, 200

    def find(self):
        """
        Trouve tous les markers actuellement présents sur la caméra
        :return: {'status': 'error', 'message': 'Video not initialized'}, 404 si la caméra n'est pas initialisée
        :return: {'status': 'error', 'message': 'Marker not found'}, 404 si aucun marker n'est présent
        :return: {'status': 'success', 'message': json_list}, 200 si un ou plusieurs markers sont présents où
        json_list est un dictionnaire contenant l'id du marker et les coordonnées des coins du marker
        """
        if request.method == 'GET':
            if self.device_id is None:
                return {'status': 'error', 'message': 'Video not initialized'}, 404
            else:
                self.cap = VideoCapture(self.device_id)
                success, frame = self.cap.read()
                h, w = frame.shape[:2]
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM,
                                                                 cv2.CV_16SC2)
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                if not success:
                    self.cap.release()
                    return {'status': 'error', 'message': 'Marker not found'}, 404
                corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, self.aruco_dict,
                                                                          parameters=self.parameters)
                if ids is None:
                    self.cap.release()
                    return {'status': 'error', 'message': 'Marker not found'}, 404

                json_list = []
                for i in range(len(ids)):
                    json_list.append({'id': str(ids[i][0]), 'corners': corners[i][0].tolist()})
                self.cap.release()
                return {'status': 'success', 'message': json_list}, 200

    def find_by_id(self, id):
        """
        Trouve un marker avec l'id donné
        :param id : id du marker
        :return: {'status': 'error', 'message': 'Video not initialized'}, 404 si la caméra n'est pas initialisée
        :return: {'status': 'error', 'message': 'Marker not found'}, 404 si le marker n'est pas présent
        :return: {'status': 'success', 'message': json_list}, 200 si le marker est présent où json_list est un
        dictionnaire contenant l'id du marker et les coordonnées des coins du marker
        """
        if request.method == 'GET':
            if self.device_id is None:
                return {'status': 'error', 'message': 'Video not initialized'}, 404
            else:
                self.cap = VideoCapture(self.device_id)
                success, frame = self.cap.read()
                h, w = frame.shape[:2]
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM,
                                                                 cv2.CV_16SC2)
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                if not success:
                    self.cap.release()
                    return {'status': 'error', 'message': 'Video not initialized'}, 404
                (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                                                   self.aruco_dict,
                                                                   parameters=self.parameters)
                for i in range(len(ids)):
                    if ids[i][0] == int(id):
                        json_list = {'id': str(ids[i][0]), 'corners': corners[i][0].tolist()}
                        self.cap.release()
                        return {'status': 'success', 'message': json_list}, 200
                else:
                    self.cap.release()
                    return {'status': 'error', 'message': 'Marker not found'}, 404

    def position(self):
        """
        Trouve la position du marker par rapport au marker de référence
        :return: {'status': 'error', 'message': 'Video not initialized'}, 404 si la caméra n'est pas initialisée
        :return: {'status': 'error', 'message': 'Marker not found'}, 404 si le marker n'est pas présent
        :return: {'status': 'success', 'message': json_list}, 200 si le marker est présent où json_list est un
        dictionnaire contenant l'id du marker, sa distance par rapport au marker de référence (euclidienne,
        en x et en y)
        """
        if request.method == 'GET':
            if self.device_id is None:
                return {'status': 'error', 'message': 'Video not initialized'}, 404
            else:
                self.cap = VideoCapture(self.device_id)
                success, frame = self.cap.read()
                h, w = frame.shape[:2]
                map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM,
                                                                 cv2.CV_16SC2)
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
                if not success:
                    return {'status': 'error', 'message': 'Video not initialized'}, 404
                frame = imutils.resize(frame, width=1000)
                (corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
                                                                   self.aruco_dict,
                                                                   parameters=self.parameters)
                if len(corners) == 0:
                    return {'status': 'error', 'message': 'Marker not found'}, 404
                self.calibrate_unit(corners, ids)
                self.find_origin(corners, ids)
                json = self.distance_from_origin(corners, ids)
                self.cap.release()
                return {'status': 'success', 'message': json}, 200

    def release(self):
        """
        Libère la caméra
        :return: {'status': 'success', 'message': 'Video released'}, 200
        :return: {'status': 'error', 'message': 'Video not initialized'}, 404
        """
        if request.method == 'GET':
            if self.device_id is None:
                return {'status': 'error', 'message': 'Video not initialized'}, 404
            else:
                self.cap.release()
                return {'status': 'success', 'message': 'Video released'}, 200

    def find_origin(self, corners, ids):
        """
        Trouve le marker de référence
        """
        for id in range(len(ids)):
            if ids[id] == REFERENCE:
                center = (corners[id][0][0] + corners[id][0][2]) / 2
                self.center_x = center[0]
                self.center_y = center[1]
        # if REFERENCE is not in the list, then the origin is None
        if REFERENCE not in ids:
            self.center_y = None
            self.center_x = None

    def distance_from_origin(self, corners, ids):
        """
        Trouve la distance du marker par rapport au marker de référence
        """
        json = {}
        for id in range(len(ids)):
            if ids[id] != REFERENCE:
                try:
                    center = (corners[id][0][0] + corners[id][0][2]) / 2
                    distance_x = (center[0] - self.center_x) * self.ratio
                    distance_y = (center[1] - self.center_y) * self.ratio
                    diag = math.sqrt(distance_x ** 2 + distance_y ** 2)
                    print(corners)
                    haut = 1.5 if ids[id] >= 11 and ids[id] <= 50 else 43
                    distance = math.sqrt(abs(diag ** 2 - haut ** 2))
                    json[id] = {'id': str(ids[id][0]), 'distance_x': distance_x, 'distance_y': distance_y,
                                'distance': distance, 'corners': (str(corners[id][0][0]), str(corners[id][0][1]),
                                                                  str(corners[id][0][2]), str(corners[id][0][3]))}
                except TypeError:
                    pass
        return json

    def calibrate_unit(self, corners, ids):
        """
        Calcule le ratio entre pixel et mètre
        """
        for id in range(len(ids)):
            if ids[id] == REFERENCE:
                pixel_size_x_1 = abs(corners[id][0][0][0] - corners[id][0][2][0])
                # pixel_size_y_1 = abs(corners[id][0][0][1] - corners[id][0][2][1])
                # pixel_size_1 = math.sqrt(pixel_size_x_1 ** 2 + pixel_size_y_1 ** 2)
                #
                # pixel_size_x_2 = abs(corners[id][0][1][0] - corners[id][0][3][0])
                # pixel_size_y_2 = abs(corners[id][0][1][1] - corners[id][0][3][1])
                # pixel_size_2 = math.sqrt(pixel_size_x_2 ** 2 + pixel_size_y_2 ** 2)

                # pixel_size = (pixel_size_1 + pixel_size_2) / 2
                if pixel_size_x_1 != 0:
                    self.ratio = self.aruco_size / pixel_size_x_1
