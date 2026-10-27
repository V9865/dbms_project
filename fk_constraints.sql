ALTER TABLE Aircraft
ADD CONSTRAINT fk_aircraft_airline
FOREIGN KEY (airline_id) REFERENCES Airline(airline_id);

ALTER TABLE Route
ADD CONSTRAINT fk_route_src_airport
FOREIGN KEY (src_airport) REFERENCES Airport(iata_code);

ALTER TABLE Route
ADD CONSTRAINT fk_route_dst_airport
FOREIGN KEY (dst_airport) REFERENCES Airport(iata_code);

ALTER TABLE FlightSchedule
ADD CONSTRAINT fk_schedule_route
FOREIGN KEY (route_id) REFERENCES Route(route_id);

ALTER TABLE FlightSchedule
ADD CONSTRAINT fk_schedule_airline
FOREIGN KEY (airline_id) REFERENCES Airline(airline_id);

ALTER TABLE FlightSchedule
ADD CONSTRAINT fk_schedule_aircraft
FOREIGN KEY (tail_number) REFERENCES Aircraft(tail_number);

ALTER TABLE FlyingStatus
ADD FOREIGN KEY (schedule_id)
REFERENCES FlightSchedule(schedule_id)
ON DELETE CASCADE;

ALTER TABLE Booking
ADD FOREIGN KEY (passenger_id)
REFERENCES Passenger(passenger_id);

ALTER TABLE Booking
ADD FOREIGN KEY (schedule_id)
REFERENCES FlightSchedule(schedule_id)
ON DELETE CASCADE;

ALTER TABLE SeatAssignment
ADD FOREIGN KEY (booking_id)
REFERENCES Booking(booking_id)
ON DELETE CASCADE;

ALTER TABLE Pilot
ADD FOREIGN KEY (crew_id)
REFERENCES CrewMember(crew_id)
ON DELETE CASCADE;

ALTER TABLE CabinCrew
ADD FOREIGN KEY (crew_id)
REFERENCES CrewMember(crew_id)
ON DELETE CASCADE;

ALTER TABLE CrewAssignment
ADD FOREIGN KEY (crew_id)
REFERENCES CrewMember(crew_id)
ON DELETE CASCADE;

ALTER TABLE CrewAssignment
ADD FOREIGN KEY (schedule_id)
REFERENCES FlightSchedule(schedule_id)
ON DELETE CASCADE;