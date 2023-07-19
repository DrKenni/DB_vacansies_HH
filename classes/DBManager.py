import psycopg2
import pandas


class DBManager:
    def __init__(self, params, name_db):
        self.params = params
        self.name_db = name_db
        pandas.set_option('display.max_columns', None)
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_colwidth', None)
        pandas.options.display.expand_frame_repr = False

    def create_db(self) -> None:
        """Создает базу данных"""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {self.name_db}")
        cur.execute(f"CREATE DATABASE {self.name_db}")
        conn.close()
        print(f"База данных {self.name_db} успешно создана.")

    def create_tables(self) -> None:
        """Создает таблицы"""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""CREATE TABLE employers(
                       employer_id SERIAL PRIMARY KEY,
                       company_name VARCHAR(150)
                    )""")
        cur.execute("""CREATE TABLE vacancies (
                       vacancy_id SERIAL PRIMARY KEY,
                       employer_id INT REFERENCES employers (employer_id),
                       vacancy_name VARCHAR(100) NOT NULL,
                       url VARCHAR(100) NOT NULL,
                       salary_from INT,
                       salary_to INT
                    )""")
        conn.close()
        print(f"Создание таблиц прошло успешно.")

    def insert_data(self, name_table, data):
        """Заполняет созданные таблицы"""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)

        try:
            with conn:
                with conn.cursor() as cursor:
                    col_count = "".join("%s," * len(data[0]))
                    query = f"INSERT INTO {name_table} VALUES ({col_count[:-1]})"
                    cursor.executemany(query, data)
                    conn.commit()
                    print(f"Таблица {name_table} заполнена успешно.")
        except psycopg2.Error as er:
            print(f"Ошибка с запросом.\n{er}")
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, COUNT(vacancy_name) as vacancies FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.employer_id
            GROUP BY company_name
        """)
        res = cur.fetchall()
        df = pandas.DataFrame(res, columns=['Название компании', 'Число вакансий'])
        print(df)
        print('-' * 100)
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT company_name, vacancy_name, salary_from, salary_to, url FROM vacancies
            INNER JOIN employers ON vacancies.employer_id = employers.employer_id
        """)
        res = cur.fetchall()
        df = pandas.DataFrame(res, columns=['Компания', 'Вакансия', 'ЗП от', 'ЗП до', 'Страница на HH.ru'])
        print(df)
        print('-' * 100)
        conn.close()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT COUNT(vacancy_id), AVG(salary_from)::numeric(10,0) as avg_salary 
            FROM vacancies
        """)
        res = cur.fetchall()
        df = pandas.DataFrame(res, columns=['Количество вакансий', 'Средняя зарплата'])
        print(df)
        print('-' * 100)
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        cur = conn.cursor()
        cur.execute("""
            SELECT vacancy_name, salary_from FROM vacancies
            WHERE salary_from <> 0 AND salary_from > (SELECT AVG(salary_from) FROM vacancies)
            ORDER BY salary_from DESC
        """)
        res = cur.fetchall()
        df = pandas.DataFrame(res, columns=['Вакансия(ЗП выше среднего)', 'Зарплата'])
        print(df)
        print('-' * 100)
        conn.close()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова,
         например “python”."""
        conn = psycopg2.connect(dbname=self.name_db, **self.params)
        cur = conn.cursor()
        cur.execute(f"""
            SELECT vacancy_name, salary_from, url FROM vacancies
            WHERE vacancy_name LIKE '%{keyword}%'
        """)
        res = cur.fetchall()
        if len(res) != 0:
            df = pandas.DataFrame(res, columns=['Вакансия', 'Зарплата', 'Страница на HH.ru'])
            print(df)
        else:
            print('Результатов не найдено!')
        print('-' * 100)
        conn.close()
