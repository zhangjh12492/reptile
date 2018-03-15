from lxml import html, etree
import requests
from bs4 import BeautifulSoup


def read_html():
    page = requests.get("https://movie.douban.com/top250")
    bfs = BeautifulSoup(page.text, "html.parser")
    grid_view = bfs.find("ol", class_="grid_view")
    titles = []
    averages = []
    evals = []
    for li in grid_view.children:
        try:
            hd = li.find("div", class_="hd")
            title = hd.span.contents[0]
            titles.append(title)
        except Exception as err:
            print(err)
        try:
            bd = li.find("div", class_="bd")
            star = bd.find("div", class_="star").find_all('span')
            eval_ = star[1].contents[0]
            average = star[3].contents[0]
            averages.append(average)
            evals.append(eval_)
        except Exception as err:
            print(err)

        # title = hd.a.span.content
        # titles.append(title)
        # li.find("")
        # print(li)
        # print()
        print("=========================111111111111111111============================")
        print("=========================22222222222222222============================")
    print(titles)
    print(averages)
    print(evals)


if __name__ == '__main__':
    read_html()
