create database internship;
\c internship;

create table users(
id serial NOT NULL PRIMARY KEY,
username text,
password text,
firstname text,
lastname text,
email text 
);

create table internships(
id serial NOT NULL PRIMARY KEY,
title text,
address text,
description text
);

create table reviews(
id serial NOT NULL PRIMARY KEY,
reviewer text,
review text,
status int, 
email text,
inernship_id int references inernships(id),
q1 text,
q2 text,
q3 text,
q4 text,
q5 boolean,
q6 boolean
);



INSERT INTO users VALUES (1,'ik','123','imad','kassim','ik@gmail.com');
INSERT INTO users VALUES (2,'mk','456','mo','alg','ma@yahoo.com');

INSERT INTO inernships VALUES (1,'ibm dv','31 perth','full-time');
INSERT INTO inernships VALUES (2,'google','918 gerarrd','part-time');