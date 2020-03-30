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
-- Table structure for table `StandardTargetsForDropDownSelection`
--

DROP TABLE IF EXISTS `StandardTargetsForDropDownSelection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StandardTargetsForDropDownSelection` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `DisplayTargetName` varchar(50) DEFAULT NULL,
  `TargetGUID` varchar(50) DEFAULT NULL,
  `RestrictToThisBallType` varchar(45) DEFAULT NULL,
  `DisplayRiverYN` varchar(45) DEFAULT NULL,
  `JpgFileName` varchar(145) DEFAULT NULL,
  `CreateDtm` timestamp NULL DEFAULT NULL,
  `UpdateDtm` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1000 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StandardTargetsForDropDownSelection`
--

LOCK TABLES `StandardTargetsForDropDownSelection` WRITE;
/*!40000 ALTER TABLE `StandardTargetsForDropDownSelection` DISABLE KEYS */;
INSERT INTO `StandardTargetsForDropDownSelection` VALUES (1,'SMv1 - Early Development','SMV1-EARLYDEV','NONE','N','SMV1-EARLYDEV.jpg','2018-08-16 05:00:00',NULL),(2,'SMv1 - Early Dev. w/River','SMV1-ED-R','NONE','Y','SMV1-ED-R.jpg','2018-08-16 05:00:00',NULL),(3,'SMv1 - Intermediate','SMV1-INTERMED','NONE','N','SMV1-INTERMED.jpg','2018-08-16 05:00:00',NULL),(4,'SMv1 - Intermediate w/River','SMV1-IM-R','NONE','Y','SMV1-IM-R.jpg','2018-08-16 05:00:00',NULL),(5,'SMv1 - Select','SMV1-SELECT','NONE','N','SMV1-SELECT.jpg','2018-08-16 05:00:00',NULL),(6,'SMv1 - Select w/ River','SMV1-SL-R','NONE','Y','SMV1-SL-R.jpg','2018-08-16 05:00:00',NULL),(7,'SMv1 - Pitchers Advantage','SMV1-PITCHADV','NONE','N','SMV1-PITCHADV.jpg','2018-08-16 05:00:00',NULL),(8,'SMv1 - Pitcher Adv w/River','SMV1-PA-R','NONE','Y','SMV1-PA-R.jpg','2018-08-16 05:00:00',NULL),(999,'files located:  /var/www/html/img',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `StandardTargetsForDropDownSelection` ENABLE KEYS */;
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
