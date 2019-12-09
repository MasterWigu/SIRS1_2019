drop database if exists AVD_SCORE;

create database AVD_SCORE;
use AVD_SCORE;

drop table if exists user cascade;
drop table if exists attack cascade;


create table user(
	username varchar(255) not null unique,
    password varchar(255) not null,
    permissions int not null default 1,
    points int not null default 0,
    constraint pk_user primary key(username)
);


create table attack(
	fingerprint varchar(500) not null,
    explanation varchar(500) not null,
    submit_time timestamp not null,
    username varchar(255) not null,
    constraint pk_attack primary key(fingerprint, username),
    constraint fk_attack foreign key(username) references user(username)
);

INSERT INTO user VALUES ('admin', '$2y$10$ciyHnA1quHJoYPRMk5jQ4eSa9OWfGg2.jfyKla2Zp7nQ2zXu1Ukxe', 0, 0);