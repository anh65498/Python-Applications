# Table of Content
- CSV file

- numpy

- Plotting data with matplotlib

- GUI with tkinter







## CSV file

```python
import csv

# Read 1 line at a time and split each line into a list of field values

with open(‘infile.csv’) as fh :
      reader = csv.reader(fh)        # reader object is an iterator
      for row in reader :                # each row is a list of fields in a line
            print(row[0], row[-1])    # print the first and last fields
# Write a list of data into a comma separated line in the output file
with open(‘outfile.csv’, ‘w’, newline='') as file :
     writer = csv.writer(file)         # create a writer object
     for aList in table :                 # table is a list of lists of data to be written to file
        writer.writerow(aList)    # write the list to file as a comma separated line
```



## numpy
> import numpy as np

- numpy basic data type is an array. Each array only contain 1 type of data, either integers or floats

#### Create a numpy array
```python
import numpy as np
arr = np.array([1, 3.4, 2.5, 7])   
output:   [1.  3.4   2.5   7. ]
```

#### Check data type of array
`print(ar.dtype)`

#### Change data type of array
```python
intArr = arr.astype(int)    
# convert array of float to int
```   
#### Array Dimension
- Get dimension of an array as a tuple of (# of rows, # of columns)
`print(arr.shape)`

- Change the dimension of an array by assigning a tuple of (num rows, num cols) to the shape attribute. The new array's rows * columns must be the same before and after the dimension change.
`arr.shape = (3,4)`

#### Access Array with Integer Index
- 1D array
```python
arr[0]	# first element
arr[-1]	# last element
arr[:3]	# first 3 elements, using a slice
```

- 2D array
```python
arr[2, 0]       	 # 1 element at 3rd row, 1st column
arr[-1, :3]     	 #  last row, first 3 elements
arr[:2, 4:8]	 #  elements in the first 2 rows, from 5th to 8th columns
arr[: , :2]       # entire row of first 2 column
```

#### Access Array with Integer Index
```python
arr = np.array([ [4, 7, 3, 4, 2], [2, 6, 4, 9, 8] ])
print(arr <= 4)          # output:    [ [True  False  True  True   True]                                                             	      [True  False  True  False  False] ]
print(arr[arr <= 4])                  # output:    [ 4  3  4  2  2  4  ]

```      

#### Initialize numpy Array with List
- Convert a list to a 1D array, and a 1D array to a list
```
arr = np.array([1, 3.4, 2.5, 7])	     
# arr =  [1.  3.4   2.5   7. ]
L = list(arr)		     
# L = [1.0, 3.4, 2.5, 7.0]
```
- Convert 2D array needs to be created from a list of lists, and 2D numpy array back to list of lists
```
arr = np.array( [[2, 4, 6], [5, 6, 7]] )
# arr =   [ [2  4  6]  [5  6  7] ]
L = [list(row) for row in list(arr)]     
# L = [[2, 4, 6], [5, 6, 7]]
```


## Plotting Data with matplotlib

####  Add title for the plot:    

`plt.title(“plot title”)`

#### Change the font size of labels & titles:    

`plt.xlabel(“x label text”, fontsize=12)`



## GUI with tkinter
#### GUI w/o OOP

```python
import tkinter as tk

# create a main window object
win = tk.Tk()     
# change the title
win.title("Main Window")    
# change the background color of the window
win.configure(bg='black')   # or blue, cyan, gray, green, magenta, maroon, orange
# change the min/max size to a larger dimension
win.minsize(w,h)    #width and height are integers, in pixel
win.maxsize(w,h)
# to set location of the Window
geometry("+xStart+yStart")

win.mainloop()   # window stays open til [x] is clicked
```


#### Set up location of components (labels, buttons, ...) in the window
***Without callign pack() or grid() on the component, it will not be displayed in the window***

`pack()` will place each component vertically, center of window and on top of each other, starting at first line
`pack(side=tk.RIGHT)` or `pack(side=tk.LEFT)` will place component side-by-side on 1 line, right-aligned or left-aligned, starting at middle of the window


```python
win = tk.Tk()

tk.Label(win, text="red", fg="red").pack()
tk.Label(win, text="blue", fg="blue").pack()

tk.Label(win, text="orange", fg="orange").pack(side = tk.RIGHT)
tk.Label(win, text="magenta", fg="magenta").pack(side = tk.RIGHT)

tk.Label(win, text="pink", fg="pink").pack(side = tk.LEFT)

win.mainloop()
```
// insert drawing






`grid(row=n, column=m, columnspan = 2)` (take up col m and m+ 1)
`grid(row=n, column=m, rowspan = 3)`  (take up rows n, n+1, and n+2)

- If no row or column is specified, the row defaults to the next available row and the column defaults to 0.

- If a specified row (or column) number is larger than the current max row (or column) number, grid puts the component in the next available row (or column), but this means more components can be inserted in front of the newly specified location.

#### Grid method: resize (fill in later)





#### Passing Python data to tkinter graphic component

- tkinter provides 4 data classes that we can use to translate our Python data type into a corresponding Tk data type: `StringVar` ,	`IntVar` , `DoubleVar` , `BooleanVar`

- The 4 tkinter data classes have:
&nbsp;&nbsp;&nbsp;&nbsp;&nbspm;&nbsp + `get()` method: to fetch data out of the data object into a Python data type
&nbsp;&nbsp;&nbsp;&nbsp;&nbspm;&nbsp + `set()`` method: to store a Python data type into the data object

- Example: Create a Label with string and a Label with number

```python
myStr = tk.StringVar().set("hello")	# create tkinter string object
L = tk.Label(textvariable = myStr)  # create a label with the Tk string in myStr
L.grid()

randNum = tk.IntVar().set(1234)
tk.Label(win, textvariable = randNum).grid()
```
// insert drawing



### Widgets
- Components of the GUI window that display data or get input from the user. Example:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Label: display text or image
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Entry: read in a line of text from the user
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Button: provide a button for the user to click
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Radiobutton: provide a radio button for the user to select a choice
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Canvas: display graphics
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Listbox: display multiple lines of text that can be selected
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Scrollbar: used when there are more items than the listbox display size
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + MessageBox: display a pop up message in a new window

### Container Widgets
- Frame: a grouping of related widgets

- Toplevel: a separate window that is spawned from the main window

### Label Widget
+ Display a line of text or an image in a window

Literal string
```
L = tk.Label(master, text=“text string to display”).grid()`  
# change the "text" string
L["text"] = "new text string to display"
```

String object
```
myStr = tk.StringVar().set("hello")  
tk.Label(textvariable = myStr).grid()  # create a label with the Tk string in myStr
```

#### Button Widget
+ Display a button for the user to click, which will perform some task.

`B = tk.Button(masterWindow, text=“description”, width=N, command=cbfName)`

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - text is the description printed on the button
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - width is the size of the button
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - functionName is a **callback function** , which will perform a task when the button is pressed.

***Callback Function***
- If the callback function has input arguments, use this format
`b = tk.Button(text = “click here”, command=lambda : cbfName(arg))`


#### RadioButton Widget
To create a radiobutton:
`RB = tk.Radiobutton(master, text=“description”, variable=control_var, value=val, command=cbfName)`
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + description is a text string to describe the choice for the button
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + control_var is a Tk variable that can store an int or a string. All buttons in the set must use the same control_var.
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + val is the same data type as control_var, it is the unique ID that we give to each radiobutton in the set

- When a choice is clicked, the value of the choice is stored in controlVar. We can write code that uses this value to make a decision to do one task vs. another.

- Example:
```
controlVar = tk.IntVar()
tk.Radiobutton(win, text="Choice 1", variable=controlVar, value=1,command=callbackfnt).grid()
tk.Radiobutton(win, text="Choice 2", variable=controlVar, value=2).grid()
tk.Radiobutton(win, text="Choice 3", variable=controlVar, value=3).grid()
```

#### Entry
- Read in a line of text from user

```
entryText = tk.StringVar()		# create StringVar to store user input
def fct(event) : 			# callback function that:
    print("Hi,", entryText.get()).      #  prints Hi and user input name in CLT
    E.delete(0, tk.END)		#  - then clears out the entry widget
L = tk.Label(win, text="Enter your name: ").grid()	# create label for prompt
E = tk.Entry(win, textvariable=entryText)   # create entry for user input
E.grid(row=0, column=1)
E.bind("<Return>", fct)		# bind Return / Enter key to callback fct
```
// draw photo

#### Frame Widget
- Group widgets that work together

- A window can contain multiple frames. A frame can contain other frames

```
win = tk.Tk()
entryText = tk.StringVar()		# to store user input

def fct(event) : 			# callback function that:
    F2 = tk.Frame(win)
    L = tk.Label(F2, text=entryText.get()).pack()
    E.delete(0, tk.END)		#  - then clears out the entry widget
    F2.pack()

F1 = tk.Frame(win)
L = tk.Label(F1, text="Enter your message: ").grid()	# create label for prompt
E = tk.Entry(F1, textvariable=entryText)   # create entry for user input
E.grid(row=0, column=1)
E.bind("<Return>", fct)		

F1.pack()

win.mainloop()
```
// draw photo






#### Toplevel widget

- When a top level window appears it is important to:
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Disable events in other windows
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; + Put the focus on the current top level window

- If the master of the top level window has other tasks to do after creating the top level window, then the master might need to wait for the top level window to close before the master resumes the other tasks.

```
topWin = tk.Toplevel(master)
topWin.grab_set()          # ‘grab’ event input, disabling events for other windows
topWin.focus_set()         # set focus on current window
topWin.transient(masterWin)
master.wait_window(topWin)
```

#### Closing Window
```
win.destroy()         # close current window
```

- When user click [X] but we don't want to close the window immediately, we override

```
win.protocol(“WM_DELETE_WINDOW”, callback_fct)
```

#### Structuring GUI code

- Example of main window class and top level window class

```python
import tkinter as tk
class DisplayWin(tk.Toplevel):
    def __init__(self, master):      
        super().__init__(master)    
        tk.Label(self,text="Hi!").grid()

        tk.Button(self, text="Return 5 to main window and close this Top Level Window", command=self.ret5).grid()
        self.grab_set()          # ‘grab’ event input, disabling events for other windows
        self.focus_set()         # set focus on current window
        self.transient(master)  # top level window to be transient to its master window # works for window

    def ret5(self):
        self.val = 5
        self.destroy()       # window gets destroy but object still stays

    # Preq: button is pressed and ret5 runs
    def get5(self):         # need get method because val is a member of class DisplayWin, not MainWin
        return self.val

class MainWin(tk.Tk):
    def __init__(self):
        super().__init__()              # run the constructor of tk. Pass nothing because this is main window

        self.geometry("+500+500")
        self.title("Main Window")
        tk.Button(self, text="say hi", command=self.sayhi).pack()  # no input arg == no lambda

    def sayhi(self):
        self.top = DisplayWin(self)
        self.wait_window(self.top)   # wait for top level's button to be closed to proceed
        tk.Label(self, text=self.top.get5()).pack()       # window gets destroy but object still stays until garbage collection


app = MainWin()
app.mainloop()
```
