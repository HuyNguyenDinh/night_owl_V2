CREATE USER IF NOT EXISTS 'night_owl'@'localhost' IDENTIFIED BY 'nightowl';
ALTER USER 'night_owl'@'localhost' IDENTIFIED BY 'nightowl';
CREATE DATABASE IF NOT EXISTS night_owl;
GRANT ALL PRIVILEGES ON *.* TO 'night_owl'@'localhost';
FLUSH PRIVILEGES;