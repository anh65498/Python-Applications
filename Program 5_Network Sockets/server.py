# Anh Pham
# The server code simulates a server that's running at a remote site. The server accepts a request from a client and  produces an output data set for the client.

import socket
import sys          # to accept command line arguments
import numpy as np
import pickle
import threading

# Global constant
HOST = '127.0.0.1'
PORT = 5555
DATA_POINTS = 50
MAXCLIENT = 4
MIN_TIMEOUT = 10
MAX_TIMEOUT = 30


def printMinMax(funct):
    '''Purpose: print the max and min of the return values of a function'''
    def wrapper(*args, **kwargs):
        arr  = funct(*args, **kwargs)
#*args and **kwargs of existingFunction, not wrapper
        print("Min: ", arr[1].min(), ". Max: ", arr[1].max())
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
    return (arr, np.sin(frequency * 2 * np.pi * arr))

def respond(conn, addr):
    '''
    Purpose: target function of thread, receive and send data to client request
    Params: conn - socket
    '''
    while True:
        fromClient = conn.recv(1024)  # receive a tuple of graph type and argument list) from client
        user_input = pickle.loads(fromClient)

        # print("From client:", addr)
        # print("Received:", user_input)

        # get choice and args for graph from client
        if user_input[0] == 'q':
            conn.close()
            break

        graphType, argsList = user_input #(menu_choice, argsList)
        # print(*argsList)

        # get dataset depending on client
        if graphType == 'p':
            dataSet = power(*argsList)
        elif graphType == 's':
            dataSet = sine(*argsList)

        # send back data set to client
        bstring = pickle.dumps(dataSet)
        conn.send(bstring)

def startConnections(timeout, s):
    try:
        (conn, addr) = s.accept()

        # accept client request
        # accept() is blocking, it waits until there is a request from a client.
        # 'conn' is a new socket object that is used by the server to send and receive data with the client
        # 'addr' is the address bound to the client socket
        # only alive as long as s is alive


        t= threading.Thread(target = respond, args = (conn,addr))
        t.start()
        t.join()

    except socket.timeout:     	# exception when the timer times out
        print("No request from client. Socket timeout. Release the socket.")


def main():
    if len(sys.argv) != 3 :
        print("This program accepts 2 arguments from CLI!")
        sys.exit()

    threads = []
    # get number of client and timer from CLI
    try:
        numClient  = int(sys.argv[1])
        timeout     = int(sys.argv[2])
        if numClient > MAXCLIENT:
            print("This program accepts up to " + str(MAXCLIENT) + " clients please")
            sys.exit()
        if timeout < MIN_TIMEOUT or timeout > MAX_TIMEOUT:
            print("This program accepts a timer between " + str(MIN_TIMEOUT) + " and " + str(MAX_TIMEOUT))
            sys.exit()
    except ValueError:
        print("This program only accepts integers!")
        sys.exit()


    with socket.socket() as s :
        s.bind((HOST, PORT))        # bind the server socket to HOST and PORT_NUMBER
        # print("Server hostname:", HOST, "port:", PORT)

        s.listen()              # enable server socket to listen to client's requests
        s.settimeout(timeout)   # raise exception if there's no when there's no incoming client from accept() method. Even when there's a connection establisn already

        for i in range(numClient):
            t= threading.Thread(target = startConnections, args = (timeout, s,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

main()
