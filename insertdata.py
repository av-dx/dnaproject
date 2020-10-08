from searchdata import SearchEvents, SearchEmp, lsManagerByCity, SearchCust


def insertCustomer(cur, con):
    try:
        print("Enter new customer details: ")
        row = {}
        row['fname'] = input("First Name of the Customer: ")
        row['lname'] = input("Last Name of the customer: ")
        row['poi_type'] = input("Type of POI: ")
        row['poi_number'] = input("POI Number: ")
        query = "INSERT INTO CUSTOMER(fname,lname,poi_type,poi_number) VALUES (%s,%s,%s,%s)"
        cur.execute(query, (row['fname'], row['lname'],
                            row['poi_type'], row['poi_number']))
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


def insertEvent(cur, con):
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
            "Transaction date & time(YYYY-MM-DD hh:mm:ss): ")
        row1['amount'] = float(input("Amount : "))
        #row1['cust_id'] = cust_id

        cur.execute("INSERT INTO PAYMENT(transdate, amount) VALUES (%s, %s)",
                    (row1['transdate'], row1['amount']))
        cur.execute("SELECT LAST_INSERT_ID()")
        row['booking_id'] = cur.fetchone()['LAST_INSERT_ID()']
        cur.execute("INSERT INTO EVENT(start_datetime, end_datetime, type, name, city, booking_id) VALUES (%s, %s, %s, %s, %s, %s)", (
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


def insertContact(cur, con):

    name = input("Enter Customer name to search for :")
    SearchCust(name, cur, con)
    cust_id = int(input("Enter Customer ID: "))
    while(1):
        phone = input("Enter Phone details: ")
        try:
            query = "INSERT INTO CONTACT VALUES (%s,%s)"
            cur.execute(query, (cust_id, phone))
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


def insertEmployee(role, cur, con, last_agent_city=None):
    try:
        print("Enter new Employee details: ")
        row = {}
        row['fname'] = input("First Name of the Employee: ")
        row['lname'] = input("Last Name of the Employee: ")
        row['doj'] = input("Date of joining(YYYY-MM-DD): ")
        row['salary'] = int(input("Salary: "))
        row['city_of_work'] = input("City of work: ")
        row['contact'] = input("Contact: ")
        query = "INSERT INTO EMPLOYEE(fname,lname,doj,salary,city_of_work,contact) VALUES (%s,%s,%s,%s,%s,%s)"
        cur.execute(query, (row['fname'], row['lname'], row['doj'],
                            row['salary'], row['city_of_work'], row['contact']))
        cur.execute("SELECT LAST_INSERT_ID()")
        last_id = cur.fetchone()['LAST_INSERT_ID()']
        if role == 1:
            cur.execute(
                "INSERT INTO AGENT VALUES(%s,%s)", (last_id, 0))
            insertAgent(last_id, cur, con)
            return last_id
        elif role == 2:
            qualif = input("Qualfication of the Administrator: ")
            cur.execute(
                "INSERT INTO ADMINISTRATOR VALUES(%s,%s)", (last_id, qualif))
            print("Administrator added successfully.")
            con.commit()
            return last_id
        elif role == 3:
            tlevel = int(input("Tlevel of the Technician: "))
            cur.execute(
                "INSERT INTO TECHNICIAN VALUES(%s,%s)", (last_id, tlevel))
            print("Technician added successfully.")
            con.commit()
            return last_id

        elif role == 4:
            insertManager(last_id, last_agent_city, cur, con)
            return last_id
        else:
            con.rollback()
            print("Wrong input try again")
        con.commit()

    except Exception as e:
        con.rollback()
        print("Failed to insert Employee into database")
        print(">>>>>>>>>>>>>", e)


def insertAgent(last_id, cur, con):
    try:
        cur.execute(
            "SELECT city_of_work FROM EMPLOYEE WHERE emp_id=%s", last_id)
        city = cur.fetchone()['city_of_work']
        while(1):
            x = int(input(
                "To what manager will this agent report to?: Press 1 for existing Manager, 2 for new Manager "))
            if (x == 1):
                num_mgr_city = lsManagerByCity(city, cur, con)
                if (num_mgr_city == -1):
                    continue
                mgr_id = int(
                    input("Enter Employee(Manager) ID of the record to whom this agent would report: "))
                cur.execute("SELECT * FROM MANAGER WHERE mgr_id=%s", mgr_id)
                record = cur.fetchone()
                if (record is None):
                    print("This Manager ID doesnt exist! Create a new manager")
                    continue
                else:
                    print("Agent added successfully.")
                    break
            elif (x == 2):
                print("Enter the new Manager details: ")
                mgr_id = insertEmployee(4, cur, con, city)
                break
            else:
                print("Invalid Option!")
                continue
        insertReportsTo(last_id, mgr_id, cur, con)
        con.commit()
        return mgr_id
    except Exception as e:
        con.rollback()
        print("Failed to insert Agent into database")
        print(">>>>>>>>>>>>>", e)
    return


def insertManager(last_id, last_agent_city, cur, con):
    try:
        cur.execute(
            "SELECT city_of_work FROM EMPLOYEE WHERE emp_id=%s", (last_id))
        city_name = cur.fetchone()['city_of_work']
        queryMgr = "SELECT COUNT(city_of_work) FROM EMPLOYEE,MANAGER WHERE city_of_work=%s AND EMPLOYEE.emp_id=MANAGER.mgr_id"
        cur.execute(queryMgr, city_name)
        if(cur.fetchone()['COUNT(city_of_work)'] == 2):
            raise Exception(
                "There are already two managers to handle %s. Try again." % city_name)
        years = int(input("Years of Experience: "))
        cur.execute(
            "INSERT INTO MANAGER VALUES(%s,%s)", (last_id, years))
        if (last_agent_city is not None) and (last_agent_city != city_name):
            raise Exception("The manager and agent aren't of the same city!")
        else:
            print("Manager added successfully.")
            return last_id
    except Exception as e:
        con.rollback()
        print("Failed to insert Agent into database")
        print(">>>>>>>>>>>>>", e)


def makeBooking(cur, con):
    try:
        # Takes booking details as input
        row = {}
        print("Enter new Booking's details: ")
        print("Does an existing customer booking again or a new customer is availing the service? Press 1 for existing, 2(or any other key) for new customer")
        x = int(input())
        if x == 1:
            name = input("Enter Customer name to search for :")
            SearchCust(name, cur, con)
            row["cust_id"] = int(input("Customer ID: "))
        else:  # Inserting a new customer in the database, cust id being auto incremented
            row["cust_id"] = insertCustomer(cur, con)
            if (row["cust_id"] is None):
                raise Exception("Booking failed : Customer could not be added")

        row["agent_id"] = int(input("Agent ID: "))
        cur.execute(
            "SELECT fname, lname FROM CUSTOMER WHERE cust_id=%s", row['cust_id'])
        cust = cur.fetchone()
        cur.execute(
            "SELECT fname, lname, bookings_made FROM EMPLOYEE, AGENT WHERE emp_id IN (SELECT agent_id FROM AGENT) AND emp_id=%s", row['agent_id'])
        agent = cur.fetchone()
        if (cust is None):
            raise Exception("Customer with that ID doesn't exist!")
        if (agent is None):
            raise Exception("Agent with that ID doesn't exist!")

        print("Make a booking for Customer :", cust['fname'], cust['lname'],
              "through Agent :", agent['fname'], agent['lname'], "?", sep=' ')
        if (input("Y/N : ").lower() == 'y'):
            ebpair = insertEvent(cur, con)
            if (ebpair is None):
                raise Exception("Booking failed : Event could not be added")
            row['event_id'] = ebpair[0]
            row['booking_id'] = ebpair[1]
            query = "INSERT INTO BOOKS VALUES(%s, %s, %s, %s)"
            cur.execute(
                query, (row['event_id'], row['cust_id'], row['agent_id'], row['booking_id']))
            query = "UPDATE AGENT SET bookings_made=%s WHERE agent_id=%s"
            cur.execute(query, (agent['bookings_made']+1, row['agent_id']))
            con.commit()
            print("Booking Done!")
        else:
            raise Exception("Booking was cancelled!")
    except Exception as e:
        con.rollback()
        print("Failed to insert Booking into database")
        print(">>>>>>>>>>>>>", e)
    return


def insertSpecialGuest(cur, con):
    try:
        nameofevent = input("Enter the name of the Event: ")
        print("Here are the matching records: ")
        SearchEvents(nameofevent, cur, con)
        required_id = int(input("Enter the event ID for the event: "))
        query1 = "SELECT * FROM SPECIAL_GUEST WHERE event_id=%s"
        cur.execute(query1, required_id)
        required_tuple = cur.fetchone()
        if(required_tuple is None):
            print("This Event ID doesn't exist! ")
            return
        else:
            querySPG = "SELECT COUNT(event_id) FROM SPECIAL_GUEST WHERE event_id=%s"
            cur.execute(querySPG, required_id)
            if(cur.fetchone()['COUNT(event_id)'] == 3):
                print(
                    "There are already three special guests visiting this event. Try again.")
                return

            row = {}
            print("Please enter the details of the Special Guest")
            row['event_id'] = input("Event ID for the event: ")
            row['name'] = input("Name of the Guest: ")
            row['occupation'] = input("Occupation of the Guest: ")
            row['contact'] = input("Contact of the Guest: ")
            cur.execute("INSERT INTO SPECIAL_GUEST(event_id,name,occupation,contact) VALUES (%s, %s, %s, %s)", (
                row['event_id'], row['name'], row['occupation'], row['contact']))
            con.commit()
            print("The Special Guest is registered into the database")
        return
    except Exception as e:
        con.rollback()
        print("Failed to insert Special Guest ")
        print(">>>>>>>>>>>>>", e)
        return None


def insertReportsTo(agent_id, mgr_id, cur, con):
    try:
        cur.execute(
            "SELECT city_of_work AS city FROM AGENT, EMPLOYEE WHERE agent_id=emp_id AND agent_id=%s", agent_id)
        agent = cur.fetchone()
        cur.execute(
            "SELECT city_of_work AS city FROM MANAGER, EMPLOYEE WHERE mgr_id=emp_id AND mgr_id=%s", mgr_id)
        mgr = cur.fetchone()
        if (agent is None):
            raise Exception("Agent with that ID doesnt exist!")
        if (mgr is None):
            raise Exception("Manager with that ID doesnt exist!")
        if (agent['city'] == mgr['city']):
            cur.execute("INSERT INTO REPORTS_TO VALUES (%s,%s)",
                        (agent_id, mgr_id))
            con.commit()
        else:
            raise Exception(
                "Agent is not of the same City as Manager! Cannot add")
    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)
