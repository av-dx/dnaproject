from insertdata import insertAgent
from searchdata import SearchCust, SearchEvents, SearchEmp
from texttable import Texttable


def delContact(cur, con):
    try:
        name = input(
            "Search for the customer name whose contact you want to delete(Simply press enter if you want to see the whole list) : ")
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
                    print("Number already selected for deletion!")
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
        eventname = input("Enter the name of the Event(Simply press enter to see the whole list): ")
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


def delAgent(agent_id,cur,con):
    try:
        query = "DELETE FROM REPORTS_TO WHERE agent_id=%d" % (
            agent_id)
        cur.execute(query)
        query = "DELETE FROM AGENT WHERE agent_id=%d" % (agent_id)
        cur.execute(query)
        query = "DELETE FROM EMPLOYEE WHERE emp_id=%d" % (agent_id)
        cur.execute(query)
        con.commit()
        print("Deletion Successful")
        return 0

    except Exception as e:
        con.rollback()
        print("Failed to delete employees from database")
        print(">>>>>>>>>>>>>", e)
        return -1


def delEmployee(cur, con):
    try:
        name = input(
            "Search for the Employee name whose contact you want to delete(Simply press enter to see the whole list) : ")
        SearchEmp(name, cur, con)
        emp_id = int(
            input("Enter the Employee ID who you want to fire(delete) : "))
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
        if(admin > 0):
            print("Administrator")
        if(manager > 0):
            print("Manager")
        if(agent > 0):
            print("Agent")

        if (input("Do you wish to delete this Employee (y/N) ?").lower() == 'y'):

            if(agent>0):
                query = "DELETE FROM REPORTS_TO WHERE agent_id=%d" % (
                    emp_id)
                cur.execute(query)
            if(manager>0):#to handle min max constarint of agent and managers
                query1 = "SELECT agent_id FROM REPORTS_TO WHERE mgr_id=%d" % (emp_id)
                cur.execute(query1)
                list1 = []
                for row in cur:
                    list1.append(row['agent_id'])


                query2 = "DELETE FROM REPORTS_TO WHERE mgr_id=%d" % (
                    emp_id)
                cur.execute(query2)
                cur.execute("SELECT agent_id FROM REPORTS_TO")
                list2 = []
                for row in cur:
                    list2.append(row['agent_id'])

                for agent_id in list1:
                    if agent_id not in list2:
                        print("If you delete the required manager, then the agent %d wont be reporting to anyone.", agent_id)
                        cur.execute("SELECT emp_id,fname,lname,city_of_work FROM AGENT, EMPLOYEE WHERE agent_id=%d AND agent_id=emp_id" % (agent_id))
                        for row in cur:
                            print (row)#printing without table for now
                        print("1. Fire this agent as well")
                        print("2. Replace with existing Manager/Hire new manager")
                        agmg = int(input())
                        if (agmg == 1):
                            if(delAgent(agent,cur,con) == -1):
                                return
                        elif (agmg == 2):
                            mgr_id = insertAgent(agent_id,cur,con)
                            print("The agent %d now reports to manager %d",(agent,mgr_id))

                        else:
                            print("Wrong input.")
                            raise Exception("Wrong input. Deletion cancelled!")

            query = "DELETE FROM AGENT WHERE agent_id=%d" % (emp_id)
            cur.execute(query)
            query = "DELETE FROM MANAGER WHERE mgr_id=%d" % (emp_id)
            cur.execute(query)
            query = "DELETE FROM ADMINISTRATOR WHERE admin_id=%d" % (emp_id)
            cur.execute(query)
            query = "DELETE FROM TECHNICIAN WHERE tech_id=%d" % (emp_id)
            cur.execute(query)
            query = "DELETE FROM EMPLOYEE WHERE emp_id=%d" % (emp_id)
            cur.execute(query)
            con.commit()
            print("Deletion Successful")
        else:
            raise Exception("Deletion was cancelled!")
    except Exception as e:
        con.rollback()
        print("Failed to delete employees from database")
        print(">>>>>>>>>>>>>", e)
    return
