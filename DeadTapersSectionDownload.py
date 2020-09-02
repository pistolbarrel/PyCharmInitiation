import re
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
import argparse
import os


def extract_urls(soup):
    urls = []
    g_table = soup.find('div', attrs={'class': 'node__content'})
    for row in g_table.findAll('div', attrs={'class': 'field--type-text-with-summary'}):
        for cont in row.contents:
            url = extract_url(cont)
            if url:
                urls.append(url)
                continue
            for c2 in cont:
                url = extract_url(c2)
                if url:
                    urls.append(url)
                    break
                continue
    return urls


def extract_description(soup, output_text):
    g_table = soup.find('div', attrs={'class': 'node__content'})
    for row in g_table.findAll('div', attrs={'class': 'field--type-text-with-summary'}):
        txt = row.text
        output_text += txt + '\n\n'
        print(txt)
        print()
        strings = txt.split('\n')
        for string in strings:
            # matches mm/dd/yy
            match = re.search(r'(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d\d', string)
            if match:
                sub_string = string[match.start(): match.start() + 50]
                output_text += sub_string + '\n'
                print(sub_string)
        output_text += '\n'
        print()
        return output_text


def extract_submission_date(soup, output_text):
    g_table = soup.find('div', attrs={'class': 'node__submitted'})
    for row in g_table.findAll('span',
                               attrs={'class': 'field field--name-created field--type-created field--label-hidden'}):
        txt = row.text
        # matches mm/dd/yyyy
        match = re.search(r'(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/([0-9][0-9][0-9][0-9])', txt)
        output_text += match.group() + '\n'
        print(match.group())
        return match.group(), output_text


def extract_url(cont):
    try:
        if 'onclick' in cont.attrs:
            url_str = cont['onclick']
            s2 = url_str.split('url=')[1]
            s3 = s2.split('&title')[0]
            return s3
    except AttributeError:
        pass


def convert_date_to_yyyyddmm(date_str, delim):
    dt = parse(date_str)
    return dt.strftime('%Y' + delim + '%m' + delim + '%d')


def filename_from_url(url):
    parts = url.split('/')
    return parts[-1]


def download_single_file(source, target):
    resp = requests.get(source, verify=False)

    with open(target, "wb") as f:
        f.write(resp.content)


def create_change_to_dl_directory(original_dir, sub_date):
    converted_date = convert_date_to_yyyyddmm(sub_date, '-')
    new = os.path.join(original_dir, converted_date)
    os.makedirs(new, exist_ok=True)
    os.chdir(new)
    return new


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    parser.add_argument("-n", "--no_download", help="Skip the download", action='store_false')
    return parser.parse_args()


def download_files(args, sub_date, urls, output_text):
    original_dir = os.getcwd()
    create_change_to_dl_directory(original_dir, sub_date)
    for dl_url in urls:
        out_string = dl_url + ' ==> ' + os.path.join(os.getcwd(), filename_from_url(dl_url))
        output_text += out_string + '\n'
        print(out_string)
        if args.no_download:
            print('Downloading......')
            download_single_file(dl_url, filename_from_url(dl_url))
    with open('TapersSection' + convert_date_to_yyyyddmm(sub_date, '-') + '.txt', 'w') as f:
        f.write(output_text)
    os.chdir(original_dir)


def main():
    output_text = ''
    args = process_args()
    if args.url:
        url = args.url
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    sub_date, output_text = extract_submission_date(soup, output_text)
    output_text = extract_description(soup, output_text)

    urls = extract_urls(soup)
    download_files(args, sub_date, urls, output_text)

    print('DONE')


if __name__ == "__main__":
    main()