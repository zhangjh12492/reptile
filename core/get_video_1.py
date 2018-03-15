import urllib
import re
from tkinter import Image
from urllib import request
import os
import random

import time

import sys

from utils.util import getRootPath
import requests
from bs4 import BeautifulSoup
import multiprocessing
from contextlib import closing
from tqdm import tqdm
import requests
import progressbar
import requests.packages.urllib3

save_path="./news1.mp4"
url = "https://dns.63mimi.com/20180126/10/1/xml/91_d1f327803d104889af78aadd68c069fe.mp4"
response = requests.request("GET", url, stream=True, data=None, headers=None)

total_length = int(response.headers.get("Content-Length"))
with open(save_path, 'wb') as f:
    # widgets = ['Processed: ', progressbar.Counter(), ' lines (', progressbar.Timer(), ')']
    # pbar = progressbar.ProgressBar(widgets=widgets)
    # for chunk in pbar((i for i in response.iter_content(chunk_size=1))):
    #     if chunk:
    #         f.write(chunk)
    #         f.flush()

    widgets = ['Progress: ', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
    for chunk in response.iter_content(chunk_size=1):
        if chunk:
            f.write(chunk)
            f.flush()
        pbar.update(len(chunk) + 1)
    pbar.finish()

# url = "https://dns.63mimi.com/20180126/10/1/xml/91_d1f327803d104889af78aadd68c069fe.mp4"
# urllib.request.urlretrieve(url, filename="./news1.mp4")
