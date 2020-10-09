import requests
from bs4 import BeautifulSoup
import argparse
import CriterionMovieParse


class CriterionParser:
    def __init__(self, url):
        self.url = url
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'html5lib')
        # print(self.soup.prettify())
        self.url_type = self.determine_url_type(self.soup)
        self.series_name = ''

    @staticmethod
    def extract_series_name_and_description(soup):
        match = 'Criterion Collection Edition '
        ret_str = ['NoName', 'NoAddition', 'NoDescription']
        table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
        if table:
            ret_str = []
            for string in table.stripped_strings:
                ret_str.append(string)
            if ret_str[1][:len(match)] == match:
                ret_str[0] = ret_str[1]
        return ret_str[0], ret_str[2]

    def url_type_helper(self, soup):
        series_name, description = self.extract_series_name_and_description(soup)
        return series_name, description

    @staticmethod
    def extract_collection_title_feature(soup):
        ret = []
        table = soup.find('li', attrs={'class': 'js-collection-item'})
        for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
            movie = [item.a.text.strip(), item.a['href']]
            ret.append(movie)
        return ret

    def extract_episode_time_and_url(self):
        ret = []
        table = self.soup.find('ul', attrs={'class': 'js-load-more-items-container'})
        if table:
            for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
                movie = [item.a.text.strip(), item.a['href']]
                ret.append(movie)
        return ret

    def get_collection_info(self):
        series_name, not_used = self.extract_series_name_and_description(self.soup)
        series_name = "Collection:" + series_name
        series = self.extract_collection_title_feature(self.soup)
        series += self.extract_episode_time_and_url()
        return series_name, series

    def get_edition_info(self):
        series_name, not_used = self.extract_series_name_and_description(self.soup)
        series = self.extract_collection_title_feature(self.soup)
        series += self.extract_episode_time_and_url()
        return series_name, series

    def determine_url_type(self, soup):
        matchStar = 'Starring '
        matchEdition = 'Criterion Collection Edition '
        two = ''
        url_type = None
        one, two = self.url_type_helper(soup)
        if one == 'NoName' and two == 'NoDescription':
            url_type = 'movie'
        elif url_type is None and two[:len(matchStar)] == matchStar:
            url_type = 'collection'
        elif url_type is None and one[:len(matchEdition)] == matchEdition:
            url_type = 'edition'
        elif url_type is None:
            url_type = 'series'
        return url_type

    def get_series_info(self):
        series_name, description = self.extract_series_name_and_description(self.soup)
        series_name = "Criterion:" + series_name
        series = self.extract_episode_time_and_url()
        next_url = self.extract_next_url()
        while next_url:
            r = requests.get(next_url)
            self.soup = BeautifulSoup(r.content, 'html5lib')
            next_url = self.extract_next_url()
            series += self.extract_episode_time_and_url()
        return series_name, description, series

    def extract_next_url(self):
        ret_str = None
        table = self.soup.find('div', attrs={'class': 'row loadmore'})
        if table:
            for item in table.findAll('a', attrs={'class': 'js-load-more-link'}):
                ret_str = "https://www.criterionchannel.com" + item['href']
        return ret_str

    def process(self):
        if self.url_type == 'movie':
            print('Examined ' + self.url)
            self.parse_movies_list([['', self.url]])
        elif self.url_type == 'collection':
            self.series_name, extracted_episode_info = self.get_collection_info()
            print('Examined ' + self.url)
            self.parse_movies_list(extracted_episode_info)
        elif self.url_type == 'edition':
            self.series_name, extracted_episode_info = self.get_edition_info()
            print('Examined ' + self.url)
            self.parse_movies_list(extracted_episode_info)
        else:
            self.series_name, description, extracted_episode_info = self.get_series_info()
            print('Examined ' + self.url)
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
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html5lib')
            url_type = self.determine_url_type(soup)
            if url_type == 'collection':
                time, url = self.extract_collection_title_feature(soup)[0]
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
