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


#正在访问的页面队列
g_Url_Queue = queue.Queue() 
#已爬取的url
g_Viewed_set = set()
#准备爬取的url
g_Viewing_set = set()
#图片的url
g_Pic_Queue = queue.Queue()
# 创建一个logger
logger_name = logging.getLogger('namelogger')
logger_name.setLevel(logging.DEBUG)
# 创建一个logger
logger_error = logging.getLogger('errorlogger')
logger_error.setLevel(logging.DEBUG)
# 创建一个logger
logger_debug = logging.getLogger('debuglogger')
logger_debug.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
name_file = logging.FileHandler('namelog.log')
name_file.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
error_file = logging.FileHandler('errorlog.log')
error_file.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
debug_file = logging.FileHandler('debuglog.log')
debug_file.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
name_file.setFormatter(formatter)
error_file.setFormatter(formatter)
debug_file.setFormatter(formatter)
# 给logger添加handler
logger_name.addHandler(name_file)
logger_error.addHandler(error_file)
logger_debug.addHandler(debug_file)

mutex = threading.RLock()
#判断目录是否存在
def IsDirExit(filename):
    if not os.path.exists(filename):
        os.mkdir(filename)
    return False

#判断是否是需要的网址

def IsNeededUrl():
    return False
#解析网址

def ParseUrl(g_Url_Queue,g_Viewed_set,g_Viewing_set):
    while g_Url_Queue:
        current_url = g_Url_Queue.get()
        try:
            re_request = my_session.get(current_url)
        except :
            logger_error.info("这个网址访问异常==============" + current_url)
            continue

        mutex.acquire()
        try:
        	
        	re_request.encoding = 'utf-8'
        	My_soup = BeautifulSoup(re_request.text)

        except :
            logger_error.info("构建beautifulSoup失败===========" + current_url)
            print("构建beautifulSoup失败===========" + current_url)
            continue
        Soup_f_b = My_soup.find('body')
        if Soup_f_b == None:
            logger_error.info("该Url没有body属性============" + current_url)
            continue
        #pic url
        list_img = Soup_f_b.select("img[alt]")
        for img in list_img:
            if img.get('src') not in g_Viewed_set and img.get('src')not in g_Viewing_set:
                try:
                    result_pic = my_session.get(img_url)
                except:
                    logger_error.info("这个网址访问异常==============" + img_url)
                if result_pic.status_code == 200:
                    IsDirExit(picDir)
                    picDir = os.path.join(picDir + '/' + picno + '.jpg')
                    with open(filename) as code:
                        code.write(result_pic.content)
                    picno += 1
                g_Pic_Queue.put(img.get('src'))
                print(img.get('src'))
        print("PIC over")
        #next url
        url_list = My_soup.select("body a")
        print(url_list)
        for a in url_list:
            print(a.get('href'))
            if a.get('href') not in g_Viewed_set and a.get('href') not in g_Viewing_set:   
                g_Viewing_set.add(a.get('href')) 
                g_Url_Queue.put(a.get('href'))
        print("next over")
        #name url
        name_list = My_soup.select("meta[itemprop='description']")
        for name in name_list:
            logger_name.info(name.get('content'))
        print("name over")
        g_Viewed_set.add(current_url)
        mutex.release()

    return False


#本地目录
picDir = os.path.abspath('.')
picDir = os.path.join(picDir, 'picDir')
#picture number
picno = 0
#定义线程爬取网址
logger_debug.info('开始爬虫了')
#建立一个永久会话
my_session = requests.session()
#定义初始网址
initial_page = "http://wufazhuce.com/one/1293"
#定义一个伪装成浏览器的头
my_header = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
#使用get方法发生请求
#result_get = my_session.get(initial_page)

#向爬取的队列插入url
g_Url_Queue.put(initial_page)
#向将要爬取的集合插入url,求并集 (I use |= to put data into set)
g_Viewing_set.add(initial_page) 
#使用线程爬取所有url，并将爬到的url放到队列
g_threadPool = threadpool.ThreadPool(10)
#python2 is xrange, python3 is range
#for i in range(1,10):
for i in range(10):
    create_thread = threading.Thread(target=ParseUrl, args=(g_Url_Queue,g_Viewed_set,g_Viewing_set))
    create_thread.start()
    create_thread.join()
    
logger_debug.info("爬取url完成，共爬取到了%d个Url")
#逐个分析队列中的url

#
