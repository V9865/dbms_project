import mysql.connector
from datetime import datetime

def connect():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    conn.autocommit = False
    return conn

# -------------------------------
# INITIALIZE DATABASE + TABLES
# -------------------------------
def initialize_database(cursor):
    cursor.execute("CREATE DATABASE IF NOT EXISTS airlinedb;")
    cursor.execute("USE airlinedb;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Airline(
        airline_id INT PRIMARY KEY,
        icao_code VARCHAR(10) UNIQUE,
        name VARCHAR(100) NOT NULL,
        country VARCHAR(100),
        founding_year INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Airport(
        iata_code VARCHAR(10) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        city VARCHAR(100),
        country VARCHAR(100) NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Aircraft(
        tail_number VARCHAR(20) PRIMARY KEY,
        model VARCHAR(50),
        manufacturer VARCHAR(50),
        seating_cap INT NOT NULL CHECK (seating_cap > 0),
        airline_id INT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Route(
        route_id INT PRIMARY KEY,
        src_airport VARCHAR(20) NOT NULL,
        dst_airport VARCHAR(20) NOT NULL,
        dist_km INT CHECK (dist_km > 0),
        dur_hrs INT CHECK (dur_hrs > 0),
        CHECK (src_airport <> dst_airport)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FlightSchedule(
        schedule_id INT PRIMARY KEY,
        flight_number VARCHAR(20),
        departure_time TIME,
        arrival_time TIME,
        days_operated VARCHAR(50),
        route_id INT,
        airline_id INT,
        tail_number VARCHAR(20)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS FlyingStatus(
        status_id INT PRIMARY KEY,
        op_date DATE,
        status VARCHAR(20),
        delay_minutes INT CHECK (delay_minutes >= 0),
        schedule_id INT,
        CHECK (status IN ('OnTime','Delayed','Cancelled','Landed'))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Passenger(
        passenger_id INT PRIMARY KEY,
        passport_no VARCHAR(20) UNIQUE,
        name VARCHAR(100) NOT NULL,
        dob DATE NOT NULL,
        nationality VARCHAR(50),
        email VARCHAR(100) UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Booking(
        booking_id INT PRIMARY KEY,
        booking_ref VARCHAR(20) UNIQUE,
        booking_date DATE,
        ticket_class VARCHAR(20),
        fare DECIMAL(10,2) CHECK (fare > 0),
        passenger_id INT,
        schedule_id INT,
        CHECK (ticket_class IN ('Economy','Business','First'))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS SeatAssignment(
        assignment_id INT PRIMARY KEY,
        seat_number VARCHAR(10),
        assigned_at TIMESTAMP,
        booking_id INT UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewMember(
        crew_id INT PRIMARY KEY,
        name VARCHAR(100),
        employee_id VARCHAR(20) UNIQUE,
        crew_type VARCHAR(20),
        CHECK (crew_type IN ('Pilot','CabinCrew'))
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pilot(
        crew_id INT PRIMARY KEY,
        license_no VARCHAR(50),
        rating VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CabinCrew(
        crew_id INT PRIMARY KEY,
        role VARCHAR(50),
        section VARCHAR(50)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CrewAssignment(
        assignment_id INT PRIMARY KEY,
        crew_id INT,
        schedule_id INT,
        role_on_flight VARCHAR(50)
    );
    """)

    _add_foreign_keys(cursor)
    print("Tables ensured.")
    cursor.execute("SHOW TABLES;")
    print("DEBUG Tables after creation:", cursor.fetchall())

def _add_foreign_keys(cursor):
    fk_statements = [
        ("fk_aircraft_airline",
         "ALTER TABLE Aircraft ADD CONSTRAINT fk_aircraft_airline "
         "FOREIGN KEY (airline_id) REFERENCES Airline(airline_id)"),
        ("fk_route_src_airport",
         "ALTER TABLE Route ADD CONSTRAINT fk_route_src_airport "
         "FOREIGN KEY (src_airport) REFERENCES Airport(iata_code)"),
        ("fk_route_dst_airport",
         "ALTER TABLE Route ADD CONSTRAINT fk_route_dst_airport "
         "FOREIGN KEY (dst_airport) REFERENCES Airport(iata_code)"),
        ("fk_schedule_route",
         "ALTER TABLE FlightSchedule ADD CONSTRAINT fk_schedule_route "
         "FOREIGN KEY (route_id) REFERENCES Route(route_id)"),
        ("fk_schedule_airline",
         "ALTER TABLE FlightSchedule ADD CONSTRAINT fk_schedule_airline "
         "FOREIGN KEY (airline_id) REFERENCES Airline(airline_id)"),
        ("fk_schedule_aircraft",
         "ALTER TABLE FlightSchedule ADD CONSTRAINT fk_schedule_aircraft "
         "FOREIGN KEY (tail_number) REFERENCES Aircraft(tail_number)"),
        ("fk_flyingstatus_schedule",
         "ALTER TABLE FlyingStatus ADD FOREIGN KEY (schedule_id) "
         "REFERENCES FlightSchedule(schedule_id) ON DELETE CASCADE"),
        ("fk_booking_passenger",
         "ALTER TABLE Booking ADD FOREIGN KEY (passenger_id) "
         "REFERENCES Passenger(passenger_id)"),
        ("fk_booking_schedule",
         "ALTER TABLE Booking ADD FOREIGN KEY (schedule_id) "
         "REFERENCES FlightSchedule(schedule_id) ON DELETE CASCADE"),
        ("fk_seatassignment_booking",
         "ALTER TABLE SeatAssignment ADD FOREIGN KEY (booking_id) "
         "REFERENCES Booking(booking_id) ON DELETE CASCADE"),
        ("fk_pilot_crew",
         "ALTER TABLE Pilot ADD FOREIGN KEY (crew_id) "
         "REFERENCES CrewMember(crew_id) ON DELETE CASCADE"),
        ("fk_cabincrew_crew",
         "ALTER TABLE CabinCrew ADD FOREIGN KEY (crew_id) "
         "REFERENCES CrewMember(crew_id) ON DELETE CASCADE"),
        ("fk_crewassignment_crew",
         "ALTER TABLE CrewAssignment ADD FOREIGN KEY (crew_id) "
         "REFERENCES CrewMember(crew_id) ON DELETE CASCADE"),
        ("fk_crewassignment_schedule",
         "ALTER TABLE CrewAssignment ADD FOREIGN KEY (schedule_id) "
         "REFERENCES FlightSchedule(schedule_id) ON DELETE CASCADE"),
    ]
    
    for name, stmt in fk_statements:
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as e:
            if e.errno in (1826, 1060):
                pass
            else:
                raise

# -------------------------------
# UTIL FUNCTIONS
# -------------------------------
def get_all_tables(cursor):
    cursor.execute("SHOW TABLES;")
    return [table[0] for table in cursor.fetchall()]

def get_table_columns(cursor, table_name):
    cursor.execute(f"DESCRIBE {table_name};")
    return cursor.fetchall()

def print_separator():
    print("-" * 60)

def pick_table(cursor):
    tables = get_all_tables(cursor)
    print("\nAvailable Tables:")
    for i, t in enumerate(tables, 1):
        print(f"  {i}. {t}")
    choice = input("\nEnter table number or name: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(tables):
        return tables[int(choice) - 1]
    elif choice in tables:
        return choice
    else:
        print("Invalid table selection.")
        return None

# ----------------
# CRUD OPERATIONS
# ----------------
def create_record(cursor, table_name, columns):
    values = []
    insert_cols = []
    for col in columns:
        field, dtype, is_nullable, key, default, extra = col
        if "auto_increment" in extra.lower():
            continue
        user_input = input(f"Enter value for {field} ({dtype}): ")
        insert_cols.append(field)
        if user_input == "" and is_nullable == "YES":
            values.append("NULL")
        elif "char" in dtype or "text" in dtype:
            values.append(f"'{user_input}'")
        elif "date" in dtype:
            date_value = datetime.strptime(user_input, "%Y-%m-%d")
            values.append(f"'{date_value.strftime('%Y-%m-%d')}'")
        else:
            values.append(user_input)
    query = f"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({', '.join(values)});"
    cursor.execute(query)
    print("Record inserted successfully.")

def retrieve_records(cursor, table_name):
    condition = input("Enter WHERE condition (or press Enter to fetch all): ")
    query = f"SELECT * FROM {table_name}"
    if condition.strip():
        query += f" WHERE {condition}"
    cursor.execute(query)
    rows = cursor.fetchall()
    if not rows:
        print("No records found.")
    else:
        for row in rows:
            print(row)

def update_record(cursor, table_name):
    set_clause = input("Enter SET clause (e.g., name='John', age=30): ")
    condition = input("Enter WHERE clause (e.g., id=2): ")
    query = f"UPDATE {table_name} SET {set_clause} WHERE {condition};"
    cursor.execute(query)
    print("Record(s) updated successfully.")

def delete_record(cursor, table_name):
    condition = input("Enter WHERE clause for deletion (e.g., id=2): ")
    query = f"DELETE FROM {table_name} WHERE {condition};"
    cursor.execute(query)
    print("Record(s) deleted successfully.")

# ================================
# SEARCH FLIGHTS
# ================================
def search_flights(cursor):
    print_separator()
    print("  SEARCH FLIGHTS")
    print_separator()
    print("  1. By Source Airport (e.g. BLR)")
    print("  2. By Destination Airport (e.g. DEL)")
    print("  3. By Flight Number (e.g. 6E201)")
    choice = input("Enter choice (1/2/3): ").strip()
    if choice == '1':
        code = input("Enter source airport IATA code: ").strip().upper()
        query = """
            SELECT fs.flight_number, a.name AS airline,
                   r.src_airport, r.dst_airport,
                   fs.departure_time, fs.arrival_time, fs.days_operated
            FROM FlightSchedule fs
            JOIN Route r ON fs.route_id = r.route_id
            JOIN Airline a ON fs.airline_id = a.airline_id
            WHERE r.src_airport = %s;
        """
        cursor.execute(query, (code,))
    elif choice == '2':
        code = input("Enter destination airport IATA code: ").strip().upper()
        query = """
            SELECT fs.flight_number, a.name AS airline,
                   r.src_airport, r.dst_airport,
                   fs.departure_time, fs.arrival_time, fs.days_operated
            FROM FlightSchedule fs
            JOIN Route r ON fs.route_id = r.route_id
            JOIN Airline a ON fs.airline_id = a.airline_id
            WHERE r.dst_airport = %s;
        """
        cursor.execute(query, (code,))
    elif choice == '3':
        fnum = input("Enter flight number: ").strip().upper()
        query = """
            SELECT fs.flight_number, a.name AS airline,
                   r.src_airport, r.dst_airport,
                   fs.departure_time, fs.arrival_time, fs.days_operated
            FROM FlightSchedule fs
            JOIN Route r ON fs.route_id = r.route_id
            JOIN Airline a ON fs.airline_id = a.airline_id
            WHERE fs.flight_number = %s;
        """
        cursor.execute(query, (fnum,))
    else:
        print("Invalid choice.")
        return
    rows = cursor.fetchall()
    print_separator()
    print(f"{'Flight':<10} {'Airline':<22} {'From':<6} {'To':<6} {'Dep':<10} {'Arr':<10} {'Days'}")
    print_separator()
    if not rows:
        print("No flights found.")
    else:
        for r in rows:
            print(f"{str(r[0]):<10} {str(r[1]):<22} {str(r[2]):<6} {str(r[3]):<6} {str(r[4]):<10} {str(r[5]):<10} {r[6]}")
    print_separator()

# ================================
# JOIN VIEW
# ================================
def view_booking_details(cursor):
    print_separator()
    print("  BOOKING DETAILS (JOIN VIEW)")
    print_separator()
    ref = input("Enter booking reference (e.g. BK-001) or press Enter for all: ").strip()
    query = """
        SELECT
            b.booking_ref,
            p.name AS passenger,
            p.nationality,
            fs.flight_number,
            r.src_airport,
            r.dst_airport,
            b.ticket_class,
            b.fare,
            sa.seat_number,
            fly.status,
            fly.op_date
        FROM Booking b
        JOIN Passenger p ON b.passenger_id = p.passenger_id
        JOIN FlightSchedule fs ON b.schedule_id = fs.schedule_id
        JOIN Route r ON fs.route_id = r.route_id
        LEFT JOIN SeatAssignment sa ON sa.booking_id = b.booking_id
        LEFT JOIN FlyingStatus fly ON fly.schedule_id = fs.schedule_id
    """
    if ref:
        query += " WHERE b.booking_ref = %s"
        cursor.execute(query, (ref,))
    else:
        cursor.execute(query)
    rows = cursor.fetchall()
    print_separator()
    if not rows:
        print("No bookings found.")
    else:
        for r in rows:
            print(f"Ref       : {r[0]}")
            print(f"Passenger : {r[1]} ({r[2]})")
            print(f"Flight    : {r[3]}  |  {r[4]} -> {r[5]}")
            print(f"Class     : {r[6]}  |  Fare: ${r[7]}  |  Seat: {r[8]}")
            print(f"Status    : {r[9]} on {r[10]}")
            print_separator()


# ================================
# STATS SUMMARY
# ================================
def show_stats(cursor):
    print_separator()
    print("  DATABASE STATISTICS SUMMARY")
    print_separator()
    cursor.execute("""
        SELECT a.name, COUNT(b.booking_id) AS total_bookings,
               SUM(b.fare) AS total_revenue
        FROM Airline a
        JOIN FlightSchedule fs ON a.airline_id = fs.airline_id
        JOIN Booking b ON fs.schedule_id = b.schedule_id
        GROUP BY a.name
        ORDER BY total_revenue DESC;
    """)
    rows = cursor.fetchall()
    print(f"\n{'Airline':<25} {'Bookings':<12} {'Revenue (USD)'}")
    print("-" * 50)
    for r in rows:
        print(f"{str(r[0]):<25} {str(r[1]):<12} ${r[2]}")
    cursor.execute("""
        SELECT status, COUNT(*) AS count
        FROM FlyingStatus
        GROUP BY status
        ORDER BY count DESC;
    """)
    rows = cursor.fetchall()
    print(f"\n{'Flight Status':<20} {'Count'}")
    print("-" * 30)
    for r in rows:
        print(f"{str(r[0]):<20} {r[1]}")
    cursor.execute("""
        SELECT r.src_airport, r.dst_airport, COUNT(b.booking_id) AS bookings
        FROM Route r
        JOIN FlightSchedule fs ON r.route_id = fs.route_id
        JOIN Booking b ON fs.schedule_id = b.schedule_id
        GROUP BY r.src_airport, r.dst_airport
        ORDER BY bookings DESC
        LIMIT 5;
    """)
    rows = cursor.fetchall()
    print(f"\n{'Route':<15} {'Bookings'}")
    print("-" * 25)
    for r in rows:
        print(f"{r[0]} -> {r[1]:<8} {r[2]}")
    print_separator()


# ================================
# BOOKING SUMMARY
# ================================
def booking_summary_report(cursor):
    print_separator()
    print("  PASSENGER BOOKING SUMMARY REPORT")
    print_separator()
    cursor.execute("""
        SELECT
            p.passenger_id,
            p.name,
            p.nationality,
            COUNT(b.booking_id) AS total_bookings,
            SUM(b.fare) AS total_spent,
            GROUP_CONCAT(b.booking_ref ORDER BY b.booking_date SEPARATOR ', ') AS booking_refs
        FROM Passenger p
        LEFT JOIN Booking b ON p.passenger_id = b.passenger_id
        GROUP BY p.passenger_id, p.name, p.nationality
        ORDER BY total_spent DESC;
    """)
    rows = cursor.fetchall()
    print(f"\n{'ID':<5} {'Name':<20} {'Country':<12} {'Bookings':<10} {'Total Spent':<15} {'Refs'}")
    print("-" * 80)
    for r in rows:
        spent = f"${r[4]}" if r[4] else "$0"
        refs = r[5] if r[5] else "None"
        print(f"{r[0]:<5} {str(r[1]):<20} {str(r[2]):<12} {str(r[3]):<10} {spent:<15} {refs}")
    print_separator()


def print_main_menu():
    print("\n" + "=" * 60)
    print("         AIRLINE MANAGEMENT SYSTEM")
    print("=" * 60)
    print("  --- CRUD Operations ---")
    print("  1. Create   — Insert a new record")
    print("  2. Retrieve — View records")
    print("  3. Update   — Modify a record")
    print("  4. Delete   — Remove a record")
    print("  --- Advanced Features ---")
    print("  5. Search Flights")
    print("  6. View Booking Details (JOIN View)")
    print("  7. Statistics Summary")
    print("  8. Passenger Booking Report")
    print("  ---")
    print("  0. Exit")
    print("=" * 60)
    

def main():
    conn = connect()
    cursor = conn.cursor()
    try:
        initialize_database(cursor)
        conn.commit()
        cursor.execute("SELECT DATABASE();")
        print("Current DB:", cursor.fetchone())
        cursor.close()
        cursor = conn.cursor()
        while True:
            print_main_menu()
            choice = input("Enter your choice: ").strip()
            if choice == '0':
                print("Exiting. Goodbye!")
                break
            elif choice in ('1', '2', '3', '4'):
                table_name = pick_table(cursor)
                if not table_name:
                    continue
                columns = get_table_columns(cursor, table_name)
                if choice == '1':
                    create_record(cursor, table_name, columns)
                elif choice == '2':
                    retrieve_records(cursor, table_name)
                elif choice == '3':
                    update_record(cursor, table_name)
                elif choice == '4':
                    delete_record(cursor, table_name)
                commit_choice = input("Commit changes? (yes/no): ").strip().lower()
                if commit_choice == 'yes':
                    conn.commit()
                else:
                    conn.rollback()
                    print("Changes rolled back.")
            elif choice == '5':
                search_flights(cursor)
            elif choice == '6':
                view_booking_details(cursor)
            elif choice == '7':
                show_stats(cursor)
            elif choice == '8':
                booking_summary_report(cursor)
            else:
                print("Invalid choice. Please enter a number from the menu.")
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
