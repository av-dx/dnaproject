from texttable import Texttable


def avgBookingFees(cityinput,cur,con):
    try:
        #cityinput = input("Enter City Name : ")
        query = "SELECT AVG(amount) FROM PAYMENT WHERE booking_id IN (SELECT booking_id FROM EVENT WHERE city=%s)"
        cur.execute(query,cityinput)
        table = Texttable()
        table.header(["Average Fees in ",cityinput])
        for row in cur:
            table.add_row([row['AVG(amount)']])
        print(table.draw())

    except Exception as e:
        con.rollback()
        print("Failed to retreive values.")
        print(">>>>>>>>>>>>>", e)

    return


def countEmployee(cur,con):
    try:
        #print("Enter which entity you want to count: Press 1 for Employees, 2 for customers")
        #x = int(input())
        query = "SELECT COUNT(emp_id) AS employees,city_of_work FROM EMPLOYEE GROUP BY city_of_work"
        cur.execute(query)
        table = Texttable()
        table.header(["No. of employees","City"])
        table.set_cols_dtype(["i", "t"])
        for row in cur:
            table.add_row([row['employees'], row['city_of_work']])
        print(table.draw())

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)

    return

def countCust(cur,con):
    try:
        query = "SELECT COUNT(BOOKS.cust_id) AS customer,EVENT.city AS city FROM BOOKS INNER JOIN EVENT ON BOOKS.event_id=EVENT.event_id GROUP BY EVENT.city"
        cur.execute(query)
        table = Texttable()
        table.header(["No. of customers","City"])
        table.set_cols_dtype(["i", "t"])
        for row in cur:
            table.add_row([row['customer'], row['city']])
        print(table.draw())

    except Exception as e:
        con.rollback()
        print("Failed to fetch from database")
        print(">>>>>>>>>>>>>", e)

    return