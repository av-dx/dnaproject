from searchdata import SearchCust, SearchEvents, SearchEmp


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
            doj = input("Date of Joiningt: "+ str(record['doj'])+' --> ')
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
            con.commit()
            print("Record updated successfully!")
    except Exception as e:
        con.rollback()
        print("Failed to modify values.")
        print(">>>>>>>>>>>>>", e)
