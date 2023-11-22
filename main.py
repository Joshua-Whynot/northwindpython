import mysql.connector #import db connector

#connect to db with credentials and select the database.
mydb = mysql.connector.connect(
    host="localhost",
    user="cs4430",
    password="cs4430",
    database="northwind"
)

def main():
    if mydb.is_connected():
        print('Database Connection Complete.') #print if the connection is active
    else:
        print('Database Connection Failed. View README for help.') #print if the connection is not active
        return -1 #exit the program if the connection is not active

    run = True #set run to true
    print('Welcome to the Northwind Database!') #print welcome message
    while run == True: #run the program until the user exits
        choice = get_input() #get user input
        match choice: #check user input
            case 1: 
                add_customer(mydb)
            case 2:
                add_order(mydb)
            case 3:
                add_product(mydb)
            case 4:
                remove_order(mydb)
            case 5:
                ship_order(mydb)
            case 6:
                view_pending_orders(mydb)
            case 7:
                more_options()
            case 8:
                print('Exiting...')
                run = False
            case 9:
                print('Invalid Input. Please try again.')
                continue
        
            
    

def get_input():
    print('Please select an option below.(enter only the number of the option)') #print options
    print('1. Add Customer')
    print('2. Add Order')
    print('3. Add Product')
    print('4. Remove Order')
    print('5. Ship Order')
    print('6. View Pending Orders')
    print('7. More Options')
    print('8. Exit')
    choice = input('Enter your choice: ') #get user input
    #check user input and return the choice
    if choice == '1':
        return 1
    elif choice == '2':
        return 2
    elif choice == '3':
        return 3
    elif choice == '4':
        return 4
    elif choice == '5':
        return 5
    elif choice == '6':
        return 6
    elif choice == '7':
        return 7
    elif choice == '8':
        return 8
    else:
        return 9
        

def add_customer(db):
    cursor = db.cursor() #create cursor
    try:
        print('Adding a new customer...')

        # Fetching the current highest ID and incrementing it by 1 for the new customer
        cursor.execute("SELECT MAX(ID) FROM Customers")
        max_id_result = cursor.fetchone()
        max_id = max_id_result[0] if max_id_result[0] is not None else 0
        new_customer_id = max_id + 1

        # Getting customer details
        company_name = input('Enter Company Name: ')
        last_name = input('Enter Last Name: ') 
        first_name = input('Enter First Name: ')
        job_title = input('Enter Job Title: ')
        phone = input('Enter Business Phone Number: ')
        fax = input('Enter Fax Number: ')
        address = input('Enter Address: ')
        city = input('Enter City: ')
        state = input('Enter State (Two letter State code ex:"MI" for Michigan): ')
        zipcode = input('Enter Zip Code: ')
        country = input('Enter Country: ')
        # insert customer into db
        query = "INSERT INTO Customers (ID, Company, LastName, FirstName, JobTitle, BusinessPhone, Fax, Address, City, State, ZIP, Country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (new_customer_id, company_name, last_name, first_name, job_title, phone, fax, address, city, state, zipcode, country)
        cursor.execute(query, values)
        db.commit()
        print(f'Customer added successfully with ID: {new_customer_id}') #confirm add
    except mysql.connector.Error as err:
        print(f"Error: {err}") #print error
    finally:
        cursor.close() #close our cursor after operation is complete

    return

