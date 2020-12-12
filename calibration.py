import numpy as np
import cv2 
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import os


#Constants
WORKDIR = 'Images/'
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
BOARD = aruco.CharucoBoard_create(7,5,1,0.8, ARUCO_DICT)

#Parameters
images = np.array([WORKDIR + file for file in os.listdir(WORKDIR) if file.startswith("image") and file.endswith(".png")])
order = np.argsort([int(p.split(".")[-2].split("_")[-1]) for p in images])
images = images[order]

#Detect the markers on all the image
def read_chessboard(images):
    print("Pose Estimation starts: ")
    allCorners = []
    allIDs = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("Processing image {0}".format(im))
        
        frame = cv2.imread(im)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, ARUCO_DICT)
        if len(corners) > 0 :
            #SUB PIXEL DETECTION
            for corner in corners :
                cv2.cornerSubPix(gray, corner, winSize = (3,3), zeroZone = (-1, 1), criteria = criteria)
                res2 = aruco.interpolateCornersCharuco(corners, ids, gray, BOARD)
                if res2[1] is not None and res2 is not None and len(res2[1])>3 and decimator%1==0 :
                    allCorners.append(res2[1])
                    allIDs.append(res2[2])
        decimator+=1
    imsize = gray.shape
    return allCorners, allIDs, imsize

#allCorners, allIds, imsize = read_chessboard(images)

#Calibrate the camera based on the previous markers detection
def calibrate_camera(allCorners, allIds, imsize):
    print("Camera Calibration")
    cameraMatrixInit = np.array([[1000., 0., imsize[0]/2.], [0., 1000., imsize[1]/2.], [0., 0., 1.]])
    print(cameraMatrixInit)
    distCoeffsInit = np.zeros((5,1))
    print(distCoeffsInit)
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    print(flags)
    ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors, stdDeviationsIntrinsics, stdDeviationsExtrinsics, perViewErrors = aruco.calibrateCameraCharucoExtended(charucoCorners = allCorners, charucoIds = allIds, board = BOARD, imageSize = imsize, cameraMatrix = cameraMatrixInit, distCoeffs = distCoeffsInit, flags = flags, criteria = (cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))
    print(ret)
    return ret, camera_matrix, distortion_coefficients0, rotation_vectors, translation_vectors

#ret, mtx, dist, rvecs, tvecs = calibrate_camera(allCorners=allCorners, allIds=allIds, imsize= imsize)


#Store the calibration parameters in a .txt file
def storeCalibrationParameters(ret, camera_matrix, distortion_coefficients0):
    with open("CalibrationParameters.txt", "w") as file:
        file.write(f"Camera calibration parameters : ret = {ret}, camera_Matrix = {camera_matrix}, distortion = {distortion_coefficients0}'")

#storeCalibrationParameters(ret, camera_matrix, distortion_coefficients0)