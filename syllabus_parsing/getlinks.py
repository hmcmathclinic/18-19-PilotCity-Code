from bs4 import BeautifulSoup, SoupStrainer
import re as re
from urllib.request import urlopen


def getLinks(url):
    links = []
    html = urlopen(url)
    bsObj = BeautifulSoup(html.read(), "lxml")
    for link in bsObj.find_all('a'):
        href = link.get('href')
        if href and ("http://" in href or "https://" in href):
            links.append(href)
    return links


def retrieveAllSubLinks(url, depth, hset, domainName):
    if depth == 0:
        return
    else:
        links = getLinks(url)
        for link in links:
            if link not in hset and domainName in link:
                hset.add(link)
                retrieveAllSubLinks(link, depth - 1, hset, domainName)  