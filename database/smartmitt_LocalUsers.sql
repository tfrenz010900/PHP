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
-- Table structure for table `LocalUsers`
--

DROP TABLE IF EXISTS `LocalUsers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `LocalUsers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `AccountID` varchar(50) DEFAULT '',
  `Active` varchar(10) DEFAULT NULL,
  `ThrowsRightOrLeft` varchar(5) DEFAULT 'R',
  `StudentFirst` varchar(125) DEFAULT '',
  `StudentLast` varchar(125) DEFAULT '',
  `StudentNickname` varchar(125) DEFAULT '',
  `StudentDOB` date DEFAULT NULL,
  `StudentGender` varchar(5) DEFAULT '',
  `StudentPasswordEncrypted` varchar(125) DEFAULT '',
  `StudentPasswordPlainText` varchar(125) DEFAULT '',
  `StudentEmail` varchar(125) DEFAULT '',
  `Sport` varchar(50) DEFAULT '',
  `CompLevel` varchar(50) DEFAULT '',
  `CreateDtm` timestamp NULL DEFAULT NULL,
  `PaidThroughDateDtm` timestamp NULL DEFAULT NULL,
  `LastSynchFromEasyInsightDtm` timestamp NULL DEFAULT NULL,
  `LastUpdateDtm` timestamp NULL DEFAULT NULL,
  `LastSpeedDisplayTimeSecs` int(11) DEFAULT '4',
  `LastImpactDisplayTimeSecs` int(11) DEFAULT '4',
  `LastYdeltaValueUsed` varchar(45) DEFAULT '0',
  `LastDisplayRiverYN` varchar(45) DEFAULT 'N',
  `LastSessionAutoTimeOutMinutes` int(11) DEFAULT NULL,
  `LastDisplayPitchCountBarsOnLedYN` varchar(45) DEFAULT 'N',
  `PitchingDistanceFeet` int(11) DEFAULT NULL,
  `VideoDataAcceptanceYN` varchar(5) DEFAULT NULL,
  `VideoAcceptanceDtm` timestamp NULL DEFAULT NULL,
  `CoachID1` varchar(45) DEFAULT NULL,
  `CoachID2` varchar(45) DEFAULT NULL,
  `CoachID3` varchar(45) DEFAULT NULL,
  `CoachID4` varchar(45) DEFAULT NULL,
  `CoachID5` varchar(45) DEFAULT NULL,
  `CoachID6` varchar(45) DEFAULT NULL,
  `CoachID7` varchar(45) DEFAULT NULL,
  `CoachID8` varchar(45) DEFAULT NULL,
  `ReleaseSpeedAddon` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LocalUsers`
--

LOCK TABLES `LocalUsers` WRITE;
/*!40000 ALTER TABLE `LocalUsers` DISABLE KEYS */;
INSERT INTO `LocalUsers` VALUES (7,'smartmitt','1','R','Admin','Admin','Admin','2018-11-09','M','','smartmitt','admin@smartmitt.com','Softball','Professional','2020-03-16 15:32:24',NULL,'2020-03-16 15:32:24','2020-03-16 15:32:24',6,4,'0','Y',NULL,'N',38,NULL,NULL,'C100055','','','','','','','','6'),(8,'A100096','1','R','Chris','Paddack','Impact','1996-12-05','M','','smartmitt','smartmitt.demo@gmail.com','Baseball','Professional','2019-10-28 00:25:06','2019-01-21 18:32:19','2019-10-28 00:25:06','2019-10-28 00:25:06',1,5,'0','Y',NULL,'Y',60,NULL,NULL,'C100035','C100120','C100064','C100060','','','','','3'),(9,'A100139','1','R','DEMO','DEMO','DEMO','2019-07-05','M','smartmitt','smartmitt','mikem@extrainnings-middleton.com','Baseball','College','2019-08-18 22:33:24','2019-08-18 22:33:24','2019-08-18 22:33:24','2019-08-18 22:33:24',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'C100070','','','','','','','','3'),(10,'A100048','1','R','Alex','Flores','Alex','1998-08-14','F','','smartmitt','msu-aflores2@mcneese.edu','Softball','College','2019-08-20 12:41:40','2019-08-20 12:41:40','2019-08-20 12:41:44','2019-08-20 12:41:44',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'C100095','C100044','','','','','','','5'),(11,'A100049','1','R','Caroline','Settle','Caroline','1997-10-03','F','','smartmitt','msu-csettle@mcneese.edu','Softball','College','2019-08-20 13:09:11','2019-08-20 12:42:49','2019-08-20 16:14:31','2019-08-20 16:14:31',2,2,'0','Y',NULL,'Y',43,NULL,NULL,'C100095','C100044','','','','','','','5'),(12,'A100221','1','L','McNeese','Demo','McNeese','2019-08-20','F','smartmitt','smartmitt','mcneese.demo@gmail.com','Softball','College','2019-08-20 16:05:00','2019-08-20 16:02:48','2019-08-20 16:05:00','2019-08-20 16:05:00',4,4,'0','Y',NULL,'Y',43,NULL,NULL,'C100095','','','','','','','','4'),(13,'A100228','1','R','Lucas','Giolito','Lucas','1994-07-14','M','','smartmitt','chisox.demo@gmail.com','Baseball','Professional','2019-08-28 21:52:51','2019-08-28 19:55:00','2019-08-28 21:52:51','2019-08-28 21:52:51',1,1,'0','Y',NULL,'Y',60,NULL,NULL,'C100035','','','','','','','','6'),(14,'A100230','1','R','Sandlot','Demo','Sandlot','2019-08-28','M','','smartmitt','sandlot@gmail.com','Baseball','Travel','2019-10-18 22:54:24','2019-08-28 21:00:13','2019-10-18 22:54:24','2019-10-18 22:54:24',1,4,'0','Y',NULL,'Y',60,NULL,NULL,'C100093','','','','','','','','4'),(15,'A100213','1','L','Bull','Pen','BULLP-BB','2019-07-12','M','smartmitt','smartmitt','bullpen.bb@gmail.com','Baseball','18U','2019-09-13 21:07:55','2019-09-13 21:00:51','2019-09-13 21:07:55','2019-09-13 21:07:55',1,1,'0','Y',NULL,'Y',43,NULL,NULL,'C100100','','','','','','','','2'),(16,'A100247','1','R','Demo','Yard','The Yard','2019-10-08','M','smartmitt','smartmitt','theyard@gmail.com','Baseball','17U','2019-10-08 20:24:58','2019-10-08 20:24:37','2019-10-08 20:24:58','2019-10-08 20:24:58',1,1,'0','Y',NULL,'Y',60,NULL,NULL,'','','','','','','','','4'),(17,'A100035','1','R','Alex','Frenz','Al','2018-12-05','F','','smartmitt','thomasfrenz@gmail.com','Softball','College','2019-10-08 21:21:33','2019-10-08 21:21:33','2019-10-08 21:21:36','2019-10-08 21:21:36',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'','','','','','','','','3'),(18,'A100075','0','R','Parker','Conrad','Parker','2019-03-17','F','smartmitt','smartmitt','pac73@ou.edu','Softball','College','2019-10-18 22:50:51','2019-10-18 22:50:51','2019-10-18 22:50:51','2019-10-18 22:50:51',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'C100053','','','','','','','','3'),(19,'A100075','0','R','Parker','Conrad','Parker','2019-03-17','F','smartmitt','smartmitt','pac73@ou.edu','Softball','College','2019-10-28 00:21:13','2019-10-28 00:21:13','2019-10-28 00:21:13','2019-10-28 00:21:13',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'C100053','','','','','','','','3'),(20,'A100075','0','R','Parker','Conrad','Parker','2019-03-17','F','smartmitt','smartmitt','pac73@ou.edu','Softball','College','2019-10-28 00:24:37','2019-10-28 00:24:37','2019-10-28 00:24:37','2019-10-28 00:24:37',4,4,'0','N',NULL,'N',NULL,NULL,NULL,'C100053','','','','','','','','3');
/*!40000 ALTER TABLE `LocalUsers` ENABLE KEYS */;
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
