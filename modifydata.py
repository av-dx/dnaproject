from searchdata import SearchCust, SearchEvents, SearchEmp
from insertdata import insertAgent

def modifyCustomer(cur, con):
    try:
        print("Enter the name of Customer: ")
        name = input()
        print("Here are the matching records :")
        SearchCust(name, cur, con)
        cust_id = int(
            input("Enter Customer ID of the record you want to modify : "))
        cur.execute("SELECT * FROM CUSTOMER WHERE cust_id="+str(cust_id))
        record = cur.fetchone()
        if (record is None):
            raise Exception("This Customer ID doesnt exist!")
        else:
            print(
                "Press enter to accept current value, or type the new value, type NULL to set it to NULL.")
            fname = input("First Name : "+record['fname']+' --> ')
            if fname:
                if (fname == 'NULL'):
                    record['fname'] = ''
                else:
                    record['fname'] = fname
            lname = input("Last Name : "+record['lname']+' --> ')
            if lname:
                if (lname == 'NULL'):
                    record['lname'] = ''
                else:
                    record['lname'] = lname
            poi_type = input("POI poi_type : "+record['poi_type']+' --> ')
            if poi_type:
                if (poi_type == 'NULL'):
                    record['poi_type'] = ''
                else:
                    record['poi_type'] = poi_type
            poi_number = input(
                "POI Number : "+record['poi_number']+' --> ')
            if poi_number:
                if (poi_number == 'NULL'):
                    record['poi_number'] = ''
                else:
                    record['poi_number'] = poi_number
            query = "UPDATE CUSTOMER SET fname='%s', lname='%s', poi_type='%s', poi_number='%s' WHERE cust_id='%d'" % (
                record['fname'], record['lname'], record['poi_type'], record['poi_number'], cust_id)
            cur.execute(query)
            con.commit()
            print("Record updated successfully!")
    except Exception as e:
        con.rollback()
        print("Failed to modify values.")
        print(">>>>>>>>>>>>>", e)


def modifyEvent(cur, con):
    try:
        print("Enter the name of Event: ")
        name = input()
        print("Here are the matching records :")
        SearchEvents(name, cur, con)
        event_id = int(
            input("Enter Event ID of the record you want to modify : "))
        cur.execute("SELECT * FROM EVENT WHERE event_id="+str(event_id))
        record = cur.fetchone()
        if (record is None):
            raise Exception("This Event ID doesnt exist!")
        else:
            print(
                "Press enter to accept current value, or type the new value, type NULL to set it to NULL.")
            start_datetime = input(
                "Starting of the event : "+str(record['start_datetime'])+' --> ')
            if start_datetime:
                if (start_datetime == 'NULL'):
                    record['start_datetime'] = ''
                else:
                    record['start_datetime'] = start_datetime
            end_datetime = input(
                "When does the event end : "+str(record['end_datetime'])+' --> ')
            if end_datetime:
                if (end_datetime == 'NULL'):
                    record['end_datetime'] = ''
                else:
                    record['end_datetime'] = end_datetime
            eventtype = input("Type of Event: "+record['type']+' --> ')
            if eventtype:
                if (eventtype == 'NULL'):
                    record['type'] = ''
                else:
                    record['type'] = eventtype
            name = input(
                "Name : "+record['name']+' --> ')
            if name:
                if (name == 'NULL'):
                    record['name'] = ''
                else:
                    record['name'] = name
            city = input("City: "+record['city']+' --> ')
            if city:
                if (city == 'NULL'):
                    record['city'] = ''
                else:
                    record['city'] = city

            query = "UPDATE EVENT SET start_datetime='%s', end_datetime='%s', type='%s', name='%s', city='%s' WHERE event_id='%d'" % (
                record['start_datetime'], record['end_datetime'], record['type'], record['name'], record['city'], event_id)
            cur.execute(query)
            con.commit()
            print("Record updated successfully!")
    except Exception as e:
        con.rollback()
        print("Failed to modify values.")
        print(">>>>>>>>>>>>>", e)


