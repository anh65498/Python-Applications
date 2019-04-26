# Anh Pham
# This program analyze U.S college tuition over between 1971 - 2018 and lets the user
# view the tuition trend, the room and board trend, and the total cost of 4 years of college
# for a range of years.
from college import Data_Analyzer

def main():
    college = Data_Analyzer()
    college.parseData()
    # print(college._data)
    college.plot_tuition()
    college.plot_room_and_board()
    college.get_college_cost()

main()


'''Output:
#1: Testing FileIO exception
Could not read input file tuition.csv

'''
