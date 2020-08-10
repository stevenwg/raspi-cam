import cv2
import time
import timeit
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
# URL = "rtsp://admin:pass@192.168.1.199:554/stream0"
URL1 = "rtsp://admin:pass@192.168.1.211:554/stream0"
URL2 = "rtsp://osense:Osense168@192.168.1.212:554/stream0"
URL3 = "rtsp://osense:Osense168@192.168.1.213:554/stream0"
URL4 = "rtsp://osense:Osense168@192.168.1.214:554/stream0"
URL5 = "rtsp://osense:Osense168@192.168.1.215:554/stream0"
URL6 = "rtsp://osense:Osense168@192.168.1.216:554/stream0"
URL7 = "rtsp://osense:Osense168@192.168.1.217:554/stream0"
URL8 = "rtsp://osense:Osense168@192.168.1.218:554/stream0"
URL9 = "rtsp://osense:Osense168@192.168.1.219:554/stream0"

# 連接攝影機
ipcam1 = ipcamCapture(URL1)
ipcam2 = ipcamCapture(URL2)
# ipcam3 = ipcamCapture(URL3)
ipcam4 = ipcamCapture(URL4)
# ipcam5 = ipcamCapture(URL5)
# ipcam6 = ipcamCapture(URL6)
ipcam7 = ipcamCapture(URL7)
ipcam8 = ipcamCapture(URL8)
# ipcam9 = ipcamCapture(URL9)

# 啟動子執行緒
ipcam1.start()
ipcam2.start()
# ipcam3.start()
ipcam4.start()
# ipcam5.start()
# ipcam6.start()
ipcam7.start()
ipcam8.start()
# ipcam9.start()

# 暫停1秒，確保影像已經填充
time.sleep(1)

# cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('cam_1', cv2.WINDOW_NORMAL)
cv2.namedWindow('cam_2', cv2.WINDOW_NORMAL)
cv2.namedWindow('cam_4', cv2.WINDOW_NORMAL)
cv2.namedWindow('cam_7', cv2.WINDOW_NORMAL)
cv2.namedWindow('cam_8', cv2.WINDOW_NORMAL)
# # 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    start = timeit.default_timer()
    # 使用 getframe 取得最新的影像
    I1 = ipcam1.getframe()
    I2 = ipcam2.getframe()
    # I3 = ipcam3.getframe()
    I4 = ipcam4.getframe()
    # I5 = ipcam5.getframe()
    # I6 = ipcam6.getframe()
    I7 = ipcam7.getframe()
    I8 = ipcam8.getframe()
    # I9 = ipcam9.getframe()
    # if I1 == [] or I2 == [] or I3 == [] or I4 == [] or I5 == [] or I6 == [] or I7 == [] or I8 == [] or I9 == []:
    #     continue
    if I1 == [] or I2 == [] or I4 == [] or I7 == [] or I8 == []:
        continue
    
    # cv2.imshow('Image', I)
    # cv2.imshow('cam_1', I1)
    # cv2.imshow('cam_2', I2)
    # cv2.imshow('cam_4', I4)
    # cv2.imshow('cam_7', I7)
    # cv2.imshow('cam_8', I8)

    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    # start_save = timeit.default_timer()
    # cv2.imwrite('result_9cam/' + time_now + '_cam1.jpg', I1)
    # print('imwrite time: ', (timeit.default_timer()-start_save))
    # cv2.imwrite('result_9cam/' + time_now + '_cam2.jpg', I2)
    # cv2.imwrite('result_9cam/' + time_now + '_cam3.jpg', I3)
    # cv2.imwrite('result_9cam/' + time_now + '_cam4.jpg', I4)
    # cv2.imwrite('result_9cam/' + time_now + '_cam5.jpg', I5)
    # cv2.imwrite('result_9cam/' + time_now + '_cam6.jpg', I6)
    # cv2.imwrite('result_9cam/' + time_now + '_cam7.jpg', I7)
    # cv2.imwrite('result_9cam/' + time_now + '_cam8.jpg', I8)
    # cv2.imwrite('result_9cam/' + time_now + '_cam9.jpg', I9)
    # print('write 9 down')
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break

    print("exec_time: ", (timeit.default_timer()-start), ", fps: ", 1/(timeit.default_timer()-start))