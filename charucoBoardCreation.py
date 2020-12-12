import numpy as np
import cv2 
import cv2.aruco as aruco
import matplotlib.pyplot as plt

#CONSTANTES
ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_6X6_250)
WORKDIR = "./CHarUco/"

#Board creation
board = aruco.CharucoBoard_create(7,5,1,0.8, ARUCO_DICT)
imboard = board.draw((2000,2000))
cv2.imwrite(filename= WORKDIR + "chessboard.tiff", img=imboard)

#Show board
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.imshow(imboard, cmap = 'gray', interpolation = 'nearest')
ax.axis('off')
plt.show()

