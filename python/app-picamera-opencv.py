# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# cam_width = 4056
# cam_height = 3040
cam_width = 3280
cam_height = 2464


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (cam_width, cam_height)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(cam_width, cam_height))

# camera.capture("no_preview.jpg")
# time.sleep(0.1)

# # allow the camera to warmup
# time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # show the frame
    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # rawCapture.seek(0)
 
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

camera.close()