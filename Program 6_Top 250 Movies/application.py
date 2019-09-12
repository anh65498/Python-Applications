# Contributors : Omar Burney and Anh Pham
#
# Classes written by Anh:
#       MovieListWin
#
# Classes written by Omar:
#       MainWin
#       PlotMenuWin
#       ScatterPlotWin
#       HistogramPlotWin
#       SearchWin
#       MovieDataWin
#
# - - - - - - - - - - - - - - - - - - - - - - - -
#      DESCRIPTION
# - - - - - - - - - - - - - - - - - - - - - - - -
#
# Movie application: User can choose to
#   1. see top 250 IMDB's movies
#   2. view the trends in scatterplots and histograms
#   3. search for any movie and view movie data
#
# This script contains the frontend GUI for Movie application.
# Run backend.py if movieDB.db is not present to build the
# Database used in this file, application.py


import requests                 # used for pulling data from API
import urllib.request           # used for loading images
import os                       # used for saving movie data file
import sqlite3                  # used for interacting with the database
import numpy as np              # used for plotting data
import threading                # used for searching from API
import queue                    # used for threading
import matplotlib               # used for connecting plot to tkinter
matplotlib.use('TkAgg')         # tell matplotlib to work with Tkinter
import tkinter as tk            # normal import of tkinter for GUI
import tkinter.messagebox as tkmb   # used for displaying error messages
import  tkinter.filedialog      # used for saving files
from tkinter import ttk         # used for displaying list of data
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt # used for plotting
import collections              # used for plotting
from PIL import Image, ImageTk  # used for showing images

API_URL = "http://www.omdbapi.com/?apikey=<your key>"
API_KEY = "d2dfce13"
SEARCH_FROM_URL = (API_URL + "&type=movie&s=<your search>&page=<page number>").replace('<your key>', API_KEY)
FETCH_FROM_URL = (API_URL + "&i=<imdb id>").replace('<your key>', API_KEY)
JSON_DB = 'movies.json'
MOVIE_DB = "movieDB.db"

class MainWin(tk.Tk):
    """Create main menu with 3 options"""
    def __init__(self):
        """create main window"""
        # create main window
        super().__init__()
        self.title("Movies")
        # connect to database. if database file doesn't exist, exit program
        if not os.path.isfile(MOVIE_DB):
            tkmb.showerror("No database", "Please run backend.py before you run application.py", parent=self)
            raise SystemExit
        tk.Button(self, text='Top 250 IMDB Movies', command=lambda : MovieListWin(self)).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self, text='Movie Data Visualization', command=lambda : PlotMenuWin(self)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self, text='Search Movie', command=lambda : SearchWin(self)).grid(row=0, column=2, padx=5, pady=5)

