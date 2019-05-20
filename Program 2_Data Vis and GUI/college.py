# Anh Pham
# This file analyze the data of the colleges
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class Data_Analyzer:
    # declare these variables as local variable so they aren't instantiated with every Data_Analyzer object
    _filename   = "tuition.csv"
    _start_year = 1971
    _end_year   = 2018
    _years = np.arange(_start_year,_end_year + 1)
    _grad_year = 0

    '''
        Q: When should a variable be an instance variable (self.fig) and when should it be a local variable (fig)?
        A: always think twice before making an instance variable.
        You're adding to the "bulk" of the object with every instance variable,
        since instance variables stay around for the lifetime of the object.
        If the variable is only used within one method and is not needed by any other method, it should be a local variable.
        When the method (function) finishes running, local variables are cleared out of the run time stack so they don't stick around and unnecessarily take up space.
    '''

    def __init__(self):
        '''
        Purpose: read data from input file and store it in numpy array
                 There are 2 datasets in the file (2018 dollar and original dollar),
                 We only work with 2018 dollar costs only.
        '''

        self._data = np.loadtxt(self._filename, delimiter=",")      # we can make this local var but as instance variable, catch exception in what call it
        (row, col) = self._data.shape
        # self._data = self._data[:48, :]     #watch the index
        self._data = self._data[:row//2, :]     # This is a view, an instance variable
        # self._data = self._data[:row//2, range(0,col,2)]     # Another example of view, which only has dollar amount and not rate

         # Shouldn't have try-except to handle file IO here because the user wouldn't know the problem from the GUI



    def plot_tuition(self):
        '''
        Purpose: plot the tuition cost over time  for private 4-years, public 4-years, and public 2-years
        '''
        colorLabelList = [('-b', 'Private 4-year'), ('-r', 'Public 4-year'), ('-g','Public 2-year')]
        # without repeating plt.plot() 3 times, use a loop
        for i in range(len(colorLabelList)):
            plt.plot( self._years , self._data[:, 2*i], colorLabelList[i][0], label=colorLabelList[i][1] )

        plt.legend(loc="best")      # pick the best location for labels/legions
        plt.xlabel("Year")
        plt.ylabel("Tuition (dollars)")
        plt.xticks( self._years, self._years, rotation="90", fontsize="8" )
        plt.title("Tuition Trend", fontsize=13, weight="bold")
        # plt.show()
        plt.tight_layout()  # to make room for xlabel

    def plot_room_and_board(self):      # def rbTrend(self):
        '''
        Purpose: plot the room and board cost over time for private 4-years and public 4-years
        '''
        plt.plot( self._years , self._data[:, 6] - self._data[:, 0], "-m", label="Private 4-year" )
        plt.plot( self._years , self._data[:, 8] - self._data[:, 2], "-c", label="Public 4-year" )
        plt.legend(loc="best")      # pick the best location for labels/legions
        plt.xlabel("Year")
        plt.ylabel("Room and Board (dollars)")
        plt.xticks( self._years, self._years, rotation="90", fontsize="8" )
        plt.title("Room and Board Trend")
        # plt.show()
        plt.tight_layout()    # to make room for xlabel


    def retVal(funct):
        '''
        Params:  None
        Ret   :  None
        Purpose: Decorator to print the return value of the function that it decorates.
                 Decorator are supposed to be general so we can reuse it a lot. That's why general terms: retVal, fun, args, kwargs, ...
        '''
        def wrapper(*args, **kwargs) :       # closure,
            result = funct(*args, **kwargs)      # call existing function
            print(result)
            return result
        return wrapper

    @retVal
    def compare_college_cost(self):
        '''
        Ret: tuple of 4 costs for the 4 years to implement decorator for practice
        Purpose: User enter the graduation year, and your plot will show the cost of 4 years of college for each the 4 paths above. 
        '''
        # grad_year = 0
        # while (grad_year not in range(self._start_year + 3, self._end_year + 1)):
        #     grad_year = int(input("Enter year of graduation: "))

        begin_year = self._grad_year - 3
        # get the cost of different college path
        _4_yrs_private              = self._data[begin_year - self._start_year : self._grad_year - self._start_year + 1, 0]
        _4_yrs_public               = self._data[begin_year - self._start_year : self._grad_year - self._start_year + 1, 2]
        _2_yrs_cc                   = self._data[begin_year - self._start_year : self._grad_year - self._start_year - 2 + 1, 4]
        _2_yrs_public_2_yrs_private = np.concatenate((_2_yrs_cc , _4_yrs_private[2:]))
        _2_yrs_public_2_yrs_public  = np.concatenate((_2_yrs_cc , _4_yrs_public[2:]))

        # calculate the sum of 4 years
        costs_of_4_plans = (sum(_4_yrs_private), sum(_4_yrs_public), sum(_2_yrs_public_2_yrs_private), sum(_2_yrs_public_2_yrs_public))

        # plotting bar chart - method 1
        label = ["4 Years Private", "4 Years Public", "2 Years Public & \n 2 Yrs Private","2 Years Public &\n 2 Yrs Public" ]
        data = [costs_of_4_plans[0], costs_of_4_plans[1], costs_of_4_plans[2], costs_of_4_plans[3]]
        plt.bar( (1,2,3,4), data)

        # plotting bar chart - method 2
        # mode = [
        #     (firstYear, None, 'blue', 'First Year')
        #     (secondYear, None, 'red', 'Second Year')
        #     (thirdYear, None, 'yellow', 'Third Year')
        #     (fourthYear, None, 'green', 'Last Year')
        # ]
        # for year, bottom, color, label in mode:
            # plt.bar( (1,2,3,4), year, bottom = bottom, color = color, data)

        # label x and y axes
        plt.xlabel("Types of plan for " + str(begin_year) + " - " + str(self._grad_year))
        plt.ylabel("Cost (in dollars)")
        # adjust x-axis ticks
        plt.xticks((1,2,3,4), label, fontsize=3)
        # display the plot
        plt.tight_layout()  # to make room for xlabel
        # plt.show()
        return costs_of_4_plans
