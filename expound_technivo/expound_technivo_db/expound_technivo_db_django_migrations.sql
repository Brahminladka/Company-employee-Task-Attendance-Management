CREATE DATABASE  IF NOT EXISTS `expound_technivo_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `expound_technivo_db`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: expound_technivo_db
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-08-24 14:53:08.639249'),(2,'auth','0001_initial','2025-08-24 14:53:09.046897'),(3,'admin','0001_initial','2025-08-24 14:53:09.125377'),(4,'admin','0002_logentry_remove_auto_add','2025-08-24 14:53:09.130376'),(5,'admin','0003_logentry_add_action_flag_choices','2025-08-24 14:53:09.135232'),(6,'contenttypes','0002_remove_content_type_name','2025-08-24 14:53:09.209108'),(7,'auth','0002_alter_permission_name_max_length','2025-08-24 14:53:09.247677'),(8,'auth','0003_alter_user_email_max_length','2025-08-24 14:53:09.261228'),(9,'auth','0004_alter_user_username_opts','2025-08-24 14:53:09.266561'),(10,'auth','0005_alter_user_last_login_null','2025-08-24 14:53:09.302784'),(11,'auth','0006_require_contenttypes_0002','2025-08-24 14:53:09.304095'),(12,'auth','0007_alter_validators_add_error_messages','2025-08-24 14:53:09.308142'),(13,'auth','0008_alter_user_username_max_length','2025-08-24 14:53:09.346999'),(14,'auth','0009_alter_user_last_name_max_length','2025-08-24 14:53:09.400911'),(15,'auth','0010_alter_group_name_max_length','2025-08-24 14:53:09.415000'),(16,'auth','0011_update_proxy_permissions','2025-08-24 14:53:09.421679'),(17,'auth','0012_alter_user_first_name_max_length','2025-08-24 14:53:09.471640'),(18,'sessions','0001_initial','2025-08-24 14:54:19.449080'),(19,'core','0001_initial','2025-08-24 15:03:26.574329'),(20,'core','0002_attendance_shared_with','2025-08-25 07:42:29.300911'),(21,'core','0003_employee_exit_date_employee_manager','2025-08-27 07:56:40.231727'),(22,'core','0002_employee_manager_names','2025-08-27 13:56:14.407879'),(23,'core','0003_alter_employee_manager_names','2025-08-27 14:07:16.409775'),(24,'core','0002_employee_role','2025-08-28 13:26:30.512221');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-31 21:26:16
