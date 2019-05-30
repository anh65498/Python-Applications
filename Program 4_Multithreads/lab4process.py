# Anh Pham
# Program description:
#       An multiprocessing application that lets the user look up US national parks within a state
#       so that they can plan their summer vacation trips. Once user choose the states,
#       this program will show a list of park's within those states.
#       User can then choose as many park name as possible to save to a file

import requests
import json
import tkinter as tk
import tkinter.messagebox as tkmb
import multiprocessing as mp
import pickle                           # for multiprocessing
import os
import tkinter.filedialog              # for file dialog


BaseURL = "https://developer.nps.gov/api/v1"
APIkeys = "Dd2O3pfwKcMrRVm2TQP4tvlGGbNffyYriLglLPdh"
MAX_STATES = 3          # number of maximum states user can choose
INPUT_FILE = "states_hash.json"
OUTPUT_FILE = "parks.txt"


class MainWin(tk.Tk):
    '''
    Purpose:    Display a Main Window, asks user to select up to 3 states from the listbox
                of 50 states (the state names come from the states_hash.json file)
                and display status messages later after user selection.
    '''
    def __init__(self, ):
        # create a dictionary of state code - state name
        with open(INPUT_FILE, 'r') as fh:
            self.state_dict = json.load(fh)

        # self.list_to_print   = []            # list of state name : park name to display on toplevel
        self.processes = []             # keep track of child processes
        # self.queue = mp.Queue()      # use queue instead of list here because main proc can't wait to fetch all data like in list, main proc display the # data as soon as 1 thread fini
        self.dataCounter = 0                # keep track of number of element in the queue of data fetched



        # create a main window
        super().__init__()
        self.geometry("450x350+100+100")
        self.title("US National Parks")
        self.protocol("WM_DELETE_WINDOW", self.close)

        L = tk.Label(self, text="Select up to {} states".format(MAX_STATES), anchor="center")
        # L.grid(row=0, padx=20)
        L.pack()

        # create a listbox
        frame = tk.Frame(self)
        self.listbox = tk.Listbox(frame, height=10, width=30, selectmode="multiple")
        scrollbar = tk.Scrollbar(frame, orient="vertical")      # create a scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")         # row should be the same as listbox. ns means the widget should be stretched vertically to fill the whole cell
        # frame.grid(row=1, padx=35)
        frame.pack()

        for name in self.state_dict.values():
            self.listbox.insert(tk.END, name)
        # self.listbox.bind('<<ListboxSelect>>', self.callbackFct)  # immediately as user select from listbox, fire callbackFct
        tk.Button(self, text="OK", command=self.startProcesses).pack()  # no input arg == no lambda
        self.status_label = tk.Label(self, text="")
        self.status_label.pack()


    def startProcesses(self):
        '''
        Purpose:
                When the user clicks OK in main window, check if they had choosen 1 - 3 choices from the listbox. 
                If not, pop up an error window to display the error message,
                else, start child processes that fetch data
        '''
        self.choices = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        # if user choose none or more than MAX_STATE, pop up an error window and let user choose again
        if len(self.choices) < 1 or len(self.choices) > MAX_STATES:
            tkmb.showerror("Error", "Please choose between 1-{} states".format(MAX_STATES), parent=self)
        else:
            print(self.choices)

            self.status_label.config(text="Fetching data for {} state(s).".format(len(self.choices)), justify="left")
            args = [[state_name, self.state_dict] for state_name in self.choices ]       # args: [ [state_name, {state_dict}], [state_name, {state_dict}], ]


            # mp.set_start_method('spawn')       # use spawn instead of fork on Mac/Linux
            with mp.Pool(processes=MAX_STATES) as pool:         # normal creation of pool
                results = pool.map(fetchData, args)        # tuple of state_name and resultDict from fetchData all the runs.


            # blocked until all processes are done
            d = displayWindow(self, results)
            self.wait_window(d)

            # for state_name in self.choices:
            #     p = mp.Process(target = fetchData, args = (state_name, self.state_dict, self.choices, self.queue), name=state_name)
            #     self.processes.append(p)
            #     p.start()


    def close(self):
        '''
            Purpose: When user quit the program, end all child processes before ending main thread/main window
        '''
        for p in self.processes:
            p.join()
        # checked with is_alive and all proc are killed
        self.destroy()

    def callbackFct(self, event):
        '''
            Purpose: Immediately as user select from listbox, print the choice use make to terminal
        '''
        values = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        print (', '.join(values))

