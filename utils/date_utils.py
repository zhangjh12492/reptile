import time
import re
import datetime
from utils.PyLog import logger


def parse_time(dt, format_str=None):
    """
        # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        # 将"2012-03-28 06:53:40"转化为时间戳
        # s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        # return int(s)
    """
    # dt为字符串
    # 中间过程一般都需要将字符串转化为时间数组
    if format_str:
        # return time.mktime(time.strptime(dt, format_str))
        return time.strptime(dt, format_str)
    else:
        return time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))


def format_time(tm, format_str=None):
    if format_str:
        return time.strftime(format_str, tm)
    return


def sifting_date_str_stamp(date_str):
    """
    将获取到的日期转成有效的13位时间戳
    """
    try:
        if re.match(r'[0-9]+年\s\d月', "2016年 4月11日 10:30"):
            time_stamp = time.mktime(time.strptime("2016年 4月11日 10:30", '%Y年 %m月%d日 %H:%M'))
            return int(time_stamp * 1000)
        elif re.match(r'\d月', "4月11日 10:30"):
            year = format_time(time.localtime(), '%Y')
            date_str = year + "年 4月11日 10:30"
            time_stamp = time.mktime(time.strptime(date_str, '%Y年 %m月%d日 %H:%M'))
            return int(time_stamp * 1000)
        elif re.match(r'今天\d', "今天09:17"):
            date_str = format_time(time.localtime(), '%Y-%m-%d')
            date_str = date_str + " " + "今天09:17"[2:]
            time_stamp = time.mktime(time.strptime(date_str, '%Y-%m-%d %H:%M'))
            return int(time_stamp * 1000)
        elif re.match(r'\d+', "35分钟前"):
            minute = re.match(r'\d+', "35分钟前").group()
            that_time = datetime.datetime.now() + datetime.timedelta(minutes=-int(minute))
            return int(that_time.timestamp() * 1000)
    except Exception as err:
        logger.error("--> sifting real timestamp error, {} , {} ".format(date_str, str(err)))
    # 默认为当前日期
    return int(time.time() * 1000)


'''
时间测试
'''
'''
print(int(time.mktime(parse_time('2018-03-14 00:00:00', '%Y-%m-%d %H:%M:%S')) * 1000))
print(time.localtime())
print(format_time(time.localtime(), '%Y'))
date_str = '今天09:17'
print(date_str[2:])
date_str = "2016年 4月11日 10:30"
if date_str.__contains__('年'):
    time_stamp = time.mktime(time.strptime(date_str, '%Y年 %m月%d日 %H:%M'))
    print(time_stamp)
    print(time.strftime('%Y-%m-%d', time.localtime(time_stamp)))
    print(date_str)
date_str = "3月13日 22:07"
if re.match(r'[0-9]+年\s\d月', "2016年 4月11日 10:30"):
    time_stamp = time.mktime(time.strptime("2016年 4月11日 10:30", '%Y年 %m月%d日 %H:%M'))
    print("2016年 4月11日 10:30 is {}".format(time_stamp))
if re.match(r'\d月', "4月11日 10:30"):
    year = format_time(time.localtime(), '%Y')
    date_str = year + "年 4月11日 10:30"
    time_stamp = time.mktime(time.strptime(date_str, '%Y年 %m月%d日 %H:%M'))
    print("4月11日 10:30 is {}".format(time_stamp))
if re.match(r'今天\d', "今天09:17"):
    date_str = format_time(time.localtime(), '%Y-%m-%d')
    date_str = date_str + " " + "今天09:17"[2:]
    time_stamp = time.mktime(time.strptime(date_str, '%Y-%m-%d %H:%M'))
    print("今天09:17 is {}".format(time_stamp))
if re.match(r'\d+', "35分钟前"):
    minute = re.match(r'\d+', "35分钟前").group()
    print(minute)
    that_time = datetime.datetime.now() + datetime.timedelta(minutes=-int(minute))
    print("35分钟前是 : {}".format(that_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("35分钟前是 : {}".format(that_time.timestamp()))
'''

'''
comment = "评论(4)"
print(re.search(r"\d+", comment).group())
'''
