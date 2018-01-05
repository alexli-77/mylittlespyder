import queue 
import requests #引入网页请求
import os  #引入os命令
import logging
import time
import threading #引入线程
from logger import logger_error
from logger import logger_debug
#mutex = threading.RLock()
class picconsumer(threading.Thread):
    def __init__(self, name, queue, mutex, session):
        threading.Thread.__init__(self)
        self.name = name
        self.picno = 0
        self.mutex = mutex
        self.data = queue
        self.session = session
        #本地目录
        self.picDir = os.path.abspath('.')
        self.picDir = os.path.join(self.picDir, 'picDir')

    # 判断目录是否存在
    def IsDirExit(self):
        if not os.path.exists(self.picDir):
            os.mkdir(self.picDir)

    def run(self):
        print("---------------")
        while True:
            while self.data.qsize() > 0:
                self.mutex.acquire()
                pic_url = self.data.get();
                try:
                    re_request = self.session.get(pic_url)
                except :
                    logger_error.info("这个网址访问异常==============" + pic_url)
                    continue
                if re_request.status_code == 200:
                    print(self.picDir)
                    picconsumer.IsDirExit(self)
                    filepath = os.path.join(self.picDir + '/' + str(self.picno) + '.jpg')
                    with open(filepath, 'wb') as code:
                        code.write(re_request.content)
                        self.picno += 1
                        logger_debug.info("pic: ---" + filepath)
                self.mutex.release()
                time.sleep(1)





        