class MovieListWin(tk.Toplevel):
    '''Purpose: Display top 250 movies based on filters'''
    def __init__(self, master):
        super().__init__(master)
        self.transient()
        self.focus_set()
        self.grab_set()
        self.title("Top 250 Movie Database")
        self.protocol("WM_DELETE_WINDOW", self._close)

        self.conn = sqlite3.connect(MOVIE_DB)
        self.cur  = self.conn.cursor()

        # 3 buttons to rank top 250 IMDB's movie: by ranking, by year, or by length
        F1 = tk.Frame(self)
        tk.Button(F1, text="View By Ranking", command=lambda:self.view("id")).pack(side = tk.LEFT,padx=10, pady=10)
        tk.Button(F1, text="View By Year", command=lambda:self.view("year")).pack(side = tk.LEFT, padx=10, pady=10)
        tk.Button(F1, text="View By Runtime", command=lambda:self.view("runtime")).pack(side = tk.LEFT, padx=10, pady=10)
        F1.pack()

        # Text Entry for user to filter the list by range
        self.F2 = tk.Frame(self)
        self.minEntry = tk.StringVar()		# create StringVar to store user input
        self.rangeEntry = tk.StringVar()
        self.maxEntry = tk.StringVar()

        t = [("min", self.minEntry), ("max", self.maxEntry)]
        self.E = [None, None]       # list of Text Entry widgets

        tk.Label(self.F2, text="Enter integers in the fields below to filter the list of movies.").grid(columnspan=4)
        # create 2 Text Entry: Min and Max for filtering
        for i in range(len(self.E)):
            tk.Label(self.F2, text=t[i][0].title()).grid()
            self.E[i] = tk.Entry(self.F2, textvariable=t[i][1])   # min will store the string that the user enters.
            self.E[i].grid(row=i+1, column=1)
            binding = (lambda x: lambda event: self.validateFilter(event, filterType=t[x][0]))(i)
            # 2 lambdas to bind the copy of i to validateFilter() at the moment it is created inside the loop, not binding the value of i at the end of the loop when user activate validateFilter()
            self.E[i].bind("<Return>", binding)

        self.F2.pack_forget()

        # Create a table to view movie by ranking/year/length and hide it
        self.F3 = tk.Frame(self)
        self.tree = ttk.Treeview(self.F3, columns = (1,2), height = 25, show = "headings")
        self.tree.pack(side = 'left')
        self.tree.column(1, width = 40)
        self.tree.column(2, width = 450)
        scroll = ttk.Scrollbar(self.F3, orient="vertical", command=self.tree.yview)
        scroll.pack(side = 'right', fill = 'y')
        self.tree.configure(yscrollcommand=scroll.set)

        self.F3.pack_forget()

    def view(self, category):
        '''
        Purpose : fetch data from DB in order then display all 250 ranked by categories
        '''
        self.category = category
        # set header and clear table
        self.tree.heading(1, text="Index")
        self.tree.delete(*self.tree.get_children())

        if self.category == "id":
            self.info = "rating"
            column2 = "Name"
        elif self.category == "year" or self.category == "runtime":
            self.info = self.category
            column2 = self.category.title()

        self.tree.heading(2, text=column2)
        self.cur.execute('''SELECT title, {} FROM Movies ORDER BY {} ASC'''.format(self.info, self.category))

        # fetch data from DB and display
        data = self.cur.fetchall()
        for count, d in enumerate(data, start=1):
            self.tree.insert('', 'end', values = ( count, str(d[0]) + "  " + "(" + str(d[1]) + ")"))           # {Godfather} 9.2

        self.F2.pack()
        self.F3.pack(padx=10, pady=10)

    def validateFilter(self, event, filterType):
        '''Purpose: callback function for Entry Widget to validate the filters'''
        _min = self.cur.execute("SELECT {} FROM Movies ORDER BY {} ASC".format(self.info, self.info)).fetchone()[0]
        _max = self.cur.execute("SELECT {} FROM Movies ORDER BY {} DESC".format(self.info, self.info)).fetchone()[0]
        _userMin = _min
        _userMax = _max
        try:
            minText = self.minEntry.get()
            _userMin = float(minText) if minText != "" else _min        # if blank, get min value from DB

            maxText = self.maxEntry.get()
            _userMax = float(maxText) if maxText != "" else _max
            if _userMax > _max or _userMax < _min or _userMin < _min or _userMin > _max:
                tkmb.showerror("Out of range", "The minimum value of {} is {} and the maximum value of {} is {} in the database".format(self.info, _min, self.info, _max), parent=self)
        except ValueError:
            tkmb.showerror("Invalid Input", "Please check min/max value again. Only input numbers.", parent=self)

        self.range = [_userMin, _userMax]
        self.filteredView()

        # clear entry box
        for i in range(2):
            self.E[i].delete(0, tk.END)		#  - then clears out the entry widget


    def filteredView(self):
        # empty the tree
        self.tree.delete(*self.tree.get_children())

        self.cur.execute("SELECT title, {} FROM Movies WHERE {} BETWEEN ? AND ? ORDER BY {} ASC".format(self.info, self.info, self.info),(self.range[0], self.range[1]))
        data = self.cur.fetchall()
        for count, d in enumerate(data, start=1):
            self.tree.insert('', 'end', values = ( count, str(d[0]) + "  " + "(" + str(d[1]) + ")"))           # {Godfather} 9.2


    def _close(self):
        ''' Purpose: Before destroying the window, close the connection to DB '''
        self.conn.close()
        self.destroy()

