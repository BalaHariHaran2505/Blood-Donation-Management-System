CREATE DATABASE IF NOT EXISTS BloodDonationDB;
USE BloodDonationDB;

CREATE TABLE IF NOT EXISTS Donors (
    DonorID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    BloodGroup VARCHAR(5),
    Contact VARCHAR(15),
    LastDonationDate DATE
);

CREATE TABLE IF NOT EXISTS Recipients (
    RecipientID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Age INT,
    BloodGroup VARCHAR(5),
    Contact VARCHAR(15),
    BloodRequired INT
);

CREATE TABLE IF NOT EXISTS BloodInventory (
    BloodGroup VARCHAR(5) PRIMARY KEY,
    UnitsAvailable INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Donations (
    DonationID INT AUTO_INCREMENT PRIMARY KEY,
    DonorID INT,
    BloodGroup VARCHAR(5),
    DonationDate DATE,
    FOREIGN KEY (DonorID) REFERENCES Donors(DonorID)
);


CREATE TABLE IF NOT EXISTS Requests (
    RequestID INT AUTO_INCREMENT PRIMARY KEY,
    RecipientID INT,
    BloodGroup VARCHAR(5),
    UnitsRequested INT,
    RequestDate DATE,
    Status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (RecipientID) REFERENCES Recipients(RecipientID)
);

DELIMITER //

CREATE TRIGGER after_donation_insert
AFTER INSERT ON Donations
FOR EACH ROW
BEGIN
    UPDATE BloodInventory
    SET UnitsAvailable = UnitsAvailable + 1
    WHERE BloodGroup = NEW.BloodGroup;

    IF ROW_COUNT() = 0 THEN
        INSERT INTO BloodInventory (BloodGroup, UnitsAvailable)
        VALUES (NEW.BloodGroup, 1);
    END IF;
END;
//

DELIMITER