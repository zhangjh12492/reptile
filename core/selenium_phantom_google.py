import threading
import time
import multiprocessing

import os

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from common.constants import global_consts
import json

from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from pyvirtualdisplay import Display

'''
$phantomjs -h
Usage:
   phantomjs [switchs] [options] [script] [argument [argument [...]]]

Options:
  --cookies-file=<val>                 Sets the file name to store the persistent cookies
  --config=<val>                       Specifies JSON-formatted configuration file
  --debug=<val>                        Prints additional warning and debug message: 'true' or 'false' (default)
  --disk-cache=<val>                   Enables disk cache: 'true' or 'false' (default)
  --ignore-ssl-errors=<val>            Ignores SSL errors (expired/self-signed certificate errors): 'true' or 'false' (default)
  --load-images=<val>                  Loads all inlined images: 'true' (default) or 'false'
  --local-storage-path=<val>           Specifies the location for offline local storage
  --local-storage-quota=<val>          Sets the maximum size of the offline local storage (in KB)
  --local-to-remote-url-access=<val>   Allows local content to access remote URL: 'true' or 'false' (default)
  --max-disk-cache-size=<val>          Limits the size of the disk cache (in KB)
  --output-encoding=<val>              Sets the encoding for the terminal output, default is 'utf8'
  --remote-debugger-port=<val>         Starts the script in a debug harness and listens on the specified port
  --remote-debugger-autorun=<val>      Runs the script in the debugger immediately: 'true' or 'false' (default)
  --proxy=<val>                        Sets the proxy server, e.g. '--proxy=http://proxy.company.com:8080'
  --proxy-auth=<val>                   Provides authentication information for the proxy, e.g. ''-proxy-auth=username:password'
  --proxy-type=<val>                   Specifies the proxy type, 'http' (default), 'none' (disable completely), or 'socks5'
  --script-encoding=<val>              Sets the encoding used for the starting script, default is 'utf8'
  --web-security=<val>                 Enables web security, 'true' (default) or 'false'
  --ssl-protocol=<val>                 Sets the SSL protocol (supported protocols: 'SSLv3' (default), 'SSLv2', 'TLSv1', 'any')
  --ssl-certificates-path=<val>        Sets the location for custom CA certificates (if none set, uses system default)
  --webdriver=<val>                    Starts in 'Remote WebDriver mode' (embedded GhostDriver): '[[<IP>:]<PORT>]' (default '127.0.0.1:8910')
  --webdriver-logfile=<val>            File where to write the WebDriver's Log (default 'none') (NOTE: needs '--webdriver')
  --webdriver-loglevel=<val>           WebDriver Logging Level: (supported: 'ERROR', 'WARN', 'INFO', 'DEBUG') (default 'INFO') (NOTE: needs '--webdriver')
  --webdriver-selenium-grid-hub=<val>  URL to the Selenium Grid HUB: 'URL_TO_HUB' (default 'none') (NOTE: needs '--webdriver')
  -w,--wd                              Equivalent to '--webdriver' option above
  -h,--help                            Shows this message and quits
  -v,--version                         Prints out PhantomJS version

Any of the options that accept boolean values ('true'/'false') can also accept 'yes'/'no'.

Without any argument, PhantomJS will launch in interactive mode (REPL).

Documentation can be found at the web site, http://phantomjs.org.
'''
from utils.PyLog import *


