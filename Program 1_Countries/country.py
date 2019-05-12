# Author: Anh Pham
# Country class, whose member variables are name, continent, population density, and literature rate

import re

class Country:
    def __init__(self, line):
        ''' Constructor
         Purpose: Parsing input line
                  All member variables are strings
         Params: line (str) - a line from input
        '''
        self._list = []

        mo = re.search(r'"?([^"]*)"?\s*,([^,]*)\s*,([\d.]*),([\d.]*)', line)
        if mo:
            self._list = [x.strip() for x in mo.groups()]

        # if line.startwith('"'):
        #     line = line.replace(',', ';' , 1)
        
        # Change the countries' names that contain a comma to a semicolon
        if (self._list[0].find(",") != -1):
            self._list[0] = self._list[0].replace(",", ";")

        # All of these instance variable are strings
        self._name, self._continent, self._pop_den, self._lit_rate = self._list

        # if literacy rate is not provided
        if (self._lit_rate == '' ):
            self._lit_rate = -1


    def __str__(self):
        '''Print country's name'''
        return self._name


    def get_name(self):
        ''' return country's name'''
        return self._name

    def get_continent(self):
        ''' return country's continent '''
        return self._continent

    def get_pop_den(self):
        ''' return population density '''
        return float(self._pop_den)


    def get_lit_rate(self):
        ''' return literacy's rate'''
        return float(self._lit_rate)
