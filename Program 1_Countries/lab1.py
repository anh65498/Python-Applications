# Author: Anh Pham
'''
    From input file lab1in.csv, this program parse country's name, continent, population density and literacy rate
    and
        1. Print countries in descending order of literacy rate
        2. Print countries based on population density
'''
from country import Country
import collections

DEFAULT_IN_FILE = "lab1in.csv.xls"

def getData(filename = DEFAULT_IN_FILE):
    '''
    Params: filename - input file's name
    Ret   : list of Country objects parsed from filename
    Purpose:    Read each line from the input file and create a Country object.
                Store all the Country objects in a list.
                Print the number of countries that are read in.
    '''
    try:
        countryList = []
        with open(filename, "r") as infile:
            for line in infile:
                country = Country(line)
                countryList.append(country)
                # OR:
                # countryList = [Country(line) for line in infile]

        # print the number of countries that are read in
        print("Read in {} countries\n".format(len(countryList)))
        return countryList
    except IOError:
        print("Could not read input file", filename)
        raise SystemExit


def printAll(countryList : list):
    '''
    Params: countryList - list of Country objects
    Purpose: Print a counting number and the name of each Country object in countryList on one line.
    Ret: none
    '''
    for count, country in enumerate(countryList, start = 1):
        print(count, country)


def getChoice():
    '''
    Purpose: Print a menu of 3 choices
             Keep prompting the user until there is a valid choice
    Ret:     user choice.
    Params:  none
    '''
    print("="*60 + "\n" + "l. Print countries in descending order of literacy rate\n" + "d. Print countries based on population density\n")
    print("q. Quit")
    print("="*60)

    #prompt user for correct menu choice
    user_choice = None
    while (user_choice not in ["l", "d", "q"]):
        user_choice = input("Enter your choice: ")
    #OR:
    # match = re.search('^[ldq]$', choice, re.I)
    # while match == NONE:
    #     user_choice = input("Enter your choice: ")

    return user_choice

def retVal(funct):
    '''
    Params:  None
    Ret   :  None
    Purpose: Decorator to print the return value of the function that it decorates.
    '''
    def wrapper(*args, **kwargs) :       # closure,
        result = funct(*args, **kwargs)      # call existing function
        print(result)
        return result
    return wrapper

@retVal
def print_population_density(countryList):
    '''
    Params: countryList - list of Country object
    Purpose: Calculate the population density of each part of the world
             Print the continent name and the population density
    Ret: a tuple of the highest and lowest population density values among the 7 continents (to practice decorator)
    '''

    # dictionary where key is continent and value is a list of all of the population of countries on the continent
    populationDict = collections.defaultdict(list)
    for country in countryList:
        if ("EUROPE" in country.get_continent()):            # Eastern Europe and Western Europe should be counted as Europe.
            populationDict["EUROPE"].append(country.get_pop_den())
        elif ("AFRICA" in country.get_continent()):            # Eastern Europe and Western Europe should be counted as Europe.
                populationDict["AFRICA"].append(country.get_pop_den())
        elif ("LATIN AMER." in country.get_continent()):            # Eastern Europe and Western Europe should be counted as Europe.
                populationDict["SOUTHERN AMERICA"].append(country.get_pop_den())
        else:
            populationDict[country.get_continent()].append(country.get_pop_den())

    # list of max and min population density from 7 continents
    max_pop_den, min_pop_den = [],[]

    for continent, listOfPop in populationDict.items():
        average           = sum(listOfPop)/len(listOfPop)
        max_pop_den.append(max(listOfPop))
        min_pop_den.append(min(listOfPop))
        print("{:20} {:6.1f}".format(continent,average))

    return (max(max_pop_den), min(min_pop_den))

def generate_lit_rate_list(countryList) :
    '''
    Params: countryList - list of Country object
    Purpose: Generator that yields one list of Country objects at a time, in descending range of literacy rate.
    Ret/Yield: list of Country objects in a range
    '''

    upper_limit, lower_limit = 100, 90   # only run in first func call. Later, all the iterator are in infinite loop
    countryList = sorted(countryList, key=lambda t : t.get_lit_rate(), reverse=True)

    while True and lower_limit > 0:
        yield [country for country in countryList if lower_limit < country.get_lit_rate() <= upper_limit]         # list comprehension of x that is within the range
        lower_limit -= 10
        upper_limit -= 10


