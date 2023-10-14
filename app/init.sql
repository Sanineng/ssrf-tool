ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';

CREATE DATABASE IF NOT EXISTS `users`;

USE `users`;
CREATE TABLE user(
  idx int auto_increment primary key,
  uid varchar(128) not null,
  upw varchar(128) not null
);

INSERT INTO user(uid, upw) values('test_account', '969c001e294ae93faaf6ee4dad18fd03');
FLUSH PRIVILEGES;