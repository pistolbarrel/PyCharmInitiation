import requests
from bs4 import BeautifulSoup
import argparse


def extract_title_length(table):
    for item in table.findAll('div', attrs={'class': 'contain margin-top-large column small-16'}):
        return item.h1.text.strip(), item.h5.text.strip()


def extract_info(table):
    info = []
    for item in table.findAll('div', attrs={'class': 'site-font-secondary-color'}):
        for string in item.stripped_strings:
            info.append(string)
    return info


class MovieParse:
    def __init__(self, url):
        url = url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        self.table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})

    def print_info(self, supplied_length=None):
        diryrcnty, stars, descr, director, year = '', '', '', '', ''
        title, length = extract_title_length(self.table)
        info = extract_info(self.table)
        if len(info) == 4:
            diryrcnty, stars, descr, ex_descr = info
            director, year, country = diryrcnty.split('•')
            director = director.replace("Directed by ", "")
            stars = stars.replace("Starring ", "")
            stars = stars.replace(',', ';')
            descr = descr + '\n\n' + ex_descr
        if len(info) == 3:
            diryrcnty, stars, descr = info
            splits = diryrcnty.split('•')
            if len(splits) == 3:
                director, year, country = splits
            if len(splits) == 2:
                year, country = splits
            if director:
                director = director.replace("Directed by ", "")
            stars = stars.replace("Starring ", "")
            stars = stars.replace(',', ';')

        if len(info) == 2:
            diryrcnty, descr = info
            if '•' in diryrcnty:
                splits = diryrcnty.split('•')
                if len(splits) == 3:
                    director, year, country = splits
                if len(splits) == 2:
                    year, country = splits
                if director:
                    director = director.replace("Directed by ", "")
            else:
                descr = diryrcnty + '\n\n' + descr
        if len(info) == 1:
            descr = info[0]

        if year:
            title = title + " (" + year.strip() + ")"

        a = 42
        if not supplied_length:
            length = length.split('•')[1].strip()
            print(length)
        print(title)
        if director:
            print(director)
        if stars:
            print(stars)
        if descr:
            print()
            print(descr)


def main():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    if args.url:
        url = args.url
    r = requests.get(url)
    movie_parser = MovieParse(url)
    print('='*54)
    movie_parser.print_info()
    print('='*54)
    print()
    print()


if __name__ == "__main__":
    main()