def modifyEmployee(cur, con):
    try:
        print("Enter the name of Employee: ")
        name = input()
        print("Here are the matching records :")
        SearchEmp(name, cur, con)
        emp_id = int(
            input("Enter Employee ID of the record you want to modify : "))
        cur.execute("SELECT * FROM EMPLOYEE WHERE emp_id="+str(emp_id))
        record = cur.fetchone()
        if (record is None):
            raise Exception("This Employee ID doesnt exist!")
        else:
            print(
                "Press enter to accept current value, or type the new value, type NULL to set it to NULL.")
            fname = input("First Name : "+str(record['fname'])+' --> ')
            if fname:
                if (fname == 'NULL'):
                    record['fname'] = ''
                else:
                    record['fname'] = fname
            lname = input("Last Name : "+str(record['lname'])+' --> ')
            if lname:
                if (lname == 'NULL'):
                    record['lname'] = ''
                else:
                    record['lname'] = lname
            doj = input("Date of Joining: " + str(record['doj'])+' --> ')
            if doj:
                if (doj == 'NULL'):
                    record['doj'] = ''
                else:
                    record['doj'] = doj
            salary = input("Salary : "+str(record['salary'])+' --> ')
            if salary:
                if (salary == 'NULL'):
                    record['salary'] = 0
                else:
                    record['salary'] = float(salary)
            city_of_work = input("City: "+record['city_of_work']+' --> ')
            if city_of_work:
                if (city_of_work == 'NULL'):
                    record['city_of_work'] = ''
                else:
                    record['city_of_work'] = city_of_work
            contact = input("Contact: "+record['contact']+' --> ')
            if contact:
                if (contact == 'NULL'):
                    record['contact'] = ''
                else:
                    record['contact'] = contact

            query = "UPDATE EMPLOYEE SET fname='%s', lname='%s', doj='%s', salary='%f', city_of_work='%s', contact='%s' WHERE emp_id='%d'" % (
                record['fname'], record['lname'], record['doj'], record['salary'], record['city_of_work'], record['contact'], emp_id)
            cur.execute(query)

            # Change Roles
            agent = cur.execute(
                "SELECT emp_id,fname, lname, bookings_made FROM EMPLOYEE, AGENT WHERE emp_id IN (SELECT agent_id FROM AGENT) AND emp_id=%d" % (emp_id))
            manager = cur.execute(
                "SELECT emp_id,fname, lname, years_of_experience FROM EMPLOYEE, MANAGER WHERE emp_id IN (SELECT mgr_id FROM MANAGER) AND emp_id=%d" % (emp_id))
            admin = cur.execute(
                "SELECT emp_id,fname, lname, qualification FROM EMPLOYEE, ADMINISTRATOR WHERE emp_id IN (SELECT admin_id FROM ADMINISTRATOR) AND emp_id=%d" % (emp_id))
            tech = cur.execute(
                "SELECT emp_id,fname, lname, tlevel FROM EMPLOYEE, TECHNICIAN WHERE emp_id IN (SELECT tech_id FROM TECHNICIAN) AND emp_id=%d" % (emp_id))

            print("Currently this employee is a", end=' ')
            if(tech > 0):
                print("Technician")
                role = 3
            if(admin > 0):
                print("Administrator")
                role = 2
            if(manager > 0):
                print("Manager")
                role = 4
            if(agent > 0):
                print("Agent")
                role = 1

            while(1):
                print("What role do you want to assign to this employee ?")
                print("1. Agent")
                print("2. Administrator")
                print("3. Technician")
                print("4. Manager")
                newrole = int(input())
                if ((newrole < 1) or (newrole > 4)):
                    print("Wrong input try again!")
                    continue
                else:
                    break

            if (newrole != role):
                cur.execute("DELETE FROM REPORTS_TO WHERE agent_id=%d OR mgr_id=%d" % (
                    emp_id, emp_id))
                cur.execute("DELETE FROM AGENT WHERE agent_id=%d" % (emp_id))
                cur.execute("DELETE FROM MANAGER WHERE mgr_id=%d" % (emp_id))
                cur.execute("DELETE FROM ADMINISTRATOR WHERE admin_id=%d" % (
                    emp_id))
                cur.execute(
                    "DELETE FROM TECHNICIAN WHERE tech_id=%d" % (emp_id))

                if (newrole == 1):
                    insertAgent(emp_id, cur, con)
                elif (newrole == 2):
                    qualification = input("Enter the qualification : ")
                    cur.execute("INSERT INTO ADMINISTRATOR VALUES (%d,'%s')" % (
                        emp_id, qualification))
                elif (newrole == 3):
                    tlevel = int(input("Enter technicians level : "))
                    cur.execute("INSERT INTO TECHNICIAN VALUES (%d,%d)" %
                                (emp_id, tlevel))
                else:
                    years = int(input("Years of Experience: "))
                    cur.execute(
                        "INSERT INTO MANAGER VALUES('%d','%d')" % (emp_id, years))
            con.commit()
            print("Record updated successfully!")
    except Exception as e:
        con.rollback()
        print("Failed to modify values.")
        print(">>>>>>>>>>>>>", e)
