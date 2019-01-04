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
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `user_state` (
  `vk_id` int(11) NOT NULL,
  `state` varchar(5) COLLATE utf8_unicode_ci NOT NULL DEFAULT '-1',
  `studnum_attempts` int(11) DEFAULT '0',
  PRIMARY KEY (`vk_id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `voter` (
  `voter_id` int(11) NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) CHARACTER SET utf8 NOT NULL,
  `stud_num` int(11) NOT NULL,
  `year` tinyint(4) NOT NULL,
  `group` varchar(10) CHARACTER SET utf8 DEFAULT NULL,
  `is_self_named` tinyint(1) DEFAULT NULL,
  `vk_id` int(11) DEFAULT NULL,
  `voter_num` int(11) DEFAULT NULL,
  `stream` int(11) DEFAULT NULL,
  PRIMARY KEY (`voter_id`),
  UNIQUE KEY `vk_id_UNIQUE` (`vk_id`),
  KEY `voter_name_IND` (`fullname`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `user_voter_vars` (
  `vk_id` int(11) NOT NULL,
  `voter_id` int(11) NOT NULL,
  `is_self_named` tinyint(4) DEFAULT '0',
  PRIMARY KEY (`vk_id`,`voter_id`),
  KEY `voter_id_fk_idx` (`voter_id`),
  CONSTRAINT `voter_id_fk` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `vote` (
  `voter_id` int(11) NOT NULL,
  `cand_id` int(11) NOT NULL,
  `is_confirm` tinyint(1) NOT NULL DEFAULT '0',
  `conf_date` datetime DEFAULT NULL,
  PRIMARY KEY (`voter_id`,`cand_id`),
  KEY `cand_fk_idx` (`cand_id`),
  CONSTRAINT `cand_fk` FOREIGN KEY (`cand_id`) REFERENCES `candidate` (`cand_id`),
  CONSTRAINT `voter_votes_fk` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`)
) DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
