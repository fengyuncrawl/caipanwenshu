-- caipan.sql

drop database if exists `caipan`;

create database `caipan`;

use `caipan`;

drop table if exists `panjueshu`;

create table panjueshu (
    `id` int(10) not null auto_increment,
    `name` varchar(200),
    `cause` varchar(200),
	`docid` varchar(100) not null,
    `area` varchar(200),
    `proced` varchar(200),
    `types` varchar(50),
    `num` varchar(100),
	`court` varchar(100),
	`dates` varchar(50),
	`yiju` text,
	`content` longtext,
	`url` varchar(100),
    primary key (`id`)
) engine=innodb default charset=utf8;
