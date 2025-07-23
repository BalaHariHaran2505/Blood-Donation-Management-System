# Blood-Donation-Management-System
A command-line based project built with Python and MySQL to simulate real-world blood bank operations. It supports donor and recipient registration, donation tracking, inventory updates, request processing, and reporting.

## Features
* Donor registration with auto-generated ID
* Recipient registration and blood request logging
* Donation entry with automatic inventory update via trigger
* Real-time blood request approval based on available stock
* Blood inventory and donation history reports

## Technologies
* Python 3
* MySQL
* mysql-connector-python

## How to Run
1. Set up the database using `schema.sql`
2. Install dependencies:

   ```
   pip install mysql-connector-python
   ```
3. Configure `db_config.py` with your MySQL credentials
4. Run the application:

   ```
   python main.py
   ```

## Project Status
Completed for internship submission. Supports all required features with real-time database integration.
