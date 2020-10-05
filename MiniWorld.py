import subprocess as sp
import pymysql
import pymysql.cursors
import texttable
from texttable import Texttable
from insertdata import *
from modifydata import *
from searchdata import *
from deletedata import *


def avgBookingFees():
    try:
        cityinput = input("Enter City Name : ")

        query = "SELECT AVG(amount) FROM PAYMENT WHERE booking_id IN (SELECT booking_id FROM EVENT WHERE city='%s')" % (
                cityinput)
        cur.execute(query)
        table = Texttable()
        table.header(["Average Fees in "+cityinput])
        for row in cur:
            table.add_row([row['AVG(amount)']])
        print(table.draw())

    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)

    return


def UpdateData():
    print("What do you wnat to do: ")
    print("1. Insert.")
    print("2. Modify.")
    print("3. Delete.")
    x = int(input())
    if x == 1:
        print("What do you want to insert?")
        print("1. Customer")
        print("2. Contact of Customer")
        print("3. Location")
        print("4. Employee")
        print("5. Reports To")
        # only for existing booking ID as new payment is covered in new booking.
        print("6. Payment")
        print("7. Event")
        print("8. Special Guest")

    if x == 2:
        print("What do you want to modify?")
        print("1. Customer")
        print("2. Contact of Customer")
        print("3. Location")
        print("4. Employee")
        print("5. Reports To")  # both attributes are modifiyable.
        # only for existing booking ID as new payment is covered in new booking.
        print("6. Payment")
        print("7. Event")
        print("8. Special Guest")
        y = int(input())
        if y == 1:
            modifyCustomer(cur, con)


def countEntities():
    try:
        print(
            "Enter which entity you want to count: Press 1 for Employees, 2 for customers")

        x = int(input())
        if (x == 1):
            query = "SELECT COUNT(emp_id),city_of_work FROM EMPLOYEE GROUP BY city_of_work"
        # elif (x == 2):
        #    query = "SELECT COUNT(cityname) FROM LOCATION"
        elif (x == 2):
            query = "SELECT COUNT(BOOKS.cust_id),EVENT.city FROM BOOKS INNER JOIN EVENT ON BOOKS.event_id=EVENT.event_id GROUP BY EVENT.city"

        cur.execute(query)
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)

        return


def PartSearch():  # For now its just search on names,if we want we can make it on any column
    print("1. Search for Employees")
    print("2. Search for Events")
    print("3. Search for customers")
    ch = int(input("Enter Choice: "))
    if(ch == 1):
        x = input("Search(name or part of name): ")
        SearchEmp(x, cur, con)
    elif(ch == 2):
        x = input("Search(name or part of name): ")
        SearchEvents(x, cur, con)
    elif(ch == 3):
        x = input("Search(name or part of name): ")
        SearchCust(x, cur, con)
    else:
        print("Invalid Option")
    return


def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        makeBooking(cur, con)
    elif(ch == 2):
        avgBookingFees()
    elif(ch == 3):
        lsEmpByCity(cur, con)
    elif(ch == 4):
        lsAgentByCity(cur, con)
    elif(ch == 5):
        countEntities()
    elif(ch == 6):
        lsEventBwDates(cur, con)
    elif(ch == 7):
        PartSearch()
    elif(ch == 8):
        UpdateData()
    else:
        print("Error: Invalid Option")


# Global
while(1):
    tmp = sp.call('clear', shell=True)

    # Can be skipped if you want to hard core username and password
    username = input("Username: ")
    password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server
        con = pymysql.connect(host='localhost',
                              user=username,
                              password=password,
                              db='caaltd',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                print("1. Make a booking")
                print("2. Display Average Booking Fee for a city")
                print("3. Display Employees for a given city")
                print("4. List Agents in a City")
                print("5. Count Entities")
                print("6. List Events between two Dates")
                print("7. Search by partial text")
                print("8. Update")
                print("9. Logout")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch >= 9:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
