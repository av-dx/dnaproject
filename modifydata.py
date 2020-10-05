from searchdata import SearchCust

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
            print("This Customer ID doesnt exist!")
            return
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
            poi_type = input("POI Type : "+record['poi_type']+' --> ')
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
