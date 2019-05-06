import json
from difflib import get_close_matches
import tkinter as tk                        # for GUI
import tkinter.messagebox as tkmb   # for error window

class Dictionary:
    def __init__(self):
        self.dict = json.load(open("data.json"))     # dictionary of key and value is a list

    def translate(self, word):
        '''
        Purpose: Search for word in dictionary. If user input is wrong, find the closest match to that input in our dictionary
        Params: w - word user input , dict - our dictionary
        Return: True if found, False if not found
        '''

        if word.lower() in self.dict:
            return self.dict[word]
        elif word.title() in self.dict:         # for example: 'Crimean Federal District'
            return self.dict[word.title()]
        elif word.upper() in self.dict:         # for example: USA or NATO
            return self.dict[word.upper()]

        # if user mispell
        elif len(get_close_matches(word, self.dict.keys())) > 0:
            yn = input("Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(word, self.dict.keys())[0]).lower()
            if yn == "y":
                return self.dict[get_close_matches(word, self.dict.keys())[0]]
            elif yn == "n":
                 return "The word doesn't exist. Please double check it."
            else:
                return "We didn't understand your entry."
        else:
            return "The word doesn't exist. Please double check it."


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

        L = tk.Label(self, text="Enter a word you want to look up: ", font=("Arial", 18, "bold")).grid(sticky='w')
        # instance variables because we need to access them in another method of this class
        self.input_word = tk.StringVar()
        self.E = tk.Entry(self, textvariable=self.input_word)
        self.E.grid(row=0, padx=300, sticky='w')          # must be seperated from the self.E because AttributeError: 'NoneType' object has no attribute 'bind'
        self.E.bind("<Return>", self.getDefinition)     # python doesn't wait for callback to finish

        self.L1 = tk.Label(self, text='', font=("Arial", 16, "bold"))       # for word
        self.L1.grid(sticky='w', pady=10)
        self.L2 = tk.Label(self, text='', font=("Arial", 14))       # for defintion
        self.L2.grid(sticky='w', padx=30)

    def getDefinition(self, event):
        '''
        Purpose: Display the definition of the word user inputs if found in our dictionary.
                 If not found, display message on the window
                 Auto clear the input field after user press Enter
        Params, Ret: none
        '''
        word = str(self.input_word.get())
        result = Dictionary().translate(word)   # return a list of definition
        print(result, "\n\n")

        # Overwrite word
        self.L1.config(text=word.title())
        # Overwrite definition
        for i in range(len(result)):
            result[i] = result[i].replace("e.g.", "for example: ")
            result[i] = result[i].replace(". ", ".\n")

            result[i] = result[i].replace(".\\n", ".\n")

        definitions = '\n'.join(result)
        print(definitions)

        
        self.L2.config(text=definitions, anchor="w", justify="left")
        # self.L2.grid(sticky="w")

        self.E.delete(0, tk.END)        # clear out the entry widget



def main():
    app = mainWin()
    app.mainloop()


if __name__ == "__main__":
    main()
