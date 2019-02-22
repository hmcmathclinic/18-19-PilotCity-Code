# coding: utf-8
from time import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selectolax.parser import HTMLParser
import re

# https://rushter.com/blog/python-fast-html-parser/
def get_text_bs(html):
    tree = BeautifulSoup(urlopen(html), 'lxml')

    body = tree.body
    if body is None:
        return None

    for tag in body.select('script'):
        tag.decompose()
    for tag in body.select('style'):
        tag.decompose()

    text = body.get_text()
    print(re.sub('[\n\t\r+]', '', text))

    return text

html = 'https://www.hmc.edu/summer-session/'
get_text_bs(html)

# from lxml import etree
# import requests
# from bs4 import BeautifulSoup

# page = requests.get("https://aus-alamedausd-ca.schoolloop.com/")
# soup = BeautifulSoup(page.content, 'html.parser')
# all_text = soup.find_all('p')
# for text in all_text:
# 	print(text.get_text())

