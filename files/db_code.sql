CREATE TABLE employers(
employer_id SERIAL PRIMARY KEY,
company_name VARCHAR(150));

CREATE TABLE vacancies (
vacancy_id SERIAL PRIMARY KEY,
employer_id INT REFERENCES employers (employer_id),
vacancy_name VARCHAR(100) NOT NULL,
url VARCHAR(100) NOT NULL,
salary_from INT,
salary_to INT);

