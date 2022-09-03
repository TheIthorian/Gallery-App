-- MySQL Script generated by MySQL Workbench
-- Mon Apr  5 15:20:50 2021
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


-- -----------------------------------------------------
-- Table Gallery.Users_T
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Gallery.Users_T (
  UserId INT NOT NULL AUTO_INCREMENT,
  Username VARCHAR(45) NOT NULL,
  Email VARCHAR(320),
  Password VARCHAR(45) NOT NULL,
  AdminInd INT NOT NULL CONSTRAINT Users_CC01 CHECK (AdminInd IN (5, 6)),
  Status INT NOT NULL CONSTRAINT Users_CC02 CHECK (Status IN (0, 1, 2)),
  TmStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (UserId))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table Gallery.Gallery_T
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Gallery.Gallery_T (
  GalleryId INT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(45) NOT NULL,
  Status INT NOT NULL CONSTRAINT Gallery_CC01 CHECK (Status IN (0, 1)),
  UserId INT NOT NULL REFERENCES Users_T (UserId),
  AddedDate DATETIME NOT NULL,
  TmStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (GalleryId))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table Gallery.Image_T
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Gallery.Image_T (
  ImageId INT NOT NULL AUTO_INCREMENT,
  Title VARCHAR(45) NOT NULL,
  URL VARCHAR(3200) NOT NULL,
  Path VARCHAR(3200) NOT NULL,
  Suffix VARCHAR(20) NOT NULL,
  OriginalWidth INT NOT NULL,
  OriginalHeight INT NOT NULL,
  Width INT NOT NULL,
  Height INT NOT NULL,
  Status INT NOT NULL CONSTRAINT Image_CC01 CHECK (Status IN (0, 1)),
  UserId INT REFERENCES Users_T (UserId),
  AddedByUserId INT NOT NULL REFERENCES Users_T (UserId),
  TmStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (ImageId))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table Gallery.GalleryImage_T
-- -----------------------------------------------------
/*
CREATE TABLE IF NOT EXISTS Gallery.GalleryImage_T (
  GalleryImageId INT NOT NULL AUTO_INCREMENT,
  GalleryId INT NOT NULL,
  ImageId INT NOT NULL,
  Title VARCHAR(45),
  UserId INT REFERENCES Users_T (UserId),
  TmStamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (GalleryImageId))
ENGINE = InnoDB;
*/
USE Gallery ;


-- -----------------------------------------------------
-- View Gallery.Users
-- -----------------------------------------------------
CREATE  OR REPLACE VIEW Users AS
SELECT
UserId,
Username,
Email,
Password,
AdminInd,
Status,
TmStamp
FROM Users_T;

-- -----------------------------------------------------
-- View Gallery.Gallery
-- -----------------------------------------------------
CREATE  OR REPLACE VIEW Gallery AS
SELECT 
GalleryId,
Title,
Status,
UserId,
AddedDate,
TmStamp
FROM Gallery_T;

-- -----------------------------------------------------
-- View Gallery.Image
-- -----------------------------------------------------
CREATE  OR REPLACE VIEW Image AS
SELECT
ImageId,
Title,
URL,
Path,
Suffix,
OriginalWidth,
OriginalHeight,
Width,
Height,
Status,
GalleryId,
UserId,
AddedByUserId,
TmStamp
FROM Image_T;

-- -----------------------------------------------------
-- View Gallery.GalleryImage
-- -----------------------------------------------------
/*
CREATE OR REPLACE VIEW GalleryImage AS
SELECT
  GalleryImageId,
  GalleryId,
  ImageId,
  Title,
  UserId,
  TmStamp
FROM GalleryImage_T;
*/


GRANT SELECT ON TABLE Gallery.* TO 'RO';
GRANT SELECT, INSERT, TRIGGER ON TABLE Gallery.* TO 'UA';
GRANT SELECT ON TABLE Gallery.* TO 'UA';
GRANT ALL ON Gallery.* TO 'Admin';
GRANT SELECT ON TABLE Gallery.* TO 'Admin';
GRANT SELECT, INSERT, TRIGGER ON TABLE Gallery.* TO 'Admin';
GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE Gallery.* TO 'Admin';
GRANT EXECUTE ON ROUTINE Gallery.* TO 'Admin';


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
