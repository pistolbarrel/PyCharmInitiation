import requests
from bs4 import BeautifulSoup
import argparse
import CriterionMovieParse


def extract_series_name_and_description(soup):
    ret_str = []
    table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
    for string in table.stripped_strings:
        ret_str.append(string)
    return ret_str[0], ret_str[2]


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    return args


def extract_collection_title_feature(soup):
    ret = []
    table = soup.find('li', attrs={'class': 'js-collection-item'})
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = [item.a.text.strip(), item.a['href']]
        ret.append(movie)
    return ret


def extract_episode_time_and_url(soup):
    ret = []
    table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = [item.a.text.strip(), item.a['href']]
        ret.append(movie)
    return ret


def get_collection_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    series_name, not_used = extract_series_name_and_description(soup)
    series_name = "Collection:" + series_name
    series = extract_collection_title_feature(soup)
    series += extract_episode_time_and_url(soup)
    return series_name, series


def url_type_helper(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    series_name, description = extract_series_name_and_description(soup)
    return series_name, description


def determine_url_type(url):
    match = 'Starring '
    two = ''
    url_type = None
    try:
        one, two = url_type_helper(url)
    except AttributeError:
        url_type = 'movie'
    if url_type is None and two[:len(match)] == match:
        url_type = 'collection'
    elif url_type is None:
        url_type = 'series'
    return url_type


def parse_movies_list(url_type, series_name, movies_list):
    i = 0
    for movie in movies_list:
        i += 1
        time, url = movie
        movie_parser = CriterionMovieParse.MovieParse(url)
        if url_type == 'movie':
            print('=' * 54)
        else:
            print('+' * 54)
            print(i)
            print(time)
        if series_name:
            print(series_name)
        movie_parser.print_info(time)
        if url_type == 'movie':
            print('=' * 54)
        else:
            print('+' * 54)
        print()
        print()


def get_series_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    series_name, description = extract_series_name_and_description(soup)
    series = extract_episode_time_and_url(soup)
    return series_name, description, series


def main():
    args = process_args()
    series_name = ''
    if args.url:
        url = args.url
        url_type = determine_url_type(url)

        if url_type == 'movie':
            parse_movies_list(url_type, series_name, [['', url]])
        elif url_type == 'collection':
            series_name, extracted_episode_info = get_collection_info(url)
            parse_movies_list(url_type, series_name, extracted_episode_info)
        else:
            series_name, description, extracted_episode_info = get_series_info(url)
            series_name = "Criterion:" + series_name
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(series_name)
            print(description)
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print()
            print()
            parse_movies_list(url_type, series_name, extracted_episode_info)


if __name__ == "__main__":
    main()
