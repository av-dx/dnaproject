import subprocess as sp
import pymysql
import pymysql.cursors
import texttable
from texttable import Texttable
from insertdata import *
from modifydata import *
from searchdata import *
from deletedata import *
from reportdata import *


def insertMenu():
    print("1. Insert a booking")
    print("2. Insert Contacts")
    print("3. Insert a new Customer")
    print("4. Insert a new Employee")
    print("5. Insert Special Guest to an Event")
    print("6. Back")
    ch = int(input("Enter choice> "))
    sp.call('clear', shell=True)
    if(ch == 1):
        makeBooking(cur, con)
    elif(ch == 2):
        insertContact(cur, con)
    elif(ch == 3):
        insertCustomer(cur, con)
    elif(ch == 4):
        print("1. Agent")
        print("2. Administrator")
        print("3. Technician")
        print("4. Manager")
        role = int(input())
        if ((role < 1) or (role > 4)):
            print("Wrong input try again!")
            return
        insertEmployee(role, cur, con)
    elif(ch == 5):
        insertSpecialGuest(cur, con)
    else:
        return


def deleteMenu():
    print("1. Delete Customer Contacts")
    print("2. Delete Special Guest for an Event")
    print("3. Delete Employee")
    print("4. Back")
    ch = int(input("Enter choice> "))
    sp.call('clear', shell=True)
    if(ch == 1):
        delContact(cur, con)
    elif(ch == 2):
        delSpecialGuest(cur, con)
    elif(ch == 3):
        delEmployee(cur, con)
    else:
        return


def searchMenu():
    print("1. Search for Agent based on city")
    print("2. Search for Employee by name")
    print("3. Search for Employee by city")
    print("4. Search for Events by name")
    print("5. Search for Events between dates")
    print("6. Search for Customer by name")
    print("7. Back")
    ch = int(input("Enter choice> "))
    sp.call('clear', shell=True)
    if(ch == 1):
        lsAgentByCity(cur, con)
    elif(ch == 2):
        name = input("Enter name to search for : ")
        SearchEmp(name, cur, con)
    elif(ch == 3):
        lsEmpByCity(cur, con)
    elif(ch == 4):
        name = input("Enter name to search for : ")
        SearchEvents(name,cur,con)
    elif(ch == 5):
        lsEventBwDates(cur, con)
    elif(ch == 6):
        name = input("Enter name to search for : ")
        SearchCust(name, cur, con)
    else:
        return


def updateMenu():
    print("1. Update a Customer record")
    print("2. Update an Event record")
    print("3. Update an Employee record")
    print("4. Back")
    ch = int(input("Enter choice> "))
    sp.call('clear', shell=True)
    if(ch == 1):
        modifyCustomer(cur, con)
    elif(ch == 2):
        modifyEvent(cur, con)
    elif(ch == 3):
        modifyEmployee(cur, con)
    else:
        return

def reportsMenu():
    print("1. Display Average Booking Fees based on city")
    print("2. Display the number of employees citywise")
    print("3. Display the number of customers who booked events citywise")
    print("4. Back")
    ch = int(input())
    sp.call('clear', shell=True)
    if(ch == 1):
        cityinput = input("Enter city name: ")
        avgBookingFees(cityinput,cur,con)
    elif(ch == 2):
        countEmployee(cur,con)
    elif(ch == 3):
        countCust(cur,con)
    else:
        return


def adminMenu(ch):
    if(ch == 1):
        insertMenu()
    elif(ch == 2):
        deleteMenu()
    elif(ch == 3):
        searchMenu()
    elif(ch == 4):
        updateMenu()
    elif(ch == 5):
        reportsMenu()
    else:
        print("Error: Invalid Option")


def custMenu(ch):
    if(ch == 1):
        lsAgentByCity(cur, con)
    elif(ch == 2):
        lsEventBwDates(cur, con)
    else:
        print("Error: Invalid Option")


# Global
while(1):
    tmp = sp.call('clear', shell=True)

    print(r"   ____    _        _         _    _      _   ")
    print(r"  / ___|  / \      / \       | |  | |_ __| |  ")
    print(r" | |     / _ \    / _ \      | |  | __/ _` |  ")
    print(r" | |___ / ___ \  / ___ \     | |__| || (_| |_ ")
    print(r"  \____/_/   \_\/_/   \_\    |_____\__\__,_(_)")
    print(r"                                              ")

    username = input("Username: ")
    password = input("Password: ")

    try:
        if username == "customer":
            adminMode = 0
            con = pymysql.connect(host='localhost',
                                  user="customer",
                                  password="customer#caaltd",
                                  db='caaltd',
                                  cursorclass=pymysql.cursors.DictCursor)
            tmp = sp.call('clear', shell=True)
            print("Logged in as a customer.")
        else:
            adminMode = 1
            con = pymysql.connect(host='localhost',
                                  user=username,
                                  password=password,
                                  db='caaltd',
                                  cursorclass=pymysql.cursors.DictCursor)
            tmp = sp.call('clear', shell=True)
            print("Logged in as an admin.")
        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")
        input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            if adminMode:
                while(1):
                    sp.call('clear', shell=True)
                    print("1. Insert Records")
                    print("2. Delete Records")
                    print("3. Search Records")
                    print("4. Update Records")
                    print("5. View Reports")
                    print("6. Logout")
                    ch = int(input("Enter choice> "))
                    sp.call('clear', shell=True)
                    if ch >= 6:
                        break
                    else:
                        adminMenu(ch)
                        input("Enter any key to CONTINUE>")
            else:
                while(1):
                    sp.call('clear', shell=True)
                    print("1. Search for Agent based on City")
                    print("2. Search for Events between dates")
                    print("3. Logout")
                    ch = int(input("Enter choice> "))
                    sp.call('clear', shell=True)
                    if ch >= 3:
                        break
                    else:
                        custMenu(ch)
                        input("Enter any key to CONTINUE>")

    except:
        tmp = sp.call('clear', shell=True)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")