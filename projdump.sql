-- MySQL dump 10.13  Distrib 5.7.31, for Linux (x86_64)
--
-- Host: localhost    Database: PROJECT
-- ------------------------------------------------------
-- Server version	5.7.31-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ADMINISTRATOR`
--

DROP TABLE IF EXISTS `ADMINISTRATOR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ADMINISTRATOR` (
  `admin_id` int(11) NOT NULL,
  `qualification` int(11) NOT NULL,
  PRIMARY KEY (`admin_id`),
  CONSTRAINT `ADMINISTRATOR_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `EMPLOYEE` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ADMINISTRATOR`
--

LOCK TABLES `ADMINISTRATOR` WRITE;
/*!40000 ALTER TABLE `ADMINISTRATOR` DISABLE KEYS */;
/*!40000 ALTER TABLE `ADMINISTRATOR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AGENT`
--

DROP TABLE IF EXISTS `AGENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AGENT` (
  `agent_id` int(11) NOT NULL,
  `bookings_made` int(11) NOT NULL,
  PRIMARY KEY (`agent_id`),
  CONSTRAINT `AGENT_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `EMPLOYEE` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AGENT`
--

LOCK TABLES `AGENT` WRITE;
/*!40000 ALTER TABLE `AGENT` DISABLE KEYS */;
INSERT INTO `AGENT` VALUES (1,1);
/*!40000 ALTER TABLE `AGENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `BOOKS`
--

