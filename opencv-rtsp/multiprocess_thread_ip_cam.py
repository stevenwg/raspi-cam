import time
from datetime import datetime
import cv2
import timeit
import threading

class ipCamCapture:
    def __init__(self, USER, PWD, IP, INDEX, SAVEPATH=[]):
        self.Frame = []
        self.status = False
        self.isStop = False
        self.URL = "rtsp://%s:%s@%s/stream0" % (USER, PWD, IP)
        self.savePath = SAVEPATH
		
	# 攝影機連接。
        self.capture = cv2.VideoCapture(self.URL)
        self.resolution = (
            int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        print('IP: ', IP, ', Resolution: ', self.resolution, ', FPS: ', self.fps)

    def start(self):
	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
        print('IP: ', IP, ' cam started!')
        threading.Thread(target=self.queryFrameThread, daemon=True, args=()).start()

    def stop(self):
	# 記得要設計停止無限迴圈的開關。
        self.isStop = True
        print('IP: ', IP, ' cam stopped!')
   
    def getFrame(self):
	# 當有需要影像時，再回傳最新的影像。
        return self.Frame
        
    def queryFrameThread(self):
        while (not self.isStop):
            self.status, self.Frame = self.capture.read()
        
        self.capture.release()

    def saveFrameThread(self):
        threading.Thread(target=self.saveFrame, daemon=True, args=()).start()

    def saveFrame(self):
        time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:0]
        cv2.imwrite((self.savePath + time_now + '_cam' + INDEX + '.jpg'), self.Frame)
        print("ID: ", INDEX, ", ", time_now, ", save time: ", (timeit.default_timer()-start))


def run():
    # URL1 = 'rtsp://admin:pass@192.168.1.211:554/stream0'
    USER = ['admin', 'osense', 'osense', 'osense', 'osense']
    PWD = ['pass', 'Osense168', 'Osense168', 'Osense168', 'Osense168']
    IP = ['192.168.1.211:554', '192.168.1.212:554', '192.168.1.214:554', '192.168.1.217:554', '192.168.1.218:554']
    INDEX = [211, 212, 213, 214, 217, 218]
    SAVEPATH = 'result_multiprocess_thread/'

    ipCams = []
    for idx in range(len(INDEX)):
        ipCams.append(ipCamCapture(USER[idx], PWD[idx], IP[idx], INDEX[idx], SAVEPATH))
    
    for ipCam in ipCams:
        ipCam.start()

    for ipCam in ipCams:
        cv2.namedWindow(IP[idx], cv2.WINDOW_NORMAL)
        
    while True:
        start = timeit.default_timer()
        for ipCam in ipCams:
            cv2.imshow(IP[idx], ipCam.getFrame())
        
        for ipCam in ipCams:
            ipCam.saveFrameThread()
        time.sleep(0.15)
        
        if cv2.waitKey(1) == 27:
            cv2.destroyAllWindows()
            for ipCam in ipCams:
                ipCam.stop()
            break
        
        print(len(IP), ' cameras exec time: ', (timeit.default_timer()-start))
    


if __name__ == '__main__':
    run()

