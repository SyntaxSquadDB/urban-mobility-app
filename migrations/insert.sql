INSERT INTO PASSENGER (passenger_id, first_name, last_name, email) VALUES
('P001', 'Alice', 'Smith', 'alice.smith@email.com'),
('P002', 'Bob', 'Jones', 'bob.jones@email.com');

INSERT INTO DRIVER (driver_id, first_name, last_name, license_number) VALUES
('D001', 'Charlie', 'Brown', 'LIC-998877'),
('D002', 'Diana', 'Prince', 'LIC-112233');

INSERT INTO VEHICLE (vehicle_id, license_plate, make_model, driver_id) VALUES
('V001', 'CA 123-456', 'Toyota Corolla', 'D001'),
('V002', 'CJ 987-654', 'Honda Civic', 'D002');

INSERT INTO TRIP (trip_id, trip_date, distance_km, fare, passenger_id, driver_id, vehicle_id) VALUES
('TR001', '2026-10-08 08:30:00', 12.5, 150.00, 'P001', 'D001', 'V001'),
('TR002', '2026-10-09 17:45:00', 8.2, 95.50, 'P002', 'D002', 'V002');

INSERT INTO INSPECTION_LOG (log_id, inspection_date, status, vehicle_id) VALUES
('IN001', '2026-09-01 10:00:00', 'Pass', 'V001'),
('IN002', '2026-09-15 11:30:00', 'Pass', 'V002');

INSERT INTO SAFETY_ALERT (alert_id, alert_reason, alert_date, trip_id) VALUES
('SA001', 'Driver exceeded speed limit in residential zone', '2026-10-08 09:00:00', 'TR001');

INSERT INTO PAYMENT_METHOD (method_id, card_type, last_four, passenger_id) VALUES
('PM001', 'Visa', '4321', 'P001'),
('PM002', 'Mastercard', '8765', 'P002');

INSERT INTO LANGUAGE (language_id, language_name, driver_id) VALUES
('L001', 'English', 'D001'),
('L002', 'IsiXhosa', 'D001'),
('L003', 'Afrikaans', 'D002');