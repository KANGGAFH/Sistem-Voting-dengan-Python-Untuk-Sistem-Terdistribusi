CREATE DATABASE voting_db;
USE voting_db;

CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'voter') NOT NULL DEFAULT 'voter',
    has_voted TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE elections (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    active TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE candidates (
    id INT(11) NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    election_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (election_id) REFERENCES elections(id) ON DELETE CASCADE
);

CREATE TABLE votes (
    id INT(11) NOT NULL AUTO_INCREMENT,
    voter_id INT(11) NOT NULL,
    candidate_id INT(11) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (voter_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE
);
