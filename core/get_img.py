import urllib
from tkinter import Image
from urllib import request
import os
import random

import time

from utils.util import getRootPath
import requests
from bs4 import BeautifulSoup
import multiprocessing

# def save_img_request():

img_hinge_folder = "hanjiakeji"

headers = {"CF-RAY": "3f9ebe38d2f8999d-LAX",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, sdch",
           "Cookie": "__cfduid=d8d782c35207cce70f5cf3c5bd9fd60c21520696001; __guid=95667230.1894906878969241600.1520778848838.0574; monitor_count=1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}


def save_img_urllib(file_url, folder_path=None, file_name=None):
    try:
        req = urllib.request.Request(url=file_url,
                                     headers=headers)
        response = urllib.request.urlopen(req, timeout=60)
        if not folder_path:
            folder_path = getRootPath() + "imgs" + os.sep + "s5.img26" + os.sep
        file_path = folder_path + file_name
        f = open(file_path, "wb")
        f.write(response.read())
        f.close()
    except Exception as err:
        print("--> save img url:{}, failed :{}", file_url, str(err))


def save_img_requests(file_url, folder_path=None, file_name=None):
    try:
        req = requests.get(url=file_url, headers=headers, timeout=90)
        response = urllib.request.urlopen(req, timeout=60)
        if not folder_path:
            folder_path = getRootPath() + "imgs" + os.sep + "s5.img26" + os.sep
        file_path = folder_path + file_name
        f = open(file_path, "wb")
        f.write(response.read())
        f.close()
    except Exception as err:
        print("--> save img url:{}, failed :{}", file_url, str(err))


def get_99smg_imgs(index=None):
    print("--> start {}".format(index))
    folder_path = getRootPath() + "imgs{}{}{}{}{}".format(os.sep, img_hinge_folder, os.sep, index, os.sep)

    # page = requests.get("http://www.99smg.com/html/article/2018-3/index19995.html")
    url = "http://www.hanjiakeji.com/html/article/index{}.html".format(index)
    page = requests.get(url)
    bfs = BeautifulSoup(page.text, "html.parser")
    grid_view = bfs.find_all("img")
    print("img size : {}, url :{}".format(str(grid_view.__len__()), url))
    if grid_view.__len__() == 0:
        print("{} is null".format(index))
        return
    if not create_folder(folder_path):
        print("{} 已经存在，不需要重新拉取".format(folder_path))
        return
    for img in grid_view:
        src = img['src']
        srcs = src.split("/")
        img_name = srcs[srcs.__len__() - 1]
        file_path = folder_path + img_name
        print(file_path)
        save_img_urllib(src, folder_path=folder_path, file_name=img_name)


def create_folder(path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + "创建成功")
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def multi_get_imgs():
    for i in range(1, 600):
        # 多进程代码开了16个进程
        pool = multiprocessing.Pool(processes=16)
        results = []
        for index in range(19700 + (i - 1) * 10, 19600 + i * 10):
            results.append(pool.apply_async(get_99smg_imgs, (index,)))
        # for i in range(len(proxies)):
        # results[i].get()
        pool.close()
        pool.join()


def func_with_return(msg):
    print("*msg: ", msg)
    time.sleep(3)
    print("*end")
    return "{} return".format(msg)


def iqiyi_video():
    url = "http://www.iqiyi.com/w_19rwdzlq6d.html#vfrm=3-17-5-1&curid=10927991209_7f0601742e8c8ffee04e4eb4f6f5fb29"
    page = requests.get(url, headers=headers)
    print(page.text)


# if __name__ == "__main__":
#     # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#     pool = multiprocessing.Pool(processes=3)
#     results = []
#     for i in range(10):
#         msg = "hello [{}]".format(i)
#         res = pool.apply_async(func_with_return, (msg,))  # 异步开启进程, 非阻塞型, 能够向池中添加进程而不等待其执行完毕就能再次执行循环
#         results.append(res)
#
#     print("--" * 10)
#     pool.close()  # 关闭pool, 则不会有新的进程添加进去
#     pool.join()  # 必须在join之前close, 然后join等待pool中所有的线程执行完毕
#     print("All process done.")
#
#     print("Return results: ")
#     for i in results:
#         print(i.get())  # 获得进程的执行结果

if __name__ == '__main__':
    # multi_get_imgs()
    iqiyi_video()
