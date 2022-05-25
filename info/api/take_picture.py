import datetime
import cv2
import numpy as np


def undistord(img_path):
    DIM = (640, 480)
    K = np.array([[379.6688975804594, 0.0, 312.0300482074414], [0.0, 379.5133193658524, 227.21496286416718],
                       [0.0, 0.0, 1.0]])
    D = np.array([[-0.08455712051937993], [-0.13201934759139028], [0.21704389572592145], [-0.11366112601728705]])
    img = cv2.imread(img_path)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # cap = cv2.VideoCapture(2)
    # ret, frame = cap.read()
    # time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # cv2.imwrite('./images_calibration/calibration_image{}.jpg'.format(time), frame)
    # cap.release()
    undistord('./images_calibration/calibration_image2022-05-21_16-47-32.jpg')
