# College Prices Analyzer and Visualizer

From CSV input file (tuition.csv) containing data of average Tuition and Fees and Room and Board in 2018 Dollars, this program lets the user view the tuition trend, the room and board trend, and the total cost of 4 years of college of 4 college path for a range of year (1971-72 to 2018-19)


## Getting Started
### Prerequisite
+  Python3

+ Install modules
```bash
$ pip3 install numpy
$ pip3 install matplotlib
```

+ If you see no graph
```bash
$ mkdir ~/.matplotlib
$ touch ~/.matplotlib/matplotlibrc
$ echo "backend: TkAgg" > ~/.matplotlib/matplotlibrc
```



## Running the Tests
```bash
$ python3 lab2.py
```

+ **Error: Could not read input file tuition.csv.xls**:
cd in Command Line Tool to the directory that contain all the .py file before run `$python3 lab2.py` again.

### Main Menu:

![main_menu](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/main_menu.png)

### Plots:
#### When user click on "Plot Tuition Trend" button
![tuition_trend](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/tuition_trend.png)

#### When user click on "Plot Room and Board Trend" button

![room_and_board.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/room_and_board.png)

### College Paths:
#### When user click on "Plot College Cost" button and they enter invalid year
![user_input.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/user_input.png)
![user_input_1.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/user_input_1.png)
![error_msg.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/error_msg.png)

#### When user click on "Plot College Cost" button and they enter valid year. E.g.: 2000
![user_input_2.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/user_input_2.png)
![user_input_3.png](https://github.com/anh65498/Python-Applications/blob/master/Program%202_Data%20Vis%20and%20GUI/Photos%20for%20readme/user_input_3.png)

#### When user click on "Plot College Cost" button and they press "Enter"
+ Program will assume graduation year is the latest year from input file.


## Authors

* **Anh Pham**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Clare Ng - Professor at De Anza College
