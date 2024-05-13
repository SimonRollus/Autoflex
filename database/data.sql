DROP TABLE IF EXISTS RentalContract;
DROP TABLE IF EXISTS Car;
DROP TABLE IF EXISTS Brand;
DROP TABLE IF EXISTS PrivateIndividual;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Company;
DROP TABLE IF EXISTS `User`;

CREATE TABLE `User` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(32) NOT NULL,
    lastName VARCHAR(32) NOT NULL,
    email VARCHAR(32) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    phoneNumber VARCHAR(10)
);

CREATE TABLE PrivateIndividual (
    id INT PRIMARY KEY,
    `address` VARCHAR(128) NOT NULL,
    driverLicense VARCHAR(15) NOT NULL,
    CONSTRAINT fk_private_individual_is_a_user FOREIGN KEY (id) REFERENCES `User`(id) ON DELETE CASCADE
);

CREATE TABLE Company (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(32) NOT NULL,
    sector VARCHAR(32) NOT NULL,
    `address` VARCHAR(128) NOT NULL
);

CREATE TABLE Employee (
    id INT PRIMARY KEY,
    companyId INT NOT NULL,
    department VARCHAR(32) NOT NULL,
    CONSTRAINT fk_employee_is_a_user FOREIGN KEY (id) REFERENCES `User`(id) ON DELETE CASCADE,
    CONSTRAINT fk_employee_works_for_a_company FOREIGN KEY (companyId) REFERENCES Company(id)
);

