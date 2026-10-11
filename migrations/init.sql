-- create db
CREATE DATABASE IF NOT EXISTS urban_mobility_db;
USE urban_mobility_db;

-- Create PASSENGER table
CREATE TABLE PASSENGER (
    passenger_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Create DRIVER table
CREATE TABLE DRIVER (
    driver_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL
);

-- Create VEHICLE table
CREATE TABLE VEHICLE (
    vehicle_id VARCHAR(50) PRIMARY KEY,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    make_model VARCHAR(100) NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES DRIVER(driver_id) ON DELETE CASCADE
);

-- Create TRIP table (bridge entity)
CREATE TABLE TRIP (
    trip_id VARCHAR(50) PRIMARY KEY,
    trip_date DATETIME NOT NULL,
    distance_km DECIMAL(5,2) NOT NULL CHECK (distance_km > 0),
    fare DECIMAL(10,2) NOT NULL CHECK (fare >= 0),
    passenger_id VARCHAR(50) NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    vehicle_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (driver_id) REFERENCES DRIVER(driver_id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id) ON DELETE CASCADE
);

-- Create INSPECTION_LOG table (weak entity)
CREATE TABLE INSPECTION_LOG (
    log_id VARCHAR(50) PRIMARY KEY,
    inspection_date DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Pass', 'Fail', 'Pending')),
    vehicle_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id) ON DELETE CASCADE
);

-- Create SAFETY_ALERT table (weak entity)
CREATE TABLE SAFETY_ALERT (
    alert_id VARCHAR(50) PRIMARY KEY,
    alert_reason TEXT NOT NULL,
    alert_date DATETIME NOT NULL,
    trip_id VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (trip_id) REFERENCES TRIP(trip_id) ON DELETE CASCADE
);

-- Create PAYMENT_METHOD table (weak entity)
CREATE TABLE PAYMENT_METHOD (
    method_id VARCHAR(50) PRIMARY KEY,
    card_type VARCHAR(50) NOT NULL,
    last_four VARCHAR(4) NOT NULL,
    passenger_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id) ON DELETE CASCADE
);

-- Create LANGUAGE table (weak entity)
CREATE TABLE LANGUAGE (
    language_id VARCHAR(50) PRIMARY KEY,
    language_name VARCHAR(50) NOT NULL,
    driver_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES DRIVER(driver_id) ON DELETE CASCADE
);