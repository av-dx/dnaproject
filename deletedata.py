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
