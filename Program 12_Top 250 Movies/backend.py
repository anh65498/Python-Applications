import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import json


SCRAPE_URL = "https://www.imdb.com/chart/top"
API_URL    = "http://www.omdbapi.com/"
API_KEY    = "&apikey=d2dfce13"
ROBOT_URL  = "https://www.imdb.com/robots.txt"

# create tables in database
conn = sqlite3.connect("movieDB.db")
cur  = conn.cursor()
cur.execute("DROP TABLE   IF EXISTS  Movies")
cur.execute('''CREATE TABLE Movies (
                id          INTEGER NOT NULL PRIMARY KEY,
                title        TEXT UNIQUE ON CONFLICT IGNORE,
                year        INTEGER,
                rating      REAL,
                runtime      TEXT,
                plot        TEXT,
                genre       TEXT)''')


# parse website for movie titles, year released, runtime, genre, plot, IMDB rating to add into database
page = requests.get(SCRAPE_URL)
soup = BeautifulSoup(page.content, "lxml")

# parse strings of titles and IMDB ID
titles      = [ title.get_text() for title in soup.select(".titleColumn a") ]
IMDBid      = [ re.search("(tt\d+)", title["href"]).group(1) for title in soup.select(".titleColumn a") ]
# Using IMDBid on OMDBapi to retrieve JSON of movie titles, year released, runtime, genre, plot, IMDB rating to add into database
movieData   = [ requests.get(API_URL + "?i=" + id + API_KEY).json() for id in IMDBid]       # list of dictionary of movie data
years       = [ int(movie["Year"]) for movie in movieData ]
runtime     = [ int(re.search("(\d+)", movie["Runtime"]).group(1)) for movie in movieData ]
genres       = [ movie["Genre"] for movie in movieData ]
plots        = [ movie["Plot"] for movie in movieData ]
imdbRatings = [ float(movie["imdbRating"]) for movie in movieData]

# Replace strings of years, runtime and rating in movieData to numbers then write movieData to JSON file
for i in range(len(movieData)):
    movieData[i]["Year"] = years[i]
    movieData[i]["Runtime"] = runtime[i]
    movieData[i]["imdbRating"] = imdbRatings[i]

# create a JSON file of movie data
with open("movies.json", 'w') as fp:
    json.dump(movieData, fp, indent=3)
# print("***** Total elapsed time: {:.2f}s".format(time.time()-start))  # 0.15s to fetch all data in iterator-style

# zip
data = tuple(zip(titles, years, imdbRatings, runtime, plots, genres))

for movie in data:
    cur.execute('''INSERT INTO Movies
                    (title, year, rating, runtime, plot, genre)
                    VALUES (?,?,?,?,?,?)''', (movie))

conn.commit()
conn.close()
