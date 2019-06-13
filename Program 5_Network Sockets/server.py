# Anh Pham
# The server code simulates a server that's running at a remote site. The server accepts a request from a client and  produces an output data set for the client.

import socket
import sys          # to accept command line arguments
import numpy as np
import pickle

# Global constant
HOST = '127.0.0.1'
PORT = 5555
DATA_POINTS = 50
# DATA_POINTS = 10

def printMinMax(funct):
    '''Purpose: print the max and min of the return values of a function'''
    def wrapper(*args, **kwargs):
        arr  = funct(*args, **kwargs)
#*args and **kwargs of existingFunction, not wrapper
        print("Smallest return value: ", arr[1].min())
        print("Biggest return value: ", arr[1].max())
        return arr
    return wrapper       # rule 2 of closure

@printMinMax
def power(exponent, min, max):
    arr =  np.linspace(min, max, DATA_POINTS)
    # send the array back to client
    return (arr, arr**exponent)

@printMinMax
def sine(frequency):
    arr =  np.linspace(0, 1, DATA_POINTS)
    # send the array back to client
    return (arr, np.sin(arr))


if len(sys.argv) != 3 :
    print("This program accepts 2 arguments from CLI!")
    sys.exit()

try:
    max_client  = int(sys.argv[1])
    timeout     = int(sys.argv[2])
except ValueError:
    print("This program only accepts integers!")
    sys.exit()


with socket.socket() as s :

    s.bind((HOST, PORT))        # bind the server socket to HOST and PORT_NUMBER
    print("Server hostname:", HOST, "port:", PORT)

    s.listen()                  # enable server socket to listen to client's requests
    (conn, addr) = s.accept()   # accept client request
    # 'conn' is a new socket object that is used by the server to send and receive data with the client
    # 'addr' is the address bound to the client socket
    while True:
        fromClient = conn.recv(1024)  # receive a tuple of graph type and argument list) from client
        user_input = pickle.loads(fromClient)
        print("From client:", addr)
        print("Received:", user_input)

        # get choice and args for graph from client
        if user_input[0] == 'q':
            break

        graphType, argsList = user_input #(menu_choice, argsList)
        print(*argsList)

        # get dataset depending on client
        if graphType == 'p':
            dataSet = power(*argsList)
        elif graphType == 's':
            dataSet = sine(*argsList)

        # send back data set to server
        bstring = pickle.dumps(dataSet)
        conn.send(bstring)
