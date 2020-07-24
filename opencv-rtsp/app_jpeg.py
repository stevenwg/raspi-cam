import cv2
import urllib.request
import numpy as np
import time
import threading

# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
		
	# 攝影機連接。
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # self.stream = urllib.request.urlopen(URL)
        password_mgr.add_password(None, URL, "admin", "pass")
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        # urllib.request.install_opener(opener)
        #self.stream = urllib.request.urlopen(URL + "/getimage")
        self.stream = opener.open("http://192.168.0.200:80/getimage")
        self.bytes = ''

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
            self.bytes += self.stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                self.Frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.CV_LOAD_IMAGE_COLOR)
        self.capture.release()

URL = "http://192.168.0.200:80"

# 連接攝影機
ipcam = ipcamCapture(URL)

# 啟動子執行緒
ipcam.start()

# 暫停1秒，確保影像已經填充
time.sleep(1)

# 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    I = ipcam.getframe()
    
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Image', I)
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    cv2.imwrite('result/' + time_now + '.jpg', I)
    if cv2.waitKey(1000) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break
