import requests
from common.constants import global_consts
from bs4 import BeautifulSoup

class StockInfo():

    def get_newstock(self, url, headers=None, proxies=None):
        page = requests.get(url=r"" + url, headers=headers, proxies=proxies)
        return page


if __name__ == "__main__":
    stockInfo = StockInfo()
    headers = dict(global_consts['headers'], **global_consts['headers_1'])
    result = stockInfo.get_newstock(global_consts['sina_bussiness'], headers)
    if result.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(result.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = result.apparent_encoding
    encode_content = result.content.decode(encoding, 'replace').encode('utf-8', 'replace')
    print(str(result.content, encoding="utf-8"))
    # print(result.text)
    print(result.encoding)
    page = BeautifulSoup(result.text, "html.parser")
    file = open(global_consts['sina_bs_folder'] + global_consts['sina_bs_html_name'], 'w', encoding='utf-8')
    file.write(result.text)
    print(page.find(id='feedCardContent'))
