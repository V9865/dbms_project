CREATE TABLE Airline(
    airline_id INT PRIMARY KEY, 
    icao_code VARCHAR(10) UNIQUE,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100),
    founding_year INT);
     
CREATE TABLE Airport(
    iata_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100) NOT NULL);
    
CREATE TABLE Aircraft(
    tail_number VARCHAR(20) PRIMARY KEY,
    model VARCHAR(50),
    manufacturer VARCHAR(50),
    seating_cap INT NOT NULL CHECK (seating_cap>0),
    airline_id INT(20));
    
CREATE TABLE Route(
    route_id INT PRIMARY KEY,
    src_airport VARCHAR(20) NOT NULL,
    dst_airport VARCHAR(20) NOT NULL,
    dist_km INT CHECK (dist_km>0),
    dur_hrs INT CHECK(dur_hrs>0),
    CHECK (src_airport <> dst_airport));
    
CREATE TABLE FlightSchedule (
    schedule_id INT PRIMARY KEY,
    flight_number VARCHAR(20),
    departure_time TIME,
    arrival_time TIME,
    days_operated VARCHAR(50),
    route_id INT,
    airline_id INT,
    tail_number VARCHAR(20)
);

CREATE TABLE FlyingStatus (
    status_id INT PRIMARY KEY,
    op_date DATE,
    status VARCHAR(20),
    delay_minutes INT CHECK (delay_minutes >= 0),
    schedule_id INT,
    CHECK (status IN ('OnTime','Delayed','Cancelled','Landed'))
);

CREATE TABLE Passenger (
    passenger_id INT PRIMARY KEY,
    passport_no VARCHAR(20) UNIQUE,
    name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    nationality VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

CREATE TABLE Booking (
    booking_id INT PRIMARY KEY,
    booking_ref VARCHAR(20) UNIQUE,
    booking_date DATE,
    ticket_class VARCHAR(20),
    fare DECIMAL(10,2) CHECK (fare > 0),
    passenger_id INT,
    schedule_id INT,
    CHECK (ticket_class IN ('Economy','Business','First'))
);

CREATE TABLE SeatAssignment (
    assignment_id INT PRIMARY KEY,
    seat_number VARCHAR(10),
    assigned_at TIMESTAMP,
    booking_id INT UNIQUE
);

CREATE TABLE CrewMember (
    crew_id INT PRIMARY KEY,
    name VARCHAR(100),
    employee_id VARCHAR(20) UNIQUE,
    crew_type VARCHAR(20),
    CHECK (crew_type IN ('Pilot','CabinCrew'))
);

CREATE TABLE Pilot (
    crew_id INT PRIMARY KEY,
    license_no VARCHAR(50),
    rating VARCHAR(50)
);

CREATE TABLE CabinCrew (
    crew_id INT PRIMARY KEY,
    role VARCHAR(50),
    section VARCHAR(50)
);

CREATE TABLE CrewAssignment (
    assignment_id INT PRIMARY KEY,
    crew_id INT,
    schedule_id INT,
    role_on_flight VARCHAR(50)
);