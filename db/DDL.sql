
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
-- Table structure for table `bach_to_master`
--

DROP TABLE IF EXISTS `bach_to_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bach_to_master` (
  `stud_num` int(11) NOT NULL,
  `new_stud_num` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `candidate`
--

DROP TABLE IF EXISTS `candidate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `candidate` (
  `cand_id` int(11) NOT NULL AUTO_INCREMENT,
  `surname` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `midname` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `year` tinyint(4) NOT NULL,
  `vk_id` int(11) DEFAULT NULL,
  `description` text COLLATE utf8_unicode_ci,
  `program` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL,
  `video` varchar(70) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`cand_id`),
  KEY `voter_fk_idx` (`vk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prev_users`
--

DROP TABLE IF EXISTS `prev_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prev_users` (
  `vk_id` int(11) NOT NULL,
  `stud_num` int(11) NOT NULL,
  PRIMARY KEY (`vk_id`,`stud_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_msg`
--

DROP TABLE IF EXISTS `user_msg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_msg` (
  `vk_id` int(11) NOT NULL,
  `msg_id` int(11) NOT NULL,
  PRIMARY KEY (`vk_id`,`msg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_msgs`
--

DROP TABLE IF EXISTS `user_msgs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_msgs` (
  `vk_id` int(11) NOT NULL,
  `msg_id` int(11) NOT NULL,
  PRIMARY KEY (`vk_id`,`msg_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_state`
--

DROP TABLE IF EXISTS `user_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_state` (
  `vk_id` int(11) NOT NULL,
  `state` varchar(5) COLLATE utf8_unicode_ci NOT NULL DEFAULT '-1',
  `studnum_attempts` int(11) DEFAULT '0',
  PRIMARY KEY (`vk_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user_voter_vars`
--

DROP TABLE IF EXISTS `user_voter_vars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_voter_vars` (
  `vk_id` int(11) NOT NULL,
  `voter_id` int(11) NOT NULL,
  `is_self_named` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`vk_id`,`voter_id`),
  KEY `voter_id_fk_idx` (`voter_id`),
  CONSTRAINT `voter_id_fk` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vote` (
  `voter_id` int(11) NOT NULL,
  `cand_id` int(11) NOT NULL,
  `is_confirm` tinyint(1) NOT NULL DEFAULT '0',
  `conf_date` datetime DEFAULT NULL,
  PRIMARY KEY (`voter_id`,`cand_id`),
  KEY `cand_fk_idx` (`cand_id`),
  CONSTRAINT `cand_fk` FOREIGN KEY (`cand_id`) REFERENCES `candidate` (`cand_id`),
  CONSTRAINT `voter_votes_fk` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `voter`
--

DROP TABLE IF EXISTS `voter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `voter` (
  `voter_id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) CHARACTER SET utf8 NOT NULL,
  `stud_num` int(11) NOT NULL,
  `year` tinyint(4) NOT NULL,
  `group` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `is_self_named` tinyint(1) DEFAULT NULL,
  `vk_id` int(11) DEFAULT NULL,
  `voter_num` int(11) DEFAULT NULL,
  `stream` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`voter_id`),
  UNIQUE KEY `vk_id_UNIQUE` (`vk_id`),
  KEY `voter_name_IND` (`fullname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
