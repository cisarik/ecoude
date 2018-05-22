-- MySQL dump 10.13  Distrib 5.1.54, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: ecoude
-- ------------------------------------------------------
-- Server version	5.1.54-1ubuntu4

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `permission_id_refs_id_a7792de1` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_message`
--

DROP TABLE IF EXISTS `auth_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `auth_message_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_message`
--

LOCK TABLES `auth_message` WRITE;
/*!40000 ALTER TABLE `auth_message` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=118 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add message',4,'add_message'),(11,'Can change message',4,'change_message'),(12,'Can delete message',4,'delete_message'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add content type',6,'add_contenttype'),(17,'Can change content type',6,'change_contenttype'),(18,'Can delete content type',6,'delete_contenttype'),(19,'Can add session',7,'add_session'),(20,'Can change session',7,'change_session'),(21,'Can delete session',7,'delete_session'),(22,'Can add site',8,'add_site'),(23,'Can change site',8,'change_site'),(24,'Can delete site',8,'delete_site'),(25,'Can add sequences',9,'add_sequences'),(26,'Can change sequences',9,'change_sequences'),(27,'Can delete sequences',9,'delete_sequences'),(28,'Can add framework',10,'add_framework'),(29,'Can change framework',10,'change_framework'),(30,'Can delete framework',10,'delete_framework'),(31,'Can add problem',11,'add_problem'),(32,'Can change problem',11,'change_problem'),(33,'Can delete problem',11,'delete_problem'),(34,'Can add project',12,'add_project'),(35,'Can change project',12,'change_project'),(36,'Can delete project',12,'delete_project'),(37,'Can add input file',13,'add_inputfile'),(38,'Can change input file',13,'change_inputfile'),(39,'Can delete input file',13,'delete_inputfile'),(40,'Can add output file',14,'add_outputfile'),(41,'Can change output file',14,'change_outputfile'),(42,'Can delete output file',14,'delete_outputfile'),(43,'Can add input generator file',15,'add_inputgeneratorfile'),(44,'Can change input generator file',15,'change_inputgeneratorfile'),(45,'Can delete input generator file',15,'delete_inputgeneratorfile'),(46,'Can add source code file',16,'add_sourcecodefile'),(47,'Can change source code file',16,'change_sourcecodefile'),(48,'Can delete source code file',16,'delete_sourcecodefile'),(49,'Can add timeline list',17,'add_timelinelist'),(50,'Can change timeline list',17,'change_timelinelist'),(51,'Can delete timeline list',17,'delete_timelinelist'),(52,'Can add theme',18,'add_theme'),(53,'Can change theme',18,'change_theme'),(54,'Can delete theme',18,'delete_theme'),(55,'Can add theme list',19,'add_themelist'),(56,'Can change theme list',19,'change_themelist'),(57,'Can delete theme list',19,'delete_themelist'),(58,'Can add chart theme list',20,'add_chartthemelist'),(59,'Can change chart theme list',20,'change_chartthemelist'),(60,'Can delete chart theme list',20,'delete_chartthemelist'),(61,'Can add chart style list',21,'add_chartstylelist'),(62,'Can change chart style list',21,'change_chartstylelist'),(63,'Can delete chart style list',21,'delete_chartstylelist'),(64,'Can add priority list',22,'add_prioritylist'),(65,'Can change priority list',22,'change_prioritylist'),(66,'Can delete priority list',22,'delete_prioritylist'),(67,'Can add framework list',23,'add_frameworklist'),(68,'Can change framework list',23,'change_frameworklist'),(69,'Can delete framework list',23,'delete_frameworklist'),(70,'Can add menu',24,'add_menu'),(71,'Can change menu',24,'change_menu'),(72,'Can delete menu',24,'delete_menu'),(73,'Can add menu list',25,'add_menulist'),(74,'Can change menu list',25,'change_menulist'),(75,'Can delete menu list',25,'delete_menulist'),(76,'Can add statistic',26,'add_statistic'),(77,'Can change statistic',26,'change_statistic'),(78,'Can delete statistic',26,'delete_statistic'),(79,'Can add tag',27,'add_tag'),(80,'Can change tag',27,'change_tag'),(81,'Can delete tag',27,'delete_tag'),(82,'Can add note',28,'add_note'),(83,'Can change note',28,'change_note'),(84,'Can delete note',28,'delete_note'),(85,'Can add tag list',29,'add_taglist'),(86,'Can change tag list',29,'change_taglist'),(87,'Can delete tag list',29,'delete_taglist'),(88,'Can add idea',30,'add_idea'),(89,'Can change idea',30,'change_idea'),(90,'Can delete idea',30,'delete_idea'),(91,'Can add idea list',31,'add_idealist'),(92,'Can change idea list',31,'change_idealist'),(93,'Can delete idea list',31,'delete_idealist'),(94,'Can add project idea list',32,'add_projectidealist'),(95,'Can change project idea list',32,'change_projectidealist'),(96,'Can delete project idea list',32,'delete_projectidealist'),(97,'Can add link',33,'add_link'),(98,'Can change link',33,'change_link'),(99,'Can delete link',33,'delete_link'),(100,'Can add link list',34,'add_linklist'),(101,'Can change link list',34,'change_linklist'),(102,'Can delete link list',34,'delete_linklist'),(103,'Can add project link list',35,'add_projectlinklist'),(104,'Can change project link list',35,'change_projectlinklist'),(105,'Can delete project link list',35,'delete_projectlinklist'),(106,'Can add todo',36,'add_todo'),(107,'Can change todo',36,'change_todo'),(108,'Can delete todo',36,'delete_todo'),(109,'Can add todo list',37,'add_todolist'),(110,'Can change todo list',37,'change_todolist'),(111,'Can delete todo list',37,'delete_todolist'),(112,'Can add project todo list',38,'add_projecttodolist'),(113,'Can change project todo list',38,'change_projecttodolist'),(114,'Can delete project todo list',38,'delete_projecttodolist'),(115,'Can add problem tag list',39,'add_problemtaglist'),(116,'Can change problem tag list',39,'change_problemtaglist'),(117,'Can delete problem tag list',39,'delete_problemtaglist');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admin','','','cisary@gmail.com','sha1$0c1d5$58b0f7b813e2bb9d957094c59446ea0539cdac97',1,1,1,'2011-10-12 22:35:47','2011-10-12 21:13:56'),(2,'AnonymousUser','','','','sha1$94e12$efa04e1c2f01db61ab5be5ebfef09efa119b74fa',0,1,0,'2011-10-12 21:15:20','2011-10-12 21:15:20');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `group_id_refs_id_f0ee9890` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `permission_id_refs_id_67e79cb` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_user_id` (`user_id`),
  KEY `django_admin_log_content_type_id` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=54 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2011-10-12 21:15:20',1,3,'2','AnonymousUser',1,''),(2,'2011-10-12 21:21:42',1,17,'1','admin',1,''),(3,'2011-10-12 21:21:50',1,17,'1','admin',2,'No fields changed.'),(4,'2011-10-12 21:21:57',1,17,'2','AnonymousUser',1,''),(5,'2011-10-12 21:32:48',1,18,'1','Blue',1,''),(6,'2011-10-12 21:33:05',1,19,'1','admin',1,''),(7,'2011-10-12 21:35:06',1,19,'2','AnonymousUser',1,''),(8,'2011-10-12 21:35:47',1,27,'1','GP',1,''),(9,'2011-10-12 21:36:12',1,27,'2','GA',1,''),(10,'2011-10-12 21:36:29',1,27,'3','Business',1,''),(11,'2011-10-12 21:36:48',1,27,'4','AI',1,''),(12,'2011-10-12 21:41:04',1,9,'1','Sequence',1,''),(13,'2011-10-12 21:42:38',1,10,'1','pyGene',1,''),(14,'2011-10-12 21:43:35',1,10,'2','GPSDK',1,''),(15,'2011-10-12 21:44:35',1,10,'3','AjGa',1,''),(16,'2011-10-12 21:45:21',1,10,'4','AForge.NET',1,''),(17,'2011-10-12 21:46:03',1,23,'1','pyGene',1,''),(18,'2011-10-12 21:46:08',1,23,'2','GPSDK',1,''),(19,'2011-10-12 21:46:14',1,23,'3','AjGa',1,''),(20,'2011-10-12 21:46:20',1,23,'4','AForge.NET',1,''),(21,'2011-10-12 21:48:10',1,11,'1','SantaFe\'s Ant',1,''),(22,'2011-10-12 21:48:47',1,11,'2','Travelling Salesman',1,''),(23,'2011-10-12 21:49:32',1,15,'1','Ant grid',1,''),(24,'2011-10-12 21:50:00',1,15,'2','TSP canvas',1,''),(25,'2011-10-12 21:51:19',1,22,'1','PriorityList object',1,''),(26,'2011-10-12 21:52:23',1,21,'1','admin',1,''),(27,'2011-10-12 21:52:28',1,21,'2','AnonymousUser',1,''),(28,'2011-10-12 21:52:44',1,20,'1','admin',1,''),(29,'2011-10-12 21:52:49',1,20,'2','AnonymousUser',1,''),(30,'2011-10-12 22:29:13',1,17,'1','admin',2,'Changed show.'),(31,'2011-10-12 22:58:00',1,12,'1','GPSDK SantaFe example',1,''),(32,'2011-10-12 22:58:40',1,12,'2','PyGene TSP example',1,''),(33,'2011-10-12 22:59:11',1,12,'3','AjGa TSP example',1,''),(34,'2011-10-12 23:00:25',1,12,'4','AForge TSP example',1,''),(35,'2011-10-12 23:09:56',1,16,'1','Main',1,''),(36,'2011-10-12 23:10:23',1,16,'2','Main',1,''),(37,'2011-10-12 23:11:04',1,16,'3','Position',1,''),(38,'2011-10-12 23:11:39',1,16,'4','Population',1,''),(39,'2011-10-12 23:12:03',1,16,'5','Mutator',1,''),(40,'2011-10-12 23:12:29',1,16,'6','Main',1,''),(41,'2011-10-12 23:12:55',1,16,'7','GradientMutator',1,''),(42,'2011-10-12 23:13:21',1,16,'8','Genome',1,''),(43,'2011-10-12 23:13:46',1,16,'9','Evolution',1,''),(44,'2011-10-12 23:14:13',1,16,'10','Evaluator',1,''),(45,'2011-10-12 23:14:40',1,16,'11','Crossing',1,''),(46,'2011-10-12 23:15:05',1,16,'12','Creator',1,''),(47,'2011-10-12 23:15:30',1,16,'13','TSPFitnessFunction',1,''),(48,'2011-10-12 23:15:57',1,16,'14','TSPChromosome',1,''),(49,'2011-10-12 23:17:52',1,39,'1','GP',1,''),(50,'2011-10-12 23:18:10',1,39,'2','AI',1,''),(51,'2011-10-12 23:18:29',1,39,'3','GA',1,''),(52,'2011-10-12 23:18:44',1,39,'4','Business',1,''),(53,'2011-10-12 23:22:15',1,26,'1','admin',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=40 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'message','auth','message'),(5,'log entry','admin','logentry'),(6,'content type','contenttypes','contenttype'),(7,'session','sessions','session'),(8,'site','sites','site'),(9,'sequences','system','sequences'),(10,'framework','system','framework'),(11,'problem','system','problem'),(12,'project','system','project'),(13,'input file','system','inputfile'),(14,'output file','system','outputfile'),(15,'input generator file','system','inputgeneratorfile'),(16,'source code file','system','sourcecodefile'),(17,'timeline list','system','timelinelist'),(18,'theme','system','theme'),(19,'theme list','system','themelist'),(20,'chart theme list','system','chartthemelist'),(21,'chart style list','system','chartstylelist'),(22,'priority list','system','prioritylist'),(23,'framework list','system','frameworklist'),(24,'menu','system','menu'),(25,'menu list','system','menulist'),(26,'statistic','system','statistic'),(27,'tag','system','tag'),(28,'note','system','note'),(29,'tag list','system','taglist'),(30,'idea','system','idea'),(31,'idea list','system','idealist'),(32,'project idea list','system','projectidealist'),(33,'link','system','link'),(34,'link list','system','linklist'),(35,'project link list','system','projectlinklist'),(36,'todo','system','todo'),(37,'todo list','system','todolist'),(38,'project todo list','system','projecttodolist'),(39,'problem tag list','system','problemtaglist');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('42ca1fdad1ff0e4596382894d9531f47','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5mZmM1ODA2Y2RkZjg3NTAxNzI1\nYzE1Y2IwODlhODRjZQ==\n','2011-10-26 21:14:40'),('569167f2b3cf6d097fd41ef5416a4897','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEEigEBdS5mZmM1ODA2Y2RkZjg3NTAxNzI1\nYzE1Y2IwODlhODRjZQ==\n','2011-10-26 22:35:47');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_chartstylelist`
--

DROP TABLE IF EXISTS `system_chartstylelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_chartstylelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chartstyle` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_chartstylelist_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_chartstylelist`
--

LOCK TABLES `system_chartstylelist` WRITE;
/*!40000 ALTER TABLE `system_chartstylelist` DISABLE KEYS */;
INSERT INTO `system_chartstylelist` VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `system_chartstylelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_chartthemelist`
--

