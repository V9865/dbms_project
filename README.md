# Airline Database Management System

A relational database for airline operations in **MySQL**, with a menu-driven **Python** command-line app for managing records, searching flights and generating reports.

Built for the Database Management Systems course at IIIT Bangalore.

![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)

---

## Schema

13 tables covering airlines, airports, aircraft, routes, flight schedules, passengers, bookings, seats and crew.

| Area | Tables |
| --- | --- |
| Fleet & network | `Airline`, `Airport`, `Aircraft`, `Route` |
| Operations | `FlightSchedule`, `FlyingStatus` |
| Customers | `Passenger`, `Booking`, `SeatAssignment` |
| Crew | `CrewMember`, `Pilot`, `CabinCrew`, `CrewAssignment` |

**Integrity rules**
- Primary keys on every table, and foreign keys linking schedules to routes, aircraft and airlines, bookings to passengers and schedules, and crew to flights
- `CHECK` constraints for positive fares, distances and seating capacity, valid flight statuses and ticket classes, and source airport ≠ destination
- `Pilot` and `CabinCrew` specialize `CrewMember` (one-to-one on the crew ID)
- Changes made in the app run inside a **transaction**: you choose to commit or roll back

## CLI features

- **CRUD** on any table: pick a table, then create, view, update or delete records
- **Flight search** by source airport, destination airport or flight number
- **Booking lookup** with passenger, flight and seat details joined together
- **Statistics:** bookings and revenue per airline, flights by status, busiest routes
- **Passenger summary report:** bookings, total spend and booking references per passenger

## Files

| File | Purpose |
| --- | --- |
| `connector.py` | Python CLI; creates the database and tables on first run |
| `create_schema.sql` | Table definitions |
| `fk_constraints.sql` | Foreign key constraints, added after tables exist |
| `insert_data.sql` | Sample data for every table |

---

## Getting started

**Requirements:** MySQL 8.0+, Python 3.9+

```bash
git clone https://github.com/V9865/dbms_project.git
cd dbms_project
pip install -r requirements.txt
```

1. Open `connector.py` and set your MySQL `user` and `password` in the `connect()` function.
2. Run the app once to create the `airlinedb` database, tables and foreign keys, then exit (`0`):
   ```bash
   python connector.py
   ```
3. Load the sample data:
   ```bash
   mysql -u root -p < insert_data.sql
   ```
4. Run the app again and use the menu:
   ```bash
   python connector.py
   ```

To set up the database without Python, run `create_schema.sql`, then `fk_constraints.sql`, then `insert_data.sql` inside a database named `airlinedb`.
