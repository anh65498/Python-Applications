# Anh Pham
# Analyze data
import numpy as np
import matplotlib.pyplot as plt

class Data_Analyzer:
    def __init__(self):
        self._filename   = "tuition.csv.xls"
        self._start_year = 1971
        self._end_year   = 2018
        self._years = np.arange(self._start_year,self._end_year + 1)

    def parseData(self):
        '''
        Purpose: read data from input file and store it in numpy array
                 There are 2 datasets in the file (2018 dollar and original dollar),
                 We only work with 2018 dollar costs only.
        '''
        try:
            self._data = np.loadtxt(self._filename, delimiter=",")
            self._data = self._data[:48, :]     #watch the index ????
        except IOError:
            print("Could not read input file", self._filename)
            raise SystemExit

    def plot_tuition(self):
        '''
        Purpose: plot the tuition cost over time  for private 4-years, public 4-years, and public 2-years
        '''
        plt.plot( self._years , self._data[:, 0], "-b", label="Private 4-year" )
        plt.plot( self._years , self._data[:, 2], "-r", label="Public 4-year" )
        plt.plot( self._years , self._data[:, 4], "-g", label="Public 2-year" )
        plt.legend(loc="best")      # pick the best location for labels/legions
        plt.xlabel("Year")
        plt.ylabel("Tuition (dollars)")
        plt.xticks( self._years, self._years, rotation="90", fontsize="8" )
        plt.title("Tuition Trend")
        plt.show()

    def plot_room_and_board(self):
        '''
        Purpose: plot the room and board cost over time for private 4-years and public 4-years
        '''
        plt.plot( self._years , self._data[:, 6], "-m", label="Private 4-year" )
        plt.plot( self._years , self._data[:, 8], "-c", label="Public 4-year" )
        plt.legend(loc="best")      # pick the best location for labels/legions
        plt.xlabel("Year")
        plt.ylabel("Room and Board (dollars)")
        plt.xticks( self._years, self._years, rotation="90", fontsize="8" )
        plt.title("Room and Board Trend")
        plt.show()

    def retVal(funct):
        '''
        Params:  None
        Ret   :  None
        Purpose: Decorator to print the return value of the function that it decorates.
        '''
        def wrapper(*args, **kwargs) :       # closure,
            result = funct(*args, **kwargs)      # call existing function
            print(result)
            return result
        return wrapper

    @retVal
    def get_college_cost(self):
        '''
        Ret: tuple of 4 costs for the 4 years to implement decorator for practice
        Purpose: User enter the graduation year, and your plot will show the cost of 4 years of college for each the 4 paths above. 
        '''
        grad_year = 0
        while (grad_year not in range(self._start_year + 3, self._end_year + 1)):
            grad_year = int(input("Enter year of graduation: "))

        begin_year = grad_year - 3
        # calculating cost
        _4_yrs_private              = self._data[begin_year - self._start_year : grad_year - self._start_year + 1, 0]
        _4_yrs_public               = self._data[begin_year - self._start_year : grad_year - self._start_year + 1, 2]
        _2_yrs_cc                   = self._data[begin_year - self._start_year : grad_year - self._start_year - 2 + 1, 4]
        _2_yrs_public_2_yrs_private = np.concatenate((_2_yrs_cc , _4_yrs_private[2:]))
        _2_yrs_public_2_yrs_public  = np.concatenate((_2_yrs_cc , _4_yrs_public[2:]))

        costs_of_4_plans = (sum(_4_yrs_private), sum(_4_yrs_public), sum(_2_yrs_public_2_yrs_private), sum(_2_yrs_public_2_yrs_public))
        # plotting bar chart
        label = ["4 Years Private", "4 Years Public", "2 Years Public & \n 2 Yrs Private","2 Years Public &\n 2 Yrs Public" ]
        data = [costs_of_4_plans[0], costs_of_4_plans[1], costs_of_4_plans[2], costs_of_4_plans[3]]
        plt.bar( (1,2,3,4), data)
        # label x and y axes
        plt.xlabel("Types of plan")
        plt.ylabel("Cost (in dollars)")
        # adjust x-axis ticks
        plt.xticks((1,2,3,4), label)
        # display the plot
        plt.show()
        return costs_of_4_plans

    def getEndYear(self):
        return self._end_year
