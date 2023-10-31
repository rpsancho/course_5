-- CREATE TABLE employers

CREATE TABLE employers
(
	employer_id smallint PRIMARY KEY NOT NULL,
	hh_id int NOT NULL,
	alternate_url varchar(100) NOT NULL,
	name varchar(50) NOT NULL,
	open_vacancies int NOT NULL,
	vacancies_url varchar(100) NOT NULL
);

CREATE TABLE vacancies
(
	vacancy_id smallint PRIMARY KEY NOT NULL,
	employer_id smallint REFERENCES employers(employer_id) NOT NULL,
	hh_id int NOT NULL,
	name varchar(50) NOT NULL,
	alternate_url varchar(100) NOT NULL,
	salary_from varchar(20) NOT NULL,
	responsibility varchar(100) NOT NULL,
	requirement varchar(100) NOT NULL
);