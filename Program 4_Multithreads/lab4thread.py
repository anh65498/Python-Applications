# Anh Pham and Omar Burney
# An application that lets the user look up US national parks within a state
# so that they can plan their summer vacation trips.

# problem: Select up to 3 state is not aligned center

import requests
import json
import tkinter as tk
import tkinter.messagebox as tkmb
import  threading

BaseURL = "https://developer.nps.gov/api/v1"
APIkeys = "Dd2O3pfwKcMrRVm2TQP4tvlGGbNffyYriLglLPdh"
MAX_STATES = 3          # number of maximum states user can choose
INPUT_FILE = "states_hash.json"

class MainWin(tk.Tk):
    '''
    Purpose: Display a Main Window, asks user to select up to 3 states from the listbox
    of 50 states (the state names come from the states_hash.json file)
    and display status messages later after user selection.
    '''
    def __init__(self, ):
        # create a dictionary of state code - state name
        with open(INPUT_FILE, 'r') as fh:
            self.state_dict = json.load(fh)

        self.finished_fetching = False       # flag for fetching data via API
        self.list_of_dict    = []            # list of dictionary of parks facts
        self.event = threading.Event()                # for display window to run after fetching data finishes
        self.threads = []

        # create a main window
        super().__init__()
        self.geometry("350x350+100+100")
        self.title("US National Parks")

        L = tk.Label(self, text="Select up to {} states".format(MAX_STATES), anchor="center")
        L.grid(row=0, padx=20)

        # create a listbox
        frame = tk.Frame(self)
        self.listbox = tk.Listbox(frame, height=10, width=30, selectmode="multiple")
        scrollbar = tk.Scrollbar(frame, orient="vertical")      # create a scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")         # row should be the same as listbox. ns means the widget should be stretched vertically to fill the whole cell
        frame.grid(row=1, padx=35)

        for names in self.state_dict.values():
            self.listbox.insert(tk.END, names)

        self.listbox.bind('<<ListboxSelect>>', self.callbackFct)

        tk.Button(self, text="OK", command=self.checkNumChoice).grid(padx=20)  # no input arg == no lambda

        self.status_label = tk.Label(self, text="Status_message")
        self.status_label.grid_forget()        # use grid_forget() to hide


    def callbackFct(self, event):

        values = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        print (', '.join(values))

    def checkNumChoice(self):
        '''
        Purpose:
        When the user clicks OK in main window, check that there are 1 - 3 choices
        from the listbox.  If there are no choices or more than 3 choices,
        pop up an error window to display the error message.
        Then let the user choose from the states again.
        '''

        self.choices = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        if len(self.choices) < 1 or len(self.choices) > MAX_STATES:
            # pop up an error window
            tkmb.showerror("Error", "Please choose between 1-{} states".format(MAX_STATES), parent=self)
            #let user choose again
        else:
            aStringVar = tk.StringVar()         # to update label of state name and park
            self.dataCounter = 0                # counter to display toplevel window once all threads finish running
            # For each choice, create a thread to fetch data for the state that the user chooses.
            # print(self.choices)
            # print(len(self.choices))
            for state_name in self.choices:
                t = threading.Thread(target = self.fetchData, args = (state_name, aStringVar))
                self.threads.append(t)

            for t in self.threads:
                t.start()

            # for t in self.threads:
            #     t.join()
            self.after(3000, self.displayData)



    def displayData(self):
        # if self.finished_fetching:
        # wait = self.event.wait()
        if self.finished_fetching:
            print("Finished fetching")
            dialog_win = displayWindow(self, self.list_of_dict, self.choices)
        # master.wait_window(dialog_win)  # master wait for the top level window to close before the master resumes the other tasks.
        else:
            self.after(3000, self.displayData)

    def fetchData(self, state_name, aStringVar):
        '''
        What: Callback function of thread(s) that user create from 1-3 choices of states in listbox
        Purpose: Fetch data for the state that the user chooses. 
                As it finishes fetching the data, update blank label at the bottom of the window to display the state name and the number of parks there are in the state.
        '''
        # get state code from user's input of state's name
        # state_name = input("Enter a state's name you want to look up: ").title()
        for k, v in self.state_dict.items():
            if v == state_name:
                state_code = k
            # what if there's no match?????
        URL = BaseURL + "/parks?stateCode={0}&api_key={1}".format(state_code, APIkeys)

        page = requests.get(URL)
        resultDict = page.json()
        self.list_of_dict.append(resultDict)            # dictionary of park datas fetched from API
        # print(resultDict, end="\n\n")

        status_string = aStringVar.get()

        aStringVar.set(status_string + state_name + ": " + resultDict["total"] + " parks"+ "  ")

        # update label that show state name : number of parks
        self.status_label.config(textvariable=aStringVar, justify="left")
        self.status_label.grid()
        lock = threading.Lock()
        with lock:
            self.dataCounter += 1           # keep counter to display toplevel window once all threads finish running
            print(self.dataCounter)
            if self.dataCounter == len(self.choices):
                print("Yeah")
                self.finished_fetching = True
                # self.event.set()
        # print(self.dataCounter)
        # could use a Queue here
        # thread is still running

class displayWindow(tk.Toplevel):
    def __init__(self, master, list_of_dict, choices):
        '''
        Params:     resultDict  - dictionary of parks' data fetched from API
                    choices     - list of strings of state name that user choose from listbox in main window
        '''
        super().__init__(master)
        self.grab_set()          # ‘grab’ event input, disabling events for other windows
        self.focus_set()         # set focus on current window
        self.transient(master)

        super().__init__()
        self.geometry("550x350+100+100")

        L = tk.Label(self, text="Select parks to save to file")
        L.grid(row=0, padx=20)

        # create a listbox
        frame = tk.Frame(self)
        scrollbar = tk.Scrollbar(frame, orient="vertical")      # create a scrollbar
        self.listbox = tk.Listbox(frame, height=15, width=30, selectmode="multiple", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side="left")
        scrollbar.pack(side="right", fill="y")         # row should be the same as listbox. ns means the widget should be stretched vertically to fill the whole cell
        frame.grid(row=1, padx=35)

        state_names = [name for name in choices]
        park_names  = [park for park_data in list_of_dict for park in park_data["data"]]
        # prolly do zip() here

        for i in range(len(state_names)):
            for j in range(int(list_of_dict[i]["total"])):
                self.listbox.insert(tk.END, state_names[i] + ": " + list_of_dict[i]["data"][j]["fullName"])

        # print(state_codes)
        # self.listbox.bind('<<ListboxSelect>>', self.callbackFct)

        # tk.Button(self, text="OK", command=self.checkNumChoice).grid(padx=20)

def main():
    # look up state code using states_hash.json
    # create a dictionary of state code - state name

    app = MainWin()
    app.mainloop()


if __name__ == "__main__":
    main()


# resultDict only contain 1 dictionary of the last park. On point 1 of displayWin
