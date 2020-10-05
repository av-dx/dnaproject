from texttable import Texttable


def lsEmpByCity(cur, con):
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


def lsAgentByCity(cur, con):
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


def lsEventBwDates(cur, con):
    try:
        date_start = input("Enter the start date(YYYY-MM-DD): ")
        date_end = input("Enter the end date(YYYY-MM-DD): ")
        query = "SELECT type,name,start_datetime,end_datetime FROM EVENT WHERE start_datetime >= '%s' AND end_datetime <= '%s'" % (
                date_start, date_end)
        cur.execute(query)
        print("Events in between are: ")
        for row in cur:
            print(row)

    except Exception as e:
        con.rollback()
        print("Failed to reach database :( ")
        print(">>>>>>>>>>>>>", e)


def SearchEvents(x, cur, con):
    try:

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


def SearchEmp(x, cur, con):
    try:

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


def SearchCust(x, cur, con):
    try:

        query = "SELECT * FROM CUSTOMER WHERE fname LIKE '%s' OR lname LIKE '%s'" % (
            "%"+x+"%", "%"+x+"%")
        cur.execute(query)
        table = Texttable()
        table.header(["Cust ID", "Fname", "Lname", "POI Type",
                      "POI Number", "Contact"])
        table.set_cols_dtype(["i", "t", "t", "t", "t", "t"])
        custs = []
        for r in cur:
            custs.append(r)
        for row in custs:
            cur.execute("SELECT phone FROM CONTACT WHERE cust_id=" +
                        str(row['cust_id']))
            contacts = ""
            for ph in cur:
                contacts += ph['phone'] + '\n'
            table.add_row([row['cust_id'], row['fname'], row['lname'],
                           row['poi_type'], row['poi_number'], contacts])
        print(table.draw())
    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)