class PlotMenuWin(tk.Toplevel):
    """Show options for graphs"""
    def __init__(self, master):
        """show user the 3 graph options they have"""
        super().__init__(master)
        self.transient()
        self.focus_set()
        self.grab_set()
        conn = sqlite3.connect("movieDB.db")
        self.cur  = conn.cursor()

        tk.Label(self, text="IMDB's Top 250 Rated Movies").grid()
        F = tk.Frame(self)
        tk.Button(F, text='Average Movie Runtime Per Year', command=self.yearVsAvgRuntime).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(F, text='Runtime Distribution', command=lambda: self.plotHistogram('Runtime')).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(F, text='Release Year Distribution', command=lambda: self.plotHistogram('Year')).grid(row=0, column=2, padx=5, pady=5)
        F.grid()

    def plotHistogram(self, key):
        """compile histogram data and prompt graph"""
        self.cur.execute("SELECT {} FROM Movies".format(key))
        x = [m[0] for m in self.cur.fetchall()]
        if key == 'Runtime':
            graph_labels = ('Runtime Distribution', 'Number Of Movies', 'Runtime (minutes)')
        elif key == 'Year':
            graph_labels = ('Release Year Distribution', 'Number Of Movies', 'Release Year')
        else:
            graph_labels = ()
        HistogramPlotWin(self, x, *graph_labels)

    def yearVsAvgRuntime(self):
        """compile scatterplot data and prompt graph"""
        self.cur.execute("SELECT Year, Runtime FROM Movies")
        data = [ {'Year': m[0], 'Runtime':m[1] } for m in self.cur.fetchall()]
        runtimePerYear = collections.defaultdict(int)
        moviesPerYear = collections.defaultdict(int)
        averageRuntime = collections.defaultdict(float)
        for movie in data:
            runtimePerYear[movie['Year']] += movie['Runtime']
            moviesPerYear[movie['Year']] += 1
        for key in runtimePerYear.keys():
            averageRuntime[key] = runtimePerYear[key] / moviesPerYear[key]

        years = [k for k, v in averageRuntime.items()]
        avgRun = [v for k, v in averageRuntime.items()]
        ScatterPlotWin(self, years, avgRun, 'Year', 'Runtime (minutes)', 'Average Movie Runtime Per Year')

