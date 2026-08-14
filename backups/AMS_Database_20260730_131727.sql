-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: ams_db
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `first_name` varchar(120) NOT NULL,
  `surname` varchar(120) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('Administrator','Staff') DEFAULT 'Staff',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'Mr','Souvik','Maiti','souvik99','souvikmaiti178@gmail.com','scrypt:32768:8:1$vvtAUu60PivppM8i$a825c8de2c03fc52e8b54ac51077e992324aa1c3f6c621044880bf176bc2fdd9a30e69805444c35b901244cbb3d00a0036d89bf42c7d5b901a5b1151bb526e0f','Staff','2026-07-20 07:07:34'),(2,'Mr','Surajit','Paul','surajit88','amsmanpower25@gmail.com','scrypt:32768:8:1$6zvo3AMIw9AqEUKI$87406adce920e1ab11d2fdf3790c3e37fe5d745d0166693fee17c9363693b1379f2ca83b5818919166663c165f2163f0f3c9ff0132d484028ce27503b851d200','Administrator','2026-07-20 08:14:31');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `announcements`
--

DROP TABLE IF EXISTS `announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `announcements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `message` text NOT NULL,
  `updated_by` int DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `updated_by` (`updated_by`),
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`updated_by`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `announcements`
--

LOCK TABLES `announcements` WRITE;
/*!40000 ALTER TABLE `announcements` DISABLE KEYS */;
INSERT INTO `announcements` VALUES (1,'Welcome to AMS Resources | Hiring Across India | Call Us Today for Staffing Solutions | Trusted Manpower Consultancy',1,'2026-07-22 13:44:59');
/*!40000 ALTER TABLE `announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applications`
--

DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `application_id` varchar(20) NOT NULL,
  `mandate_id` varchar(20) NOT NULL,
  `employer` varchar(200) NOT NULL,
  `designation` varchar(200) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `passport_no` varchar(50) NOT NULL,
  `dob` date DEFAULT NULL,
  `age` int DEFAULT NULL,
  `passport_type` enum('ECNR','ECR') DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `gender` enum('Male','Female','Others') DEFAULT NULL,
  `marital_status` enum('Single','Married','Divorced') DEFAULT NULL,
  `address` text,
  `india_experience` decimal(4,1) DEFAULT NULL,
  `gulf_experience` decimal(4,1) DEFAULT NULL,
  `total_experience` decimal(4,1) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  `cv_file` varchar(255) DEFAULT NULL,
  `passport_copy` varchar(255) DEFAULT NULL,
  `photo` varchar(255) DEFAULT NULL,
  `education_certificate` varchar(255) DEFAULT NULL,
  `experience_certificate` varchar(255) DEFAULT NULL,
  `trade_certificate` varchar(255) DEFAULT NULL,
  `status` enum('Pending','Shortlisted','Interviewed','Selected','Rejected') DEFAULT 'Pending',
  `applied_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `application_id` (`application_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applications`
--

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (2,'APP-2026-0001','AMS-2026-0004','Alghanim International','Sheet Metal Fitter','Sobuj Manna','S8958752','1995-12-21',30,'ECR','9934624568','sobuj.manna@gmail.com','Male','Divorced','Patanda, Bihar, 754215',3.0,2.0,5.0,'Madhyamik','cv/PRASENJIT_MAITY_OL.pdf','passport/SUBRATA_BYAPARI_PP_F.pdf','photo/PRADIP_HAZRA_V1215199.jpg','education/BAIN_HARIDAS.pdf','experience/BISWAS_UTTAM.pdf','trade/GHOSH_SWARAJIT.pdf','Selected','2026-07-22 11:23:14');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidates`
--

DROP TABLE IF EXISTS `candidates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidates` (
  `id` int NOT NULL AUTO_INCREMENT,
  `candidate_id` varchar(20) NOT NULL,
  `full_name` varchar(200) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `target_role` varchar(150) DEFAULT NULL,
  `cv_file` varchar(255) NOT NULL,
  `status` enum('Available','Under Review','Shortlisted','Placed','Inactive') DEFAULT 'Available',
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `candidate_id` (`candidate_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidates`
--

LOCK TABLES `candidates` WRITE;
/*!40000 ALTER TABLE `candidates` DISABLE KEYS */;
INSERT INTO `candidates` VALUES (1,'CAN-2026-0001','Mona Das','9875421556','mona.das235@email.com','Receptionist','candidates/MONDAL_WASIM.pdf','Shortlisted','2026-07-23 06:30:16');
/*!40000 ALTER TABLE `candidates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `client_name` varchar(200) NOT NULL,
  `country` varchar(100) NOT NULL,
  `logo_file` varchar(255) NOT NULL,
  `created_by` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `clients_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `admins` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'Sinopec Engineering','UAE','1d8722bf49f14b8ca30c5c736b574e14.png',1,'2026-07-23 11:28:43'),(2,'Al Arkan Construction LLC','Oman','62668ce4fcd344a1a7cf670da74fb0c8.png',1,'2026-07-23 11:32:04'),(3,'Almen','Kuwait','e124b13fc02e4c2a84781412169865b0.jpg',1,'2026-07-23 11:32:41'),(4,'Alghanim International','UAE','ffef3e78cb4f415183cd223df8b41547.jpg',1,'2026-07-23 11:33:26'),(5,'Dhafir Technologies LLC','UAE','90a7ae145ec2487f826b60ed8b235fa4.png',1,'2026-07-23 11:35:24'),(6,'Al Adrak','Oman','5efe2cb076da481ca81939361bf49dfd.png',1,'2026-07-23 11:36:59'),(7,'Eram Engineering','Saudi Arabia','e2fe753d86fa472797758aa4c1dba62b.png',1,'2026-07-23 11:37:48'),(8,'Jurong Engineering Limited','Abu Dhabi','f176f10b9b6e4862a6f44793525e3503.png',1,'2026-07-23 11:39:32'),(9,'MIDMAC Contracting Company W.L.L','Qatar','050d55f4fdae4c2588c601c053197021.png',1,'2026-07-23 11:43:11'),(10,'NMDC Energy','Abu Dhabi','85a0ed79a9bd4bc78cc86abc497713c4.png',1,'2026-07-23 11:43:47');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(200) NOT NULL,
  `email` varchar(150) NOT NULL,
  `subject` varchar(255) DEFAULT NULL,
  `message` text NOT NULL,
  `status` enum('Unread','Read','Replied','Archived') DEFAULT 'Unread',
  `replied` enum('No','Yes') DEFAULT 'No',
  `replied_by` int DEFAULT NULL,
  `replied_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (3,'Babai Das','amsresourceskolkata@outlook.com','Passport Related','I want to know about status of my passport.','Replied','No',NULL,NULL,'2026-07-23 14:22:15');
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gallery`
--

DROP TABLE IF EXISTS `gallery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gallery` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `media_file` varchar(255) NOT NULL,
  `media_type` enum('image','video') NOT NULL,
  `uploaded_by` int DEFAULT NULL,
  `uploaded_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uploaded_by` (`uploaded_by`),
  CONSTRAINT `gallery_ibfk_1` FOREIGN KEY (`uploaded_by`) REFERENCES `admins` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gallery`
--

LOCK TABLES `gallery` WRITE;
/*!40000 ALTER TABLE `gallery` DISABLE KEYS */;
INSERT INTO `gallery` VALUES (2,'Trade Test','2591d163418b47659bb4756530f0ea5c.mp4','video',1,'2026-07-23 09:32:57'),(4,'Logo','be65efbec5e449d7bbf3f914355c1783.jpg','image',1,'2026-07-23 10:17:55'),(5,'Outsourcing','0f2a6ac4ca2b465f9f358abd2e5d372f.png','image',1,'2026-07-23 10:26:05'),(6,'Interview','54534d4219974e13b4951bbee9b52148.jpeg','image',1,'2026-07-23 10:33:38'),(7,'Interviewer','7749d757d6b446c29650a2d4b316d8ae.jpeg','image',1,'2026-07-23 10:34:02');
/*!40000 ALTER TABLE `gallery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `jobs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mandate_id` varchar(20) NOT NULL,
  `employer` varchar(200) NOT NULL,
  `designation` varchar(200) NOT NULL,
  `industry` varchar(150) NOT NULL,
  `experience` varchar(150) DEFAULT NULL,
  `location` varchar(150) DEFAULT NULL,
  `specifications` text,
  `status` enum('Active','Closed') DEFAULT 'Active',
  `created_by` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mandate_id` (`mandate_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `admins` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (2,'AMS-2026-0002','Sinopec Engineering','Shuttering Carpenter','Engineering','1-2 Years','Dubai','Free Food • Free Accommodation • Salary: 1200 AED','Closed',1,'2026-07-21 08:53:52'),(3,'AMS-2026-0003','Sinopec Engineering','Insulator','Engineering','1-2 Years','UAE','Free Food • Free Accommodation • Salary: 1200 AED','Active',2,'2026-07-21 09:06:48'),(4,'AMS-2026-0004','Alghanim International','Sheet Metal Fitter','Engineering','1-2 Years','UAE','Free Food • Free Accommodation • Salary: 1200 AED','Active',2,'2026-07-21 09:10:53');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `testimonials`
--

DROP TABLE IF EXISTS `testimonials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `testimonials` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(150) NOT NULL,
  `designation` varchar(150) NOT NULL,
  `message` text NOT NULL,
  `photo` varchar(255) NOT NULL,
  `status` enum('Active','Inactive') DEFAULT 'Active',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `testimonials`
--

LOCK TABLES `testimonials` WRITE;
/*!40000 ALTER TABLE `testimonials` DISABLE KEYS */;
INSERT INTO `testimonials` VALUES (1,'John Smith','HR Manager','Outstanding recruitment service. Highly professional and reliable team.','0f7776ab85464fd699e4b56be8846178.jpg','Active','2026-07-25 06:05:32'),(2,'Sarah Williams','Operations Head','They helped us hire top-quality candidates in record time.','e5d92e48df934ddfbae0ea7e868dbd25.jpg','Active','2026-07-25 06:07:35'),(4,'David Brown','CEO','Excellent communication and seamless hiring process.','a722f2cd00014973b60daa2de9a5d21c.jpg','Active','2026-07-25 06:48:23');
/*!40000 ALTER TABLE `testimonials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-30 13:17:27
