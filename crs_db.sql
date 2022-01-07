-- DROP DATABASE IF EXISTS CRS;

-- CREATE DATABASE CRS;

DROP TABLE IF EXISTS student;

CREATE TABLE student (
    student_id BIGINT PRIMARY KEY,
    student_name VARCHAR ( 100 ) UNIQUE NOT NULL,
    student_email VARCHAR ( 255 ) UNIQUE NOT NULL
);

DROP TABLE IF EXISTS prof;

CREATE TABLE prof(
    prof_id VARCHAR (50) PRIMARY KEY,
    prof_name VARCHAR (100) NOT NULL
);

DROP TABLE IF EXISTS course;

CREATE TABLE course(
    course_id VARCHAR (50) PRIMARY KEY,
    course_name VARCHAR( 100 ) NOT NULL,
    course_cap INT NOT NULL,
    course_slot TIME NOT NULL,
    course_day INT NOT NULL,
    is_open_type INT,
    is_math_type INT,
    is_science_type INT,
    is_hum_type INT,
    prof_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (prof_id) REFERENCES prof (prof_id)
);

DROP TABLE IF EXISTS cr_approved;

CREATE TABLE cr_approved(
  student_id BIGINT NOT NULL,
  course_id VARCHAR (50) NOT NULL,
  as_type VARCHAR (20),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES student (student_id),
  FOREIGN KEY (course_id) REFERENCES course (course_id)
);

DROP TABLE IF EXISTS all_course_data;

CREATE TABLE all_course_data(
    student_id BIGINT NOT NULL,
    course_id VARCHAR (50) NOT NULL,
    as_type VARCHAR (20),
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student (student_id),
    FOREIGN KEY (course_id) REFERENCES course (course_id)
); 