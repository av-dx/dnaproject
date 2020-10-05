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

def insertContact(cur,con):
    cust_id = input("Enter Customer ID: ")
    while(1):
        phone = input("Enter Phone details: ")
        try:
            query = "INSERT INTO CONTACT VALUES ('%s','%s')" % (cust_id,phone)
            cur.execute(query)
            con.commit()
        except Exception as e:
            con.rollback()
            print("Failed to insert Customer into database")
            print(">>>>>>>>>>>>>", e)
            break
        print("do you want to add more contact detail for this customer? (y/n)")
        if (input().lower() == 'y'):
            continue
        else:
            break
    return

def insertEmployee(cur,con):
    try:
        print("Enter new Employee details: ")
        row = {}
        row['fname'] = input("First Name of the Employee: ")
        row['lname'] = input("Last Name of the Employee: ")
        row['doj'] = input("Date of joining(YYY-MM-DD): ")
        row['salary'] = int(input("Salary: "))
        row['city_of_work'] = input("City of work: ")
        row['contact'] = input("Contact: ")
        query = "INSERT INTO EMPLOYEE(fname,lname,doj,salary,city_of_work,contact) VALUES ('%s','%s','%s','%f','%s','%s')" % (
            row['fname'],row['lname'],row['doj'],row['salary'],row['city_of_work'],row['contact'])
        cur.execute(query)
        cur.execute("SELECT LAST_INSERT_ID()")
        last_id = cur.fetchone()['LAST_INSERT_ID()']
        con.commit()
        role = input("What is the role of this employee?(Agent/Manager/Administrator/Technician): ").lower()
        if role == 'agent':
            cur.execute(
                "INSERT INTO AGENT VALUES('%d','%d')" % (last_id,0))
            con.commit()
        elif role == 'administrator':
            qualif = input("Qualfication of the Administrator: ")
            cur.execute(
                "INSERT INTO ADMINISTRATOR VALUES('%d','%s')" % (last_id,qualif))
            con.commit()
        elif role == 'technician':
            tlevel = int(input("Tlevel of the Technician: "))
            cur.execute(
                "INSERT INTO TECHNICIAN VALUES('%d','%d')" % (last_id,tlevel))
            con.commit()

        elif role == 'manager':
            years = int(input("Years of Experience: "))
            cur.execute(
                "INSERT INTO MANAGER VALUES('%d','%d')" % (last_id,years))
            con.commit()
        else:
            print("Wrong input try again")

    except Exception as e:
        con.rollback()
        print("Failed to insert Customer into database")
        print(">>>>>>>>>>>>>", e)
    return


def makeBooking(cur, con):
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
            "SELECT fname, lname, bookings_made FROM EMPLOYEE, AGENT WHERE emp_id IN (SELECT agent_id FROM AGENT) AND emp_id="+str(row['agent_id']))
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
            query = "UPDATE AGENT SET bookings_made='%d' WHERE agent_id='%d'" % (
                    agent['bookings_made']+1, row['agent_id'])
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
