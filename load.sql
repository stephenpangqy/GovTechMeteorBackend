DROP DATABASE IF EXISTS household_grant;
CREATE DATABASE household_grant;
USE household_grant;

DROP TABLE IF EXISTS household;
CREATE TABLE household(
    unit_no varchar(10) not null,
    housing_type varchar(50) not null,
    primary key(unit_no)
    
);

DROP TABLE IF EXISTS family_member;
CREATE TABLE family_member(
	name varchar(50) not null,
    gender char(1) not null,
    marital_status varchar(30) not null,
    spouse_name varchar(50) not null,
    occupation_type varchar(20) not null, # Unemployed, Student or Employed
    annual_income int not null,
    date_of_birth varchar(30) not null,
    unit_no varchar(10) not null,
    primary key(name, spouse_name),
    constraint fk1 foreign key(unit_no) references household(unit_no)
    
    
);

DROP TABLE IF EXISTS grant_schemes;
CREATE TABLE grant_schemes(
	grant_name varchar(100) not null,
    criteria varchar(200) not null,
	qualifying_members varchar(200) not null,
    primary key(grant_name)
);

INSERT INTO household VALUES ("2A","Condominium");
INSERT INTO household VALUES ("272","HDB");
INSERT INTO household VALUES ("274","HDB");
INSERT INTO household VALUES ("5","Landed");
INSERT INTO family_member VALUES ("Dana Lee", "F", "Married", "Don Lee", "Employed", 80000, "1980-07-18","2A");
INSERT INTO family_member VALUES ("Don Lee", "M", "Married", "Dana Lee", "Employed", 120000, "1972-05-12","2A");
INSERT INTO family_member VALUES ("Jerica Leona", "F", "Single", "", "Student", 0, "1998-02-03","2A");
INSERT INTO family_member VALUES ("Kyla", "F", "Single", "", "Student", 0, "2005-04-02","2A");
INSERT INTO family_member VALUES ("Bryan Tan", "M", "Married", "Mora Low", "Employed", 70000, "1982-05-02","272");
INSERT INTO family_member VALUES ("Mora Low", "F", "Married", "Bryan Tan", "Unemployed", 0, "1986-06-11","272");
INSERT INTO family_member VALUES ("Mieka Tan", "F", "Married", "Justin Tan", "Unemployed", 0, "1945-06-11","272");
INSERT INTO family_member VALUES ("Justin Tan", "M", "Married", "Mieka Tan", "Unemployed", 0, "1936-02-21","272");
INSERT INTO family_member VALUES ("Baby Tan", "F", "Single", "", "Unemployed", 0, "2022-09-10","272");
INSERT INTO family_member VALUES ("Sarah May", "F", "Single", "", "Employed", 65000, "1991-11-12","274");
INSERT INTO family_member VALUES ("Koh Ee Qing", "F", "Married", "Chan Yi Hao", "Employed", 72000, "1982-11-12","5");
INSERT INTO family_member VALUES ("Chan Yi Hao", "M", "Married", "Koh Ee Qing", "Employed", 53000, "1973-05-12","5");


INSERT INTO grant_schemes VALUES ("Student Encouragement Bonus","MEMBER_AGE<16,TOTAL_INCOME<200000","AGE<16");
INSERT INTO grant_schemes VALUES ("Multigeneration Scheme","MEMBER_AGE<18,MEMBER_AGE>55,TOTAL_INCOME<150000","ALL");
INSERT INTO grant_schemes VALUES ("Elder Bonus", "MEMBER_AGE>55","AGE>=55");
INSERT INTO grant_schemes VALUES ("Baby Sunshine Grant", "MEMBER_AGE<0.7","AGE<0.7");
INSERT INTO grant_schemes VALUES ("YOLO GST Grant", "TOTAL_INCOME<100000","ALL");