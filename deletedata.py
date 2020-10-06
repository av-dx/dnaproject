from searchdata import SearchCust
from texttable import Texttable


def delContact(cur, con):
    try:
        name = input(
            "Search for the customer name whose contact you want to delete : ")
        SearchCust(name, cur, con)
        cust_id = int(
            input("Enter the customer ID whose contact you want to delete : "))
        cur.execute("SELECT * FROM CONTACT WHERE cust_id=%d" % (cust_id))
        cust = []
        todelete = []
        table = Texttable()
        table.header(["S.No.", "Phone"])
        table.set_cols_dtype(["i", "t"])
        for i, row in enumerate(cur):
            cust.append(row)
            table.add_row([i+1, row['phone']])
        if len(cust) == 0:
            raise Exception("This customer has no contacts stored!")
        print(table.draw())
        while (len(todelete) <= len(cust)):
            sno = input(
                "Enter the Sno of the Phone no. you want to delete, leave blank to quit :")
            if sno:
                sno = int(sno)
                todel = cust[sno-1]
                if (todel in todelete):
                    print("Number already deleted!")
                    continue
                else:
                    todelete.append(todel)
                    cur.execute("DELETE FROM CONTACT WHERE cust_id=%d AND phone='%s'" % (
                        cust_id, todel['phone']))
                    continue
            else:
                break
        if (len(todelete) > 0):
            ch = input(
                "Are you sure you want to delete the selected numbers? (y/N)")
            if (ch.lower() == 'y'):
                con.commit()
                print("Contacts deleted!")
            else:
                con.rollback()
                print("Contacts were not deleted.")
    except Exception as e:
        con.rollback()
        print("Failed to delete contacts from database")
        print(">>>>>>>>>>>>>", e)
       

def deleteSpecialGuest(cur,con):
    try:
        eventname = input("Enter the name of the Event: ")
        SearchEvents(eventname,cur,con)
        required_id = int(input("Enter the event ID you want to perform the operation in: "))
        cur.execute("SELECT * FROM SPECIAL_GUEST WHERE event_id = %d" %(required_id))
        spec = []
        todelete = []
        table = Texttable()
        table.header(["Serial No.","Name"])
        table.set_cols_dtype(["i", "t"])
        for i,row in enumerate(cur):
            spec.append(row)
            table.add_row([i+1, row['name']])
        print(table.draw())
        while(len(todelete) <= len(spec)):
            sno = int(input("Enter the Serial No(From the list) of the name you want to delete | leave blank to quit: "))
            if(sno <= len(spec)):
                if sno:
                    sno = int(sno)
                    todel = spec[sno-1]
                    if(todel in todelete):
                        print("Special Guest already deleted")
                        continue
                    else:
                        todelete.append(todel)
                        cur.execute("DELETE FROM SPECIAL_GUEST WHERE event_id = %d AND name = %s" %(required_id,todel['name']))
                        continue
                else:
                    break
            else:
                print("Serial Number out of Range! ")
                break
        if (len(todelete) > 0):
            ch = input("Are you sure you want to delete the Special Guest(y/n): ")
            if(ch.lower()=='y'):
                con.commit()
                print("Not special anymore!")
            else:
                con.rollback()
                print("Special Guest not deleted! ")
    except Exception as e:
        con.rollback()
        print("Failed to delete Special Guest")
        print(">>>>>>>>>>>>>",e)



