import picamera
import time


#Parameters
RESOLUTION =  (1280, 960)
FRAMERATE = 30
TIME_INTERVAL = 3
NUMBER_OF_IMAGES = 10

def video_to_image():
    #Initialize the camera
    with picamera.PiCamera() as camera:
        camera.resolution = RESOLUTION
        camera.framerate = FRAMERATE
        camera.start_preview()
        try : 
            for i, filename in enumerate(camera.capture_continuous('imageBoussole_{counter:02d}.png')):
                print(filename)
                time.sleep(TIME_INTERVAL)
                if i == NUMBER_OF_IMAGES - 1 :
                    break
        finally : 
            camera.stop_preview()