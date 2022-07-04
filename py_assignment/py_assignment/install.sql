CREATE TABLE IF NOT EXISTS `hall` (
	`id_hall` int(11) AUTO_INCREMENT PRIMARY KEY,
	`name` varchar(500) NOT NULL,
	`capacity` int(11) NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=100;

CREATE TABLE IF NOT EXISTS `professor` (
	`id_professor` int(11) AUTO_INCREMENT PRIMARY KEY,
	`name` varchar(500) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=100;

CREATE TABLE IF NOT EXISTS `hall_available` (
	`id_hall_available` int(11) AUTO_INCREMENT PRIMARY KEY,
	`id_hall` int(11) NOT NULL,
    `id_professor` int(11) NOT NULL,
    `time_start` timestamp NOT NULL,
    `time_end` timestamp NOT NULL,
    `state` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=100;