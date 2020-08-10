import time
from datetime import datetime
import multiprocessing as mp
import cv2
import timeit
import threading

# class ipCamCapture:
#     def __init__(self, USER, PWD, IP, INDEX, SAVEPATH=[]):
#         self.Frame = []
#         self.status = False
#         self.isStop = False
#         self.URL = "rtsp://%s:%s@%s/stream0" % (USER, PWD, IP)
#         self.savePath = SAVEPATH
		
# 	# 攝影機連接。
#         self.capture = cv2.VideoCapture(self.URL)
#         self.resolution = (
#             int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
#             int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#         self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))
#         print('IP: ', IP, ', Resolution: ', self.resolution, ', FPS: ', self.fps)

#     def start(self):
# 	# 把程式放進子執行緒，daemon=True 表示該執行緒會隨著主執行緒關閉而關閉。
#         print('IP: ', IP, ' cam started!')
#         threading.Thread(target=self.queryFrameThread, daemon=True, args=()).start()
#         threading.Thread(target=self.saveThread, daemon=True, args=()).start()

#     def stop(self):
# 	# 記得要設計停止無限迴圈的開關。
#         self.isStop = True
#         print('IP: ', IP, ' cam stopped!')
   
#     def getframe(self):
# 	# 當有需要影像時，再回傳最新的影像。
#         return self.Frame
        
#     def queryFrameThread(self):
#         while (not self.isStop):
#             self.status, self.Frame = self.capture.read()
        
#         self.capture.release()

#     def saveThread(self):
#         mp.set_start_method(method='spawn')  # init
#         while (not self.isStop):
#             if self.Frame == []:
#                 continue
#             processe = mp.Process(target=self.saveFrame, args=())
#             processe.daemon = True
#             processe.start()

#     def saveFrame(self):
#         time_now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
#         cv2.imwrite(self.savePath, time_now, '_cam', INDEX, '.jpg', self.Frame)


# # URL1 = 'rtsp://admin:pass@192.168.1.211:554/stream0'
# USER = 'admin'
# PWD = 'pass'
# IP = '192.168.1.211:554'
# INDEX = 211
# SAVEPATH = 'result_multiprocess_thread/'

# ipcam1 = ipCamCapture(USER, PWD, IP, INDEX, SAVEPATH)
# ipcam1.start()

# while True:
#     I1 = ipcam1.getframe()
#     if cv2.waitKey(1) == 27:
#         cv2.destroyAllWindows()
#         ipcam.stop()
#         break



def saveFrame():
    start = timeit.default_timer()
    frame = cv2.imread('result_9cam_fastsaving/2020-08-08_18-09-06_cam5.jpg')
    savePath = 'result_multiprocess_thread/'
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-1]
    cv2.imwrite((savePath + time_now + '_cam_test.jpg'), frame)
    # img_str = cv2.imencode('.jpg', frame)[1].tostring()
    print(time_now, ", save time: ", (timeit.default_timer()-start))


def run():
    start = timeit.default_timer()
    mp.set_start_method(method='spawn')  # init
    processes = []
    # for i in range(100):
    while True:
        # process = mp.Process(target=saveFrame, args=())
        # process.daemon = True
        # process.start()
        # processes.append(process)
        # time.sleep(0.2)
        thread = threading.Thread(target=saveFrame, daemon=True, args=()).start()
        time.sleep(0.03)

    
    # for process in processes:
    #     process.join()
    time.sleep(5)
    print('total time: ', (timeit.default_timer()-start))
    


if __name__ == '__main__':
    run()

