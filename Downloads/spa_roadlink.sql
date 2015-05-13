-- phpMyAdmin SQL Dump
-- version 4.2.6deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 13, 2015 at 12:06 PM
-- Server version: 10.0.19-MariaDB-1~utopic-log
-- PHP Version: 5.5.12-2ubuntu4.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mesh`
--

-- --------------------------------------------------------

--
-- Table structure for table `spa_roadlink`
--

CREATE TABLE IF NOT EXISTS `spa_roadlink` (
`ID` int(11) NOT NULL,
  `fictitious` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `identifier` varchar(38) COLLATE utf8_unicode_ci DEFAULT NULL,
  `class` varchar(22) COLLATE utf8_unicode_ci DEFAULT NULL,
  `roadNumber` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name1` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name1_lang` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name2` varchar(150) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name2_lang` varchar(3) COLLATE utf8_unicode_ci DEFAULT NULL,
  `formOfWay` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `strategic` varchar(7) COLLATE utf8_unicode_ci DEFAULT NULL,
  `length` float DEFAULT NULL,
  `structure` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `loop` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `startNode` varchar(38) COLLATE utf8_unicode_ci DEFAULT NULL,
  `endNode` varchar(38) COLLATE utf8_unicode_ci DEFAULT NULL,
  `formsPart` varchar(41) COLLATE utf8_unicode_ci DEFAULT NULL,
  `GEOMETRY` linestring NOT NULL
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=3181443 ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `spa_roadlink`
--
ALTER TABLE `spa_roadlink`
 ADD PRIMARY KEY (`ID`), ADD SPATIAL KEY `GEOMETRY` (`GEOMETRY`), ADD KEY `name1` (`name1`), ADD KEY `formsPart` (`formsPart`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `spa_roadlink`
--
ALTER TABLE `spa_roadlink`
MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3181443;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
