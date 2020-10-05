import subprocess as sp
import pymysql
import pymysql.cursors
import texttable
from texttable import Texttable
from insertdata import *


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


def lsEmpByCity():
    try:
        # Takes City name as input
        city = input("Enter the City name to search for: ")

        query = "SELECT * FROM EMPLOYEE WHERE city_of_work='%s'" % city

        cur.execute(query)
        print("List of employees in ", city)
        table = Texttable()
        table.header(["Emp ID", "Fname", "Lname", "D.O.J.",
                      "Salary", "City of Work", "Contact"])
        table.set_cols_dtype(["i", "t", "t", "t", "t", "t", "t"])
        for row in cur:
            table.add_row([row['emp_id'], row['fname'], row['lname'],
                           row['doj'], row['salary'], row['city_of_work'], row['contact']])
        print(table.draw())

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)


def lsAgentByCity():
    try:
        # takes city name as input
        city = input("Enter the City name you want to search in: ")
        query = "SELECT fname, lname, contact FROM AGENT, EMPLOYEE WHERE agent_id=emp_id AND city_of_work='%s'" % (
                city)
        cur.execute(query)
        print("List of Agents in ", city)
        table = Texttable()
        table.header(["Fname", "Lname", "Contact"])
        table.set_cols_dtype(["t", "t", "t"])
        for row in cur:
            table.add_row([row['fname'], row['lname'], row['contact']])
        print(table.draw())
    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)


def makeBooking():
    try:
        # Takes booking details as input
        row = {}
        print("Enter new Booking's details: ")
        print("Does an existing customer booking again or a new customer is availing the service? Press 1 for existing, 2(or any other key) for new customer")
        x = int(input())
        if x == 1:
            row["cust_id"] = int(input("Customer ID: "))
        else:  # Inserting a new customer in the database, cust id being auto incremented
            row["cust_id"] = insertCustomer(cur, con)
            if (row["cust_id"] is None):
                print("Booking failed")
                return

        row["agent_id"] = int(input("Agent ID: "))
        cur.execute(
            "SELECT fname, lname FROM CUSTOMER WHERE cust_id="+str(row['cust_id']))
        cust = cur.fetchone()
        cur.execute(
            "SELECT fname, lname FROM EMPLOYEE WHERE emp_id IN (SELECT agent_id FROM AGENT) AND emp_id="+str(row['agent_id']))
        agent = cur.fetchone()
        if (cust is None):
            print("The customer doesn't exist!")
            return
        if (agent is None):
            print("Agent with that ID doesn't exist")
            return

        print("Make a booking for Customer :", cust['fname'], cust['lname'],
              "through Agent :", agent['fname'], agent['lname'], "?", sep=' ')
        if (input("Y/N : ").lower() == 'y'):
            ebpair = insertEvent(cur, con, row['cust_id'])
            if (ebpair is None):
                print("Booking failed")
                return
            row['event_id'] = ebpair[0]
            row['booking_id'] = ebpair[1]
            query = "INSERT INTO BOOKS VALUES(%d, %d, %d, %d)" % (
                    row["event_id"], row["cust_id"], row["agent_id"], row["booking_id"])
            cur.execute(query)
            con.commit()
            print("Booking Done!")
        else:
            print("Booking was cancelled")
    except Exception as e:
        con.rollback()
        print("Failed to insert Booking into database")
        print(">>>>>>>>>>>>>", e)
    return


def countEntities():
    try:
        print("Enter which entity you want to count: Press 1 for Employees, 2 for cities(locations), 3 for customers")
        x = int(input())
        if (x == 1):
            query = "SELECT COUNT(emp_id),city_of_work FROM EMPLOYEE GROUP BY city_of_work"
        elif (x == 2):
            query = "SELECT COUNT(cityname) FROM LOCATION"
        elif (x == 3):
            query = "SELECT COUNT(BOOKS.cust_id),EVENT.city FROM BOOKS INNER JOIN EVENT ON BOOKS.event_id=EVENT.event_id GROUP BY EVENT.city"

        cur.execute(query)
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)

        return


def lsEventBwDates():
    try:
        date_start = input("Enter the start date(YYYY-MM-DD): ")
        date_end = input("Enter the end date(YYYY-MM-DD): ")
        query = "SELECT event_id,type FROM EVENT WHERE start_datetime >= '%s' AND end_datetime <= '%s'" % (
                date_start, date_end)
        cur.execute(query)
        print("Events in between are: ")
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to reach database :( ")
        print(">>>>>>>>>>>>>", e)


def PartSearch():  # For now its just search on names,if we want we can make it on any column
    print("1. Search for Employees")
    print("2. Search for Events")
    print("3. Search for Customers")
    ch = int(input("Enter Choice: "))
    if(ch == 1):
        SearchEmp()
    elif(ch == 2):
        SearchEvents()
    elif(ch == 3):
        SearchCust()
    else:
        print("Invalid Option")
    return


def SearchEmp():
    try:
        x = input("Search(name or part of name): ")
        query = "SELECT * FROM EMPLOYEE WHERE fname LIKE '%s' OR lname LIKE '%s'" % (
            "%"+x+"%", "%"+x+"%")
        cur.execute(query)
        table = Texttable()
        table.header(["Emp ID", "Fname", "Lname", "D.O.J.",
                      "Salary", "City of Work", "Contact"])
        table.set_cols_dtype(["i", "t", "t", "t", "t", "t", "t"])
        for row in cur:
            table.add_row([row['emp_id'], row['fname'], row['lname'],
                           row['doj'], row['salary'], row['city_of_work'], row['contact']])
        print(table.draw())
    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)
    return


def SearchEvents():
    try:
        x = input("Search(name or part of name): ")
        query = "SELECT * FROM EVENT WHERE name LIKE '%s'" % ("%"+x+"%")
        cur.execute(query)
        table = Texttable()
        table.header(["Event ID", "Start", "End", "Type",
                      "Name", "City", "Booking ID"])
        table.set_cols_dtype(["i", "t", "t", "t", "t", "t", "i"])
        for row in cur:
            table.add_row([row['event_id'], row['start_datetime'], row['end_datetime'],
                           row['type'], row['name'], row['city'], row['booking_id']])
        print(table.draw())
    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)
    return


def SearchCust():
    try:
        x = input("Search(name or part of name): ")
        query = "SELECT * FROM CUSTOMER WHERE fname LIKE '%s' OR lname LIKE '%s'" % (
            "%"+x+"%", "%"+x+"%")
        cur.execute(query)
        table = Texttable()
        table.header(["Cust ID", "Fname", "Lname", "POI Type",
                      "POI Number", "Contact"])
        table.set_cols_dtype(["i", "t", "t", "t", "t", "t"])
        for row in cur:
            cur.execute("SELECT phone FROM CONTACT WHERE cust_id=" +
                        str(row['cust_id']))
            contacts = ""
            for ph in cur.fetchall():
                contacts += ph['phone'] + '\n'
            table.add_row([row['cust_id'], row['fname'], row['lname'],
                           row['poi_type'], row['poi_number'], contacts])
        print(table.draw())
    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)
    return


def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        makeBooking()
    elif(ch == 2):
        avgBookingFees()
    elif(ch == 3):
        lsEmpByCity()
    elif(ch == 4):
        lsAgentByCity()
    elif(ch == 5):
        countEntities()
    elif(ch == 6):
        lsEventBwDates()
    elif(ch == 7):
        PartSearch()
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
                print("8. Log out")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch >= 8:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
