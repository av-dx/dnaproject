from searchdata import SearchCust, SearchEvents
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


def delReportsTo(agent_id, mgr_id, cur, con):
    try:
        if (agent_id == 'any') and (mgr_id == 'any'):
            raise Exception("Invalid arguments to delReportsTo()")
        elif agent_id == 'any':
            query = "DELETE FROM REPORTS_TO WHERE mgr_id=%d" % (mgr_id)
        elif mgr_id == 'any':
            query = "DELETE FROM REPORTS_TO WHERE agent_id=%d" % (agent_id)
        else:
            query = "DELETE FROM REPORTS_TO WHERE agent_id=%d AND mgr_id=%d" % (
                agent_id, mgr_id)
        cur.execute(query)
        con.commit()
    except Exception as e:
        con.rollback()
        print("Failed to delete reports_to record from database")
        print(">>>>>>>>>>>>>", e)


def delSpecialGuest(cur, con):
    try:
        eventname = input("Enter the name of the Event: ")
        SearchEvents(eventname, cur, con)
        required_id = int(
            input("Enter the event ID you want to perform the operation in: "))
        cur.execute("SELECT * FROM SPECIAL_GUEST WHERE event_id = %d" %
                    (required_id))
        spec = []
        todelete = []
        table = Texttable()
        table.header(["Serial No.", "Name"])
        table.set_cols_dtype(["i", "t"])
        for i, row in enumerate(cur):
            spec.append(row)
            table.add_row([i+1, row['name']])
        if len(spec) == 0:
            raise Exception("This event has no special guests stored!")
        print(table.draw())
        while(len(todelete) <= len(spec)):
            sno = input(
                "Enter the Serial No(From the list) of the name you want to delete | leave blank to quit: ")
            if sno:
                sno = int(sno)
                if(sno <= len(spec)):
                    print("Serial No. out of range!")
                    continue
                todel = spec[sno-1]
                if(todel in todelete):
                    print("Special Guest already deleted")
                    continue
                else:
                    todelete.append(todel)
                    cur.execute("DELETE FROM SPECIAL_GUEST WHERE event_id = %d AND name = %s" % (
                        required_id, todel['name']))
                    continue
            else:
                break
        if (len(todelete) > 0):
            ch = input(
                "Are you sure you want to delete the Special Guest(y/n): ")
            if(ch.lower() == 'y'):
                con.commit()
                print("Not special anymore!")
            else:
                con.rollback()
                print("Special Guest not deleted! ")
    except Exception as e:
        con.rollback()
        print("Failed to delete Special Guest")
        print(">>>>>>>>>>>>>", e)
