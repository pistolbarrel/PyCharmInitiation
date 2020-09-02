import requests
from bs4 import BeautifulSoup
import CriterionMovieParse


def main():
    url = 'https://www.criterionchannel.com/two-by-dorothy-arzner'
    series_name, eps, descr, series = get_series_info(url)
    series_name = "Criterion:" + series_name
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print(series_name)
    print(descr)
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print()
    print()
    i = 0
    for movie in series:
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


def get_series_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    # print(soup.prettify())
    table = soup.find('div', attrs={'class': 'collection-details grid-padding-left'})
    ret_str = []
    for string in table.stripped_strings:
        ret_str.append(string)

    table = soup.find('ul', attrs={'class': 'js-load-more-items-container'})
    series = []
    for item in table.findAll('div', attrs={'class': 'grid-item-padding'}):
        movie = []
        movie.append(item.a.text.strip())
        movie.append(item.a['href'])
        series.append(movie)
    return ret_str[0], ret_str[1], ret_str[2], series


if __name__ == "__main__":
    main()