def get_lit_rate_range(lit_rate_range):
    '''
    Params:  list of countries within a range generated by the generator generate_lit_rate_list
    Purpose: Let user press the Enter key to get a list of countries within a descending literacy rate.
    Ret:     None
    '''

    while(input("Press Enter to see countries and literacy rates, anything else to quit: ") == ''):
        try:
            lit_rate_list = next(lit_rate_range)
            if len(lit_rate_list) == 0:
                print("No literacy data.")
            for country in lit_rate_list:
                print("{:33} {:6.1f}%".format(country.get_name(), country.get_lit_rate()))
        except StopIteration:
            print("No more data")
            break


def main():
    '''
    Params, Ret: none
    Purpose: get and parse data from input file, print the country' names
             display average population density and literacy rate in range
    '''
    countryList = getData()                   # if user want to input another file, put the input file as argument here
    printAll(countryList)
    lit_rate_range = generate_lit_rate_list(countryList)    # create a generator

    # functs is a dictionary with key - user choice, value: (function, function's argument)
    # change function's argument to a list of argument if necessary in the future
    # then functions would take *args
    functs = {
        "l": (get_lit_rate_range, lit_rate_range),
        "d": (print_population_density, countryList),
    }

    user_choice = getChoice()
    while(user_choice.lower() != 'q'):
        op = functs[user_choice]
        argument = op[1]
        op[0](argument)          # we can use this since all of them share the same parameters.
        user_choice = getChoice()


if __name__ == "__main__":
    main()

'''
1) why does import country doesn't work but from country import Country work?

'''

'''Output:
Read in 227 countries

1 Afghanistan
2 Albania
3 Algeria
4 American Samoa
5 Andorra
6 Angola
7 Anguilla
    < cut to save space >
224 Western Sahara
225 Yemen
226 Zambia
227 Zimbabwe
============================================================
l. Print countries in descending order of literacy rate
d. Print countries based on population density
q. Quit
============================================================
Enter your choice: l
Press Enter to see countries and literacy rates, anything else to quit:
Andorra                            100.0%
Australia                          100.0%
Denmark                            100.0%
Finland                            100.0%
Liechtenstein                      100.0%
Luxembourg                         100.0%
      < cut to save space>
China                               90.9%
Peru                                90.9%
Zimbabwe                            90.7%
Vietnam                             90.3%
Press Enter for next names, anything else to quit:      # Enter key
Guadeloupe: 90.0%
Bahrain: 89.1%
Antigua & Barbuda: 89.0%
     <cut to save space>
Swaziland: 81.6%
Zambia: 80.6%
El Salvador: 80.2%
Press Enter for next names, anything else to quit:
Botswana: 79.8%
Iran: 79.4%
Sao Tome & Principe: 79.3%
     <cut to save space>
Tunisia                             74.2%
Guatemala                           70.6%
Rwanda                              70.4%
Press Enter to see countries and literacy rates, anything else to quit:m
============================================================
l. Print countries in descending order of literacy rate
d. Print countries based on population density
q. Quit
============================================================
============================================================
Enter your choice: l
Press Enter to see countries and literacy rates, anything else to quit:
Algeria                             70.0%
Uganda                              69.9%
Cambodia                            69.4%
Madagascar                          68.9%
    <cut to save space>
Gabon                               63.2%
Malawi                              62.7%
Sudan                               61.1%
Togo                                60.9%
Press Enter to see countries and literacy rates, anything else to quit: r
============================================================
l. Print countries in descending order of literacy rate
d. Print countries based on population density
q. Quit
============================================================
============================================================
Enter your choice: d
ASIA                 1264.8
EUROPE                521.2
AFRICA                 86.7
OCEANIA               131.2
SOUTHERN AMERICA      136.2
NEAR EAST             427.1
NORTHERN AMERICA      260.9
(16271.5, 0.0)
============================================================
l. Print countries in descending order of literacy rate
d. Print countries based on population density
q. Quit
============================================================
Enter your choice: qq
Enter your choice: q
'''
