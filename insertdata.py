def insertCustomer(cur, con):
    try:
        print("Enter new customer details: ")
        row = {}
        row['fname'] = input("First Name of the Customer: ")
        row['lname'] = input("Last Name of the customer: ")
        row['poi_type'] = input("Type of POI: ")
        row['poi_number'] = input("POI Number: ")
        query = "INSERT INTO CUSTOMER(fname,lname,poi_type,poi_number) VALUES ('%s','%s','%s','%s')" % (
            row['fname'], row['lname'], row['poi_type'], row['poi_number'])
        cur.execute(query)
        cur.execute("SELECT LAST_INSERT_ID()")
        last_id = cur.fetchone()['LAST_INSERT_ID()']
        con.commit()
        print("The customer is inserted into the database")
        return last_id
    except Exception as e:
        con.rollback()
        print("Failed to insert Customer into database")
        print(">>>>>>>>>>>>>", e)
        return None


def insertEvent(cur, con, cust_id):
    try:
        print("Enter the Event details: ")
        row = {}
        row['start_datetime'] = input(
            "Start date & time(YYYY-MM-DD hh:mm:ss): ")
        row['end_datetime'] = input(
            "End date & time(YYYY-MM-DD hh:mm:ss): ")
        row['type'] = input(
            "Type of the event(like wedding/birthday,etc): ")
        row['name'] = input("Name of the Event: ")
        row['city'] = input(
            "City where the event is going to be held: ")

        print("Event will be added after booking payment !")
        print("Enter payment details : ")
        row1 = {}
        row1['transdate'] = input(
            "Start date & time(YYYY-MM-DD hh:mm:ss): ")
        row1['amount'] = float(input(
            "Amount : "))
        row1['cust_id'] = cust_id

        cur.execute("INSERT INTO PAYMENT(transdate, amount, cust_id) VALUES ('%s', '%f', '%d')" % (
            row1['transdate'], row1['amount'], row1['cust_id']))
        cur.execute("SELECT LAST_INSERT_ID()")
        row['booking_id'] = cur.fetchone()['LAST_INSERT_ID()']

        cur.execute("INSERT INTO EVENT(start_datetime, end_datetime, type, name, city, booking_id) VALUES ('%s', '%s', '%s', '%s', '%s', '%d')" % (
            row['start_datetime'], row['end_datetime'], row['type'], row['name'], row['city'], row['booking_id']))
        cur.execute("SELECT LAST_INSERT_ID()")
        row['event_id'] = cur.fetchone()['LAST_INSERT_ID()']
        con.commit()
        return (row['event_id'], row['booking_id'])
    except Exception as e:
        con.rollback()
        print("Failed to insert Event into database")
        print(">>>>>>>>>>>>>", e)
        return None
