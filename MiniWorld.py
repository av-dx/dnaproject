import subprocess as sp
import pymysql
import pymysql.cursors


def option2():
    """
    Function to implement option 1
    """
    try:
        cityinput = input()

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


def option3():
    try:
        # Takes City name as input
        print("Enter the CityName to search for: ")
        city = input()

        query = "SELECT * FROM EMPLOYEE WHERE city_of_work='%s'" % city
        print(query)
        cur.execute(query)
        print("List of employees in ", city)
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)


def option4():
    """
    Function to implement option 3
    """
    print("Not implemented")


def makeBooking():
    try:
        # Takes booking details as input
        row = {}
        print("Enter new Booking's details: ")
        row["cust_id"] = int(input("Customer ID: "))
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
        elif (agent is None):
            print("Agent with that ID doesn't exist")
            return
        else:
            print("Make a booking for Customer :", cust['fname'], cust['lname'],
                  "through Agent :", agent['fname'], agent['lname'], "?", sep=' ')
            if (input("Y/N : ").lower() == 'y'):
                # add EVENT
                print("Event Added!")
                # add PAYMENT (BOOKING)
                print("Booking Done!")
                query = "INSERT INTO BOOKS VALUES(%d, %d, %d, %d)" % (
                    row["event_id"], row["cust_id"], row["agent_id"], row["booking_id"])
                # [TO FIX] the above will fail as EVENT and BOOKING adding arent yet implemented;
                cur.execute(query)
                con.commit()
                print("Inserted Into Database")
    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
    return


def option5():
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
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

        return


def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        makeBooking()
    elif(ch == 2):
        option2()
    elif(ch == 3):
        option3()
    elif(ch == 4):
        option4()
    elif(ch == 5):
        option5()
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
                              db='dataproj',
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
                # Here taking example of Employee Mini-world
                print("1. Make a booking")  # Hire an Employee
                print("2. Display Average Booking Fee for a city")
                print("3. Display employees for a given city")
                print("4. Option 4")  # Employee Statistics
                print("5. OPTION 5")
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch >= 6:
                    break
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