DROP TABLE IF EXISTS `BOOKS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BOOKS` (
  `event_id` int(11) NOT NULL,
  `cust_id` int(11) NOT NULL,
  `agent_id` int(11) NOT NULL,
  `booking_id` int(11) NOT NULL,
  PRIMARY KEY (`event_id`),
  KEY `cust_id` (`cust_id`),
  KEY `agent_id` (`agent_id`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `BOOKS_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `EVENT` (`event_id`),
  CONSTRAINT `BOOKS_ibfk_2` FOREIGN KEY (`cust_id`) REFERENCES `CUSTOMER` (`cust_id`),
  CONSTRAINT `BOOKS_ibfk_3` FOREIGN KEY (`agent_id`) REFERENCES `AGENT` (`agent_id`),
  CONSTRAINT `BOOKS_ibfk_4` FOREIGN KEY (`booking_id`) REFERENCES `PAYMENT` (`booking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BOOKS`
--

LOCK TABLES `BOOKS` WRITE;
/*!40000 ALTER TABLE `BOOKS` DISABLE KEYS */;
INSERT INTO `BOOKS` VALUES (1,1,1,1);
/*!40000 ALTER TABLE `BOOKS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CONTACT`
--

DROP TABLE IF EXISTS `CONTACT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CONTACT` (
  `cust_id` int(11) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`cust_id`,`phone`),
  CONSTRAINT `CONTACT_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `CUSTOMER` (`cust_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CONTACT`
--

LOCK TABLES `CONTACT` WRITE;
/*!40000 ALTER TABLE `CONTACT` DISABLE KEYS */;
/*!40000 ALTER TABLE `CONTACT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CUSTOMER`
--

DROP TABLE IF EXISTS `CUSTOMER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CUSTOMER` (
  `cust_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(40) NOT NULL,
  `lname` varchar(40) DEFAULT NULL,
  `poi_type` varchar(20) NOT NULL,
  `poi_number` varchar(30) NOT NULL,
  PRIMARY KEY (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMER`
--

LOCK TABLES `CUSTOMER` WRITE;
/*!40000 ALTER TABLE `CUSTOMER` DISABLE KEYS */;
INSERT INTO `CUSTOMER` VALUES (1,'Rajesh','Agarwal','Adhaar','1098 1099 1100');
/*!40000 ALTER TABLE `CUSTOMER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLOYEE`
--

DROP TABLE IF EXISTS `EMPLOYEE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EMPLOYEE` (
  `emp_id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(40) NOT NULL,
  `lname` varchar(40) DEFAULT NULL,
  `doj` date NOT NULL,
  `salary` decimal(15,2) DEFAULT NULL,
  `city_of_work` varchar(40) DEFAULT NULL,
  `contact` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`emp_id`),
  KEY `city_of_work` (`city_of_work`),
  CONSTRAINT `EMPLOYEE_ibfk_1` FOREIGN KEY (`city_of_work`) REFERENCES `LOCATION` (`cityname`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLOYEE`
--

LOCK TABLES `EMPLOYEE` WRITE;
/*!40000 ALTER TABLE `EMPLOYEE` DISABLE KEYS */;
INSERT INTO `EMPLOYEE` VALUES (1,'A','B','2020-09-10',20000.00,'Kolkata', '+911234567890');
/*!40000 ALTER TABLE `EMPLOYEE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EVENT`
--

DROP TABLE IF EXISTS `EVENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EVENT` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime NOT NULL,
  `type` varchar(30) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `city` varchar(40) NOT NULL,
  `booking_id` int(11) NOT NULL,
  PRIMARY KEY (`event_id`),
  KEY `city` (`city`),
  KEY `booking_id` (`booking_id`),
  CONSTRAINT `EVENT_ibfk_1` FOREIGN KEY (`city`) REFERENCES `LOCATION` (`cityname`),
  CONSTRAINT `EVENT_ibfk_2` FOREIGN KEY (`booking_id`) REFERENCES `PAYMENT` (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EVENT`
--

LOCK TABLES `EVENT` WRITE;
/*!40000 ALTER TABLE `EVENT` DISABLE KEYS */;
INSERT INTO `EVENT` VALUES (1,'2020-09-10 12:00:00','2020-09-13 12:00:00','Wedding','A weds B','Kolkata',1);
/*!40000 ALTER TABLE `EVENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOCATION`
--

DROP TABLE IF EXISTS `LOCATION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LOCATION` (
  `cityname` varchar(40) NOT NULL,
  `locality` varchar(100) NOT NULL,
  `pincode` int(11) NOT NULL,
  PRIMARY KEY (`cityname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOCATION`
--

LOCK TABLES `LOCATION` WRITE;
/*!40000 ALTER TABLE `LOCATION` DISABLE KEYS */;
INSERT INTO `LOCATION` VALUES ('Kolkata','Ballygunge',700019);
/*!40000 ALTER TABLE `LOCATION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MANAGER`
--

DROP TABLE IF EXISTS `MANAGER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MANAGER` (
  `mgr_id` int(11) NOT NULL,
  `years_of_experience` int(11) NOT NULL,
  PRIMARY KEY (`mgr_id`),
  CONSTRAINT `MANAGER_ibfk_1` FOREIGN KEY (`mgr_id`) REFERENCES `EMPLOYEE` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MANAGER`
--

LOCK TABLES `MANAGER` WRITE;
/*!40000 ALTER TABLE `MANAGER` DISABLE KEYS */;
/*!40000 ALTER TABLE `MANAGER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PAYMENT`
--

DROP TABLE IF EXISTS `PAYMENT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PAYMENT` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `transdate` datetime NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `cust_id` int(11) NOT NULL,
  PRIMARY KEY (`booking_id`,`transdate`),
  KEY `cust_id` (`cust_id`),
  CONSTRAINT `PAYMENT_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `CUSTOMER` (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PAYMENT`
--

LOCK TABLES `PAYMENT` WRITE;
/*!40000 ALTER TABLE `PAYMENT` DISABLE KEYS */;
INSERT INTO `PAYMENT` VALUES (1,'2020-09-15 15:00:00',100000.00,1),(1,'2020-09-16 15:00:00',50000.00,1);
/*!40000 ALTER TABLE `PAYMENT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REPORTS_TO`
--

DROP TABLE IF EXISTS `REPORTS_TO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `REPORTS_TO` (
  `agent_id` int(11) NOT NULL,
  `mgr_id` int(11) NOT NULL,
  PRIMARY KEY (`agent_id`,`mgr_id`),
  KEY `mgr_id` (`mgr_id`),
  CONSTRAINT `REPORTS_TO_ibfk_1` FOREIGN KEY (`agent_id`) REFERENCES `AGENT` (`agent_id`),
  CONSTRAINT `REPORTS_TO_ibfk_2` FOREIGN KEY (`mgr_id`) REFERENCES `MANAGER` (`mgr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REPORTS_TO`
--

LOCK TABLES `REPORTS_TO` WRITE;
/*!40000 ALTER TABLE `REPORTS_TO` DISABLE KEYS */;
/*!40000 ALTER TABLE `REPORTS_TO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SPECIAL_GUEST`
--

DROP TABLE IF EXISTS `SPECIAL_GUEST`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SPECIAL_GUEST` (
  `event_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `occupation` varchar(40) DEFAULT NULL,
  `contact` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`event_id`,`name`),
  CONSTRAINT `SPECIAL_GUEST_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `EVENT` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SPECIAL_GUEST`
--

LOCK TABLES `SPECIAL_GUEST` WRITE;
/*!40000 ALTER TABLE `SPECIAL_GUEST` DISABLE KEYS */;
/*!40000 ALTER TABLE `SPECIAL_GUEST` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TECHNICIAN`
--

DROP TABLE IF EXISTS `TECHNICIAN`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TECHNICIAN` (
  `tech_id` int(11) NOT NULL,
  `tlevel` int(11) NOT NULL,
  PRIMARY KEY (`tech_id`),
  CONSTRAINT `TECHNICIAN_ibfk_1` FOREIGN KEY (`tech_id`) REFERENCES `EMPLOYEE` (`emp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TECHNICIAN`
--

LOCK TABLES `TECHNICIAN` WRITE;
/*!40000 ALTER TABLE `TECHNICIAN` DISABLE KEYS */;
/*!40000 ALTER TABLE `TECHNICIAN` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-04 19:48:18
