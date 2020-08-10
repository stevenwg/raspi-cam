import cv2
import time
import threading
import timeit

# 接收攝影機串流影像，採用多執行緒的方式，降低緩衝區堆疊圖幀的問題。
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
		
        if URL != 0:
            self.Frame = cv2.imread(URL)
	# 攝影機連接。
        if URL == 0:
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
            if URL == 0:
                time_start = timeit.default_timer()
                self.status, self.Frame = self.capture.read()
                print('capture.read time: %.3f' % (timeit.default_timer() - time_start))
            pass
        
        # self.capture.release()

URL = 0

URL1 = 'result_9cam/2020-08-07_21-49-54_cam1.jpg'
URL2 = 'result_9cam/2020-08-07_21-49-54_cam2.jpg'
URL3 = 'result_9cam/2020-08-07_21-49-54_cam3.jpg'
URL4 = 'result_9cam/2020-08-07_21-49-54_cam4.jpg'
URL5 = 'result_9cam/2020-08-07_21-49-54_cam5.jpg'
URL6 = 'result_9cam/2020-08-07_21-49-54_cam6.jpg'
URL7 = 'result_9cam/2020-08-07_21-49-54_cam7.jpg'
URL8 = 'result_9cam/2020-08-07_21-49-54_cam8.jpg'
URL9 = 'result_9cam/2020-08-07_21-49-54_cam9.jpg'

# 連接攝影機
# ipcam = ipcamCapture(URL)
ipcam1 = ipcamCapture(URL1)
ipcam2 = ipcamCapture(URL2)
ipcam3 = ipcamCapture(URL3)
ipcam4 = ipcamCapture(URL4)
ipcam5 = ipcamCapture(URL5)
ipcam6 = ipcamCapture(URL6)
ipcam7 = ipcamCapture(URL7)
ipcam8 = ipcamCapture(URL8)
ipcam9 = ipcamCapture(URL9)

# 啟動子執行緒
# ipcam.start()
ipcam1.start()
ipcam2.start()
ipcam3.start()
ipcam4.start()
ipcam5.start()
ipcam6.start()
ipcam7.start()
ipcam8.start()
ipcam9.start()

# 暫停1秒，確保影像已經填充
time.sleep(1)

# # 使用無窮迴圈擷取影像，直到按下Esc鍵結束
while True:
    # 使用 getframe 取得最新的影像
    # I =ipcam.getframe()
    I1 = ipcam1.getframe()
    I2 = ipcam2.getframe()
    I3 = ipcam3.getframe()
    I4 = ipcam4.getframe()
    I5 = ipcam5.getframe()
    I6 = ipcam6.getframe()
    I7 = ipcam7.getframe()
    I8 = ipcam8.getframe()
    I9 = ipcam9.getframe()
    # if I == []:
    #     coutinue
    if I1 == [] or I2 == [] or I3 == [] or I4 == [] or I5 == [] or I6 == [] or I7 == [] or I8 == [] or I9 == []:
        continue
    
    # cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    # cv2.imshow('Image', I)
    time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())

    time_start = timeit.default_timer()
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam1.bmp', I1)
    print('Saving 1 time: %.3f' % (timeit.default_timer() - time_start))
    
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam2.bmp', I2)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam3.bmp', I3)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam4.bmp', I4)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam5.bmp', I5)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam6.bmp', I6)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam7.bmp', I7)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam8.bmp', I8)
    cv2.imwrite('result_9cam_fastsaving/' + time_now + '_cam9.bmp', I9)
    print('Saving 9 time: %.3f' % (timeit.default_timer() - time_start))
    
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        break
