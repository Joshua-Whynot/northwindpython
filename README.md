Program: CS4430 Assignment 4
Author: Joshua Whynot
Date: 11/20/2023


                OVERVIEW    
-----------------------------------------
This program enables a user to interact with the Microsoft Northwind Trading Company training Database.
The user will be able to perform the following actions:
    1: Add Customer
    2: Add Order
    3: Add Product
    4: Remove Order
    5: Ship Order
    6: View Pending Orders
    7: More Options (WIP)
    8: Exit

                USAGE
-----------------------------------------
This Program is written with Python3 and uses the MySQL connectory library to connect and query an SQL database. This guide assumes you already have MySQL installed and setup.

Getting Started:
    1. Install Python3: 
        Windows: Visit https://www.python.org/downloads/ to select the correct version for your machine.
        Linux CLI: "sudo apt install Python3"
    2. Install PIP:
        Windows: PIP is installed with Python3 with the Windows Installer
        Linux CLI: "sudo apt install pip"
    3. Install MySQL Connector for Python3:
        For both Windows and Linux type the following: "python3 -m pip install mysql-connector-python"

Opening the Database in MySQL:
    1. Populate the DB in MySQL (fill in your username and provide your password): "mysql -p -u <YOUR_USERNAME> < northwind.sql"
    2. Open the DB in MySQL: "mysql -p -u <YOUR_USERNAME>"

Running the Program:
    First, replace the user credentials in "main.py" at the top of the file with your own database credentials. The default is the values outlines previously in the class.
    To run the program open the command line and type: "python3 main.py" in the project directory. This can be used on Linux or Windows.
    The options in the program will be provided to you.
    If you are experiencing issues with the database connection ensure the credentials are correct and a database is active at the address.
    