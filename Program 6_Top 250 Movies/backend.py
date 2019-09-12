# Contributors : Anh Pham
# This script contains the backend that will create a Database and JSON for Movies
# Run this to build the Database before running the application.py
#
# Methods written by Anh:
#       main

import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import json
import time
import os

build_db   = False           # True to build DB
build_json = False          # True to build JSON file
build_dp   = False           # True to automatically install dependencies on the first run (set to False afterwards)

SCRAPE_URL = "https://www.imdb.com/chart/top"
API_URL    = "http://www.omdbapi.com/"
# API_KEY    = "&apikey=d2dfce13"
# API_KEY    = "&apikey=thewdb"
API_KEY    = "&apikey=7c7784fd"
ROBOT_URL  = "https://www.imdb.com/robots.txt"

def main():
    if not build_db:
        return
    # create table in database
    conn = sqlite3.connect("movieDB.db")
    cur  = conn.cursor()
    cur.execute("DROP TABLE   IF EXISTS  Movies")   # delete existing table
    cur.execute("DROP TABLE   IF EXISTS  Genres")

    cur.execute('''CREATE TABLE Movies (
                    id          INTEGER NOT NULL PRIMARY KEY,
                    title       TEXT,
                    year        INTEGER,
                    rating      REAL,
                    runtime     INTEGER,
                    plot        TEXT,
                    genre_id    TEXT,
                    posterLink  TEXT,
                    director    TEXT,
                    actor       TEXT,
                    award       TEXT  )''')

    cur.execute('''CREATE TABLE Genres(
                    id          INTEGER NOT NULL PRIMARY KEY,
                    genre       TEXT UNIQUE ON CONFLICT IGNORE)''')

    # parse website for movie titles, year released, runtime, genre, plot, IMDB rating to add into database
    page = requests.get(SCRAPE_URL)
    soup = BeautifulSoup(page.content, "lxml")

    # parse strings of titles and IMDB ID
    titles      = [ title.get_text() for title in soup.select(".titleColumn a") ]
    IMDBid      = [ re.search("(tt\d+)", title["href"]).group(1) for title in soup.select(".titleColumn a") ]
    # Using IMDBid on OMDBapi to retrieve JSON of movie titles, year released, runtime, genre, plot, IMDB rating to add into database
    # 9 list comprehension take half as much time as 1 for loop (tested)
    movieData   = [ requests.get(API_URL + "?i=" + id + API_KEY).json() for id in IMDBid]       # list of dictionary of movie data
    years       = [ int(movie["Year"]) for movie in movieData ]
    runtime     = [ int(re.search("(\d+)", movie["Runtime"]).group(1)) for movie in movieData ]
    genreList   = [ movie["Genre"].split(",") for movie in movieData ]
    plots       = [ movie["Plot"] for movie in movieData ]
    imdbRatings = [ float(movie["imdbRating"]) for movie in movieData]
    posterLinks = [ movie["Poster"] for movie in movieData ]
    directors   = [ movie["Director"] for movie in movieData ]
    actors      = [ movie["Actors"] for movie in movieData ]
    awards      = [ movie["Awards"] for movie in movieData ]

    # create a JSON file of movie data
    if build_json:
        # Replace strings of years, runtime and rating in movieData to numbers then write movieData to JSON file
        # could replace this loop with database????
        for i in range(len(movieData)):
            movieData[i]["Year"] = years[i]
            movieData[i]["Runtime"] = runtime[i]
            movieData[i]["imdbRating"] = imdbRatings[i]

        with open("movies.json", 'w') as fp:
            json.dump(movieData, fp, indent=3)


    data = zip(genreList, titles, years, imdbRatings, runtime, plots, posterLinks, directors, actors, awards)   # iterator of tuples
    genreIds = {}


    # build Movies and Genres DB
    for movie in data:
        idGenList = []          # list of strings of genre's id from Genre table
        # insert the genres of each movie into Genres table
        for genre in movie[0]:          # movies[0] contains the all genres of current movie
            genre = genre.strip()
            if not genre in genreIds:   # this loop cut 250 Db queries to 12 DB queries
                cur.execute("INSERT INTO Genres (genre) VALUES (?)", (genre,))
                cur.execute("SELECT id FROM Genres WHERE genre = ?", (genre,))
                gen_id = cur.fetchone()[0]
                genreIds[genre] = str(gen_id)
                # turn id integer to string, append string to list of strings to insert a string of genre_id to Movies table.
            idGenList.append(str(gen_id))       # For example:  ['20', '12']

        fields = (*movie[1: ], ','.join(idGenList))
        cur.execute('''INSERT INTO Movies
                (title, year, rating, runtime, plot, posterLink, director, actor, award)
                VALUES (?,?,?,?,?,?,?,?,?)''', (movie[1: ]) )
        # insert genre_id to Movies table
        cur.execute("UPDATE Movies SET genre_id =? WHERE title=?", (','.join(idGenList), movie[1]) )
        idGenList = []

    conn.commit()
    conn.close()

def preinstall():
    '''Ask user if they want to install dependecies and get newest movies ranking to reduce waiting time'''
    while True:
        print("Do you want to install the dependencies? If this is your first time running the app, enter `y`. Otherwise, enter `n`")
        build_dp = input("> ").strip().lower()
        if build_dp != "y" and build_dp != "n":
            print("Please only enter `y` or `n`") 
        else:
            if build_dp == 'y':
                build_dp = True
            elif build_dp == 'n':
                build_dp = False
            break

    while True:
        print("If this is your first time running the application, enter 'y'. If not and you don't want to get the newest ranking from IMDB, press 'n' to shorten the waiting time")
        build_db = input("> ").strip().lower()
        if build_db != "y" and build_db != "n":
            print("Please only enter `y` or `n`") 
        else:
            if build_db == 'y':
                build_db = True
            elif build_db == 'n':
                build_db = False
            break

    return (build_dp, build_db)

if __name__ == '__main__':
    start=time.time()
    build_dp, build_db = preinstall()
    
    if build_dp :
        os.system("pip3 install -r requirements.txt")
    if build_db:
        print("It might take 10-60 seconds to build the database. Please wait. Once the process finishes, the app GUI will appear.")
        main()
        print("It took {} seconds to finish building database".format(time.time() - start))
