# Write a Python app that create a database IMDB's top 250 movies' name, year of release, director name and stars
# Then allow user to
#   * Rank by movie IMDB's ranking, length, year

# Future features:
# create an option to search for movie
# use threading to fetch data from 3 pages
# line 70

import requests
from bs4 import BeautifulSoup
import time
import re
import sqlite3
import tkinter as tk
from tkinter import ttk

# main window
class MainWin(tk.Tk):
    def __init__(self):

        self.conn = sqlite3.connect("movieDB.db")
        self.cur  = self.conn.cursor()
        start = time.time()
        self.createDB()
        print("***** Total elapsed time: {:.2f}s".format(time.time()-start))  # 0.15s to fetch all data in iterator-style
        super().__init__()
        self.geometry("500x550+400+50")
        self.title("Top 250 Movie Database")
        self.protocol("WM_DELETE_WINDOW", self._close)

        # 3 buttons: view by ranking, view by year, view by length
        frame1 = tk.Frame(self)
        tk.Button(frame1, text="View By Ranking", command=lambda:self.view("id")).pack(side = tk.LEFT,padx=10, pady=10)
        tk.Button(frame1, text="View By Year", command=lambda:self.view("year")).pack(side = tk.LEFT, padx=10, pady=10)
        tk.Button(frame1, text="View By Length", command=lambda:self.view("length")).pack(side = tk.LEFT, padx=10, pady=10)
        frame1.pack()

        # Create a table to view movie by ranking/year/length
        frame2 = tk.Frame(self)
        frame2.pack()

        self.tree = ttk.Treeview(frame2, columns = (1,2), height = 25, show = "headings")
        self.tree.pack(side = 'left')

        self.tree.column(1, width = 40)
        self.tree.column(2, width = 350)

        scroll = ttk.Scrollbar(frame2, orient="vertical", command=self.tree.yview)
        scroll.pack(side = 'right', fill = 'y')

        self.tree.configure(yscrollcommand=scroll.set)



    def view(self, type):
        ''' Purpose : fetch data by type, display it '''
        # set header and clear table
        self.tree.heading(1, text="Rank")
        self.tree.delete(*self.tree.get_children())

        if type == "id":
            self.tree.heading(2, text="Name")
            self.cur.execute('''SELECT name FROM Movies ORDER BY {} ASC'''.format(type))
        else:
            self.tree.heading(2, text=type.title())
            self.cur.execute('''SELECT name, {} FROM Movies ORDER BY {} ASC'''.format(type, type))

        # fetch data from DB and display


        for count, *movie in enumerate(self.cur.fetchall(), start=1):
            self.tree.insert('', 'end', values = ( count, *movie ) )


    def createDB(self):
        '''
        Purpose: Scrape top 250 movie data from imdb.com and create database
        '''
        page1 = requests.get("https://www.imdb.com/search/title?groups=top_250&sort=user_rating")
        page2 = requests.get("https://www.imdb.com/search/title?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt")
        page3 = requests.get("https://www.imdb.com/search/title?groups=top_250&sort=user_rating,desc&start=101&ref_=adv_nxt")

        # create database

        self.cur.execute("DROP TABLE   IF EXISTS  Movies")
        self.cur.execute('''CREATE TABLE Movies (
                        id          INTEGER NOT NULL PRIMARY KEY,
                        name        TEXT UNIQUE ON CONFLICT IGNORE,
                        year        INTEGER,
                        director    TEXT,
                        rating      REAL,
                        length      TEXT)''')


        for page in [page1, page2, page3]:
            soup = BeautifulSoup(page.content, "lxml")

            movie = soup.select(".lister-item-content")

            start = time.time()

            title   = [ m.find("a").get_text().strip() for m in movie ]
            pattern = '(\d+)'
            year    = [int(re.search(pattern, y.get_text()).group(0)) for m in movie for y in m.select(".lister-item-year")]
            director = [m.select("p")[2].find("a").get_text() for m in movie]
            ratings   = [float(m.find("div").find("div")["data-value"]) for m in movie]

            length  = [int(re.search(pattern, m.find('p').select(".runtime")[0].get_text()).group(0)) for m in movie ]           # some movie has undefined lenght

            # print("***** Total elapsed time: {:.2f}s".format(time.time()-start))  # 0.15s to fetch all data in iterator-style

            # zip
            data = tuple(zip(title,year,director,ratings,length))

            for movie in data:
                self.cur.execute('''INSERT INTO Movies
                                (name, year, director, rating, length)
                                VALUES (?,?,?,?,?)''', (movie))

            # self.cur.execute('''SELECT name FROM Movies WHERE name LIKE '%father' ''')
            # print(self.cur.fetchone() )

    def _close(self):
        ''' Purpose: Before destroying the window, close the connection to DB '''
        self.conn.close()
        self.destroy()

def main():
    app = MainWin()
    app.mainloop()

main()
# 1) instead of 4 iterator, do loop. Which is faster?
