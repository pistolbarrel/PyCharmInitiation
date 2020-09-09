import requests
from bs4 import BeautifulSoup
import CriterionMovieParse
import argparse


def main():
    args = process_args()
    if args.url:
        url = args.url
        series_name, description, extracted_episode_info = get_series_info(url)
        series_name = "Criterion:" + series_name
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print(series_name)
        print(description)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print()
        i = 0
        for movie in extracted_episode_info:
            i += 1
            time, url = movie
            movie_parser = CriterionMovieParse.MovieParse(url)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(i)
            print(time)
            print(series_name)
            movie_parser.print_info(time)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print()
            print()

    a = 42


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    return args


def get_series_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    series_name, description = extract_series_name_and_description(soup)
    series = extract_episode_time_and_url(soup)
    return series_name, description, series


def extract_series_name_and_description(soup):
    ret_str = []
    table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
    for string in table.stripped_strings:
        ret_str.append(string)
    return ret_str[0], ret_str[2]


def extract_episode_time_and_url(soup):
    series = []
    table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = [item.a.text.strip(), item.a['href']]
        series.append(movie)
    return series


if __name__ == "__main__":
    main()