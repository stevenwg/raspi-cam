import time
from datetime import datetime
import cv2
import timeit
import threading

def saveFrame():
    start = timeit.default_timer()
    frame = cv2.imread('result_9cam_fastsaving/2020-08-08_18-09-06_cam1.jpg')
    savePath = 'result_multiprocess_thread/'
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-1]
    cv2.imwrite((savePath + time_now + '_cam_test.jpg'), frame)
    # cv2.imwrite((savePath + time_now + '_cam_test.bmp'), frame) # No decode, fast speed
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