class SeleniumPhantomJs():

    def __init__(self):
        '''新闻对象'''
        self.news_objs = {}
        '''标题'''
        self.titles = []
        '''概要'''
        self.synopsis = []
        '''内容链接'''
        self.cont_href = []
        '''标签 以及'''
        self.tags = []
        self.driver = None
        self.times = []

    def openDriver(self, page=None):
        try:
            '''设置proxy'''
            '''  设置方法 一、
            proxy = Proxy({
                'proxyType': ProxyType.MANUAL,
                'httpProxy': '182.121.201.9:9999'  # 代理ip和端口
            })
            
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            
            proxy.add_to_capabilities(desired_capabilities)
            print "add proxy" + proxy.http_proxy
            
            driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
            driver.get('http://httpbin.org/ip')
            print(driver.page_source)
            '''

            ''' 设置方法二、'''
            '''
            service_args = [
                '--proxy=182.121.201.9:9999',
            ]
            driver = webdriver.PhantomJS(service_args=service_args)
            driver.get('http://httpbin.org/ip')
            print driver.page_source
            driver.close()
            '''
            # display = Display(visible=0, size=(800, 600))
            # display.start()

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            prefs = {"profile.managed_default_content_settings.images": 2}  # not load image
            options.add_experimental_option("prefs", prefs)

            options.add_argument('lang=zh_CN.UTF-8')
            options.add_argument(
                'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
            url = global_consts['sina_bussiness']
            self.driver = webdriver.Chrome(chrome_options=options)
            # self.driver.set_window_size(1360, 5500)
            logger.info("--> get driver start : {}".format(page))
            self.driver.get(url)
            # self.driver.set_page_load_timeout(20)
            logger.info("--> get driver success : {}".format(page))
        except Exception as err:
            logger.error("--> driver connect time out : {}".format(page), err)
            self.driver.quit()

    def fillContentFromHtml(self):
        ''' 拉取html中的主要信息 '''
        try:
            feedCardContent = self.driver.find_element_by_id('feedCardContent')
            feed_card_item = feedCardContent.find_element_by_xpath('//*[@id="feedCardContent"]/div[7]'). \
                find_elements_by_tag_name("div")
            for card_item in feed_card_item:
                # print(card_item.get_attribute("innerHTML"))
                if card_item.get_attribute("class") == 'feed-card-item':
                    # print(card_item.get_attribute("class"))
                    h2 = card_item.find_element_by_tag_name("h2").find_element_by_tag_name("a")
                    self.titles.append(h2.text)
                    feed_card_txt = card_item.find_element_by_tag_name("div").find_element_by_tag_name("div"). \
                        find_element_by_tag_name('a')
                    self.synopsis.append(feed_card_txt.text)
                    self.cont_href.append(feed_card_txt.get_attribute("href"))
                    # 发布时间
                    feed_card_time = card_item.find_element_by_class_name("feed-card-time")
                    if feed_card_time:
                        self.times.append(feed_card_time.text)

                    # 标签
                    feed_card_tags = card_item.find_element_by_class_name("feed-card-tags")
                    __tags = []
                    if feed_card_tags:
                        tagsA = feed_card_tags.find_elements_by_tag_name("a")
                        for A in tagsA:
                            __tags.append({A.get_attribute("href"), A.text})

                    # 评论
                    feed_card_actions = card_item.find_element_by_class_name("feed-card-actions")
                    if feed_card_actions:
                        comment = feed_card_actions.find_element_by_tag_name("a").text
                    news_obj = {feed_card_txt.get_attribute("href"): {"title": h2.text, "synopsis": feed_card_txt.text,
                                                                      "href": feed_card_txt.get_attribute("href"),
                                                                      "create_time": feed_card_time.text,
                                                                      "tags": __tags, "comment": comment}}
                    logger.info("--> type : {} , news_obj : ".format(type(news_obj), str(news_obj)))
                    self.news_objs = dict(self.news_objs, **news_obj)
                    logger.info("--> type : {}, self.news_obj : {}".format(type(self.news_objs), str(self.news_objs)))

        except Exception as err:
            logger.error("--> parse html error, ", err)

    def getNextPageContent(self, sleepTime=9):
        """获取下一页的数据"""
        try:
            feedCardPage = self.driver.find_element_by_class_name('pagebox_next')
            if feedCardPage:
                nextPage = feedCardPage.find_element_by_tag_name("a")
                print("--> start next page {}".format(nextPage.text))
                nextPage.click()
                time.sleep(sleepTime)
                return True
            else:
                logger.info("--> no next page!")
                return False
        except Exception as err:
            logger.error(err)
            return False

    def setCurrentPage(self, pageNo):
        currentPage = self.driver.find_element_by_class_name('pagebox_num')
        js = 'document.getElementsByClassName("pagebox_num")[0].setAttribute("data-page",{})'.format(pageNo)
        self.driver.execute_script(js)
        currentPage.find_element_by_tag_name("a").click()
        time.sleep(4)

    def beddingNextPage(self, count=3):
        for i in range(0, count):
            self.scroll()
            time.sleep(6)

    def scroll(self, scrollTop=4000):
        self.driver.execute_script("window.scrollBy(0,{})".format(scrollTop))

    def close_driver(self):
        self.driver.quit()


def multi_process(page):
    seleniumPhantomJs = SeleniumPhantomJs()
    try:
        time.sleep(1)
        logger.info("--> step 1, open driver " + str(page))
        seleniumPhantomJs.openDriver(page)
        logger.info("--> step 2, bedding next page " + str(page))
        seleniumPhantomJs.beddingNextPage()
        logger.info("--> step 3, set current page " + str(page))
        seleniumPhantomJs.setCurrentPage(page)
        logger.info("--> step 4, bedding next page " + str(page))
        seleniumPhantomJs.beddingNextPage()
        logger.info("--> step 5, save img " + str(page))
        seleniumPhantomJs.driver.save_screenshot("./imgs/{}.png".format(page + 1))
        logger.info("--> step 6, fill content from html " + str(page))
        seleniumPhantomJs.fillContentFromHtml()
        logger.info("--> step 7, start close driver :{}".format(page))
        logger.info(
            "--> type :{} result : {}".format(type(seleniumPhantomJs.news_objs), str(seleniumPhantomJs.news_objs)))
        result = json.dumps(seleniumPhantomJs.news_objs, default=set_default)
        seleniumPhantomJs.close_driver()
        logger.info("--> step 8, close driver success : {}".format(page))
    except Exception as err:
        seleniumPhantomJs.driver.quit()
        logger.error("--> exec error, ", err)

    file_path = global_consts["sina_bs_folder"] + "20180313{}{}.txt".format(os.sep, page + 1)
    try:
        file = open(file_path, 'w')
        file.write(result + "\n")
        file.close()
    except Exception as err:
        file.close()
        logger.error("--> write file failed , file : {}, {}".format(file_path, str(err)), err)
    return True

    # nextPage = seleniumPhantomJs.getNextPageContent()
    # for j in range(0, 4):
    #     if not nextPage:
    #         seleniumPhantomJs.beddingNextPage(2)
    #         nextPage = seleniumPhantomJs.getNextPageContent()
    #     else:
    #         break


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def loadContent(page):
    file_path = global_consts["sina_bs_folder"] + "20180313{}{}.txt".format(os.sep, page + 1)
    file = open(file_path, 'r')
    str = file.read()
    logger.info("--> result : " + json.loads(str))
    return json.loads(str)


if __name__ == '__main__':
    '''
        for i in range(0, 210):
            multi_process(page=i)
    '''


    results = []
    for i in range(1, 50):
        # 多进程代码开了16个进程
        pool = multiprocessing.Pool(processes=6)
        for index in range(0 + (i - 1) * 4, i * 4):
            logger.info("--> 当前页 : {}".format(index))
            results.append(pool.apply_async(multi_process, (index,)))
        pool.close()
        pool.join()
        time.sleep(7)

    for i in range(results.__len__()):
        print("--> 执行结果, {} : {}".format(i, results[i].get()))
    ''''''

    '''
    file_names = os.listdir(global_consts["sina_bs_folder"] + "20180313")
    print(file_names)
    for f in file_names:
        file_path = global_consts["sina_bs_folder"] + "20180313{}{}".format(os.sep, f)
        file = open(file_path, 'r')
        try:
            ss = file.read()
            file.close()
            if ss and json.loads(ss).__len__() > 0:
                logger.info("{}  ".format(ss))
        except Exception as err:
            logger.error("--> get file error, {}, ".format(file_path, err))
        finally:
            file.close()
    '''
