-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (i686)
--
-- Host: 127.0.0.1    Database: smartmitt
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

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
-- Table structure for table `SessionStatusCodes`
--

DROP TABLE IF EXISTS `SessionStatusCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SessionStatusCodes` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `CodeValue` varchar(45) DEFAULT NULL,
  `Description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SessionStatusCodes`
--

LOCK TABLES `SessionStatusCodes` WRITE;
/*!40000 ALTER TABLE `SessionStatusCodes` DISABLE KEYS */;
INSERT INTO `SessionStatusCodes` VALUES (1,'NEW','Freshly created by the PHP front-end with the next available sequence number.  Check to see if a NEW exists before creating a NEW.'),(2,'SUSPENDED','Suspended for any reason, paused by student, power failure, timed-out, etc.   If SUSPENDED session is found when student logs in, ask what to do - continue, close/update, discard (are you sure?)'),(3,'OPEN','Currently pitching this session and it\'s being ran/managed by the Python back-end software.  Same as suspended, if find a session OPEN for a student that logs in, ask what to to- continue, abort, close/upload.'),(4,'CANCELLED','We never delete session records to keep the sequence numbers in line.  this session was cancelled for what-ever reason and is not valid in any way.'),(5,'COMPLETED','This session was pitched and properly closed by the pitcher/coach and is pending upload to Easy Insight cloudl database.'),(6,'UPLOADED','This session is completely done, closed by pitcher to COMPLETED status, and the software has uploaded it to Easy Insight cloud DB.');
/*!40000 ALTER TABLE `SessionStatusCodes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-16 10:48:57
