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
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `MachineID` varchar(20) DEFAULT NULL,
  `AccountID` varchar(100) DEFAULT NULL,
  `SeqSessionNumber` int(11) DEFAULT NULL,
  `Status` varchar(20) DEFAULT NULL COMMENT 'New, Open, PendingUpload, Closed, Suspended(ended prematurely)',
  `SessionType` varchar(20) DEFAULT NULL,
  `StandardTargetGUID` varchar(50) DEFAULT NULL COMMENT 'GUID',
  `PracticeGUID` varchar(50) DEFAULT NULL COMMENT 'GUID',
  `GameLineUpGUID` varchar(50) DEFAULT NULL COMMENT 'GUID',
  `ArcadeGUID` varchar(50) DEFAULT NULL COMMENT 'GUID',
  `BallType` varchar(10) DEFAULT NULL,
  `DisplaySpeedForSeconds` int(11) DEFAULT NULL,
  `DisplayImpactForSeconds` int(11) DEFAULT NULL,
  `SuspendTimeOutSeconds` int(11) DEFAULT NULL,
  `DisplayRiverYN` varchar(5) DEFAULT NULL,
  `DisplayPitchCountBarsYN` varchar(5) DEFAULT NULL,
  `YverticalOffsetDeltaValue` varchar(10) DEFAULT NULL,
  `PitchingDistanceFeet` int(11) DEFAULT NULL,
  `SystemOnLineYN` varchar(5) DEFAULT NULL,
  `StudentDisplayName` varchar(45) DEFAULT NULL,
  `CreateDtm` timestamp NULL DEFAULT NULL,
  `LastBackEndPingDtm` timestamp NULL DEFAULT NULL,
  `LastFrontEndPingDtm` timestamp NULL DEFAULT NULL,
  `SessionEndedDtm` timestamp NULL DEFAULT NULL,
  `SessionUploadedDtm` timestamp NULL DEFAULT NULL,
  `PracticeRepetitions` int(11) DEFAULT NULL,
  `ReleaseSpeedAddon` int(11) DEFAULT NULL,
  `TimetoshowPlaySpeed` int(5) DEFAULT NULL,
  `TimetoshowReleaseSpeed` int(5) DEFAULT NULL,
  `ShowSuccessOrMiss` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=588 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES (543,'SM990005','A100230',645,'Open','standard','SMV1-IM-R',NULL,NULL,NULL,'Baseball',1,4,60,'Y','Y',NULL,60,'Y','Sandlot','2019-10-18 22:54:24',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(544,'SM990005','A100096',646,'Open','standard','SMV1-SL-R',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-27 19:54:35',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(545,'SM990005','A100096',647,'Open','standard','SMV1-SELECT',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-27 20:31:54',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(546,'SM990005','A100096',648,'Open','standard','SMV1-PA-R',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-27 20:38:15',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(547,'SM990005','A100096',649,'Open','standard','SMV1-SL-R',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-27 23:50:37',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(548,'SM990005','A100096',650,'UPLOADED','standard','SMV1-SELECT',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-28 00:08:56',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(549,'SM990005','A100096',651,'Open','standard','SMV1-INTERMED',NULL,NULL,NULL,'Baseball',1,5,60,'Y','Y',NULL,60,'Y','Impact','2019-10-28 00:25:06',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(550,'SM990005','smartmitt',652,'KILLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',4,4,15,'Y','N',NULL,43,'N','Admin','2019-12-15 21:09:03',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(551,'SM990005','smartmitt',653,'Open','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',4,4,15,'Y','N',NULL,43,'N','Admin','2019-12-15 21:21:28',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(552,'SM990005','smartmitt',654,'KILLED','standard','SMV1-INTERMED',NULL,NULL,NULL,'Softball',4,4,15,'Y','N',NULL,43,'N','Admin','2020-03-04 16:59:04',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(553,'SM990005','smartmitt',655,'CANCELLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,15,'Y','N',NULL,43,'N','Admin','2020-03-04 17:11:27',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(554,'SM990005','smartmitt',656,'CANCELLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,15,'Y','N',NULL,43,'N','Admin','2020-03-04 17:13:06',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(555,'SM990005','smartmitt',657,'CANCELLED','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',6,4,15,'Y','N',NULL,43,'N','Admin','2020-03-04 18:12:43',NULL,NULL,NULL,NULL,3,NULL,NULL,NULL,NULL),(556,'SM990005','smartmitt',658,'KILLED','standard','SMV1-IM-R',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-04 18:45:32',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(557,'SM990005','smartmitt',659,'KILLED','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-04 18:59:31',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(558,'SM990005','smartmitt',660,'CANCELLED','standard','SMV1-PA-R',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-04 19:00:49',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(559,'SM990005','smartmitt',661,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 05:49:48',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(560,'SM990005','smartmitt',662,'CANCELLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 05:59:25',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(561,'SM990005','smartmitt',663,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 06:26:13',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(562,'SM990005','smartmitt',664,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 06:34:43',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(563,'SM990005','smartmitt',665,'KILLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 13:20:29',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(564,'SM990005','smartmitt',666,'UPLOADED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 13:27:21',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(565,'SM990005','smartmitt',667,'CANCELLED','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 14:34:00',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(566,'SM990005','smartmitt',668,'UPLOADED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 21:12:17',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(567,'SM990005','smartmitt',669,'CANCELLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-05 21:20:18',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(568,'SM990005','smartmitt',670,'UPLOADED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-06 22:19:32',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(569,'SM990005','smartmitt',671,'CANCELLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-06 22:27:42',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(570,'SM990005','smartmitt',672,'UPLOADED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-06 23:17:51',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(571,'SM990005','smartmitt',673,'KILLED','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-07 06:02:53',NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL),(572,'SM990005','smartmitt',674,'CANCELLED','practice',NULL,'C100055-Switch Sides Out and In',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-07 09:47:17',NULL,NULL,NULL,NULL,1,NULL,6,6,'yes'),(573,'SM990005','smartmitt',675,'KILLED','standard','SMV1-ED-R',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-07 18:42:03',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(574,'SM990005','smartmitt',676,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 05:12:44',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(575,'SM990005','smartmitt',677,'UPLOADED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 07:02:57',NULL,NULL,NULL,NULL,1,NULL,6,6,''),(576,'SM990005','smartmitt',678,'KILLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 10:49:32',NULL,NULL,NULL,NULL,1,NULL,6,6,''),(577,'SM990005','smartmitt',679,'KILLED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 10:50:31',NULL,NULL,NULL,NULL,1,NULL,6,6,'no'),(578,'SM990005','smartmitt',680,'UPLOADED','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 13:02:58',NULL,NULL,NULL,NULL,1,NULL,6,6,'no'),(579,'SM990005','smartmitt',681,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 13:16:41',NULL,NULL,NULL,NULL,NULL,NULL,6,6,'no'),(580,'SM990005','smartmitt',682,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 13:18:57',NULL,NULL,NULL,NULL,NULL,NULL,6,6,'no'),(581,'SM990005','smartmitt',683,'KILLED','practice',NULL,'',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 13:25:21',NULL,NULL,NULL,NULL,3,NULL,6,6,'no'),(582,'SM990005','smartmitt',684,'CANCELLED','standard','SMV1-IM-R',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 13:43:57',NULL,NULL,NULL,NULL,NULL,NULL,6,6,'no'),(583,'SM990005','smartmitt',685,'KILLED','practice',NULL,'',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,43,'N','Admin','2020-03-09 18:06:59',NULL,NULL,NULL,NULL,9,NULL,6,6,'no'),(584,'SM990005','smartmitt',686,'KILLED','practice',NULL,'',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,40,'N','Admin','2020-03-12 22:04:05',NULL,NULL,NULL,NULL,9,NULL,6,6,'no'),(585,'SM990005','smartmitt',687,'KILLED','practice',NULL,'',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,38,'N','Admin','2020-03-13 15:55:11',NULL,NULL,NULL,NULL,9,NULL,6,6,'no'),(586,'SM990005','smartmitt',688,'KILLED','standard','SMV1-EARLYDEV',NULL,NULL,NULL,'Softball',6,4,30,'Y','N',NULL,38,'N','Admin','2020-03-13 16:00:38',NULL,NULL,NULL,NULL,NULL,NULL,6,6,'no'),(587,'SM990005','smartmitt',689,'Open','practice',NULL,'C100055-Inside and Outside Pitched',NULL,NULL,'Softball',6,4,30,'Y','N',NULL,38,'N','Admin','2020-03-16 15:32:24',NULL,NULL,NULL,NULL,1,NULL,6,6,'no');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
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
