import mysql.connector
import os
import re
import bcrypt
from getpass import getpass
from datetime import datetime

from time import sleep

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

## App map 
## 1. Register
## 2. Login 
    ## 3. Rent a car
    ## 4. Rental stats
    ## 5. Car stats
    ## 6. Brand stats
    ## 7. Company stats
    ## 8. User info
        ## 9. Update info
        ## 10. Delete account
    ## 11. Logout
## 12. Exit

def get_db_connection():

    try:
        db = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("DATABASE")
        )

        print("Connected to the database.")

        return db
        
    except Exception as e:
        print("An error occurred while connecting to the database.")
        print(e)
        exit(1)

def register_user(db) :

    console = Console()
    mycursor = db.cursor()

    print("Register")
    print("--------------------")

    while True:

        ## First name validation
        print("Enter your first name: ")
        firstname = input()

        if len(firstname) < 1 or len(firstname) > 32:
            console.print("First name must be between 1 and 32 characters. Please try again.", style="bold red")
        else:
            break

    ## Last name validation
    while True:
        print("Enter your last name: ")
        lastname = input()

        if len(lastname) < 1 or len(lastname) > 32:
            console.print("Last name must be between 1 and 32 characters. Please try again.", style="bold red")
        else:
            break

    ## Phone number validation
    while True:
        print("Enter your phone number: ")
        phoneNumber = input()

        if len(phoneNumber) < 1 or len(phoneNumber) > 10:
            console.print("Phone number must be 10 digits. Please try again.", style="bold red")
        else:
            if not re.match(r"^\d{10}$", phoneNumber):
                console.print("Invalid phone number format. Please try again.", style="bold red")
            else:
                break

    ## Email validation
    while True:
        print("Enter your email: ")
        email = input()

        if len(email) < 1:
            console.print("Email cannot be empty. Please try again.", style="bold red")
        else:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                console.print("Invalid email format. Please try again.", style="bold red")
            else:
                mycursor.execute("SELECT * FROM `User` WHERE email = %s", (email,))

                if mycursor.fetchone():
                    console.print("Email already exists. Please try again.", style="bold red")
                else:
                    break

    ## Password validation
    while True:
        password = getpass("Enter your password: ")

        if len(password) < 1:
            console.print("Password cannot be empty. Please try again.", style="bold red")
        else:
            ## isComplexEnough: inputs.password.value.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@;?#\$%\^&\*])/),
            if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@;?#\$%\^&\*])", password):
                console.print("Password must contain at least one lowercase letter, one uppercase letter, one number, and one special character. Please try again.", style="bold red")
            else:
                print("Confirm your password: ")
                confirm_password = getpass("Confirm your password: ")

                if password != confirm_password:
                    console.print("Passwords do not match. Please try again.", style="bold red")
                else:
                    encrypted_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
                    break

    ## Type of user validation
    while True:
        print("Are you a private individual or an employee of a company? (private/employee)")
        
        user_type = input()

        if user_type.lower() not in ["private", "employee"]:
            console.print("Invalid user type. Please try again.", style="bold red")
        else:
            break

    ## Employee use that text below
    if user_type.lower() == "employee":

        is_employee = True

        ## Company name validation
        while True:
            print("Enter your company name: ")
            company_name = input()

            if len(company_name) < 1:
                console.print("Company name cannot be empty. Please try again.", style="bold red")
            else:
                mycursor.execute("SELECT * FROM Company WHERE name = %s", (company_name,))

                if not mycursor.fetchone():
                    console.print("Company does not exist. Please try again.", style="bold red")
                else:
                    break

        ## Department validation
        while True:
            print("Enter your department: ")
            department = input()

            if len(department) < 1 and len(department) > 32:
                console.print("Department must be between 1 and 32 characters. Please try again.", style="bold red")
            else:
                break

    
    ## Private individual use that text below
    if user_type.lower() == "private":
        is_employee = False

        while True:
            print("Enter your address: ")
            address = input()

            if len(address) < 1:
                print("Address cannot be empty. Please try again.")
            else:
                break

        ## Driving license validation
        while True:
            print("Enter your driving license number: ")
            drivingLicense = input()

            if len(drivingLicense) < 1:
                print("Driving license number cannot be empty. Please try again.")
            else:
                break

    ## Insert user into database
    mycursor.execute("START TRANSACTION")
    
    try:
        mycursor.execute("BEGIN")
        mycursor.execute("INSERT INTO `User` (firstname, lastname, email, phoneNumber, password) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, email, phoneNumber, encrypted_password))

        if is_employee:
            
            user_id = mycursor.lastrowid

            mycursor.execute("SELECT id FROM Company WHERE name = %s", (company_name,))
            company_id = mycursor.fetchone()[0]
            
            mycursor.execute("INSERT INTO Employee (id, companyId, department) VALUES (%s, %s, %s)", (user_id, company_id, department)) 
        else:
            mycursor.execute("INSERT INTO PrivateIndividual (id, address, driverLicense) VALUES (%s, %s, %s)", (mycursor.lastrowid, address, drivingLicense))

        mycursor.execute("COMMIT")

        os.system('clear')

        print("🎉 User registered successfully. ")
        print("Please login to continue. 🎉")
        print("\n")

    except Exception as e:
        mycursor.execute("ROLLBACK")
        print("An error occurred while registering the user. Please try again.")
        print(e)

def login_user(db) :
    print("Login")
    print("--------------------")

    mycursor = db.cursor()

    while True:
        print("Enter your email: ")
        email = input()

        if len(email) < 1:
            print("Email cannot be empty. Please try again.")
        else:
            mycursor.execute("SELECT * FROM `User` WHERE email = %s", (email,))

            user = mycursor.fetchone()

            if not user:
                print("User does not exist. Please try again.")
            else:
                break

    while True:
        print("Enter your password: ")
        password = getpass()

        if len(password) < 1:
            print("Password cannot be empty. Please try again.")
        else:

            source_password = user[4].encode("utf-8")

            plaintext = password.encode("utf-8")

            if not bcrypt.checkpw(plaintext, source_password):
                print("Incorrect password. Please try again.")
            else:
                print("Login successful.")
                break

    return user 

def rent_a_car(db, user):
    console = Console()
    mycursor = db.cursor()

    console.print("Rent a car 🚗", style="bold blue")
    
    while True:
        mycursor.execute("SELECT id, brand, model, year, color, pricePerKm, totalKm, nextAvailableDate FROM carStats WHERE hasReachedMaxKilometers = 0 ORDER BY nextAvailableDate DESC")
        cars = mycursor.fetchall()

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Brand")
        table.add_column("Model")
        table.add_column("Year")
        table.add_column("Price Per Km (€)")
        table.add_column("Total Km")
        table.add_column("Next Available Date", style="green")

        for car in cars:
            if car[7] == "Available now":
                style = "white"
            else:
                style = "grey30"
            table.add_row(str(car[0]), car[1], car[2], str(car[3]), f"{car[5]}€/km", str(car[6]), car[7], style=style)

        console.print(table)

        car_id = console.input("Enter the ID of the car you want to rent: ")

        mycursor.execute("SELECT * FROM carStats WHERE id = %s", (car_id,))
        car = mycursor.fetchone()

        if not car:
            console.print("Car does not exist. Please try again.", style="bold red")
        else:
            if car[6] != "Available now":
                console.print("Car is already rented. Please try again.", style="bold red")
            else:
                break

    while True:
        endDate = console.input("Enter the end date of the rental (YYYY-MM-DD): ")
        startDate = datetime.today().strftime('%Y-%m-%d')

        if not re.match(r"\d{4}-\d{2}-\d{2}", endDate):
            console.print("Invalid date format. Please try again.", style="bold red")
        else:
            if endDate < startDate:
                console.print("End date must be after Today. Please try again.", style="bold red")
            else:
                break

    try:
        mycursor.execute("INSERT INTO RentalContract (carId, userId, startDate, endDate) VALUES (%s, %s, %s, %s)", (car_id, user[0], startDate, endDate))
        console.print("Car rented successfully. 🎉", style="bold green")

    except Exception as e:
        console.print("An error occurred while renting the car. Please try again.", style="bold red")
        console.print(str(e))

def rental_stats(db):
    console = Console()
    mycursor = db.cursor()

    choice = console.input("Do you want to see a certain year's rental statistics or all years? (year/all) ")

    if choice.lower() == "year":
        year = console.input("Enter the year: ")
        mycursor.execute("SELECT * FROM rentalStats WHERE year = %s", (year,))
        rentals = mycursor.fetchall()

        console.print(f"Rental statistics for {year} 📊")
    else:
        mycursor.execute("SELECT * FROM rentalStats")
        rentals = mycursor.fetchall()

        console.print("Rental statistics 📊")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Year")
    table.add_column("Month")
    table.add_column("Total rentals")
    table.add_column("Total Kilometers")
    table.add_column("Total revenue")

    for rental in rentals:
        table.add_row(str(rental[0]), str(rental[1]), str(rental[2]), str(rental[3]), str(rental[4]))

    console.print(table)
    console.input("Press any key to continue...")

def car_stats(db):
    console = Console()
    mycursor = db.cursor()

    console.print("Car statistics 🚗")
    
    mycursor.execute("SELECT * FROM carStats")
    cars = mycursor.fetchall()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Brand")
    table.add_column("Model")
    table.add_column("Year")
    table.add_column("Color")
    table.add_column("Price per km")
    table.add_column("Total rentals")
    table.add_column("Total km")
    table.add_column("Revenue")
    table.add_column("Status")

    for car in cars:
        status = "Has reached maximum kilometers" if car[10] == 1 else "Available now" if car[6] == "Available now" else f"Next available date: {car[6]}"
        table.add_row(str(car[0]), car[1], car[2], str(car[3]), car[4], str(car[5]), str(car[7]), str(car[8]), str(car[9]), status)

    console.print(table)
    console.input("Press any key to continue...")

def brand_stats(db):
    console = Console()
    mycursor = db.cursor()

    console.print("Brand statistics 🚗")

    mycursor.execute("SELECT name, totalCars, totalRentals, totalKm, Revenue, mostRentedCar FROM brandStats")
    brands = mycursor.fetchall()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Brand")
    table.add_column("Total cars")
    table.add_column("Total rentals")
    table.add_column("Total km")
    table.add_column("Revenue")
    table.add_column("Most rented car")

    for brand in brands:
        table.add_row(brand[0], str(brand[1]), str(brand[2]), str(brand[3]), str(brand[4]), brand[5])

    console.print(table)
    console.input("Press any key to continue...")

def company_stats(db):
    console = Console()
    mycursor = db.cursor()

    console.print("Company statistics 🏢")

    mycursor.execute("SELECT name, totalEmployee, totalRentals, totalKm, Revenue FROM companyStats")
    companies = mycursor.fetchall()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Company")
    table.add_column("Total employees")
    table.add_column("Total rentals")
    table.add_column("Total revenue")

    for company in companies:
        table.add_row(company[0], str(company[1]), str(company[2]), str(company[3]), str(company[4]))

    console.print(table)
    console.input("Press any key to continue...")

def user_info(db, user):
    os.system('clear')

    print(user)

    console = Console()
    mycursor = db.cursor()

    mycursor.execute("SELECT id, firstName, lastName, email, phoneNumber FROM `User` WHERE id = %s", (user[0],))
    user_data = mycursor.fetchone()

    if user_data:
        user_info_panel = f"First name: {user_data[1]}\n"
        user_info_panel += f"Last name: {user_data[2]}\n"
        user_info_panel += f"Email: {user_data[3]}\n"
        user_info_panel += f"Phone: {user_data[4]}"

        mycursor.execute("SELECT * FROM Employee WHERE id = %s", (user_data[0],))
        employee = mycursor.fetchone()

        if employee:
            mycursor.execute("SELECT name FROM Company WHERE id = %s", (employee[1],))
            company = mycursor.fetchone()

            employee_info_panel = f"Company: {company[0]}\n"
            employee_info_panel += f"Department: {employee[2]}"
            console.print(Panel(employee_info_panel, title="Employee Information", expand=False))
        else:
            
            mycursor.execute("SELECT * FROM PrivateIndividual WHERE id = %s", (user_data[0],))
            private = mycursor.fetchone()

            if private:
                private_info_panel = f"Address: {private[1]}\n"
                private_info_panel += f"Driving license: {private[2]}"
                console.print(Panel(private_info_panel, title="Private Individual Information", expand=False)) 

        console.print(Panel(user_info_panel, title="User Information", expand=False))
    
    print("--------------------")

    print("Please select an option: ")

    print("\t1. Update information")

    print("\t2. Delete account")

    print("\t3. Go back")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        result = update_user_info(db, user)
        print("result")
        print(result)
        user_info(db, result)
    elif choice == 2:
        delete_user(db, user)
        return None
    elif choice == 3:
        return user
    else:
        console.print("Invalid choice. Please try again.", style="bold red")

def update_user_info(db, user):

    console = Console()
    mycursor = db.cursor()

    print("Update information")
    print("--------------------")

    print("Enter your first name (do not type anything to keep the current value): ")
    firstname = input()

   
    print("Enter your last name (do not type anything to keep the current value): ")
    lastname = input()

    while True:
        print("Enter your phone number (do not type anything to keep the current value): ")
        phone = input()

        ## if phone number is empty, keep the current value
        if not phone:
            break
        else:
            if not re.match(r"^\d{10}$", phone):
                console.print("Invalid phone number format. Please try again.", style="bold red")
            else:
                break

    
    new_firstname = firstname if firstname else user[1]
    new_lastname = lastname if lastname else user[2]
    new_phone = phone if phone else user[5]

    print("New first name: ", new_firstname)
    print("New last name: ", new_lastname)
    print("New phone number: ", new_phone)

    try:
        mycursor.execute("UPDATE `User` SET firstName = %s, LastName = %s, phoneNumber = %s WHERE id = %s", (new_lastname, new_firstname, new_phone, user[0]))
        print("User information updated successfully.")

        mycursor.execute("SELECT * FROM `User` WHERE id = %s", (user[0],))

        user = mycursor.fetchone()

        return user
    
    except Exception as e:
        console.print("An error occurred while updating the user information. Please try again.", style="bold red")
        print(e)
    finally:
        mycursor.close()

def delete_user(db, user):

    console = Console()

    mycursor = db.cursor()

    print("Delete account")
    print("--------------------")

    print("Are you sure you want to delete your account? (yes/no)")
    choice = input()

    if choice.lower() == "yes":
        try:
            mycursor.execute("DELETE FROM `User` WHERE id = %s", (user[0],))
            print("User deleted successfully.")
            return
        except Exception as e:
            console.print("An error occurred while deleting the user. Please try again.", style="bold red")
            print(e)
    else:
        return


if __name__ == "__main__":

    console = Console()
    db = get_db_connection()

    user = None

    while True:

        os.system('clear')

        if user:
            print(f"Welcome back, {user[1]} {user[2]} 👋 ")
            print("Please select an option: ")
            print("\t1. Rent a car\n\t2. Rental stats\n\t3. Car stats\n\t4. Brand stats\n\t5. Company stats\n\t6. User info\n\t7. Logout\n\t8. Exit")
            
            choice = int(input("Enter your choice: "))

            if choice == 1:
                os.system('clear')
                rent_a_car(db, user)
            elif choice == 2:
                os.system('clear')
                rental_stats(db)
            elif choice == 3:
                os.system('clear')
                car_stats(db)
            elif choice == 4:
                os.system('clear')
                brand_stats(db)
            elif choice == 5:
                os.system('clear')
                company_stats(db)
            elif choice == 6:
                os.system('clear')
                user = user_info(db, user)
                continue
            elif choice == 7:
                print("Logging out...")
                user = None
                continue
            elif choice == 8:
                print("Exiting...")
                break
        else:
            print("Welcome to the Autoflex !!! \n")
            print("Please select an option: ")
            print("\t1. Register\n\t2. Login\n\t3. Exit")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                os.system('clear')
                register_user(db)
                print("Please login to continue.")
            elif choice == 2:
                os.system('clear')
                user = login_user(db)
            elif choice == 3:
                print("Exiting...")
                break
            else:
                console.print("Invalid choice. Please try again.", style="bold red")

    db.close()

    

    


    
    
    