DROP TABLE IF EXISTS `system_chartthemelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_chartthemelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `charttheme` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_chartthemelist_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_chartthemelist`
--

LOCK TABLES `system_chartthemelist` WRITE;
/*!40000 ALTER TABLE `system_chartthemelist` DISABLE KEYS */;
INSERT INTO `system_chartthemelist` VALUES (1,2,1),(2,0,2);
/*!40000 ALTER TABLE `system_chartthemelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_framework`
--

DROP TABLE IF EXISTS `system_framework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_framework` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `dir` varchar(200) NOT NULL,
  `extension` varchar(5) NOT NULL,
  `coding` varchar(20) NOT NULL,
  `rundirectly` tinyint(1) NOT NULL,
  `buildcommand` varchar(50) NOT NULL,
  `buildparameters` varchar(200) NOT NULL,
  `runcommand` varchar(50) NOT NULL,
  `beforeruncommands` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_framework`
--

LOCK TABLES `system_framework` WRITE;
/*!40000 ALTER TABLE `system_framework` DISABLE KEYS */;
INSERT INTO `system_framework` VALUES (1,'pyGene','pygene','py','utf-8',1,' ',' ','python','export PYTHONPATH=../'),(2,'GPSDK','gpsdk','cs','utf-8',0,'gmcs','-r:../WGP.dll -out:runfile.exe','mono runfile.exe','export MONO_PATH=../'),(3,'AjGa','ajga','cs','utf-8',0,'gmcs','-r:../BaseEvolution.dll -out:runfile.exe','mono runfile.exe','export MONO_PATH=../'),(4,'AForge.NET','aforge','cs','utf-8',0,'gmcs','-r:../AForge.Genetic.dll -out:runfile.exe','mono runfile.exe','export MONO_PATH=../');
/*!40000 ALTER TABLE `system_framework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_frameworklist`
--

DROP TABLE IF EXISTS `system_frameworklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_frameworklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `framework_id` int(11) NOT NULL,
  `active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_frameworklist_user_id` (`user_id`),
  KEY `system_frameworklist_framework_id` (`framework_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_frameworklist`
--

LOCK TABLES `system_frameworklist` WRITE;
/*!40000 ALTER TABLE `system_frameworklist` DISABLE KEYS */;
INSERT INTO `system_frameworklist` VALUES (1,1,1,1),(2,1,2,1),(3,1,3,0),(4,1,4,1);
/*!40000 ALTER TABLE `system_frameworklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_idea`
--

DROP TABLE IF EXISTS `system_idea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_idea` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_idea_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_idea`
--

LOCK TABLES `system_idea` WRITE;
/*!40000 ALTER TABLE `system_idea` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_idea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_idealist`
--

DROP TABLE IF EXISTS `system_idealist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_idealist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note_id` int(11) NOT NULL,
  `idea_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_idealist_note_id` (`note_id`),
  KEY `system_idealist_idea_id` (`idea_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_idealist`
--

LOCK TABLES `system_idealist` WRITE;
/*!40000 ALTER TABLE `system_idealist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_idealist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_inputfile`
--

DROP TABLE IF EXISTS `system_inputfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_inputfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `template` varchar(200) NOT NULL,
  `problem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_inputfile_problem_id` (`problem_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_inputfile`
--

LOCK TABLES `system_inputfile` WRITE;
/*!40000 ALTER TABLE `system_inputfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_inputfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_inputgeneratorfile`
--

DROP TABLE IF EXISTS `system_inputgeneratorfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_inputgeneratorfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `template` varchar(200) NOT NULL,
  `problem_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_inputgeneratorfile_user_id` (`user_id`),
  KEY `system_inputgeneratorfile_problem_id` (`problem_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_inputgeneratorfile`
--

LOCK TABLES `system_inputgeneratorfile` WRITE;
/*!40000 ALTER TABLE `system_inputgeneratorfile` DISABLE KEYS */;
INSERT INTO `system_inputgeneratorfile` VALUES (1,1,'Ant grid','inputgeneratorfiles/2',1),(2,1,'TSP canvas','inputgeneratorfiles/1',2);
/*!40000 ALTER TABLE `system_inputgeneratorfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_link`
--

DROP TABLE IF EXISTS `system_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_link` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_link_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_link`
--

LOCK TABLES `system_link` WRITE;
/*!40000 ALTER TABLE `system_link` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_linklist`
--

DROP TABLE IF EXISTS `system_linklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_linklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note_id` int(11) NOT NULL,
  `link_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_linklist_note_id` (`note_id`),
  KEY `system_linklist_link_id` (`link_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_linklist`
--

LOCK TABLES `system_linklist` WRITE;
/*!40000 ALTER TABLE `system_linklist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_linklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_menu`
--

DROP TABLE IF EXISTS `system_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `url` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_menu`
--

LOCK TABLES `system_menu` WRITE;
/*!40000 ALTER TABLE `system_menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_menulist`
--

DROP TABLE IF EXISTS `system_menulist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_menulist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `framework_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_menulist_framework_id` (`framework_id`),
  KEY `system_menulist_menu_id` (`menu_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_menulist`
--

LOCK TABLES `system_menulist` WRITE;
/*!40000 ALTER TABLE `system_menulist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_menulist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_note`
--

DROP TABLE IF EXISTS `system_note`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_note` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `problem_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_note_problem_id` (`problem_id`),
  KEY `system_note_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_note`
--

LOCK TABLES `system_note` WRITE;
/*!40000 ALTER TABLE `system_note` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_note` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_outputfile`
--

DROP TABLE IF EXISTS `system_outputfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_outputfile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fitness` int(11) NOT NULL,
  `template` varchar(200) NOT NULL,
  `inputfile_id` int(11) NOT NULL,
  `solved` tinyint(1) NOT NULL,
  `framework_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_outputfile_inputfile_id` (`inputfile_id`),
  KEY `system_outputfile_framework_id` (`framework_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_outputfile`
--

LOCK TABLES `system_outputfile` WRITE;
/*!40000 ALTER TABLE `system_outputfile` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_outputfile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_prioritylist`
--

DROP TABLE IF EXISTS `system_prioritylist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_prioritylist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `priority` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_prioritylist_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_prioritylist`
--

LOCK TABLES `system_prioritylist` WRITE;
/*!40000 ALTER TABLE `system_prioritylist` DISABLE KEYS */;
INSERT INTO `system_prioritylist` VALUES (1,1,4);
/*!40000 ALTER TABLE `system_prioritylist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_problem`
--

DROP TABLE IF EXISTS `system_problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_problem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `template` varchar(100) NOT NULL,
  `notes` int(11) NOT NULL,
  `links` int(11) NOT NULL,
  `ideas` int(11) NOT NULL,
  `todos` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_problem_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_problem`
--

LOCK TABLES `system_problem` WRITE;
/*!40000 ALTER TABLE `system_problem` DISABLE KEYS */;
INSERT INTO `system_problem` VALUES (1,1,'2011-10-12 21:47:47','SantaFe\'s Ant','Basic gennetic programming problem','problems/2.html',0,0,0,0),(2,1,'2011-10-12 21:48:25','Travelling Salesman','Basic factorial complexivity problem','problems/1.html',0,0,0,0);
/*!40000 ALTER TABLE `system_problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_problemtaglist`
--

DROP TABLE IF EXISTS `system_problemtaglist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_problemtaglist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `problem_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_problemtaglist_problem_id` (`problem_id`),
  KEY `system_problemtaglist_tag_id` (`tag_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_problemtaglist`
--

LOCK TABLES `system_problemtaglist` WRITE;
/*!40000 ALTER TABLE `system_problemtaglist` DISABLE KEYS */;
INSERT INTO `system_problemtaglist` VALUES (1,1,1),(2,1,4),(3,2,2),(4,2,3);
/*!40000 ALTER TABLE `system_problemtaglist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_project`
--

DROP TABLE IF EXISTS `system_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `framework_id` int(11) NOT NULL,
  `problem_id` int(11) NOT NULL,
  `runnable` tinyint(1) NOT NULL,
  `public` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_project_framework_id` (`framework_id`),
  KEY `system_project_problem_id` (`problem_id`),
  KEY `system_project_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_project`
--

LOCK TABLES `system_project` WRITE;
/*!40000 ALTER TABLE `system_project` DISABLE KEYS */;
INSERT INTO `system_project` VALUES (1,'GPSDK SantaFe example',2,1,1,1,1),(2,'PyGene TSP example',1,2,1,1,1),(3,'AjGa TSP example',3,2,1,1,1),(4,'AForge TSP example',4,2,1,1,1);
/*!40000 ALTER TABLE `system_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_projectidealist`
--

DROP TABLE IF EXISTS `system_projectidealist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_projectidealist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `idea_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_projectidealist_project_id` (`project_id`),
  KEY `system_projectidealist_idea_id` (`idea_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_projectidealist`
--

LOCK TABLES `system_projectidealist` WRITE;
/*!40000 ALTER TABLE `system_projectidealist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_projectidealist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_projectlinklist`
--

DROP TABLE IF EXISTS `system_projectlinklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_projectlinklist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `link_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_projectlinklist_project_id` (`project_id`),
  KEY `system_projectlinklist_link_id` (`link_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_projectlinklist`
--

LOCK TABLES `system_projectlinklist` WRITE;
/*!40000 ALTER TABLE `system_projectlinklist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_projectlinklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_projecttodolist`
--

DROP TABLE IF EXISTS `system_projecttodolist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_projecttodolist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `todo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_projecttodolist_project_id` (`project_id`),
  KEY `system_projecttodolist_todo_id` (`todo_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_projecttodolist`
--

LOCK TABLES `system_projecttodolist` WRITE;
/*!40000 ALTER TABLE `system_projecttodolist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_projecttodolist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_sequences`
--

DROP TABLE IF EXISTS `system_sequences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_sequences` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `problems` int(11) NOT NULL,
  `problemlists` int(11) NOT NULL,
  `tags` int(11) NOT NULL,
  `taglists` int(11) NOT NULL,
  `problemtaglists` int(11) NOT NULL,
  `notes` int(11) NOT NULL,
  `links` int(11) NOT NULL,
  `linklists` int(11) NOT NULL,
  `ideas` int(11) NOT NULL,
  `idealists` int(11) NOT NULL,
  `todos` int(11) NOT NULL,
  `todolists` int(11) NOT NULL,
  `projects` int(11) NOT NULL,
  `sourcecodefiles` int(11) NOT NULL,
  `inputfiles` int(11) NOT NULL,
  `outputfiles` int(11) NOT NULL,
  `inputgeneratorfiles` int(11) NOT NULL,
  `projectlinklists` int(11) NOT NULL,
  `projectidealists` int(11) NOT NULL,
  `projecttodolists` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_sequences`
--

LOCK TABLES `system_sequences` WRITE;
/*!40000 ALTER TABLE `system_sequences` DISABLE KEYS */;
INSERT INTO `system_sequences` VALUES (1,2,0,4,0,4,0,0,0,0,0,0,0,4,15,0,0,2,0,0,0);
/*!40000 ALTER TABLE `system_sequences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_sourcecodefile`
--

DROP TABLE IF EXISTS `system_sourcecodefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_sourcecodefile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `template` varchar(200) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_sourcecodefile_project_id` (`project_id`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_sourcecodefile`
--

LOCK TABLES `system_sourcecodefile` WRITE;
/*!40000 ALTER TABLE `system_sourcecodefile` DISABLE KEYS */;
INSERT INTO `system_sourcecodefile` VALUES (1,'Main','10/Main.cs',1),(2,'Main','9/Main.py',2),(3,'Position','2/Position.cs',3),(4,'Population','2/Population.cs',3),(5,'Mutator','2/Mutator.cs',3),(6,'Main','2/Main.cs',3),(7,'GradientMutator','2/GradientMutator.cs',3),(8,'Genome','2/Genome.cs',3),(9,'Evolution','2/Evolution.cs',3),(10,'Evaluator','2/Evaluator.cs',3),(11,'Crossing','2/Crossing.cs',3),(12,'Creator','2/Creator.cs',3),(13,'TSPFitnessFunction','1/TSPFitnessFunction.cs',4),(14,'TSPChromosome','1/TSPChromosome.cs',4);
/*!40000 ALTER TABLE `system_sourcecodefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_statistic`
--

DROP TABLE IF EXISTS `system_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `tags` int(11) NOT NULL,
  `notes` int(11) NOT NULL,
  `links` int(11) NOT NULL,
  `ideas` int(11) NOT NULL,
  `todos` int(11) NOT NULL,
  `problems` int(11) NOT NULL,
  `projects` int(11) NOT NULL,
  `files` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_statistic_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_statistic`
--

LOCK TABLES `system_statistic` WRITE;
/*!40000 ALTER TABLE `system_statistic` DISABLE KEYS */;
INSERT INTO `system_statistic` VALUES (1,1,4,0,0,0,0,2,4,15);
/*!40000 ALTER TABLE `system_statistic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_tag`
--

DROP TABLE IF EXISTS `system_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_tag_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_tag`
--

LOCK TABLES `system_tag` WRITE;
/*!40000 ALTER TABLE `system_tag` DISABLE KEYS */;
INSERT INTO `system_tag` VALUES (1,'GP',1,'2011-10-12 21:35:45'),(2,'GA',1,'2011-10-12 21:36:10'),(3,'Business',1,'2011-10-12 21:36:27'),(4,'AI',1,'2011-10-12 21:36:46');
/*!40000 ALTER TABLE `system_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_taglist`
--

DROP TABLE IF EXISTS `system_taglist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_taglist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_taglist_note_id` (`note_id`),
  KEY `system_taglist_tag_id` (`tag_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_taglist`
--

LOCK TABLES `system_taglist` WRITE;
/*!40000 ALTER TABLE `system_taglist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_taglist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_theme`
--

DROP TABLE IF EXISTS `system_theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_theme` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_theme`
--

LOCK TABLES `system_theme` WRITE;
/*!40000 ALTER TABLE `system_theme` DISABLE KEYS */;
INSERT INTO `system_theme` VALUES (1,'Blue');
/*!40000 ALTER TABLE `system_theme` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_themelist`
--

DROP TABLE IF EXISTS `system_themelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_themelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `theme_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_themelist_theme_id` (`theme_id`),
  KEY `system_themelist_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_themelist`
--

LOCK TABLES `system_themelist` WRITE;
/*!40000 ALTER TABLE `system_themelist` DISABLE KEYS */;
INSERT INTO `system_themelist` VALUES (1,1,1),(2,1,2);
/*!40000 ALTER TABLE `system_themelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_timelinelist`
--

DROP TABLE IF EXISTS `system_timelinelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_timelinelist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `show` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_timelinelist_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_timelinelist`
--

LOCK TABLES `system_timelinelist` WRITE;
/*!40000 ALTER TABLE `system_timelinelist` DISABLE KEYS */;
INSERT INTO `system_timelinelist` VALUES (1,0,1),(2,1,2);
/*!40000 ALTER TABLE `system_timelinelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_todo`
--

DROP TABLE IF EXISTS `system_todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_todo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `user_id` int(11) NOT NULL,
  `text` varchar(1000) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_todo_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_todo`
--

LOCK TABLES `system_todo` WRITE;
/*!40000 ALTER TABLE `system_todo` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_todo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_todolist`
--

DROP TABLE IF EXISTS `system_todolist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_todolist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `note_id` int(11) NOT NULL,
  `todo_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `system_todolist_note_id` (`note_id`),
  KEY `system_todolist_todo_id` (`todo_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_todolist`
--

LOCK TABLES `system_todolist` WRITE;
/*!40000 ALTER TABLE `system_todolist` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_todolist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2011-10-12 21:28:27
