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
-- Table structure for table `BallSpeedSettingMethods`
--

DROP TABLE IF EXISTS `BallSpeedSettingMethods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BallSpeedSettingMethods` (
  `BS_Method_AutoNumberKey` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `BS_MethodCode` varchar(45) DEFAULT NULL,
  `BS_MethodName` varchar(45) DEFAULT NULL,
  `BS_MethodDescription` varchar(145) DEFAULT NULL,
  `BS_MethodAddedBy` varchar(45) DEFAULT NULL,
  `BS_MethodAddedDateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `BS_MethodLastUpdateBy` varchar(45) DEFAULT NULL,
  `BS_MethodLastUpdateDateTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`BS_Method_AutoNumberKey`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BallSpeedSettingMethods`
--

LOCK TABLES `BallSpeedSettingMethods` WRITE;
/*!40000 ALTER TABLE `BallSpeedSettingMethods` DISABLE KEYS */;
INSERT INTO `BallSpeedSettingMethods` VALUES (2,'PS-01','PlateSpeed Meth 01','Plate Speed Method 01: measured by DT100 behind LED panel near middle location\n','Tim Crosno- SM ADMIN USER','2019-08-12 09:05:31','Tim Crosno- SM ADMIN USER\n','2019-08-12 09:09:43'),(3,'RS-01','Release Speed Meth 01','Release Speed Method 01: CALCULATED from value manually entered in Pithers record and ADDED to Plate Speed','Tim Crosno- SM ADMIN USER','2019-08-12 09:14:06','Tim Crosno- SM ADMIN USER','2019-08-12 09:14:54');
/*!40000 ALTER TABLE `BallSpeedSettingMethods` ENABLE KEYS */;
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
