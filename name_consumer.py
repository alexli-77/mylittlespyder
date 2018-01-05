import queue 
import requests #引入网页请求
import os  #引入os命令
import logging
import time
import threading #引入线程
from logger import logger_name
from logger import logger_debug
#mutex = threading.RLock()

class nameconsumer(threading.Thread):
	def __init__(self, name, queue, mutex):
		threading.Thread.__init__(self)
		self.name = name
		self.data = queue
		self.mutex = mutex
	#在Python的解释器内部，当我们调用x.deal_name_task()时，实际上Python解释成nameconsumer.deal_name_task(t)，也就是说把self替换成类的实例。
	def run(self):
		while True:
			while self.data.qsize() > 0:
				self.mutex.acquire()
				print("--------1111111111-------")
				name = self.data.get()
				logger_name.info(name)
				logger_debug.info("name: ---" + name)
				self.mutex.release()
			time.sleep(1)
		