import queue
from bs4 import BeautifulSoup
import requests #引入网页请求
import os  #引入os命令
import logging
import time
import threading #引入线程
from logger import logger_error

class Producer(threading.Thread):
    def __init__(self, name , my_session, g_Url_Queue,g_Viewed_set,g_Viewing_set,g_Pic_Queue,g_name_Queue,mutex):
        threading.Thread.__init__(self)
        self.name = name
        self.urlq = g_Url_Queue
        self.viewset = g_Viewed_set
        self.viewingset = g_Viewing_set
        self.picqueue = g_Pic_Queue
        self.nameq = g_name_Queue
        self.session = my_session
        self.mutex = mutex

    def IsDirExit(self,filename):
        if not os.path.exists(filename):
            os.mkdir(filename)
            return False

#解析网址
    def run(self):
        while self.urlq:
            try:
                current_url = self.urlq.get()
                re_request = self.session.get(current_url)
                print(re_request)
            except:
                logger_error.info("这个网址访问异常==============" + current_url)
                continue
            try:
                re_request.encoding = 'utf-8'
                My_soup = BeautifulSoup(re_request.text,'html.parser')
            except:
                logger_error.info("构建beautifulSoup失败===========" + current_url)
                print("构建beautifulSoup失败===========" + current_url)
                continue
            Soup_f_b = My_soup.find('body')
            if Soup_f_b == None:
                logger_error.info("该Url没有body属性============" + current_url)
                continue
            #pic url
            list_img = Soup_f_b.select("img[alt]")
            self.mutex.acquire()
            for img in list_img:
                if img.get('src') not in self.viewset and img.get('src')not in self.viewingset:
                    try:
                        tmpstr = (img.get('src')).find("http")
                    except:
                        logger_error.info("find失败===========" + current_url)
                        continue
                    if tmpstr != -1:
                        self.picqueue.put(img.get('src'))
                        print(self.picqueue.qsize())
                        print(img.get('src'))
                        print("PIC over")
            self.mutex.release()

            #next url
            url_list = My_soup.select("body a")
            #print(url_list)
            self.mutex.acquire()
            for a in url_list:
                print(a.get('href'))
                if a.get('href') not in self.viewset and a.get('href') not in self.viewingset:
                    try:
                        tmpstr = (a.get('href')).find("http")
                    except:
                        logger_error.info("find失败===========" + current_url)
                        continue
                    if tmpstr != -1:
                        print('yes')
                        self.viewingset.add(a.get('href'))
                        self.urlq.put(a.get('href'))
                        print(self.urlq.qsize())
                        print("next over")
            self.mutex.release()
                         
            #name url
            name_list = My_soup.select("meta[itemprop='description']")
            self.mutex.acquire()
            for name in name_list:
                self.nameq.put(name.get('content'))
                print(self.urlq.qsize())
                print("name over")
            self.viewset.add(current_url)
            self.mutex.release()
            time.sleep(1)
        
