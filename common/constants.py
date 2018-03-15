from utils.util import getRootPath
import os


class ENV:
    LOCAL = "local"
    TEST = "test"
    PROD = "prod"
    MYSQL_CONF_TYPE = 'mysqld'
    MYSQL_FILE_TYPE = "mysql"
    MYSQL_CHARSET = "utf8"


global_consts = {
    # "sina_bussiness": "https://www.cnblogs.com/luxiaojun/p/6144748.html",
    "sina_bussiness": "http://finance.sina.com.cn/stock/newstock/",
    # "sina_bussiness": "http://finance.sina.com.cn/",
    # "sina_bussiness": "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%8A%96%E9%9F%B3%E8%A7%86%E9%A2%91&oq=%25E6%258A%2596%25E9%259F%25B3&rsv_pq=f6e740ae00000c54&rsv_t=09222CYySRgUIaDf5TO0H1kHaPgRYC%2BfiEz7Mm60FLHiEfa04L8wgl5rd6o&rqlang=cn&rsv_enter=1&inputT=845&rsv_sug3=27&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&rsv_sug4=1529",
    "sina_bs_folder": getRootPath() + "content{}sina{}stock{}newstock{}".format(os.sep, os.sep, os.sep, os.sep),
    "sina_bs_file_name": "newstock_content.txt",
    "sina_bs_html_name": "newstock_content.html",
    "sina_module": {"10000": "新股滚动新闻", "10001": "最新动态", "10002": "新股评论",
                    "10003": "IPO中介", "10004": "PE动态", "10005": "新三板"},
    "headers": {"CF-RAY": "3f9ebe38d2f8999d-LAX",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Content-Type": "video/mp4",
                "Content-Range": "bytes 5455561-5455561/32348253",
                "ETag": "\"894a0b45896d31:0\"",
                "Accept-Ranges": "bytes 0-77546066/77546067",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Cookie": "__cfduid=d8d782c35207cce70f5cf3c5bd9fd60c21520696001; __guid=95667230.1894906878969241600.1520778848838.0574; monitor_count=1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                },
    "headers_1": {"Content-MD5": "6f/eolPekQpDVfTqCBHpWg==",
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
                  },
    "dev": ENV.LOCAL
}
