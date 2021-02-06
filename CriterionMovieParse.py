import requests
from bs4 import BeautifulSoup
import argparse
import MovieDatabase
import CriterionMiniSeriesParse


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
        self.url = url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        self.table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})
        cmsp_length = None
        if not self.table:
            # desperate attempt to salvage the effort
            cmsp = CriterionMiniSeriesParse.extract_series_title_feature(soup)
            cmsp_length = cmsp[0][0]
            r = requests.get(cmsp[0][1])
            soup = BeautifulSoup(r.content, 'html5lib')
            self.table = soup.find('div', attrs={'class': 'column small-16 medium-8 large-10'})
        diryrcnty, stars, descr, director, year, country = '', '', '', '', '', ''
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

        if title[0:4] == "The ":
            title = title[4:] + ", " + title[0:3]

        if title[0:2] == "A ":
            title = title[2:] + ", " + title[0:1]

        if year:
            title = title + " (" + year.strip() + ")"

        if '•' in length:
            length = length.split('•')[1].strip()

        if director:
            director = director.replace(" and ", ",")
            director = director.replace(",", ";")
            director = director.replace(";;", ";")

        self.length = length
        if cmsp_length:
            self.length = cmsp_length
        self.title = title
        self.director = director
        self.country = country.strip()
        self.stars = stars
        self.descr = descr
        self.year = year.strip()

    def print_info(self, supplied_length=None):

        print(self.url)
        if not supplied_length:
            print(self.length)
        print(self.title)
        if self.director:
            print(self.director)
        if self.country:
            print(self.country)
        if self.stars:
            print(self.stars)
        if self.descr:
            print()
            print(self.descr)

    def addToDatabase(self, supplied_length=None, collection=None, episode=None):
        movie_db = MovieDatabase.MovieDatabase()
        movie_length = self.length
        if supplied_length:
            movie_length = supplied_length

        movie_id = movie_db.add_movie(self.title, movie_length, self.url, self.descr)

        for director in self.director.split(';'):
            if director:
                director_id = movie_db.add_director(director.strip())
                movie_db.insert_movie_director(movie_id, director_id)

        for actor in self.stars.split(';'):
            actor_id = movie_db.add_actor(actor.strip())
            movie_db.insert_movie_actor(movie_id, actor_id)

        for country in self.country.split(';'):
            country_id = movie_db.add_country(country.strip())
            movie_db.insert_movie_country(movie_id, country_id)

        if collection and episode:
            collection_id = movie_db.add_collection(collection.strip())
            movie_db.insert_movie_collection(movie_id, collection_id, episode)


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