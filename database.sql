CREATE TABLE `items` (
	`id` INTEGER PRIMARY KEY,
	`name` VARCHAR(20),
	`item_id` VARCHAR(20),
	`location` VARCHAR(20),
	`date` DATETIME(20)
);

CREATE TABLE `users` (
	`id` INTEGER PRIMARY KEY,
	`firstname` VARCHAR(20),
	'lastname' VARCHAR(20),
	`email` VARCHAR(50),
	`password` VARCHAR(20),
	`date` DATETIME(20)
);

CREATE TABLE `unclassified`(
	`id` INTEGER PRIMARY KEY,
	`name` VARCHAR(20),
	`item_id` VARCHAR(20),
	`date` DATETIME(20)
);

CREATE TABLE `notifications`(
	`id` INTEGER PRIMARY KEY,
	`content` VARCHAR(50),
	`date` DATETIME(20)
);