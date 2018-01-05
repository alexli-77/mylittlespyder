#从第一个url开始，不停爬取网站的url，将爬到的url放入View_Queue，再爬取时，从View_Queue中
#将已爬取的url放入已爬取的容器
from bs4 import BeautifulSoup
import threadpool
#引入队列
import queue 
import requests #引入网页请求
import os  #引入os命令
import logging
import threading #引入线程
from collections import deque
#introduced threadpool
from pic_consumer import picconsumer
from name_consumer import nameconsumer
from producer import Producer
from logger import logger_debug

def IsNeededUrl():
    return False


#picture number

#使用线程爬取所有url，并将爬到的url放到队列
#g_threadPool = threadpool.ThreadPool(10)
#python2 is xrange, python3 is range

if __name__ == "__main__":
    #定义线程爬取网址
    logger_debug.info('开始爬虫了')
    #建立一个永久会话
    my_session = requests.session()
    #定义初始网址
    initial_page = "http://wufazhuce.com/one/1293"
    #定义一个伪装成浏览器的头
    my_header = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
    #正在访问的页面队列
    g_Url_Queue = queue.Queue() 
    #已爬取的url
    g_Viewed_set = set()
    #准备爬取的url
    g_Viewing_set = set()
    #motto队列
    g_name_Queue = queue.Queue() 
    #图片的url
    g_Pic_Queue = queue.Queue()
    #向爬取的队列插入url
    g_Url_Queue.put(initial_page)
    #向将要爬取的集合插入url,求并集 (I use |= to put data into set)
    g_Viewing_set.add(initial_page) 
    #使用线程爬取所有url，并将爬到的url放到队列
    #本地目录
    mutex = threading.Lock()
    #picDir = os.path.abspath('.')
    #picDir = os.path.join(picDir, 'picDir')
    p1 = Producer("Producer-1",my_session,g_Url_Queue,g_Viewed_set,g_Viewing_set,g_Pic_Queue,g_name_Queue,mutex)
    c1 = picconsumer("Consumer-1",g_Pic_Queue,mutex,my_session)
    c2 = nameconsumer("consumer-2",g_name_Queue,mutex)

    p1.start()
    c1.start()
    c2.start()

    logger_debug.info("爬取url完成，共爬取到了%d个Url")
#逐个分析队列中的url