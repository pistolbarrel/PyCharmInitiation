import sqlite3
from sqlite3 import Error


class MovieDatabase:
    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        db_file = r"C:\Users\Greg\MyMovies.sl3"
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn

    def add_movie(self, title, duration, url, desc):
        idx = self.find_a_Movie(title)
        if not idx:
            idx = self.insert_a_Movie(title, duration, url, desc)
        return idx

    def find_a_Movie(self, title):
        cur = self.conn.cursor()
        cur.execute("select m.IDMovie from movies m where m.Title =?", (title,))

        rows = cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def insert_a_Movie(self, title, duration, url, desc):
        cur = self.conn.cursor()
        tup = (title, duration, url, desc)
        cur.execute("insert into movies (title, duration, url, description) values (?,?,?,?)", tup)
        self.conn.commit()
        return cur.lastrowid

    def add_director(self, name):
        id = self.find_director(name)
        if not id:
            id = self.insert_director(name)
        return id

    def find_director(self, name):
        cur = self.conn.cursor()
        cur.execute("select m.DirectorId from directors m where m.Name =?", (name,))

        rows = cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def insert_director(self, name):
        cur = self.conn.cursor()
        tup = (name,)
        cur.execute("insert into directors (name) values (?)", tup)
        self.conn.commit()
        return cur.lastrowid

    def insert_movie_director(self, movie_id, director_id):
        cur =self.conn.cursor()
        tup = (movie_id, director_id)
        try:
            cur.execute("insert into moviedirector (MovieId, DirectorId) values (?,?)", tup)
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        return cur.lastrowid

    def add_actor(self, name):
        id = self.find_actor(name)
        if not id:
            id = self.insert_actor(name)
        return id

    def find_actor(self, name):
        cur = self.conn.cursor()
        cur.execute("select t.ActorId from actors t where t.Name =?", (name,))

        rows = cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def insert_actor(self, name):
        cur = self.conn.cursor()
        tup = (name,)
        cur.execute("insert into actors (name) values (?)", tup)
        self.conn.commit()
        return cur.lastrowid

    def insert_movie_actor(self, movie_id, director_id):
        cur = self.conn.cursor()
        tup = (movie_id, director_id)
        try:
            cur.execute("insert into MovieActor (MovieId, ActorId) values (?,?)", tup)
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        return cur.lastrowid

    def add_country(self, name):
        id = self.find_country(name)
        if not id:
            id = self.insert_country(name)
        return id

    def find_country(self, name):
        cur = self.conn.cursor()
        cur.execute("select t.countryId from countries t where t.Name =?", (name,))

        rows = cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def insert_country(self, name):
        cur = self.conn.cursor()
        tup = (name,)
        cur.execute("insert into countries (name) values (?)", tup)
        self.conn.commit()
        return cur.lastrowid

    def insert_movie_country(self, movie_id, director_id):
        cur = self.conn.cursor()
        tup = (movie_id, director_id)
        try:
            cur.execute("insert into Moviecountry (MovieId, countryId) values (?,?)", tup)
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        return cur.lastrowid

    def add_collection(self, name):
        id = self.find_collection(name)
        if not id:
            id = self.insert_collection(name)
        return id

    def find_collection(self, name):
        cur = self.conn.cursor()
        cur.execute("select t.collectionId from collections t where t.Name =?", (name,))

        rows = cur.fetchall()
        if rows:
            return rows[0][0]
        else:
            return None

    def insert_collection(self, name):
        cur = self.conn.cursor()
        tup = (name,)
        cur.execute("insert into collections (name) values (?)", tup)
        self.conn.commit()
        return cur.lastrowid

    def insert_movie_collection(self, movie_id, collection_id, episode):
        cur = self.conn.cursor()
        tup = (movie_id, collection_id, episode)
        try:
            cur.execute("insert into Moviecollection (MovieId, collectionId, episode) values (?,?, ?)", tup)
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
        return cur.lastrowid

def main():
    movie_title = "The Future (2011)"
    duration = "1:30:52"
    url = r"https://www.criterionchannel.com/pre-code-joan-blondell/season:1/videos/joan-blondell-intro"
    desc = r'Adapted by Harold Pinter from the landmark novel by Margaret Atwood, the original screen adaptation of ' \
           r'THE HANDMAID’S TALE takes place in an authoritarian future America where young, healthy women must serve ' \
           r'the country by giving birth to babies for an increasingly infertile society determined to produce a more ' \
           r'“pure” generation. When she is forced to become a childbearing “handmaiden” for the wealthy Commander (' \
           r'Robert Duvall) and his wife (Faye Dunaway), Offred (Natasha Richardson) launches a rebellion to reclaim ' \
           r'her autonomy. '
    directors = 'Volker Schlöndorff'
    actors = 'Natasha Richardson; Faye Dunaway; Aidan Quinn'
    countries = 'Czechoslovakia'
    collection = 'Criterion:Czechoslovak New Wave'
    episode = '3'

    movie_db = MovieDatabase()

    movie_id = movie_db.add_movie(movie_title, duration, url, desc)

    for director in directors.split(';'):
        director_id = movie_db.add_director(director)
        movie_db.insert_movie_director(movie_id, director_id)

    for actor in actors.split(';'):
        actor_id = movie_db.add_actor(actor)
        movie_db.insert_movie_actor(movie_id, actor_id)

    for country in countries.split(';'):
        country_id = movie_db.add_country(country)
        movie_db.insert_movie_country(movie_id, country_id)

    collection_id = movie_db.add_collection(collection)
    movie_db.insert_movie_collection(movie_id, collection_id, episode)


if __name__ == '__main__':
    main()