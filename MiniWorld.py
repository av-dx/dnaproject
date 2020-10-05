import subprocess as sp
import pymysql
import pymysql.cursors
from pymysql.constants import CLIENT
from insertdata import *


def avgBookingFees():
    try:
        cityinput = input("Enter City Name : ")

        query = "SELECT AVG(amount) FROM PAYMENT WHERE booking_id IN (SELECT booking_id FROM EVENT WHERE city='%s')" % (
            cityinput)
        print(query)
        cur.execute(query)
        for row in cur:
            print(row)

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
        print(query)
        cur.execute(query)
        print("List of employees in ", city)
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)


def lsAgentByCity():
    try:
        # takes city name as input
        city = input("Enter the City name you want to search in: ")
        query = "SELECT agent_id, fname, lname, bookings_made FROM AGENT, EMPLOYEE WHERE agent_id=emp_id AND city_of_work='%s'" % (
            city)
        cur.execute(query)
        print("List of Agents in ", city)
        for row in cur:
            print(row)

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
                              cursorclass=pymysql.cursors.DictCursor,
                              client_flag=CLIENT.MULTI_STATEMENTS)
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
                print("7. Log out")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch >= 7:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
