import os
import ssl
import urllib
from urllib import request

import requests
from tqdm import tqdm

from utils.util import getRootPath

ssl._create_default_https_context = ssl._create_unverified_context

headers = {"CF-RAY": "3f9ebe38d2f8999d-LAX",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Content-Type": "video/mp4",
           "Content-Range": "bytes 5455561-5455561/32348253",
           "ETag": "\"894a0b45896d31:0\"",
           "Accept-Ranges": "bytes 0-77546066/77546067",
           "Accept-Encoding": "gzip, deflate, sdch",
           "Cookie": "__cfduid=d8d782c35207cce70f5cf3c5bd9fd60c21520696001; __guid=95667230.1894906878969241600.1520778848838.0574; monitor_count=1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           }

headers_1 = {"Content-MD5": "6f/eolPekQpDVfTqCBHpWg==",
             "EagleId": "ca7f4c8115208313809688788e",
             "ETag": "\"E9FFDEA253DE910A4355F4EA0811E95A\"",
             "Server": "Tengine",
             "Timing-Allow-Origin": "*",
             "Via": "cache12.l2cm12[98,206-0,H], cache14.l2cm12[101,0], cache32.l2sg1[0,206-0,H], cache15.l2sg1[1,0], cache3.hk1[0,206-0,H], cache11.hk1[,0]",
             "X-Cache": "HIT TCP_MEM_HIT dirn:-2:-2 mlen:0",
             "x-oss-hash-crc64ecma": "3687040222160165818",
             "x-oss-object-type": "Normal",
             "x-oss-request-id": "5AA60B8DA1A55C396EBBC19E",
             "x-oss-server-time": "65", "x-oss-storage-class": "Standard",
             "X-Swift-CacheTime": "604800",
             "X-Swift-SaveTime": "Mon, 12 Mar 2018 05:09:37 GMT",
             "Referer": "http://video.eastday.com/a/161212025204364813630.html?qid=01359"
             }
url_name = []


def get():
    # url = 'http://akm667.inter.iqiyi.com/videos/v0/20180310/40/95/148ea8dd74cdc7bae1569c15f9a61c02.f4v?key=01694dd1185f8c366c1f81b2eb0d05271&dis_k=4018dfb10e7c339d19d1e4cbd5197dc3&dis_t=1520829914&src=iqiyi.com&uuid=793aead2-5aa605da-ed&rn=1520829913892&qd_ip=793aead2&qyid=275ff01132314db4547722bd2c3b98d2&qd_tm=1520829897735&qd_vipdyn=0&cross-domain=1&pri_idc=akm_oversea_hash&pv=0.1&qd_aid=956826900&qd_stert=0&qypid=956826900_02020031010000000000&qd_p=793aead2&qd_uid=0&qd_src=01010031010000000000&qd_index=1&qd_vip=0&qd_tvid=956826900&qd_vipres=0&qd_k=961b6f0414a1f2abded616717e73a4a1&range=8192-7166975'
    url = ''
    folder_path = getRootPath() + "video{}".format(os.sep)
    file_name = "91_d1f327803d104889af78aadd68c069fe.mp4"
    print(file_name)
    saveVideo(url, folder_path=folder_path, file_name=file_name)


# 传入文件名和video地址
def saveVideo(req_url, folder_path=None, file_name=None):
    try:
        req = urllib.request.Request(url=req_url, headers=headers)
        ''' 如果是https 去掉验证'''
        if req_url.startswith("https"):
            context = ssl._create_unverified_context()
            response = urllib.request.urlopen(req, context=context)
        else:
            response = urllib.request.urlopen(req)
        if not folder_path:
            folder_path = getRootPath() + "video" + os.sep
        file_path = folder_path + file_name
        f = open(file_path, "wb")
        f.write(response.read())
        f.close()
    except Exception as err:
        print("--> save video url:{}, failed :{}", req_url, str(err))


from urllib.request import urlopen


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """

    header = dict(headers, **headers_1)
    req = urllib.request.Request(url=url, headers=header)
    file_size = int(urllib.request.urlopen(req, timeout=60).info().get('Content-Length', -1))

    """
    print(urlopen(url).info())
    # output
    Server: AliyunOSS
    Date: Tue, 19 Dec 2017 06:55:41 GMT
    Content-Type: application/octet-stream
    Content-Length: 29771146
    Connection: close
    x-oss-request-id: 5A38B7EDCE2B804FFB1FD51C
    Accept-Ranges: bytes
    ETag: "9AA9C1783224A1536D3F1E222C9C791B-6"
    Last-Modified: Wed, 15 Nov 2017 10:38:33 GMT
    x-oss-object-type: Multipart
    x-oss-hash-crc64ecma: 14897370096125855628
    x-oss-storage-class: Standard
    x-oss-server-time: 4
    """

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size

    header = dict(header, **{"Range": "bytes=%s-%s" % (first_byte, file_size)})
    print(header)

    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=url.split('/')[-1])
    '''如果是https开头的，去调验证'''
    verify = True
    if url.startswith("https"):
        verify = False
    req = requests.get(url, headers=header, stream=True, verify=verify)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == '__main__':
    # url = "https://fs31.aipai.com/user/73/39648073/7083476/card/38885157/card.mp4?l=a"
    url = "http://mvpc.eastday.com/vshenghuo/20161212/20161212025204364813630_1_06400360.mp4"
    download_from_url(url, "./06400361.mp4")

# if __name__ == '__main__':
#     get()
