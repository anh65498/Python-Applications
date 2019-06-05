import os
import tkinter as tk
import tkinter.filedialog
import textwrap
import requests
from bs4 import BeautifulSoup
import shutil

CLASSES     = ["4A", "4B", "4C"]
BASE_URL    = "http://nebula2.deanza.edu/~lanasheridan/"


class MainWindow(tk.Tk):
    ''' Main Window: Pop up a window with a label and ask if user want to download at current directory '''
    def __init__(self):
        self.cwd = os.getcwd()
        font = ("Arial", 15)


        super().__init__()
        self.geometry("500x200+300+250")
        self.title("Download Sheridan's Physics letures")

        labelFrame = tk.Frame(self)
        tk.Label(labelFrame, text="Dowload lectures and save to", font= font).pack()
        tk.Label(labelFrame, text=textwrap.fill(self.cwd, width=50), font= ("Arial", 17, "bold")).pack()
        # tk.Label(labelFrame, text=textwrap.fill("Click 'OK' to proceed, 'Change Folder' to change directory, [X] to quit program", width=60), font= font).pack()
        labelFrame.grid(columnspan=6)

        tk.Button(self, text="OK", command=lambda:TopWindow(self, self.cwd)).grid(row=1, column=1)
        tk.Button(self, text="Change Folder", command=self.showFileDialog).grid(row=1, column=3)
        tk.Button(self, text="Cancel", command=self.close).grid(row=1, column=5)
        # get current directory in a string to display in label

    def showFileDialog(self):
        ''' if user click cancel, pop up file dialog to let user choose another directory and cd to cwd '''
        directory = tk.filedialog.askdirectory(initialdir = self.cwd)
        os.chdir(directory)
        self.cwd = os.getcwd()
        print("current directory: ", self.cwd)


    def close(self):
        self.destroy()

class TopWindow(tk.Toplevel):
    def __init__(self, master, cwd):
        super().__init__(master)
        '''Ask user to choose which classes to download lectures'''
        self.title("Choose class(es) to download lectures from")
        self.geometry("400x100+700+250")
        self.grab_set()       # disable grabbing events for other window
        self.focus_set()      # Moves the keyboard focus to this widget

        self.LB = tk.Listbox(self, height=len(CLASSES), width=15, selectmode="multiple")
        self.LB.insert(tk.END, *CLASSES)
        self.LB.grid(columnspan=4)

        tk.Button(self, text="OK", command=lambda:self.downloadLectures(master, cwd)).grid(row=1, column=2)
        tk.Button(self, text="Cancel", command=self.close).grid(row=1, column=4)

    def downloadLectures(self, master, cwd):
        # see which classes user select
        selected = [self.LB.get(index) for index in self.LB.curselection()]
        print(*selected)

        # Create a folder for Physics 4A, 4B, 4C
        for _class in selected:
            if not os.path.isdir(cwd + "/Physics " + _class):
                os.mkdir(cwd + "/Physics " + _class)

            os.chdir(cwd + "/Physics " + _class)
            print(cwd + "/Physics " + _class)
            # First, let's just download all Physics 4C
            # Go online and grab links to each lecture to a generator?
            page = requests.get(BASE_URL + _class + "/Archive-Physics" + _class + "Lectures.html")
            # download each lecture from generator
            soup = BeautifulSoup(page.content, "lxml")
            for link in soup.select('.card a'):
                # print(BASE_URL + "4C/" + link["href"])
                # example: http://nebula2.deanza.edu/~lanasheridan/4C/Phys4C-Lecture49.pdf
                page = requests.get(BASE_URL + _class + "/" + link["href"], stream=True)

                # save your RAM, read and save data in chunk
                # chunk_size = 2000
                # with open(link["href"], 'w') as f:
                     # for block in page.iter_content(chunk_size=128):    # or 256, 1024, 2048
                     #    outfile.write(block)


                # Method 2
                with open(link["href"], 'wb') as f:
                        shutil.copyfileobj(page.raw, f)

            self.destroy()
            master.destroy()

    def close(self):
        ''' Destroy window when user click Cancel '''
        self.destroy()

def main():
    app = MainWindow()
    app.mainloop()

main()