def fetchData(args):
    '''
    Purpose: This global function fetch data for the state that the user chooses. 
             As it finishes fetching the data, update blank label at the bottom of the window to display the state name and the number of parks there are in the state.
    Params: args    list of tuple of different state_name but same state_dict from state_hash.json.
            Example: [ (state_name, {state_dict}), (state_name, {state_dict}), ]
    '''

    state_name, state_dict = args[0], args[1]       # replace with unpacking later

    for k, v in state_dict.items():
        if v == state_name:
            state_code = k

    URL = BaseURL + "/parks?stateCode={0}&api_key={1}".format(state_code, APIkeys)

    page = requests.get(URL)            # may take a long time
    resultDict = page.json()
    state_name_and_park_data = (state_name, resultDict["data"])

    print(resultDict, end="\n\n")

    # # queue.put( list_to_print )
    #
    # # update status_label of mainWindow
    # lock = mp.Lock()
    # with lock:
    #     dataCounter += 1
    #     print("Number of data fetched now: ", dataCounter)
    #
    # if dataCounter == len(choices):       # remove this variable and replace it with length of queue
    #     print("Finish fetching {} data".format(dataCounter))

    return state_name_and_park_data



class displayWindow(tk.Toplevel):
    def __init__(self, master, results):
        '''
        Params:
                    choices     - user's state choices, in alphabet order of the listbox, not in order of fetch
                    state_dict  - dictionary of state code - state name
                    results     - tuple of state_name and its resultDict from fetchData() all the runs.
        '''
        self.dict_of_list = {}      # list of list to print

        super().__init__(master)
        self.grab_set()          # ‘grab’ event input, disabling events for other windows
        self.focus_set()         # set focus on current window
        self.transient(master)

        self.geometry("550x350+500+100")
        L = tk.Label(self, text="Select parks to save to file")
        L.grid(row=0, padx=20)

        # create a listbox
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame, orient="vertical")      # create a scrollbar
        self.listbox = tk.Listbox(frame, height=15, width=50, selectmode="multiple", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")         # row should be the same as listbox. ns means the widget should be stretched vertically to fill the whole cell
        frame.grid(row=1, padx=35)

        # fill the listbox with state : park's name in order of fetching
        for element in results:
            state_name = element[0]
            park_data  = element[1]   # list of all parks' facts in the state
            self.dict_of_list[state_name] = park_data
            # print(state_name, park_data)
            # print("*****")

            for i in range(len(park_data)):
                self.listbox.insert(tk.END, state_name + " : " + park_data[i]["fullName"])

        tk.Button(self, text="OK", command= lambda: self.printToFile(master)).grid(padx=20)  # no input arg == no lambda

        self.protocol("WM_DELETE_WINDOW", lambda : self.close(master))       # If the user choose to close the display window by clicking 'X'

    def printToFile(self, master):
        '''
        Purpose: check if user has selected at least 1 choice
                 if yes, write the selected parks' fullName, state names, and "description".
                 if no, display message
        '''
        self.choices = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        if len(self.choices) == 0:
            # pop up an error window
            tkmb.showerror("Error: Number of choices", "Please choose at least 1 state")
        else:
            # create a file dialog window to let the user choose a directory to save the output file
            directory = tk.filedialog.askdirectory(initialdir= '.')
            # If the user chooses to cancel from the file dialog window,
            # then the user is back at the display window again and can select parks from the listbox.
            # If the user chooses a directory, check to see if a file named "parks.txt" (global constant) already exists in the user chosen directory. 
            if directory != "":
                # change directory
                # print("User choose: ", directory)
                os.chdir(directory)
                output_path =  os.path.join(directory, OUTPUT_FILE)
                if os.path.isfile( output_path ):
                    #  If it does, warn user that the file will be overwritten. 
                     tkmb.askokcancel("Overwritting existing file", "{} already exists. Click OK and it will be overwritten".format(OUTPUT_FILE), parent=self)
                     # if user click ok, overwrite existing file
                     f= open( output_path, "w")
                     f.close()

                values = [self.listbox.get(idx).split(":") for idx in self.listbox.curselection()]
                '''
                    ['Florida ', ' De Soto National Memorial']
                    ['Florida ', ' Gulf Islands National Seashore']
                    ['Colorado ', ' Black Canyon Of The Gunnison National Park']
                '''

                with open(OUTPUT_FILE, 'a') as fh:
                    for park in values:
                        for data in self.dict_of_list[park[0].strip()]:
                            if data["fullName"] == park[1].strip():
                                description = data["description"]
                                break

                        fh.write( "*** "+ park[1].strip() + ", " + park[0].strip() + "\n")
                        fh.write( description + "\n\n")

            self.close(master)


    def close(self, master) :
        '''
            Purpose: Before closing the displayWindow, clear the status_label of the mainWindow
        '''
        master.status_label.config(text="", justify="left")
        self.destroy()




def main():
    mp.set_start_method('spawn')       # use spawn instead of fork on Mac/Linux
    app = MainWin()
    app.mainloop()


if __name__ == "__main__":
    main()

# look at my data structure, review data structure in lecture 1, homework 1 and homework 2 and homework 3
    # suggestion: when fetch data, parse data for full name and description before putting it in queue

# if user choose to do it again, remember previous state choice in main window


# Future feature: status_label display "Fetching Data" while thread runs and thread will replace it once it fetches data
# Future feature: display address of the choosen park
# Future feature: scale mainwindow to size (when user enlarge the window)
# Future feature spam click the ok button to open multiple windows to pick parks in
