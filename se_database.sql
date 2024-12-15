-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 15, 2024 at 03:53 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `se_database`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `lotName` varchar(50) NOT NULL,
  `bookingDate` date NOT NULL,
  `timeStarted` time NOT NULL,
  `timeEnded` time NOT NULL,
  `ClientID` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`lotName`, `bookingDate`, `timeStarted`, `timeEnded`, `ClientID`) VALUES
('Lot IP003', '2024-12-17', '13:00:00', '16:30:00', '231004168');

-- --------------------------------------------------------

--
-- Table structure for table `parking_lots`
--

CREATE TABLE `parking_lots` (
  `name` varchar(50) NOT NULL,
  `latitude1` decimal(20,15) NOT NULL,
  `longitude1` decimal(20,15) NOT NULL,
  `latitude2` decimal(20,15) NOT NULL,
  `longitude2` decimal(20,15) NOT NULL,
  `status` enum('available','reserved','occupied','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parking_lots`
--

INSERT INTO `parking_lots` (`name`, `latitude1`, `longitude1`, `latitude2`, `longitude2`, `status`) VALUES
('Lot IP001', 13.405581896431616, 123.376980411010430, 13.405542932132011, 123.377003632488180, 'occupied'),
('Lot IP002', 13.405578721330884, 123.377037160100240, 13.405538584414021, 123.377063369921250, 'available'),
('Lot IP003', 13.405574546229933, 123.377093486488480, 13.405531886491611, 123.377120979130370, 'reserved'),
('Lot IP004', 13.405552334217062, 123.377228187395890, 13.405510065346709, 123.377252327276540, 'available'),
('Lot IP005', 13.405535288577386, 123.377277137709480, 13.405493019707033, 123.377301277590130, 'occupied'),
('Lot IP006', 13.405526242936998, 123.377326723605140, 13.405484974066645, 123.377350863485790, 'available');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` varchar(255) NOT NULL,
  `FIrstName` varchar(255) NOT NULL,
  `MiddleName` varchar(255) NOT NULL,
  `LastName` varchar(255) NOT NULL,
  `Role` enum('admin','employee','student') NOT NULL,
  `CspcEmail` varchar(255) NOT NULL,
  `PhoneNumber` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `FIrstName`, `MiddleName`, `LastName`, `Role`, `CspcEmail`, `PhoneNumber`, `Password`) VALUES
('221008049', 'Jayp', 'Surara', 'Bazar', 'admin', 'jabazar@my.cspc.edu.ph', '09454523496', 'ddb293b5b47020df66a30f184d03d312b0a485d9e6e2b2315c09d567e3c34a02'),
('231004168', 'Alfredo', 'Obrero', 'Sasota', 'student', 'alsasota@my.cspc.edu.ph', '09923051944', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`lotName`),
  ADD KEY `fk_studentID` (`ClientID`);

--
-- Indexes for table `parking_lots`
--
ALTER TABLE `parking_lots`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `fk_studentID` FOREIGN KEY (`ClientID`) REFERENCES `users` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
