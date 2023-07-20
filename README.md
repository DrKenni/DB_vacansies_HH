# Курсовая 5. Работа с базами данных
В рамках проекта необходимо получить данные о компаниях и вакансиях с сайта [hh.ru](http://hh.ru/), спроектировать 
таблицы в БД ***PostgreSQL*** и загрузить полученные данные в созданные таблицы.

---
## Старт проекта
- Сперва нужно прописать данные для подключения к БД (файл database.ini). 
- Запуск проекта осуществляется через файл main.py. 
- Для начала нужно создать базу данных, указав её название. 
- Далее нужно выбрать из меню команду, которая выдаст результат.

---
## Класс ParserHH
Класс основан на публичном API [hh.ru](http://hh.ru/). Данные получает с помощью библиотеки ***requests***.

### Имеет следующие методы:
- `get_employers()`: Берет список компаний с публичного API.
- `get_vacancies()`: Берет список вакансий с публичного API, на основе списка компаний.


## Класс DBManager
Класс подключается Postgres, создает базу данных и таблицы для занесения в них информации с сайта 
[hh.ru](http://hh.ru/). Использует библиотеку ***psycopg2*** для работы с БД. 

### Имеет следующие методы:

#### Основные методы

- `create_db()`: Подключается и создает базу данных в Postgres.
- `create_tables()`: Создает таблицы с работодателями и вакансиями.
- `insert_data()`: Заполняет таблицы с работодателями и вакансиями.

#### Методы для работы с пользователем



- `get_companies_and_vacancies_count()`: получает список всех компаний и количество вакансий у каждой компании.
- `get_all_vacancies()`: получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты
и ссылки на вакансию.
- `get_avg_salary()`: получает среднюю зарплату по вакансиям.
- `get_vacancies_with_higher_salary()`: получает список всех вакансий, у которых зарплата выше средней по всем 
вакансиям.
- `get_vacancies_with_keyword()`: получает список всех вакансий, в названии которых содержатся переданные в 
метод слова, например “python”.

