# coding=utf-8
import sys

# coding=utf-8

# refer to http://www.cnblogs.com/haigege/p/5492177.html
# Step1: scroll and generate Markdown format Menu

from selenium import webdriver
import time


def scroll_top(driver):
    if driver.name == "chrome":
        js = "var q=document.body.scrollTop=0"
    else:
        js = "var q=document.documentElement.scrollTop=0"
    return driver.execute_script(js)


# 拉到底部
def scroll_foot(driver):
    if driver.name == "chrome":
        js = "var q=document.body.scrollTop=2000"
    else:
        js = "var q=document.documentElement.scrollTop=2000"
    return driver.execute_script(js)


def write_text(filename, info):
    """
    :param info: 要写入txt的文本内容
    :return: none
    """
    # 创建/打开info.txt文件，并写入内容
    with open(filename, 'w') as fp:
        fp.write(info)
        fp.write('\n')


def sroll_multi(driver, times=5, loopsleep=2):
    # 40 titles about 3 times
    for i in range(times):
        time.sleep(loopsleep)
        print("Scroll foot %s time..." % i)
        scroll_foot(driver)
    time.sleep(loopsleep)


# Note: titles is titles_WebElement type object
def write_menu(filename, titles):
    with open(filename, 'w') as fp:
        pass
    for title in titles:
        if r'目录' not in title.text:
            print("[" + title.text + "](" + title.get_attribute("href") + ")")
            t = title.text
            t = title.text.replace(":", "：")
            t = title.text.replace("|", "丨")
            t = title.text
            write_text(filename, "[" + t + "](" + title.get_attribute("href") + ")")
            # assert type(title) == "WebElement"
            # print type(title)


def main(url):
    # eg. <a class="title" href="/p/6f543f43aaec" target="_blank"> titleXXX</a>
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    # driver.maximize_window()
    driver.get(url)
    sroll_multi(driver)
    titles = driver.find_elements_by_xpath('.//a[@class="title"]|.//a[target="_blank"]')
    write_menu(filename, titles)


if __name__ == '__main__':
    # sample link
    url = 'http://www.jianshu.com/u/73632348f37a'
    filename = r'info.txt'
    main(url)
