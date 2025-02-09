# **Data And Applications**
##    Project Phase-IV 
##      Team C.A.A.
---
*Aashwin Vaish(2019114014)*\
*Aravapalli Akhilesh(2019114016)*\
*Chayan Kochar(2019114008)*
 
 
 A Database Applications project which provides a Command-Line-Interface(CLI) for accessing it. This database is specifically designed for storing information for a Convention Hall Company CAA.Ltd.. You can store,retreive,delete and modify data in the database.

 
 Steps to use: 
* Download or Clone the repo into your local system.
* The folder contains an .sql file and 4 .py files which are for different types of queries.
* Download texttable from pip. We have used this library just for printing tables. USE [pip3 install texttable] in the terminal.
* Download stdiomask from pip. We have used this to mask the password.
* Create a database named 'caaltd'(without quotes)
* Import the sql file into your mysql local system. USE [mysql -u <username> -p caaltd < caaltd.sql] in terminal.
* To create a 'customer' user with READ-ONLY permissions to the database :
  * Log in as a root user to MySQL [sudo mysql -p].
  * Run the following commands.
  ```
  CREATE USER 'customer'@'localhost' IDENTIFIED BY 'customer#caaltd';
  GRANT SELECT ON caaltd.* TO 'customer'@'localhost' IDENTIFIED BY 'customer#caaltd';
  FLUSH PRIVILEGES;
  ```
* Run the Miniworld.py file in python3 in the terminal.
* You will be welcomed by a CLI(Command-Line-Interface) in which you can access the database as a customer or an administrator/    admin.
  * If you are a customer -> enter the username as 'customer'(without quotes). Customer has to be added by system root and will have limited privileges restricted to searching and viewing.
  * If you are an admin -> enter your username and password.
* Now, you can choose between the operations/types of queries required.(Ex: Insert,Delete,Modify,Search)
* You can choose to continue to ask your query or 'logout' from the database using the 'logout' option mentioned