def add_order(db):
    cursor = db.cursor()
    try:
        # Get the next OrderID by finding the maximum ID present and adding one
        cursor.execute("SELECT MAX(OrderID) FROM Orders")
        max_order_id_result = cursor.fetchone()
        max_order_id = max_order_id_result[0] if max_order_id_result[0] is not None else 0
        new_order_id = max_order_id + 1

        print('Adding a new order...')
        
        # Get order information from user
        customer_id = input('Enter Customer ID: ')
        employee_id = input('Enter Employee ID: ')
        order_date = input('Enter Order Date (YYYY-MM-DD): ')
        ship_address = input('Enter Ship Address: ')
        ship_city = input('Enter Ship City: ')
        ship_state = input('Enter Ship State: ')
        ship_zip = input('Enter Ship ZIP: ')
        ship_country = input('Enter Ship Country: ')
        
        # Insert the order into the Orders table with the new Order ID
        orders_query = """
            INSERT INTO Orders (OrderID, CustomerID, EmployeeID, OrderDate, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(orders_query, (new_order_id, customer_id, employee_id, order_date, ship_address, ship_city, ship_state, ship_zip, ship_country))
        
        # Get details for order items
        products_to_add = []
        while True:
            product_id = input('Enter Product ID (or "done" to finish): ')
            if product_id.lower() == 'done':
                break
            
            # Check if the product ID exists and is not discontinued
            cursor.execute("SELECT ID, Discontinued FROM Products WHERE ID = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                print(f"Product ID {product_id} does not exist.")
                continue
            elif product[1]:
                print(f"Product ID {product_id} is discontinued and cannot be added to the order.")
                continue
            
            quantity = input('Enter Quantity: ')
            discount = input('Enter Discount: ')
            
            # Get the list price from the Products table
            cursor.execute("SELECT ListPrice FROM Products WHERE ID = %s", (product_id,))
            list_price = cursor.fetchone()[0]
            
            products_to_add.append((new_order_id, product_id, quantity, list_price, discount))
        
        if not products_to_add:
            print("No products added. Order will not be created.")
            return
        
        # Insert each product into the Order_Details table
        details_query = """
            INSERT INTO Order_Details (OrderID, ProductID, Quantity, UnitPrice, Discount) 
            VALUES (%s, %s, %s, %s, %s)
        """
        for product_detail in products_to_add:
            cursor.execute(details_query, product_detail)
        
        db.commit()
        print(f'Order {new_order_id} added successfully with {len(products_to_add)} products.')
    except mysql.connector.Error as err:
        db.rollback()  # Rollback in case of error
        print(f"Error: {err}")
    finally:
        cursor.close()


def add_product(db):
    print('Please enter the following information to add a product.')
    return

def remove_order(db):
    cursor = db.cursor()
    try:
        order_id_to_remove = input('Enter the Order ID to remove: ')

        # First, delete related records from Order_Details table
        delete_order_details_query = "DELETE FROM Order_Details WHERE OrderID = %s"
        cursor.execute(delete_order_details_query, (order_id_to_remove,))

        # Next, delete the record from the Orders table
        delete_order_query = "DELETE FROM Orders WHERE OrderID = %s"
        cursor.execute(delete_order_query, (order_id_to_remove,))

        db.commit()
        print(f'Order {order_id_to_remove} and its details have been successfully removed.')
    except mysql.connector.Error as err:
        db.rollback()  # Rollback in case of error
        print(f"Error: {err}")
    finally:
        cursor.close()

def ship_order(db):
    cursor = db.cursor()
    try:
        order_id_to_ship = input('Enter the Order ID to ship: ')
        
        # Check the stock for each product in the order
        cursor.execute("""
            SELECT ProductID, Quantity
            FROM Order_Details
            WHERE OrderID = %s
        """, (order_id_to_ship,))
        order_details = cursor.fetchall()
        
        for product_id, quantity_ordered in order_details:
            # Calculate total quantity available for the product
            cursor.execute("""
                SELECT SUM(Quantity)
                FROM Inventory_Transactions
                WHERE ProductID = %s AND TransactionType IN (1, 3)  # Assuming 1 and 3 correspond to 'Received' and 'On Hold'
            """, (product_id,))
            quantity_purchased = cursor.fetchone()[0] or 0
            
            cursor.execute("""
                SELECT SUM(Quantity)
                FROM Inventory_Transactions
                WHERE ProductID = %s AND TransactionType = 2  # Assuming 2 corresponds to 'Sold'
            """, (product_id,))
            quantity_sold = cursor.fetchone()[0] or 0
            
            quantity_available = quantity_purchased - quantity_sold
            if quantity_available < quantity_ordered:
                raise Exception(f"Cannot ship order {order_id_to_ship}. Not enough stock for product {product_id}.")
        
        # If all products are in stock, proceed to update the Orders table with shipping details
        ship_date = input('Enter Ship Date (YYYY-MM-DD): ')
        shipper_id = input('Enter Shipper ID: ')
        shipping_fee = input('Enter Shipping Fee: ')
        
        cursor.execute("""
            UPDATE Orders
            SET ShippedDate = %s, ShipperID = %s, ShippingFee = %s
            WHERE OrderID = %s
        """, (ship_date, shipper_id, shipping_fee, order_id_to_ship))
        
        # Insert inventory transactions for each product sold
        for product_id, quantity_ordered in order_details:
            cursor.execute("""
                INSERT INTO Inventory_Transactions (TransactionType, TransactionCreatedDate, ProductID, Quantity, CustomerOrderID)
                VALUES (2, NOW(), %s, %s, %s)  # Assuming 2 corresponds to 'Sold'
            """, (product_id, quantity_ordered, order_id_to_ship))
        
        db.commit()
        print(f'Order {order_id_to_ship} has been shipped successfully.')
    except Exception as e:
        db.rollback()  # Rollback in case of any error
        print(f"Error: {e}")
    finally:
        cursor.close()


def view_pending_orders(db):
    cursor = db.cursor()
    try:
        print('Fetching pending orders...')
        
        # Select orders that have not been shipped, ordered by OrderDate
        query = """
            SELECT OrderID, CustomerID, OrderDate, ShipName, ShipAddress, ShipCity, ShipState, ShipZIP, ShipCountry
            FROM Orders
            WHERE ShippedDate IS NULL
            ORDER BY OrderDate ASC
        """
        cursor.execute(query)
        pending_orders = cursor.fetchall()
        
        if not pending_orders:
            print("There are no pending orders.")
            return
        
        print(f"{'OrderID':<10} {'CustomerID':<12} {'OrderDate':<12} {'ShipName':<20} {'ShipAddress':<20} {'ShipCity':<15} {'ShipState':<10} {'ShipZIP':<10} {'ShipCountry':<15}")
        for order in pending_orders:
            print(f"{order[0]:<10} {order[1]:<12} {str(order[2]):<12} {order[3]:<20} {order[4]:<20} {order[5]:<15} {order[6]:<10} {order[7]:<10} {order[8]:<15}")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()


def more_options():
    print('More options coming soon...')
    return

#call main only if this file is the main script being ran.
if __name__ == "__main__": 
    main()