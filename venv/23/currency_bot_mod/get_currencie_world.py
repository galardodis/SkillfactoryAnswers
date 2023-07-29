import requests
import lxml.html
from bs4 import BeautifulSoup
import text


def get_currencie():
    currencie = {}
    html = requests.get(text.url_wiki).content
    tree = lxml.html.document_fromstring(html)
    root = BeautifulSoup(html, 'html.parser')
    el = root.find('tbody').find_all('tr')
    count = 0
    while count <= len(el):
        xpath1 = f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{count}]/td[2]/a'
        xpath2 = f'/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[{count}]/td[7]'
        title_name = tree.xpath(f'{xpath1}/text()')
        title_code = tree.xpath(f'{xpath2}/text()')
        if title_code:
            title_code = title_code[0].rstrip()
        else:
            count += 1
            continue
        if len(title_name) == 1:
            title_name = title_name[0]
        if len(title_name) == 2:
            title_name = title_name[1].strip('()')
            title_name = title_name.replace(title_name[0], title_name[0].title(), 1)
        count += 1
        if title_code in currencie.values():
            continue
        else:
            currencie[title_name] = title_code
    return currencie
