import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import argparse
import os
import sys

def extract_description(soup):
    GDtable = soup.find('div', attrs={'class': 'node__content'})
    for row in GDtable.findAll("div", attrs={'class': 'field--type-text-with-summary'}):
        return row.text


def extract_item(soup, field_name):
    gDJamtable = soup.find('div', attrs={'class': field_name})
    for item in gDJamtable.findAll("div", attrs={'class': 'field__item'}):
        return item.text


def convertDateToDDMMYY(dateStr, delim):
    dt = parse(dateStr)
    return dt.strftime('%m'+delim+'%d'+delim+'%y')


def mungeDate(date):
    parts = date.split('-')
    return parts[0] + parts[1][2:]


def filenamefromurl(url):
    parts = url.split('/')
    return parts[-1]


def download(source, target):
    resp = requests.get(source, verify=False)

    f = open(target, "wb")
    f.write(resp.content)
    f.close()


def main():
    usageDesc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usageDesc)
    parser.add_argument("-u", "--url", help="URL to parse")
    parser.add_argument("-n", "--no_download", help="Skip the download")
    args = parser.parse_args()
    if args.url:
        url = args.url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    info = {}
    info['desc'] = extract_description(soup)
    info['date'] = extract_item(soup, 'field--name-field-jam-date')
    info['date_simple'] = convertDateToDDMMYY(info['date'], '/')
    info['city'] = extract_item(soup, 'field--name-field-jam-location')
    info['venue'] = extract_item(soup, 'field--name-field-jam-venue')
    info['url'] = extract_item(soup, 'field--name-field-streamos-mp3-url')
    info['feat_date'] = extract_item(soup, 'field--name-field-homepage-feature-title')
    info['feat_date_simple'] = convertDateToDDMMYY(mungeDate(info['feat_date']), '-')

    print(info['date_simple']+' '+info['venue']+' in '+info['city'])
    print('Grateful Dead')
    print('Good Music')
    print(info['feat_date_simple']+' - JOTW')
    print(info['desc'])
    print(info['venue'])
    print(info['date'])
    print(info['city'])

    print(info['url'])

    if not args.no_download:
        print('Downloading mp3 to:')
        print(os.getcwd()+'\\'+filenamefromurl(info['url']))
        download(info['url'], filenamefromurl(info['url']))

    print('DONE')


if __name__ == "__main__":
    main()