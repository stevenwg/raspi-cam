from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
from datetime import datetime
import timeit
import threading

# cam_width = 4056
# cam_height = 3040
cam_width = 640
cam_height = 540

# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = None
        self.status = False
        self.isstop = False

        self.camera = PiCamera()
        self.camera.resolution = (cam_width, cam_height)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(cam_width, cam_height))
		
	# 攝影機連接。
        # self.capture = cv2.VideoCapture(URL)

    def start(self):
	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
	# 記得要設計停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')
   
    def getframe(self):
	# 當有需要影像時，再回傳最新的影像。
        return self.Frame
        
    def queryframe(self):
        start = timeit.default_timer()
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            print("frame rate: %.5f" % (1/(timeit.default_timer() - start)))
            start = timeit.default_timer()

            self.Frame = frame.array
            self.rawCapture.truncate(0)
            datestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
            cv2.imwrite(datestr + ".jpg", self.Frame)
            


        self.camera.close()
        # self.capture.release()

URL = 0

# 連接攝影機
ipcam = ipcamCapture(URL)

# 啟動子執行緒
ipcam.start()

# 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    I = ipcam.getframe()
    if I is None:
        continue
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', I)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break
