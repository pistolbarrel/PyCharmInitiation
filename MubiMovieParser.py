import datetime

import requests
from bs4 import BeautifulSoup
import argparse
import MovieDatabase

def extract_title(table):
    for item in table.findAll('h1', attrs={'class': 'css-75z8j3 eyplj683'}):
        return item.text

def extract_director(table):
    for item in table.findAll('span', attrs={'itemprop': 'name'}):
        return item.text

def extract_country(table):
    ret = []
    for item in table.findAll('div', attrs={'class': 'css-1f4y68f eyplj689'}):
        for str in item.stripped_strings:
            ret.append(str)
    return ret[0]

def extract_year(table):
    for item in table.findAll('span', attrs={'itemprop': 'dateCreated'}):
        return item.text

def extract_length(table):
    for item in table.findAll('time', attrs={'itemprop': 'duration'}):
        return item.text


def extract_info(table):
    for item in table.findAll('div', attrs={'itemprop': 'description'}):
        return item.text


def extract_crew(table):
    ret = []
    if table:
        for item in table.findAll('h3', attrs={'class': 'css-79elbk'}):
            name = extract_cast_name(item)
            role = extract_cast_role(item)
            ret.append((name, role))
    return ret


def extract_cast_name(table):
    for item in table.findAll('span', attrs={'class': 'css-1marmfu'}):
        return item.text


def extract_cast_role(table):
    for item in table.findAll('span', attrs={'class': 'css-1ojo4he'}):
        return item.text


class MubiMovieParse:
    def __init__(self, url):
        self.url = url
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        print(soup.prettify())
        self.table = soup.find('div', attrs={'class': 'css-ep7xq6 e1wsxkld12'})
        diryrcnty, stars, descr, director, year, country = '', '', '', '', '', ''
        title = extract_title(self.table)
        director = extract_director(self.table)
        country = extract_country(self.table)
        year = extract_year(self.table)
        length = extract_length(self.table)
        descr = extract_info(self.table)

        self.table = soup.find('div', attrs={'class': 'css-13wkbp7'})
        crew = extract_crew(self.table)

        if title[0:4] == "The ":
            title = title[4:] + ", " + title[0:3]

        if title[0:2] == "A ":
            title = title[2:] + ", " + title[0:1]
        title = title + ' (' + year + ')'

        length = datetime.timedelta(minutes=int(length))

        for member in crew:
            name, role = member
            if (role == 'Cast'):
                stars += name + ';'
        stars = stars[:-1]

        self.length = length
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
    movie_parser = MubiMovieParse(url)
    print('='*54)
    movie_parser.print_info()
    print('='*54)
    print()
    print()


if __name__ == "__main__":
    main()