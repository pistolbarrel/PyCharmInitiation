import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import argparse
import os


def extract_description(soup):
    GDtable = soup.find('div', attrs={'class': 'node__content'})
    for row in GDtable.findAll("div", attrs={'class': 'field--type-text-with-summary'}):
        return row.text


def extract_url(soup):
    GDtable = soup.find('div', attrs={'class': 'node__content'})
    for row in GDtable.findAll("div", attrs={'class': 'field--type-text-with-summary'}):
        url_string = str(row.contents[2])
        start = url_string.find("https:")
        stop = url_string.find(".mp3") + 4
        return url_string[start:stop]

def extract_item(soup, field_name):
#    print(soup.prettify())
    gDJamtable = soup.find('div', attrs={'class': field_name})
    if field_name == 'field--name-field-homepage-feature-title' and gDJamtable is None:
        gDJamtable = soup.find('div', attrs={'class': 'views-field views-field-nothing-3'})
        for item in gDJamtable.findAll("div", attrs={'class': 'custom-title'}):
            return item.text
    if field_name == 'field--name-field-streamos-mp3-url' and gDJamtable is None:
        gDJamtable = soup.find('div', attrs={'class': 'field--name-field-amazon-s3-mp3-url'})
        for item in gDJamtable.findAll("div", attrs={'class': 'custom-title'}):
            return item.text
    for item in gDJamtable.findAll("div", attrs={'class': 'field__item'}):
        return item.text


def extract_feature_date(soup, field_name):
    gDJamtable = soup.find('div', attrs={'class': field_name})
    for item in gDJamtable.findAll("div", attrs={'class': 'custom-title'}):
        return item.text


def date_to_ddmmyy(date_str, delim):
    dt = parse(date_str)
    return dt.strftime('%m' + delim + '%d' + delim + '%y')


def date_to_ddmmyyyy(date_str, delim):
    # will leave out left zero in month and day
    dt = parse(date_str)
    return dt.strftime('%#m' + delim + '%#d' + delim + '%Y')


def date_to_yyyyddmm(date_str, delim):
    dt = parse(date_str)
    return dt.strftime('%Y' + delim + '%m' + delim + '%d')


def date_range_to_start_date(date):
    parts = date.split('-')
    return parts[0] + ',' + parts[1][-5:]


def filename_from_url(url):
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
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-n", "--no_download", help="Skip the download", action='store_false')
    args = parser.parse_args()
    if args.url:
        url = args.url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    info = {}
    info['desc'] = extract_description(soup)
    info['date'] = extract_item(soup, 'field--name-field-jam-date')
    info['date_simple'] = date_to_ddmmyy(info['date'], '/')
    info['city'] = extract_item(soup, 'field--name-field-jam-location')
    info['venue'] = extract_item(soup, 'field--name-field-jam-venue')
    info['url'] = extract_url(soup)
    info['feat_date'] = extract_item(soup, 'field--name-field-homepage-feature-title')
    info['feat_date_simple'] = date_to_ddmmyyyy(date_range_to_start_date(info['feat_date']), '/')
    info['feat_date_complex'] = date_to_yyyyddmm(date_range_to_start_date(info['feat_date']), '-')

    print(info['date_simple']+' '+info['venue']+' in '+info['city'])
    print('Grateful Dead')
    print('Good Music')
    print(info['feat_date_complex']+' - JOTW')
    print(info['feat_date_simple'])
    print(info['desc'])
    print(info['venue'])
    print(info['date'])
    print(info['city'])

    print(info['url'])

    if args.no_download:
        print('Downloading mp3 to:')
        print(os.getcwd() + '\\' + filename_from_url(info['url']))
        download(info['url'], filename_from_url(info['url']))

    print('DONE')


if __name__ == "__main__":
    main()