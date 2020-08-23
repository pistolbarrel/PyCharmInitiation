import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import argparse
import os
import sys



def main():
    url = 'https://www.criterionchannel.com/three-starring-jane-fonda'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    print(soup.prettify())
    table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
    for item in table.findAll('li', attrs={'class': 'js-collection-item'}):
        for str in item.stripped_strings:
            print(str)
    a = 42

if __name__ == "__main__":
    main()