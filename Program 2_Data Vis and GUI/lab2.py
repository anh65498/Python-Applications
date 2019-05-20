# Anh Pham
# Purpose: This program analyzes U.S college tuition and/or room and board between 1971 - 2018
# and lets the user view the tuition trend, the room and board trend, and the total cost of 4 years of college
# for a range of years.
# This file contains the GUI

from college import Data_Analyzer
import tkinter as tk        # for GUI
import tkinter.messagebox as tkmb   # for error window
import matplotlib
matplotlib.use('TkAgg')               	# tell matplotlib to work with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt

class mainWindow(tk.Tk):
    def __init__(self):
        super().__init__()              # run the constructor of tk. Pass nothing because this is main window

        self.minsize(450,80)
        self.geometry("+350+400")
        '''
        Purpose: Create and display the main window with 3 buttons
                    to plot tuition trend, plot room and board trend, plot college cost
                    When the user clicks X on the main window, all GUI windows should close.
        '''
        try:
            self.collegeData = Data_Analyzer()      # in try block because code in constructor
        except FileNotFoundError as e:
            # if file couldn't be opened, alert user via messagebox. If user click 'ok', destroy mainWindow()
            if tkmb.showerror("File could not found", str(e), parent=self) == 'ok':
                self.destroy()

        self._Frame = tk.Frame(self)
        self._Frame.grid()
        self.title("College Pricing from " + str(self.collegeData._start_year) + " to " + str(self.collegeData._end_year))
        tk.Button(self._Frame, text="plot tuition trend".title(), command= lambda : ToplevelWindow(self, self.collegeData.plot_tuition)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        tk.Button(self._Frame, text="plot room and board trend".title(), command= lambda : ToplevelWindow(self, self.collegeData.plot_room_and_board)).grid(row=0, column=1, padx=10, pady=10, sticky='w')
        tk.Button(self._Frame, text="plot college cost".title(), command= self.plotDialogWindow).grid(row=0, column=2, padx=10, pady=10, sticky='ew')

        # Refactored
    # def plotToplevel_Tuition(self):
    #     '''Purpose: create a toplevel window and call its function to plot tuition trend'''
    #     topWin = ToplevelWindow(self).plotTuitionTrend(self.collegeData)
    #
    # def plotToplevel_RoomBoard(self):
    #     '''Purpose: create a toplevel window and call its function to plot room and board trend'''
    #     topWin = ToplevelWindow(self).plotRoomBoard(self.collegeData)

    def plotDialogWindow(self):
        '''Purpose: create a toplevel dialog window and get user's graduation year to show college options'''
        dialogWin = DialogWindow(self, self.collegeData)
        # dialogWin.grab_set()              # this belongs to dialogWin. An object should set up itself.
        # dialogWin.focus_set()             # this belongs to dialogWin. An object should set up itself.
        # dialogWin.transient(self)         # this belongs to dialogWin. An object should set up itself.

        self.wait_window(dialogWin)  # tell master window to wait for the top level window to close before master resumes other tasks
        year = dialogWin.getYear()
        if year != -1:
            ToplevelWindow(self, self.collegeData.compare_college_cost)



class ToplevelWindow(tk.Toplevel):
    '''
    Purpose: plot 3 plots (tuition trend, room and board trend, total costs) as
             toplevel window when user click on buttons in main window
    Disclaimer:
    The plot window stays opened on screen until the user clicks X on it to close, or until the user clicks X on the main window to close the entire application.
    There can be multiple plot windows on screen if the user chooses to plot multiple times and doesn't close the plot windows.
    '''

    def __init__(self, master, plotFct, *args, **kwargs):
        super().__init__(master)
        self.title("Plot")
        self.minsize(550,500)
        self.transient(master)  # Makes this a transient window (is always drawn on top of its master)

        fig = plt.figure()     # create a matplotlib figure
        plotFct(*args, **kwargs)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()   # position canvas in the window
        canvas.draw()


class DialogWindow(tk.Toplevel):

    def __init__(self, master, collegeData):
        '''
        Purpose: display a toplevel window and get the year of graduation from the user.
        '''
        super().__init__(master)
        # self.title("College")     # maybe inherit
        self.minsize(300,80)
        self.geometry("+300+300")

        tk.Label(self, text="Enter a year of graduation or press Enter for the latest year (" + str(collegeData._end_year) + ")").grid()

        self.grad_year_string = tk.StringVar()
        self.collegeData = collegeData      # a pointer, appropriate collegeData to become a member data


        self.E = tk.Entry(self, textvariable=self.grad_year_string)
        self.E.grid(row=0, column=1)
        self.E.bind("<Return>", self.validateYear)

        self.grab_set()
        self.focus_set()
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", lambda : self._close) # if the user uses X to close the window without entering any year, there should not be a plot. Override the X to pass back a value so that the main window doesn't plot.

    def validateYear(self, event):
        '''
        Purpose: called when user pressed Enter, it validate user year input
                 and pop up error message window if input is invalid
        '''
        self.errorFlag = False
        if self.grad_year_string.get() == '':
            self.collegeData._grad_year = self.collegeData._end_year
        else:
            try:
                self.collegeData._grad_year = int(self.grad_year_string.get())
                # print(self.grad_year)
                if self.collegeData._grad_year not in range(self.collegeData._start_year + 3, self.collegeData._end_year + 1):
                    self.errorFlag = True
            except ValueError:
                self.errorFlag = True

        self.E.delete(0, tk.END)		# clears out the entry widget

        # print(self.grad_year)
        if self.errorFlag:
            # print(self.grad_year_string)
            # print("error with input")
            errorMs = "Year must be 4 digits between " + str(self.collegeData._start_year + 3) + " and " + str(self.collegeData._end_year)
            tkmb.showerror("Error", errorMs , parent=self)
        else:
            self.destroy()

    def _close(self, master):
        '''
        Callback function
        Purpose: if the user uses X to close the window without entering any year, there should not be a plot. Override the X to pass back a value so that the main window doesn't plot.
        '''
        print("Here")
        self.grad_year_string.set(-1)
        self.destroy()

    def getYear(self):
        return self.collegeData._grad_year

def main():

    # # print(college._data)
    # college.plot_tuition()
    # college.plot_room_and_board()
    # college.compare_college_cost()

    app = mainWindow()
    app.mainloop()


if __name__ == '__main__':
    main()





'''Output:
#1: Testing FileIO exception
Could not read input file tuition.csv

'''
