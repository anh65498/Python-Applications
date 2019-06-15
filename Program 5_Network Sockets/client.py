# Anh Pham
# This script simulates a client, which will display menu, prompt user for input, send input to server and receive data back to plot

import socket
import pickle
import  matplotlib.pyplot  as  plt

HOST = '127.0.0.1'
PORT = 5555

def displayMenu():
    '''Display menu of choices for client to choose from'''
    print("p: power function")
    print("s: sine function")
    print("q: quit")

def processInput():
    '''
    Purpose: input validation
    Return: a tuple of menu choice and list of integers from client
    '''
    menu_choice = None

    while menu_choice not in ['p', 'q', 's']:
        menu_choice = input("Enter choice or q to quit: ")

    if menu_choice == 'p':
        argsList = validateInput("Enter exponent, min-x, max-x: ", 3)
    elif menu_choice == 's':
        argsList = validateInput("Enter frequency: ", 1)
    elif menu_choice == 'q':
        argsList = None
    tup = (menu_choice, argsList)
    return tup


def validateInput(prompt, numArgs):
    ''' Purpose: validate input and number of argument in input
        Ret: 1 integer or list of integers as arguments for plot'''
    while True:
        args = input(prompt)
        if len(args.split(",")) != numArgs:
            print("Please input " + str(numArgs) + " numbers!")
            continue
        try:
            args = [int(x) for x in args.split(",")]
            return args
        except ValueError:
            print("Please only input numbers")
            continue

def main():
    with socket.socket() as s :
        s.connect((HOST, PORT))
        print("Client connect to:", HOST, "port:", PORT)

        # print menu and prompt arguments from user
        displayMenu()
        user_input = processInput()   # tuple of choice and argsList
        # send all user input (type of graph and arguments) to the server
        print("Client is sending: ", user_input)
        bstring = pickle.dumps(user_input)
        s.send(bstring)	# send mesg to server

        while user_input[0] != 'q':
            fromServer = s.recv(1024)	# receive data from server
            dataSet = pickle.loads(fromServer)

            # plot the data set with matplotlib
            plt.title(dataSet[2])
            plt.plot(dataSet[0], dataSet[1])
            plt.xlabel("x")
            plt.show()

            # print menu and prompt arguments from user again
            displayMenu()
            user_input = processInput()   # tuple of choice and argsList
            bstring = pickle.dumps(user_input)
            s.send(bstring)	# send mesg to server

main()
