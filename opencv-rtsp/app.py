import cv2
import time
import threading

# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
		
	# 攝影機連接。
        self.capture = cv2.VideoCapture(URL)
        self.resolution = (
            int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        print('Resolution: ', self.resolution)
        print('FPS: ', self.fps)

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
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()
        
        self.capture.release()

# URL = "rtsp://admin:pass@192.168.0.200:554/stream0"
# URL = "rtsp://admin:pass@192.168.1.211:554/stream0"
URL = 'rtsp://osense:Osense168@192.168.1.214/stream0'

# 連接攝影機
ipcam = ipcamCapture(URL)

# 啟動子執行緒
ipcam.start()

# 暫停1秒，確保影像已經填充
time.sleep(1)

# # 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    I = ipcam.getframe()
    if I == []:
        continue
    
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', I)
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    cv2.imwrite('result/' + time_now + '.bmp', I)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break
