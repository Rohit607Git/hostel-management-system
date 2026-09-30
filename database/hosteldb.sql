-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: hostel
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `Course_id` int NOT NULL,
  `course_name` varchar(20) NOT NULL,
  `duration` varchar(20) NOT NULL,
  PRIMARY KEY (`Course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'bca','3'),(2,'mca','2'),(3,'btech','4'),(4,'mtech','2'),(5,'bba','2'),(6,'mba','2');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `payment_date` date DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (2,3,50000.00,'2006-09-20','2006-09-30'),(3,1,100000.00,'2025-05-30',NULL),(6,5,500.00,'2025-05-21','2025-03-05'),(7,5,1000.00,'2025-05-24',NULL);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int NOT NULL,
  `role_name` varchar(255) NOT NULL,
  `permissions` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (0,'no role',NULL),(1,'lead administrator','0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15'),(2,'adminstrator','0'),(3,'moderator',NULL);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `room`
--

DROP TABLE IF EXISTS `room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `room` (
  `Room_id` int NOT NULL,
  `room_no` int NOT NULL,
  `block` varchar(10) NOT NULL,
  `available` char(1) NOT NULL,
  `beds` int NOT NULL,
  `ac` char(1) NOT NULL,
  `wifi` char(1) NOT NULL,
  `tv` char(1) NOT NULL,
  PRIMARY KEY (`Room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `room`
--

LOCK TABLES `room` WRITE;
/*!40000 ALTER TABLE `room` DISABLE KEYS */;
INSERT INTO `room` VALUES (101,1,'A','Y',4,'Y','Y','Y'),(102,2,'A','Y',3,'Y','Y','Y'),(103,3,'A','Y',4,'Y','Y','Y'),(104,4,'A','Y',2,'N','Y','Y'),(201,1,'B','Y',4,'N','Y','Y'),(202,2,'B','Y',4,'N','Y','N');
/*!40000 ALTER TABLE `room` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `Student_id` int NOT NULL,
  `Registration_No` int DEFAULT NULL,
  `Name` varchar(20) NOT NULL,
  `Gender` char(1) NOT NULL,
  `Father_Name` varchar(20) NOT NULL,
  `Mother_Name` varchar(20) NOT NULL,
  `DOB` date NOT NULL,
  `Address` varchar(50) NOT NULL,
  `Phone_no` char(10) DEFAULT NULL,
  `Room_id` int DEFAULT NULL,
  `Course_id` int DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Verify` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`Student_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,2025001,'ryan singh','M','d singh','meena singh','2000-02-29','k123 new delhi','9876543210',101,1,'abcd',1),(2,2025002,'Ajay saho','M','Raj saho','preeti saho','2004-02-29','T92 mumbai','9872346120',102,2,'demo',1),(3,2025003,'tommy bradshaw','M','michael bradshaw','tina bradshaw','2000-06-05','J62 LUCKNOW','9845316270',103,3,'test',1),(4,2025004,'mireya allen','M','peter allen','gwen allen','2000-08-20','J62 chennai','9846396270',201,5,'test',1),(5,2025005,'sadasdasdsa','F','asdasdasdasd','asdsadasd','9988-05-20','asdasdasasdsa','1234567890',103,3,'abc',1),(6,2025006,'asd','M','asd','ads','2008-09-20','ads','1234567890',NULL,NULL,'123456',1),(7,2025008,'hello','M','asd','asd','2005-06-05','asd','0123456789',NULL,NULL,'1324',0);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `name` varchar(255) DEFAULT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `role_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('admin2','123456',3),('admin3','7981',0),('admin','1234',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-21  2:06:07
