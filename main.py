from db_config import get_connection

# 1. Donor Registration
def register_donor():
    print("\n Donor Registration")
    name = input("Name: ")
    age = int(input("Age: "))
    blood_group = input("Blood Group: ").upper()
    contact = input("Contact: ")
    last_donation = input("Last Donation Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Donors (Name, Age, BloodGroup, Contact, LastDonationDate)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, age, blood_group, contact, last_donation))
    conn.commit()
    donor_id = cursor.lastrowid
    print(f" New donor registered: {name} ({blood_group}) [Donor ID: {donor_id}]")
    cursor.close()
    conn.close()

# 2. Recipient Registration
def register_recipient():
    print("\n Recipient Registration")
    name = input("Name: ")
    age = int(input("Age: "))
    blood_group = input("Blood Group: ").upper()
    contact = input("Contact: ")
    blood_required = int(input("Units Required: "))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Recipients (Name, Age, BloodGroup, Contact, BloodRequired)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, age, blood_group, contact, blood_required))
    conn.commit()
    recipient_id = cursor.lastrowid
    print(f" New blood request registered: {name} ({blood_group}) needs {blood_required} units.")
    cursor.close()
    conn.close()

# 3. Blood Donation Entry
def donate_blood():
    print("\n Blood Donation Entry")
    donor_id = int(input("Donor ID: "))
    blood_group = input("Blood Group: ").upper()
    donation_date = input("Donation Date (YYYY-MM-DD): ")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Donations (DonorID, BloodGroup, DonationDate)
        VALUES (%s, %s, %s)
    """, (donor_id, blood_group, donation_date))
    conn.commit()
    print(f" Donation recorded: Donor ID {donor_id} ({blood_group}) donated 1 unit.")

    cursor.execute("SELECT UnitsAvailable FROM BloodInventory WHERE BloodGroup = %s", (blood_group,))
    units = cursor.fetchone()[0]
    print(f" Updated Blood Inventory: {blood_group} → {units} units available.")
    cursor.close()
    conn.close()

# 4. Blood Requesting Process
def request_blood():
    print("\n Blood Request Processing")
    blood_group = input("Requested Blood Group: ").upper()
    units_requested = int(input("Units Requested: "))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT UnitsAvailable FROM BloodInventory WHERE BloodGroup = %s", (blood_group,))
    result = cursor.fetchone()
    available_units = result[0] if result else 0

    print(f" Available stock for {blood_group}: {available_units} units.")

    if available_units >= units_requested:
        print(" Request can be approved.")
        cursor.execute("""
            UPDATE BloodInventory
            SET UnitsAvailable = UnitsAvailable - %s
            WHERE BloodGroup = %s
        """, (units_requested, blood_group))
        conn.commit()
        print(f" Blood issued: {units_requested} unit(s) of {blood_group}")
    else:
        print(" Request denied: Not enough stock.")

    cursor.close()
    conn.close()

# 5. Blood Inventory Report
def show_inventory():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BloodInventory")
    print("\n Blood Inventory Report")
    print("-----------------------------")
    print("Blood Group | Units Available")
    print("-----------------------------")
    for row in cursor.fetchall():
        print(f"{row[0]:<12} | {row[1]}")
    print("-----------------------------")
    cursor.close()
    conn.close()

# 6. Donation History Report
def donation_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Donors.Name, Donations.BloodGroup, Donations.DonationDate
        FROM Donations
        JOIN Donors ON Donations.DonorID = Donors.DonorID
    """)
    print("\n Donation History Report")
    print("-------------------------------")
    print("Name           | Group | Date")
    print("-------------------------------")
    for row in cursor.fetchall():
        print(f"{row[0]:<15} | {row[1]:<5} | {row[2]}")
    print("-------------------------------")
    cursor.close()
    conn.close()

# Menu
def main():
    while True:
        print("\n Blood Donation Management System")
        print("1. Donor Registration")
        print("2. Recipient Registration")
        print("3. Blood Donation Entry")
        print("4. Blood Request Processing")
        print("5. Blood Inventory Report")
        print("6. Donation History Report")
        print("0. Exit")

        choice = input("Select an option: ")
        if choice == "1":
            register_donor()
        elif choice == "2":
            register_recipient()
        elif choice == "3":
            donate_blood()
        elif choice == "4":
            request_blood()
        elif choice == "5":
            show_inventory()
        elif choice == "6":
            donation_history()
        elif choice == "0":
            print(" Goodbye!")
            break
        else:
            print(" Invalid option. Try again.")

if __name__ == "__main__":
    main()