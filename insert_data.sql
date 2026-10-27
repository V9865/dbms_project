-- ============================================
-- AIRLINE MANAGEMENT SYSTEM - SAMPLE DATA
-- Run this AFTER create_schema.sql and fk_constraints.sql
-- ============================================

USE airlinedb;

-- 1. AIRLINE
INSERT INTO Airline VALUES
(1, 'UAE', 'Emirates', 'UAE', 1985),
(2, 'SIA', 'Singapore Airlines', 'Singapore', 1947),
(3, 'BAW', 'British Airways', 'United Kingdom', 1974),
(4, 'DAL', 'Delta Air Lines', 'USA', 1925),
(5, 'IGO', 'IndiGo', 'India', 2006);

-- 2. AIRPORT
INSERT INTO Airport VALUES
('DXB', 'Dubai International Airport', 'Dubai', 'UAE'),
('SIN', 'Changi Airport', 'Singapore', 'Singapore'),
('LHR', 'Heathrow Airport', 'London', 'United Kingdom'),
('JFK', 'John F. Kennedy International Airport', 'New York', 'USA'),
('BLR', 'Kempegowda International Airport', 'Bengaluru', 'India'),
('DEL', 'Indira Gandhi International Airport', 'Delhi', 'India'),
('BOM', 'Chhatrapati Shivaji Maharaj International Airport', 'Mumbai', 'India');

-- 3. AIRCRAFT (depends on Airline)
INSERT INTO Aircraft VALUES
('A6-ENA', 'Boeing 777-300ER', 'Boeing', 354, 1),
('A6-ENB', 'Airbus A380-800', 'Airbus', 517, 1),
('9V-SKA', 'Boeing 787-10', 'Boeing', 337, 2),
('G-XLEA', 'Airbus A380-800', 'Airbus', 469, 3),
('N717DL', 'Boeing 767-300', 'Boeing', 218, 4),
('VT-INA', 'Airbus A320neo', 'Airbus', 186, 5),
('VT-INB', 'Airbus A321neo', 'Airbus', 222, 5);

-- 4. ROUTE (depends on Airport)
INSERT INTO Route VALUES
(1, 'DXB', 'LHR', 5480, 7),
(2, 'SIN', 'JFK', 15349, 18),
(3, 'LHR', 'JFK', 5540, 7),
(4, 'BLR', 'DEL', 1740, 3),
(5, 'DEL', 'BOM', 1148, 2),
(6, 'BLR', 'BOM', 840, 2),
(7, 'DXB', 'BLR', 2844, 4);

-- 5. CREW MEMBER
INSERT INTO CrewMember VALUES
(1, 'Capt. Arjun Sharma', 'EMP001', 'Pilot'),
(2, 'Capt. Priya Nair', 'EMP002', 'Pilot'),
(3, 'Capt. James Cole', 'EMP003', 'Pilot'),
(4, 'Rahul Verma', 'EMP004', 'CabinCrew'),
(5, 'Sneha Iyer', 'EMP005', 'CabinCrew'),
(6, 'David Brown', 'EMP006', 'CabinCrew'),
(7, 'Meera Patel', 'EMP007', 'CabinCrew');

-- 6. PILOT (depends on CrewMember)
INSERT INTO Pilot VALUES
(1, 'LIC-IN-4421', 'ATPL'),
(2, 'LIC-IN-5530', 'ATPL'),
(3, 'LIC-UK-2218', 'CPL');

-- 7. CABIN CREW (depends on CrewMember)
INSERT INTO CabinCrew VALUES
(4, 'Lead Attendant', 'Business'),
(5, 'Attendant', 'Economy'),
(6, 'Attendant', 'Economy'),
(7, 'Lead Attendant', 'First');

-- 8. FLIGHT SCHEDULE (depends on Route, Airline, Aircraft)
INSERT INTO FlightSchedule VALUES
(1, 'EK101', '08:00:00', '15:00:00', 'Mon,Wed,Fri', 1, 1, 'A6-ENA'),
(2, 'SQ021', '23:55:00', '17:45:00', 'Daily', 2, 2, '9V-SKA'),
(3, 'BA117', '10:30:00', '17:30:00', 'Mon,Thu,Sat', 3, 3, 'G-XLEA'),
(4, '6E201', '06:00:00', '09:00:00', 'Daily', 4, 5, 'VT-INA'),
(5, '6E305', '13:00:00', '15:00:00', 'Daily', 5, 5, 'VT-INB'),
(6, 'EK568', '14:00:00', '18:00:00', 'Tue,Thu,Sun', 7, 1, 'A6-ENB');

-- 9. FLYING STATUS (depends on FlightSchedule)
INSERT INTO FlyingStatus VALUES
(1, '2025-05-01', 'OnTime', 0, 1),
(2, '2025-05-01', 'Delayed', 45, 2),
(3, '2025-05-01', 'Landed', 0, 3),
(4, '2025-05-02', 'OnTime', 0, 4),
(5, '2025-05-02', 'Cancelled', 0, 5),
(6, '2025-05-03', 'Delayed', 120, 6);

-- 10. PASSENGER
INSERT INTO Passenger VALUES
(1, 'P1234567', 'Aarav Mehta', '1990-06-15', 'Indian', 'aarav.mehta@email.com'),
(2, 'P2345678', 'Sara Johnson', '1985-11-22', 'American', 'sara.j@email.com'),
(3, 'P3456789', 'Liang Wei', '1998-03-08', 'Chinese', 'liang.wei@email.com'),
(4, 'P4567890', 'Fatima Al-Hassan', '1993-07-30', 'Emirati', 'fatima.h@email.com'),
(5, 'P5678901', 'Riya Kapoor', '2000-01-12', 'Indian', 'riya.k@email.com'),
(6, 'P6789012', 'Tom Clarke', '1978-09-03', 'British', 'tom.c@email.com');

-- 11. BOOKING (depends on Passenger, FlightSchedule)
INSERT INTO Booking VALUES
(1, 'BK-001', '2025-04-10', 'Economy', 450.00, 1, 1),
(2, 'BK-002', '2025-04-11', 'Business', 2200.00, 2, 2),
(3, 'BK-003', '2025-04-12', 'First', 5500.00, 3, 3),
(4, 'BK-004', '2025-04-15', 'Economy', 85.00, 4, 4),
(5, 'BK-005', '2025-04-16', 'Economy', 75.00, 5, 5),
(6, 'BK-006', '2025-04-20', 'Business', 1800.00, 6, 6);

-- 12. SEAT ASSIGNMENT (depends on Booking)
INSERT INTO SeatAssignment VALUES
(1, '24B', '2025-04-10 10:30:00', 1),
(2, '8A', '2025-04-11 09:15:00', 2),
(3, '2K', '2025-04-12 11:00:00', 3),
(4, '15C', '2025-04-15 07:45:00', 4),
(5, '18F', '2025-04-16 08:20:00', 5),
(6, '6D', '2025-04-20 14:00:00', 6);

-- 13. CREW ASSIGNMENT (depends on CrewMember, FlightSchedule)
INSERT INTO CrewAssignment VALUES
(1, 1, 1, 'Captain'),
(2, 4, 1, 'Lead Attendant'),
(3, 5, 1, 'Attendant'),
(4, 2, 2, 'Captain'),
(5, 6, 2, 'Attendant'),
(6, 3, 3, 'Captain'),
(7, 7, 3, 'Lead Attendant'),
(8, 1, 6, 'Captain'),
(9, 4, 6, 'Lead Attendant');
