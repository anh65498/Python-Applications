# Movie Database GUI Application	

This program first builds a local database by scraping IMDB website for top 250 movies of all time.
Through a simple GUI window, users can easily 
	1. See top 250 imdb rated movies ordered and filtered them by rating, runtime, and year and range
		+ View by desceding ranking
			![ranking]()
		+ View the movies between 1995 and 2000 
			![year_range]()
	2. See the trend of movies over the year via graphs
		+ Scatterplot for average movie runtime per year (movies are getting longer as time passes)
			![average_runtime_per_year]()
		+ Histogram for runtime distribution of 250 top movies (the most popular length is 120 minutes)
		+ Histogram for release year distribution (the most popular release year is 2010)
	3. Search movie. Enter any movie name you want to look up for information and poster
		+ Example: Search all movies whose title contain "room"
			![search_room]()
		+ Example: Choose "The Room" for more information. Click "Save" to save the movie's information to a text file anywhere on their computer.
			![room]()



## Getting Started
### Prerequisite
+  Python3

## How to run

1. Download this project to your local computer.

2. Open terminal and change directory to your local project folder using command `$cd`

3. In terminal, run the application by `$python3 application.py`

## Troubleshooting

- If the program freeze and you want to shut down, in your terminal, press Control + C.
## Structure

MainWin
   |
   |---MovieListWin
   |          desc : allow user to see top 250 imdb rated movies ordered and
   |                 filtered by rating, runtime, and year
   |
   |---PlotMenuWin
   |      |   desc : allow user to choose from 3 plots showing movie data trends
   |      |
   |      |---ScatterPlotWin
   |      |      desc : plot a scatter plot graph with a linear trendline
   |      |
   |      |---HistogramPlotWin
   |             desc : plot a histogram graph showing distribution of data (bell curve)
   |
   |---SearchWin
          |   desc : allow user to search local database and omdb API for any movie using the search bar,
          |          then display matching search results in a list for user to select.
          |
          |---MovieDataWin
                 desc : display movie poster and other movie data such as title, runtime, year and more.
                        allow user to save movie data as a text file with file name beign the movie name

## Dependencies

- backend.py:
    + Web / api access
        - BeautifulSoup
        - requests
    + Database / Json
        - sqlite3
        - json
    + Network:
        - os
    + Others:
        - re
        - time


- application.py:
    + GUI
        - tkinter
        - ttk
        - tkinter.messagebox
        - tkinter.filedialog
    + Data visualization / analysis
        - numpy
        - matplotlib
        - FigureCanvasTkAgg
    + System
        - os
    + Database
        - sqlite3
    + Threading
        - threading
        - queue
    + Web / api access
        - requests
        - urllib.request
    + Others
        - collections
        - Image
        - ImageTk
		- Pillow  (used for saving and loading images(posters))

## Authors

* **Anh Pham**
* **Omar Burney**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Clare Ng - Professor at De Anza College