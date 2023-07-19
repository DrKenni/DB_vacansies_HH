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

SELECT company_name, COUNT(vacancy_name) as vacancies FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id
GROUP BY company_name;

SELECT company_name, vacancy_name, salary_from, salary_to, url
FROM vacancies
INNER JOIN employers ON vacancies.employer_id = employers.employer_id;

SELECT COUNT(vacancy_id), AVG(salary_from)::numeric(10,0) as avg_salary
FROM vacancies;

SELECT vacancy_name, salary_from FROM vacancies
WHERE salary_from <> 0 AND salary_from > (SELECT AVG(salary_from)
FROM vacancies)
ORDER BY salary_from DESC;

SELECT vacancy_name, salary_from, url
FROM vacancies
WHERE vacancy_name LIKE '%python%';