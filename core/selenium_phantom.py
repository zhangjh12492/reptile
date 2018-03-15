from selenium import webdriver
from common.constants import global_consts
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

params = DesiredCapabilities.PHANTOMJS  # 这本身是一个dict格式类属性
params['phantomjs.page.settings.userAgent'] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")

news_obj = {}
titles = []
synopsis = []
cont_href = []
tags = []

phantomExePath = "C:\custom_program\python3_6_1\Scripts\phantomjs.exe"
# phantomExePath = "E:\chromedriver\chromedriver.exe"
driver = webdriver.PhantomJS()
driver.maximize_window()  # 设置全屏
# driver.set_window_size('1380', '900')
url = global_consts['sina_bussiness']
driver.get(url)  # 加载网页
''' 此处可用，使用window.scrollBy()'''
js = "window.scrollBy(0,3000)"
driver.execute_script(js)
time.sleep(8)
driver.save_screenshot('1.png')  # 截图保存

feedCardContent = driver.find_element_by_id('feedCardContent')
feed_card_item = feedCardContent.find_element_by_xpath('//*[@id="feedCardContent"]/div[7]'). \
    find_elements_by_tag_name("div")
for card_item in feed_card_item:
    # print(card_item.get_attribute("innerHTML"))
    if card_item.get_attribute("class") == 'feed-card-item':
        print(card_item.get_attribute("class"))
        h2 = card_item.find_element_by_tag_name("h2").find_element_by_tag_name("a")
        titles.append(h2.text)
        feed_card_txt = card_item.find_element_by_tag_name("div").find_element_by_tag_name("div"). \
            find_element_by_tag_name('a')
        synopsis.append(feed_card_txt.text)
        cont_href.append(feed_card_txt.get_attribute("href"))
        news_obj[feed_card_txt.get_attribute("href")] = {"title": h2.text, "synopsis": feed_card_txt.text,
                                                         "href": feed_card_txt.get_attribute("href")}


feed_card_item_1 = feedCardContent.find_element_by_xpath('//*[@id="feedCardContent"]/div[7]/div[11]')
print()
print("=============")
driver.quit()

import json

print(titles)
print(cont_href)
print(synopsis)
print(json.dumps(news_obj))