class ScatterPlotWin(tk.Toplevel):
    """Shows scatter plot data; dots and linear trend line"""
    def __init__(self, master, x_data, y_data, x_label, y_label, plot_title):
        """show scatter plot"""
        super().__init__(master)
        fig = plt.figure(figsize=(7, 7))
        # create scatter plot of data
        plt.scatter(x_data, y_data)
        plt.title(plot_title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        # create best fit line
        z = np.polyfit(x_data, y_data, 1)
        p = np.poly1d(z)
        plt.plot(x_data, p(x_data), "g")
        # connect plots to GUI
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

class HistogramPlotWin(tk.Toplevel):
    """Shows histogram data (bellcurve trend)"""
    def __init__(self, master, x_data, title='', y_label='', x_label=''):
        """show histogram plot"""
        super().__init__(master)
        fig = plt.figure(figsize=(7, 7))
        # create histogram with 10 bins
        plt.hist(x_data, bins=10)
        plt.title(title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

class SearchWin(tk.Toplevel):
    """Provide Widgets for searching movies from database adn API"""
    def __init__(self, master):
        """Create search bare and listbox of search results"""
        super().__init__(master)
        self.transient()
        self.grab_set()
        self.focus_set()
        conn = sqlite3.connect("movieDB.db")
        self.cur  = conn.cursor()
        self.q = queue.Queue()
        self.fetched_movies = {}

        def destroySearchWindow():
            """close connection to database on window close"""
            conn.close()
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", destroySearchWindow)

        # search widgets
        F1 = tk.Frame(self)
        self.movie_name = tk.StringVar()
        searchBox = tk.Entry(F1, textvariable=self.movie_name)
        searchBox.bind('<Return>', self.search)
        searchBox.grid(row=0, column=0)
        tk.Button(F1, text='Search', command=self.search).grid(row=0, column=1)
        F1.grid()

        # show results of search
        F2 = tk.Frame(self)
        S = tk.Scrollbar(F2)
        self.L = tk.Listbox(F2, height=10, width=45, yscrollcommand=S.set)
        S.config(command=self.L.yview)
        self.L.grid(row=0, column=0)
        S.grid(row=0, column=1, sticky='ns')
        tk.Button(F2, text='View Data', command=self.viewData).grid(columnspan=2)
        F2.grid(padx=10, pady=10)

    def search(self, event=None):
        """based on typed query, give search results in listbox"""
        movie_to_search = self.movie_name.get()
        self.cur.execute("SELECT Title FROM Movies WHERE Title LIKE '%'||?||'%'", (movie_to_search,))
        movies = { movie[0] for movie in self.cur.fetchall() }

        for x in range(1, 4):
            website = SEARCH_FROM_URL.replace('<page number>', str(x)).replace('<your search>', movie_to_search.replace(' ', '%20'))
            t = threading.Thread(target=self.fetchData, args=(website,x))
            t.start()

        for x in range(1,4):
            print(self.q.get())
        movies |= set(self.fetched_movies.keys())
        self.L.delete(0, tk.END)  # clear
        self.L.insert(tk.END, *sorted(movies))
        if len(self.fetched_movies.keys()) == 0:
            tkmb.showinfo('Movie Search' ,'No Results Came Back')

    def fetchData(self, website, page):
        """Used in thread to fetch data from API"""
        try:
            temp = requests.get(website).json()
            for movie in temp['Search']:
                while True:
                    if movie['Title'] not in self.fetched_movies.keys():
                        self.fetched_movies[movie['Title']] = movie['imdbID']
                        break
                    else:
                        movie['Title'] = movie['Title'] + ' '
        except KeyError:
            print('no results')
        self.q.put(page)

    def viewData(self):
        """fetch data from clicked movie and open wnidow for showing data"""
        keys = ('Title', 'Year', 'imdbRating', 'Runtime', 'Plot', 'Genre', 'Poster', 'Director', 'Actors', 'Awards')

        # Search for user selection in database and API
        try:
            movie_title = self.L.get(self.L.curselection())
            self.cur.execute("SELECT title, year, rating, runtime, plot, genre_id, posterLink, director, actor, award FROM Movies WHERE Title = ?", (movie_title,))
            movie_values = self.cur.fetchone()

            # check if selection is in the local database
            if movie_values is not None:
                movie = dict(zip(keys, tuple(movie_values)))
                movie['Runtime'] = str(movie['Runtime'])

                # fetch all genres from the db
                genres = []
                for genre_id in [int(x) for x in movie['Genre'].split(',')]:
                    self.cur.execute('''SELECT genre FROM GENRES WHERE id = ?''', (genre_id,))
                    genres.append(self.cur.fetchone()[0])
                movie['Genre'] = ', '.join(genres)

            # fetch data from API if not in database
            else:
                movie = requests.get(FETCH_FROM_URL.replace('<imdb id>', self.fetched_movies[movie_title])).json()
                movie = {key: movie[key] for key in keys}
            MovieDataWin(self, movie)
        except tk.TclError:
            print("Nothing was selected")

class MovieDataWin(tk.Toplevel):
    """Show movie data and poster"""
    def __init__(self, master, movie_data):
        """create GUI todisplay movie data and poster"""
        super().__init__(master)
        self.transient()
        self.focus_set()

        # Display Movie Poster
        try:
            if movie_data['Poster'] != 'N/A':
                urllib.request.urlretrieve(movie_data['Poster'], "poster.jpg")
                image = Image.open("poster.jpg")
                image = image.resize((160,240))
            else:
                image = Image.open("default_poster.jpg")
        except urllib.error.HTTPError:      # windows error
            image = Image.open("default_poster.jpg")
        except urllib.error.URLError:       # mac error
            image = Image.open("default_poster.jpg")
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo)
        label.image = photo  # keep a reference!
        label.grid(row=0, column=0)

        # display all data
        Movie_Data_Frame = tk.Frame(self)
        year = str(movie_data['Year'])[:4]
        rating = str(movie_data['imdbRating'])
        runtime = movie_data['Runtime'].replace(' min', '')
        tk.Label(Movie_Data_Frame, text=movie_data['Title'], wraplength=300, font=('Helvetica',20)).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Year: ' + year).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='imdb Rating: ' + rating).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Runtime: ' + str(runtime) + ' mins').grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Plot: ' + movie_data['Plot'], wraplength=300, justify=tk.LEFT).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Genre: ' + movie_data['Genre'], wraplength=300, justify=tk.LEFT).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Director: ' + movie_data['Director']).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Actors: ' + movie_data['Actors'], wraplength=300, justify=tk.LEFT).grid(sticky='w')
        tk.Label(Movie_Data_Frame, text='Awards: ' + movie_data['Awards'], wraplength=300, justify=tk.LEFT).grid(sticky='w')
        Movie_Data_Frame.grid(row=0, column=1)
        tk.Button(self, text='Save Movie', command=lambda : self.writeToFile(movie_data)).grid(sticky="nsew")

    def writeToFile(self, movie_data):
        """Write movie data to a file named based off film"""
        path = os.getcwd()
        directory = tk.filedialog.askdirectory(initialdir= path)
        filename = os.path.join(directory, movie_data['Title'].replace(' ', '_').replace(':', '').replace("'", '')+'.txt')
        with open(filename, 'w') as fw:
            for k, v in movie_data.items():
                print(k, v)
                fw.write(str(k) + ": " + str(v) + "\n")

def builDatabase():
    # build database and install dependencies 
    os.system("python3 backend.py")

if __name__ == '__main__':
    builDatabase()
    # GUI application
    root = MainWin()
    root.mainloop()
