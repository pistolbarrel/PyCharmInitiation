import requests
from bs4 import BeautifulSoup
import argparse
import CriterionMovieParse


class CriterionParser:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html5lib')
        self.url_type = self.determine_url_type()
        self.series_name = ''

    def extract_series_name_and_description(self):
        ret_str = []
        table = self.soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
        for string in table.stripped_strings:
            ret_str.append(string)
        return ret_str[0], ret_str[2]

    def extract_collection_title_feature(self):
        ret = []
        table = self.soup.find('li', attrs={'class': 'js-collection-item'})
        for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
            movie = [item.a.text.strip(), item.a['href']]
            ret.append(movie)
        return ret

    def extract_episode_time_and_url(self):
        ret = []
        table = self.soup.find('ul', attrs={'class': 'js-load-more-items-container'})
        for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
            movie = [item.a.text.strip(), item.a['href']]
            ret.append(movie)
        return ret

    def get_collection_info(self):
        series_name, not_used = self.extract_series_name_and_description()
        series_name = "Collection:" + series_name
        series = self.extract_collection_title_feature()
        series += self.extract_episode_time_and_url()
        return series_name, series

    def url_type_helper(self):
        series_name, description = self.extract_series_name_and_description()
        return series_name, description

    def determine_url_type(self):
        match = 'Starring '
        two = ''
        url_type = None
        try:
            one, two = self.url_type_helper()
        except AttributeError:
            url_type = 'movie'
        if url_type is None and two[:len(match)] == match:
            url_type = 'collection'
        elif url_type is None:
            url_type = 'series'
        return url_type

    def get_series_info(self):
        series_name, description = self.extract_series_name_and_description()
        series = self.extract_episode_time_and_url()
        series_name = "Criterion:" + series_name
        return series_name, description, series

    def process(self):
        if self.url_type == 'movie':
            self.parse_movies_list([['', self.url]])
        elif self.url_type == 'collection':
            self.series_name, extracted_episode_info = self.get_collection_info()
            self.parse_movies_list(extracted_episode_info)
        else:
            self.series_name, description, extracted_episode_info = self.get_series_info()
            print('+' * 54)
            print(self.series_name)
            print(description)
            print('+' * 54)
            print()
            print()
            self.parse_movies_list(extracted_episode_info)

    def parse_movies_list(self, movies_list):
        i = 0
        for movie in movies_list:
            i += 1
            time, url = movie
            movie_parser = CriterionMovieParse.MovieParse(url)
            if self.url_type == 'movie':
                print('=' * 54)
            else:
                print('+' * 54)
                print(i)
                print(time)
            if self.series_name:
                print(self.series_name)
            movie_parser.print_info(time)
            if self.url_type == 'movie':
                print('=' * 54)
            else:
                print('+' * 54)
            print()
            print()


def process_args():
    usage_desc = "This is how you use this thing"
    parser = argparse.ArgumentParser(description=usage_desc)
    parser.add_argument("url", help="URL to parse")
    args = parser.parse_args()
    return args


def main():
    args = process_args()
    if args.url:
        parser = CriterionParser(args.url)
        parser.process()


if __name__ == "__main__":
    main()