CREATE TABLE Brand (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Car (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brandId INT NOT NULL,
    model VARCHAR(32) NOT NULL,
    year INT NOT NULL CHECK (year > 1900 AND year < 2024),
    color VARCHAR(32) NOT NULL,
    pricePerKm DECIMAL(10, 2) NOT NULL CHECK (pricePerKm > 0),
    maxKilometers INT NOT NULL DEFAULT 100000 CHECK (maxKilometers > 10000),
    CONSTRAINT fk_car_belongs_to_a_brand FOREIGN KEY (brandId) REFERENCES Brand(id)
);

CREATE TABLE RentalContract (
    id INT AUTO_INCREMENT PRIMARY KEY,
    carId INT NOT NULL,
    userId INT NOT NULL,
    startDate DATE NOT NULL,
    endDate DATE NOT NULL,
    totalKm INT NOT NULL DEFAULT 0 CHECK (totalKm >= 0),
    CONSTRAINT fk_rental_contract_is_for_a_car FOREIGN KEY (carId) REFERENCES Car(id),
    CONSTRAINT fk_rental_contract_is_for_a_user FOREIGN KEY (userId) REFERENCES `User`(id),
    CONSTRAINT chk_rental_contract_dates CHECK (startDate < endDate)
);

INSERT INTO `User` (firstName, lastName, email, `password`, phoneNumber) VALUES ('Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown');

INSERT INTO Company (`name`, sector, `address`) VALUES ('Company 1', 'Sector 1', '`address`e 1');
INSERT INTO Company (`name`, sector, `address`) VALUES ('Company 2', 'Sector 2', '`address`e 2');
INSERT INTO Company (`name`, sector, `address`) VALUES ('Company 3', 'Sector 3', '`address`e 3');

INSERT INTO `User` (firstName, lastName, email, `password`, phoneNumber) VALUES ('John', 'Doe', 'email1@gmail.com', '$2b$12$PXEbl65kQaeeMQlCBBs0X.hsRMpujm2/Sv5iXtab7i/QmpleP.uAa', '1234567890');
INSERT INTO `User` (firstName, lastName, email, `password`, phoneNumber) VALUES ('Jane', 'Doe', 'email2@gmail.com', '$2b$12$PXEbl65kQaeeMQlCBBs0X.hsRMpujm2/Sv5iXtab7i/QmpleP.uAa', '1234567890');
INSERT INTO `User` (firstName, lastName, email, `password`, phoneNumber) VALUES ('Alice', 'Doe', 'email3@gmail.com', '$2b$12$PXEbl65kQaeeMQlCBBs0X.hsRMpujm2/Sv5iXtab7i/QmpleP.uAa', '1234567890');

INSERT INTO Employee (id, companyId, department) VALUES (2, 1, 'Department 1');
INSERT INTO Employee (id, companyId, department) VALUES (3, 2, 'Department 2');
INSERT INTO Employee (id, companyId, department) VALUES (4, 3, 'Department 3');

INSERT INTO Brand (name) VALUES ('Toyota');
INSERT INTO Brand (name) VALUES ('Honda');
INSERT INTO Brand (name) VALUES ('Nissan');
INSERT INTO Brand (name) VALUES ('Mazda');
INSERT INTO Brand (name) VALUES ('Subaru');
INSERT INTO Brand (name) VALUES ('Suzuki');
INSERT INTO Brand (name) VALUES ('Mitsubishi');
INSERT INTO Brand (name) VALUES ('Daihatsu');
INSERT INTO Brand (name) VALUES ('Isuzu');

INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (1, 'Corolla', 2019, 'White', 0.5);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (2, 'Civic', 2018, 'Black', 0.6);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (3, 'Skyline', 2017, 'Blue', 0.7);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (4, 'RX-7', 2016, 'Red', 0.8);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (5, 'Impreza', 2015, 'Green', 0.9);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (6, 'Swift', 2014, 'Yellow', 1.0);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (7, 'Lancer', 2013, 'Orange', 1.1);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (8, 'Mira', 2012, 'Purple', 1.2);
INSERT INTO Car (brandId, model, year, color, pricePerKm) VALUES (9, 'Panther', 2011, 'Brown', 1.3);

INSERT INTO RentalContract (carId, userId, startDate, endDate, totalKm) VALUES (1, 2, '2020-01-01', '2020-01-02', 100);
INSERT INTO RentalContract (carId, userId, startDate, endDate, totalKm) VALUES (2, 3, '2020-01-01', '2020-01-02', 200);
INSERT INTO RentalContract (carId, userId, startDate, endDate, totalKm) VALUES (3, 4, '2020-01-01', '2020-01-02', 300);


CREATE TRIGGER before_delete_user_who_has_rental_contract BEFORE DELETE ON `User`
FOR EACH ROW
UPDATE RentalContract SET userId = 1 WHERE userId = OLD.id;

/* Empêche l'ajout de contrats de location pour des voitures qui ont déjà atteint leur kilométrage maximum */

DELIMITER $$


CREATE TRIGGER delete_all_employee_from_company AFTER DELETE ON Company
FOR EACH ROW
BEGIN
    DELETE FROM Employee WHERE companyId = OLD.id;
    UPDATE RentalContract SET userId = 1 WHERE userId IN (SELECT id FROM Employee WHERE companyId = OLD.id);
END $$

CREATE TRIGGER cannot_delete_the_unknown_user BEFORE DELETE ON `User`
FOR EACH ROW
BEGIN
    IF OLD.id = 1 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete the unknown user';
    END IF;
END $$

CREATE TRIGGER before_insert_rental_contract_for_car_with_max_kilometers
BEFORE INSERT ON RentalContract
FOR EACH ROW
BEGIN
    IF (EXISTS (
        SELECT * FROM Car c
        WHERE c.id = NEW.carId AND 
        (SELECT COALESCE(SUM(totalKm), 0) FROM RentalContract WHERE carId = NEW.carId) >= c.maxKilometers
    )) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Car has reached max kilometers';
    END IF;
END $$

CREATE TRIGGER before_insert_rental_contract_for_rented_car BEFORE INSERT ON RentalContract
FOR EACH ROW
BEGIN
     IF EXISTS (
        SELECT 1 FROM RentalContract
        WHERE carId = NEW.carId
        AND NEW.startDate BETWEEN startDate AND endDate
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Car is already rented';
    END IF;
END $$

DELIMITER ;

/* Nous permet de voir les statistiques des voiture louées */
CREATE VIEW carStats AS
SELECT
    c.id,
    b.name AS brand,
    c.model,
    c.year,
    c.color,
    c.pricePerKm,
    COALESCE (
        (SELECT endDate 
        FROM RentalContract rc 
        WHERE rc.carId = c.id 
        AND CURDATE() BETWEEN rc.startDate AND rc.endDate),
        'Available now'
    ) AS nextAvailableDate,
    (
        SELECT COUNT(rc.id) 
        FROM RentalContract rc 
        WHERE rc.carId = c.id
    ) AS totalRentals,
    COALESCE(
        (
            SELECT SUM(rc.totalKm) 
            FROM RentalContract rc 
            WHERE rc.carId = c.id
        ), 
        0
    ) AS totalKm,
    COALESCE(
        (
            SELECT SUM(rc.totalKm * c.pricePerKm) 
            FROM RentalContract rc 
            WHERE rc.carId = c.id
        ), 
        0
    ) AS Revenue,
    COALESCE(
        (SELECT 1 FROM Car c2 WHERE c2.id = 1 AND (SELECT SUM(totalKm) FROM RentalContract rc WHERE rc.carId = c.id) >= c2.maxKilometers),
        0
    ) as hasReachedMaxKilometers
FROM
    Car c
LEFT JOIN Brand b ON c.brandId = b.id;


/* Nous permet de voir les statistiques des marques de voiture louées */
CREATE VIEW brandStats AS
SELECT
    b.id,
    b.name,
    COALESCE((SELECT COUNT(c.id) FROM Car c WHERE c.brandId = b.id), 0) AS totalCars,
    COALESCE((SELECT COUNT(rc.id) FROM RentalContract rc INNER JOIN Car c ON rc.carId = c.id WHERE c.brandId = b.id), 0) AS totalRentals,
    COALESCE((SELECT SUM(rc.totalKm) FROM RentalContract rc INNER JOIN Car c ON rc.carId = c.id WHERE c.brandId = b.id), 0) AS totalKm,
    COALESCE((SELECT SUM(rc.totalKm * c.pricePerKm) FROM RentalContract rc INNER JOIN Car c ON rc.carId = c.id WHERE c.brandId = b.id), 0) AS Revenue,
    (SELECT CONCAT(c.model, ' #', c.id) 
     FROM Car c 
     INNER JOIN RentalContract rc ON rc.carId = c.id
     WHERE c.brandId = b.id
     GROUP BY c.model, c.id
     ORDER BY COUNT(rc.id) DESC LIMIT 1) AS mostRentedCar
FROM
    Brand b;



/* Nous permet de voir les statistiques des locations des utilisateurs */
CREATE VIEW rentalStats AS
SELECT
    YEAR(rc.startDate) AS year,
    MONTH(rc.startDate) AS month,
    COUNT(rc.id) AS totalRentals,
    SUM(rc.totalKm) AS totalKm,
    SUM(rc.totalKm * c.pricePerKm) AS Revenue
FROM
    RentalContract rc
INNER JOIN Car c ON c.id = rc.carId
GROUP BY
    YEAR(rc.startDate),
    MONTH(rc.startDate) 
WITH ROLLUP;


/* Nous permet de voir les statistiques des entreprises */
CREATE VIEW companyStats AS
SELECT
    c.id,
    c.name,
    COALESCE((SELECT COUNT(e.id) FROM Employee e WHERE e.companyId = c.id), 0) AS totalEmployees,
    COALESCE((SELECT COUNT(rc.id) FROM RentalContract rc INNER JOIN Employee e ON rc.userId = e.id WHERE e.companyId = c.id), 0) AS totalRentals,
    COALESCE((SELECT SUM(rc.totalKm) FROM RentalContract rc INNER JOIN Employee e ON rc.userId = e.id WHERE e.companyId = c.id), 0) AS totalKm,
    COALESCE((SELECT SUM(rc.totalKm * car.pricePerKm) FROM RentalContract rc INNER JOIN Employee e ON rc.userId = e.id INNER JOIN Car car ON rc.carId = car.id WHERE e.companyId = c.id), 0) AS Revenue
FROM
    Company c;


