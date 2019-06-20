# Anh Pham
# The script simulates a server that's running at a remote site.
# The server accepts a request from a client and  produces an output data set for the client.

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
        # *args and **kwargs of existingFunction, not wrapper
        print("Min: ", arr.min(), ". Max: ", arr.max())
        return arr
    return wrapper       # rule 2 of closure

@printMinMax
def power(conn, exponent, min, max):
    '''
    Purpose: create a numpy array and output array for power function. Send back the output array and plot's title to client's Connection
    Params: conn - client's connection socket, min/max - min/max value for exponent function
    Ret: output array to be used by decorator to print out min and max value
    '''
    arr         =  np.linspace(min, max, DATA_POINTS)
    output_arr  = arr**exponent
    # send the array back to client
    bstring = pickle.dumps((arr, output_arr))
    conn.send(bstring)
    return output_arr

@printMinMax
def sine(conn, frequency):
    '''
    Purpose: create a numpy array and output array for sine function. Send back the output array and plot's title to client's Connection
    Params: conn - client's connection socket, frequency - frequency value for sine function
    Ret: output array to be used by decorator to print out min and max value
    '''
    arr         =  np.linspace(0, 1, DATA_POINTS)
    output_arr  = np.sin(frequency * 2 * np.pi * arr)
    # send the array back to client
    bstring = pickle.dumps((arr, output_arr))
    conn.send(bstring)
    return output_arr



def startConnections(conn):
    '''
    Purpose: time client's response. Any client out of max number of clients created without a response within timeout second will be released
             if there's client reponse within time limit, receive and send data to client request
    Params: s - server socket
    '''
    while True:
        fromClient = conn.recv(1024)  # receive a tuple of graph type and argument list from client
        user_input = pickle.loads(fromClient)

        # get choice and args for graph from client
        if user_input[0] == 'q':
            conn.close()
            break

        graphType, argsList = user_input     # (menu_choice, argsList)

        # run function to send data back to client depending on client's graph choice
        if graphType == 'p':
            power(conn, *argsList)
        elif graphType == 's':
            sine(conn, *argsList)



def main():
    '''
    Purpose: validate command line's argument variables, create a socket and number of threads that user specify in argv to handle connection sockets
    '''
    if len(sys.argv) != 3 :
        print("Usage: python3 server.py number_of_client num_of_secs_timeout!")
        sys.exit()

    threads = []
    # get number of client and timer from CLI
    try:
        numClient  = int(sys.argv[1])
        timeout     = int(sys.argv[2])
        if numClient > MAXCLIENT or numClient < 1:
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
        print("Server is up. Server's hostname:", HOST, ", port:", PORT)
        s.listen()              # enable server socket to listen to client's requests
        try:
            s.settimeout(timeout)   # raise exception if there's no when there's no incoming client from accept() method. Even when there's a connection establisn already
            (conn, addr) = s.accept()       # accept client request
            # accept() is blocking, it waits until there is a request from a client.
            # 'conn' is a new socket object that is used by the server to send and receive data with the client
            # 'addr' is the address bound to the client socket
            # only alive as long as s is alive

            for i in range(numClient):
                t= threading.Thread(target = startConnections, args = (conn,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        except socket.timeout:     	# exception when the timer times out
            print("No request from client. Connection socket timeout. Release the socket.")


main()
