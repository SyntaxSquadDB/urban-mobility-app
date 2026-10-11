import os
import mysql.connector
from dotenv import load_dotenv
from decimal import Decimal
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT", 3306))
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
DATABASE = os.getenv("DB_NAME", "urban_mobility_db")

def get_connection():
    """Establishes and returns a secure connection to the MySQL database."""
    return mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def _format_value(val):
    """Helper function to format different data types for clean console output."""
    if val is None:
        return "NULL"
    elif isinstance(val, Decimal):
        return f"{val:.2f}"
    elif isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M:%S")
    return str(val)

def _print_table(headers, rows):
    """Helper function to print query results in a neat, aligned tabular format."""
    if not rows:
        print("No results found.\n")
        return

    # Calculate column widths based on headers and data
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(_format_value(val)))
            
    # Print headers
    header_row = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
    print(header_row)
    print("-" * len(header_row))
    
    # Print rows
    for row in rows:
        print(" | ".join(_format_value(val).ljust(w) for val, w in zip(row, col_widths)))
    print("\n")

def run_migrations():
    """Executes schema creation and data insertion from external .sql files."""
    print("--- Running Database Migrations ---")
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        migration_files = ['migrations/init.sql', 'migrations/insert.sql']
        
        for filepath in migration_files:
            if not os.path.exists(filepath):
                print(f"Skipping {filepath} (file not found).")
                continue
                
            with open(filepath, 'r') as file:
                sql_script = file.read()
                
            # Split by semicolon and execute each statement
            statements = sql_script.split(';')
            for statement in statements:
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
            print(f"Successfully executed {filepath}")
            
    except mysql.connector.Error as err:
        print(f"Error running migrations: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    print("-" * 35 + "\n")

def run_all_queries():
    """Executes all SQL queries from Section 6.0 and prints formatted results."""
    queries = [
        # 6.1 Simple Queries
        ("Query 1: All registered vehicles and their license plates",
         "SELECT vehicle_id, license_plate, make_model FROM VEHICLE;"),
         
        ("Query 2: Vehicle inspection logs ordered by date",
         "SELECT log_id, inspection_date, status, vehicle_id FROM INSPECTION_LOG ORDER BY inspection_date DESC;"),
         
        # 6.2 Medium Queries
        ("Query 3: Formatted passenger names and their payment methods",
         "SELECT CONCAT(P.first_name, ' ', P.last_name) AS full_name, M.card_type, M.last_four FROM PASSENGER P JOIN PAYMENT_METHOD M ON P.passenger_id = M.passenger_id;"),
         
        ("Query 4: Identify drivers using a specific vehicle brand (Toyota)",
         "SELECT driver_id, first_name, last_name FROM DRIVER WHERE driver_id IN (SELECT driver_id FROM VEHICLE WHERE make_model LIKE '%Toyota%');"),
         
        ("Query 5: Total revenue and average trip distance per driver",
         "SELECT D.first_name, D.last_name, SUM(T.fare) AS total_revenue, AVG(T.distance_km) AS average_distance FROM DRIVER D JOIN TRIP T ON D.driver_id = T.driver_id GROUP BY D.driver_id, D.first_name, D.last_name ORDER BY total_revenue DESC;"),
         
        ("Query 6: Filter trips by specific Date functions and Joins (Oct 2026)",
         "SELECT T.trip_id, T.trip_date, T.fare, P.email AS passenger_email FROM TRIP T JOIN PASSENGER P ON T.passenger_id = P.passenger_id WHERE MONTH(T.trip_date) = 10 AND YEAR(T.trip_date) = 2026;"),
         
        # 6.3 Complex Queries
        ("Query 7: High-Earning Drivers with Distance Thresholds",
         "SELECT D.driver_id, CONCAT(D.first_name, ' ', D.last_name) AS driver_name, COUNT(T.trip_id) AS total_trips, SUM(T.fare) AS total_earnings FROM DRIVER D JOIN TRIP T ON D.driver_id = T.driver_id JOIN VEHICLE V ON D.driver_id = V.driver_id GROUP BY D.driver_id, driver_name HAVING total_earnings > 100.00 AND SUM(T.distance_km) >= 10.00;"),
         
        ("Query 8: High-Risk Trips Generating Safety Alerts",
         "SELECT P.passenger_id, P.first_name, P.last_name, P.email FROM PASSENGER P WHERE P.passenger_id IN (SELECT T.passenger_id FROM TRIP T WHERE (T.distance_km > 10.00 OR T.fare > 100.00) AND T.trip_id IN (SELECT trip_id FROM SAFETY_ALERT));"),
         
        ("Query 9: Passenger Spending Habits by Card Type",
         "SELECT P.passenger_id, P.first_name, M.card_type, COUNT(T.trip_id) AS trip_count, AVG(T.fare) AS avg_fare_spent FROM PASSENGER P JOIN PAYMENT_METHOD M ON P.passenger_id = M.passenger_id JOIN TRIP T ON P.passenger_id = T.passenger_id GROUP BY P.passenger_id, P.first_name, M.card_type HAVING (avg_fare_spent > 50.00 AND trip_count >= 1) OR M.card_type = 'Visa';"),
         
        ("Query 10: Comprehensive Fleet Safety Audit",
         "SELECT V.vehicle_id, V.license_plate, D.license_number, COUNT(T.trip_id) AS operational_trips, SUM(T.distance_km) AS fleet_distance FROM VEHICLE V JOIN DRIVER D ON V.driver_id = D.driver_id LEFT JOIN TRIP T ON V.vehicle_id = T.vehicle_id GROUP BY V.vehicle_id, V.license_plate, D.license_number HAVING operational_trips > 0 AND (fleet_distance > 5.00 OR fleet_distance < 100.00) ORDER BY fleet_distance DESC;")
    ]

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        for title, sql in queries:
            print(f"--- {title} ---")
            cursor.execute(sql)
            
            # Fetch headers
            headers = [desc[0] for desc in cursor.description]
            # Fetch all rows
            rows = cursor.fetchall()
            
            _print_table(headers, rows)
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    # Note: You can comment out run_migrations() if your DB is already set up to avoid overwriting data
    run_migrations()
    run_all_queries()
    print("All queries executed successfully.")