# Anh Pham and Omar Burney
# An application that lets the user look up US national parks within a state
# so that they can plan their summer vacation trips.


import requests
import json
import tkinter as tk

BaseURL = "https://developer.nps.gov/api/v1"
APIkeys = "Dd2O3pfwKcMrRVm2TQP4tvlGGbNffyYriLglLPdh"
max_states = 3          # number of maximum states user can choose


class MainWin(tk.Tk):
    '''
    Purpose: Display a Main Window, asks user to select up to 3 states from the listbox
    of 50 states (the state names come from the states_hash.json file)
    and display status messages later after user selection.
    '''
    def __init__(self):
        super().__init__()
        self.geometry("500x500+300+300")
        self.title("US National Parks")
        tk.Label(self, text="Select up to {} states".format(max_states))


        # tk.Button(self, text="say hi", command=self.sayhi).pack()  # no input arg == no lambda

def main():
    # look up state code using states_hash.json
    # create a dictionary of state code - state name
    # with open('states_hash.json', 'r') as fh:
    #     state_dict = json.load(fh)
    #
    # get state code from user's input of state's name
    # state_name = input("Enter a state's name you want to look up: ").title()
    # for k, v in state_dict.items():
    #     if v == state_name:
    #         state_code = k
    #     # what if there's no match?????
    #
    # URL     = BaseURL + "/parks?stateCode={0}&api_key={1}".format(state_code, APIkeys)
    #
    #
    # page = requests.get(URL)
    # resultDict = page.json()
    # print(resultDict, end="\n\n")

    app = MainWin()
    app.mainloop()


if __name__ == "__main__":
    main()
