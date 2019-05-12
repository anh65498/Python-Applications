import json
from difflib import get_close_matches
import tkinter as tk                        # for GUI


class Dictionary:
    dict = json.load(open("data.json"))     # dictionary of key and value is a list

    def __init__(self):
        self._mispell = False
        self._notFound = False

    def translate(self, word):
        '''
        Purpose: Search for word in dictionary. If user input is wrong, find the closest match to that input in our dictionary
        Params: w - word user input , dict - our dictionary
        Return: list of definition if found, list of close matches if user mispell, and empy list if not found
        '''
        if word.lower() in self.dict:
            return self.dict[word]
        elif word.title() in self.dict:         # for example: 'Crimean Federal District'
            return self.dict[word.title()]
        elif word.upper() in self.dict:         # for example: USA or NATO
            return self.dict[word.upper()]

        # if user mispell
        elif len(get_close_matches(word, self.dict.keys())) > 0:
            self._mispell = True
            self._close_matches = get_close_matches(word, self.dict.keys())     # list of the best “good enough” matches
            print(self._close_matches)
            # yn = input("Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(word, self.dict.keys())[0]).lower()
        else:
            self._notFound = True
            print("Not found")



class mainWin(tk.Tk):
    def __init__(self):
        '''
        Purpose: Create and display the main window that let user enter a word to look up
                 and display the definition if found
        '''
        self.word = ""
        super().__init__()              # run the constructor of tk. Pass nothing because this is main window
        self.minsize(550, 200)

        self.geometry("+150+250")
        self.title("English Dictionary")

        # Input field
        L = tk.Label(self, text="Enter a word you want to look up: ", font=("Arial", 18, "bold")).grid(sticky='w')
        # instance variables because we need to access them in another method of this class
        self.input_word = tk.StringVar()
        self.E = tk.Entry(self, textvariable=self.input_word)
        self.E.grid(row=0, padx=300, sticky='w')          # must be seperated from the self.E because AttributeError: 'NoneType' object has no attribute 'bind'
        self.E.bind("<Return>", self.getDefinition)     # python doesn't wait for callback to finish

        # Label for word
        self.L1 = tk.Label(self, text='', font=("Arial", 16, "bold"))       # for word
        self.L1.grid(pady=10)

        # Label for definition
        self.L2 = tk.Label(self, text='', font=("Arial", 14))
        self.L2.grid(padx=30)

    def getDefinition(self, event):
        '''
        Purpose: Display the definition of the word user inputs if found in our dictionary.
                 If not found, display message on the window
                 Auto clear the input field after user press Enter
        Params, Ret: none
        '''
        self._word = str(self.input_word.get())
        self._myDict = Dictionary()
        result = self._myDict.translate(self._word)   # return a list of definition

        print(self._myDict, "\n")
        print(type(self._myDict), "\n\n")
        print(result, "\n")
        print(type(result), "\n\n")


        # if user type BS
        if self._myDict._notFound:       # ????? 'NoneType' object has no attribute '_found'
            print("No word match your input.")
            self.L1.config(text=self._word, justify="left")
            self.L2.config(text="No definition found for your input", justify="left")
            return
        elif self._myDict._mispell:
            self.getCloseMatch()
        else:
            # user type word correctly
            self.printWord(self._word)

        self.E.delete(0, tk.END)        # clear out the entry widget

    def printWord(self, word):
        '''
        Display word and definition to screen, used for both when user enter right word and mispell
        '''
        # Overwrite word
        print("Word inside printWord is", word)

        self.L1.config(text=word.title())
        result = self._myDict.translate(word)   # return a list of definition

        # Overwrite definition in data.json to display
        for i in range(len(result)):
            result[i] = result[i].replace("e.g.", "for example: ")
            result[i] = result[i].replace(". ", ".\n")
            result[i] = result[i].replace(".\\n", ".\n")

        definitions = '\n'.join(result)
        print(definitions)

        self.L2.config(text=definitions, justify="left")

        self.L1.grid()
        self.L2.grid()

    def getCloseMatch(self):
        '''
        Purpose: Display the definition of the word user inputs if found in our dictionary.
                 If not found, display message on the window
                 Auto clear the input field after user press Enter
        Params, Ret: none
        '''
        self.L1.grid_forget()
        self.L2.grid_forget()


        self._controlVar = tk.IntVar()
        self.rb1 = tk.Radiobutton(self, text=self._myDict._close_matches[0], variable=self._controlVar, value=0, command= lambda : self.chooseWord(self._controlVar))
        self.rb1.grid()       # hide this radiobutton until callbackfnt
        self.rb2 = tk.Radiobutton(self, text=self._myDict._close_matches[1], variable=self._controlVar, value=1, command= lambda : self.chooseWord(self._controlVar))
        self.rb2.grid()       # hide this radiobutton
        self.rb3 = tk.Radiobutton(self, text=self._myDict._close_matches[2], variable=self._controlVar, value=2, command= lambda : self.chooseWord(self._controlVar))
        self.rb3.grid()
        # self.rb4 = tk.Radiobutton(self, text="The word doesn't exist. Please double check it.", variable=self._controlVar, value=3, command= lambda : printNoMatch())
        # self.rb4.grid()

    def chooseWord(self, controlVar):
        '''
            Purpose: Once the user choose one of the close match, will hide the radio button
                     and display the word and definition
        '''
        chosenWord = self._myDict._close_matches[controlVar.get()]

        self.rb1.grid_forget()
        self.rb2.grid_forget()
        self.rb3.grid_forget()
        # self.rb4.grid_forget()

        self.printWord(chosenWord)


def main():
    app = mainWin()
    app.mainloop()


if __name__ == "__main__":
    main()

# Future feature:
## 1) Add definition to word. For example: "ghoul" isn't registered in data.json
