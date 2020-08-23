import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import argparse
import os
import sys


def extract_title_length(table):
    for item in table.findAll('div', attrs={'class': 'contain margin-top-large column small-16'}):
        return item.h1.text.strip(), item.h5.text.strip()


def extract_info(table):
    info = []
    for item in table.findAll('div', attrs={'class': 'site-font-secondary-color'}):
        for str in item.stripped_strings:
            info.append(str)
    return info
    a=42

def main():
    url = 'https://www.criterionchannel.com/videos/kramer-vs-kramer'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.prettify())
    table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})

    title, length = extract_title_length(table)
    one, two, three = extract_info(table)
    director, year, country = one.split('•')
    director = director.replace("Directed by ", "")
    title = title + " (" + year.strip() + ")"
    two = two.replace("Starring ", "")
    two = two.replace(',', ';')


    a = 42
    print(length)
    print(title)
    print(director)
    print(two)
    print()
    print(three)



if __name__ == "__main__":
    main()