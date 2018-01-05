import queue 
import requests #引入网页请求
import os  #引入os命令
import logging
import threading #引入线程

class Consumer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        while 1:
            try:
                queue.pop()
                print("Consumer: %s get a product" % self.name)
                time.sleep(2)
            except:
                print("Queue is empty!")
                time.sleep(2)
                print("Consumer: %s sleep 2 seconds" % self.name)
